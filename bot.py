"""
Cambodia Biz Agent \u2014 Bot Khmer + English
FAQ + buy flow + admin support
Token: @NiMoBizAgent_bot (Railway)
"""

import logging
import io
import json as _json
import asyncio
import urllib.request
import qrcode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# \u2500\u2500\u2500 KHQR GENERATOR \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

def _tlv(tag: str, value: str) -> str:
    return f"{tag}{len(value):02d}{value}"

def _crc16(data: str) -> int:
    crc = 0xFFFF
    for ch in data:
        crc ^= ord(ch) << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if crc & 0x8000 else (crc << 1)
            crc &= 0xFFFF
    return crc

def make_aba_qr(amount_usd: float) -> io.BytesIO:
    aba_info = _tlv("00", "abaakhppxxx@abaa") + _tlv("01", "008113648")
    amount_s = str(int(amount_usd)) if amount_usd == int(amount_usd) else f"{amount_usd:.2f}"
    body = (
        _tlv("00", "01") + _tlv("01", "12") +
        _tlv("29", aba_info) +
        _tlv("52", "5999") + _tlv("53", "840") +
        _tlv("54", amount_s) +
        _tlv("58", "KH") +
        _tlv("59", "SOVANNY LONG") +
        _tlv("60", "PHNOM PENH") +
        "6304"
    )
    full = body + f"{_crc16(body):04X}"
    buf = io.BytesIO()
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(full)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
    buf.seek(0)
    return buf

# \u2500\u2500\u2500 CONFIG \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

TOKEN           = "8750588238:AAFUJ3o6iR7Cu92on2HdsvLhKP5pQHs15Bo"
ADMIN_ID        = 8704923191
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz3OQtNOOOgXmCwbO-sODdFw_TDQd8zRAMwtEbqML1H3pApYywaYeXzr0gcE44OjOOF/exec"

async def _post_to_sheet(data: dict):
    def _send():
        body = _json.dumps(data).encode()
        req = urllib.request.Request(
            APPS_SCRIPT_URL, data=body,
            headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            logging.warning(f"Sheet POST error: {e}")
    await asyncio.get_event_loop().run_in_executor(None, _send)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# \u2500\u2500\u2500 PAYMENT INFO \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

BANK_INFO = {
    "basic": {"label": "Basic", "price_usd": "$97",  "price_riel": "\u2248 400,000 Riel"},
    "pro":   {"label": "Pro",   "price_usd": "$297", "price_riel": "\u2248 1,200,000 Riel"},
    "vip":   {"label": "VIP",   "price_usd": "$597", "price_riel": "\u2248 2,400,000 Riel"},
}

BANK_DETAILS = {
    "km": (
        "\U0001f4b3 *\u1796\u17d0\u178f\u17cc\u1798\u17b6\u1793\u1780\u17b6\u179a\u1795\u17d2\u1791\u17c1\u179a\u1794\u17d2\u179a\u17b6\u1780\u17cb*\n\n"
        "\U0001f3e6 *ABA Bank*\n"
        "\u179b\u17c1\u1781\u1782\u178e\u1793\u17b8: `000 123 456`\n"
        "\u1788\u17d2\u1798\u17c4\u17c7: NIMO TEAM\n\n"
        "\U0001f4f1 *Wing Money*\n"
        "\u179b\u17c1\u1781\u1791\u17bc\u179a\u179f\u17d0\u1796\u17d2\u1791: `012 345 678`\n"
        "\u1788\u17d2\u1798\u17c4\u17c7: NIMO TEAM\n\n"
        "\u26a0\ufe0f *\u179f\u1798\u17d2\u1782\u17b6\u179b\u17cb:* \u179f\u17bc\u1798\u179f\u179a\u179f\u17c1\u179a\u179b\u17c1\u1781\u1780\u17bc\u178a\u1794\u1789\u17d2\u1787\u17b6\u1791\u17b7\u1789 NiMo \u1795\u17d2\u1789\u17be\u17a2\u17c4\u1799 \u1780\u17d2\u1793\u17bb\u1784\u1780\u17b6\u179a\u1795\u17d2\u1791\u17c1\u179a\u17d4"
    ),
    "en": (
        "\U0001f4b3 *Payment Details*\n\n"
        "\U0001f3e6 *ABA Bank*\n"
        "Account: `000 123 456`\n"
        "Name: NIMO TEAM\n\n"
        "\U0001f4f1 *Wing Money*\n"
        "Phone: `012 345 678`\n"
        "Name: NIMO TEAM\n\n"
        "\u26a0\ufe0f *Note:* Include the order code NiMo provides in the transfer remark."
    ),
}

# \u2500\u2500\u2500 CONTENT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

CONTENT = {
    "km": {
        "faq": {
            "q_nimo": {
                "label": "\U0001f464 NiMo \u1787\u17b6\u1793\u179a\u178e\u17b6?",
                "answer": (
                    "\U0001f464 *NiMo \u1787\u17b6\u1793\u179a\u178e\u17b6?*\n\n"
                    "NiMo \u1794\u17b6\u1793\u1780\u17be\u178f\u1785\u17c1\u1789\u1796\u17b8\u1794\u17c6\u178e\u1784\u1794\u17d2\u179a\u17b6\u1790\u17d2\u1793\u17b6\u1798\u17bd\u1799:\n\n"
                    "_\u1785\u1784\u17cb\u1785\u17c6\u178e\u17bc\u179b\u179a\u17bd\u1798\u17a2\u17d2\u179c\u17b8\u1798\u17bd\u1799\u1798\u17b6\u1793\u17a2\u178f\u17d2\u1790\u1793\u17d0\u1799 \u178a\u179b\u17cb\u179f\u17a0\u1782\u1798\u1793\u17cd\u17a2\u17b6\u1787\u17b8\u179c\u1780\u1798\u17d2\u1798\u1793\u17c5\u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6\u17d4_\n\n"
                    "\u1781\u178e\u17c8\u1794\u17d2\u179a\u1791\u17c1\u179f\u1787\u17b7\u178f\u1781\u17b6\u1784\u1794\u17d2\u179a\u17be AI \u179f\u17d2\u179c\u17d0\u1799\u1794\u17d2\u179a\u179c\u178f\u17d2\u178f\u17b7\u178f\u17b6\u17c6\u1784\u1796\u17b8\u1799\u17bc\u179a \u2014 "
                    "\u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784\u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6\u1787\u17b6\u1785\u17d2\u179a\u17be\u1793\u1793\u17c5\u1792\u17d2\u179c\u17be\u1780\u17b6\u179a\u178a\u17c4\u1799\u178a\u17c3\u17d4 "
                    "\u1798\u17b7\u1793\u1798\u17c2\u1793\u1798\u17b7\u1793\u1785\u1784\u17cb\u1794\u17d2\u178a\u17bc\u179a \u2014 \u1782\u17d2\u179a\u17b6\u1793\u17cb\u178f\u17c2\u1798\u17b7\u1793\u1791\u17b6\u1793\u17cb\u1798\u17b6\u1793\u17a7\u1794\u1780\u179a\u178e\u17cd\u179f\u1798\u179f\u17d2\u179a\u1794\u17d4\n\n"
                    "NiMo \u1780\u17be\u178f\u17a1\u17be\u1784\u178a\u17be\u1798\u17d2\u1794\u17b8\u1794\u17c6\u1796\u17c1\u1789\u1785\u1793\u17d2\u179b\u17c4\u17c7\u1793\u17c4\u17c7 \u2014 "
                    "\u1787\u17bd\u1799\u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784\u1781\u17d2\u1798\u17c2\u179a access AI \u178a\u17c4\u1799\u1784\u17b6\u1799 \u1787\u17b6\u1797\u17b6\u179f\u17b6\u179a\u1794\u179f\u17cb\u1781\u17d2\u179b\u17bd\u1793\u17d4"
                ),
            },
            "q_system": {
                "label": "\U0001f4ac \u1781\u17d2\u1789\u17bb\u17c6\u1798\u17b7\u1793\u1791\u17b6\u1793\u17cb\u1799\u179b\u17cb\u1785\u17d2\u1794\u17b6\u179f\u17cb\u17a2\u17c6\u1796\u17b8\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u1793\u17c1\u17c7",
                "answer": (
                    "\U0001f4ac *\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792 Cambodia Biz Agent \u178a\u17c6\u178e\u17be\u179a\u1780\u17b6\u179a\u1799\u17c9\u17b6\u1784\u178a\u17bc\u1785\u1798\u17d2\u178f\u17c1\u1785?*\n\n"
                    "\u1799\u179b\u17cb\u17b1\u17d2\u1799\u179f\u17b6\u1798\u1789\u17d2\u1789: \u1794\u1784 \u1798\u17b6\u1793 *\u1794\u17bb\u1782\u17d2\u1782\u179b\u17b7\u1780 AI \u1785\u17c6\u1793\u17bd\u1793 5 \u1793\u17b6\u1780\u17cb* \u2014 \u1798\u17d2\u1793\u17b6\u1780\u17cb\u1792\u17d2\u179c\u17be\u1780\u17b6\u179a\u1784\u17b6\u179a 1:\n\n"
                    "\U0001f50d \u179f\u17d2\u179a\u17b6\u179c\u1787\u17d2\u179a\u17b6\u179c\u1791\u17b8\u1795\u17d2\u179f\u17b6\u179a \u1793\u17b7\u1784\u1782\u17bc\u1794\u17d2\u179a\u1787\u17c2\u1784\n"
                    "\U0001f4e3 \u1794\u1784\u17d2\u1780\u17be\u178f\u1798\u17b6\u178f\u17b7\u1780\u17b6 FB/TikTok/Instagram\n"
                    "\U0001f4b0 \u179f\u179a\u179f\u17c1\u179a\u1791\u17c6\u1796\u17d0\u179a\u179b\u1780\u17cb \u1793\u17b7\u1784\u1794\u17b7\u1791\u1780\u17b6\u179a\u1794\u1789\u17d2\u1787\u17b6\u1791\u17b7\u1789\n"
                    "\U0001f4e6 \u1791\u1791\u17bd\u179b\u1780\u17b6\u179a\u1794\u1789\u17d2\u1787\u17b6\u1791\u17b7\u1789 \u1793\u17b7\u1784\u1787\u17bc\u1793\u178a\u17c6\u178e\u17b9\u1784\u178a\u17c4\u1799\u179f\u17d2\u179c\u17d0\u1799\u1794\u17d2\u179a\u179c\u178f\u17d2\u178f\u17b7\n"
                    "\U0001f4ca \u179a\u1794\u17b6\u1799\u1780\u17b6\u179a\u178e\u17cd\u1785\u17c6\u178e\u17bc\u179b \u1793\u17b7\u1784\u1794\u1784\u17d2\u1780\u17be\u1793\u1794\u17d2\u179a\u179f\u17b7\u1791\u17d2\u1792\u1797\u17b6\u1796\n\n"
                    "\u1794\u1784\u1794\u1789\u17d2\u1787\u17b6\u1787\u17b6\u1797\u17b6\u179f\u17b6\u1781\u17d2\u1798\u17c2\u179a \u2014 AI \u1792\u17d2\u179c\u17be\u1780\u17b6\u179a\u1797\u17d2\u179b\u17b6\u1798\u17d7\u17d4\n\n"
                    "\u1798\u17b7\u1793\u1785\u17b6\u17c6\u1794\u17b6\u1785\u17cb\u1785\u17c1\u17c7\u179f\u179a\u179f\u17c1\u179a\u1780\u17bc\u178a\u17d4 \U0001f680"
                ),
            },
            "q_different": {
                "label": "\U0001f19a Cambodia Biz Agent \u1781\u17bb\u179f\u1796\u17b8 Agent \u178a\u1791\u17c3?",
                "answer": (
                    "\U0001f19a *Cambodia Biz Agent \u1781\u17bb\u179f\u1796\u17b8 Agent \u178a\u1791\u17c3\u178a\u17bc\u1785\u1798\u17d2\u178a\u17c1\u1785?*\n\n"
                    "AI Agent \u1787\u17b6\u1785\u17d2\u179a\u17be\u1793\u178f\u17d2\u179a\u17bc\u179c\u1794\u17b6\u1793\u179f\u17b6\u1784\u179f\u1784\u17cb\u179f\u1798\u17d2\u179a\u17b6\u1794\u17cb\u1791\u17b8\u1795\u17d2\u179f\u17b6\u179a\u1781\u17b6\u1784\u179b\u17b7\u1785 \u2014 "
                    "\u1797\u17b6\u179f\u17b6\u17a2\u1784\u17cb\u1782\u17d2\u179b\u17c1\u179f Stripe payments \u179f\u17d2\u1791\u17b8\u179b US/EU \u17d4\n\n"
                    "*Cambodia Biz Agent \u1781\u17bb\u179f: \u179f\u17b6\u1784\u179f\u1784\u17cb\u1787\u17b6\u1796\u17b7\u179f\u17c1\u179f\u179f\u1798\u17d2\u179a\u17b6\u1794\u17cb\u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784\u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6\u17d4*\n\n"
                    "\U0001f1f0\U0001f1ed *\u1797\u17b6\u179f\u17b6:* \u1781\u17d2\u1798\u17c2\u179a\u1792\u1798\u17d2\u1798\u1787\u17b6\u178f\u17b7 \u2014 \u1798\u17b7\u1793\u1798\u17c2\u1793 google translate\n\n"
                    "\U0001f4b3 *\u1780\u17b6\u179a\u1791\u17bc\u1791\u17b6\u178f\u17cb:* ABA Pay, Wing Money, Bakong KHQR \u2014 \u1782\u17d2\u1798\u17b6\u1793\u1780\u17b6\u178f\u17a2\u1793\u17d2\u178f\u179a\u1787\u17b6\u178f\u17b7\n\n"
                    "\U0001f4f1 *\u179c\u17c1\u1791\u17b7\u1780\u17b6:* Facebook, TikTok, Telegram \u2014 \u178f\u17d2\u179a\u17bc\u179c\u1787\u17b6\u1780\u1793\u17d2\u179b\u17c2\u1784\u1781\u17d2\u1798\u17c2\u179a\u1791\u17b7\u1789\n\n"
                    "\U0001f91d *\u1787\u17c6\u1793\u17bd\u1799:* NiMo \u1793\u17c5\u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6 \u1799\u179b\u17cb\u1791\u17b8\u1795\u17d2\u179f\u17b6\u179a \u1787\u17bd\u1799\u1795\u17d2\u1791\u17b6\u179b\u17cb\n\n"
                    "\u179f\u17b6\u1784\u179f\u1784\u17cb\u1796\u17b8\u1797\u17b6\u1796\u1787\u17b6\u1780\u17cb\u179f\u17d2\u178a\u17c2\u1784\u1793\u17c3\u1791\u17b8\u1795\u17d2\u179f\u17b6\u179a\u1793\u17c1\u17c7 \u2014 \u1798\u17b7\u1793\u1798\u17c2\u1793 copy \u1796\u17b8\u1780\u1793\u17d2\u179b\u17c2\u1784\u1795\u17d2\u179f\u17c1\u1784\u17d4"
                ),
            },
            "q_save": {
                "label": "\U0001f4b0 \u1781\u17d2\u1789\u17bb\u17c6\u1793\u17b9\u1784\u179f\u1793\u17d2\u179f\u17c6\u1794\u17b6\u1793\u17a2\u17d2\u179c\u17b8?",
                "answer": (
                    "\U0001f4b0 *\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u1793\u17c1\u17c7\u1787\u17bd\u1799\u1781\u17d2\u1789\u17bb\u17c6\u179f\u1793\u17d2\u179f\u17c6\u1794\u17b6\u1793\u17a2\u17d2\u179c\u17b8?*\n\n"
                    "\u17a2\u17d2\u179c\u17b8\u178a\u17c2\u179b\u1794\u1784\u179f\u1793\u17d2\u179f\u17c6\u1794\u17b6\u1793\u1785\u17d2\u179a\u17be\u1793\u1794\u17c6\u1795\u17bb\u178f \u2014 \u1798\u17b7\u1793\u1798\u17c2\u1793\u179b\u17bb\u1799\u17d4 \u1796\u17c1\u179b\u179c\u17c1\u179b\u17b6\u17d4\n\n"
                    "\u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784\u1787\u17b6\u1798\u1792\u17d2\u1799\u1798\u1798\u17b6\u1793 3 \u1798\u17c9\u17c4\u1784/\u1790\u17d2\u1784\u17c3 \u1785\u17c6\u178e\u17b6\u1799\u179b\u17be\u1780\u17b6\u179a\u1784\u17b6\u179a\u178a\u178a\u17c2\u179b\u17d7:\n"
                    "\u179f\u179a\u179f\u17c1\u179a caption \u1786\u17d2\u179b\u17be\u1799\u179f\u17b6\u179a \u1794\u17d2\u179a\u1780\u17b6\u179f \u17d4\n\n"
                    "*3 \u1798\u17c9\u17c4\u1784 \xd7 30 \u1790\u17d2\u1784\u17c3 = 90 \u1798\u17c9\u17c4\u1784/\u1781\u17c2* \u2014 Cambodia Biz Agent \u1792\u17d2\u179c\u17be\u1787\u17c6\u1793\u17bd\u179f\u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1785\u17c6\u1796\u17c4\u17c7 cost:\n\n"
                    "\U0001f50d \u179f\u17d2\u179a\u17b6\u179c\u1787\u17d2\u179a\u17b6\u179c: $100\u2013200/\u178a\u1784\n"
                    "\U0001f4e3 Content: $50\u2013150/\u1781\u17c2\n"
                    "\U0001f4ac Inbox: $200\u2013300/\u1781\u17c2\n"
                    "\U0001f4e6 \u178a\u17c4\u17c7\u179f\u17d2\u179a\u17b6\u1799\u1780\u17b6\u179a\u1794\u1789\u17d2\u1787\u17b6\u1791\u17b7\u1789: $150\u2013250/\u1781\u17c2\n"
                    "\U0001f4ca \u179a\u1794\u17b6\u1799\u1780\u17b6\u179a\u178e\u17cd: $100\u2013200/\u1781\u17c2\n\n"
                    "*\u1787\u17bd\u179b\u1798\u1793\u17bb\u179f\u17d2\u179f: ~$700\u20131,200/\u1781\u17c2*\n\n"
                    "Cambodia Biz Agent: \u1798\u17d2\u178a\u1784\u1794\u17c9\u17bb\u178e\u17d2\u178e\u17c4\u17c7 \U0001f7e6$97 \xb7 \u2b50$297 \xb7 \U0001f7e1$597\n\n"
                    "\u1786\u17d2\u1793\u17b6\u17c6\u178a\u17c6\u1794\u17bc\u1784 \u179f\u1793\u17d2\u179f\u17c6 *$8,000\u201314,000* \U0001f4b0"
                ),
            },
            "q_location": {
                "label": "\U0001f3e2 \u1780\u17b6\u179a\u17b7\u1799\u17b6\u179b\u17d0\u1799 NiMo \u1793\u17c5\u1791\u17b8\u178e\u17b6?",
                "answer": (
                    "\U0001f3e2 *\u1780\u17b6\u179a\u17b7\u1799\u17b6\u179b\u17d0\u1799 NiMo \u1793\u17c5\u1791\u17b8\u178e\u17b6?*\n\n"
                    "NiMo \u178a\u17c6\u178e\u17be\u179a\u1780\u17b6\u179a online \u1791\u17b6\u17c6\u1784\u179f\u17d2\u179a\u17bb\u1784 \u2014 \u1782\u17d2\u1798\u17b6\u1793\u1780\u17b6\u179a\u17b7\u1799\u17b6\u179b\u17d0\u1799 physical \u17d4 "
                    "\u178a\u17bc\u1785\u1796\u17c1\u179b\u1794\u1784\u1791\u17b7\u1789 app \u17ac course online \u2014 "
                    "\u1782\u17d2\u1798\u17b6\u1793\u1780\u17b6\u179a\u17b7\u1799\u17b6\u179b\u17d0\u1799 \u1780\u17cf\u1794\u17d2\u179a\u17be\u1794\u17b6\u1793\u1792\u1798\u17d2\u1798\u178f\u17b6\u17d4\n\n"
                    "\u17a2\u17d2\u179c\u17b8\u179f\u17c6\u1781\u17b6\u1793\u17cb: NiMo \u1792\u17b6\u1793\u17b6 *30 \u1790\u17d2\u1784\u17c3 \u1794\u1784\u17d2\u179c\u17b7\u179b\u179b\u17bb\u1799 100%* "
                    "\u1794\u17d2\u179a\u179f\u17b7\u1793\u1794\u17be\u1794\u1784\u1798\u17b7\u1793\u1796\u17c1\u1789\u1785\u17b7\u178f\u17d2\u178f\u17d4 \u2764\ufe0f"
                ),
            },
            "q_price": {
                "label": "\U0001f4b5 Cambodia Biz Agent \u178f\u1798\u17d2\u179b\u17c3\u1794\u17c9\u17bb\u1793\u17d2\u1798\u17b6\u1793?",
                "answer": (
                    "\U0001f4b5 *Cambodia Biz Agent \u178f\u1798\u17d2\u179b\u17c3\u1794\u17c9\u17bb\u1793\u17d2\u1798\u17b6\u1793? \u1798\u17b6\u1793\u1790\u17d2\u179b\u17c3/\u1781\u17c2?*\n\n"
                    "\u1791\u17b7\u1789\u1798\u17d2\u178a\u1784 \u2014 \u1794\u17d2\u179a\u17be\u1787\u17b6\u179a\u17c0\u1784\u179a\u17a0\u17bc\u178f\u17d4 \u1798\u17b6\u1793 3 \u1780\u1789\u17d2\u1785\u1794\u17cb:\n\n"
                    "\U0001f7e6 *Basic $97* (\u2248 400,000 Riel)\n"
                    "\u179f\u17b6\u1780\u179b\u17d2\u1794\u1784 \u2014 \u17a0\u17b6\u1793\u17b7\u1797\u17d0\u1799\u178f\u17b7\u1785\u1794\u17c6\u1795\u17bb\u178f\n\n"
                    "\u2b50 *Pro $297* (\u2248 1,200,000 Riel)\n"
                    "\u179f\u17d2\u179c\u17d0\u1799\u1794\u17d2\u179a\u179c\u178f\u17d2\u178f\u17b7 24/7\n\n"
                    "\U0001f7e1 *VIP $597* (\u2248 2,400,000 Riel)\n"
                    "NiMo \u178a\u17c6\u17a1\u17be\u1784\u1787\u17b6\u1798\u17bd\u1799\u1794\u1784 Zoom \u2014 \u1785\u1794\u17cb\u1794\u17d2\u179a\u17be\u1797\u17d2\u179b\u17b6\u1798\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1790\u17d2\u179b\u17c3\u1794\u17d2\u179a\u1785\u17b6\u17c6\u1781\u17c2\u178f\u17c2\u1798\u17bd\u1799: Claude Pro ~$20.\n\n"
                    "*\u1782\u17d2\u1798\u17b6\u1793\u1790\u17d2\u179b\u17c3\u179b\u17b6\u1780\u17cb\u179f\u17d2\u1784\u17b6\u178f\u17cb \u1782\u17d2\u1798\u17b6\u1793\u1780\u17b6\u179a renew \u17d4*"
                ),
            },
            "q_which_plan": {
                "label": "\U0001f914 \u1781\u17d2\u1789\u17bb\u17c6\u1798\u17b7\u1793\u178a\u17b9\u1784\u1790\u17b6\u1780\u1789\u17d2\u1785\u1794\u17cb\u178e\u17b6\u179f\u17b6\u1780\u179f\u1798",
                "answer": (
                    "\U0001f914 *\u1780\u1789\u17d2\u1785\u1794\u17cb\u178e\u17b6\u179f\u17b6\u1780\u179f\u1798\u1787\u17b6\u1798\u17bd\u1799\u17a0\u17b6\u1784\u179a\u1794\u179f\u17cb\u1794\u1784?*\n\n"
                    "\U0001f7e6 *Basic $97* \u2014 \u1791\u17be\u1794\u179f\u17d2\u1782\u17b6\u179b\u17cb AI \u1785\u1784\u17cb\u179f\u17b6\u1780\u179b\u17d2\u1794\u1784\u1798\u17bb\u1793\n"
                    "\u2192 \u1794\u17bb\u1782\u17d2\u1782\u179b\u17b7\u1780 AI 5 \u1793\u17b6\u1780\u17cb + \u1780\u17b6\u179a\u178e\u17c2\u1793\u17b6\u17c6\u1787\u17b6\u1797\u17b6\u179f\u17b6\u1781\u17d2\u1798\u17c2\u179a + \u1780\u17b6\u179a\u1782\u17b6\u17c6\u1791\u17d2\u179a 30 \u1790\u17d2\u1784\u17c3\n\n"
                    "\u2b50 *Pro $297* \u2014 \u17a0\u17b6\u1784\u178a\u17c6\u178e\u17be\u179a\u1780\u17b6\u179a \u1785\u1784\u17cb\u179f\u17d2\u179c\u17d0\u1799\u1794\u17d2\u179a\u179c\u178f\u17d2\u178f\u17b7 24/7\n"
                    "\u2192 Chatbot \u1786\u17d2\u179b\u17be\u1799 + \u1794\u17d2\u179a\u1780\u17b6\u179f\u178a\u17c4\u1799\u179f\u17d2\u179c\u17d0\u1799\u1794\u17d2\u179a\u179c\u178f\u17d2\u178f\u17b7 + \u1791\u1791\u17bd\u179b booking\n\n"
                    "\U0001f7e1 *VIP $597* \u2014 \u1798\u17b7\u1793\u1785\u1784\u17cb\u178a\u17c6\u17a1\u17be\u1784\u1781\u17d2\u179b\u17bd\u1793\u17af\u1784 NiMo \u1792\u17d2\u179c\u17be\u1787\u17c6\u1793\u17bd\u179f\n"
                    "\u2192 \u178a\u17c6\u17a1\u17be\u1784\u179a\u17bd\u1785 \u1794\u17d2\u179a\u17be\u1794\u17b6\u1793\u1797\u17d2\u179b\u17b6\u1798 \u1780\u17b6\u179a\u1782\u17b6\u17c6\u1791\u17d2\u179a 90 \u1790\u17d2\u1784\u17c3\n\n"
                    "\u1798\u17b7\u1793\u1794\u17d2\u179a\u17b6\u1780\u178a? \u1794\u17d2\u179a\u17b6\u1794\u17cb NiMo \u17a2\u17c6\u1796\u17b8\u17a0\u17b6\u1784\u179a\u1794\u179f\u17cb\u1794\u1784 \u2014 \u1799\u17be\u1784\u178e\u17c2\u1793\u17b6\u17c6\u1780\u1789\u17d2\u1785\u1794\u17cb\u178f\u17d2\u179a\u17b9\u1798\u178f\u17d2\u179a\u17bc\u179c \U0001f447"
                ),
            },
            "q_worth": {
                "label": "\U0001f48e $297 \u1798\u17b6\u1793\u178f\u1798\u17d2\u179b\u17c3\u1785\u17c6\u178e\u17b6\u1799\u1791\u17c1?",
                "answer": (
                    "\U0001f48e *$297 \u1798\u17b6\u1793\u178f\u1798\u17d2\u179b\u17c3\u1785\u17c6\u178e\u17b6\u1799\u1791\u17c1?*\n\n"
                    "\u1785\u17bc\u179a\u17b1\u17d2\u1799\u179b\u17c1\u1781\u178f\u1794\u178f\u17c2\u17d4\n\n"
                    "*\u1794\u17bb\u1782\u17d2\u1782\u179b\u17b7\u1780 inbox \u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6:* $200\u2013300/\u1781\u17c2\n"
                    "\u2192 8 \u1798\u17c9\u17c4\u1784/\u1790\u17d2\u1784\u17c3\u17d4 \u1788\u1794\u17cb\u1788\u179a\u17d4 \u1788\u17ba = \u1794\u1793\u17d2\u1790\u1799 productivity \u17d4\n\n"
                    "*Cambodia Biz Agent Pro $297* \u2014 \u1798\u17d2\u178a\u1784\u1794\u17c9\u17bb\u178e\u17d2\u178e\u17c4\u17c7\n"
                    "\u2192 24/7 \u17d4 \u1798\u17b7\u1793\u1788\u1794\u17cb \u17d4 \u1798\u17b7\u1793\u179f\u17bb\u17c6\u17a1\u17be\u1784\u1794\u17d2\u179a\u17b6\u1780\u17cb \u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "$297 = \u1790\u17d2\u179b\u17c3 inbox \u1780\u17d2\u179a\u17c4\u1798\u1798\u17bd\u1799\u1781\u17c2 \u17d4\n"
                    "\u1794\u17c9\u17bb\u1793\u17d2\u178f\u17c2 Cambodia Biz Agent \u1792\u17d2\u179c\u17be*\u1787\u17b6\u179a\u17c0\u1784\u179a\u17a0\u17bc\u178f* \u17d4\n\n"
                    "\u1794\u17d2\u179a\u179f\u17b7\u1793\u1794\u17be AI \u1787\u17bd\u1799\u1794\u1784\u1794\u17b7\u1791 5 \u1780\u17b6\u179a\u1794\u1789\u17d2\u1787\u17b6\u1791\u17b7\u1789/\u1781\u17c2 \u2014 $297  \u179a/\u17a0\u17be\u1799 \u17d4"
                ),
            },
            "q_warranty": {
                "label": "\U0001f6e1\ufe0f \u1795\u179b\u17b7\u178f\u1795\u179b\u1798\u17b6\u1793\u1780\u17b6\u179a\u1792\u17b6\u1793\u17b6\u179a\u17c9\u17b6\u1794\u17cb\u179a\u1784?",
                "answer": (
                    "\U0001f6e1\ufe0f *\u1795\u179b\u17b7\u178f\u1795\u179b\u1798\u17b6\u1793\u1780\u17b6\u179a\u1792\u17b6\u1793\u17b6? \u17a2\u17b6\u1785\u1794\u1784\u17d2\u179c\u17b7\u179b\u179b\u17bb\u1799?*\n\n"
                    "\u1798\u17b6\u1793\u1787\u17b6\u1780\u17b6\u179a\u1794\u17d2\u179a\u17b6\u1780\u178a \u17d4 NiMo \u1791\u17c6\u1793\u17bb\u1780\u1785\u17b7\u178f\u17d2\u178f \u17d4\n\n"
                    "*\u1792\u17b6\u1793\u17b6 30 \u1790\u17d2\u1784\u17c3 \u2014 \u1794\u1784\u17d2\u179c\u17b7\u179b\u179b\u17bb\u1799 100% \u178a\u17c4\u1799/\u17a0\u17c1\u178f\u17bb\u1795\u179b \u17d4*\n\n"
                    "\u1791\u17b7\u1789 \u17d4 \u1792\u17d2\u179c\u17be\u178f\u17b6\u1798\u1780\u17b6\u179a\u178e\u17c2\u1793\u17b6\u17c6 30 \u1790\u17d2\u1784\u17c3 \u17d4 "
                    "\u1794\u17d2\u179a\u179f\u17b7\u1793\u1794\u17be/\u178a\u17c6\u178e\u17be\u179a\u1780\u17b6\u179a/\u1796\u17b7\u1796\u178e\u17cc\u1793\u17b6 \u2014 \u1795\u17d2\u1789\u17be NiMo Telegram \u17d4 "
                    "\u1794\u1784\u17d2\u179c\u17b7\u179b\u1780\u17d2\u1793\u17bb\u1784 24 \u1798\u17c9\u17c4\u1784 \u17d4\n\n"
                    "*\u17a0\u17b6\u1793\u17b7\u1797\u17d0\u1799: NiMo \u17d4 \u1798\u17b7\u1793/\u1794\u1784 \u17d4* \u2764\ufe0f"
                ),
            },
            "q_tech": {
                "label": "\U0001f630 \u1781\u17d2\u1789\u17bb\u17c6\u1781\u17d2\u179b\u17b6\u1785\u178a\u17c6\u17a1\u17be\u1784\u1798\u17b7\u1793\u1794\u17b6\u1793",
                "answer": (
                    "\U0001f630 *\u1798\u17b7\u1793\u1785\u17c1\u17c7\u1794\u1785\u17d2\u1785\u17c1\u1780\u179c\u17b7\u1791\u17d2\u1799\u17b6 \u2014 \u17a2\u17b6\u1785\u178a\u17c6\u17a1\u17be\u1784\u1794\u17b6\u1793\u1791\u17c1?*\n\n"
                    "\u1794\u17b6\u1793! \u1793\u17c1\u17c7\u1787\u17b6\u17a0\u17c1\u178f\u17bb\u1795\u179b:\n\n"
                    "\u2705 \u1780\u17b6\u179a\u178e\u17c2\u1793\u17b6\u17c6\u1787\u17b6\u1797\u17b6\u179f\u17b6\u1781\u17d2\u1798\u17c2\u179a \u1798\u17b6\u1793\u179a\u17bc\u1794\u1797\u17b6\u1796\u1794\u1784\u17d2\u17a0\u17b6\u1789\u1787\u17b6\u1787\u17c6\u17a0\u17b6\u1793\u17d7\n"
                    "\u2705 \u1798\u17b6\u1793\u179c\u17b8\u178a\u17c1\u17a2\u17bc\u1798\u17be\u179b\u178f\u17b6\u1798\n"
                    "\u2705 \u1794\u17d2\u179a\u17be Bot \u1787\u17bd\u1799 24/7\n"
                    "\u2705 NiMo \u1795\u17d2\u1791\u17b6\u179b\u17cb\u1786\u17d2\u179b\u17be\u1799\u1796\u17c1\u179b\u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a\n\n"
                    "\u1780\u1789\u17d2\u1785\u1794\u17cb VIP: NiMo \u17a2\u1784\u17d2\u1782\u17bb\u1799\u178a\u17c6\u17a1\u17be\u1784\u1787\u17b6\u1798\u17bd\u1799\u1794\u1784\u178f\u17b6\u1798 Zoom 2 \u1798\u17c9\u17c4\u1784 \u2014 "
                    "\u1794\u1784\u1782\u17d2\u179a\u17b6\u1793\u17cb\u178f\u17c2\u1798\u17be\u179b \u17a0\u17be\u1799\u1785\u17bb\u1785\u178f\u17b6\u1798\u17d4 \U0001f3af"
                ),
            },
            "q_time": {
                "label": "\u23f0 \u1785\u17c6\u178e\u17b6\u1799\u1796\u17c1\u179b\u1794\u17c9\u17bb\u1793\u17d2\u1798\u17b6\u1793\u178a\u17be\u1798\u17d2\u1794\u17b8\u1785\u17b6\u1794\u17cb\u1795\u17d2\u178a\u17be\u1798?",
                "answer": (
                    "\u23f0 *\u1785\u17c6\u178e\u17b6\u1799\u1796\u17c1\u179b\u1794\u17c9\u17bb\u1793\u17d2\u1798\u17b6\u1793\u178a\u17be\u1798\u17d2\u1794\u17b8\u1785\u17b6\u1794\u17cb\u1794\u17d2\u179a\u17be?*\n\n"
                    "*Basic & Pro:* \u178a\u17c6\u17a1\u17be\u1784\u178f\u17b6\u1798\u1780\u17b6\u179a\u178e\u17c2\u1793\u17b6\u17c6 ~2\u20133 \u1798\u17c9\u17c4\u1784 \u2014 "
                    "\u1792\u17d2\u179c\u17be\u1796\u17c1\u179b\u179b\u17d2\u1784\u17b6\u1785 \u17d4 \u1790\u17d2\u1784\u17c3 2 \u1798\u17b6\u1793 content \u17d4 \u1790\u17d2\u1784\u17c3 3 \u178a\u17c6\u178e\u17be\u179a\u1780\u17b6\u179a \u17d4\n\n"
                    "*VIP:* Zoom 2 \u1798\u17c9\u17c4\u1784\u1787\u17b6\u1798\u17bd\u1799 NiMo \u2014 "
                    "NiMo \u1792\u17d2\u179c\u17be test \u1785\u1794\u17cb\u1794\u17d2\u179a\u1782\u179b\u17cb \u17d4\n\n"
                    "\u1791\u17b7\u1789\u1796\u17c1\u179b\u1796\u17d2\u179a\u17b9\u1780 \u2014 \u179b\u17d2\u1784\u17b6\u1785\u1798\u17b6\u1793 content \u178a\u17c6\u1794\u17bc\u1784 \U0001f680"
                ),
            },
            "q_device": {
                "label": "\U0001f4f1 \u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a\u17a7\u1794\u1780\u179a\u178e\u17cd\u17a2\u17d2\u179c\u17b8?",
                "answer": (
                    "\U0001f4f1 *\u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a\u17a7\u1794\u1780\u179a\u178e\u17cd\u17a2\u17d2\u179c\u17b8?*\n\n"
                    "Computer \u17ac smartphone \u1780\u17cf\u1794\u17d2\u179a\u17be\u1794\u17b6\u1793 \U0001f60a\n\n"
                    "\U0001f4bb *Computer:* NiMo \u178e\u17c2\u1793\u17b6\u17c6 \u178a\u17c6\u17a1\u17be\u1784\u178a\u17c6\u1794\u17bc\u1784 + \u1798\u17be\u179b\u179a\u1794\u17b6\u1799\u1780\u17b6\u179a\u178e\u17cd\n\n"
                    "\U0001f4f1 *Smartphone:* \u1794\u17d2\u179a\u178f\u17b7\u1794\u178f\u17d2\u178f\u17b7\u1780\u17b6\u179a\u1794\u17d2\u179a\u1785\u17b6\u17c6\u1790\u17d2\u1784\u17c3 \u1786\u17d2\u179b\u17be\u1799 post report\n\n"
                    "Computer \u178e\u17b6\u178a\u17c2\u179b scroll Facebook \u179f\u17d2\u179a\u17bd\u179b \u2014 \u1794\u17d2\u179a\u17be Cambodia Biz Agent \u1794\u17b6\u1793 \u17d4 "
                    "\u1782\u17d2\u1798\u17b6\u1793\u1780\u17b6\u179a upgrade \u17d4"
                ),
            },
            "q_internet": {
                "label": "\U0001f310 \u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a internet \u179b\u17bf\u1793?",
                "answer": (
                    "\U0001f310 *\u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a internet \u179b\u17d2\u1794\u17bf\u1793\u1781\u17d2\u1796\u179f\u17cb?*\n\n"
                    "\u1798\u17b7\u1793\u1791\u17b6\u1798\u1791\u17b6\u179a \u17d4 Internet \u1794\u17d2\u179a\u17be Facebook + Telegram \u1792\u1798\u17d2\u1798\u178f\u17b6 \u2014 \u1794\u17d2\u179a\u17be Agent \u1794\u17b6\u1793 \u17d4\n\n"
                    "WiFi \u1795\u17d2\u1791\u17c7 \u17ac 4G \u1780\u17cf OK \u17d4 \u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792 run cloud \u2014 "
                    "phone/computer \u1782\u17d2\u179a\u17b6\u1793\u17cb\u178f\u17c2 \u1795\u17d2\u1789\u17be command \U0001f680"
                ),
            },
            "q_team": {
                "label": "\U0001f465 \u1794\u17bb\u1782\u17d2\u1782\u179b\u17b7\u1780\u17a2\u17b6\u1785\u1794\u17d2\u179a\u17be\u179a\u17bd\u1798\u1782\u17d2\u1793\u17b6?",
                "answer": (
                    "\U0001f465 *\u1794\u17bb\u1782\u17d2\u1782\u179b\u17b7\u1780\u17a0\u17b6\u1784\u17a2\u17b6\u1785\u1794\u17d2\u179a\u17be\u179a\u17bd\u1798?*\n\n"
                    "\u1794\u17b6\u1793\u1787\u17b6\u1780\u17b6\u179a\u1794\u17d2\u179a\u17b6\u1780\u178a! NiMo \u179a\u1785\u1793\u17b6 Cambodia Biz Agent \u17b1\u17d2\u1799\u1794\u17d2\u179a\u17be team \u1791\u17b6\u17c6\u1784\u1798\u17bc\u179b \U0001f60a\n\n"
                    "\u2705 Inbox staff \u1794\u17d2\u179a\u17be AI \u1786\u17d2\u179b\u17be\u1799\u17a2\u178f\u17b7\u1790\u17b7\u1787\u1793\n"
                    "\u2705 Content staff \u1794\u17d2\u179a\u17be AI \u1794\u1784\u17d2\u1780\u17be\u178f\u1780\u17b6\u179a\u1794\u17d2\u179a\u1780\u17b6\u179f\n"
                    "\u2705 Manager \u1794\u17d2\u179a\u17be AI \u1798\u17be\u179b\u1785\u17c6\u178e\u17bc\u179b\n\n"
                    "Access account \u178f\u17c2\u1798\u17bd\u1799 \u2014 collaborate \u1784\u17b6\u1799 \u17d4\n\n"
                    "\U0001f4a1 Claude Pro $20/\u1781\u17c2 share team \u1791\u17b6\u17c6\u1784\u17a2\u179f\u17cb \u2014 "
                    "\u1782\u17d2\u1798\u17b6\u1793\u1780\u17b6\u179a\u1791\u17b7\u1789 account \u178a\u17b6\u1785\u17cb \u17d4"
                ),
            },
            "q_data": {
                "label": "\U0001f512 \u1791\u17b7\u1793\u17d2\u1793\u1793\u17d0\u1799\u17a0\u17b6\u1784\u1787\u17d2\u179a\u17b6\u1794\u1785\u17c1\u1789?",
                "answer": (
                    "\U0001f512 *\u1791\u17b7\u1793\u17d2\u1793\u1793\u17d0\u1799\u17a0\u17b6\u1784 \u1787\u17d2\u179a\u17b6\u1794\u1785\u17c1\u1789?*\n\n"
                    "NiMo \u1792\u17b6\u1793\u17b6: \u1791\u17b7\u1793\u17d2\u1793\u1793\u17d0\u1799\u179a\u1794\u179f\u17cb\u1794\u1784\u1798\u17b6\u1793\u179f\u17bb\u179c\u178f\u17d2\u1790\u17b7\u1797\u17b6\u1796 \u17d4\n\n"
                    "\u2705 \u1791\u17b7\u1793\u17d2\u1793\u1793\u17d0\u1799\u1787\u17b6\u179a\u1794\u179f\u17cb\u1794\u1784 \u2014 store \u1780\u17d2\u1793\u17bb\u1784 account \u1795\u17d2\u1791\u17b6\u179b\u17cb \u17d4\n\n"
                    "\u2705 NiMo \u1798\u17b7\u1793 collect/sell/share \u1791\u17b7\u1793\u17d2\u1793\u1793\u17d0\u1799 \u17d4\n\n"
                    "\u2705 Security \u179f\u17d2\u178a\u1784\u17cb\u178a\u17b6\u179a Anthropic (US) \u2014 "
                    "\u178a\u17bc\u1785 bank \u1792\u17c6 \u17d4\n\n"
                    "\u17a0\u17b6\u1784\u1787\u17b6\u179a\u1794\u179f\u17cb\u1794\u1784 \u2192 \u1791\u17b7\u1793\u17d2\u1793\u1793\u17d0\u1799\u1787\u17b6\u179a\u1794\u179f\u17cb\u1794\u1784 \u2192 NiMo \u1798\u17b7\u1793\u1791\u17bb\u1780\u17a2\u17d2\u179c\u17b8 \u2764\ufe0f"
                ),
            },
            "q_after_warranty": {
                "label": "\U0001f91d \u1795\u17bb\u178f\u1780\u17b6\u179a\u1792\u17b6\u1793\u17b6 NiMo \u1787\u17bd\u1799?",
                "answer": (
                    "\U0001f91d *\u1795\u17bb\u178f 30 \u1790\u17d2\u1784\u17c3 NiMo \u1787\u17bd\u1799?*\n\n"
                    "\u1780\u17b6\u179a\u1792\u17b6\u1793\u17b6 = policy \u1794\u1784\u17d2\u179c\u17b7\u179b\u179b\u17bb\u1799 \u2014 \u1787\u17c6\u1793\u17bd\u1799 NiMo \u1782\u17d2\u1798\u17b6\u1793\u1780\u17b6\u179a\u1780\u17c6\u178e\u178f\u17cb \U0001f60a\n\n"
                    "\u2705 Telegram NiMo \u1793\u17c5\u1796\u17c1\u179b\u178e\u17b6 \u2014 \u1787\u17bd\u1799 \u17d4\n\n"
                    "\u2705 Community group \u2014 \u179a\u17c0\u1793\u1796\u17b8\u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784\u1795\u17d2\u179f\u17c1\u1784 \u17d4\n\n"
                    "\u2705 Update \u1790\u17d2\u1798\u17b8 \u2014 \u17a5\u178f\u1782\u17b7\u178f\u1790\u17d2\u179b\u17c3 \u17d4\n\n"
                    "NiMo \u1798\u17b7\u1793 abandon \u17d4 \u2764\ufe0f"
                ),
            },
            "q_update": {
                "label": "\U0001f199 \u1798\u17b6\u1793\u1780\u17b6\u179a update?",
                "answer": (
                    "\U0001f199 *\u1798\u17b6\u1793 update/upgrade \u1790\u17d2\u1784\u17c3\u1780\u17d2\u179a\u17c4\u1799? \u1790\u17d2\u179b\u17c3?*\n\n"
                    "Update \u1787\u17b6\u1793\u17b7\u1785\u17d2\u1785 \u2014 \u17a5\u178f\u1782\u17b7\u178f\u1790\u17d2\u179b\u17c3 \U0001f381\n\n"
                    "NiMo upgrade \u1795\u17d2 \u17a2\u17b6\u179f\u17cb feedback \u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784 \u17d4 \u1796\u17c1\u179b\u1798\u17b6\u1793:\n\n"
                    "\u2705 Feature \u1790\u17d2\u1798\u17b8\n"
                    "\u2705 AI command \u1794\u17d2\u179a\u179f\u17be\u179a\n"
                    "\u2705 Speed + effectiveness\n\n"
                    "\u2192 \u1791\u1791\u17bd\u179b update \u178a\u17c4\u1799 group \u2014 \u178a\u17c4\u1799 pay \u1790\u17d2\u1798\u17b8 \u17d4\n\n"
                    "\u1791\u17b7\u1789\u1798\u17d2\u178a\u1784 \u2014 upgrade \u1787\u17b6\u179a\u17c0\u1784\u179a\u17a0\u17bc\u178f \u17d4"
                ),
            },
            "q_community": {
                "label": "\U0001f465 NiMo \u1798\u17b6\u1793 community group?",
                "answer": (
                    "\U0001f465 *NiMo \u1798\u17b6\u1793 community group?*\n\n"
                    "\u1798\u17b6\u1793\u1787\u17b6\u1780\u17b6\u179a\u1794\u17d2\u179a\u17b6\u1780\u178a \U0001f49b\n\n"
                    "\u1780\u17d2\u179a\u17c4\u1799\u1791\u17b7\u1789 NiMo add \u1785\u17bc\u179b *Telegram community* \u17d4 \u1791\u17b8\u1793\u17c4\u17c7:\n\n"
                    "\u2705 \u1787\u17bd\u1794\u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784\u1781\u17d2\u1798\u17c2\u179a \u2014 \u1785\u17c2\u1780\u179a\u17c6\u179b\u17c2\u1780\u1794\u1791\u1796\u17b7\u179f\u17c4\u1792 \u17d4\n\n"
                    "\u2705 \u179a\u17c0\u1793 AI \u1794\u17d2\u179a\u1780\u1794\u178a\u17c4\u1799\u1794\u17d2\u179a\u179f\u17b7\u1791\u17d2\u1792 \u17d4\n\n"
                    "\u2705 Tips + AI command \u1790\u17d2\u1798\u17b8\u1794\u17d2\u179a\u1785\u17b6\u17c6\u179f\u1794\u17d2\u178a\u17b6\u17a0\u17cd \u17d4\n\n"
                    "\u2705 \u1787\u17c6\u1793\u17bd\u1799 NiMo + community \u17d4\n\n"
                    "\u1794\u1784\u1798\u17b7\u1793\u178a\u17c2\u179b\u1791\u17c5\u1798\u17d2\u1793\u17b6\u1780\u17cb \u2764\ufe0f"
                ),
            },
            "q_competitor": {
                "label": "\u2694\ufe0f \u1782\u17bc\u1794\u17d2\u179a\u1787\u17c2\u1784\u1794\u17d2\u179a\u17be Agent \u1795\u1784?",
                "answer": (
                    "\u2694\ufe0f *\u1782\u17bc\u1794\u17d2\u179a\u1787\u17c2\u1784\u1794\u17d2\u179a\u17be \u2014 \u1781\u17d2\u1789\u17bb\u17c6\u1793\u17c5 advantage?*\n\n"
                    "\u1785\u17c6\u179b\u17be\u1799: advantage \u1793\u17c5 \u2014 \u17a0\u17be\u1799\u1792\u17c6\u1787\u17b6\u1784 \u1794\u17d2\u179a\u179f\u17b7\u1793\u1794\u17be\u1785\u17b6\u1794\u17cb\u1795\u17d2\u178a\u17be\u1798\u1798\u17bb\u1793 \u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*\u1798\u17d2\u1785\u17b6\u179f\u17cb\u17a0\u17b6\u1784\u1797\u17b6\u1782\u1785\u17d2\u179a\u17be\u1793\u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6 \u1798\u17b7\u1793\u1791\u17b6\u1793\u17cb\u1794\u17d2\u179a\u17be AI \u17d4*\n"
                    "\u179a\u17c0\u1784\u179a\u17b6\u179b\u17cb\u1790\u17d2\u1784\u17c3 wait = \u1790\u17d2\u1784\u17c3 competitor \u1791\u17c5 \u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*\u1794\u17d2\u179a\u17be tool \u178a\u17bc\u1785\u1782\u17d2\u1793\u17b6 \u2260 result \u178a\u17bc\u1785\u1782\u17d2\u1793\u17b6 \u17d4*\n\n"
                    "\u17a0\u17b6\u1784 2 \u1794\u17d2\u179a\u17be tool \u178a\u17bc\u1785 \u2014 \u1794\u17c9\u17bb\u1793\u17d2\u178f\u17c2:\n"
                    "\u2022 \u1795\u179b\u17b7\u178f\u1795\u179b \u2260\n"
                    "\u2022 Brand style \u2260\n"
                    "\u2022 Customer approach \u2260\n\n"
                    "AI \u179a\u17c0\u1793\u178f\u17b6\u1798 \u17a0\u17b6\u1784\u1794\u1784 \u2014 \u1782\u17d2\u1798\u17b6\u1793 copy \u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Advantage = \u1794\u17d2\u179a\u17be *\u179b\u17bf\u1793 \u1794\u17d2\u179a\u179f\u17be\u179a \u179f\u17d2\u1790\u17b7\u178f\u1790\u17c1\u179a* \u1787\u17b6\u1784 \u17d4"
                ),
            },
            "q_think": {
                "label": "\U0001f914 \u179f\u17bc\u1798\u1791\u17bb\u17d2\u1799\u1785\u17b7\u178f\u17d2\u178f\u1794\u1793\u17d2\u1790\u17c2\u1798",
                "answer": (
                    "\U0001f914 *\u179f\u17bc\u1798\u1791\u17bb\u17d2\u1799\u1785\u17b7\u178f\u17d2\u178f\u1794\u1793\u17d2\u1790\u17c2\u1798*\n\n"
                    "\u1785\u17c6\u1796\u17c4\u17c7 \u2014 \u1780\u17b6\u179a \u2460\u1785\u17c6\u178e \u2461\u1785\u17c6\u178e \u2462 \u2462 \U0001f60a\n\n"
                    "\u1794\u17c9\u17bb\u1793\u17d2\u178f\u17c2 NiMo \u1785\u1784\u17cb\u17b1\u17d2\u1799\u1794\u1784\u178a\u17b9\u1784 3 \u1785\u17c6\u178e\u17bb\u1785:\n\n"
                    "*\u1791\u17b8\u1798\u17bd\u1799 \u2014 \u178f\u1798\u17d2\u179b\u17c3 early bird \u17d4*\n"
                    "\u1780\u17d2\u179a\u17c4\u1799 launch \u17d4 \u17d4 \u17d4 \u178f\u1798\u17d2\u179b\u17c3 \u2191 \u17d4 \u1791\u17b7\u1789\u1790\u17d2\u1784\u17c3\u1793\u17c1\u17c7 = best price \u17d4\n\n"
                    "*\u1791\u17b8\u1796\u17b8\u179a \u2014 \u1792\u17b6\u1793\u17b6 30 \u1790\u17d2\u1784\u17c3 100% \u17d4*\n"
                    "= Try \u178a\u17c4\u1799 risk \u2248 0 \u17d4 \u1798\u17b7\u1793good \u2192 \u1794\u17d2\u179a\u17b6\u1780\u17cb back \u17d4\n\n"
                    "*\u1791\u17b8\u1794\u17b8 \u2014 \u179a\u17c0\u1784\u179a\u17b6\u179b\u17cb\u1790\u17d2\u1784\u17c3 wait = \u1790\u17d2\u1784\u17c3 lose \u17d4*\n"
                    "\u1796\u17c1\u179b order \u1794\u17b6\u178f\u17cb c\u01a1h\u1ed9i \u17d4 \u17d4 \u17d4 \u17d4 \u17d4 \u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1794\u1784\u178f\u17d2\u179a\u17bc\u179c info \u1794\u1793\u17d2\u1790\u17c2\u1798? NiMo \u1793\u17c5\u1791\u17b8\u1793\u17c1\u17c7 \U0001f60a"
                ),
            },
            "q_try": {
                "label": "\U0001f9ea \u1785\u1784\u17cb\u179f\u17b6\u1780\u179b\u17d2\u1794\u1784\u1798\u17bb\u1793\u1791\u17b7\u1789",
                "answer": (
                    "\U0001f9ea *\u1785\u1784\u17cb\u179f\u17b6\u1780\u179b\u17d2\u1794\u1784\u1798\u17bb\u1793\u1791\u17b7\u1789*\n\n"
                    "NiMo \u1799\u179b\u17cb \U0001f60a\n\n"
                    "\u1794\u17c9\u17bb\u1793\u17d2\u178f\u17c2: Try = result \u1796\u17b7\u178f\u1794\u17d2\u179a\u17b6\u1780\u178a \u1793\u17c5 \u17a0\u17b6\u1784 \u1796\u17b7\u178f\u1794\u17d2\u179a\u17b6\u1780\u178a \u17d4\n"
                    "*\u1798\u17b7\u1793 \u17a2\u17b6\u1785\u1792\u17d2\u179c\u17be \u178a\u17c4\u1799/\u1785\u17b6\u1794\u17cb '\u1796\u17b7\u178f\u1794\u17d2\u179a\u17b6\u1780\u178a \u17d4*\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u17a0\u17be\u1799 NiMo \u1798\u17b6\u1793 *Basic $97* = 'free trial with refund':\n\n"
                    "\u2705 5 AI Employees \u1796\u17c1\u1789\n"
                    "\u2705 Run \u17a0\u17b6\u1784\u1796\u17b7\u178f\u1794\u17d2\u179a\u17b6\u1780\u178a\n"
                    "\u2705 Result 30 \u1790\u17d2\u1784\u17c3\n"
                    "\u2705 \u2260good \u2192 100% back\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*Risk \u1796\u17b7\u178f = continue \u1798\u17d2\u1793\u17b6\u1780\u17cb \u2014 \u1781\u178e\u17c8/\u1785 way \u17d4*"
                ),
            },
            "q_claude_pro": {
                "label": "\U0001f4b3 Claude Pro $20/\u1781\u17c2 \u1787\u17b6\u17a2\u17d2\u179c\u17b8?",
                "answer": (
                    "\U0001f4b3 *Claude Pro $20/\u1781\u17c2 \u1787\u17b6\u17a2\u17d2\u179c\u17b8? \u178f\u1798\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a?*\n\n"
                    "Cambodia Biz Agent run \u179b\u17be Claude AI (Anthropic \u2014 US) \u17d4 "
                    "\u178a\u17be\u1798\u17d2\u1794\u17b8\u1794\u17d2\u179a\u17be \u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a Claude Pro *$20/\u1781\u17c2* \u2014 "
                    "\u1785\u17c6\u178e\u17b6\u1799 Anthropic \u1795\u17d2\u1791\u17b6\u179b\u17cb \u1798\u17b7\u1793 NiMo \u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "\u1794\u17c9\u17bb\u1793\u17d2\u178f\u17c2 cost \u1796\u17b7\u178f:\n\n"
                    "\u2705 $20/\u1781\u17c2 = 1 employee 24/7 \u17d4\n"
                    "\u2705 AI Agents \u1791\u17b6\u17c6\u1784 5 run account 1 \u17d4\n"
                    "\u2705 Cancel \u1796\u17c1\u179b\u178e\u17b6 \u17d4\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Inbox staff \u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6 = $200\u2013300/\u1781\u17c2 \u17d4\n"
                    "Claude Pro = $20/\u1781\u17c2 \u17d4 *Save $180\u2013280/\u1781\u17c2 \u17d4*"
                ),
            },
            "q_riel": {
                "label": "\U0001f4b5 \u17a2\u17b6\u1785\u1794\u1784\u17cb\u1787\u17b6\u179a\u17c0\u179b\u1794\u17b6\u1793?",
                "answer": (
                    "\U0001f4b5 *\u17a2\u17b6\u1785\u1794\u1784\u17cb\u1787\u17b6\u179a\u17c0\u179b?*\n\n"
                    "\u1794\u17b6\u1793\u1787\u17b6\u1780\u17b6\u179a\u1794\u17d2\u179a\u17b6\u1780\u178a! \u1795\u17d2\u1791\u17c1\u179a\u179a\u17c0\u179b\u1792\u1798\u17d2\u1798\u178f\u17b6 \u2014 "
                    "ABA convert USD \u179f\u17d2\u179c\u17d0\u1799\u1794\u17d2\u179a\u179c\u178f\u17d2\u178f\u17b7 \u17d4\n\n"
                    "\U0001f7e6 *Basic $97* \u2248 400,000 Riel\n"
                    "\u2b50 *Pro $297* \u2248 1,200,000 Riel\n"
                    "\U0001f7e1 *VIP $597* \u2248 2,400,000 Riel"
                ),
            },
            "q_industry": {
                "label": "\U0001f6cd\ufe0f \u17a0\u17b6\u1784\u1781\u17d2\u1789\u17bb\u17c6 \u2260 tech \u17a2\u17b6\u1785\u1794\u17d2\u179a\u17be?",
                "answer": (
                    "\U0001f6cd\ufe0f *\u17a0\u17b6\u1784\u1781\u17d2\u1789\u17bb\u17c6 [food/fashion/beauty]\u2026 \u1794\u17d2\u179a\u17be Agent \u1794\u17b6\u1793?*\n\n"
                    "NiMo \u1786\u17d2\u179b\u17be\u1799: *\u1794\u17d2\u179a\u179f\u17b7\u1793\u1794\u17be sell online \u1793\u17c5\u1780\u1798\u17d2\u1796\u17bb\u1787\u17b6 \u2014 \u1794\u17d2\u179a\u17be\u1794\u17b6\u1793 \u17d4*\n\n"
                    "NiMo tested:\n\n"
                    "\U0001f457 Fashion & accessories\n"
                    "\U0001f484 Beauty & skincare\n"
                    "\U0001f371 Food & specialty\n"
                    "\U0001f4da Courses & consulting\n"
                    "\U0001f486 Spa, salon, studio\n"
                    "\U0001f3e0 Furniture & home\n"
                    "\U0001f338 Flowers & gifts\n\n"
                    "AI \u179a\u17c0\u1793\u178f\u17b6\u1798 \u1795\u179b\u17b7\u178f\u1795\u179b + style \u17a0\u17b6\u1784 \u2014 \u1798\u17b7\u1793 apply formula rigid \u17d4\n\n"
                    "\u1798\u17b7\u1793\u1794\u17d2\u179a\u17b6\u1780\u178a? \u1794\u17d2\u179a\u17b6\u1794\u17cb niche NiMo \u2014 \u1796\u17b7\u1782\u17d2\u179a\u17c4\u17c7 free \U0001f447"
                ),
            },
            "q_delivery": {
                "label": "\U0001f4e6 \u1795\u17d2\u1791\u17c1\u179a\u200b\u1794\u17d2\u179a\u17b6\u1780\u17cb\u200b\u17a0\u17be\u1799\u200b \u1791\u1791\u17bd\u179b\u200b\u178a\u17bc\u1785\u200b\u1798\u17d2\u178a\u17c1\u1785?",
                "answer": (
                    "\U0001f4e6 *\u1780\u17d2\u179a\u17c4\u1799\u1795\u17d2\u1791\u17c1\u179a\u1794\u17d2\u179a\u17b6\u1780\u17cb \u1791\u1791\u17bd\u179b\u178a\u17bc\u1785\u1798\u17d2\u178a\u17c1\u1785?*\n\n"
                    "\u1784\u17b6\u1799 \u2014 4 \u1787\u17c6\u17a0\u17b6\u1793:\n\n"
                    "*\u1787\u17c6\u17a0\u17b6\u1793 1 \u2014 \u1795\u17d2\u1791\u17c1\u179a*\n"
                    "\u1787\u17d2\u179a\u17be\u179f package \u2192 \u1795\u17d2\u1791\u17c1\u179a info NiMo \u1795\u17d2\u178a\u179b\u17cb\n\n"
                    "*\u1787\u17c6\u17a0\u17b6\u1793 2 \u2014 \u1795\u17d2\u1789\u17be confirm*\n"
                    "Screenshot \u2192 \u1788\u17d2\u1798\u17c4\u17c7 + phone + package \u2192 \u1795\u17d2\u1789\u17be bot\n\n"
                    "*\u1787\u17c6\u17a0\u17b6\u1793 3 \u2014 NiMo confirm & \u1795\u17d2\u1789\u17be*\n"
                    "NiMo verify + \u1795\u17d2\u1789\u17be product \u1780\u17d2\u1793\u17bb\u1784 30 \u1793\u17b6\u1791\u17b8\n\n"
                    "*\u1787\u17c6\u17a0\u17b6\u1793 4 \u2014 \u1791\u1791\u17bd\u179b + \u1785\u17b6\u1794\u17cb\u1795\u17d2\u178a\u17be\u1798*\n"
                    "Kit + guide PDF + video + group support \U0001f680\n\n"
                    "*VIP:* \u1780\u17d2\u179a\u17c4\u1799\u1791\u1791\u17bd\u179b Kit NiMo \u178e\u17b6\u178f\u17cb Zoom \u17d4"
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "\U0001f50d \u179f\u17d2\u179c\u17c2\u1784\u1799\u179b\u17cb\u17a2\u17c6\u1796\u17b8 Cambodia Biz Agent",
                "questions": ["q_nimo", "q_system", "q_different", "q_save", "q_location"],
            },
            "cat_price": {
                "label": "\U0001f4b0 \u178f\u1798\u17d2\u179b\u17c3 & \u1780\u1789\u17d2\u1785\u1794\u17cb",
                "questions": ["q_price", "q_which_plan", "q_worth", "q_warranty"],
            },
            "cat_tech": {
                "label": "\U0001f6e0\ufe0f \u1780\u17b6\u179a\u178a\u17c6\u17a1\u17be\u1784 & \u1794\u1785\u17d2\u1785\u17c1\u1780\u179c\u17b7\u1791\u17d2\u1799\u17b6",
                "questions": ["q_tech", "q_time", "q_device", "q_internet", "q_team"],
            },
            "cat_support": {
                "label": "\U0001f512 \u1780\u17b6\u179a\u1792\u17b6\u1793\u17b6 & \u1787\u17c6\u1793\u17bd\u1799",
                "questions": ["q_data", "q_after_warranty", "q_update", "q_community"],
            },
            "cat_doubt": {
                "label": "\U0001f914 \u1793\u17c5\u178f\u17c2\u179f\u17d2\u1791\u17b6\u1780\u17cb\u179f\u17d2\u1791\u17be\u179a",
                "questions": ["q_competitor", "q_think", "q_try"],
            },
            "cat_buy": {
                "label": "\U0001f6cd\ufe0f \u1780\u17b6\u179a\u1791\u17b7\u1789",
                "questions": ["q_claude_pro", "q_riel", "q_industry", "q_delivery"],
            },
        },
        "s": {
            "welcome": (
                "\U0001f44b \u179f\u17bd\u179f\u17d2\u178f\u17b8! \u1781\u17d2\u1789\u17bb\u17c6\u1787\u17b6\u1787\u17c6\u1793\u17bd\u1799\u1780\u17b6\u179a\u179a\u1794\u179f\u17cb *NiMo Team*\u17d4\n\n"
                "\u1794\u1784\u1798\u17b6\u1793\u179f\u17c6\u178e\u17bd\u179a\u17a2\u17d2\u179c\u17b8\u17a2\u17c6\u1796\u17b8 *Cambodia Biz Agent*?\n"
                "\u1787\u17d2\u179a\u17be\u179f\u179f\u17c6\u178e\u17bd\u179a\u1781\u17b6\u1784\u1780\u17d2\u179a\u17c4\u1798 \u2014 \u1781\u17d2\u1789\u17bb\u17c6\u1786\u17d2\u179b\u17be\u1799\u1797\u17d2\u179b\u17b6\u1798\u17d7 \U0001f447"
            ),
            "choose_cat":       "\u1787\u17d2\u179a\u17be\u179f\u179f\u17c6\u178e\u17bd\u179a\u178a\u17c2\u179b\u1794\u1784\u1785\u1784\u17cb\u178a\u17b9\u1784:",
            "buy_title": (
                "\U0001f389 *\u179b\u17d2\u17a2\u178e\u17b6\u179f\u17cb! \u1794\u1784\u1785\u1784\u17cb\u1787\u17d2\u179a\u17be\u179f\u1780\u1789\u17d2\u1785\u1794\u17cb\u178e\u17b6?*\n\n"
                "\U0001f7e6 *Basic $97* \u2014 \u179f\u17b6\u1780\u179b\u17d2\u1794\u1784\u1798\u17bb\u1793\n"
                "\u2b50 *Pro $297* \u2014 \u179f\u17d2\u179c\u17d0\u1799\u1794\u17d2\u179a\u179c\u178f\u17d2\u178f\u17b7 24/7\n"
                "\U0001f7e1 *VIP $597* \u2014 NiMo \u178a\u17c6\u17a1\u17be\u1784\u1787\u17c6\u1793\u17bd\u179f\n\n"
                "\u1787\u17d2\u179a\u17be\u179f\u1780\u1789\u17d2\u1785\u1794\u17cb \U0001f447"
            ),
            "buy_btn":          "\U0001f4b3 \u1781\u17d2\u1789\u17bb\u17c6\u1785\u1784\u17cb\u1791\u17b7\u1789\u17a5\u17a1\u17bc\u179c",
            "consult_btn":      "\U0001f4ac \u179f\u17bd\u179a NiMo \u178a\u17c4\u1799\u1795\u17d2\u1791\u17b6\u179b\u17cb",
            "back_btn":         "\u2b05\ufe0f \u178f\u17d2\u179a\u17a1\u1794\u17cb\u1791\u17c5\u1798\u17c9\u17ba\u1793\u17bb\u1799",
            "back_cat":         "\u2b05\ufe0f \u179f\u17c6\u178e\u17bd\u179a\u1795\u17d2\u179f\u17c1\u1784\u1791\u17c0\u178f",
            "unsure_btn":       "\U0001f914 \u1781\u17d2\u1789\u17bb\u17c6\u1798\u17b7\u1793\u1791\u17b6\u1793\u17cb\u1794\u17d2\u179a\u17b6\u1780\u178a \u2014 \u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a\u1796\u17b7\u1782\u17d2\u179a\u17c4\u17c7",
            "consult_msg": (
                "\U0001f4ac *\u179f\u17bd\u179f\u17d2\u178f\u17b8! NiMo \u179a\u17b8\u1780\u179a\u17b6\u1799\u1787\u17bd\u1799\u1794\u1784* \u2764\ufe0f\n\n"
                "\u1785\u17bb\u1785\u179b\u17b8\u1784\u1781\u17b6\u1784\u1780\u17d2\u179a\u17c4\u1798 \u178a\u17be\u1798\u17d2\u1794\u17b8\u1791\u17c6\u1793\u17b6\u1780\u17cb\u1791\u17c6\u1793\u1784\u1795\u17d2\u1791\u17b6\u179b\u17cb\u1787\u17b6\u1798\u17bd\u1799\u17a2\u17d2\u1793\u1780\u1794\u17d2\u179a\u17b9\u1780\u17d2\u179f\u17b6:\n\n"
                "\U0001f449 [Chat with NiMo Advisor](https://t.me/sovanny68)\n\n"
                "_\u1794\u1793\u17d2\u1791\u17b6\u1794\u17cb\u1796\u17b8\u1791\u1791\u17bd\u179b\u1780\u17b6\u179a\u1794\u17d2\u179a\u17b9\u1780\u17d2\u179f\u17b6 \u179f\u17bc\u1798\u178f\u17d2\u179a\u17a1\u1794\u17cb\u1798\u1780\u1791\u17b7\u1789\u178a\u17c4\u1799\u1794\u17d2\u179a\u17be /start_ \U0001f6d2"
            ),
            "end_consult_btn":  "\U0001f51a \u1794\u1789\u17d2\u1785\u1794\u17cb \u2014 \u178f\u17d2\u179a\u17a1\u1794\u17cb\u1791\u17c5\u1798\u17c9\u17ba\u1793\u17bb\u1799",
            "end_consult_msg":  "\u2705 \u1794\u17b6\u1793\u1794\u1789\u17d2\u1785\u1794\u17cb\u17d4 \u17a2\u179a\u1782\u17bb\u178e\u1794\u1784 \u2764\ufe0f\n\n\u1785\u17bb\u1785 /start \u178a\u17be\u1798\u17d2\u1794\u17b8\u1794\u17be\u1780\u1798\u17c9\u17ba\u1793\u17bb\u1799\u17d4",
            "confirm_paid_btn": "\u2705 \u1781\u17d2\u1789\u17bb\u17c6\u1794\u17b6\u1793\u1795\u17d2\u1791\u17c1\u179a\u1794\u17d2\u179a\u17b6\u1780\u17cb\u179a\u17bd\u1785\u17a0\u17be\u1799",
            "ask_more_btn":     "\u2753 \u1781\u17d2\u1789\u17bb\u17c6\u178f\u17d2\u179a\u17bc\u179c\u1780\u17b6\u179a\u179f\u17bd\u179a\u1794\u1793\u17d2\u1790\u17c2\u1798",
            "view_payment_btn": "\U0001f4b3 \u1798\u17be\u179b\u1796\u17d0\u178f\u17cc\u1798\u17b6\u1793\u1795\u17d2\u1791\u17c1\u179a\u1794\u17d2\u179a\u17b6\u1780\u17cb",
            "unknown_msg":      "\u1781\u17d2\u1789\u17bb\u17c6\u1791\u1791\u17bd\u179b\u1794\u17b6\u1793\u179f\u17b6\u179a\u1794\u1784\u17a0\u17be\u1799 \u2764\ufe0f\n\n\u1794\u1784\u1785\u1784\u17cb:",
            "ask_bill":         "\U0001f4f8 *\u1787\u17c6\u17a0\u17b6\u1793\u1791\u17b8 1/3: \u1795\u17d2\u1789\u17be\u179a\u17bc\u1794\u1797\u17b6\u1796\u1794\u1784\u17d2\u1780\u17b6\u1793\u17cb\u178a\u17c3*\n\n\u179f\u17bc\u1798 *\u1790\u178f\u17a2\u17c1\u1780\u17d2\u179a\u1784\u17cb* \u1780\u17b6\u179a\u1795\u17d2\u1791\u17c1\u179a\u1794\u17d2\u179a\u17b6\u1780\u17cb \U0001f447",
            "need_photo":       "\u26a0\ufe0f \u179f\u17bc\u1798\u1795\u17d2\u1789\u17be *\u179a\u17bc\u1794\u1797\u17b6\u1796* \u1794\u1784\u17d2\u1780\u17b6\u1793\u17cb\u178a\u17c3 \U0001f4f8",
            "ask_name":         "\u2705 \u1791\u1791\u17bd\u179b\u1794\u17b6\u1793\u179a\u17bc\u1794\u1797\u17b6\u1796\u17a0\u17be\u1799!\n\n\U0001f464 *\u1787\u17c6\u17a0\u17b6\u1793\u1791\u17b8 2/3: \u1788\u17d2\u1798\u17c4\u17c7\u1796\u17c1\u1789*\n\n\u179f\u17bc\u1798\u179c\u17b6\u1799\u1788\u17d2\u1798\u17c4\u17c7\u179a\u1794\u179f\u17cb\u1794\u1784:",
            "need_text":        "\u26a0\ufe0f \u179f\u17bc\u1798\u179c\u17b6\u1799\u1787\u17b6\u17a2\u1780\u17d2\u179f\u179a\u17d4",
            "ask_phone":        "\u2705 \u1791\u1791\u17bd\u179b\u1794\u17b6\u1793\u1788\u17d2\u1798\u17c4\u17c7\u17a0\u17be\u1799!\n\n\U0001f4f1 *\u1787\u17c6\u17a0\u17b6\u1793\u1791\u17b8 3/3: \u179b\u17c1\u1781\u1791\u17bc\u179a\u179f\u17d0\u1796\u17d2\u1791*\n\n\u179f\u17bc\u1798\u1794\u1789\u17d2\u1785\u17bc\u179b\u179b\u17c1\u1781\u1791\u17bc\u179a\u179f\u17d0\u1796\u17d2\u1791:",
            "complete_msg": (
                "\U0001f389 *\u1791\u1791\u17bd\u179b\u1794\u17b6\u1793\u1796\u17d0\u178f\u17cc\u1798\u17b6\u1793\u1782\u17d2\u179a\u1794\u17cb\u1782\u17d2\u179a\u17b6\u1793\u17cb\u17a0\u17be\u1799!*\n\n"
                "\U0001f4cb *\u179f\u1784\u17d2\u1781\u17c1\u1794\u1780\u17b6\u179a\u1794\u1789\u17d2\u1787\u17b6\u1791\u17b7\u1789:*\n"
                "\u2022 \u179b\u17c1\u1781\u1780\u17bc\u178a: `{order_id}`\n"
                "\u2022 \u1788\u17d2\u1798\u17c4\u17c7: {name}\n"
                "\u2022 \u1791\u17bc\u179a\u179f\u17d0\u1796\u17d2\u1791: {phone}\n"
                "\u2022 \u1780\u1789\u17d2\u1785\u1794\u17cb: {label} ({price_usd})\n\n"
                "NiMo \u1793\u17b9\u1784\u1796\u17b7\u1793\u17b7\u178f\u17d2\u1799 \u1793\u17b7\u1784\u1794\u1789\u17d2\u1787\u17b6\u1780\u17cb\u1780\u17d2\u1793\u17bb\u1784 *30 \u1793\u17b6\u1791\u17b8* \u23f0\n\n"
                "\u17a2\u179a\u1782\u17bb\u178e\u1794\u1784\u178a\u17c2\u179b\u1791\u17bb\u1780\u1785\u17b7\u178f\u17d2\u178f NiMo \u2764\ufe0f"
            ),
            "package_msg": (
                "\U0001f389 *\u1794\u1784\u1794\u17b6\u1793\u1787\u17d2\u179a\u17be\u179f {label} \u2014 {price_usd}* ({price_riel})\n\n"
                "\U0001f4f2 *\u179f\u17bc\u1798 Scan QR ABA \u1781\u17b6\u1784\u179b\u17be \u178a\u17be\u1798\u17d2\u1794\u17b8\u1794\u1784\u17cb\u1794\u17d2\u179a\u17b6\u1780\u17cb*\n\n"
                "\U0001f4b5 *\u1785\u17c6\u1793\u17bd\u1793\u1791\u17b9\u1780\u1794\u17d2\u179a\u17b6\u1780\u17cb: {price_usd}*\n\n"
                "\u1794\u1793\u17d2\u1791\u17b6\u1794\u17cb\u1796\u17b8\u1795\u17d2\u1791\u17c1\u179a\u1794\u17d2\u179a\u17b6\u1780\u17cb\u17a0\u17be\u1799 \u179f\u17bc\u1798\u1785\u17bb\u1785\u1794\u17ca\u17bc\u178f\u17bb\u1784\u1781\u17b6\u1784\u1780\u17d2\u179a\u17c4\u1798 \U0001f447"
            ),
        },
    },

    "en": {
        "faq": {
            "q_nimo": {
                "label": "\U0001f464 Who is NiMo?",
                "answer": (
                    "\U0001f464 *Who is NiMo?*\n\n"
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
                "label": "\U0001f4ac I don't understand how this system works",
                "answer": (
                    "\U0001f4ac *How does Cambodia Biz Agent work?*\n\n"
                    "Simply put: you get *5 AI Employees* \u2014 each does 1 job:\n\n"
                    "\U0001f50d Market research & competitor analysis\n"
                    "\U0001f4e3 Create content for FB/TikTok/Instagram\n"
                    "\U0001f4b0 Write sales pages & close orders\n"
                    "\U0001f4e6 Auto-receive orders & send delivery notifications\n"
                    "\U0001f4ca Revenue reports & weekly optimization\n\n"
                    "You give commands in Khmer or English \u2014 AI works instantly.\n\n"
                    "No coding needed. \U0001f680"
                ),
            },
            "q_different": {
                "label": "\U0001f19a How is this different from other AI agents?",
                "answer": (
                    "\U0001f19a *How is Cambodia Biz Agent different from other agents?*\n\n"
                    "Most AI Agents are built for Western markets \u2014 "
                    "English, Stripe payments, US/EU business styles.\n\n"
                    "*Cambodia Biz Agent is different: built specifically for Cambodian business owners.*\n\n"
                    "\U0001f1f0\U0001f1ed *Language:* Natural Khmer \u2014 not machine translation\n\n"
                    "\U0001f4b3 *Payments:* ABA Pay, Wing Money, Bakong KHQR \u2014 no international card needed\n\n"
                    "\U0001f4f1 *Platforms:* Facebook, TikTok, Telegram \u2014 where Cambodian customers buy\n\n"
                    "\U0001f91d *Support:* NiMo is based in Cambodia, understands the market, gives direct support\n\n"
                    "Built from the real realities of this market \u2014 not copied from elsewhere."
                ),
            },
            "q_save": {
                "label": "\U0001f4b0 What will I save?",
                "answer": (
                    "\U0001f4b0 *What specifically will I save?*\n\n"
                    "What you save most \u2014 not money. *Time.*\n\n"
                    "Average shop owners spend ~3 hours/day on repetitive tasks: "
                    "writing captions, replying messages, posting, compiling orders.\n\n"
                    "*3 hours \xd7 30 days = 90 hours/month* \u2014 Cambodia Biz Agent handles all that.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "On money \u2014 real numbers:\n\n"
                    "\U0001f50d Market research: $100\u2013200/time\n"
                    "\U0001f4e3 Content writing: $50\u2013150/month\n"
                    "\U0001f4ac Order closing: $200\u2013300/month\n"
                    "\U0001f4e6 Order processing: $150\u2013250/month\n"
                    "\U0001f4ca Reporting: $100\u2013200/month\n\n"
                    "*Hiring people: ~$700\u20131,200/month*\n\n"
                    "Cambodia Biz Agent: one-time only\n"
                    "\U0001f7e6 Basic $97 \xb7 \u2b50 Pro $297 \xb7 \U0001f7e1 VIP $597\n\n"
                    "Year 1: save *$8,000\u201314,000* compared to hiring \U0001f4b0"
                ),
            },
            "q_location": {
                "label": "\U0001f3e2 Where is NiMo's office?",
                "answer": (
                    "\U0001f3e2 *Where is NiMo's office?*\n\n"
                    "NiMo operates fully online \u2014 no physical office. "
                    "This is a modern digital business model, like buying an app or online course "
                    "\u2014 you don't need to know where the office is to use it.\n\n"
                    "What matters more than an address: NiMo offers a *30-day 100% money-back guarantee* "
                    "if you're not satisfied. That's a clearer commitment than any address. \u2764\ufe0f"
                ),
            },
            "q_price": {
                "label": "\U0001f4b5 How much does Cambodia Biz Agent cost?",
                "answer": (
                    "\U0001f4b5 *How much does Cambodia Biz Agent cost? Monthly fees?*\n\n"
                    "Buy once \u2014 use forever. 3 plans to choose from:\n\n"
                    "\U0001f7e6 *Basic $97* (\u2248 400,000 Riel)\n"
                    "First-time trial \u2014 lowest risk\n\n"
                    "\u2b50 *Pro $297* (\u2248 1,200,000 Riel)\n"
                    "Full automation 24/7\n\n"
                    "\U0001f7e1 *VIP $597* (\u2248 2,400,000 Riel)\n"
                    "NiMo installs directly via Zoom \u2014 done and ready to use immediately\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Only ongoing cost: Claude Pro account ~$20/month.\n\n"
                    "*No hidden fees. No renewals. No surprises.*"
                ),
            },
            "q_which_plan": {
                "label": "\U0001f914 I don't know which plan fits me",
                "answer": (
                    "\U0001f914 *Which plan fits your shop?*\n\n"
                    "\U0001f7e6 *Basic $97* \u2014 New to AI, want to try first\n"
                    "\u2192 5 AI Employees + Khmer guide + 30-day support\n\n"
                    "\u2b50 *Pro $297* \u2014 Shop running, want full automation 24/7\n"
                    "\u2192 Chatbot + auto-post + auto-booking\n\n"
                    "\U0001f7e1 *VIP $597* \u2014 Don't want to install yourself\n"
                    "\u2192 NiMo installs everything, ready to use, 90-day support\n\n"
                    "Not sure? Tell NiMo about your shop \u2014 we'll recommend the right plan in 5 mins \U0001f447"
                ),
            },
            "q_worth": {
                "label": "\U0001f48e Is $297 worth it?",
                "answer": (
                    "\U0001f48e *Is $297 (or whatever I spend) worth it?*\n\n"
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
                "label": "\U0001f6e1\ufe0f Is there a warranty / refund policy?",
                "answer": (
                    "\U0001f6e1\ufe0f *Is there a warranty? Can I get a refund?*\n\n"
                    "Yes \u2014 and NiMo is confident about this.\n\n"
                    "*30-day guarantee \u2014 100% refund, no questions asked.*\n\n"
                    "Buy Cambodia Biz Agent. Follow the guide for 30 days. "
                    "If the system doesn't work as NiMo described \u2014 "
                    "message NiMo on Telegram. Refund within 24 hours.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "*The risk is on NiMo. Not on you.* \u2764\ufe0f"
                ),
            },
            "q_tech": {
                "label": "\U0001f630 I'm afraid I can't install it",
                "answer": (
                    "\U0001f630 *Not tech-savvy \u2014 can I still install it?*\n\n"
                    "Yes! Here's why:\n\n"
                    "\u2705 Step-by-step guide in Khmer with images\n"
                    "\u2705 Video tutorials to follow\n"
                    "\u2705 Bot support 24/7\n"
                    "\u2705 NiMo personally answers when needed\n\n"
                    "VIP plan: NiMo installs it with you via Zoom in 2 hours \u2014 "
                    "you just watch and click. \U0001f3af"
                ),
            },
            "q_time": {
                "label": "\u23f0 How long does setup take?",
                "answer": (
                    "\u23f0 *How long before I can start using it?*\n\n"
                    "*Basic & Pro:* Self-install following the guide ~2\u20133 hours \u2014 "
                    "do it in the evening or when free, no need to stop selling. "
                    "Day 2 you can create content. Day 3 the system runs on its own.\n\n"
                    "*VIP:* Just 1 Zoom session 2 hours with NiMo \u2014 "
                    "you watch, NiMo does everything, tests and hands over. Done.\n\n"
                    "Many NiMo customers buy in the morning \u2014 by evening they already have their first content to post \U0001f680"
                ),
            },
            "q_device": {
                "label": "\U0001f4f1 What devices do I need?",
                "answer": (
                    "\U0001f4f1 *What devices do I need to use this?*\n\n"
                    "Both computer and smartphone work \u2014 use whatever you have \U0001f60a\n\n"
                    "\U0001f4bb *Computer:* Recommended for initial setup and viewing reports \u2014 bigger screen is easier.\n\n"
                    "\U0001f4f1 *Smartphone only:* After NiMo helps with setup, you can run everything by phone \u2014 "
                    "reply to customers, post content, check revenue, all on app.\n\n"
                    "If it can scroll Facebook smoothly \u2014 it can run Cambodia Biz Agent. No upgrades needed."
                ),
            },
            "q_internet": {
                "label": "\U0001f310 Do I need fast internet?",
                "answer": (
                    "\U0001f310 *Do I need high-speed internet?*\n\n"
                    "No \u2014 just internet good enough for Facebook and Telegram.\n\n"
                    "Home WiFi or 4G both work fine. The system runs on cloud servers \u2014 "
                    "your device only needs to send commands, not do heavy processing \U0001f680"
                ),
            },
            "q_team": {
                "label": "\U0001f465 Can my staff use it too?",
                "answer": (
                    "\U0001f465 *Can my shop staff use it together?*\n\n"
                    "Absolutely! NiMo designed Cambodia Biz Agent for the whole shop \u2014 not just one person \U0001f60a\n\n"
                    "\u2705 Inbox staff use AI to reply customers faster\n"
                    "\u2705 Content staff use AI to create daily posts\n"
                    "\u2705 Managers use AI to view revenue reports\n\n"
                    "Everyone accesses one account \u2014 easy collaboration, no user limit.\n\n"
                    "\U0001f4a1 Claude Pro $20/month can be shared across the whole team \u2014 split the cost, no need for individual accounts."
                ),
            },
            "q_data": {
                "label": "\U0001f512 Will my shop data be leaked?",
                "answer": (
                    "\U0001f512 *Will my shop data be leaked?*\n\n"
                    "NiMo understands your concern \u2014 and here's NiMo's clear commitment: your data is completely safe.\n\n"
                    "\u2705 *Your data belongs to you:* Customers, orders, messages \u2014 all stored in your own account, no one else can access.\n\n"
                    "\u2705 *NiMo doesn't touch your shop data:* NiMo doesn't collect, sell, or share your data with anyone.\n\n"
                    "\u2705 *International security standards:* Built on Anthropic's platform (US) \u2014 same security standard as banks.\n\n"
                    "Your shop \u2192 your data \u2192 your control. NiMo keeps nothing. \u2764\ufe0f"
                ),
            },
            "q_after_warranty": {
                "label": "\U0001f91d What happens after the warranty?",
                "answer": (
                    "\U0001f91d *What support after the 30-day warranty?*\n\n"
                    "The 30-day warranty is just the refund policy \u2014 NiMo supports you with no time limit \U0001f60a\n\n"
                    "\u2705 Message NiMo on Telegram anytime \u2014 bugs, advice, optimization, NiMo is there.\n\n"
                    "\u2705 Join community group \u2014 learn from other shop owners using Cambodia Biz Agent.\n\n"
                    "\u2705 Receive updates when NiMo upgrades the system \u2014 completely free.\n\n"
                    "NiMo sells you the system \u2014 but doesn't abandon you after receiving payment. \u2764\ufe0f"
                ),
            },
            "q_update": {
                "label": "\U0001f199 Are there updates?",
                "answer": (
                    "\U0001f199 *Are there future updates/upgrades? Do they cost extra?*\n\n"
                    "Regular updates \u2014 completely free for existing customers \U0001f381\n\n"
                    "NiMo continually improves Cambodia Biz Agent based on real feedback. When there are:\n\n"
                    "\u2705 New features\n"
                    "\u2705 Better AI commands\n"
                    "\u2705 Speed & effectiveness improvements\n\n"
                    "\u2192 You receive updates automatically via group, no extra payment.\n\n"
                    "Buy once \u2014 get upgraded forever."
                ),
            },
            "q_community": {
                "label": "\U0001f465 Is there a community group?",
                "answer": (
                    "\U0001f465 *Does NiMo have a community group?*\n\n"
                    "Yes! This is one of the values NiMo is most proud of \U0001f49b\n\n"
                    "After purchasing, NiMo adds you to a *private Telegram community* where you:\n\n"
                    "\u2705 Meet other Cambodian shop owners \u2014 share real daily experiences.\n\n"
                    "\u2705 Learn more effective AI usage from those who went before.\n\n"
                    "\u2705 Receive new tips & AI commands NiMo updates weekly.\n\n"
                    "\u2705 Get quick answers \u2014 NiMo and community are ready to help.\n\n"
                    "You never go alone \u2014 the whole community goes with you \u2764\ufe0f"
                ),
            },
            "q_competitor": {
                "label": "\u2694\ufe0f What if competitors use it too?",
                "answer": (
                    "\u2694\ufe0f *If competitors use it too, do I still have an advantage?*\n\n"
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
                "label": "\U0001f914 Let me think about it",
                "answer": (
                    "\U0001f914 *Let me think about it*\n\n"
                    "Of course \u2014 this is a business decision \U0001f60a\n\n"
                    "But before thinking, 3 things NiMo wants you to know:\n\n"
                    "*One \u2014 Current price is early bird.*\n"
                    "After launch, price goes up. Buying today = best price.\n\n"
                    "*Two \u2014 30-day 100% money-back guarantee.*\n"
                    "You're trying with virtually zero real risk. Not happy \u2192 refund.\n\n"
                    "*Three \u2014 Every day you wait is a day lost.*\n"
                    "Not money \u2014 but time, orders, opportunities. Those can't be refunded.\n\n"
                    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n\n"
                    "Need more info to decide? NiMo is here \U0001f60a"
                ),
            },
            "q_try": {
                "label": "\U0001f9ea I want to try before buying",
                "answer": (
                    "\U0001f9ea *I want to try before buying*\n\n"
                    "NiMo understands \u2014 and doesn't blame that \U0001f60a\n\n"
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
                "label": "\U0001f4b3 What is Claude Pro $20/month?",
                "answer": (
                    "\U0001f4b3 *What is Claude Pro $20/month? Is it required?*\n\n"
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
                "label": "\U0001f4b5 Can I pay in Riel?",
                "answer": (
                    "\U0001f4b5 *Can I pay in Riel?*\n\n"
                    "Yes! Transfer in Riel normally \u2014 "
                    "ABA Bank automatically converts to USD.\n\n"
                    "\U0001f7e6 *Basic $97* \u2248 400,000 Riel\n"
                    "\u2b50 *Pro $297* \u2248 1,200,000 Riel\n"
                    "\U0001f7e1 *VIP $597* \u2248 2,400,000 Riel"
                ),
            },
            "q_industry": {
                "label": "\U0001f6cd\ufe0f Does my business type work?",
                "answer": (
                    "\U0001f6cd\ufe0f *I sell [food/beauty/fashion/services]\u2026 will it work?*\n\n"
                    "NiMo's short answer: *if you sell online in Cambodia, your shop works.*\n\n"
                    "NiMo has tested Cambodia Biz Agent across many industries:\n\n"
                    "\U0001f457 Fashion & accessories\n"
                    "\U0001f484 Beauty & skincare\n"
                    "\U0001f371 Food & specialty\n"
                    "\U0001f4da Courses & consulting\n"
                    "\U0001f486 Spa, salon, studio\n"
                    "\U0001f3e0 Furniture & home goods\n"
                    "\U0001f338 Flowers & gifts\n\n"
                    "AI learns according to your shop's products and style \u2014 not a rigid formula.\n\n"
                    "Not sure? Tell NiMo your specific industry \u2014 free consultation \U0001f447"
                ),
            },
            "q_delivery": {
                "label": "\U0001f4e6 How do I receive after paying?",
                "answer": (
                    "\U0001f4e6 *After transferring, how do I receive the product?*\n\n"
                    "Simple \u2014 just 4 steps:\n\n"
                    "*Step 1 \u2014 Transfer*\n"
                    "Choose a plan \u2192 transfer to the info NiMo provides\n\n"
                    "*Step 2 \u2014 Send confirmation*\n"
                    "Screenshot the transfer \u2192 send with name + phone + chosen plan to bot\n\n"
                    "*Step 3 \u2014 NiMo confirms & delivers*\n"
                    "NiMo verifies and sends the full product within 30 minutes\n\n"
                    "*Step 4 \u2014 Receive & begin*\n"
                    "Get the Kit + guide PDF + videos + support group \u2014 start setup \U0001f680\n\n"
                    "*VIP:* After receiving the Kit, NiMo contacts you to schedule a Zoom session."
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "\U0001f50d Learn about Cambodia Biz Agent",
                "questions": ["q_nimo", "q_system", "q_different", "q_save", "q_location"],
            },
            "cat_price": {
                "label": "\U0001f4b0 Pricing & Plans",
                "questions": ["q_price", "q_which_plan", "q_worth", "q_warranty"],
            },
            "cat_tech": {
                "label": "\U0001f6e0\ufe0f Setup & Technology",
                "questions": ["q_tech", "q_time", "q_device", "q_internet", "q_team"],
            },
            "cat_support": {
                "label": "\U0001f512 Warranty & Support",
                "questions": ["q_data", "q_after_warranty", "q_update", "q_community"],
            },
            "cat_doubt": {
                "label": "\U0001f914 Still Hesitating",
                "questions": ["q_competitor", "q_think", "q_try"],
            },
            "cat_buy": {
                "label": "\U0001f6cd\ufe0f Buying",
                "questions": ["q_claude_pro", "q_riel", "q_industry", "q_delivery"],
            },
        },
        "s": {
            "welcome": (
                "\U0001f44b Hello! I'm the assistant of *NiMo Team*.\n\n"
                "What are you wondering about *Cambodia Biz Agent*?\n"
                "Choose a question below \u2014 I'll answer right away \U0001f447"
            ),
            "choose_cat":       "Choose a question:",
            "buy_title": (
                "\U0001f389 *Great! Which plan do you want?*\n\n"
                "\U0001f7e6 *Basic $97* \u2014 Try it first\n"
                "\u2b50 *Pro $297* \u2014 Full automation 24/7\n"
                "\U0001f7e1 *VIP $597* \u2014 NiMo installs it for you\n\n"
                "Choose a plan \U0001f447"
            ),
            "buy_btn":          "\U0001f4b3 I WANT TO BUY NOW",
            "consult_btn":      "\U0001f4ac Chat directly with NiMo",
            "back_btn":         "\u2b05\ufe0f Back to main menu",
            "back_cat":         "\u2b05\ufe0f Other questions",
            "unsure_btn":       "\U0001f914 I'm not sure \u2014 need advice",
            "consult_msg": (
                "\U0001f4ac *Hi! NiMo is happy to help you* \u2764\ufe0f\n\n"
                "Click the link below to chat directly with our advisor:\n\n"
                "\U0001f449 [Chat with NiMo Advisor](https://t.me/sovanny68)\n\n"
                "_After consulting, come back here to place your order with /start_ \U0001f6d2"
            ),
            "end_consult_btn":  "\U0001f51a End consultation \u2014 back to menu",
            "end_consult_msg":  "\u2705 Consultation ended. Thank you \u2764\ufe0f\n\nType /start to open the menu again.",
            "confirm_paid_btn": "\u2705 I have transferred \u2014 send receipt",
            "ask_more_btn":     "\u2753 I have more questions",
            "view_payment_btn": "\U0001f4b3 View payment details",
            "unknown_msg":      "I received your message \u2764\ufe0f\n\nWhat would you like to do?",
            "ask_bill":         "\U0001f4f8 *Step 1/3: Send payment receipt*\n\nPlease *screenshot* the bank transfer confirmation \U0001f447",
            "need_photo":       "\u26a0\ufe0f Please send a *photo* of your receipt \U0001f4f8",
            "ask_name":         "\u2705 Receipt received!\n\n\U0001f464 *Step 2/3: Full name*\n\nPlease enter your full name:",
            "need_text":        "\u26a0\ufe0f Please enter text.",
            "ask_phone":        "\u2705 Name received!\n\n\U0001f4f1 *Step 3/3: Phone number*\n\nPlease enter your phone number:",
            "complete_msg": (
                "\U0001f389 *All information received!*\n\n"
                "\U0001f4cb *Order summary:*\n"
                "\u2022 Order ID: `{order_id}`\n"
                "\u2022 Name: {name}\n"
                "\u2022 Phone: {phone}\n"
                "\u2022 Plan: {label} ({price_usd})\n\n"
                "NiMo will verify and confirm within *30 minutes* \u23f0\n\n"
                "Thank you for trusting NiMo \u2764\ufe0f"
            ),
            "package_msg": (
                "\U0001f389 *You selected {label} \u2014 {price_usd}* ({price_riel})\n\n"
                "\U0001f4f2 *Scan the ABA QR code above to pay*\n\n"
                "\U0001f4b5 *Amount: {price_usd}*\n\n"
                "After transferring, tap the button below to send your receipt \U0001f447"
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
        InlineKeyboardButton("\U0001f1f0\U0001f1ed \u1797\u17b6\u179f\u17b6\u1781\u17d2\u1798\u17c2\u179a", callback_data="lang_km"),
        InlineKeyboardButton("\U0001f1ec\U0001f1e7 English",    callback_data="lang_en"),
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
        [InlineKeyboardButton("\U0001f7e6 Basic $97  (\u2248 400,000 Riel)",   callback_data="buy_basic")],
        [InlineKeyboardButton("\u2b50 Pro $297   (\u2248 1,200,000 Riel)", callback_data="buy_pro")],
        [InlineKeyboardButton("\U0001f7e1 VIP $597  (\u2248 2,400,000 Riel)",  callback_data="buy_vip")],
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
    context.user_data.clear()
    await update.message.reply_text(
        "\U0001f1f0\U0001f1ed \u1787\u17d2\u179a\u17be\u179f\u1797\u17b6\u179f\u17b6  |  \U0001f1ec\U0001f1e7 Choose language:",
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

        amounts = {"basic": 97, "pro": 297, "vip": 597}
        caption = s["package_msg"].format(
            label=info["label"],
            price_usd=info["price_usd"],
            price_riel=info["price_riel"],
        )
        try:
            await query.message.delete()
        except Exception:
            pass
        qr_buf = make_aba_qr(amounts[package])
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=qr_buf,
            caption=caption,
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
        user = query.from_user
        if ADMIN_ID and user.id != ADMIN_ID:
            lang = get_lang(context)
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=(
                        f"\U0001f4ac *Kh\xe1ch c\u1ea7n t\u01b0 v\u1ea5n [{lang.upper()}]*\n"
                        f"\U0001f464 {user.full_name} (@{user.username or 'no username'})\n"
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
                text=f"\U0001f4ac *NiMo:*\n\n{update.message.text}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("\u2705 Sent.")
        except Exception as e:
            await update.message.reply_text(f"\u274c {e}")
        return

    # Consulting mode \u2192 forward to admin
    if consulting and not awaiting:
        text = update.message.text or "(media)"
        if ADMIN_ID:
            try:
                fwd = (
                    f"\U0001f4ac *{user.full_name}* (@{user.username or 'no username'})\n"
                    f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n{text}\n\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n`#cid:{user.id}`"
                )
                await context.bot.send_message(chat_id=ADMIN_ID, text=fwd, parse_mode="Markdown")
                if update.message.photo:
                    await context.bot.send_photo(
                        chat_id=ADMIN_ID,
                        photo=update.message.photo[-1].file_id,
                        caption=f"\U0001f4f8 {user.full_name}\n`#cid:{user.id}`",
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

        # Ghi \u0111\u01a1n v\xe0o Google Sheet CRM
        asyncio.create_task(_post_to_sheet({
            "name":     context.user_data.get("name", ""),
            "phone":    context.user_data["phone"],
            "telegram": str(user.id),
            "source":   f"bot-order-{package}",
            "order_id": context.user_data["order_id"],
            "package":  info["label"],
            "price":    info["price_usd"],
            "lang":     get_lang(context)
        }))

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
                f"\U0001f534 *\u0110\u01a0N M\u1edaI [{lang.upper()}]*\n\n"
                f"\U0001f4cb M\xe3 \u0111\u01a1n: `{context.user_data['order_id']}`\n"
                f"\U0001f464 T\xean: {context.user_data['name']}\n"
                f"\U0001f4f1 S\u0110T: {context.user_data['phone']}\n"
                f"\U0001f4e6 G\xf3i: *{info['label']}* \u2014 {info['price_usd']}\n"
                f"\U0001f194 Telegram ID: `{user.id}`\n\n"
                f"\U0001f449 L\u1ec7nh x\xe1c nh\u1eadn:\n"
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
        await update.message.reply_text("\u26d4")
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
        await update.message.reply_text("\u26d4")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Syntax: `/tra <customer_id> <message>`", parse_mode="Markdown")
        return
    try:
        cid  = int(context.args[0])
        text = " ".join(context.args[1:])
        await context.bot.send_message(
            chat_id=cid,
            text=f"\U0001f4ac *NiMo:*\n\n{text}",
            parse_mode="Markdown"
        )
        await update.message.reply_text("\u2705 Sent.")
    except Exception as e:
        await update.message.reply_text(f"\u274c {e}")

# \u2500\u2500\u2500 MAIN \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("xacnhan", xacnhan))
    app.add_handler(CommandHandler("tra",     tra))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_message))
    print("\u2705 Bot (KM + EN) \u0111ang ch\u1ea1y... /start \u0111\u1ec3 test!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
