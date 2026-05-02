import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8750588238:AAFUJ3o6iR7Cu92on2HdsvLhKP5pQHs15Bo"
NIMO_USERNAME = "nimoteam2026"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ─── NỘI DUNG 2 NGÔN NGỮ ───────────────────────────────────────────────────

CONTENT = {
    "km": {
        "welcome": (
            "👋 សួស្តី! ខ្ញុំជាជំនួយការរបស់ *NiMo Team*។\n\n"
            "អ្នកមានសំណួរអ្វីអំពី *Cambodia Biz Agent*?\n"
            "ជ្រើសរើសសំណួរខាងក្រោម — ខ្ញុំឆ្លើយភ្លាមៗ:"
        ),
        "menu_again": "តើអ្នកមានសំណួរអ្វីទៀត?\nជ្រើសសំណួរខាងក្រោម:",
        "q1_label": "💬  ខ្ញុំមិនទាន់យល់ច្បាស់អំពីប្រព័ន្ធនេះ",
        "q2_label": "🤔  ខ្ញុំមិនដឹងថាកញ្ចប់ណាសាកសម",
        "q3_label": "😰  ខ្ញុំខ្លាចដំឡើងមិនបាន",
        "consult": "💬 សួរ NiMo ដោយផ្ទាល់",
        "back": "⬅️ សំណួរផ្សេងទៀត",
        "q1": (
            "💬 *ប្រព័ន្ធ Cambodia Biz Agent ដំណើរការយ៉ាងដូចម្តេច?*\n\n"
            "យល់ឱ្យសាមញ្ញ: អ្នកមានបុគ្គលិក AI ចំនួន 5 នាក់ — ម្នាក់ធ្វើការងារ 1:\n\n"
            "🔍 ស្រាវជ្រាវទីផ្សារ និងគូប្រជែង\n"
            "📣 បង្កើតមាតិកា FB/TikTok/Instagram\n"
            "💰 សរសេរទំព័រលក់ និងបិទការបញ្ជាទិញ\n"
            "📦 ទទួលការបញ្ជាទិញ និងជូនដំណឹងដោយស្វ័យប្រវត្តិ\n"
            "📊 របាយការណ៍ចំណូល និងបង្កើនប្រសិទ្ធភាព\n\n"
            "អ្នកបញ្ជាជាភាសាខ្មែរ — AI ធ្វើការភ្លាមៗ។\n\n"
            "មិនចាំបាច់ចេះសរសេរកូដ។ 🚀"
        ),
        "q2": (
            "🤔 *កញ្ចប់ណាសាកសមជាមួយហាងរបស់អ្នក?*\n\n"
            "🟦 *Basic $97* — ទើបស្គាល់ AI ចង់សាកល្បងមុន\n"
            "→ បុគ្គលិក AI 5 នាក់ + ការណែនាំជាភាសាខ្មែរ + ការគាំទ្រ 30 ថ្ងៃ\n\n"
            "⭐ *Pro $297* — ហាងដំណើរការ ចង់ស្វ័យប្រវត្តិ 24/7\n"
            "→ Chatbot ឆ្លើយ + ប្រកាសដោយស្វ័យប្រវត្តិ + ទទួល booking\n\n"
            "🟡 *VIP $597* — មិនចង់ដំឡើងខ្លួនឯង NiMo ធ្វើជំនួស\n"
            "→ ដំឡើងរួច ប្រើបានភ្លាម ការគាំទ្រ 90 ថ្ងៃ\n\n"
            "មិនប្រាកដ? ប្រាប់ NiMo អំពីហាងរបស់អ្នក — យើងណែនាំកញ្ចប់ត្រឹមត្រូវ 👇"
        ),
        "q3": (
            "😰 *មិនចេះបច្ចេកវិទ្យា — អាចដំឡើងបានទេ?*\n\n"
            "បាន! នេះជាហេតុផល:\n\n"
            "✅ ការណែនាំជាភាសាខ្មែរ មានរូបភាពបង្ហាញជាជំហានៗ\n"
            "✅ មានវីដេអូមើលតាម\n"
            "✅ ប្រើ Bot ជួយ 24/7\n"
            "✅ NiMo ផ្ទាល់ឆ្លើយពេលត្រូវការ\n\n"
            "កញ្ចប់ VIP: NiMo អង្គុយដំឡើងជាមួយអ្នកតាម Zoom 2 ម៉ោង — "
            "អ្នកគ្រាន់តែមើល ហើយចុចតាម។ 🎯"
        ),
    },
    "en": {
        "welcome": (
            "👋 Hello! I'm the assistant of *NiMo Team*.\n\n"
            "What are you wondering about *Cambodia Biz Agent*?\n"
            "Choose a question below — I'll answer right away:"
        ),
        "menu_again": "Any other questions?\nChoose below:",
        "q1_label": "💬  I don't understand how this system works",
        "q2_label": "🤔  I don't know which plan fits me",
        "q3_label": "😰  I'm afraid I can't install it",
        "consult": "💬 Chat directly with NiMo",
        "back": "⬅️ Other questions",
        "q1": (
            "💬 *How does Cambodia Biz Agent work?*\n\n"
            "Simply put: you have 5 AI Employees — each does 1 job:\n\n"
            "🔍 Market research & competitor analysis\n"
            "📣 Create content for FB/TikTok/Instagram\n"
            "💰 Write sales pages & close orders\n"
            "📦 Auto-receive orders & send delivery notifications\n"
            "📊 Revenue reports & weekly optimization\n\n"
            "You give commands in Khmer or English — AI works instantly.\n\n"
            "No coding needed. 🚀"
        ),
        "q2": (
            "🤔 *Which plan fits your shop?*\n\n"
            "🟦 *Basic $97* — New to AI, want to try first\n"
            "→ 5 AI Employees + Khmer guide + 30-day support\n\n"
            "⭐ *Pro $297* — Shop running, want full automation 24/7\n"
            "→ Chatbot + auto-post + auto-booking\n\n"
            "🟡 *VIP $597* — Don't want to install yourself, NiMo does it for you\n"
            "→ Ready to use after handover, 90-day support\n\n"
            "Not sure? Tell NiMo about your shop — we'll recommend the right plan in 5 mins 👇"
        ),
        "q3": (
            "😰 *Not tech-savvy — can I still install it?*\n\n"
            "Yes! Here's why:\n\n"
            "✅ Step-by-step guide in Khmer with images\n"
            "✅ Video tutorials to follow\n"
            "✅ Bot support 24/7\n"
            "✅ NiMo personally answers when needed\n\n"
            "VIP plan: NiMo installs it with you via Zoom in 2 hours — "
            "you just watch and click. 🎯"
        ),
    }
}

# ─── KEYBOARDS ──────────────────────────────────────────────────────────────

def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇰🇭 ភាសាខ្មែរ", callback_data="lang_km"),
        InlineKeyboardButton("🇬🇧 English",    callback_data="lang_en"),
    ]])

def menu_keyboard(lang):
    c = CONTENT[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(c["q1_label"], callback_data="q1")],
        [InlineKeyboardButton(c["q2_label"], callback_data="q2")],
        [InlineKeyboardButton(c["q3_label"], callback_data="q3")],
    ])

def after_keyboard(lang):
    c = CONTENT[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(c["consult"], url=f"https://t.me/{NIMO_USERNAME}")],
        [InlineKeyboardButton(c["back"],    callback_data="menu")],
    ])

# ─── HANDLERS ───────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇰🇭 ជ្រើសភាសា  |  🇬🇧 Choose language:",
        reply_markup=lang_keyboard()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Chọn ngôn ngữ
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        context.user_data["lang"] = lang
        c = CONTENT[lang]
        await query.edit_message_text(
            c["welcome"],
            parse_mode="Markdown",
            reply_markup=menu_keyboard(lang)
        )
        return

    lang = context.user_data.get("lang", "km")
    c = CONTENT[lang]

    if data == "menu":
        await query.edit_message_text(
            c["menu_again"],
            reply_markup=menu_keyboard(lang)
        )
    elif data in ("q1", "q2", "q3"):
        await query.edit_message_text(
            c[data],
            parse_mode="Markdown",
            reply_markup=after_keyboard(lang)
        )

# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("✅ Bot đang chạy...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
