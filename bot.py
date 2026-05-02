import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8750588238:AAFUJ3o6iR7Cu92on2HdsvLhKP5pQHs15Bo"
NIMO_USERNAME = "nimoteam2026"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬  Tôi chưa hiểu rõ hệ thống này", callback_data="q1")],
        [InlineKeyboardButton("🤔  Tôi không biết gói nào phù hợp", callback_data="q2")],
        [InlineKeyboardButton("😰  Tôi sợ cài không được", callback_data="q3")],
    ])


def after_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Tư vấn thêm với NiMo", url=f"https://t.me/{NIMO_USERNAME}")],
        [InlineKeyboardButton("⬅️ Câu hỏi khác", callback_data="menu")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Chào bạn! Tôi là trợ lý của *NiMo Team*.\n\n"
        "Bạn đang băn khoăn điều gì về *Cambodia Biz Agent*?\n"
        "Chọn câu hỏi bên dưới — tôi trả lời ngay:",
        parse_mode="Markdown",
        reply_markup=menu_keyboard()
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.edit_message_text(
            "Bạn còn băn khoăn điều gì nữa không?\nChọn câu hỏi bên dưới:",
            reply_markup=menu_keyboard()
        )

    elif query.data == "q1":
        await query.edit_message_text(
            "💬 *Hệ thống Cambodia Biz Agent hoạt động thế nào?*\n\n"
            "Hiểu đơn giản: bạn có 5 Nhân Viên AI — mỗi người làm 1 việc:\n\n"
            "🔍 Nghiên cứu thị trường & đối thủ\n"
            "📣 Tạo content FB/TikTok/Instagram\n"
            "💰 Viết trang bán hàng & chốt đơn\n"
            "📦 Tự động nhận đơn & thông báo giao hàng\n"
            "📊 Báo cáo doanh thu & tối ưu hàng tuần\n\n"
            "Bạn ra lệnh bằng tiếng Khmer hoặc tiếng Việt — AI làm việc ngay lập tức.\n\n"
            "Không cần biết lập trình. Không cần cài app phức tạp. 🚀",
            parse_mode="Markdown",
            reply_markup=after_keyboard()
        )

    elif query.data == "q2":
        await query.edit_message_text(
            "🤔 *Gói nào phù hợp với shop của bạn?*\n\n"
            "🟦 *Basic $97* — Mới biết đến AI, muốn thử trước\n"
            "→ 5 Nhân Viên AI + hướng dẫn tiếng Khmer + hỗ trợ 30 ngày\n\n"
            "⭐ *Pro $297* — Shop đang hoạt động, muốn tự động 24/7\n"
            "→ Chatbot trả lời khách + tự động đăng bài + booking tự động\n\n"
            "🟡 *VIP $597* — Không muốn tự cài, NiMo làm hết qua Zoom\n"
            "→ Bàn giao xong là dùng được ngay, hỗ trợ 90 ngày\n\n"
            "Chưa chắc? Nhắn NiMo kể quy mô shop — tư vấn đúng gói trong 5 phút 👇",
            parse_mode="Markdown",
            reply_markup=after_keyboard()
        )

    elif query.data == "q3":
        await query.edit_message_text(
            "😰 *Không rành công nghệ — có cài được không?*\n\n"
            "Được! Đây là lý do:\n\n"
            "✅ Hướng dẫn từng bước bằng tiếng Khmer\n"
            "✅ Có ảnh minh họa & video xem theo\n"
            "✅ Bot hỗ trợ 24/7 — nhắn bất cứ lúc nào\n"
            "✅ NiMo sẵn sàng tư vấn thêm khi bạn cần\n\n"
            "Gói VIP: NiMo ngồi cài cùng bạn qua Zoom 2 tiếng — bạn chỉ xem và bấm theo. "
            "Xong là dùng được ngay 🎯",
            parse_mode="Markdown",
            reply_markup=after_keyboard()
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("✅ Bot đang chạy...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
