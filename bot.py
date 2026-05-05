"""
Cambodia Biz Agent \u2014 Bot Khmer + English
FAQ + buy flow + admin support
Token: @NiMoBizAgent_bot (Railway)
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# \u2500\u2500\u2500 CONFIG \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

TOKEN    = "8750588238:AAFUJ3o6iR7Cu92on2HdsvLhKP5pQHs15Bo"
ADMIN_ID = 8704923191

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# \u2500\u2500\u2500 PAYMENT INFO \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

BANK_INFO = {
    "basic": {"label": "Basic", "price_usd": "$97",  "price_riel": "\u2248 400,000 Riel"},
    "pro":   {"label": "Pro",   "price_usd": "$297", "price_riel": "\u2248 1,200,000 Riel"},
    "vip":   {"label": "VIP",   "price_usd": "$597", "price_riel": "\u2248 2,400,000 Riel"},
}

BANK_DETAILS = {
    "km": (
        "\U0001F4B3 *\u1796\u17D0\u178F\u17CC\u1798\u17B6\u1793\u1780\u17B6\u179A\u1795\u17D2\u1791\u17C1\u179A\u1794\u17D2\u179A\u17B6\u1780\u17CB*\n\n"
        "\U0001F3E6 *ABA Bank*\n"
        "\u179B\u17C1\u1781\u1782\u178E\u1793\u17B8: `000 123 456`\n"
        "\u1788\u17D2\u1798\u17C4\u17C7: NIMO TEAM\n\n"
        "\U0001F4F1 *Wing Money*\n"
        "\u179B\u17C1\u1781\u1791\u17BC\u179A\u179F\u17D0\u1796\u17D2\u1791: `012 345 678`\n"
        "\u1788\u17D2\u1798\u17C4\u17C7: NIMO TEAM\n\n"
        "\u26A0\uFE0F *\u179F\u1798\u17D2\u1782\u17B6\u179B\u17CB:* \u179F\u17BC\u1798\u179F\u179A\u179F\u17C1\u179A\u179B\u17C1\u1781\u1780\u17BC\u178A\u1794\u1789\u17D2\u1787\u17B6\u1791\u17B7\u1789 NiMo \u1795\u17D2\u1789\u17BE\u17A2\u17C4\u1799 \u1780\u17D2\u1793\u17BB\u1784\u1780\u17B6\u179A\u1795\u17D2\u1791\u17C1\u179A\u17D4"
    ),
    "en": (
        "\U0001F4B3 *Payment Details*\n\n"
        "\U0001F3E6 *ABA Bank*\n"
        "Account: `000 123 456`\n"
        "Name: NIMO TEAM\n\n"
        "\U0001F4F1 *Wing Money*\n"
        "Phone: `012 345 678`\n"
        "Name: NIMO TEAM\n\n"
        "\u26A0\uFE0F *Note:* Include the order code NiMo provides in the transfer remark."
    ),
}

# \u2500\u2500\u2500 CONTENT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

CONTENT = {
    "km": {
        "faq": {
            "q_nimo": {
                "label": "\U0001F464 NiMo \u1787\u17B6\u1793\u179A\u178E\u17B6?",
                "answer": (
                    "\U0001F464 *NiMo \u1787\u17B6\u1793\u179A\u178E\u17B6?*\n\n"
                    "NiMo \u1794\u17B6\u1793\u1780\u17BE\u178F\u1785\u17C1\u1789\u1796\u17B8\u1794\u17C6\u178E\u1784\u1794\u17D2\u179A\u17B6\u1790\u17D2\u1793\u17B6\u1798\u17BD\u1799:\n\n"
                    "_\u1785\u1784\u17CB\u1785\u17C6\u178E\u17BC\u179B\u179A\u17BD\u1798\u17A2\u17D2\u179C\u17B8\u1798\u17BD\u1799\u1798\u17B6\u1793\u17A2\u178F\u17D2\u1790\u1793\u17D0\u1799 \u178A\u179B\u17CB\u179F\u17A0\u1782\u1798\u1793\u17CD\u17A2\u17B6\u1787\u17B8\u179C\u1780\u1798\u17D2\u1798\u1793\u17C5\u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6\u17D4_\n\n"
                    "\u1781\u178E\u17C8\u1794\u17D2\u179A\u1791\u17C1\u179F\u1787\u17B7\u178F\u1781\u17B6\u1784\u1794\u17D2\u179A\u17BE AI \u179F\u17D2\u179C\u17D0\u1799\u1794\u17D2\u179A\u179C\u178F\u17D2\u178F\u17B7\u178F\u17B6\u17C6\u1784\u1796\u17B8\u1799\u17BC\u179A \u2014 "
                    "\u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784\u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6\u1787\u17B6\u1785\u17D2\u179A\u17BE\u1793\u1793\u17C5\u1792\u17D2\u179C\u17BE\u1780\u17B6\u179A\u178A\u17C4\u1799\u178A\u17C3\u17D4 "
                    "\u1798\u17B7\u1793\u1798\u17C2\u1793\u1798\u17B7\u1793\u1785\u1784\u17CB\u1794\u17D2\u178A\u17BC\u179A \u2014 \u1782\u17D2\u179A\u17B6\u1793\u17CB\u178F\u17C2\u1798\u17B7\u1793\u1791\u17B6\u1793\u17CB\u1798\u17B6\u1793\u17A7\u1794\u1780\u179A\u178E\u17CD\u179F\u1798\u179F\u17D2\u179A\u1794\u17D4\n\n"
                    "NiMo \u1780\u17BE\u178F\u17A1\u17BE\u1784\u178A\u17BE\u1798\u17D2\u1794\u17B8\u1794\u17C6\u1796\u17C1\u1789\u1785\u1793\u17D2\u179B\u17C4\u17C7\u1793\u17C4\u17C7 \u2014 "
                    "\u1787\u17BD\u1799\u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784\u1781\u17D2\u1798\u17C2\u179A access AI \u178A\u17C4\u1799\u1784\u17B6\u1799 \u1787\u17B6\u1797\u17B6\u179F\u17B6\u179A\u1794\u179F\u17CB\u1781\u17D2\u179B\u17BD\u1793\u17D4"
                ),
            },
            "q_system": {
                "label": "\U0001F4AC \u1781\u17D2\u1789\u17BB\u17C6\u1798\u17B7\u1793\u1791\u17B6\u1793\u17CB\u1799\u179B\u17CB\u1785\u17D2\u1794\u17B6\u179F\u17CB\u17A2\u17C6\u1796\u17B8\u1794\u17D2\u179A\u1796\u17D0\u1793\u17D2\u1792\u1793\u17C1\u17C7",
                "answer": (
                    "\U0001F4AC *\u1794\u17D2\u179A\u1796\u17D0\u1793\u17D2\u1792 Cambodia Biz Agent \u178A\u17C6\u178E\u17BE\u179A\u1780\u17B6\u179A\u1799\u17C9\u17B6\u1784\u178A\u17BC\u1785\u1798\u17D2\u178F\u17C1\u1785?*\n\n"
                    "\u1799\u179B\u17CB\u17B1\u17D2\u1799\u179F\u17B6\u1798\u1789\u17D2\u1789: \u1794\u1784 \u1798\u17B6\u1793 *\u1794\u17BB\u1782\u17D2\u1782\u179B\u17B7\u1780 AI \u1785\u17C6\u1793\u17BD\u1793 5 \u1793\u17B6\u1780\u17CB* \u2014 \u1798\u17D2\u1793\u17B6\u1780\u17CB\u1792\u17D2\u179C\u17BE\u1780\u17B6\u179A\u1784\u17B6\u179A 1:\n\n"
                    "\U0001F50D \u179F\u17D2\u179A\u17B6\u179C\u1787\u17D2\u179A\u17B6\u179C\u1791\u17B8\u1795\u17D2\u179F\u17B6\u179A \u1793\u17B7\u1784\u1782\u17BC\u1794\u17D2\u179A\u1787\u17C2\u1784\n"
                    "\U0001F4E3 \u1794\u1784\u17D2\u1780\u17BE\u178F\u1798\u17B6\u178F\u17B7\u1780\u17B6 FB/TikTok/Instagram\n"
                    "\U0001F4B0 \u179F\u179A\u179F\u17C1\u179A\u1791\u17C6\u1796\u17D0\u179A\u179B\u1780\u17CB \u1793\u17B7\u1784\u1794\u17B7\u1791\u1780\u17B6\u179A\u1794\u1789\u17D2\u1787\u17B6\u1791\u17B7\u1789\n"
                    "\U0001F4E6 \u1791\u1791\u17BD\u179B\u1780\u17B6\u179A\u1794\u1789\u17D2\u1787\u17B6\u1791\u17B7\u1789 \u1793\u17B7\u1784\u1787\u17BC\u1793\u178A\u17C6\u178E\u17B9\u1784\u178A\u17C4\u1799\u179F\u17D2\u179C\u17D0\u1799\u1794\u17D2\u179A\u179C\u178F\u17D2\u178F\u17B7\n"
                    "\U0001F4CA \u179A\u1794\u17B6\u1799\u1780\u17B6\u179A\u178E\u17CD\u1785\u17C6\u178E\u17BC\u179B \u1793\u17B7\u1784\u1794\u1784\u17D2\u1780\u17BE\u1793\u1794\u17D2\u179A\u179F\u17B7\u1791\u17D2\u1792\u1797\u17B6\u1796\n\n"
                    "\u1794\u1784\u1794\u1789\u17D2\u1787\u17B6\u1787\u17B6\u1797\u17B6\u179F\u17B6\u1781\u17D2\u1798\u17C2\u179A \u2014 AI \u1792\u17D2\u179C\u17BE\u1780\u17B6\u179A\u1797\u17D2\u179B\u17B6\u1798\u17D7\u17D4\n\n"
                    "\u1798\u17B7\u1793\u1785\u17B6\u17C6\u1794\u17B6\u1785\u17CB\u1785\u17C1\u17C7\u179F\u179A\u179F\u17C1\u179A\u1780\u17BC\u178A\u17D4 \U0001F680"
                ),
            },
            "q_different": {
                "label": "\U0001F19A Cambodia Biz Agent \u1781\u17BB\u179F\u1796\u17B8 Agent \u178A\u1791\u17C3?",
                "answer": (
                    "\U0001F19A *Cambodia Biz Agent \u1781\u17BB\u179F\u1796\u17B8 Agent \u178A\u1791\u17C3\u178A\u17BC\u1785\u1798\u17D2\u178A\u17C1\u1785?*\n\n"
                    "AI Agent \u1787\u17B6\u1785\u17D2\u179A\u17BE\u1793\u178F\u17D2\u179A\u17BC\u179C\u1794\u17B6\u1793\u179F\u17B6\u1784\u179F\u1784\u17CB\u179F\u1798\u17D2\u179A\u17B6\u1794\u17CB\u1791\u17B8\u1795\u17D2\u179F\u17B6\u179A\u1781\u17B6\u1784\u179B\u17B7\u1785 \u2014 "
                    "\u1797\u17B6\u179F\u17B6\u17A2\u1784\u17CB\u1782\u17D2\u179B\u17C1\u179F Stripe payments \u179F\u17D2\u1791\u17B8\u179B US/EU \u17D4\n\n"
                    "*Cambodia Biz Agent \u1781\u17BB\u179F: \u179F\u17B6\u1784\u179F\u1784\u17CB\u1787\u17B6\u1796\u17B7\u179F\u17C1\u179F\u179F\u1798\u17D2\u179A\u17B6\u1794\u17CB\u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784\u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6\u17D4*\n\n"
                    "\U0001F1F0\U0001F1ED *\u1797\u17B6\u179F\u17B6:* \u1781\u17D2\u1798\u17C2\u179A\u1792\u1798\u17D2\u1798\u1787\u17B6\u178F\u17B7 \u2014 \u1798\u17B7\u1793\u1798\u17C2\u1793 google translate\n\n"
                    "\U0001F4B3 *\u1780\u17B6\u179A\u1791\u17BC\u1791\u17B6\u178F\u17CB:* ABA Pay, Wing Money, Bakong KHQR \u2014 \u1782\u17D2\u1798\u17B6\u1793\u1780\u17B6\u178F\u17A2\u1793\u17D2\u178F\u179A\u1787\u17B6\u178F\u17B7\n\n"
                    "\U0001F4F1 *\u179C\u17C1\u1791\u17B7\u1780\u17B6:* Facebook, TikTok, Telegram \u2014 \u178F\u17D2\u179A\u17BC\u179C\u1787\u17B6\u1780\u1793\u17D2\u179B\u17C2\u1784\u1781\u17D2\u1798\u17C2\u179A\u1791\u17B7\u1789\n\n"
                    "\U0001F91D *\u1787\u17C6\u1793\u17BD\u1799:* NiMo \u1793\u17C5\u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6 \u1799\u179B\u17CB\u1791\u17B8\u1795\u17D2\u179F\u17B6\u179A \u1787\u17BD\u1799\u1795\u17D2\u1791\u17B6\u179B\u17CB\n\n"
                    "\u179F\u17B6\u1784\u179F\u1784\u17CB\u1796\u17B8\u1797\u17B6\u1796\u1787\u17B6\u1780\u17CB\u179F\u17D2\u178A\u17C2\u1784\u1793\u17C3\u1791\u17B8\u1795\u17D2\u179F\u17B6\u179A\u1793\u17C1\u17C7 \u2014 \u1798\u17B7\u1793\u1798\u17C2\u1793 copy \u1796\u17B8\u1780\u1793\u17D2\u179B\u17C2\u1784\u1795\u17D2\u179F\u17C1\u1784\u17D4"
                ),
            },
            "q_save": {
                "label": "\U0001F4B0 \u1781\u17D2\u1789\u17BB\u17C6\u1793\u17B9\u1784\u179F\u1793\u17D2\u179F\u17C6\u1794\u17B6\u1793\u17A2\u17D2\u179C\u17B8?",
                "answer": (
                    "\U0001F4B0 *\u1794\u17D2\u179A\u1796\u17D0\u1793\u17D2\u1792\u1793\u17C1\u17C7\u1787\u17BD\u1799\u1781\u17D2\u1789\u17BB\u17C6\u179F\u1793\u17D2\u179F\u17C6\u1794\u17B6\u1793\u17A2\u17D2\u179C\u17B8?*\n\n"
                    "\u17A2\u17D2\u179C\u17B8\u178A\u17C2\u179B\u1794\u1784\u179F\u1793\u17D2\u179F\u17C6\u1794\u17B6\u1793\u1785\u17D2\u179A\u17BE\u1793\u1794\u17C6\u1795\u17BB\u178F \u2014 \u1798\u17B7\u1793\u1798\u17C2\u1793\u179B\u17BB\u1799\u17D4 \u1796\u17C1\u179B\u179C\u17C1\u179B\u17B6\u17D4\n\n"
                    "\u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784\u1787\u17B6\u1798\u1792\u17D2\u1799\u1798\u1798\u17B6\u1793 3 \u1798\u17C9\u17C4\u1784/\u1790\u17D2\u1784\u17C3 \u1785\u17C6\u178E\u17B6\u1799\u179B\u17BE\u1780\u17B6\u179A\u1784\u17B6\u179A\u178A\u178A\u17C2\u179B\u17D7:\n"
                    "\u179F\u179A\u179F\u17C1\u179A caption \u1786\u17D2\u179B\u17BE\u1799\u179F\u17B6\u179A \u1794\u17D2\u179A\u1780\u17B6\u179F \u17D4\n\n"
                    "*3 \u1798\u17C9\u17C4\u1784 \u00D7 30 \u1790\u17D2\u1784\u17C3 = 90 \u1798\u17C9\u17C4\u1784/\u1781\u17C2* \u2014 Cambodia Biz Agent \u1792\u17D2\u179C\u17BE\u1787\u17C6\u1793\u17BD\u179F\u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1785\u17C6\u1796\u17C4\u17C7 cost:\n\n"
                    "\U0001F50D \u179F\u17D2\u179A\u17B6\u179C\u1787\u17D2\u179A\u17B6\u179C: $100\u2013200/\u178A\u1784\n"
                    "\U0001F4E3 Content: $50\u2013150/\u1781\u17C2\n"
                    "\U0001F4AC Inbox: $200\u2013300/\u1781\u17C2\n"
                    "\U0001F4E6 \u178A\u17C4\u17C7\u179F\u17D2\u179A\u17B6\u1799\u1780\u17B6\u179A\u1794\u1789\u17D2\u1787\u17B6\u1791\u17B7\u1789: $150\u2013250/\u1781\u17C2\n"
                    "\U0001F4CA \u179A\u1794\u17B6\u1799\u1780\u17B6\u179A\u178E\u17CD: $100\u2013200/\u1781\u17C2\n\n"
                    "*\u1787\u17BD\u179B\u1798\u1793\u17BB\u179F\u17D2\u179F: ~$700\u20131,200/\u1781\u17C2*\n\n"
                    "Cambodia Biz Agent: \u1798\u17D2\u178A\u1784\u1794\u17C9\u17BB\u178E\u17D2\u178E\u17C4\u17C7 \U0001F7E6$97 \u00B7 \u2B50$297 \u00B7 \U0001F7E1$597\n\n"
                    "\u1786\u17D2\u1793\u17B6\u17C6\u178A\u17C6\u1794\u17BC\u1784 \u179F\u1793\u17D2\u179F\u17C6 *$8,000\u201314,000* \U0001F4B0"
                ),
            },
            "q_location": {
                "label": "\U0001F3E2 \u1780\u17B6\u179A\u17B7\u1799\u17B6\u179B\u17D0\u1799 NiMo \u1793\u17C5\u1791\u17B8\u178E\u17B6?",
                "answer": (
                    "\U0001F3E2 *\u1780\u17B6\u179A\u17B7\u1799\u17B6\u179B\u17D0\u1799 NiMo \u1793\u17C5\u1791\u17B8\u178E\u17B6?*\n\n"
                    "NiMo \u178A\u17C6\u178E\u17BE\u179A\u1780\u17B6\u179A online \u1791\u17B6\u17C6\u1784\u179F\u17D2\u179A\u17BB\u1784 \u2014 \u1782\u17D2\u1798\u17B6\u1793\u1780\u17B6\u179A\u17B7\u1799\u17B6\u179B\u17D0\u1799 physical \u17D4 "
                    "\u178A\u17BC\u1785\u1796\u17C1\u179B\u1794\u1784\u1791\u17B7\u1789 app \u17AC course online \u2014 "
                    "\u1782\u17D2\u1798\u17B6\u1793\u1780\u17B6\u179A\u17B7\u1799\u17B6\u179B\u17D0\u1799 \u1780\u17CF\u1794\u17D2\u179A\u17BE\u1794\u17B6\u1793\u1792\u1798\u17D2\u1798\u178F\u17B6\u17D4\n\n"
                    "\u17A2\u17D2\u179C\u17B8\u179F\u17C6\u1781\u17B6\u1793\u17CB: NiMo \u1792\u17B6\u1793\u17B6 *30 \u1790\u17D2\u1784\u17C3 \u1794\u1784\u17D2\u179C\u17B7\u179B\u179B\u17BB\u1799 100%* "
                    "\u1794\u17D2\u179A\u179F\u17B7\u1793\u1794\u17BE\u1794\u1784\u1798\u17B7\u1793\u1796\u17C1\u1789\u1785\u17B7\u178F\u17D2\u178F\u17D4 \u2764\uFE0F"
                ),
            },
            "q_price": {
                "label": "\U0001F4B5 Cambodia Biz Agent \u178F\u1798\u17D2\u179B\u17C3\u1794\u17C9\u17BB\u1793\u17D2\u1798\u17B6\u1793?",
                "answer": (
                    "\U0001F4B5 *Cambodia Biz Agent \u178F\u1798\u17D2\u179B\u17C3\u1794\u17C9\u17BB\u1793\u17D2\u1798\u17B6\u1793? \u1798\u17B6\u1793\u1790\u17D2\u179B\u17C3/\u1781\u17C2?*\n\n"
                    "\u1791\u17B7\u1789\u1798\u17D2\u178A\u1784 \u2014 \u1794\u17D2\u179A\u17BE\u1787\u17B6\u179A\u17C0\u1784\u179A\u17A0\u17BC\u178F\u17D4 \u1798\u17B6\u1793 3 \u1780\u1789\u17D2\u1785\u1794\u17CB:\n\n"
                    "\U0001F7E6 *Basic $97* (\u2248 400,000 Riel)\n"
                    "\u179F\u17B6\u1780\u179B\u17D2\u1794\u1784 \u2014 \u17A0\u17B6\u1793\u17B7\u1797\u17D0\u1799\u178F\u17B7\u1785\u1794\u17C6\u1795\u17BB\u178F\n\n"
                    "\u2B50 *Pro $297* (\u2248 1,200,000 Riel)\n"
                    "\u179F\u17D2\u179C\u17D0\u1799\u1794\u17D2\u179A\u179C\u178F\u17D2\u178F\u17B7 24/7\n\n"
                    "\U0001F7E1 *VIP $597* (\u2248 2,400,000 Riel)\n"
                    "NiMo \u178A\u17C6\u17A1\u17BE\u1784\u1787\u17B6\u1798\u17BD\u1799\u1794\u1784 Zoom \u2014 \u1785\u1794\u17CB\u1794\u17D2\u179A\u17BE\u1797\u17D2\u179B\u17B6\u1798\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1790\u17D2\u179B\u17C3\u1794\u17D2\u179A\u1785\u17B6\u17C6\u1781\u17C2\u178F\u17C2\u1798\u17BD\u1799: Claude Pro ~$20.\n\n"
                    "*\u1782\u17D2\u1798\u17B6\u1793\u1790\u17D2\u179B\u17C3\u179B\u17B6\u1780\u17CB\u179F\u17D2\u1784\u17B6\u178F\u17CB \u1782\u17D2\u1798\u17B6\u1793\u1780\u17B6\u179A renew \u17D4*"
                ),
            },
            "q_which_plan": {
                "label": "\U0001F914 \u1781\u17D2\u1789\u17BB\u17C6\u1798\u17B7\u1793\u178A\u17B9\u1784\u1790\u17B6\u1780\u1789\u17D2\u1785\u1794\u17CB\u178E\u17B6\u179F\u17B6\u1780\u179F\u1798",
                "answer": (
                    "\U0001F914 *\u1780\u1789\u17D2\u1785\u1794\u17CB\u178E\u17B6\u179F\u17B6\u1780\u179F\u1798\u1787\u17B6\u1798\u17BD\u1799\u17A0\u17B6\u1784\u179A\u1794\u179F\u17CB\u1794\u1784?*\n\n"
                    "\U0001F7E6 *Basic $97* \u2014 \u1791\u17BE\u1794\u179F\u17D2\u1782\u17B6\u179B\u17CB AI \u1785\u1784\u17CB\u179F\u17B6\u1780\u179B\u17D2\u1794\u1784\u1798\u17BB\u1793\n"
                    "\u2192 \u1794\u17BB\u1782\u17D2\u1782\u179B\u17B7\u1780 AI 5 \u1793\u17B6\u1780\u17CB + \u1780\u17B6\u179A\u178E\u17C2\u1793\u17B6\u17C6\u1787\u17B6\u1797\u17B6\u179F\u17B6\u1781\u17D2\u1798\u17C2\u179A + \u1780\u17B6\u179A\u1782\u17B6\u17C6\u1791\u17D2\u179A 30 \u1790\u17D2\u1784\u17C3\n\n"
                    "\u2B50 *Pro $297* \u2014 \u17A0\u17B6\u1784\u178A\u17C6\u178E\u17BE\u179A\u1780\u17B6\u179A \u1785\u1784\u17CB\u179F\u17D2\u179C\u17D0\u1799\u1794\u17D2\u179A\u179C\u178F\u17D2\u178F\u17B7 24/7\n"
                    "\u2192 Chatbot \u1786\u17D2\u179B\u17BE\u1799 + \u1794\u17D2\u179A\u1780\u17B6\u179F\u178A\u17C4\u1799\u179F\u17D2\u179C\u17D0\u1799\u1794\u17D2\u179A\u179C\u178F\u17D2\u178F\u17B7 + \u1791\u1791\u17BD\u179B booking\n\n"
                    "\U0001F7E1 *VIP $597* \u2014 \u1798\u17B7\u1793\u1785\u1784\u17CB\u178A\u17C6\u17A1\u17BE\u1784\u1781\u17D2\u179B\u17BD\u1793\u17AF\u1784 NiMo \u1792\u17D2\u179C\u17BE\u1787\u17C6\u1793\u17BD\u179F\n"
                    "\u2192 \u178A\u17C6\u17A1\u17BE\u1784\u179A\u17BD\u1785 \u1794\u17D2\u179A\u17BE\u1794\u17B6\u1793\u1797\u17D2\u179B\u17B6\u1798 \u1780\u17B6\u179A\u1782\u17B6\u17C6\u1791\u17D2\u179A 90 \u1790\u17D2\u1784\u17C3\n\n"
                    "\u1798\u17B7\u1793\u1794\u17D2\u179A\u17B6\u1780\u178A? \u1794\u17D2\u179A\u17B6\u1794\u17CB NiMo \u17A2\u17C6\u1796\u17B8\u17A0\u17B6\u1784\u179A\u1794\u179F\u17CB\u1794\u1784 \u2014 \u1799\u17BE\u1784\u178E\u17C2\u1793\u17B6\u17C6\u1780\u1789\u17D2\u1785\u1794\u17CB\u178F\u17D2\u179A\u17B9\u1798\u178F\u17D2\u179A\u17BC\u179C \U0001F447"
                ),
            },
            "q_worth": {
                "label": "\U0001F48E $297 \u1798\u17B6\u1793\u178F\u1798\u17D2\u179B\u17C3\u1785\u17C6\u178E\u17B6\u1799\u1791\u17C1?",
                "answer": (
                    "\U0001F48E *$297 \u1798\u17B6\u1793\u178F\u1798\u17D2\u179B\u17C3\u1785\u17C6\u178E\u17B6\u1799\u1791\u17C1?*\n\n"
                    "\u1785\u17BC\u179A\u17B1\u17D2\u1799\u179B\u17C1\u1781\u178F\u1794\u178F\u17C2\u17D4\n\n"
                    "*\u1794\u17BB\u1782\u17D2\u1782\u179B\u17B7\u1780 inbox \u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6:* $200\u2013300/\u1781\u17C2\n"
                    "\u2192 8 \u1798\u17C9\u17C4\u1784/\u1790\u17D2\u1784\u17C3\u17D4 \u1788\u1794\u17CB\u1788\u179A\u17D4 \u1788\u17BA = \u1794\u1793\u17D2\u1790\u1799 productivity \u17D4\n\n"
                    "*Cambodia Biz Agent Pro $297* \u2014 \u1798\u17D2\u178A\u1784\u1794\u17C9\u17BB\u178E\u17D2\u178E\u17C4\u17C7\n"
                    "\u2192 24/7 \u17D4 \u1798\u17B7\u1793\u1788\u1794\u17CB \u17D4 \u1798\u17B7\u1793\u179F\u17BB\u17C6\u17A1\u17BE\u1784\u1794\u17D2\u179A\u17B6\u1780\u17CB \u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "$297 = \u1790\u17D2\u179B\u17C3 inbox \u1780\u17D2\u179A\u17C4\u1798\u1798\u17BD\u1799\u1781\u17C2 \u17D4\n"
                    "\u1794\u17C9\u17BB\u1793\u17D2\u178F\u17C2 Cambodia Biz Agent \u1792\u17D2\u179C\u17BE*\u1787\u17B6\u179A\u17C0\u1784\u179A\u17A0\u17BC\u178F* \u17D4\n\n"
                    "\u1794\u17D2\u179A\u179F\u17B7\u1793\u1794\u17BE AI \u1787\u17BD\u1799\u1794\u1784\u1794\u17B7\u1791 5 \u1780\u17B6\u179A\u1794\u1789\u17D2\u1787\u17B6\u1791\u17B7\u1789/\u1781\u17C2 \u2014 $297  \u179A/\u17A0\u17BE\u1799 \u17D4"
                ),
            },
            "q_warranty": {
                "label": "\U0001F6E1\uFE0F \u1795\u179B\u17B7\u178F\u1795\u179B\u1798\u17B6\u1793\u1780\u17B6\u179A\u1792\u17B6\u1793\u17B6\u179A\u17C9\u17B6\u1794\u17CB\u179A\u1784?",
                "answer": (
                    "\U0001F6E1\uFE0F *\u1795\u179B\u17B7\u178F\u1795\u179B\u1798\u17B6\u1793\u1780\u17B6\u179A\u1792\u17B6\u1793\u17B6? \u17A2\u17B6\u1785\u1794\u1784\u17D2\u179C\u17B7\u179B\u179B\u17BB\u1799?*\n\n"
                    "\u1798\u17B6\u1793\u1787\u17B6\u1780\u17B6\u179A\u1794\u17D2\u179A\u17B6\u1780\u178A \u17D4 NiMo \u1791\u17C6\u1793\u17BB\u1780\u1785\u17B7\u178F\u17D2\u178F \u17D4\n\n"
                    "*\u1792\u17B6\u1793\u17B6 30 \u1790\u17D2\u1784\u17C3 \u2014 \u1794\u1784\u17D2\u179C\u17B7\u179B\u179B\u17BB\u1799 100% \u178A\u17C4\u1799/\u17A0\u17C1\u178F\u17BB\u1795\u179B \u17D4*\n\n"
                    "\u1791\u17B7\u1789 \u17D4 \u1792\u17D2\u179C\u17BE\u178F\u17B6\u1798\u1780\u17B6\u179A\u178E\u17C2\u1793\u17B6\u17C6 30 \u1790\u17D2\u1784\u17C3 \u17D4 "
                    "\u1794\u17D2\u179A\u179F\u17B7\u1793\u1794\u17BE/\u178A\u17C6\u178E\u17BE\u179A\u1780\u17B6\u179A/\u1796\u17B7\u1796\u178E\u17CC\u1793\u17B6 \u2014 \u1795\u17D2\u1789\u17BE NiMo Telegram \u17D4 "
                    "\u1794\u1784\u17D2\u179C\u17B7\u179B\u1780\u17D2\u1793\u17BB\u1784 24 \u1798\u17C9\u17C4\u1784 \u17D4\n\n"
                    "*\u17A0\u17B6\u1793\u17B7\u1797\u17D0\u1799: NiMo \u17D4 \u1798\u17B7\u1793/\u1794\u1784 \u17D4* \u2764\uFE0F"
                ),
            },
            "q_tech": {
                "label": "\U0001F630 \u1781\u17D2\u1789\u17BB\u17C6\u1781\u17D2\u179B\u17B6\u1785\u178A\u17C6\u17A1\u17BE\u1784\u1798\u17B7\u1793\u1794\u17B6\u1793",
                "answer": (
                    "\U0001F630 *\u1798\u17B7\u1793\u1785\u17C1\u17C7\u1794\u1785\u17D2\u1785\u17C1\u1780\u179C\u17B7\u1791\u17D2\u1799\u17B6 \u2014 \u17A2\u17B6\u1785\u178A\u17C6\u17A1\u17BE\u1784\u1794\u17B6\u1793\u1791\u17C1?*\n\n"
                    "\u1794\u17B6\u1793! \u1793\u17C1\u17C7\u1787\u17B6\u17A0\u17C1\u178F\u17BB\u1795\u179B:\n\n"
                    "\u2705 \u1780\u17B6\u179A\u178E\u17C2\u1793\u17B6\u17C6\u1787\u17B6\u1797\u17B6\u179F\u17B6\u1781\u17D2\u1798\u17C2\u179A \u1798\u17B6\u1793\u179A\u17BC\u1794\u1797\u17B6\u1796\u1794\u1784\u17D2\u17A0\u17B6\u1789\u1787\u17B6\u1787\u17C6\u17A0\u17B6\u1793\u17D7\n"
                    "\u2705 \u1798\u17B6\u1793\u179C\u17B8\u178A\u17C1\u17A2\u17BC\u1798\u17BE\u179B\u178F\u17B6\u1798\n"
                    "\u2705 \u1794\u17D2\u179A\u17BE Bot \u1787\u17BD\u1799 24/7\n"
                    "\u2705 NiMo \u1795\u17D2\u1791\u17B6\u179B\u17CB\u1786\u17D2\u179B\u17BE\u1799\u1796\u17C1\u179B\u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A\n\n"
                    "\u1780\u1789\u17D2\u1785\u1794\u17CB VIP: NiMo \u17A2\u1784\u17D2\u1782\u17BB\u1799\u178A\u17C6\u17A1\u17BE\u1784\u1787\u17B6\u1798\u17BD\u1799\u1794\u1784\u178F\u17B6\u1798 Zoom 2 \u1798\u17C9\u17C4\u1784 \u2014 "
                    "\u1794\u1784\u1782\u17D2\u179A\u17B6\u1793\u17CB\u178F\u17C2\u1798\u17BE\u179B \u17A0\u17BE\u1799\u1785\u17BB\u1785\u178F\u17B6\u1798\u17D4 \U0001F3AF"
                ),
            },
            "q_time": {
                "label": "\u23F0 \u1785\u17C6\u178E\u17B6\u1799\u1796\u17C1\u179B\u1794\u17C9\u17BB\u1793\u17D2\u1798\u17B6\u1793\u178A\u17BE\u1798\u17D2\u1794\u17B8\u1785\u17B6\u1794\u17CB\u1795\u17D2\u178A\u17BE\u1798?",
                "answer": (
                    "\u23F0 *\u1785\u17C6\u178E\u17B6\u1799\u1796\u17C1\u179B\u1794\u17C9\u17BB\u1793\u17D2\u1798\u17B6\u1793\u178A\u17BE\u1798\u17D2\u1794\u17B8\u1785\u17B6\u1794\u17CB\u1794\u17D2\u179A\u17BE?*\n\n"
                    "*Basic & Pro:* \u178A\u17C6\u17A1\u17BE\u1784\u178F\u17B6\u1798\u1780\u17B6\u179A\u178E\u17C2\u1793\u17B6\u17C6 ~2\u20133 \u1798\u17C9\u17C4\u1784 \u2014 "
                    "\u1792\u17D2\u179C\u17BE\u1796\u17C1\u179B\u179B\u17D2\u1784\u17B6\u1785 \u17D4 \u1790\u17D2\u1784\u17C3 2 \u1798\u17B6\u1793 content \u17D4 \u1790\u17D2\u1784\u17C3 3 \u178A\u17C6\u178E\u17BE\u179A\u1780\u17B6\u179A \u17D4\n\n"
                    "*VIP:* Zoom 2 \u1798\u17C9\u17C4\u1784\u1787\u17B6\u1798\u17BD\u1799 NiMo \u2014 "
                    "NiMo \u1792\u17D2\u179C\u17BE test \u1785\u1794\u17CB\u1794\u17D2\u179A\u1782\u179B\u17CB \u17D4\n\n"
                    "\u1791\u17B7\u1789\u1796\u17C1\u179B\u1796\u17D2\u179A\u17B9\u1780 \u2014 \u179B\u17D2\u1784\u17B6\u1785\u1798\u17B6\u1793 content \u178A\u17C6\u1794\u17BC\u1784 \U0001F680"
                ),
            },
            "q_device": {
                "label": "\U0001F4F1 \u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A\u17A7\u1794\u1780\u179A\u178E\u17CD\u17A2\u17D2\u179C\u17B8?",
                "answer": (
                    "\U0001F4F1 *\u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A\u17A7\u1794\u1780\u179A\u178E\u17CD\u17A2\u17D2\u179C\u17B8?*\n\n"
                    "Computer \u17AC smartphone \u1780\u17CF\u1794\u17D2\u179A\u17BE\u1794\u17B6\u1793 \U0001F60A\n\n"
                    "\U0001F4BB *Computer:* NiMo \u178E\u17C2\u1793\u17B6\u17C6 \u178A\u17C6\u17A1\u17BE\u1784\u178A\u17C6\u1794\u17BC\u1784 + \u1798\u17BE\u179B\u179A\u1794\u17B6\u1799\u1780\u17B6\u179A\u178E\u17CD\n\n"
                    "\U0001F4F1 *Smartphone:* \u1794\u17D2\u179A\u178F\u17B7\u1794\u178F\u17D2\u178F\u17B7\u1780\u17B6\u179A\u1794\u17D2\u179A\u1785\u17B6\u17C6\u1790\u17D2\u1784\u17C3 \u1786\u17D2\u179B\u17BE\u1799 post report\n\n"
                    "Computer \u178E\u17B6\u178A\u17C2\u179B scroll Facebook \u179F\u17D2\u179A\u17BD\u179B \u2014 \u1794\u17D2\u179A\u17BE Cambodia Biz Agent \u1794\u17B6\u1793 \u17D4 "
                    "\u1782\u17D2\u1798\u17B6\u1793\u1780\u17B6\u179A upgrade \u17D4"
                ),
            },
            "q_internet": {
                "label": "\U0001F310 \u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A internet \u179B\u17BF\u1793?",
                "answer": (
                    "\U0001F310 *\u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A internet \u179B\u17D2\u1794\u17BF\u1793\u1781\u17D2\u1796\u179F\u17CB?*\n\n"
                    "\u1798\u17B7\u1793\u1791\u17B6\u1798\u1791\u17B6\u179A \u17D4 Internet \u1794\u17D2\u179A\u17BE Facebook + Telegram \u1792\u1798\u17D2\u1798\u178F\u17B6 \u2014 \u1794\u17D2\u179A\u17BE Agent \u1794\u17B6\u1793 \u17D4\n\n"
                    "WiFi \u1795\u17D2\u1791\u17C7 \u17AC 4G \u1780\u17CF OK \u17D4 \u1794\u17D2\u179A\u1796\u17D0\u1793\u17D2\u1792 run cloud \u2014 "
                    "phone/computer \u1782\u17D2\u179A\u17B6\u1793\u17CB\u178F\u17C2 \u1795\u17D2\u1789\u17BE command \U0001F680"
                ),
            },
            "q_team": {
                "label": "\U0001F465 \u1794\u17BB\u1782\u17D2\u1782\u179B\u17B7\u1780\u17A2\u17B6\u1785\u1794\u17D2\u179A\u17BE\u179A\u17BD\u1798\u1782\u17D2\u1793\u17B6?",
                "answer": (
                    "\U0001F465 *\u1794\u17BB\u1782\u17D2\u1782\u179B\u17B7\u1780\u17A0\u17B6\u1784\u17A2\u17B6\u1785\u1794\u17D2\u179A\u17BE\u179A\u17BD\u1798?*\n\n"
                    "\u1794\u17B6\u1793\u1787\u17B6\u1780\u17B6\u179A\u1794\u17D2\u179A\u17B6\u1780\u178A! NiMo \u179A\u1785\u1793\u17B6 Cambodia Biz Agent \u17B1\u17D2\u1799\u1794\u17D2\u179A\u17BE team \u1791\u17B6\u17C6\u1784\u1798\u17BC\u179B \U0001F60A\n\n"
                    "\u2705 Inbox staff \u1794\u17D2\u179A\u17BE AI \u1786\u17D2\u179B\u17BE\u1799\u17A2\u178F\u17B7\u1790\u17B7\u1787\u1793\n"
                    "\u2705 Content staff \u1794\u17D2\u179A\u17BE AI \u1794\u1784\u17D2\u1780\u17BE\u178F\u1780\u17B6\u179A\u1794\u17D2\u179A\u1780\u17B6\u179F\n"
                    "\u2705 Manager \u1794\u17D2\u179A\u17BE AI \u1798\u17BE\u179B\u1785\u17C6\u178E\u17BC\u179B\n\n"
                    "Access account \u178F\u17C2\u1798\u17BD\u1799 \u2014 collaborate \u1784\u17B6\u1799 \u17D4\n\n"
                    "\U0001F4A1 Claude Pro $20/\u1781\u17C2 share team \u1791\u17B6\u17C6\u1784\u17A2\u179F\u17CB \u2014 "
                    "\u1782\u17D2\u1798\u17B6\u1793\u1780\u17B6\u179A\u1791\u17B7\u1789 account \u178A\u17B6\u1785\u17CB \u17D4"
                ),
            },
            "q_data": {
                "label": "\U0001F512 \u1791\u17B7\u1793\u17D2\u1793\u1793\u17D0\u1799\u17A0\u17B6\u1784\u1787\u17D2\u179A\u17B6\u1794\u1785\u17C1\u1789?",
                "answer": (
                    "\U0001F512 *\u1791\u17B7\u1793\u17D2\u1793\u1793\u17D0\u1799\u17A0\u17B6\u1784 \u1787\u17D2\u179A\u17B6\u1794\u1785\u17C1\u1789?*\n\n"
                    "NiMo \u1792\u17B6\u1793\u17B6: \u1791\u17B7\u1793\u17D2\u1793\u1793\u17D0\u1799\u179A\u1794\u179F\u17CB\u1794\u1784\u1798\u17B6\u1793\u179F\u17BB\u179C\u178F\u17D2\u1790\u17B7\u1797\u17B6\u1796 \u17D4\n\n"
                    "\u2705 \u1791\u17B7\u1793\u17D2\u1793\u1793\u17D0\u1799\u1787\u17B6\u179A\u1794\u179F\u17CB\u1794\u1784 \u2014 store \u1780\u17D2\u1793\u17BB\u1784 account \u1795\u17D2\u1791\u17B6\u179B\u17CB \u17D4\n\n"
                    "\u2705 NiMo \u1798\u17B7\u1793 collect/sell/share \u1791\u17B7\u1793\u17D2\u1793\u1793\u17D0\u1799 \u17D4\n\n"
                    "\u2705 Security \u179F\u17D2\u178A\u1784\u17CB\u178A\u17B6\u179A Anthropic (US) \u2014 "
                    "\u178A\u17BC\u1785 bank \u1792\u17C6 \u17D4\n\n"
                    "\u17A0\u17B6\u1784\u1787\u17B6\u179A\u1794\u179F\u17CB\u1794\u1784 \u2192 \u1791\u17B7\u1793\u17D2\u1793\u1793\u17D0\u1799\u1787\u17B6\u179A\u1794\u179F\u17CB\u1794\u1784 \u2192 NiMo \u1798\u17B7\u1793\u1791\u17BB\u1780\u17A2\u17D2\u179C\u17B8 \u2764\uFE0F"
                ),
            },
            "q_after_warranty": {
                "label": "\U0001F91D \u1795\u17BB\u178F\u1780\u17B6\u179A\u1792\u17B6\u1793\u17B6 NiMo \u1787\u17BD\u1799?",
                "answer": (
                    "\U0001F91D *\u1795\u17BB\u178F 30 \u1790\u17D2\u1784\u17C3 NiMo \u1787\u17BD\u1799?*\n\n"
                    "\u1780\u17B6\u179A\u1792\u17B6\u1793\u17B6 = policy \u1794\u1784\u17D2\u179C\u17B7\u179B\u179B\u17BB\u1799 \u2014 \u1787\u17C6\u1793\u17BD\u1799 NiMo \u1782\u17D2\u1798\u17B6\u1793\u1780\u17B6\u179A\u1780\u17C6\u178E\u178F\u17CB \U0001F60A\n\n"
                    "\u2705 Telegram NiMo \u1793\u17C5\u1796\u17C1\u179B\u178E\u17B6 \u2014 \u1787\u17BD\u1799 \u17D4\n\n"
                    "\u2705 Community group \u2014 \u179A\u17C0\u1793\u1796\u17B8\u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784\u1795\u17D2\u179F\u17C1\u1784 \u17D4\n\n"
                    "\u2705 Update \u1790\u17D2\u1798\u17B8 \u2014 \u17A5\u178F\u1782\u17B7\u178F\u1790\u17D2\u179B\u17C3 \u17D4\n\n"
                    "NiMo \u1798\u17B7\u1793 abandon \u17D4 \u2764\uFE0F"
                ),
            },
            "q_update": {
                "label": "\U0001F199 \u1798\u17B6\u1793\u1780\u17B6\u179A update?",
                "answer": (
                    "\U0001F199 *\u1798\u17B6\u1793 update/upgrade \u1790\u17D2\u1784\u17C3\u1780\u17D2\u179A\u17C4\u1799? \u1790\u17D2\u179B\u17C3?*\n\n"
                    "Update \u1787\u17B6\u1793\u17B7\u1785\u17D2\u1785 \u2014 \u17A5\u178F\u1782\u17B7\u178F\u1790\u17D2\u179B\u17C3 \U0001F381\n\n"
                    "NiMo upgrade \u1795\u17D2 \u17A2\u17B6\u179F\u17CB feedback \u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784 \u17D4 \u1796\u17C1\u179B\u1798\u17B6\u1793:\n\n"
                    "\u2705 Feature \u1790\u17D2\u1798\u17B8\n"
                    "\u2705 AI command \u1794\u17D2\u179A\u179F\u17BE\u179A\n"
                    "\u2705 Speed + effectiveness\n\n"
                    "\u2192 \u1791\u1791\u17BD\u179B update \u178A\u17C4\u1799 group \u2014 \u178A\u17C4\u1799 pay \u1790\u17D2\u1798\u17B8 \u17D4\n\n"
                    "\u1791\u17B7\u1789\u1798\u17D2\u178A\u1784 \u2014 upgrade \u1787\u17B6\u179A\u17C0\u1784\u179A\u17A0\u17BC\u178F \u17D4"
                ),
            },
            "q_community": {
                "label": "\U0001F465 NiMo \u1798\u17B6\u1793 community group?",
                "answer": (
                    "\U0001F465 *NiMo \u1798\u17B6\u1793 community group?*\n\n"
                    "\u1798\u17B6\u1793\u1787\u17B6\u1780\u17B6\u179A\u1794\u17D2\u179A\u17B6\u1780\u178A \U0001F49B\n\n"
                    "\u1780\u17D2\u179A\u17C4\u1799\u1791\u17B7\u1789 NiMo add \u1785\u17BC\u179B *Telegram community* \u17D4 \u1791\u17B8\u1793\u17C4\u17C7:\n\n"
                    "\u2705 \u1787\u17BD\u1794\u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784\u1781\u17D2\u1798\u17C2\u179A \u2014 \u1785\u17C2\u1780\u179A\u17C6\u179B\u17C2\u1780\u1794\u1791\u1796\u17B7\u179F\u17C4\u1792 \u17D4\n\n"
                    "\u2705 \u179A\u17C0\u1793 AI \u1794\u17D2\u179A\u1780\u1794\u178A\u17C4\u1799\u1794\u17D2\u179A\u179F\u17B7\u1791\u17D2\u1792 \u17D4\n\n"
                    "\u2705 Tips + AI command \u1790\u17D2\u1798\u17B8\u1794\u17D2\u179A\u1785\u17B6\u17C6\u179F\u1794\u17D2\u178A\u17B6\u17A0\u17CD \u17D4\n\n"
                    "\u2705 \u1787\u17C6\u1793\u17BD\u1799 NiMo + community \u17D4\n\n"
                    "\u1794\u1784\u1798\u17B7\u1793\u178A\u17C2\u179B\u1791\u17C5\u1798\u17D2\u1793\u17B6\u1780\u17CB \u2764\uFE0F"
                ),
            },
            "q_competitor": {
                "label": "\u2694\uFE0F \u1782\u17BC\u1794\u17D2\u179A\u1787\u17C2\u1784\u1794\u17D2\u179A\u17BE Agent \u1795\u1784?",
                "answer": (
                    "\u2694\uFE0F *\u1782\u17BC\u1794\u17D2\u179A\u1787\u17C2\u1784\u1794\u17D2\u179A\u17BE \u2014 \u1781\u17D2\u1789\u17BB\u17C6\u1793\u17C5 advantage?*\n\n"
                    "\u1785\u17C6\u179B\u17BE\u1799: advantage \u1793\u17C5 \u2014 \u17A0\u17BE\u1799\u1792\u17C6\u1787\u17B6\u1784 \u1794\u17D2\u179A\u179F\u17B7\u1793\u1794\u17BE\u1785\u17B6\u1794\u17CB\u1795\u17D2\u178A\u17BE\u1798\u1798\u17BB\u1793 \u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*\u1798\u17D2\u1785\u17B6\u179F\u17CB\u17A0\u17B6\u1784\u1797\u17B6\u1782\u1785\u17D2\u179A\u17BE\u1793\u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6 \u1798\u17B7\u1793\u1791\u17B6\u1793\u17CB\u1794\u17D2\u179A\u17BE AI \u17D4*\n"
                    "\u179A\u17C0\u1784\u179A\u17B6\u179B\u17CB\u1790\u17D2\u1784\u17C3 wait = \u1790\u17D2\u1784\u17C3 competitor \u1791\u17C5 \u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*\u1794\u17D2\u179A\u17BE tool \u178A\u17BC\u1785\u1782\u17D2\u1793\u17B6 \u2260 result \u178A\u17BC\u1785\u1782\u17D2\u1793\u17B6 \u17D4*\n\n"
                    "\u17A0\u17B6\u1784 2 \u1794\u17D2\u179A\u17BE tool \u178A\u17BC\u1785 \u2014 \u1794\u17C9\u17BB\u1793\u17D2\u178F\u17C2:\n"
                    "\u2022 \u1795\u179B\u17B7\u178F\u1795\u179B \u2260\n"
                    "\u2022 Brand style \u2260\n"
                    "\u2022 Customer approach \u2260\n\n"
                    "AI \u179A\u17C0\u1793\u178F\u17B6\u1798 \u17A0\u17B6\u1784\u1794\u1784 \u2014 \u1782\u17D2\u1798\u17B6\u1793 copy \u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Advantage = \u1794\u17D2\u179A\u17BE *\u179B\u17BF\u1793 \u1794\u17D2\u179A\u179F\u17BE\u179A \u179F\u17D2\u1790\u17B7\u178F\u1790\u17C1\u179A* \u1787\u17B6\u1784 \u17D4"
                ),
            },
            "q_think": {
                "label": "\U0001F914 \u179F\u17BC\u1798\u1791\u17BB\u17D2\u1799\u1785\u17B7\u178F\u17D2\u178F\u1794\u1793\u17D2\u1790\u17C2\u1798",
                "answer": (
                    "\U0001F914 *\u179F\u17BC\u1798\u1791\u17BB\u17D2\u1799\u1785\u17B7\u178F\u17D2\u178F\u1794\u1793\u17D2\u1790\u17C2\u1798*\n\n"
                    "\u1785\u17C6\u1796\u17C4\u17C7 \u2014 \u1780\u17B6\u179A \u2460\u1785\u17C6\u178E \u2461\u1785\u17C6\u178E \u2462 \u2462 \U0001F60A\n\n"
                    "\u1794\u17C9\u17BB\u1793\u17D2\u178F\u17C2 NiMo \u1785\u1784\u17CB\u17B1\u17D2\u1799\u1794\u1784\u178A\u17B9\u1784 3 \u1785\u17C6\u178E\u17BB\u1785:\n\n"
                    "*\u1791\u17B8\u1798\u17BD\u1799 \u2014 \u178F\u1798\u17D2\u179B\u17C3 early bird \u17D4*\n"
                    "\u1780\u17D2\u179A\u17C4\u1799 launch \u17D4 \u17D4 \u17D4 \u178F\u1798\u17D2\u179B\u17C3 \u2191 \u17D4 \u1791\u17B7\u1789\u1790\u17D2\u1784\u17C3\u1793\u17C1\u17C7 = best price \u17D4\n\n"
                    "*\u1791\u17B8\u1796\u17B8\u179A \u2014 \u1792\u17B6\u1793\u17B6 30 \u1790\u17D2\u1784\u17C3 100% \u17D4*\n"
                    "= Try \u178A\u17C4\u1799 risk \u2248 0 \u17D4 \u1798\u17B7\u1793good \u2192 \u1794\u17D2\u179A\u17B6\u1780\u17CB back \u17D4\n\n"
                    "*\u1791\u17B8\u1794\u17B8 \u2014 \u179A\u17C0\u1784\u179A\u17B6\u179B\u17CB\u1790\u17D2\u1784\u17C3 wait = \u1790\u17D2\u1784\u17C3 lose \u17D4*\n"
                    "\u1796\u17C1\u179B order \u1794\u17B6\u178F\u17CB c\u01A1h\u1ED9i \u17D4 \u17D4 \u17D4 \u17D4 \u17D4 \u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1794\u1784\u178F\u17D2\u179A\u17BC\u179C info \u1794\u1793\u17D2\u1790\u17C2\u1798? NiMo \u1793\u17C5\u1791\u17B8\u1793\u17C1\u17C7 \U0001F60A"
                ),
            },
            "q_try": {
                "label": "\U0001F9EA \u1785\u1784\u17CB\u179F\u17B6\u1780\u179B\u17D2\u1794\u1784\u1798\u17BB\u1793\u1791\u17B7\u1789",
                "answer": (
                    "\U0001F9EA *\u1785\u1784\u17CB\u179F\u17B6\u1780\u179B\u17D2\u1794\u1784\u1798\u17BB\u1793\u1791\u17B7\u1789*\n\n"
                    "NiMo \u1799\u179B\u17CB \U0001F60A\n\n"
                    "\u1794\u17C9\u17BB\u1793\u17D2\u178F\u17C2: Try = result \u1796\u17B7\u178F\u1794\u17D2\u179A\u17B6\u1780\u178A \u1793\u17C5 \u17A0\u17B6\u1784 \u1796\u17B7\u178F\u1794\u17D2\u179A\u17B6\u1780\u178A \u17D4\n"
                    "*\u1798\u17B7\u1793 \u17A2\u17B6\u1785\u1792\u17D2\u179C\u17BE \u178A\u17C4\u1799/\u1785\u17B6\u1794\u17CB '\u1796\u17B7\u178F\u1794\u17D2\u179A\u17B6\u1780\u178A \u17D4*\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u17A0\u17BE\u1799 NiMo \u1798\u17B6\u1793 *Basic $97* = 'free trial with refund':\n\n"
                    "\u2705 5 AI Employees \u1796\u17C1\u1789\n"
                    "\u2705 Run \u17A0\u17B6\u1784\u1796\u17B7\u178F\u1794\u17D2\u179A\u17B6\u1780\u178A\n"
                    "\u2705 Result 30 \u1790\u17D2\u1784\u17C3\n"
                    "\u2705 \u2260good \u2192 100% back\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*Risk \u1796\u17B7\u178F = continue \u1798\u17D2\u1793\u17B6\u1780\u17CB \u2014 \u1781\u178E\u17C8/\u1785 way \u17D4*"
                ),
            },
            "q_claude_pro": {
                "label": "\U0001F4B3 Claude Pro $20/\u1781\u17C2 \u1787\u17B6\u17A2\u17D2\u179C\u17B8?",
                "answer": (
                    "\U0001F4B3 *Claude Pro $20/\u1781\u17C2 \u1787\u17B6\u17A2\u17D2\u179C\u17B8? \u178F\u1798\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A?*\n\n"
                    "Cambodia Biz Agent run \u179B\u17BE Claude AI (Anthropic \u2014 US) \u17D4 "
                    "\u178A\u17BE\u1798\u17D2\u1794\u17B8\u1794\u17D2\u179A\u17BE \u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A Claude Pro *$20/\u1781\u17C2* \u2014 "
                    "\u1785\u17C6\u178E\u17B6\u1799 Anthropic \u1795\u17D2\u1791\u17B6\u179B\u17CB \u1798\u17B7\u1793 NiMo \u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1794\u17C9\u17BB\u1793\u17D2\u178F\u17C2 cost \u1796\u17B7\u178F:\n\n"
                    "\u2705 $20/\u1781\u17C2 = 1 employee 24/7 \u17D4\n"
                    "\u2705 AI Agents \u1791\u17B6\u17C6\u1784 5 run account 1 \u17D4\n"
                    "\u2705 Cancel \u1796\u17C1\u179B\u178E\u17B6 \u17D4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Inbox staff \u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6 = $200\u2013300/\u1781\u17C2 \u17D4\n"
                    "Claude Pro = $20/\u1781\u17C2 \u17D4 *Save $180\u2013280/\u1781\u17C2 \u17D4*"
                ),
            },
            "q_riel": {
                "label": "\U0001F4B5 \u17A2\u17B6\u1785\u1794\u1784\u17CB\u1787\u17B6\u179A\u17C0\u179B\u1794\u17B6\u1793?",
                "answer": (
                    "\U0001F4B5 *\u17A2\u17B6\u1785\u1794\u1784\u17CB\u1787\u17B6\u179A\u17C0\u179B?*\n\n"
                    "\u1794\u17B6\u1793\u1787\u17B6\u1780\u17B6\u179A\u1794\u17D2\u179A\u17B6\u1780\u178A! \u1795\u17D2\u1791\u17C1\u179A\u179A\u17C0\u179B\u1792\u1798\u17D2\u1798\u178F\u17B6 \u2014 "
                    "ABA convert USD \u179F\u17D2\u179C\u17D0\u1799\u1794\u17D2\u179A\u179C\u178F\u17D2\u178F\u17B7 \u17D4\n\n"
                    "\U0001F7E6 *Basic $97* \u2248 400,000 Riel\n"
                    "\u2B50 *Pro $297* \u2248 1,200,000 Riel\n"
                    "\U0001F7E1 *VIP $597* \u2248 2,400,000 Riel"
                ),
            },
            "q_industry": {
                "label": "\U0001F6CD\uFE0F \u17A0\u17B6\u1784\u1781\u17D2\u1789\u17BB\u17C6 \u2260 tech \u17A2\u17B6\u1785\u1794\u17D2\u179A\u17BE?",
                "answer": (
                    "\U0001F6CD\uFE0F *\u17A0\u17B6\u1784\u1781\u17D2\u1789\u17BB\u17C6 [food/fashion/beauty]\u2026 \u1794\u17D2\u179A\u17BE Agent \u1794\u17B6\u1793?*\n\n"
                    "NiMo \u1786\u17D2\u179B\u17BE\u1799: *\u1794\u17D2\u179A\u179F\u17B7\u1793\u1794\u17BE sell online \u1793\u17C5\u1780\u1798\u17D2\u1796\u17BB\u1787\u17B6 \u2014 \u1794\u17D2\u179A\u17BE\u1794\u17B6\u1793 \u17D4*\n\n"
                    "NiMo tested:\n\n"
                    "\U0001F457 Fashion & accessories\n"
                    "\U0001F484 Beauty & skincare\n"
                    "\U0001F371 Food & specialty\n"
                    "\U0001F4DA Courses & consulting\n"
                    "\U0001F486 Spa, salon, studio\n"
                    "\U0001F3E0 Furniture & home\n"
                    "\U0001F338 Flowers & gifts\n\n"
                    "AI \u179A\u17C0\u1793\u178F\u17B6\u1798 \u1795\u179B\u17B7\u178F\u1795\u179B + style \u17A0\u17B6\u1784 \u2014 \u1798\u17B7\u1793 apply formula rigid \u17D4\n\n"
                    "\u1798\u17B7\u1793\u1794\u17D2\u179A\u17B6\u1780\u178A? \u1794\u17D2\u179A\u17B6\u1794\u17CB niche NiMo \u2014 \u1796\u17B7\u1782\u17D2\u179A\u17C4\u17C7 free \U0001F447"
                ),
            },
            "q_delivery": {
                "label": "\U0001F4E6 \u1795\u17D2\u1791\u17C1\u179A\u200B\u1794\u17D2\u179A\u17B6\u1780\u17CB\u200B\u17A0\u17BE\u1799\u200B \u1791\u1791\u17BD\u179B\u200B\u178A\u17BC\u1785\u200B\u1798\u17D2\u178A\u17C1\u1785?",
                "answer": (
                    "\U0001F4E6 *\u1780\u17D2\u179A\u17C4\u1799\u1795\u17D2\u1791\u17C1\u179A\u1794\u17D2\u179A\u17B6\u1780\u17CB \u1791\u1791\u17BD\u179B\u178A\u17BC\u1785\u1798\u17D2\u178A\u17C1\u1785?*\n\n"
                    "\u1784\u17B6\u1799 \u2014 4 \u1787\u17C6\u17A0\u17B6\u1793:\n\n"
                    "*\u1787\u17C6\u17A0\u17B6\u1793 1 \u2014 \u1795\u17D2\u1791\u17C1\u179A*\n"
                    "\u1787\u17D2\u179A\u17BE\u179F package \u2192 \u1795\u17D2\u1791\u17C1\u179A info NiMo \u1795\u17D2\u178A\u179B\u17CB\n\n"
                    "*\u1787\u17C6\u17A0\u17B6\u1793 2 \u2014 \u1795\u17D2\u1789\u17BE confirm*\n"
                    "Screenshot \u2192 \u1788\u17D2\u1798\u17C4\u17C7 + phone + package \u2192 \u1795\u17D2\u1789\u17BE bot\n\n"
                    "*\u1787\u17C6\u17A0\u17B6\u1793 3 \u2014 NiMo confirm & \u1795\u17D2\u1789\u17BE*\n"
                    "NiMo verify + \u1795\u17D2\u1789\u17BE product \u1780\u17D2\u1793\u17BB\u1784 30 \u1793\u17B6\u1791\u17B8\n\n"
                    "*\u1787\u17C6\u17A0\u17B6\u1793 4 \u2014 \u1791\u1791\u17BD\u179B + \u1785\u17B6\u1794\u17CB\u1795\u17D2\u178A\u17BE\u1798*\n"
                    "Kit + guide PDF + video + group support \U0001F680\n\n"
                    "*VIP:* \u1780\u17D2\u179A\u17C4\u1799\u1791\u1791\u17BD\u179B Kit NiMo \u178E\u17B6\u178F\u17CB Zoom \u17D4"
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "\U0001F50D \u179F\u17D2\u179C\u17C2\u1784\u1799\u179B\u17CB\u17A2\u17C6\u1796\u17B8 Cambodia Biz Agent",
                "questions": ["q_nimo", "q_system", "q_different", "q_save", "q_location"],
            },
            "cat_price": {
                "label": "\U0001F4B0 \u178F\u1798\u17D2\u179B\u17C3 & \u1780\u1789\u17D2\u1785\u1794\u17CB",
                "questions": ["q_price", "q_which_plan", "q_worth", "q_warranty"],
            },
            "cat_tech": {
                "label": "\U0001F6E0\uFE0F \u1780\u17B6\u179A\u178A\u17C6\u17A1\u17BE\u1784 & \u1794\u1785\u17D2\u1785\u17C1\u1780\u179C\u17B7\u1791\u17D2\u1799\u17B6",
                "questions": ["q_tech", "q_time", "q_device", "q_internet", "q_team"],
            },
            "cat_support": {
                "label": "\U0001F512 \u1780\u17B6\u179A\u1792\u17B6\u1793\u17B6 & \u1787\u17C6\u1793\u17BD\u1799",
                "questions": ["q_data", "q_after_warranty", "q_update", "q_community"],
            },
            "cat_doubt": {
                "label": "\U0001F914 \u1793\u17C5\u178F\u17C2\u179F\u17D2\u1791\u17B6\u1780\u17CB\u179F\u17D2\u1791\u17BE\u179A",
                "questions": ["q_competitor", "q_think", "q_try"],
            },
            "cat_buy": {
                "label": "\U0001F6CD\uFE0F \u1780\u17B6\u179A\u1791\u17B7\u1789",
                "questions": ["q_claude_pro", "q_riel", "q_industry", "q_delivery"],
            },
        },
        "s": {
            "welcome": (
                "\U0001F44B \u179F\u17BD\u179F\u17D2\u178F\u17B8! \u1781\u17D2\u1789\u17BB\u17C6\u1787\u17B6\u1787\u17C6\u1793\u17BD\u1799\u1780\u17B6\u179A\u179A\u1794\u179F\u17CB *NiMo Team*\u17D4\n\n"
                "\u1794\u1784\u1798\u17B6\u1793\u179F\u17C6\u178E\u17BD\u179A\u17A2\u17D2\u179C\u17B8\u17A2\u17C6\u1796\u17B8 *Cambodia Biz Agent*?\n"
                "\u1787\u17D2\u179A\u17BE\u179F\u179F\u17C6\u178E\u17BD\u179A\u1781\u17B6\u1784\u1780\u17D2\u179A\u17C4\u1798 \u2014 \u1781\u17D2\u1789\u17BB\u17C6\u1786\u17D2\u179B\u17BE\u1799\u1797\u17D2\u179B\u17B6\u1798\u17D7 \U0001F447"
            ),
            "choose_cat":       "\u1787\u17D2\u179A\u17BE\u179F\u179F\u17C6\u178E\u17BD\u179A\u178A\u17C2\u179B\u1794\u1784\u1785\u1784\u17CB\u178A\u17B9\u1784:",
            "buy_title": (
                "\U0001F389 *\u179B\u17D2\u17A2\u178E\u17B6\u179F\u17CB! \u1794\u1784\u1785\u1784\u17CB\u1787\u17D2\u179A\u17BE\u179F\u1780\u1789\u17D2\u1785\u1794\u17CB\u178E\u17B6?*\n\n"
                "\U0001F7E6 *Basic $97* \u2014 \u179F\u17B6\u1780\u179B\u17D2\u1794\u1784\u1798\u17BB\u1793\n"
                "\u2B50 *Pro $297* \u2014 \u179F\u17D2\u179C\u17D0\u1799\u1794\u17D2\u179A\u179C\u178F\u17D2\u178F\u17B7 24/7\n"
                "\U0001F7E1 *VIP $597* \u2014 NiMo \u178A\u17C6\u17A1\u17BE\u1784\u1787\u17C6\u1793\u17BD\u179F\n\n"
                "\u1787\u17D2\u179A\u17BE\u179F\u1780\u1789\u17D2\u1785\u1794\u17CB \U0001F447"
            ),
            "buy_btn":          "\U0001F4B3 \u1781\u17D2\u1789\u17BB\u17C6\u1785\u1784\u17CB\u1791\u17B7\u1789\u17A5\u17A1\u17BC\u179C",
            "consult_btn":      "\U0001F4AC \u179F\u17BD\u179A NiMo \u178A\u17C4\u1799\u1795\u17D2\u1791\u17B6\u179B\u17CB",
            "back_btn":         "\u2B05\uFE0F \u178F\u17D2\u179A\u17A1\u1794\u17CB\u1791\u17C5\u1798\u17C9\u17BA\u1793\u17BB\u1799",
            "back_cat":         "\u2B05\uFE0F \u179F\u17C6\u178E\u17BD\u179A\u1795\u17D2\u179F\u17C1\u1784\u1791\u17C0\u178F",
            "unsure_btn":       "\U0001F914 \u1781\u17D2\u1789\u17BB\u17C6\u1798\u17B7\u1793\u1791\u17B6\u1793\u17CB\u1794\u17D2\u179A\u17B6\u1780\u178A \u2014 \u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A\u1796\u17B7\u1782\u17D2\u179A\u17C4\u17C7",
            "consult_msg": (
                "\U0001F4AC *\u17A2\u179A\u1782\u17BB\u178E\u1794\u1784\u178A\u17C2\u179B\u1794\u17B6\u1793\u1791\u17B6\u1780\u17CB\u1791\u1784 NiMo!*\n\n"
                "NiMo \u1793\u17B9\u1784\u1786\u17D2\u179B\u17BE\u1799\u178F\u1794\u1794\u1784\u1786\u17B6\u1794\u17CB\u17D7\u17D4\n\n"
                "\u23F3 \u179F\u17BC\u1798\u179A\u1784\u17CB\u1785\u17B6\u17C6\u1794\u1793\u17D2\u178F\u17B7\u1785 \u2764\uFE0F"
            ),
            "end_consult_btn":  "\U0001F51A \u1794\u1789\u17D2\u1785\u1794\u17CB \u2014 \u178F\u17D2\u179A\u17A1\u1794\u17CB\u1791\u17C5\u1798\u17C9\u17BA\u1793\u17BB\u1799",
            "end_consult_msg":  "\u2705 \u1794\u17B6\u1793\u1794\u1789\u17D2\u1785\u1794\u17CB\u17D4 \u17A2\u179A\u1782\u17BB\u178E\u1794\u1784 \u2764\uFE0F\n\n\u1785\u17BB\u1785 /start \u178A\u17BE\u1798\u17D2\u1794\u17B8\u1794\u17BE\u1780\u1798\u17C9\u17BA\u1793\u17BB\u1799\u17D4",
            "confirm_paid_btn": "\u2705 \u1781\u17D2\u1789\u17BB\u17C6\u1794\u17B6\u1793\u1795\u17D2\u1791\u17C1\u179A\u1794\u17D2\u179A\u17B6\u1780\u17CB\u179A\u17BD\u1785\u17A0\u17BE\u1799",
            "ask_more_btn":     "\u2753 \u1781\u17D2\u1789\u17BB\u17C6\u178F\u17D2\u179A\u17BC\u179C\u1780\u17B6\u179A\u179F\u17BD\u179A\u1794\u1793\u17D2\u1790\u17C2\u1798",
            "view_payment_btn": "\U0001F4B3 \u1798\u17BE\u179B\u1796\u17D0\u178F\u17CC\u1798\u17B6\u1793\u1795\u17D2\u1791\u17C1\u179A\u1794\u17D2\u179A\u17B6\u1780\u17CB",
            "unknown_msg":      "\u1781\u17D2\u1789\u17BB\u17C6\u1791\u1791\u17BD\u179B\u1794\u17B6\u1793\u179F\u17B6\u179A\u1794\u1784\u17A0\u17BE\u1799 \u2764\uFE0F\n\n\u1794\u1784\u1785\u1784\u17CB:",
            "ask_bill":         "\U0001F4F8 *\u1787\u17C6\u17A0\u17B6\u1793\u1791\u17B8 1/3: \u1795\u17D2\u1789\u17BE\u179A\u17BC\u1794\u1797\u17B6\u1796\u1794\u1784\u17D2\u1780\u17B6\u1793\u17CB\u178A\u17C3*\n\n\u179F\u17BC\u1798 *\u1790\u178F\u17A2\u17C1\u1780\u17D2\u179A\u1784\u17CB* \u1780\u17B6\u179A\u1795\u17D2\u1791\u17C1\u179A\u1794\u17D2\u179A\u17B6\u1780\u17CB \U0001F447",
            "need_photo":       "\u26A0\uFE0F \u179F\u17BC\u1798\u1795\u17D2\u1789\u17BE *\u179A\u17BC\u1794\u1797\u17B6\u1796* \u1794\u1784\u17D2\u1780\u17B6\u1793\u17CB\u178A\u17C3 \U0001F4F8",
            "ask_name":         "\u2705 \u1791\u1791\u17BD\u179B\u1794\u17B6\u1793\u179A\u17BC\u1794\u1797\u17B6\u1796\u17A0\u17BE\u1799!\n\n\U0001F464 *\u1787\u17C6\u17A0\u17B6\u1793\u1791\u17B8 2/3: \u1788\u17D2\u1798\u17C4\u17C7\u1796\u17C1\u1789*\n\n\u179F\u17BC\u1798\u179C\u17B6\u1799\u1788\u17D2\u1798\u17C4\u17C7\u179A\u1794\u179F\u17CB\u1794\u1784:",
            "need_text":        "\u26A0\uFE0F \u179F\u17BC\u1798\u179C\u17B6\u1799\u1787\u17B6\u17A2\u1780\u17D2\u179F\u179A\u17D4",
            "ask_phone":        "\u2705 \u1791\u1791\u17BD\u179B\u1794\u17B6\u1793\u1788\u17D2\u1798\u17C4\u17C7\u17A0\u17BE\u1799!\n\n\U0001F4F1 *\u1787\u17C6\u17A0\u17B6\u1793\u1791\u17B8 3/3: \u179B\u17C1\u1781\u1791\u17BC\u179A\u179F\u17D0\u1796\u17D2\u1791*\n\n\u179F\u17BC\u1798\u1794\u1789\u17D2\u1785\u17BC\u179B\u179B\u17C1\u1781\u1791\u17BC\u179A\u179F\u17D0\u1796\u17D2\u1791:",
            "complete_msg": (
                "\U0001F389 *\u1791\u1791\u17BD\u179B\u1794\u17B6\u1793\u1796\u17D0\u178F\u17CC\u1798\u17B6\u1793\u1782\u17D2\u179A\u1794\u17CB\u1782\u17D2\u179A\u17B6\u1793\u17CB\u17A0\u17BE\u1799!*\n\n"
                "\U0001F4CB *\u179F\u1784\u17D2\u1781\u17C1\u1794\u1780\u17B6\u179A\u1794\u1789\u17D2\u1787\u17B6\u1791\u17B7\u1789:*\n"
                "\u2022 \u179B\u17C1\u1781\u1780\u17BC\u178A: `{order_id}`\n"
                "\u2022 \u1788\u17D2\u1798\u17C4\u17C7: {name}\n"
                "\u2022 \u1791\u17BC\u179A\u179F\u17D0\u1796\u17D2\u1791: {phone}\n"
                "\u2022 \u1780\u1789\u17D2\u1785\u1794\u17CB: {label} ({price_usd})\n\n"
                "NiMo \u1793\u17B9\u1784\u1796\u17B7\u1793\u17B7\u178F\u17D2\u1799 \u1793\u17B7\u1784\u1794\u1789\u17D2\u1787\u17B6\u1780\u17CB\u1780\u17D2\u1793\u17BB\u1784 *30 \u1793\u17B6\u1791\u17B8* \u23F0\n\n"
                "\u17A2\u179A\u1782\u17BB\u178E\u1794\u1784\u178A\u17C2\u179B\u1791\u17BB\u1780\u1785\u17B7\u178F\u17D2\u178F NiMo \u2764\uFE0F"
            ),
            "package_msg": (
                "\U0001F389 *\u1794\u1784\u1794\u17B6\u1793\u1787\u17D2\u179A\u17BE\u179F {label} \u2014 {price_usd}* ({price_riel})\n\n"
                "{bank_details}\n\n"
                "\U0001F4B5 *\u1785\u17C6\u1793\u17BD\u1793\u1791\u17B9\u1780\u1794\u17D2\u179A\u17B6\u1780\u17CB: {price_usd}*\n\n"
                "\u1794\u1793\u17D2\u1791\u17B6\u1794\u17CB\u1796\u17B8\u1795\u17D2\u1791\u17C1\u179A\u1794\u17D2\u179A\u17B6\u1780\u17CB\u17A0\u17BE\u1799 \u179F\u17BC\u1798\u1785\u17BB\u1785\u1794\u17CA\u17BC\u178F\u17BB\u1784\u1781\u17B6\u1784\u1780\u17D2\u179A\u17C4\u1798 \U0001F447"
            ),
        },
    },

    "en": {
        "faq": {
            "q_nimo": {
                "label": "\U0001F464 Who is NiMo?",
                "answer": (
                    "\U0001F464 *Who is NiMo?*\n\n"
                    "NiMo was created from a simple desire:\n\n"
                    "_To contribute something meaningful to the business community in Cambodia._\n\n"
                    "While neighboring countries have used AI to automate businesses for years \u2014 "
                    "many business owners in Cambodia are still doing everything manually every day. "
                    "Not because they don't want to change \u2014 but because no tool has truly fit them.\n\n"
                    "NiMo was born to bridge that gap \u2014 "
                    "helping Cambodian shop owners access AI practically, easily, in their own language."
                ),
            },
            "q_system": {
                "label": "\U0001F4AC I don't understand how this system works",
                "answer": (
                    "\U0001F4AC *How does Cambodia Biz Agent work?*\n\n"
                    "Simply put: you get *5 AI Employees* \u2014 each does 1 job:\n\n"
                    "\U0001F50D Market research & competitor analysis\n"
                    "\U0001F4E3 Create content for FB/TikTok/Instagram\n"
                    "\U0001F4B0 Write sales pages & close orders\n"
                    "\U0001F4E6 Auto-receive orders & send delivery notifications\n"
                    "\U0001F4CA Revenue reports & weekly optimization\n\n"
                    "You give commands in Khmer or English \u2014 AI works instantly.\n\n"
                    "No coding needed. \U0001F680"
                ),
            },
            "q_different": {
                "label": "\U0001F19A How is this different from other AI agents?",
                "answer": (
                    "\U0001F19A *How is Cambodia Biz Agent different from other agents?*\n\n"
                    "Most AI Agents are built for Western markets \u2014 "
                    "English, Stripe payments, US/EU business styles.\n\n"
                    "*Cambodia Biz Agent is different: built specifically for Cambodian business owners.*\n\n"
                    "\U0001F1F0\U0001F1ED *Language:* Natural Khmer \u2014 not machine translation\n\n"
                    "\U0001F4B3 *Payments:* ABA Pay, Wing Money, Bakong KHQR \u2014 no international card needed\n\n"
                    "\U0001F4F1 *Platforms:* Facebook, TikTok, Telegram \u2014 where Cambodian customers buy\n\n"
                    "\U0001F91D *Support:* NiMo is based in Cambodia, understands the market, gives direct support\n\n"
                    "Built from the real realities of this market \u2014 not copied from elsewhere."
                ),
            },
            "q_save": {
                "label": "\U0001F4B0 What will I save?",
                "answer": (
                    "\U0001F4B0 *What specifically will I save?*\n\n"
                    "What you save most \u2014 not money. *Time.*\n\n"
                    "Average shop owners spend ~3 hours/day on repetitive tasks: "
                    "writing captions, replying messages, posting, compiling orders.\n\n"
                    "*3 hours \u00D7 30 days = 90 hours/month* \u2014 Cambodia Biz Agent handles all that.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "On money \u2014 real numbers:\n\n"
                    "\U0001F50D Market research: $100\u2013200/time\n"
                    "\U0001F4E3 Content writing: $50\u2013150/month\n"
                    "\U0001F4AC Order closing: $200\u2013300/month\n"
                    "\U0001F4E6 Order processing: $150\u2013250/month\n"
                    "\U0001F4CA Reporting: $100\u2013200/month\n\n"
                    "*Hiring people: ~$700\u20131,200/month*\n\n"
                    "Cambodia Biz Agent: one-time only\n"
                    "\U0001F7E6 Basic $97 \u00B7 \u2B50 Pro $297 \u00B7 \U0001F7E1 VIP $597\n\n"
                    "Year 1: save *$8,000\u201314,000* compared to hiring \U0001F4B0"
                ),
            },
            "q_location": {
                "label": "\U0001F3E2 Where is NiMo's office?",
                "answer": (
                    "\U0001F3E2 *Where is NiMo's office?*\n\n"
                    "NiMo operates fully online \u2014 no physical office. "
                    "This is a modern digital business model, like buying an app or online course "
                    "\u2014 you don't need to know where the office is to use it.\n\n"
                    "What matters more than an address: NiMo offers a *30-day 100% money-back guarantee* "
                    "if you're not satisfied. That's a clearer commitment than any address. \u2764\uFE0F"
                ),
            },
            "q_price": {
                "label": "\U0001F4B5 How much does Cambodia Biz Agent cost?",
                "answer": (
                    "\U0001F4B5 *How much does Cambodia Biz Agent cost? Monthly fees?*\n\n"
                    "Buy once \u2014 use forever. 3 plans to choose from:\n\n"
                    "\U0001F7E6 *Basic $97* (\u2248 400,000 Riel)\n"
                    "First-time trial \u2014 lowest risk\n\n"
                    "\u2B50 *Pro $297* (\u2248 1,200,000 Riel)\n"
                    "Full automation 24/7\n\n"
                    "\U0001F7E1 *VIP $597* (\u2248 2,400,000 Riel)\n"
                    "NiMo installs directly via Zoom \u2014 done and ready to use immediately\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Only ongoing cost: Claude Pro account ~$20/month.\n\n"
                    "*No hidden fees. No renewals. No surprises.*"
                ),
            },
            "q_which_plan": {
                "label": "\U0001F914 I don't know which plan fits me",
                "answer": (
                    "\U0001F914 *Which plan fits your shop?*\n\n"
                    "\U0001F7E6 *Basic $97* \u2014 New to AI, want to try first\n"
                    "\u2192 5 AI Employees + Khmer guide + 30-day support\n\n"
                    "\u2B50 *Pro $297* \u2014 Shop running, want full automation 24/7\n"
                    "\u2192 Chatbot + auto-post + auto-booking\n\n"
                    "\U0001F7E1 *VIP $597* \u2014 Don't want to install yourself\n"
                    "\u2192 NiMo installs everything, ready to use, 90-day support\n\n"
                    "Not sure? Tell NiMo about your shop \u2014 we'll recommend the right plan in 5 mins \U0001F447"
                ),
            },
            "q_worth": {
                "label": "\U0001F48E Is $297 worth it?",
                "answer": (
                    "\U0001F48E *Is $297 (or whatever I spend) worth it?*\n\n"
                    "Let the numbers answer.\n\n"
                    "*Inbox staff in Cambodia:* $200\u2013300/month\n"
                    "\u2192 8 hours/day. Takes holidays. Asks for raises. Gets sick.\n\n"
                    "*Cambodia Biz Agent Pro $297* \u2014 one-time\n"
                    "\u2192 24/7. No holidays. No raises. Never quits.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "$297 = less than one month of inbox staff.\n\n"
                    "But Cambodia Biz Agent works for you *forever*.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "If AI helps you close just *5 extra orders/month* \u2014 $297 already paid for itself."
                ),
            },
            "q_warranty": {
                "label": "\U0001F6E1\uFE0F Is there a warranty / refund policy?",
                "answer": (
                    "\U0001F6E1\uFE0F *Is there a warranty? Can I get a refund?*\n\n"
                    "Yes \u2014 and NiMo is confident about this.\n\n"
                    "*30-day guarantee \u2014 100% refund, no questions asked.*\n\n"
                    "Buy Cambodia Biz Agent. Follow the guide for 30 days. "
                    "If the system doesn't work as NiMo described \u2014 "
                    "message NiMo on Telegram. Refund within 24 hours.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*The risk is on NiMo. Not on you.* \u2764\uFE0F"
                ),
            },
            "q_tech": {
                "label": "\U0001F630 I'm afraid I can't install it",
                "answer": (
                    "\U0001F630 *Not tech-savvy \u2014 can I still install it?*\n\n"
                    "Yes! Here's why:\n\n"
                    "\u2705 Step-by-step guide in Khmer with images\n"
                    "\u2705 Video tutorials to follow\n"
                    "\u2705 Bot support 24/7\n"
                    "\u2705 NiMo personally answers when needed\n\n"
                    "VIP plan: NiMo installs it with you via Zoom in 2 hours \u2014 "
                    "you just watch and click. \U0001F3AF"
                ),
            },
            "q_time": {
                "label": "\u23F0 How long does setup take?",
                "answer": (
                    "\u23F0 *How long before I can start using it?*\n\n"
                    "*Basic & Pro:* Self-install following the guide ~2\u20133 hours \u2014 "
                    "do it in the evening or when free, no need to stop selling. "
                    "Day 2 you can create content. Day 3 the system runs on its own.\n\n"
                    "*VIP:* Just 1 Zoom session 2 hours with NiMo \u2014 "
                    "you watch, NiMo does everything, tests and hands over. Done.\n\n"
                    "Many NiMo customers buy in the morning \u2014 by evening they already have their first content to post \U0001F680"
                ),
            },
            "q_device": {
                "label": "\U0001F4F1 What devices do I need?",
                "answer": (
                    "\U0001F4F1 *What devices do I need to use this?*\n\n"
                    "Both computer and smartphone work \u2014 use whatever you have \U0001F60A\n\n"
                    "\U0001F4BB *Computer:* Recommended for initial setup and viewing reports \u2014 bigger screen is easier.\n\n"
                    "\U0001F4F1 *Smartphone only:* After NiMo helps with setup, you can run everything by phone \u2014 "
                    "reply to customers, post content, check revenue, all on app.\n\n"
                    "If it can scroll Facebook smoothly \u2014 it can run Cambodia Biz Agent. No upgrades needed."
                ),
            },
            "q_internet": {
                "label": "\U0001F310 Do I need fast internet?",
                "answer": (
                    "\U0001F310 *Do I need high-speed internet?*\n\n"
                    "No \u2014 just internet good enough for Facebook and Telegram.\n\n"
                    "Home WiFi or 4G both work fine. The system runs on cloud servers \u2014 "
                    "your device only needs to send commands, not do heavy processing \U0001F680"
                ),
            },
            "q_team": {
                "label": "\U0001F465 Can my staff use it too?",
                "answer": (
                    "\U0001F465 *Can my shop staff use it together?*\n\n"
                    "Absolutely! NiMo designed Cambodia Biz Agent for the whole shop \u2014 not just one person \U0001F60A\n\n"
                    "\u2705 Inbox staff use AI to reply customers faster\n"
                    "\u2705 Content staff use AI to create daily posts\n"
                    "\u2705 Managers use AI to view revenue reports\n\n"
                    "Everyone accesses one account \u2014 easy collaboration, no user limit.\n\n"
                    "\U0001F4A1 Claude Pro $20/month can be shared across the whole team \u2014 split the cost, no need for individual accounts."
                ),
            },
            "q_data": {
                "label": "\U0001F512 Will my shop data be leaked?",
                "answer": (
                    "\U0001F512 *Will my shop data be leaked?*\n\n"
                    "NiMo understands your concern \u2014 and here's NiMo's clear commitment: your data is completely safe.\n\n"
                    "\u2705 *Your data belongs to you:* Customers, orders, messages \u2014 all stored in your own account, no one else can access.\n\n"
                    "\u2705 *NiMo doesn't touch your shop data:* NiMo doesn't collect, sell, or share your data with anyone.\n\n"
                    "\u2705 *International security standards:* Built on Anthropic's platform (US) \u2014 same security standard as banks.\n\n"
                    "Your shop \u2192 your data \u2192 your control. NiMo keeps nothing. \u2764\uFE0F"
                ),
            },
            "q_after_warranty": {
                "label": "\U0001F91D What happens after the warranty?",
                "answer": (
                    "\U0001F91D *What support after the 30-day warranty?*\n\n"
                    "The 30-day warranty is just the refund policy \u2014 NiMo supports you with no time limit \U0001F60A\n\n"
                    "\u2705 Message NiMo on Telegram anytime \u2014 bugs, advice, optimization, NiMo is there.\n\n"
                    "\u2705 Join community group \u2014 learn from other shop owners using Cambodia Biz Agent.\n\n"
                    "\u2705 Receive updates when NiMo upgrades the system \u2014 completely free.\n\n"
                    "NiMo sells you the system \u2014 but doesn't abandon you after receiving payment. \u2764\uFE0F"
                ),
            },
            "q_update": {
                "label": "\U0001F199 Are there updates?",
                "answer": (
                    "\U0001F199 *Are there future updates/upgrades? Do they cost extra?*\n\n"
                    "Regular updates \u2014 completely free for existing customers \U0001F381\n\n"
                    "NiMo continually improves Cambodia Biz Agent based on real feedback. When there are:\n\n"
                    "\u2705 New features\n"
                    "\u2705 Better AI commands\n"
                    "\u2705 Speed & effectiveness improvements\n\n"
                    "\u2192 You receive updates automatically via group, no extra payment.\n\n"
                    "Buy once \u2014 get upgraded forever."
                ),
            },
            "q_community": {
                "label": "\U0001F465 Is there a community group?",
                "answer": (
                    "\U0001F465 *Does NiMo have a community group?*\n\n"
                    "Yes! This is one of the values NiMo is most proud of \U0001F49B\n\n"
                    "After purchasing, NiMo adds you to a *private Telegram community* where you:\n\n"
                    "\u2705 Meet other Cambodian shop owners \u2014 share real daily experiences.\n\n"
                    "\u2705 Learn more effective AI usage from those who went before.\n\n"
                    "\u2705 Receive new tips & AI commands NiMo updates weekly.\n\n"
                    "\u2705 Get quick answers \u2014 NiMo and community are ready to help.\n\n"
                    "You never go alone \u2014 the whole community goes with you \u2764\uFE0F"
                ),
            },
            "q_competitor": {
                "label": "\u2694\uFE0F What if competitors use it too?",
                "answer": (
                    "\u2694\uFE0F *If competitors use it too, do I still have an advantage?*\n\n"
                    "Yes \u2014 even a bigger advantage if you start earlier.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*Right now most Cambodian shop owners don't use AI.* "
                    "Every day you wait is a day competitors get ahead.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*Same tool \u2260 same results.*\n\n"
                    "Two shops using Cambodia Biz Agent \u2014 but:\n"
                    "\u2022 Different products\n"
                    "\u2022 Different brand styles\n"
                    "\u2022 Different customer approaches\n\n"
                    "AI learns your shop's specific characteristics \u2014 nobody has an exact copy.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Real advantage = using the tool *earlier, better, more consistently*."
                ),
            },
            "q_think": {
                "label": "\U0001F914 Let me think about it",
                "answer": (
                    "\U0001F914 *Let me think about it*\n\n"
                    "Of course \u2014 this is a business decision \U0001F60A\n\n"
                    "But before thinking, 3 things NiMo wants you to know:\n\n"
                    "*One \u2014 Current price is early bird.*\n"
                    "After launch, price goes up. Buying today = best price.\n\n"
                    "*Two \u2014 30-day 100% money-back guarantee.*\n"
                    "You're trying with virtually zero real risk. Not happy \u2192 refund.\n\n"
                    "*Three \u2014 Every day you wait is a day lost.*\n"
                    "Not money \u2014 but time, orders, opportunities. Those can't be refunded.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Need more info to decide? NiMo is here \U0001F60A"
                ),
            },
            "q_try": {
                "label": "\U0001F9EA I want to try before buying",
                "answer": (
                    "\U0001F9EA *I want to try before buying*\n\n"
                    "NiMo understands \u2014 and doesn't blame that \U0001F60A\n\n"
                    "But think: trying before buying means you want real results, on your real shop, with your real products.\n\n"
                    "*There's no way to do that without actually starting.*\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "That's why NiMo has *Basic $97* \u2014 this is essentially a \"try with refund\" option:\n\n"
                    "\u2705 Full 5 AI Employees experience\n"
                    "\u2705 Run on your real shop\n"
                    "\u2705 See real results in 30 days\n"
                    "\u2705 Not satisfied \u2192 100% refund\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*The real risk isn't buying. The real risk is continuing alone \u2014 when there's another way.*"
                ),
            },
            "q_claude_pro": {
                "label": "\U0001F4B3 What is Claude Pro $20/month?",
                "answer": (
                    "\U0001F4B3 *What is Claude Pro $20/month? Is it required?*\n\n"
                    "Cambodia Biz Agent runs on Claude AI (by Anthropic \u2014 US). "
                    "To use it, you need a Claude Pro account at *$20/month* \u2014 "
                    "paid directly to Anthropic, not through NiMo.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "But look at the real cost:\n\n"
                    "\u2705 $20/month = 1 employee working 24/7, no holidays, no raises\n"
                    "\u2705 All 5 AI Agents run on 1 account \u2014 whole team shares\n"
                    "\u2705 Cancel anytime \u2014 no commitment\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Inbox staff in Cambodia = $200\u2013300/month.\n"
                    "Claude Pro = $20/month. *Save $180\u2013280 every month.*"
                ),
            },
            "q_riel": {
                "label": "\U0001F4B5 Can I pay in Riel?",
                "answer": (
                    "\U0001F4B5 *Can I pay in Riel?*\n\n"
                    "Yes! Transfer in Riel normally \u2014 "
                    "ABA Bank automatically converts to USD.\n\n"
                    "\U0001F7E6 *Basic $97* \u2248 400,000 Riel\n"
                    "\u2B50 *Pro $297* \u2248 1,200,000 Riel\n"
                    "\U0001F7E1 *VIP $597* \u2248 2,400,000 Riel"
                ),
            },
            "q_industry": {
                "label": "\U0001F6CD\uFE0F Does my business type work?",
                "answer": (
                    "\U0001F6CD\uFE0F *I sell [food/beauty/fashion/services]\u2026 will it work?*\n\n"
                    "NiMo's short answer: *if you sell online in Cambodia, your shop works.*\n\n"
                    "NiMo has tested Cambodia Biz Agent across many industries:\n\n"
                    "\U0001F457 Fashion & accessories\n"
                    "\U0001F484 Beauty & skincare\n"
                    "\U0001F371 Food & specialty\n"
                    "\U0001F4DA Courses & consulting\n"
                    "\U0001F486 Spa, salon, studio\n"
                    "\U0001F3E0 Furniture & home goods\n"
                    "\U0001F338 Flowers & gifts\n\n"
                    "AI learns according to your shop's products and style \u2014 not a rigid formula.\n\n"
                    "Not sure? Tell NiMo your specific industry \u2014 free consultation \U0001F447"
                ),
            },
            "q_delivery": {
                "label": "\U0001F4E6 How do I receive after paying?",
                "answer": (
                    "\U0001F4E6 *After transferring, how do I receive the product?*\n\n"
                    "Simple \u2014 just 4 steps:\n\n"
                    "*Step 1 \u2014 Transfer*\n"
                    "Choose a plan \u2192 transfer to the info NiMo provides\n\n"
                    "*Step 2 \u2014 Send confirmation*\n"
                    "Screenshot the transfer \u2192 send with name + phone + chosen plan to bot\n\n"
                    "*Step 3 \u2014 NiMo confirms & delivers*\n"
                    "NiMo verifies and sends the full product within 30 minutes\n\n"
                    "*Step 4 \u2014 Receive & begin*\n"
                    "Get the Kit + guide PDF + videos + support group \u2014 start setup \U0001F680\n\n"
                    "*VIP:* After receiving the Kit, NiMo contacts you to schedule a Zoom session."
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "\U0001F50D Learn about Cambodia Biz Agent",
                "questions": ["q_nimo", "q_system", "q_different", "q_save", "q_location"],
            },
            "cat_price": {
                "label": "\U0001F4B0 Pricing & Plans",
                "questions": ["q_price", "q_which_plan", "q_worth", "q_warranty"],
            },
            "cat_tech": {
                "label": "\U0001F6E0\uFE0F Setup & Technology",
                "questions": ["q_tech", "q_time", "q_device", "q_internet", "q_team"],
            },
            "cat_support": {
                "label": "\U0001F512 Warranty & Support",
                "questions": ["q_data", "q_after_warranty", "q_update", "q_community"],
            },
            "cat_doubt": {
                "label": "\U0001F914 Still Hesitating",
                "questions": ["q_competitor", "q_think", "q_try"],
            },
            "cat_buy": {
                "label": "\U0001F6CD\uFE0F Buying",
                "questions": ["q_claude_pro", "q_riel", "q_industry", "q_delivery"],
            },
        },
        "s": {
            "welcome": (
                "\U0001F44B Hello! I'm the assistant of *NiMo Team*.\n\n"
                "What are you wondering about *Cambodia Biz Agent*?\n"
                "Choose a question below \u2014 I'll answer right away \U0001F447"
            ),
            "choose_cat":       "Choose a question:",
            "buy_title": (
                "\U0001F389 *Great! Which plan do you want?*\n\n"
                "\U0001F7E6 *Basic $97* \u2014 Try it first\n"
                "\u2B50 *Pro $297* \u2014 Full automation 24/7\n"
                "\U0001F7E1 *VIP $597* \u2014 NiMo installs it for you\n\n"
                "Choose a plan \U0001F447"
            ),
            "buy_btn":          "\U0001F4B3 I WANT TO BUY NOW",
            "consult_btn":      "\U0001F4AC Chat directly with NiMo",
            "back_btn":         "\u2B05\uFE0F Back to main menu",
            "back_cat":         "\u2B05\uFE0F Other questions",
            "unsure_btn":       "\U0001F914 I'm not sure \u2014 need advice",
            "consult_msg": (
                "\U0001F4AC *Thank you for contacting NiMo!*\n\n"
                "Your message has been forwarded to our team.\n\n"
                "\u23F3 Please wait a moment \u2014 we'll reply shortly. \u2764\uFE0F"
            ),
            "end_consult_btn":  "\U0001F51A End consultation \u2014 back to menu",
            "end_consult_msg":  "\u2705 Consultation ended. Thank you \u2764\uFE0F\n\nType /start to open the menu again.",
            "confirm_paid_btn": "\u2705 I have transferred \u2014 send receipt",
            "ask_more_btn":     "\u2753 I have more questions",
            "view_payment_btn": "\U0001F4B3 View payment details",
            "unknown_msg":      "I received your message \u2764\uFE0F\n\nWhat would you like to do?",
            "ask_bill":         "\U0001F4F8 *Step 1/3: Send payment receipt*\n\nPlease *screenshot* the bank transfer confirmation \U0001F447",
            "need_photo":       "\u26A0\uFE0F Please send a *photo* of your receipt \U0001F4F8",
            "ask_name":         "\u2705 Receipt received!\n\n\U0001F464 *Step 2/3: Full name*\n\nPlease enter your full name:",
            "need_text":        "\u26A0\uFE0F Please enter text.",
            "ask_phone":        "\u2705 Name received!\n\n\U0001F4F1 *Step 3/3: Phone number*\n\nPlease enter your phone number:",
            "complete_msg": (
                "\U0001F389 *All information received!*\n\n"
                "\U0001F4CB *Order summary:*\n"
                "\u2022 Order ID: `{order_id}`\n"
                "\u2022 Name: {name}\n"
                "\u2022 Phone: {phone}\n"
                "\u2022 Plan: {label} ({price_usd})\n\n"
                "NiMo will verify and confirm within *30 minutes* \u23F0\n\n"
                "Thank you for trusting NiMo \u2764\uFE0F"
            ),
            "package_msg": (
                "\U0001F389 *You selected {label} \u2014 {price_usd}* ({price_riel})\n\n"
                "{bank_details}\n\n"
                "\U0001F4B5 *Amount to transfer: {price_usd}*\n\n"
                "After transferring, tap the button below to send your receipt \U0001F447"
            ),
        },
    },
}

# \u2500\u2500\u2500 HELPERS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

def get_lang(context) -> str:
    return context.user_data.get("lang", "km")

def C(context):
    return CONTENT[get_lang(context)]

# \u2500\u2500\u2500 KEYBOARDS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("\U0001F1F0\U0001F1ED \u1797\u17B6\u179F\u17B6\u1781\u17D2\u1798\u17C2\u179A", callback_data="lang_km"),
        InlineKeyboardButton("\U0001F1EC\U0001F1E7 English",    callback_data="lang_en"),
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
        [InlineKeyboardButton("\U0001F7E6 Basic $97  (\u2248 400,000 Riel)",   callback_data="buy_basic")],
        [InlineKeyboardButton("\u2B50 Pro $297   (\u2248 1,200,000 Riel)", callback_data="buy_pro")],
        [InlineKeyboardButton("\U0001F7E1 VIP $597  (\u2248 2,400,000 Riel)",  callback_data="buy_vip")],
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

# \u2500\u2500\u2500 HANDLERS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "\U0001F1F0\U0001F1ED \u1787\u17D2\u179A\u17BE\u179F\u1797\u17B6\u179F\u17B6  |  \U0001F1EC\U0001F1E7 Choose language:",
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
                        f"\U0001F4AC *Kh\u00E1ch c\u1EA7n t\u01B0 v\u1EA5n [{lang.upper()}]*\n"
                        f"\U0001F464 {user.full_name} (@{user.username or 'no username'})\n"
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

# \u2500\u2500\u2500 MESSAGE HANDLER \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    awaiting   = context.user_data.get("awaiting")
    consulting = context.user_data.get("consulting", False)
    user       = update.effective_user
    s          = C(context)["s"]

    # Admin reply \u2192 forward to customer
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
                text=f"\U0001F4AC *NiMo:*\n\n{update.message.text}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("\u2705 Sent.")
        except Exception as e:
            await update.message.reply_text(f"\u274C {e}")
        return

    # Consulting mode \u2192 forward to admin
    if consulting and not awaiting:
        text = update.message.text or "(media)"
        if ADMIN_ID:
            try:
                fwd = (
                    f"\U0001F4AC *{user.full_name}* (@{user.username or 'no username'})\n"
                    f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n{text}\n\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n`#cid:{user.id}`"
                )
                await context.bot.send_message(chat_id=ADMIN_ID, text=fwd, parse_mode="Markdown")
                if update.message.photo:
                    await context.bot.send_photo(
                        chat_id=ADMIN_ID,
                        photo=update.message.photo[-1].file_id,
                        caption=f"\U0001F4F8 {user.full_name}\n`#cid:{user.id}`",
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logging.error(f"Forward error: {e}")
        await update.message.reply_text("\u2705", reply_markup=end_consult_keyboard(context))
        return

    # No active flow \u2192 show options
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

    # Phone step \u2192 complete
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
                f"\U0001F534 *\u0110\u01A0N M\u1EDAI [{lang.upper()}]*\n\n"
                f"\U0001F4CB M\u00E3 \u0111\u01A1n: `{context.user_data['order_id']}`\n"
                f"\U0001F464 T\u00EAn: {context.user_data['name']}\n"
                f"\U0001F4F1 S\u0110T: {context.user_data['phone']}\n"
                f"\U0001F4E6 G\u00F3i: *{info['label']}* \u2014 {info['price_usd']}\n"
                f"\U0001F194 Telegram ID: `{user.id}`\n\n"
                f"\U0001F449 L\u1EC7nh x\u00E1c nh\u1EADn:\n"
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

# \u2500\u2500\u2500 ADMIN COMMANDS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

async def xacnhan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("\u26D4")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Syntax: `/xacnhan NIMO-ID package`", parse_mode="Markdown")
        return
    await update.message.reply_text(
        f"\u2705 Confirmed order `{context.args[0]}` \u2014 plan `{context.args[1]}`.\n"
        "_Auto-delivery will be added in the next step._",
        parse_mode="Markdown"
    )

async def tra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin replies to customer: /tra <customer_id> <message>"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("\u26D4")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Syntax: `/tra <customer_id> <message>`", parse_mode="Markdown")
        return
    try:
        cid  = int(context.args[0])
        text = " ".join(context.args[1:])
        await context.bot.send_message(
            chat_id=cid,
            text=f"\U0001F4AC *NiMo:*\n\n{text}",
            parse_mode="Markdown"
        )
        await update.message.reply_text("\u2705 Sent.")
    except Exception as e:
        await update.message.reply_text(f"\u274C {e}")

# \u2500\u2500\u2500 MAIN \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("xacnhan", xacnhan))
    app.add_handler(CommandHandler("tra",     tra))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_message))
    print("\u2705 Bot (KM + EN) \u0111ang ch\u1EA1y... /start \u0111\u1EC3 test!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
