import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime
from web_server import keep_alive

class AndroidZoneBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f'✅ Đã đồng bộ Slash Commands!')

bot = AndroidZoneBot()

# --- MENU SETUP ---
class SetupView(discord.ui.View):
    @discord.ui.select(placeholder="Chọn cấu hình server...", options=[
        discord.SelectOption(label="Community", description="Diễn đàn, chia sẻ, hỗ trợ", emoji="🤝"),
        discord.SelectOption(label="Gaming", description="Thông báo, role màu, voice chat", emoji="🎮"),
        discord.SelectOption(label="Business", description="Bán hàng, liên hệ, quản lý đơn", emoji="💰")
    ])
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]
        await interaction.response.send_message(f"🔄 Đang xây dựng cấu hình {choice}...", ephemeral=True)
        guild = interaction.guild

        if choice == "Community":
            cat = await guild.create_category("🛠️ ANDROID ZONE")
            await guild.create_text_channel("📦-app-sharing", category=cat)
            await guild.create_forum(name="🤝-community-forum", category=cat)
        elif choice == "Gaming":
            cat = await guild.create_category("🎮 GAMING ZONE")
            await guild.create_text_channel("📢-thong-bao-game", category=cat)
            await guild.create_text_channel("🎨-chon-mau-role", category=cat)
        elif choice == "Business":
            cat = await guild.create_category("🛒 BUSINESS")
            await guild.create_text_channel("📦-san-pham", category=cat)
            await guild.create_text_channel("💬-lien-he-mua-hang", category=cat)

        await interaction.edit_original_response(content=f"✅ Hoàn tất cấu hình {choice}! Các kênh cũ được giữ nguyên.")

# --- SỰ KIỆN ---
@bot.event
async def on_ready():
    keep_alive()
    print(f'✅ Bot {bot.user.name} đã sẵn sàng!')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    if role: await member.add_roles(role)

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.name == "❓-help-desk":
        await message.create_thread(name=f"💬 {message.author.name}: Help", auto_archive_duration=10080)
    await bot.process_commands(message)

# --- CÁC LỆNH SLASH ---
@bot.tree.command(name="setup", description="🔄 Mở menu cài đặt server")
@app_commands.default_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.send_message("Chọn kiểu cấu hình bạn muốn:", view=SetupView())

@bot.tree.command(name="say", description="📢 Bot nhắn nội dung vào kênh hiện tại")
@app_commands.default_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, content: str):
    await interaction.channel.send(content)
    await interaction.response.send_message("✅ Đã gửi!", ephemeral=True)

@bot.tree.command(name="clear", description="🧹 Xóa tin nhắn")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"✅ Đã xóa {deleted} tin nhắn.", ephemeral=True)

@bot.tree.command(name="warn", description="⚠️ Cảnh báo thành viên")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message(f"⚠️ {member.mention} đã bị cảnh báo: {reason}")

bot.run(os.environ.get('DISCORD_TOKEN'))
