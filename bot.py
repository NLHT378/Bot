import discord
from discord.ext import commands
from discord import app_commands
import os
from web_server import keep_alive

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.keep_channels = True # Mặc định là BẬT (Giữ kênh cũ)

    @discord.ui.select(placeholder="Chọn cấu hình server...", options=[
        discord.SelectOption(label="Community", description="Diễn đàn, chia sẻ, hỗ trợ", emoji="🤝"),
        discord.SelectOption(label="Gaming", description="Đầy đủ kênh game, voice, role màu", emoji="🎮"),
        discord.SelectOption(label="Business", description="Bán hàng, sản phẩm, đánh giá, liên hệ", emoji="💰")
    ])
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]
        guild = interaction.guild
        
        await interaction.response.send_message(f"🔄 Đang tiến hành cài đặt cấu hình **{choice}**...", ephemeral=True)

        # --- LOGIC XÓA KÊNH CŨ (Nếu nhấn nút TẮT) ---
        if not self.keep_channels:
            # Bot sẽ tìm và xóa các danh mục cũ do nó tạo ra để làm mới
            categories_to_delete = ["🛠️ CỘNG ĐỒNG ANDROID", "🎮 GAMING ZONE", "🛒 KINH DOANH - BÁN HÀNG"]
            for cat_name in categories_to_delete:
                cat = discord.utils.get(guild.categories, name=cat_name)
                if cat:
                    for channel in cat.channels:
                        await channel.delete()
                    await cat.delete()

        # --- TẠO KÊNH MỚI THEO LỰA CHỌN ---
        if choice == "Community":
            cat = await guild.create_category("🛠️ CỘNG ĐỒNG ANDROID")
            await guild.create_text_channel("💬-chat-chung", category=cat)
            await guild.create_text_channel("📦-app-sharing", category=cat)
            await guild.create_text_channel("📸-goc-khoe-may", category=cat)
            await guild.create_forum(name="❓-help-desk", category=cat)

        elif choice == "Gaming":
            cat = await guild.create_category("🎮 GAMING ZONE")
            await guild.create_text_channel("📢-thong-bao-game", category=cat)
            await guild.create_text_channel("💬-chat-game", category=cat)
            await guild.create_text_channel("🎨-chon-mau-role", category=cat)
            await guild.create_text_channel("🔍-tim-ban-choi", category=cat)
            await guild.create_voice_channel("🔊 Phòng Đội 1", category=cat)
            await guild.create_voice_channel("🔊 Phòng Đội 2", category=cat)

        elif choice == "Business":
            cat = await guild.create_category("🛒 KINH DOANH - BÁN HÀNG")
            await guild.create_text_channel("📢-thong-bao-shop", category=cat)
            await guild.create_text_channel("📦-san-pham", category=cat)
            await guild.create_text_channel("⭐-danh-gia-khach-hang", category=cat)
            await guild.create_text_channel("💬-lien-he-mua-hang", category=cat)
            await guild.create_text_channel("💸-thanh-toan", category=cat)

        await interaction.edit_original_response(content=f"✅ Đã hoàn tất cài đặt cấu hình **{choice}**!")

    # Nút Bật/Tắt tính năng giữ kênh cũ
    @discord.ui.button(label="Giữ kênh cũ: BẬT", style=discord.ButtonStyle.green)
    async def toggle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.keep_channels = not self.keep_channels
        button.label = f"Giữ kênh cũ: {'BẬT' if self.keep_channels else 'TẮT'}"
        button.style = discord.ButtonStyle.green if self.keep_channels else discord.ButtonStyle.danger
        await interaction.response.edit_message(view=self)

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

# --- SỰ KIỆN TỰ ĐỘNG ---
@bot.event
async def on_ready():
    keep_alive() 
    print(f'✅ Bot {bot.user.name} đã sẵn sàng!')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    if role: await member.add_roles(role)

# --- CÁC LỆNH SLASH (/) ---
@bot.tree.command(name="setup", description="🔄 Mở menu cài đặt cấu trúc server")
@app_commands.default_permissions(administrator=True)
async def setup_command(interaction: discord.Interaction):
    await interaction.response.send_message("⚙️ **Cài đặt Server**\nHãy chọn Bật/Tắt giữ kênh cũ, sau đó chọn cấu hình bạn muốn:", view=SetupView())

@bot.tree.command(name="say", description="📢 Bot nhắn nội dung bạn muốn vào kênh hiện tại")
@app_commands.default_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, content: str):
    await interaction.channel.send(content)
    await interaction.response.send_message("✅ Đã gửi!", ephemeral=True)

@bot.tree.command(name="clear", description="🧹 Xóa tin nhắn")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"✅ Đã xóa {len(deleted)} tin nhắn.", ephemeral=True)

@bot.tree.command(name="warn", description="⚠️ Cảnh báo thành viên")
@app_commands.default_permissions(manage_messages=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message(f"⚠️ {member.mention} đã bị cảnh báo với lý do: **{reason}**")

# Khởi chạy bot
bot.run(os.environ.get('DISCORD_TOKEN'))
