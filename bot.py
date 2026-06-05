import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from web_server import keep_alive

TEMPLATES = {
    "Streamer": {
        "VN": {
            "roles": ["👑 Tối Cao", "🛡️ Quản Trị Viên", "🔨 Kiểm Duyệt Viên", "🌟 Khách VIP", "🚀 Người Nâng Cấp (Booster)", "🎬 Đội Ngũ Media", "🎮 Cao Thủ Trứ Danh", "💬 Người Truyền Lửa", "👤 Cư Dân Mới", "👀 Kẻ Quan Sát"],
            "categories": {
                "📌 THÔNG TIN MÁY CHỦ": [("text", "đọc-luật-tại-đây"), ("text", "thông-báo-quan-trọng"), ("text", "🎉-giveaway-sự-kiện"), ("text", "🎨-chọn-vai-trò"), ("text", "🤝-hợp-tác-liên-hệ")],
                "🔴 TRUNG TÂM NỘI DUNG": [("text", "thông-báo-livestream"), ("text", "video-youtube-mới"), ("text", "📱-tiktok-shorts"), ("text", "🎬-kho-clips-highlight"), ("text", "🎨-fan-art-sáng-tạo")],
                "🌍 GIAO LƯU KẾT BẠN": [("text", "cổng-chào-tân-binh"), ("text", "trò-chuyện-tổng-hợp"), ("text", "☕-quán-trà-đá-vỉa-hè"), ("text", "🖼️-chia-sẻ-hình-ảnh"), ("text", "😂-động-meme-giải-trí"), ("text", "🎵-chia-sẻ-âm-nhạc"), ("text", "🤖-khu-vực-chơi-bot")],
                "🎮 CHIẾN TRƯỜNG GAMING": [("text", "🔍-tìm-đồng-đội-leo-rank"), ("text", "thảo-luận-chiến-thuật"), ("text", "🏆-khoe-chuỗi-thắng-rank"), ("text", "📰-tin-tức-esports")],
                "💡 HỖ TRỢ & ĐÓNG GÓP": [("text", "hỏi-đáp-thắc-mắc"), ("text", "góp-ý-xây-dựng-server"), ("text", "báo-cáo-vi-phạm")],
                "🔊 KHU VỰC GIAO TIẾP": [("voice", "Sảnh Chờ Chính"), ("voice", "Quán Cà Phê Chill"), ("voice", "🎮 Tổ Đội 1 (Tối đa 5)"), ("voice", "🎮 Tổ Đội 2 (Tối đa 5)"), ("voice", "🎮 Tổ Đội 3 (Tối đa 5)"), ("voice", "🎮 Tổ Đội 4 (Tối đa 5)"), ("voice", "🎵 Phòng Nghe Nhạc"), ("voice", "🎤 Phòng Hát Karaoke"), ("voice", "🎙️ Phòng Podcast"), ("voice", "💤 Đang Ngủ (AFK)")]
            },
            "welcome": {"channel": "đọc-luật-tại-đây", "title": "🎉 Chào mừng đến với vùng đất mới!", "desc": "Hãy chắc chắn rằng bạn đã đọc kỹ các quy định. Sau đó hãy chọn vai trò và tham gia trò chuyện cùng mọi người nhé!"}
        },
        "EN": {
            "roles": ["Supreme Leader", "Admin", "Moderator", "VIP", "Server Booster", "Media Team", "Pro Gamer", "Active Chatter", "Member", "Lurker"],
            "categories": {
                "📌 SERVER INFORMATION": [("text", "read-rules-here"), ("text", "important-announcements"), ("text", "🎉-giveaways-events"), ("text", "🎨-get-roles"), ("text", "🤝-partnerships")],
                "🔴 CONTENT HUB": [("text", "live-now"), ("text", "new-youtube-videos"), ("text", "📱-tiktok-shorts"), ("text", "🎬-clips-and-highlights"), ("text", "🎨-fan-art")],
                "🌍 COMMUNITY LOUNGE": [("text", "welcome-gate"), ("text", "general-chat"), ("text", "☕-chill-talk"), ("text", "🖼️-media-share"), ("text", "😂-memes-only"), ("text", "🎵-music-share"), ("text", "🤖-bot-commands")],
                "🎮 GAMING BATTLEFIELD": [("text", "🔍-looking-for-group"), ("text", "game-discussion"), ("text", "🏆-flex-your-rank"), ("text", "📰-esports-news")],
                "💡 SUPPORT & FEEDBACK": [("text", "q-and-a"), ("text", "server-suggestions"), ("text", "report-rule-breakers")],
                "🔊 VOICE CHANNELS": [("voice", "Main Lounge"), ("voice", "Chill Cafe"), ("voice", "🎮 Squad 1 (Max 5)"), ("voice", "🎮 Squad 2 (Max 5)"), ("voice", "🎮 Squad 3 (Max 5)"), ("voice", "🎮 Squad 4 (Max 5)"), ("voice", "🎵 Music Room"), ("voice", "🎤 Karaoke Room"), ("voice", "🎙️ Podcast Room"), ("voice", "💤 AFK")]
            },
            "welcome": {"channel": "read-rules-here", "title": "🎉 Welcome to the community!", "desc": "Please read the rules carefully. Grab your roles and say hi in the general chat!"}
        }
    },
    "Business": {
        "VN": {
            "roles": ["Giám Đốc (CEO)", "Quản Lý Cửa Hàng", "Trưởng Phòng CSKH", "Nhân Viên Sale", "Nhân Viên Kỹ Thuật", "Đối Tác Kinh Doanh", "Khách Hàng Thân Thiết", "Khách Hàng Mới"],
            "categories": {
                "🏢 BẢNG TIN TỨC": [("text", "nội-quy-cửa-hàng"), ("text", "thông-báo-chung"), ("text", "tin-tức-tuyển-dụng")],
                "🛒 GIAN HÀNG SẢN PHẨM": [("text", "hàng-mới-về"), ("text", "🔥-khuyến-mãi-hot"), ("text", "danh-mục-sản-phẩm"), ("text", "hướng-dẫn-mua-hàng")],
                "💳 GIAO DỊCH & THANH TOÁN": [("text", "thông-tin-chuyển-khoản"), ("text", "xác-nhận-đơn-hàng"), ("text", "chính-sách-đổi-trả")],
                "💬 KHÔNG GIAN KHÁCH HÀNG": [("text", "phòng-khách-giao-lưu"), ("text", "📸-khoe-đơn-hàng"), ("text", "⭐-đánh-giá-chất-lượng"), ("text", "hỏi-đáp-sản-phẩm")],
                "🔧 TRUNG TÂM BẢO HÀNH": [("text", "tiếp-nhận-khiếu-nại"), ("text", "hỗ-trợ-kỹ-thuật"), ("text", "tra-cứu-bảo-hành")],
                "📞 TỔNG ĐÀI HỖ TRỢ": [("voice", "Phòng Chờ Tư Vấn"), ("voice", "Bàn Tư Vấn Số 1"), ("voice", "Bàn Tư Vấn Số 2"), ("voice", "Bàn Tư Vấn Số 3"), ("voice", "Phòng Bảo Hành Kỹ Thuật")]
            },
            "welcome": {"channel": "nội-quy-cửa-hàng", "title": "🛒 Rất hân hạnh được phục vụ!", "desc": "Cảm ơn quý khách đã tin tưởng. Hãy tham khảo các mặt hàng mới nhất tại gian hàng nhé!"}
        },
        "EN": {
            "roles": ["CEO", "Store Manager", "Head of Support", "Sales Representative", "Technical Staff", "Business Partner", "Loyal Customer", "New Customer"],
            "categories": {
                "🏢 NOTICE BOARD": [("text", "store-policies"), ("text", "general-announcements"), ("text", "hiring-news")],
                "🛒 PRODUCT SHOWCASE": [("text", "new-arrivals"), ("text", "🔥-hot-promotions"), ("text", "product-catalog"), ("text", "how-to-buy")],
                "💳 TRANSACTIONS & BILLING": [("text", "payment-info"), ("text", "order-confirmations"), ("text", "return-policy")],
                "💬 CUSTOMER SPACE": [("text", "customer-lounge"), ("text", "📸-order-flex"), ("text", "⭐-reviews-and-ratings"), ("text", "product-q-and-a")],
                "🔧 WARRANTY CENTER": [("text", "complaints-desk"), ("text", "technical-support"), ("text", "warranty-check")],
                "📞 SUPPORT HOTLINE": [("voice", "Waiting Room"), ("voice", "Consultation Desk 1"), ("voice", "Consultation Desk 2"), ("voice", "Consultation Desk 3"), ("voice", "Technical Warranty")]
            },
            "welcome": {"channel": "store-policies", "title": "🛒 We are glad to serve you!", "desc": "Thank you for trusting us. Please check out our latest products in the showcase area!"}
        }
    },
    "Study": {
        "VN": {
            "roles": ["Hiệu Trưởng", "Giáo Viên Chủ Nhiệm", "Hội Học Sinh", "Cán Bộ Lớp", "Học Sinh Xuất Sắc", "Học Sinh Chăm Chỉ", "Học Sinh Mới"],
            "categories": {
                "🏫 THÔNG TIN CHUNG": [("text", "nội-quy-lớp-học"), ("text", "thông-báo-nhà-trường"), ("text", "lịch-học-sự-kiện")],
                "📚 TÀI LIỆU HỌC TẬP": [("text", "kho-sách-tham-khảo"), ("text", "đề-thi-thử"), ("text", "tài-liệu-môn-toán"), ("text", "tài-liệu-môn-văn"), ("text", "tài-liệu-ngoại-ngữ")],
                "✍️ GÓC THẢO LUẬN": [("text", "hỏi-đáp-bài-tập"), ("text", "chia-sẻ-phương-pháp"), ("text", "tìm-nhóm-học-chung")],
                "☕ KHU VỰC GIẢI LAO": [("text", "căn-tin-chém-gió"), ("text", "chia-sẻ-sở-thích"), ("text", "góc-tâm-sự")],
                "🎧 PHÒNG TỰ HỌC": [("voice", "Thư Viện Im Lặng"), ("voice", "Nhạc Lofi Tập Trung"), ("voice", "Nhóm Học Tập 1"), ("voice", "Nhóm Học Tập 2"), ("voice", "Phòng Nghỉ Ngơi")]
            },
            "welcome": {"channel": "nội-quy-lớp-học", "title": "🎓 Chào mừng đến với môi trường học tập!", "desc": "Chúc bạn có những giờ học hiệu quả. Hãy kết bạn và cùng nhau tiến bộ nhé!"}
        },
        "EN": {
            "roles": ["Principal", "Head Teacher", "Student Council", "Class Monitor", "Top Student", "Hardworking Student", "New Student"],
            "categories": {
                "🏫 GENERAL INFO": [("text", "class-rules"), ("text", "school-announcements"), ("text", "schedule-events")],
                "📚 STUDY MATERIALS": [("text", "reference-books"), ("text", "mock-exams"), ("text", "math-resources"), ("text", "literature-resources"), ("text", "language-resources")],
                "✍️ DISCUSSION AREA": [("text", "homework-help"), ("text", "study-methods"), ("text", "find-study-buddies")],
                "☕ BREAK ROOM": [("text", "cafeteria-chat"), ("text", "hobby-sharing"), ("text", "venting-space")],
                "🎧 STUDY ROOMS": [("voice", "Silent Library"), ("voice", "Lofi Focus"), ("voice", "Study Group 1"), ("voice", "Study Group 2"), ("voice", "Rest Area")]
            },
            "welcome": {"channel": "class-rules", "title": "🎓 Welcome to the learning environment!", "desc": "We wish you productive study sessions. Make friends and improve together!"}
        }
    }
}

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
        discord.SelectOption(label="Đa Phương Tiện / Gaming / Cộng Đồng", value="Streamer", emoji="🎥", default=True),
        discord.SelectOption(label="Kinh Doanh / Cửa Hàng / Công Ty", value="Business", emoji="🛒"),
        discord.SelectOption(label="Giáo Dục / Thư Viện / Nhóm Học", value="Study", emoji="🎓")
    ], row=1)
    async def template_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_template = select.values[0]
        for opt in select.options: opt.default = (opt.value == self.selected_template)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Giữ Kênh & Role Cũ: BẬT", style=discord.ButtonStyle.green, row=2)
    async def toggle_keep(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.keep_channels = not self.keep_channels
        button.label = "Giữ Kênh & Role Cũ: BẬT" if self.keep_channels else "XÓA SẠCH KÊNH & ROLE: BẬT"
        button.style = discord.ButtonStyle.green if self.keep_channels else discord.ButtonStyle.danger
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="🚀 TIẾN HÀNH XÂY DỰNG", style=discord.ButtonStyle.blurple, row=2)
    async def start_setup(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"⏳ NLHT Bot đang xây dựng **{self.server_name}**...", ephemeral=True)
        guild = interaction.guild
        
        try: await guild.edit(name=self.server_name)
        except: pass

        data = TEMPLATES.get(self.selected_template, TEMPLATES["Streamer"]).get(self.selected_lang, TEMPLATES["Streamer"]["VN"])

        if not self.keep_channels:
            for channel in guild.channels:
                try: await channel.delete()
                except: pass
            for role in guild.roles:
                if role.name != "@everyone" and not role.managed:
                    try: await role.delete()
                    except: pass
            await asyncio.sleep(2)

        for role_name in reversed(data["roles"]):
            if not discord.utils.get(guild.roles, name=role_name):
                try: await guild.create_role(name=role_name, hoist=True, color=self.accent_color)
                except: pass

        target_channel = None
        for cat_name, channels in data["categories"].items():
            cat = await guild.create_category(cat_name)
            for ch_type, ch_name in channels:
                created_ch = None
                if ch_type == "text": created_ch = await guild.create_text_channel(ch_name, category=cat)
                elif ch_type == "voice": 
                    created_ch = await guild.create_voice_channel(ch_name, category=cat)
                    if "Tối đa 5" in ch_name or "Max 5" in ch_name:
                        await created_ch.edit(user_limit=5)
                
                if ch_name == data["welcome"]["channel"]: target_channel = created_ch

        if target_channel:
            embed = discord.Embed(title=data["welcome"]["title"], description=data["welcome"]["desc"], color=self.accent_color)
            embed.set_footer(text=f"Powered by NLHT Bot")
            await target_channel.send(embed=embed)

        await interaction.edit_original_response(content="✅ **THIẾT LẬP HOÀN TẤT!** Server của bạn đã sẵn sàng với cấu trúc mới.")

class SetupModal(discord.ui.Modal, title='Thiết Lập Cộng Đồng bởi NLHT Bot'):
    server_name = discord.ui.TextInput(
        label='Tên Server / Cộng Đồng',
        placeholder='Ví dụ: NLHT Zone, Gaming Club...',
        required=True
    )
    accent_color = discord.ui.TextInput(
        label='Màu chủ đạo (Mã HEX) - Tuỳ chọn',
        placeholder='Ví dụ: #0000FF (Xanh), #FF0000 (Đỏ)...',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        color_val = discord.Color.default()
        hex_str = self.accent_color.value.strip()
        if hex_str:
            if hex_str.startswith('#'): hex_str = hex_str[1:]
            try: color_val = discord.Color(int(hex_str, 16))
            except ValueError: pass 
        
        embed = discord.Embed(title="⚙️ BƯỚC 2: CHỌN MẪU SERVER", description=f"Tên server mới: **{self.server_name.value}**\nBây giờ hãy chọn mẫu và trạng thái dọn dẹp kênh/role cũ.", color=color_val)
        embed.set_footer(text="Hệ thống cài đặt - NLHT Bot")
        await interaction.response.send_message(embed=embed, view=AdvancedSetupView(self.server_name.value, color_val))

class NLHTBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def setup_hook(self):
        await self.tree.sync()

bot = NLHTBot()

@bot.event
async def on_ready():
    keep_alive() 
    print(f'✅ Bot NLHT đã sẵn sàng!')

@bot.tree.command(name="setup", description="🔄 Mở bảng điều khiển cài đặt Server (NLHT Bot)")
@app_commands.default_permissions(administrator=True)
async def setup_command(interaction: discord.Interaction):
    await interaction.response.send_modal(SetupModal())

@bot.tree.command(name="say", description="📢 Bot NLHT nhắn nội dung vào kênh hiện tại")
@app_commands.default_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, content: str):
    await interaction.channel.send(content)
    await interaction.response.send_message("✅ Đã gửi!", ephemeral=True)

bot.run(os.environ.get('DISCORD_TOKEN'))
