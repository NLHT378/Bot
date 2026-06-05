import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import datetime
import os

# ==========================================
# CẤU HÌNH BOT
# ==========================================
class AndroidZoneBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f'✅ Bot {self.user.name} đã sẵn sàng!')

bot = AndroidZoneBot()
ALLOWED_ROLES = ["Owner", "Admin", "Moderator"]

# ==========================================
# GIAO DIỆN KIỂM DUYỆT
# ==========================================
class QuickModView(discord.ui.View):
    def __init__(self, target_member: discord.Member, reason: str):
        super().__init__(timeout=None)
        self.target_member = target_member
        self.reason = reason

    @discord.ui.button(label="Mute 10m", style=discord.ButtonStyle.secondary, emoji="🔇")
    async def btn_mute_10m(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.target_member.timeout(datetime.timedelta(minutes=10), reason=self.reason)
        await interaction.response.send_message(f"✅ {self.target_member.display_name} has been muted.", ephemeral=True)

    @discord.ui.button(label="BAN", style=discord.ButtonStyle.danger, emoji="🔨")
    async def btn_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.target_member.ban(reason=self.reason)
        await interaction.response.send_message(f"🚨 {self.target_member.display_name} has been banned.", ephemeral=True)

# ==========================================
# CÁC SỰ KIỆN TỰ ĐỘNG
# ==========================================
@bot.event
async def on_ready():
    # Tự động khởi chạy web server giữ thức nếu có file web_server.py
    try:
        from web_server import keep_alive
        keep_alive()
    except ImportError:
        pass
    print(f'✅ Bot {bot.user.name} đã kết nối thành công!')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    if role: await member.add_roles(role)
    channel = discord.utils.find(lambda c: 'welcome' in c.name.lower(), member.guild.text_channels)
    if channel: await channel.send(f"🎉 Welcome {member.mention} to **{member.guild.name}**!")

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.name == "❓-help-desk":
        await message.create_thread(name=f"💬 {message.author.name}: Help Request", auto_archive_duration=10080)
    await bot.process_commands(message)

# ==========================================
# LỆNH SLASH (/)
# ==========================================
@bot.tree.command(name="setup", description="🔄 Thiết lập cộng đồng Android Zone")
@app_commands.default_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Đang thiết lập...", ephemeral=True)
    guild = interaction.guild
    for r in ["Owner", "Admin", "Moderator", "VIP", "Member"]:
        if not discord.utils.get(guild.roles, name=r): await guild.create_role(name=r, hoist=True)
    cat = discord.utils.get(guild.categories, name="🛠️ ANDROID ZONE") or await guild.create_category("🛠️ ANDROID ZONE")
    if not discord.utils.get(guild.text_channels, name="📦-app-sharing"): await guild.create_text_channel("📦-app-sharing", category=cat)
    if not discord.utils.get(guild.forums, name="🤝-community-forum"): await guild.create_forum(name="🤝-community-forum", category=cat)
    await interaction.edit_original_response(content="✅ Setup hoàn tất!")

@bot.tree.command(name="warn", description="⚠️ Cảnh báo thành viên")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message(f"⚠️ Cảnh báo {member.mention}: {reason}", view=QuickModView(member, reason))

@bot.tree.command(name="clear", description="🧹 Xóa tin nhắn")
async def clear(interaction: discord.Interaction, amount: int):
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"✅ Đã xóa {len(deleted)} tin nhắn.", ephemeral=True)

# DÁN TOKEN MỚI VÀO ĐÂY (DÒNG CUỐI CÙNG)
import os
# Đọc token từ biến môi trường của hệ thống
token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
