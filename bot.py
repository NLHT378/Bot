import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from web_server import keep_alive

# ==========================================
# CẤU TRÚC SERVER MẪU
# ==========================================
TEMPLATES = {
    "Streamer": {
        "VN": {
            "roles": ["👑 Chủ Server", "🛡️ Quản Lý", "🔨 Kiểm Duyệt", "🎬 Editor", "🌟 Đăng Ký", "💬 Thành Viên Tích Cực", "👤 Thành Viên", "👀 Tàu Ngầm"],
            "categories": {
                "📌 THÔNG TIN": [("text", "luật-lệ"), ("text", "thông-báo"), ("text", "hướng-dẫn")],
                "🔴 LIVE & NỘI DUNG": [("text", "thông-báo-stream"), ("text", "clips"), ("text", "vods")],
                "🌍 CỘNG ĐỒNG": [("text", "chào-mừng"), ("text", "chat-chung"), ("text", "chơi-game")],
                "🔊 KÊNH GIỌNG NÓI": [("voice", "Phòng Chờ"), ("voice", "Phòng Game")]
            },
            "welcome": {"channel": "luật-lệ", "title": "🎉 Chào mừng đến với Server!", "desc": "Vui lòng đọc kỹ luật trước khi chat. Hãy giới thiệu bản thân ở kênh chat chung nhé!"}
        },
        "EN": {
            "roles": ["Owner", "Manager", "Moderator", "Editor", "Subscriber", "Active Member", "Member", "Lurker"],
            "categories": {
                "📌 INFORMATION": [("text", "rules"), ("text", "announcements"), ("text", "guide")],
                "🔴 LIVE & CONTENT": [("text", "stream-alerts"), ("text", "clips"), ("text", "vods")],
                "🌍 COMMUNITY": [("text", "welcome"), ("text", "general"), ("text", "gaming")],
                "🔊 VOICE CHANNELS": [("voice", "Lounge"), ("voice", "Gaming")]
            },
            "welcome": {"channel": "rules", "title": "🎉 Welcome to the Server!", "desc": "Please read the rules before chatting. Introduce yourself in the general channel!"}
        }
    },
    "Business": {
        "VN": {
            "roles": ["CEO", "Quản Lý Shop", "Nhân Viên Hỗ Trợ", "Khách VIP", "Khách Hàng"],
            "categories": {
                "🛒 CỬA HÀNG": [("text", "thông-báo-shop"), ("text", "sản-phẩm")],
                "💬 KHÁCH HÀNG": [("text", "chat-chung"), ("text", "đánh-giá"), ("text", "hỗ-trợ")],
                "📞 CSKH": [("voice", "Phòng Chờ"), ("voice", "Bảo Hành")]
            },
            "welcome": {"channel": "thông-báo-shop", "title": "🛒 Chào mừng quý khách!", "desc": "Cảm ơn bạn đã ghé thăm shop!"}
        }
    }
}

# ==========================================
# BƯỚC 2: MENU CHỌN MẪU & KHỞI CHẠY
# ==========================================
class AdvancedSetupView(discord.ui.View):
    def __init__(self, server_name: str, accent_color: discord.Color):
        super().__init__(timeout=300)
        self.server_name = server_name
        self.accent_color = accent_color
        self.selected_lang = "VN"
        self.selected_template = "Streamer"
        self.keep_channels = True

    @discord.ui.select(placeholder="🌐 Chọn Ngôn Ngữ / Language", options=[
        discord.SelectOption(label="Tiếng Việt (VN)", value="VN", emoji="🇻🇳", default=True),
        discord.SelectOption(label="English (EN)", value="EN", emoji="🇺🇸")
    ], row=0)
    async def lang_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_lang = select.values[0]
        for opt in select.options: opt.default = (opt.value == self.selected_lang)
        await interaction.response.edit_message(view=self)

    @discord.ui.select(placeholder="🏗️ Chọn cấu trúc Server...", options=[
        discord.SelectOption(label="Streamer / Creator", value="Streamer", emoji="🎥", default=True),
        discord.SelectOption(label="Business / Shop", value="Business", emoji="🛒")
    ], row=1)
    async def template_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_template = select.values[0]
        for opt in select.options: opt.default = (opt.value == self.selected_template)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Giữ Kênh Cũ: BẬT", style=discord.ButtonStyle.green, row=2)
    async def toggle_keep(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.keep_channels = not self.keep_channels
        button.label = "Giữ Kênh Cũ: BẬT" if self.keep_channels else "XÓA SẠCH KÊNH CŨ: BẬT"
        button.style = discord.ButtonStyle.green if self.keep_channels else discord.ButtonStyle.danger
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="🚀 TIẾN HÀNH XÂY DỰNG", style=discord.ButtonStyle.blurple, row=2)
    async def start_setup(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"⏳ Đang xây dựng **{self.server_name}**...\n*Vui lòng đợi khoảng 10 giây!*", ephemeral=True)
        guild = interaction.guild
        
        # Đổi tên Server theo ý người dùng
        try: await guild.edit(name=self.server_name)
        except: pass

        data = TEMPLATES.get(self.selected_template, TEMPLATES["Streamer"]).get(self.selected_lang, TEMPLATES["Streamer"]["VN"])

        # XÓA TRIỆT ĐỂ (Nuclear Wipe)
        if not self.keep_channels:
            for channel in guild.channels:
                try: await channel.delete()
                except: pass
            for role in guild.roles:
                if role.name != "@everyone" and not role.managed:
                    try: await role.delete()
                    except: pass
            await asyncio.sleep(2)

        # TẠO ROLE + ÁP DỤNG MÀU SẮC
        for role_name in reversed(data["roles"]):
            if not discord.utils.get(guild.roles, name=role_name):
                try: await guild.create_role(name=role_name, hoist=True, color=self.accent_color)
                except: pass

        # TẠO KÊNH
        target_channel = None
        for cat_name, channels in data["categories"].items():
            cat = await guild.create_category(cat_name)
            for ch_type, ch_name in channels:
                created_ch = None
                if ch_type == "text": created_ch = await guild.create_text_channel(ch_name, category=cat)
                elif ch_type == "voice": created_ch = await guild.create_voice_channel(ch_name, category=cat)
                
                if ch_name == data["welcome"]["channel"]: target_channel = created_ch

        # GỬI LỜI CHÀO BẰNG MÀU CHỦ ĐẠO
        if target_channel:
            embed = discord.Embed(title=data["welcome"]["title"], description=data["welcome"]["desc"], color=self.accent_color)
            embed.set_footer(text=f"Powered by {bot.user.name}")
            await target_channel.send(embed=embed)

        await interaction.edit_original_response(content="✅ **THIẾT LẬP HOÀN TẤT!** Server của bạn đã sẵn sàng.")

# ==========================================
# BƯỚC 1: MODAL NHẬP THÔNG TIN (GIỐNG VIDEO)
# ==========================================
class SetupModal(discord.ui.Modal, title='Thiết Lập Cộng Đồng (Bước 1)'):
    server_name = discord.ui.TextInput(
        label='Tên Server / Cộng Đồng',
        placeholder='Ví dụ: Android Zone, SolisBot Test...',
        required=True
    )
    accent_color = discord.ui.TextInput(
        label='Màu chủ đạo (Mã HEX) - Tuỳ chọn',
        placeholder='Ví dụ: #0000FF (Xanh), #FF0000 (Đỏ)...',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Chuyển đổi mã màu Hex thành màu của Discord
        color_val = discord.Color.default()
        hex_str = self.accent_color.value.strip()
        if hex_str:
            if hex_str.startswith('#'): hex_str = hex_str[1:]
            try: color_val = discord.Color(int(hex_str, 16))
            except ValueError: pass # Nếu nhập sai mã, dùng màu mặc định
        
        embed = discord.Embed(title="⚙️ BƯỚC 2: CHỌN MẪU SERVER", description=f"Tên server mới: **{self.server_name.value}**\nMàu sắc đã nhận. Hãy chọn mẫu bên dưới để hoàn tất.", color=color_val)
        await interaction.response.send_message(embed=embed, view=AdvancedSetupView(self.server_name.value, color_val))

# ==========================================
# CẤU HÌNH BOT CHÍNH
# ==========================================
class AndroidZoneBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def setup_hook(self):
        await self.tree.sync()

bot = AndroidZoneBot()

@bot.event
async def on_ready():
    keep_alive() 
    print(f'✅ Bot {bot.user.name} đã sẵn sàng!')

@bot.tree.command(name="setup", description="🔄 Mở bảng điều khiển cài đặt Server (Y hệt video)")
@app_commands.default_permissions(administrator=True)
async def setup_command(interaction: discord.Interaction):
    # Thay vì mở Menu ngay, bot sẽ mở 1 cái Bảng điền thông tin (Modal) y hệt video
    await interaction.response.send_modal(SetupModal())

@bot.tree.command(name="say", description="📢 Bot nhắn nội dung vào kênh hiện tại")
@app_commands.default_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, content: str):
    await interaction.channel.send(content)
    await interaction.response.send_message("✅ Đã gửi!", ephemeral=True)

bot.run(os.environ.get('DISCORD_TOKEN'))
