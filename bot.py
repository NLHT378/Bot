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

# --- Sự kiện ---
@bot.event
async def on_ready():
    keep_alive() 
    print(f'✅ Bot {bot.user.name} đã sẵn sàng!')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    if role: await member.add_roles(role)
    channel = discord.utils.find(lambda c: 'welcome' in c.name.lower(), member.guild.text_channels)
    if channel: await channel.send(f"🎉 Chào mừng {member.mention} đến với **{member.guild.name}**!")

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.name == "❓-help-desk":
        await message.create_thread(name=f"💬 {message.author.name}: Help Request", auto_archive_duration=10080)
    await bot.process_commands(message)

# --- Các lệnh Slash (/) ---
@bot.tree.command(name="setup", description="🔄 Thiết lập toàn bộ cấu trúc Android Zone")
@app_commands.default_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Đang thiết lập...", ephemeral=True)
    guild = interaction.guild
    for r in ["Owner", "Admin", "Moderator", "Member"]:
        if not discord.utils.get(guild.roles, name=r): await guild.create_role(name=r, hoist=True)
    cat = await guild.create_category("🛠️ ANDROID ZONE")
    await guild.create_text_channel("📦-app-sharing", category=cat)
    await guild.create_forum(name="🤝-community-forum", category=cat)
    await interaction.edit_original_response(content="✅ Setup hoàn tất!")

@bot.tree.command(name="say", description="📢 Bot nhắn nội dung bạn muốn vào kênh hiện tại")
@app_commands.default_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, content: str):
    # Bot nhắn nội dung vào kênh người dùng đang chat
    await interaction.channel.send(content)
    # Phản hồi ẩn để xác nhận
    await interaction.response.send_message("✅ Đã gửi!", ephemeral=True)

@bot.tree.command(name="clear", description="🧹 Xóa tin nhắn")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"✅ Đã xóa {len(deleted)} tin nhắn.", ephemeral=True)

@bot.tree.command(name="warn", description="⚠️ Cảnh báo thành viên")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message(f"⚠️ Cảnh báo {member.mention}: {reason}")

# Chạy Bot
bot.run(os.environ.get('DISCORD_TOKEN'))
