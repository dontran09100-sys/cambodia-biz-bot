"""
Cambodia Biz Agent ‚Äî Bot Khmer + English
FAQ + buy flow + admin support
Token: @NiMoBizAgent_bot (Railway)
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# ‚îÄ‚îÄ‚îÄ CONFIG ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

TOKEN    = "8750588238:AAFUJ3o6iR7Cu92on2HdsvLhKP5pQHs15Bo"
ADMIN_ID = 8704923191

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# ‚îÄ‚îÄ‚îÄ PAYMENT INFO ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

BANK_INFO = {
    "basic": {"label": "Basic", "price_usd": "$97",  "price_riel": "‚âà 400,000 Riel"},
    "pro":   {"label": "Pro",   "price_usd": "$297", "price_riel": "‚âà 1,200,000 Riel"},
    "vip":   {"label": "VIP",   "price_usd": "$597", "price_riel": "‚âà 2,400,000 Riel"},
}

BANK_DETAILS = {
    "km": (
        "üí≥ *·ûñ·üê·ûè·üå·ûò·û∂·ûì·ûÄ·û∂·ûö·ûï·üí·ûë·üÅ·ûö·ûî·üí·ûö·û∂·ûÄ·üã*\n\n"
        "üè¶ *ABA Bank*\n"
        "·ûõ·üÅ·ûÅ·ûÇ·ûé·ûì·û∏: `000 123 456`\n"
        "·ûà·üí·ûò·üÑ·üá: NIMO TEAM\n\n"
        "üì± *Wing Money*\n"
        "·ûõ·üÅ·ûÅ·ûë·ûº·ûö·ûü·üê·ûñ·üí·ûë: `012 345 678`\n"
        "·ûà·üí·ûò·üÑ·üá: NIMO TEAM\n\n"
        "‚ö†Ô∏è *·ûü·ûò·üí·ûÇ·û∂·ûõ·üã:* ·ûü·ûº·ûò·ûü·ûö·ûü·üÅ·ûö·ûõ·üÅ·ûÅ·ûÄ·ûº·ûä·ûî·ûâ·üí·ûá·û∂·ûë·û∑·ûâ NiMo ·ûï·üí·ûâ·ûæ·û¢·üÑ·ûô ·ûÄ·üí·ûì·ûª·ûÑ·ûÄ·û∂·ûö·ûï·üí·ûë·üÅ·ûö·üî"
    ),
    "en": (
        "üí≥ *Payment Details*\n\n"
        "üè¶ *ABA Bank*\n"
        "Account: `000 123 456`\n"
        "Name: NIMO TEAM\n\n"
        "üì± *Wing Money*\n"
        "Phone: `012 345 678`\n"
        "Name: NIMO TEAM\n\n"
        "‚ö†Ô∏è *Note:* Include the order code NiMo provides in the transfer remark."
    ),
}

# ‚îÄ‚îÄ‚îÄ CONTENT ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

CONTENT = {
    "km": {
        "faq": {
            "q_system": {
                "label": "üí¨ ·ûÅ·üí·ûâ·ûª·üÜ·ûò·û∑·ûì·ûë·û∂·ûì·üã·ûô·ûõ·üã·ûÖ·üí·ûî·û∂·ûü·üã·û¢·üÜ·ûñ·û∏·ûî·üí·ûö·ûñ·üê·ûì·üí·ûí·ûì·üÅ·üá",
                "answer": (
                    "üí¨ *·ûî·üí·ûö·ûñ·üê·ûì·üí·ûí Cambodia Biz Agent ·ûä·üÜ·ûé·ûæ·ûö·ûÄ·û∂·ûö·ûô·üâ·û∂·ûÑ·ûä·ûº·ûÖ·ûò·üí·ûè·üÅ·ûÖ?*\n\n"
                    "·ûô·ûõ·üã·û±·üí·ûô·ûü·û∂·ûò·ûâ·üí·ûâ: ·ûî·ûÑ ·ûò·û∂·ûì *·ûî·ûª·ûÇ·üí·ûÇ·ûõ·û∑·ûÄ AI ·ûÖ·üÜ·ûì·ûΩ·ûì 5 ·ûì·û∂·ûÄ·üã* ‚Äî ·ûò·üí·ûì·û∂·ûÄ·üã·ûí·üí·ûú·ûæ·ûÄ·û∂·ûö·ûÑ·û∂·ûö 1:\n\n"
                    "üîç ·ûü·üí·ûö·û∂·ûú·ûá·üí·ûö·û∂·ûú·ûë·û∏·ûï·üí·ûü·û∂·ûö ·ûì·û∑·ûÑ·ûÇ·ûº·ûî·üí·ûö·ûá·üÇ·ûÑ\n"
                    "üì£ ·ûî·ûÑ·üí·ûÄ·ûæ·ûè·ûò·û∂·ûè·û∑·ûÄ·û∂ FB/TikTok/Instagram\n"
                    "üí∞ ·ûü·ûö·ûü·üÅ·ûö·ûë·üÜ·ûñ·üê·ûö·ûõ·ûÄ·üã ·ûì·û∑·ûÑ·ûî·û∑·ûë·ûÄ·û∂·ûö·ûî·ûâ·üí·ûá·û∂·ûë·û∑·ûâ\n"
                    "üì¶ ·ûë·ûë·ûΩ·ûõ·ûÄ·û∂·ûö·ûî·ûâ·üí·ûá·û∂·ûë·û∑·ûâ ·ûì·û∑·ûÑ·ûá·ûº·ûì·ûä·üÜ·ûé·ûπ·ûÑ·ûä·üÑ·ûô·ûü·üí·ûú·üê·ûô·ûî·üí·ûö·ûú·ûè·üí·ûè·û∑\n"
                    "üìä ·ûö·ûî·û∂·ûô·ûÄ·û∂·ûö·ûé·üç·ûÖ·üÜ·ûé·ûº·ûõ ·ûì·û∑·ûÑ·ûî·ûÑ·üí·ûÄ·ûæ·ûì·ûî·üí·ûö·ûü·û∑·ûë·üí·ûí·ûó·û∂·ûñ\n\n"
                    "·ûî·ûÑ·ûî·ûâ·üí·ûá·û∂·ûá·û∂·ûó·û∂·ûü·û∂·ûÅ·üí·ûò·üÇ·ûö ‚Äî AI ·ûí·üí·ûú·ûæ·ûÄ·û∂·ûö·ûó·üí·ûõ·û∂·ûò·üó·üî\n\n"
                    "·ûò·û∑·ûì·ûÖ·û∂·üÜ·ûî·û∂·ûÖ·üã·ûÖ·üÅ·üá·ûü·ûö·ûü·üÅ·ûö·ûÄ·ûº·ûä·üî üöÄ"
                ),
            },
            "q_which_plan": {
                "label": "ü§î ·ûÅ·üí·ûâ·ûª·üÜ·ûò·û∑·ûì·ûä·ûπ·ûÑ·ûê·û∂·ûÄ·ûâ·üí·ûÖ·ûî·üã·ûé·û∂·ûü·û∂·ûÄ·ûü·ûò",
                "answer": (
                    "ü§î *·ûÄ·ûâ·üí·ûÖ·ûî·üã·ûé·û∂·ûü·û∂·ûÄ·ûü·ûò·ûá·û∂·ûò·ûΩ·ûô·û†·û∂·ûÑ·ûö·ûî·ûü·üã·ûî·ûÑ?*\n\n"
                    "üü¶ *Basic $97* ‚Äî ·ûë·ûæ·ûî·ûü·üí·ûÇ·û∂·ûõ·üã AI ·ûÖ·ûÑ·üã·ûü·û∂·ûÄ·ûõ·üí·ûî·ûÑ·ûò·ûª·ûì\n"
                    "‚Üí ·ûî·ûª·ûÇ·üí·ûÇ·ûõ·û∑·ûÄ AI 5 ·ûì·û∂·ûÄ·üã + ·ûÄ·û∂·ûö·ûé·üÇ·ûì·û∂·üÜ·ûá·û∂·ûó·û∂·ûü·û∂·ûÅ·üí·ûò·üÇ·ûö + ·ûÄ·û∂·ûö·ûÇ·û∂·üÜ·ûë·üí·ûö 30 ·ûê·üí·ûÑ·üÉ\n\n"
                    "‚≠ê *Pro $297* ‚Äî ·û†·û∂·ûÑ·ûä·üÜ·ûé·ûæ·ûö·ûÄ·û∂·ûö ·ûÖ·ûÑ·üã·ûü·üí·ûú·üê·ûô·ûî·üí·ûö·ûú·ûè·üí·ûè·û∑ 24/7\n"
                    "‚Üí Chatbot ·ûÜ·üí·ûõ·ûæ·ûô + ·ûî·üí·ûö·ûÄ·û∂·ûü·ûä·üÑ·ûô·ûü·üí·ûú·üê·ûô·ûî·üí·ûö·ûú·ûè·üí·ûè·û∑ + ·ûë·ûë·ûΩ·ûõ booking\n\n"
                    "üü° *VIP $597* ‚Äî ·ûò·û∑·ûì·ûÖ·ûÑ·üã·ûä·üÜ·û°·ûæ·ûÑ·ûÅ·üí·ûõ·ûΩ·ûì·ûØ·ûÑ NiMo ·ûí·üí·ûú·ûæ·ûá·üÜ·ûì·ûΩ·ûü\n"
                    "‚Üí ·ûä·üÜ·û°·ûæ·ûÑ·ûö·ûΩ·ûÖ ·ûî·üí·ûö·ûæ·ûî·û∂·ûì·ûó·üí·ûõ·û∂·ûò ·ûÄ·û∂·ûö·ûÇ·û∂·üÜ·ûë·üí·ûö 90 ·ûê·üí·ûÑ·üÉ\n\n"
                    "·ûò·û∑·ûì·ûî·üí·ûö·û∂·ûÄ·ûä? ·ûî·üí·ûö·û∂·ûî·üã NiMo ·û¢·üÜ·ûñ·û∏·û†·û∂·ûÑ·ûö·ûî·ûü·üã·ûî·ûÑ ‚Äî ·ûô·ûæ·ûÑ·ûé·üÇ·ûì·û∂·üÜ·ûÄ·ûâ·üí·ûÖ·ûî·üã·ûè·üí·ûö·ûπ·ûò·ûè·üí·ûö·ûº·ûú üëá"
                ),
            },
            "q_tech": {
                "label": "üò∞ ·ûÅ·üí·ûâ·ûª·üÜ·ûÅ·üí·ûõ·û∂·ûÖ·ûä·üÜ·û°·ûæ·ûÑ·ûò·û∑·ûì·ûî·û∂·ûì",
                "answer": (
                    "üò∞ *·ûò·û∑·ûì·ûÖ·üÅ·üá·ûî·ûÖ·üí·ûÖ·üÅ·ûÄ·ûú·û∑·ûë·üí·ûô·û∂ ‚Äî ·û¢·û∂·ûÖ·ûä·üÜ·û°·ûæ·ûÑ·ûî·û∂·ûì·ûë·üÅ?*\n\n"
                    "·ûî·û∂·ûì! ·ûì·üÅ·üá·ûá·û∂·û†·üÅ·ûè·ûª·ûï·ûõ:\n\n"
                    "‚úÖ ·ûÄ·û∂·ûö·ûé·üÇ·ûì·û∂·üÜ·ûá·û∂·ûó·û∂·ûü·û∂·ûÅ·üí·ûò·üÇ·ûö ·ûò·û∂·ûì·ûö·ûº·ûî·ûó·û∂·ûñ·ûî·ûÑ·üí·û†·û∂·ûâ·ûá·û∂·ûá·üÜ·û†·û∂·ûì·üó\n"
                    "‚úÖ ·ûò·û∂·ûì·ûú·û∏·ûä·üÅ·û¢·ûº·ûò·ûæ·ûõ·ûè·û∂·ûò\n"
                    "‚úÖ ·ûî·üí·ûö·ûæ Bot ·ûá·ûΩ·ûô 24/7\n"
                    "‚úÖ NiMo ·ûï·üí·ûë·û∂·ûõ·üã·ûÜ·üí·ûõ·ûæ·ûô·ûñ·üÅ·ûõ·ûè·üí·ûö·ûº·ûú·ûÄ·û∂·ûö\n\n"
                    "·ûÄ·ûâ·üí·ûÖ·ûî·üã VIP: NiMo ·û¢·ûÑ·üí·ûÇ·ûª·ûô·ûä·üÜ·û°·ûæ·ûÑ·ûá·û∂·ûò·ûΩ·ûô·ûî·ûÑ·ûè·û∂·ûò Zoom 2 ·ûò·üâ·üÑ·ûÑ ‚Äî "
                    "·ûî·ûÑ·ûÇ·üí·ûö·û∂·ûì·üã·ûè·üÇ·ûò·ûæ·ûõ ·û†·ûæ·ûô·ûÖ·ûª·ûÖ·ûè·û∂·ûò·üî üéØ"
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "üîç ·ûü·üí·ûú·üÇ·ûÑ·ûô·ûõ·üã·û¢·üÜ·ûñ·û∏ Cambodia Biz Agent",
                "questions": ["q_system", "q_which_plan", "q_tech"],
            },
        },
        "s": {
            "welcome": (
                "üëã ·ûü·ûΩ·ûü·üí·ûè·û∏! ·ûÅ·üí·ûâ·ûª·üÜ·ûá·û∂·ûá·üÜ·ûì·ûΩ·ûô·ûÄ·û∂·ûö·ûö·ûî·ûü·üã *NiMo Team*·üî\n\n"
                "·ûî·ûÑ·ûò·û∂·ûì·ûü·üÜ·ûé·ûΩ·ûö·û¢·üí·ûú·û∏·û¢·üÜ·ûñ·û∏ *Cambodia Biz Agent*?\n"
                "·ûá·üí·ûö·ûæ·ûü·ûü·üÜ·ûé·ûΩ·ûö·ûÅ·û∂·ûÑ·ûÄ·üí·ûö·üÑ·ûò ‚Äî ·ûÅ·üí·ûâ·ûª·üÜ·ûÜ·üí·ûõ·ûæ·ûô·ûó·üí·ûõ·û∂·ûò·üó üëá"
            ),
            "choose_cat":       "·ûá·üí·ûö·ûæ·ûü·ûü·üÜ·ûé·ûΩ·ûö·ûä·üÇ·ûõ·ûî·ûÑ·ûÖ·ûÑ·üã·ûä·ûπ·ûÑ:",
            "buy_title": (
                "üéâ *·ûõ·üí·û¢·ûé·û∂·ûü·üã! ·ûî·ûÑ·ûÖ·ûÑ·üã·ûá·üí·ûö·ûæ·ûü·ûÄ·ûâ·üí·ûÖ·ûî·üã·ûé·û∂?*\n\n"
                "üü¶ *Basic $97* ‚Äî ·ûü·û∂·ûÄ·ûõ·üí·ûî·ûÑ·ûò·ûª·ûì\n"
                "‚≠ê *Pro $297* ‚Äî ·ûü·üí·ûú·üê·ûô·ûî·üí·ûö·ûú·ûè·üí·ûè·û∑ 24/7\n"
                "üü° *VIP $597* ‚Äî NiMo ·ûä·üÜ·û°·ûæ·ûÑ·ûá·üÜ·ûì·ûΩ·ûü\n\n"
                "·ûá·üí·ûö·ûæ·ûü·ûÄ·ûâ·üí·ûÖ·ûî·üã üëá"
            ),
            "buy_btn":          "üí≥ ·ûÅ·üí·ûâ·ûª·üÜ·ûÖ·ûÑ·üã·ûë·û∑·ûâ·û•·û°·ûº·ûú",
            "consult_btn":      "üí¨ ·ûü·ûΩ·ûö NiMo ·ûä·üÑ·ûô·ûï·üí·ûë·û∂·ûõ·üã",
            "back_btn":         "‚¨ÖÔ∏è ·ûè·üí·ûö·û°·ûî·üã·ûë·üÖ·ûò·üâ·û∫·ûì·ûª·ûô",
            "back_cat":         "‚¨ÖÔ∏è ·ûü·üÜ·ûé·ûΩ·ûö·ûï·üí·ûü·üÅ·ûÑ·ûë·üÄ·ûè",
            "unsure_btn":       "ü§î ·ûÅ·üí·ûâ·ûª·üÜ·ûò·û∑·ûì·ûë·û∂·ûì·üã·ûî·üí·ûö·û∂·ûÄ·ûä ‚Äî ·ûè·üí·ûö·ûº·ûú·ûÄ·û∂·ûö·ûñ·û∑·ûÇ·üí·ûö·üÑ·üá",
            "consult_msg": (
                "üí¨ *·û¢·ûö·ûÇ·ûª·ûé·ûî·ûÑ·ûä·üÇ·ûõ·ûî·û∂·ûì·ûë·û∂·ûÄ·üã·ûë·ûÑ NiMo!*\n\n"
                "NiMo ·ûì·ûπ·ûÑ·ûÜ·üí·ûõ·ûæ·ûô·ûè·ûî·ûî·ûÑ·ûÜ·û∂·ûî·üã·üó·üî\n\n"
                "‚è≥ ·ûü·ûº·ûò·ûö·ûÑ·üã·ûÖ·û∂·üÜ·ûî·ûì·üí·ûè·û∑·ûÖ ‚ù§Ô∏è"
            ),
            "end_consult_btn":  "üîö ·ûî·ûâ·üí·ûÖ·ûî·üã ‚Äî ·ûè·üí·ûö·û°·ûî·üã·ûë·üÖ·ûò·üâ·û∫·ûì·ûª·ûô",
            "end_consult_msg":  "‚úÖ ·ûî·û∂·ûì·ûî·ûâ·üí·ûÖ·ûî·üã·üî ·û¢·ûö·ûÇ·ûª·ûé·ûî·ûÑ ‚ù§Ô∏è\n\n·ûÖ·ûª·ûÖ /start ·ûä·ûæ·ûò·üí·ûî·û∏·ûî·ûæ·ûÄ·ûò·üâ·û∫·ûì·ûª·ûô·üî",
            "confirm_paid_btn": "‚úÖ ·ûÅ·üí·ûâ·ûª·üÜ·ûî·û∂·ûì·ûï·üí·ûë·üÅ·ûö·ûî·üí·ûö·û∂·ûÄ·üã·ûö·ûΩ·ûÖ·û†·ûæ·ûô",
            "ask_more_btn":     "‚ùì ·ûÅ·üí·ûâ·ûª·üÜ·ûè·üí·ûö·ûº·ûú·ûÄ·û∂·ûö·ûü·ûΩ·ûö·ûî·ûì·üí·ûê·üÇ·ûò",
            "view_payment_btn": "üí≥ ·ûò·ûæ·ûõ·ûñ·üê·ûè·üå·ûò·û∂·ûì·ûï·üí·ûë·üÅ·ûö·ûî·üí·ûö·û∂·ûÄ·üã",
            "unknown_msg":      "·ûÅ·üí·ûâ·ûª·üÜ·ûë·ûë·ûΩ·ûõ·ûî·û∂·ûì·ûü·û∂·ûö·ûî·ûÑ·û†·ûæ·ûô ‚ù§Ô∏è\n\n·ûî·ûÑ·ûÖ·ûÑ·üã:",
            "ask_bill":         "üì∏ *·ûá·üÜ·û†·û∂·ûì·ûë·û∏ 1/3: ·ûï·üí·ûâ·ûæ·ûö·ûº·ûî·ûó·û∂·ûñ·ûî·ûÑ·üí·ûÄ·û∂·ûì·üã·ûä·üÉ*\n\n·ûü·ûº·ûò *·ûê·ûè·û¢·üÅ·ûÄ·üí·ûö·ûÑ·üã* ·ûÄ·û∂·ûö·ûï·üí·ûë·üÅ·ûö·ûî·üí·ûö·û∂·ûÄ·üã üëá",
            "need_photo":       "‚ö†Ô∏è ·ûü·ûº·ûò·ûï·üí·ûâ·ûæ *·ûö·ûº·ûî·ûó·û∂·ûñ* ·ûî·ûÑ·üí·ûÄ·û∂·ûì·üã·ûä·üÉ üì∏",
            "ask_name":         "‚úÖ ·ûë·ûë·ûΩ·ûõ·ûî·û∂·ûì·ûö·ûº·ûî·ûó·û∂·ûñ·û†·ûæ·ûô!\n\nüë§ *·ûá·üÜ·û†·û∂·ûì·ûë·û∏ 2/3: ·ûà·üí·ûò·üÑ·üá·ûñ·üÅ·ûâ*\n\n·ûü·ûº·ûò·ûú·û∂·ûô·ûà·üí·ûò·üÑ·üá·ûö·ûî·ûü·üã·ûî·ûÑ:",
            "need_text":        "‚ö†Ô∏è ·ûü·ûº·ûò·ûú·û∂·ûô·ûá·û∂·û¢·ûÄ·üí·ûü·ûö·üî",
            "ask_phone":        "‚úÖ ·ûë·ûë·ûΩ·ûõ·ûî·û∂·ûì·ûà·üí·ûò·üÑ·üá·û†·ûæ·ûô!\n\nüì± *·ûá·üÜ·û†·û∂·ûì·ûë·û∏ 3/3: ·ûõ·üÅ·ûÅ·ûë·ûº·ûö·ûü·üê·ûñ·üí·ûë*\n\n·ûü·ûº·ûò·ûî·ûâ·üí·ûÖ·ûº·ûõ·ûõ·üÅ·ûÅ·ûë·ûº·ûö·ûü·üê·ûñ·üí·ûë:",
            "complete_msg": (
                "üéâ *·ûë·ûë·ûΩ·ûõ·ûî·û∂·ûì·ûñ·üê·ûè·üå·ûò·û∂·ûì·ûÇ·üí·ûö·ûî·üã·ûÇ·üí·ûö·û∂·ûì·üã·û†·ûæ·ûô!*\n\n"
                "üìã *·ûü·ûÑ·üí·ûÅ·üÅ·ûî·ûÄ·û∂·ûö·ûî·ûâ·üí·ûá·û∂·ûë·û∑·ûâ:*\n"
                "‚Ä¢ ·ûõ·üÅ·ûÅ·ûÄ·ûº·ûä: `{order_id}`\n"
                "‚Ä¢ ·ûà·üí·ûò·üÑ·üá: {name}\n"
                "‚Ä¢ ·ûë·ûº·ûö·ûü·üê·ûñ·üí·ûë: {phone}\n"
                "‚Ä¢ ·ûÄ·ûâ·üí·ûÖ·ûî·üã: {label} ({price_usd})\n\n"
                "NiMo ·ûì·ûπ·ûÑ·ûñ·û∑·ûì·û∑·ûè·üí·ûô ·ûì·û∑·ûÑ·ûî·ûâ·üí·ûá·û∂·ûÄ·üã·ûÄ·üí·ûì·ûª·ûÑ *30 ·ûì·û∂·ûë·û∏* ‚è∞\n\n"
                "·û¢·ûö·ûÇ·ûª·ûé·ûî·ûÑ·ûä·üÇ·ûõ·ûë·ûª·ûÄ·ûÖ·û∑·ûè·üí·ûè NiMo ‚ù§Ô∏è"
            ),
            "package_msg": (
                "üéâ *·ûî·ûÑ·ûî·û∂·ûì·ûá·üí·ûö·ûæ·ûü {label} ‚Äî {price_usd}* ({price_riel})\n\n"
                "{bank_details}\n\n"
                "üíµ *·ûÖ·üÜ·ûì·ûΩ·ûì·ûë·ûπ·ûÄ·ûî·üí·ûö·û∂·ûÄ·üã: {price_usd}*\n\n"
                "·ûî·ûì·üí·ûë·û∂·ûî·üã·ûñ·û∏·ûï·üí·ûë·üÅ·ûö·ûî·üí·ûö·û∂·ûÄ·üã·û†·ûæ·ûô ·ûü·ûº·ûò·ûÖ·ûª·ûÖ·ûî·üä·ûº·ûè·ûª·ûÑ·ûÅ·û∂·ûÑ·ûÄ·üí·ûö·üÑ·ûò üëá"
            ),
        },
    },

    "en": {
        "faq": {
            "q_system": {
                "label": "üí¨ I don't understand how this system works",
                "answer": (
                    "üí¨ *How does Cambodia Biz Agent work?*\n\n"
                    "Simply put: you get *5 AI Employees* ‚Äî each does 1 job:\n\n"
                    "üîç Market research & competitor analysis\n"
                    "üì£ Create content for FB/TikTok/Instagram\n"
                    "üí∞ Write sales pages & close orders\n"
                    "üì¶ Auto-receive orders & send delivery notifications\n"
                    "üìä Revenue reports & weekly optimization\n\n"
                    "You give commands in Khmer or English ‚Äî AI works instantly.\n\n"
                    "No coding needed. üöÄ"
                ),
            },
            "q_which_plan": {
                "label": "ü§î I don't know which plan fits me",
                "answer": (
                    "ü§î *Which plan fits your shop?*\n\n"
                    "üü¶ *Basic $97* ‚Äî New to AI, want to try first\n"
                    "‚Üí 5 AI Employees + Khmer guide + 30-day support\n\n"
                    "‚≠ê *Pro $297* ‚Äî Shop running, want full automation 24/7\n"
                    "‚Üí Chatbot + auto-post + auto-booking\n\n"
                    "üü° *VIP $597* ‚Äî Don't want to install yourself\n"
                    "‚Üí NiMo installs everything, ready to use, 90-day support\n\n"
                    "Not sure? Tell NiMo about your shop ‚Äî we'll recommend the right plan in 5 mins üëá"
                ),
            },
            "q_tech": {
                "label": "üò∞ I'm afraid I can't install it",
                "answer": (
                    "üò∞ *Not tech-savvy ‚Äî can I still install it?*\n\n"
                    "Yes! Here's why:\n\n"
                    "‚úÖ Step-by-step guide in Khmer with images\n"
                    "‚úÖ Video tutorials to follow\n"
                    "‚úÖ Bot support 24/7\n"
                    "‚úÖ NiMo personally answers when needed\n\n"
                    "VIP plan: NiMo installs it with you via Zoom in 2 hours ‚Äî "
                    "you just watch and click. üéØ"
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "üîç Learn about Cambodia Biz Agent",
                "questions": ["q_system", "q_which_plan", "q_tech"],
            },
        },
        "s": {
            "welcome": (
                "üëã Hello! I'm the assistant of *NiMo Team*.\n\n"
                "What are you wondering about *Cambodia Biz Agent*?\n"
                "Choose a question below ‚Äî I'll answer right away üëá"
            ),
            "choose_cat":       "Choose a question:",
            "buy_title": (
                "üéâ *Great! Which plan do you want?*\n\n"
                "üü¶ *Basic $97* ‚Äî Try it first\n"
                "‚≠ê *Pro $297* ‚Äî Full automation 24/7\n"
                "üü° *VIP $597* ‚Äî NiMo installs it for you\n\n"
                "Choose a plan üëá"
            ),
            "buy_btn":          "üí≥ I WANT TO BUY NOW",
            "consult_btn":      "üí¨ Chat directly with NiMo",
            "back_btn":         "‚¨ÖÔ∏è Back to main menu",
            "back_cat":         "‚¨ÖÔ∏è Other questions",
            "unsure_btn":       "ü§î I'm not sure ‚Äî need advice",
            "consult_msg": (
                "üí¨ *Thank you for contacting NiMo!*\n\n"
                "Your message has been forwarded to our team.\n\n"
                "‚è≥ Please wait a moment ‚Äî we'll reply shortly. ‚ù§Ô∏è"
            ),
            "end_consult_btn":  "üîö End consultation ‚Äî back to menu",
            "end_consult_msg":  "‚úÖ Consultation ended. Thank you ‚ù§Ô∏è\n\nType /start to open the menu again.",
            "confirm_paid_btn": "‚úÖ I have transferred ‚Äî send receipt",
            "ask_more_btn":     "‚ùì I have more questions",
            "view_payment_btn": "üí≥ View payment details",
            "unknown_msg":      "I received your message ‚ù§Ô∏è\n\nWhat would you like to do?",
            "ask_bill":         "üì∏ *Step 1/3: Send payment receipt*\n\nPlease *screenshot* the bank transfer confirmation üëá",
            "need_photo":       "‚ö†Ô∏è Please send a *photo* of your receipt üì∏",
            "ask_name":         "‚úÖ Receipt received!\n\nüë§ *Step 2/3: Full name*\n\nPlease enter your full name:",
            "need_text":        "‚ö†Ô∏è Please enter text.",
            "ask_phone":        "‚úÖ Name received!\n\nüì± *Step 3/3: Phone number*\n\nPlease enter your phone number:",
            "complete_msg": (
                "üéâ *All information received!*\n\n"
                "üìã *Order summary:*\n"
                "‚Ä¢ Order ID: `{order_id}`\n"
                "‚Ä¢ Name: {name}\n"
                "‚Ä¢ Phone: {phone}\n"
                "‚Ä¢ Plan: {label} ({price_usd})\n\n"
                "NiMo will verify and confirm within *30 minutes* ‚è∞\n\n"
                "Thank you for trusting NiMo ‚ù§Ô∏è"
            ),
            "package_msg": (
                "üéâ *You selected {label} ‚Äî {price_usd}* ({price_riel})\n\n"
                "{bank_details}\n\n"
                "üíµ *Amount to transfer: {price_usd}*\n\n"
                "After transferring, tap the button below to send your receipt üëá"
            ),
        },
    },
}

# ‚îÄ‚îÄ‚îÄ HELPERS ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

def get_lang(context) -> str:
    return context.user_data.get("lang", "km")

def C(context):
    return CONTENT[get_lang(context)]

# ‚îÄ‚îÄ‚îÄ KEYBOARDS ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("üá∞üá≠ ·ûó·û∂·ûü·û∂·ûÅ·üí·ûò·üÇ·ûö", callback_data="lang_km"),
        InlineKeyboardButton("üá¨üáß English",    callback_data="lang_en"),
    ]])

def main_menu_keyboard(context):
    c = C(context)
    s = c["s"]
    buttons = [
        [InlineKeyboardButton(cat["label"], callback_data=cat_id)]
        for cat_id, cat in c["cats"].items()
    ]
    buttons.append([InlineKeyboardButton(s["buy_btn"],     callback_data="buy")])
    buttons.append([InlineKeyboardButton(s["consult_btn"], callback_data="consult")])
    return InlineKeyboardMarkup(buttons)

def category_menu_keyboard(cat_id, context):
    c = C(context)
    cat = c["cats"][cat_id]
    buttons = [
        [InlineKeyboardButton(c["faq"][q_id]["label"], callback_data=q_id)]
        for q_id in cat["questions"]
    ]
    buttons.append([InlineKeyboardButton(c["s"]["back_btn"], callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)

def after_answer_keyboard(cat_id, context):
    s = C(context)["s"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["buy_btn"],     callback_data="buy")],
        [InlineKeyboardButton(s["back_cat"],    callback_data=cat_id)],
        [InlineKeyboardButton(s["back_btn"],    callback_data="main_menu")],
        [InlineKeyboardButton(s["consult_btn"], callback_data="consult")],
    ])

def buy_keyboard(context):
    s = C(context)["s"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("üü¶ Basic $97  (‚âà 400,000 Riel)",   callback_data="buy_basic")],
        [InlineKeyboardButton("‚≠ê Pro $297   (‚âà 1,200,000 Riel)", callback_data="buy_pro")],
        [InlineKeyboardButton("üü° VIP $597  (‚âà 2,400,000 Riel)",  callback_data="buy_vip")],
        [InlineKeyboardButton(s["unsure_btn"], callback_data="q_which_plan")],
        [InlineKeyboardButton(s["back_btn"],   callback_data="main_menu")],
    ])

def confirm_transfer_keyboard(context):
    s = C(context)["s"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["confirm_paid_btn"], callback_data="confirm_paid")],
        [InlineKeyboardButton(s["ask_more_btn"],     callback_data="main_menu")],
    ])

def end_consult_keyboard(context):
    s = C(context)["s"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["end_consult_btn"], callback_data="end_consult")],
    ])

# ‚îÄ‚îÄ‚îÄ HANDLERS ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "üá∞üá≠ ·ûá·üí·ûö·ûæ·ûü·ûó·û∂·ûü·û∂  |  üá¨üáß Choose language:",
        reply_markup=lang_keyboard()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data  = query.data

    # Language selection
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        context.user_data["lang"] = lang
        c = CONTENT[lang]
        await query.edit_message_text(
            c["s"]["welcome"],
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(context)
        )
        return

    c = C(context)
    s = c["s"]

    # Main menu
    if data == "main_menu":
        await query.edit_message_text(
            s["welcome"],
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(context)
        )
        return

    # Category
    if data in c["cats"]:
        cat = c["cats"][data]
        await query.edit_message_text(
            f"*{cat['label']}*\n\n{s['choose_cat']}",
            parse_mode="Markdown",
            reply_markup=category_menu_keyboard(data, context)
        )
        return

    # FAQ answer
    if data in c["faq"]:
        cat_id = next(
            (cid for cid, cat in c["cats"].items() if data in cat["questions"]),
            "main_menu"
        )
        await query.edit_message_text(
            c["faq"][data]["answer"],
            parse_mode="Markdown",
            reply_markup=after_answer_keyboard(cat_id, context)
        )
        return

    # Buy menu
    if data == "buy":
        await query.edit_message_text(
            s["buy_title"],
            parse_mode="Markdown",
            reply_markup=buy_keyboard(context)
        )
        return

    # Package selected
    if data.startswith("buy_"):
        package = data.split("_")[1]
        info    = BANK_INFO[package]
        context.user_data["package"] = package
        lang    = get_lang(context)
        msg = s["package_msg"].format(
            label=info["label"],
            price_usd=info["price_usd"],
            price_riel=info["price_riel"],
            bank_details=BANK_DETAILS[lang]
        )
        await query.edit_message_text(
            msg,
            parse_mode="Markdown",
            reply_markup=confirm_transfer_keyboard(context)
        )
        return

    # Consult
    if data == "consult":
        context.user_data["consulting"] = True
        await query.edit_message_text(
            s["consult_msg"],
            parse_mode="Markdown",
            reply_markup=end_consult_keyboard(context)
        )
        if ADMIN_ID:
            user = query.from_user
            lang = get_lang(context)
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=(
                        f"üí¨ *Kh√°ch c·∫ßn t∆∞ v·∫•n [{lang.upper()}]*\n"
                        f"üë§ {user.full_name} (@{user.username or 'no username'})\n"
                        f"`#cid:{user.id}`"
                    ),
                    parse_mode="Markdown"
                )
            except Exception as e:
                logging.error(f"Admin notify error: {e}")
        return

    # End consult
    if data == "end_consult":
        context.user_data["consulting"] = False
        await query.edit_message_text(s["end_consult_msg"])
        return

    # Confirm paid
    if data == "confirm_paid":
        if "package" not in context.user_data:
            await query.edit_message_text(s["welcome"], reply_markup=main_menu_keyboard(context))
            return
        context.user_data["awaiting"] = "bill_photo"
        await query.edit_message_text(s["ask_bill"], parse_mode="Markdown")
        return

# ‚îÄ‚îÄ‚îÄ MESSAGE HANDLER ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    awaiting   = context.user_data.get("awaiting")
    consulting = context.user_data.get("consulting", False)
    user       = update.effective_user
    s          = C(context)["s"]

    # Admin reply ‚Üí forward to customer
    if (
        user.id == ADMIN_ID
        and update.message.reply_to_message
        and update.message.reply_to_message.text
        and "#cid:" in update.message.reply_to_message.text
    ):
        try:
            cid_text = update.message.reply_to_message.text.split("#cid:")[1].strip()
            cust_id  = int(cid_text.split()[0])
            await context.bot.send_message(
                chat_id=cust_id,
                text=f"üí¨ *NiMo:*\n\n{update.message.text}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("‚úÖ Sent.")
        except Exception as e:
            await update.message.reply_text(f"‚ùå {e}")
        return

    # Consulting mode ‚Üí forward to admin
    if consulting and not awaiting:
        text = update.message.text or "(media)"
        if ADMIN_ID:
            try:
                fwd = (
                    f"üí¨ *{user.full_name}* (@{user.username or 'no username'})\n"
                    f"‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ\n{text}\n‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ‚îÅ\n`#cid:{user.id}`"
                )
                await context.bot.send_message(chat_id=ADMIN_ID, text=fwd, parse_mode="Markdown")
                if update.message.photo:
                    await context.bot.send_photo(
                        chat_id=ADMIN_ID,
                        photo=update.message.photo[-1].file_id,
                        caption=f"üì∏ {user.full_name}\n`#cid:{user.id}`",
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logging.error(f"Forward error: {e}")
        await update.message.reply_text("‚úÖ", reply_markup=end_consult_keyboard(context))
        return

    # No active flow ‚Üí show options
    if not awaiting:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(s["view_payment_btn"], callback_data="buy")],
            [InlineKeyboardButton(s["consult_btn"],      callback_data="consult")],
            [InlineKeyboardButton(s["back_btn"],         callback_data="main_menu")],
        ])
        await update.message.reply_text(s["unknown_msg"], reply_markup=kb)
        return

    # Bill photo step
    if awaiting == "bill_photo":
        if not update.message.photo:
            await update.message.reply_text(s["need_photo"], parse_mode="Markdown")
            return
        context.user_data["bill_photo_id"] = update.message.photo[-1].file_id
        context.user_data["awaiting"]       = "name"
        await update.message.reply_text(s["ask_name"], parse_mode="Markdown")
        return

    # Name step
    if awaiting == "name":
        if not update.message.text:
            await update.message.reply_text(s["need_text"])
            return
        context.user_data["name"]     = update.message.text.strip()
        context.user_data["awaiting"] = "phone"
        await update.message.reply_text(s["ask_phone"], parse_mode="Markdown")
        return

    # Phone step ‚Üí complete
    if awaiting == "phone":
        if not update.message.text:
            await update.message.reply_text(s["need_text"])
            return
        from datetime import datetime
        context.user_data["phone"]    = update.message.text.strip()
        context.user_data["order_id"] = f"NIMO-{datetime.now().strftime('%y%m%d-%H%M')}"
        context.user_data["awaiting"] = None

        package = context.user_data["package"]
        info    = BANK_INFO[package]

        await update.message.reply_text(
            s["complete_msg"].format(
                order_id=context.user_data["order_id"],
                name=context.user_data["name"],
                phone=context.user_data["phone"],
                label=info["label"],
                price_usd=info["price_usd"]
            ),
            parse_mode="Markdown"
        )

        if ADMIN_ID:
            lang = get_lang(context)
            msg  = (
                f"üî¥ *ƒê∆†N M·ªöI [{lang.upper()}]*\n\n"
                f"üìã M√£ ƒë∆°n: `{context.user_data['order_id']}`\n"
                f"üë§ T√™n: {context.user_data['name']}\n"
                f"üì± SƒêT: {context.user_data['phone']}\n"
                f"üì¶ G√≥i: *{info['label']}* ‚Äî {info['price_usd']}\n"
                f"üÜî Telegram ID: `{user.id}`\n\n"
                f"üëâ L·ªánh x√°c nh·∫≠n:\n"
                f"`/xacnhan {context.user_data['order_id']} {package}`"
            )
            try:
                await context.bot.send_photo(
                    chat_id=ADMIN_ID,
                    photo=context.user_data["bill_photo_id"],
                    caption=msg,
                    parse_mode="Markdown"
                )
            except Exception as e:
                logging.error(f"Admin notify error: {e}")
        return

# ‚îÄ‚îÄ‚îÄ ADMIN COMMANDS ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

async def xacnhan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("‚õî")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Syntax: `/xacnhan NIMO-ID package`", parse_mode="Markdown")
        return
    await update.message.reply_text(
        f"‚úÖ Confirmed order `{context.args[0]}` ‚Äî plan `{context.args[1]}`.\n"
        "_Auto-delivery will be added in the next step._",
        parse_mode="Markdown"
    )

async def tra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin replies to customer: /tra <customer_id> <message>"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("‚õî")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Syntax: `/tra <customer_id> <message>`", parse_mode="Markdown")
        return
    try:
        cid  = int(context.args[0])
        text = " ".join(context.args[1:])
        await context.bot.send_message(
            chat_id=cid,
            text=f"üí¨ *NiMo:*\n\n{text}",
            parse_mode="Markdown"
        )
        await update.message.reply_text("‚úÖ Sent.")
    except Exception as e:
        await update.message.reply_text(f"‚ùå {e}")

# ‚îÄ‚îÄ‚îÄ MAIN ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("xacnhan", xacnhan))
    app.add_handler(CommandHandler("tra",     tra))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_message))
    print("‚úÖ Bot (KM + EN) ƒëang ch·∫°y... /start ƒë·ªÉ test!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
