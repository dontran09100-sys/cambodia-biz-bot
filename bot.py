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
        },
        "cats": {
            "cat_intro": {
                "label": "\U0001F50D \u179F\u17D2\u179C\u17C2\u1784\u1799\u179B\u17CB\u17A2\u17C6\u1796\u17B8 Cambodia Biz Agent",
                "questions": ["q_system", "q_which_plan", "q_tech"],
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
        },
        "cats": {
            "cat_intro": {
                "label": "\U0001F50D Learn about Cambodia Biz Agent",
                "questions": ["q_system", "q_which_plan", "q_tech"],
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
