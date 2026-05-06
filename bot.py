# -*- coding: utf-8 -*-
"""
Cambodia Biz Agent — Bot Khmer + English
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

# ─── KHQR GENERATOR ─────────────────────────────────────────────────────────

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

# ─── CONFIG ─────────────────────────────────────────────────────────────────
import os

TOKEN                = os.environ.get("BOT_TOKEN", "8750588238:AAFUJ3o6iR7Cu92on2HdsvLhKP5pQHs15Bo")
ADMIN_ID             = int(os.environ.get("ADMIN_ID", "8704923191"))
APPS_SCRIPT_URL      = os.environ.get("APPS_SCRIPT_URL", "https://script.google.com/macros/s/AKfycbz3OQtNOOOgXmCwbO-sODdFw_TDQd8zRAMwtEbqML1H3pApYywaYeXzr0gcE44OjOOF/exec")
STAFF_USERNAME       = os.environ.get("STAFF_USERNAME", "sovanny68")
ANTHROPIC_API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")
DONE_MONEY_GROUP_ID  = int(os.environ.get("DONE_MONEY_GROUP_ID", "0"))

# APV storage: {apv_code: {amount, name, time}}
_apv_store: dict = {}

import re
import base64
import time

def _parse_payway_apv(text: str) -> dict | None:
    """Parse PayWay message: extract amount, payer name, APV."""
    apv_match    = re.search(r'APV[:\s]+(\d{4,8})', text, re.IGNORECASE)
    amount_match = re.search(r'\$([0-9.]+)\s*paid', text, re.IGNORECASE)
    name_match   = re.search(r'paid by\s+([A-Z][A-Z\s]+?)\s+\(', text)
    if not apv_match:
        return None
    return {
        "apv":    apv_match.group(1),
        "amount": float(amount_match.group(1)) if amount_match else 0,
        "payer":  name_match.group(1).strip() if name_match else "Unknown"
    }

async def _ocr_bill_image(photo_bytes: bytes) -> str | None:
    """Use Claude Vision to extract APV from ABA bill screenshot."""
    if not ANTHROPIC_API_KEY:
        return None
    def _call():
        import urllib.request as _ur
        body = _json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 100,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64.b64encode(photo_bytes).decode()
                    }},
                    {"type": "text", "text": "This is an ABA bank payment confirmation. Extract ONLY the APV number (4-8 digits). Reply with just the number, nothing else."}
                ]
            }]
        }).encode()
        req = _ur.Request(
            "https://api.anthropic.com/v1/messages", data=body,
            headers={"Content-Type": "application/json",
                     "x-api-key": ANTHROPIC_API_KEY,
                     "anthropic-version": "2023-06-01"}, method="POST"
        )
        try:
            with _ur.urlopen(req, timeout=15) as r:
                result = _json.loads(r.read())
                text = result["content"][0]["text"].strip()
                m = re.search(r'\d{4,8}', text)
                return m.group(0) if m else None
        except Exception as e:
            logging.error(f"OCR error: {e}")
            return None
    return await asyncio.get_event_loop().run_in_executor(None, _call)

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Listen to DONE Money group for PayWay payment notifications."""
    if not DONE_MONEY_GROUP_ID:
        return
    if update.effective_chat.id != DONE_MONEY_GROUP_ID:
        return
    text = (update.message.text or update.message.caption or "")
    parsed = _parse_payway_apv(text)
    if not parsed:
        return
    apv = parsed["apv"]
    _apv_store[apv] = {**parsed, "ts": time.time()}
    # Purge entries older than 2 hours
    now = time.time()
    for k in list(_apv_store.keys()):
        if now - _apv_store[k].get("ts", 0) > 7200:
            del _apv_store[k]
    logging.info(f"PayWay APV captured: {apv}  amount=${parsed['amount']}  payer={parsed['payer']}")

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

# ─── PAYMENT INFO ────────────────────────────────────────────────────────────

BANK_INFO = {
    "basic": {"label": "Basic", "price_usd": "$97",  "price_riel": "≈ 400,000 Riel"},
    "pro":   {"label": "Pro",   "price_usd": "$297", "price_riel": "≈ 1,200,000 Riel"},
    "vip":   {"label": "VIP",   "price_usd": "$597", "price_riel": "≈ 2,400,000 Riel"},
}

BANK_DETAILS = {
    "km": (
        "💳 *ព័ត៌មានការផ្ទេរប្រាក់*\n\n"
        "🏦 *ABA Bank*\n"
        "លេខគណនី: `000 123 456`\n"
        "ឈ្មោះ: NIMO TEAM\n\n"
        "📱 *Wing Money*\n"
        "លេខទូរស័ព្ទ: `012 345 678`\n"
        "ឈ្មោះ: NIMO TEAM\n\n"
        "⚠️ *សម្គាល់:* សូមសរសេរលេខកូដបញ្ជាទិញ NiMo ផ្ញើអោយ ក្នុងការផ្ទេរ។"
    ),
    "en": (
        "💳 *Payment Details*\n\n"
        "🏦 *ABA Bank*\n"
        "Account: `000 123 456`\n"
        "Name: NIMO TEAM\n\n"
        "📱 *Wing Money*\n"
        "Phone: `012 345 678`\n"
        "Name: NIMO TEAM\n\n"
        "⚠️ *Note:* Include the order code NiMo provides in the transfer remark."
    ),
}

# ─── CONTENT ─────────────────────────────────────────────────────────────────

CONTENT = {
    "km": {
        "faq": {
            "q_nimo": {
                "label": "👤 NiMo ជានរណា?",
                "answer": (
                    "👤 *NiMo ជានរណា?*\n\n"
                    "NiMo បានកើតចេញពីបំណងប្រាថ្នាមួយ:\n\n"
                    "_ចង់ចំណូលរួមអ្វីមួយមានអត្ថន័យ ដល់សហគមន៍អាជីវកម្មនៅកម្ពុជា។_\n\n"
                    "ខណៈប្រទេសជិតខាងប្រើ AI ស្វ័យប្រវត្តិតាំងពីយូរ — "
                    "ម្ចាស់ហាងកម្ពុជាជាច្រើននៅធ្វើការដោយដៃ។ "
                    "មិនមែនមិនចង់ប្ដូរ — គ្រាន់តែមិនទាន់មានឧបករណ៍សមស្រប។\n\n"
                    "NiMo កើតឡើងដើម្បីបំពេញចន្លោះនោះ — "
                    "ជួយម្ចាស់ហាងខ្មែរ access AI ដោយងាយ ជាភាសារបស់ខ្លួន។"
                ),
            },
            "q_system": {
                "label": "💬 ខ្ញុំមិនទាន់យល់ច្បាស់អំពីប្រព័ន្ធនេះ",
                "answer": (
                    "💬 *ប្រព័ន្ធ Cambodia Biz Agent ដំណើរការយ៉ាងដូចម្តេច?*\n\n"
                    "យល់ឱ្យសាមញ្ញ: បង មាន *បុគ្គលិក AI ចំនួន 5 នាក់* — ម្នាក់ធ្វើការងារ 1:\n\n"
                    "🔍 ស្រាវជ្រាវទីផ្សារ និងគូប្រជែង\n"
                    "📣 បង្កើតមាតិកា FB/TikTok/Instagram\n"
                    "💰 សរសេរទំព័រលក់ និងបិទការបញ្ជាទិញ\n"
                    "📦 ទទួលការបញ្ជាទិញ និងជូនដំណឹងដោយស្វ័យប្រវត្តិ\n"
                    "📊 របាយការណ៍ចំណូល និងបង្កើនប្រសិទ្ធភាព\n\n"
                    "បងបញ្ជាជាភាសាខ្មែរ — AI ធ្វើការភ្លាមៗ។\n\n"
                    "មិនចាំបាច់ចេះសរសេរកូដ។ 🚀"
                ),
            },
            "q_different": {
                "label": "🆚 Cambodia Biz Agent ខុសពី Agent ដទៃ?",
                "answer": (
                    "🆚 *Cambodia Biz Agent ខុសពី Agent ដទៃដូចម្ដេច?*\n\n"
                    "AI Agent ជាច្រើនត្រូវបានសាងសង់សម្រាប់ទីផ្សារខាងលិច — "
                    "ភាសាអង់គ្លេស Stripe payments ស្ទីល US/EU ។\n\n"
                    "*Cambodia Biz Agent ខុស: សាងសង់ជាពិសេសសម្រាប់ម្ចាស់ហាងកម្ពុជា។*\n\n"
                    "🇰🇭 *ភាសា:* ខ្មែរធម្មជាតិ — មិនមែន google translate\n\n"
                    "💳 *ការទូទាត់:* ABA Pay, Wing Money, Bakong KHQR — គ្មានកាតអន្តរជាតិ\n\n"
                    "📱 *វេទិកា:* Facebook, TikTok, Telegram — ត្រូវជាកន្លែងខ្មែរទិញ\n\n"
                    "🤝 *ជំនួយ:* NiMo នៅកម្ពុជា យល់ទីផ្សារ ជួយផ្ទាល់\n\n"
                    "សាងសង់ពីភាពជាក់ស្ដែងនៃទីផ្សារនេះ — មិនមែន copy ពីកន្លែងផ្សេង។"
                ),
            },
            "q_save": {
                "label": "💰 ខ្ញុំនឹងសន្សំបានអ្វី?",
                "answer": (
                    "💰 *ប្រព័ន្ធនេះជួយខ្ញុំសន្សំបានអ្វី?*\n\n"
                    "អ្វីដែលបងសន្សំបានច្រើនបំផុត — មិនមែនលុយ។ ពេលវេលា។\n\n"
                    "ម្ចាស់ហាងជាមធ្យមមាន 3 ម៉ោង/ថ្ងៃ ចំណាយលើការងារដដែលៗ:\n"
                    "សរសេរ caption ឆ្លើយសារ ប្រកាស ។\n\n"
                    "*3 ម៉ោង × 30 ថ្ងៃ = 90 ម៉ោង/ខែ* — Cambodia Biz Agent ធ្វើជំនួស។\n\n"
                    "─────────\n\n"
                    "ចំពោះ cost:\n\n"
                    "🔍 ស្រាវជ្រាវ: $100–200/ដង\n"
                    "📣 Content: $50–150/ខែ\n"
                    "💬 Inbox: $200–300/ខែ\n"
                    "📦 ដោះស្រាយការបញ្ជាទិញ: $150–250/ខែ\n"
                    "📊 របាយការណ៍: $100–200/ខែ\n\n"
                    "*ជួលមនុស្ស: ~$700–1,200/ខែ*\n\n"
                    "Cambodia Biz Agent: ម្ដងប៉ុណ្ណោះ 🟦$97 · ⭐$297 · 🟡$597\n\n"
                    "ឆ្នាំដំបូង សន្សំ *$8,000–14,000* 💰"
                ),
            },
            "q_location": {
                "label": "🏢 ការិយាល័យ NiMo នៅទីណា?",
                "answer": (
                    "🏢 *ការិយាល័យ NiMo នៅទីណា?*\n\n"
                    "NiMo ដំណើរការ online ទាំងស្រុង — គ្មានការិយាល័យ physical ។ "
                    "ដូចពេលបងទិញ app ឬ course online — "
                    "គ្មានការិយាល័យ ក៏ប្រើបានធម្មតា។\n\n"
                    "អ្វីសំខាន់: NiMo ធានា *30 ថ្ងៃ បង្វិលលុយ 100%* "
                    "ប្រសិនបើបងមិនពេញចិត្ត។ ❤️"
                ),
            },
            "q_price": {
                "label": "💵 Cambodia Biz Agent តម្លៃប៉ុន្មាន?",
                "answer": (
                    "💵 *Cambodia Biz Agent តម្លៃប៉ុន្មាន? មានថ្លៃ/ខែ?*\n\n"
                    "ទិញម្ដង — ប្រើជារៀងរហូត។ មាន 3 កញ្ចប់:\n\n"
                    "🟦 *Basic $97* (≈ 400,000 Riel)\n"
                    "សាកល្បង — ហានិភ័យតិចបំផុត\n\n"
                    "⭐ *Pro $297* (≈ 1,200,000 Riel)\n"
                    "ស្វ័យប្រវត្តិ 24/7\n\n"
                    "🟡 *VIP $597* (≈ 2,400,000 Riel)\n"
                    "NiMo ដំឡើងជាមួយបង Zoom — ចប់ប្រើភ្លាម\n\n"
                    "─────────\n\n"
                    "ថ្លៃប្រចាំខែតែមួយ: Claude Pro ~$20.\n\n"
                    "*គ្មានថ្លៃលាក់ស្ងាត់ គ្មានការ renew ។*"
                ),
            },
            "q_which_plan": {
                "label": "🤔 ខ្ញុំមិនដឹងថាកញ្ចប់ណាសាកសម",
                "answer": (
                    "🤔 *កញ្ចប់ណាសាកសមជាមួយហាងរបស់បង?*\n\n"
                    "🟦 *Basic $97* — ទើបស្គាល់ AI ចង់សាកល្បងមុន\n"
                    "→ បុគ្គលិក AI 5 នាក់ + ការណែនាំជាភាសាខ្មែរ + ការគាំទ្រ 30 ថ្ងៃ\n\n"
                    "⭐ *Pro $297* — ហាងដំណើរការ ចង់ស្វ័យប្រវត្តិ 24/7\n"
                    "→ Chatbot ឆ្លើយ + ប្រកាសដោយស្វ័យប្រវត្តិ + ទទួល booking\n\n"
                    "🟡 *VIP $597* — មិនចង់ដំឡើងខ្លួនឯង NiMo ធ្វើជំនួស\n"
                    "→ ដំឡើងរួច ប្រើបានភ្លាម ការគាំទ្រ 90 ថ្ងៃ\n\n"
                    "មិនប្រាកដ? ប្រាប់ NiMo អំពីហាងរបស់បង — យើងណែនាំកញ្ចប់ត្រឹមត្រូវ 👇"
                ),
            },
            "q_worth": {
                "label": "💎 $297 មានតម្លៃចំណាយទេ?",
                "answer": (
                    "💎 *$297 មានតម្លៃចំណាយទេ?*\n\n"
                    "ចូរឱ្យលេខតបតែ។\n\n"
                    "*បុគ្គលិក inbox កម្ពុជា:* $200–300/ខែ\n"
                    "→ 8 ម៉ោង/ថ្ងៃ។ ឈប់ឈរ។ ឈឺ = បន្ថយ productivity ។\n\n"
                    "*Cambodia Biz Agent Pro $297* — ម្ដងប៉ុណ្ណោះ\n"
                    "→ 24/7 ។ មិនឈប់ ។ មិនសុំឡើងប្រាក់ ។\n\n"
                    "─────────\n\n"
                    "$297 = ថ្លៃ inbox ក្រោមមួយខែ ។\n"
                    "ប៉ុន្តែ Cambodia Biz Agent ធ្វើ*ជារៀងរហូត* ។\n\n"
                    "ប្រសិនបើ AI ជួយបងបិទ 5 ការបញ្ជាទិញ/ខែ — $297  រ/ហើយ ។"
                ),
            },
            "q_warranty": {
                "label": "🛡️ ផលិតផលមានការធានារ៉ាប់រង?",
                "answer": (
                    "🛡️ *ផលិតផលមានការធានា? អាចបង្វិលលុយ?*\n\n"
                    "មានជាការប្រាកដ ។ NiMo ទំនុកចិត្ត ។\n\n"
                    "*ធានា 30 ថ្ងៃ — បង្វិលលុយ 100% ដោយ/ហេតុផល ។*\n\n"
                    "ទិញ ។ ធ្វើតាមការណែនាំ 30 ថ្ងៃ ។ "
                    "ប្រសិនបើ/ដំណើរការ/ពិពណ៌នា — ផ្ញើ NiMo Telegram ។ "
                    "បង្វិលក្នុង 24 ម៉ោង ។\n\n"
                    "*ហានិភ័យ: NiMo ។ មិន/បង ។* ❤️"
                ),
            },
            "q_tech": {
                "label": "😰 ខ្ញុំខ្លាចដំឡើងមិនបាន",
                "answer": (
                    "😰 *មិនចេះបច្ចេកវិទ្យា — អាចដំឡើងបានទេ?*\n\n"
                    "បាន! នេះជាហេតុផល:\n\n"
                    "✅ ការណែនាំជាភាសាខ្មែរ មានរូបភាពបង្ហាញជាជំហានៗ\n"
                    "✅ មានវីដេអូមើលតាម\n"
                    "✅ ប្រើ Bot ជួយ 24/7\n"
                    "✅ NiMo ផ្ទាល់ឆ្លើយពេលត្រូវការ\n\n"
                    "កញ្ចប់ VIP: NiMo អង្គុយដំឡើងជាមួយបងតាម Zoom 2 ម៉ោង — "
                    "បងគ្រាន់តែមើល ហើយចុចតាម។ 🎯"
                ),
            },
            "q_time": {
                "label": "⏰ ចំណាយពេលប៉ុន្មានដើម្បីចាប់ផ្ដើម?",
                "answer": (
                    "⏰ *ចំណាយពេលប៉ុន្មានដើម្បីចាប់ប្រើ?*\n\n"
                    "*Basic & Pro:* ដំឡើងតាមការណែនាំ ~2–3 ម៉ោង — "
                    "ធ្វើពេលល្ងាច ។ ថ្ងៃ 2 មាន content ។ ថ្ងៃ 3 ដំណើរការ ។\n\n"
                    "*VIP:* Zoom 2 ម៉ោងជាមួយ NiMo — "
                    "NiMo ធ្វើ test ចប់ប្រគល់ ។\n\n"
                    "ទិញពេលព្រឹក — ល្ងាចមាន content ដំបូង 🚀"
                ),
            },
            "q_device": {
                "label": "📱 ត្រូវការឧបករណ៍អ្វី?",
                "answer": (
                    "📱 *ត្រូវការឧបករណ៍អ្វី?*\n\n"
                    "Computer ឬ smartphone ក៏ប្រើបាន 😊\n\n"
                    "💻 *Computer:* NiMo ណែនាំ ដំឡើងដំបូង + មើលរបាយការណ៍\n\n"
                    "📱 *Smartphone:* ប្រតិបត្តិការប្រចាំថ្ងៃ ឆ្លើយ post report\n\n"
                    "Computer ណាដែល scroll Facebook ស្រួល — ប្រើ Cambodia Biz Agent បាន ។ "
                    "គ្មានការ upgrade ។"
                ),
            },
            "q_internet": {
                "label": "🌐 ត្រូវការ internet លឿន?",
                "answer": (
                    "🌐 *ត្រូវការ internet ល្បឿនខ្ពស់?*\n\n"
                    "មិនទាមទារ ។ Internet ប្រើ Facebook + Telegram ធម្មតា — ប្រើ Agent បាន ។\n\n"
                    "WiFi ផ្ទះ ឬ 4G ក៏ OK ។ ប្រព័ន្ធ run cloud — "
                    "phone/computer គ្រាន់តែ ផ្ញើ command 🚀"
                ),
            },
            "q_team": {
                "label": "👥 បុគ្គលិកអាចប្រើរួមគ្នា?",
                "answer": (
                    "👥 *បុគ្គលិកហាងអាចប្រើរួម?*\n\n"
                    "បានជាការប្រាកដ! NiMo រចនា Cambodia Biz Agent ឱ្យប្រើ team ទាំងមូល 😊\n\n"
                    "✅ Inbox staff ប្រើ AI ឆ្លើយអតិថិជន\n"
                    "✅ Content staff ប្រើ AI បង្កើតការប្រកាស\n"
                    "✅ Manager ប្រើ AI មើលចំណូល\n\n"
                    "Access account តែមួយ — collaborate ងាយ ។\n\n"
                    "💡 Claude Pro $20/ខែ share team ទាំងអស់ — "
                    "គ្មានការទិញ account ដាច់ ។"
                ),
            },
            "q_data": {
                "label": "🔒 ទិន្នន័យហាងជ្រាបចេញ?",
                "answer": (
                    "🔒 *ទិន្នន័យហាង ជ្រាបចេញ?*\n\n"
                    "NiMo ធានា: ទិន្នន័យរបស់បងមានសុវត្ថិភាព ។\n\n"
                    "✅ ទិន្នន័យជារបស់បង — store ក្នុង account ផ្ទាល់ ។\n\n"
                    "✅ NiMo មិន collect/sell/share ទិន្នន័យ ។\n\n"
                    "✅ Security ស្ដង់ដារ Anthropic (US) — "
                    "ដូច bank ធំ ។\n\n"
                    "ហាងជារបស់បង → ទិន្នន័យជារបស់បង → NiMo មិនទុកអ្វី ❤️"
                ),
            },
            "q_after_warranty": {
                "label": "🤝 ផុតការធានា NiMo ជួយ?",
                "answer": (
                    "🤝 *ផុត 30 ថ្ងៃ NiMo ជួយ?*\n\n"
                    "ការធានា = policy បង្វិលលុយ — ជំនួយ NiMo គ្មានការកំណត់ 😊\n\n"
                    "✅ Telegram NiMo នៅពេលណា — ជួយ ។\n\n"
                    "✅ Community group — រៀនពីម្ចាស់ហាងផ្សេង ។\n\n"
                    "✅ Update ថ្មី — ឥតគិតថ្លៃ ។\n\n"
                    "NiMo មិន abandon ។ ❤️"
                ),
            },
            "q_update": {
                "label": "🆙 មានការ update?",
                "answer": (
                    "🆙 *មាន update/upgrade ថ្ងៃក្រោយ? ថ្លៃ?*\n\n"
                    "Update ជានិច្ច — ឥតគិតថ្លៃ 🎁\n\n"
                    "NiMo upgrade ផ្ អាស់ feedback ម្ចាស់ហាង ។ ពេលមាន:\n\n"
                    "✅ Feature ថ្មី\n"
                    "✅ AI command ប្រសើរ\n"
                    "✅ Speed + effectiveness\n\n"
                    "→ ទទួល update ដោយ group — ដោយ pay ថ្មី ។\n\n"
                    "ទិញម្ដង — upgrade ជារៀងរហូត ។"
                ),
            },
            "q_community": {
                "label": "👥 NiMo មាន community group?",
                "answer": (
                    "👥 *NiMo មាន community group?*\n\n"
                    "មានជាការប្រាកដ 💛\n\n"
                    "ក្រោយទិញ NiMo add ចូល *Telegram community* ។ ទីនោះ:\n\n"
                    "✅ ជួបម្ចាស់ហាងខ្មែរ — ចែករំលែកបទពិសោធ ។\n\n"
                    "✅ រៀន AI ប្រកបដោយប្រសិទ្ធ ។\n\n"
                    "✅ Tips + AI command ថ្មីប្រចាំសប្ដាហ៍ ។\n\n"
                    "✅ ជំនួយ NiMo + community ។\n\n"
                    "បងមិនដែលទៅម្នាក់ ❤️"
                ),
            },
            "q_competitor": {
                "label": "⚔️ គូប្រជែងប្រើ Agent ផង?",
                "answer": (
                    "⚔️ *គូប្រជែងប្រើ — ខ្ញុំនៅ advantage?*\n\n"
                    "ចំលើយ: advantage នៅ — ហើយធំជាង ប្រសិនបើចាប់ផ្ដើមមុន ។\n\n"
                    "─────────\n\n"
                    "*ម្ចាស់ហាងភាគច្រើនកម្ពុជា មិនទាន់ប្រើ AI ។*\n"
                    "រៀងរាល់ថ្ងៃ wait = ថ្ងៃ competitor ទៅ ។\n\n"
                    "─────────\n\n"
                    "*ប្រើ tool ដូចគ្នា ≠ result ដូចគ្នា ។*\n\n"
                    "ហាង 2 ប្រើ tool ដូច — ប៉ុន្តែ:\n"
                    "• ផលិតផល ≠\n"
                    "• Brand style ≠\n"
                    "• Customer approach ≠\n\n"
                    "AI រៀនតាម ហាងបង — គ្មាន copy ។\n\n"
                    "─────────\n\n"
                    "Advantage = ប្រើ *លឿន ប្រសើរ ស្ថិតថេរ* ជាង ។"
                ),
            },
            "q_think": {
                "label": "🤔 សូមទុ្យចិត្តបន្ថែម",
                "answer": (
                    "🤔 *សូមទុ្យចិត្តបន្ថែម*\n\n"
                    "ចំពោះ — ការ ①ចំណ ②ចំណ ③ ③ 😊\n\n"
                    "ប៉ុន្តែ NiMo ចង់ឱ្យបងដឹង 3 ចំណុច:\n\n"
                    "*ទីមួយ — តម្លៃ early bird ។*\n"
                    "ក្រោយ launch ។ ។ ។ តម្លៃ ↑ ។ ទិញថ្ងៃនេះ = best price ។\n\n"
                    "*ទីពីរ — ធានា 30 ថ្ងៃ 100% ។*\n"
                    "= Try ដោយ risk ≈ 0 ។ មិនgood → ប្រាក់ back ។\n\n"
                    "*ទីបី — រៀងរាល់ថ្ងៃ wait = ថ្ងៃ lose ។*\n"
                    "ពេល order បាត់ cơhội ។ ។ ។ ។ ។ ។\n\n"
                    "─────────\n\n"
                    "បងត្រូវ info បន្ថែម? NiMo នៅទីនេះ 😊"
                ),
            },
            "q_try": {
                "label": "🧪 ចង់សាកល្បងមុនទិញ",
                "answer": (
                    "🧪 *ចង់សាកល្បងមុនទិញ*\n\n"
                    "NiMo យល់ 😊\n\n"
                    "ប៉ុន្តែ: Try = result ពិតប្រាកដ នៅ ហាង ពិតប្រាកដ ។\n"
                    "*មិន អាចធ្វើ ដោយ/ចាប់ 'ពិតប្រាកដ ។*\n\n"
                    "─────────\n\n"
                    "ហើយ NiMo មាន *Basic $97* = 'free trial with refund':\n\n"
                    "✅ 5 AI Employees ពេញ\n"
                    "✅ Run ហាងពិតប្រាកដ\n"
                    "✅ Result 30 ថ្ងៃ\n"
                    "✅ ≠good → 100% back\n\n"
                    "─────────\n\n"
                    "*Risk ពិត = continue ម្នាក់ — ខណៈ/ច way ។*"
                ),
            },
            "q_claude_pro": {
                "label": "💳 Claude Pro $20/ខែ ជាអ្វី?",
                "answer": (
                    "💳 *Claude Pro $20/ខែ ជាអ្វី? តម្រូវការ?*\n\n"
                    "Cambodia Biz Agent run លើ Claude AI (Anthropic — US) ។ "
                    "ដើម្បីប្រើ ត្រូវការ Claude Pro *$20/ខែ* — "
                    "ចំណាយ Anthropic ផ្ទាល់ មិន NiMo ។\n\n"
                    "─────────\n\n"
                    "ប៉ុន្តែ cost ពិត:\n\n"
                    "✅ $20/ខែ = 1 employee 24/7 ។\n"
                    "✅ AI Agents ទាំង 5 run account 1 ។\n"
                    "✅ Cancel ពេលណា ។\n\n"
                    "─────────\n\n"
                    "Inbox staff កម្ពុជា = $200–300/ខែ ។\n"
                    "Claude Pro = $20/ខែ ។ *Save $180–280/ខែ ។*"
                ),
            },
            "q_riel": {
                "label": "💵 អាចបង់ជារៀលបាន?",
                "answer": (
                    "💵 *អាចបង់ជារៀល?*\n\n"
                    "បានជាការប្រាកដ! ផ្ទេររៀលធម្មតា — "
                    "ABA convert USD ស្វ័យប្រវត្តិ ។\n\n"
                    "🟦 *Basic $97* ≈ 400,000 Riel\n"
                    "⭐ *Pro $297* ≈ 1,200,000 Riel\n"
                    "🟡 *VIP $597* ≈ 2,400,000 Riel"
                ),
            },
            "q_industry": {
                "label": "🛍️ ហាងខ្ញុំ ≠ tech អាចប្រើ?",
                "answer": (
                    "🛍️ *ហាងខ្ញុំ [food/fashion/beauty]… ប្រើ Agent បាន?*\n\n"
                    "NiMo ឆ្លើយ: *ប្រសិនបើ sell online នៅកម្ពុជា — ប្រើបាន ។*\n\n"
                    "NiMo tested:\n\n"
                    "👗 Fashion & accessories\n"
                    "💄 Beauty & skincare\n"
                    "🍱 Food & specialty\n"
                    "📚 Courses & consulting\n"
                    "💆 Spa, salon, studio\n"
                    "🏠 Furniture & home\n"
                    "🌸 Flowers & gifts\n\n"
                    "AI រៀនតាម ផលិតផល + style ហាង — មិន apply formula rigid ។\n\n"
                    "មិនប្រាកដ? ប្រាប់ niche NiMo — ពិគ្រោះ free 👇"
                ),
            },
            "q_delivery": {
                "label": "📦 ផ្ទេរ​ប្រាក់​ហើយ​ ទទួល​ដូច​ម្ដេច?",
                "answer": (
                    "📦 *ក្រោយផ្ទេរប្រាក់ ទទួលដូចម្ដេច?*\n\n"
                    "ងាយ — 4 ជំហាន:\n\n"
                    "*ជំហាន 1 — ផ្ទេរ*\n"
                    "ជ្រើស package → ផ្ទេរ info NiMo ផ្ដល់\n\n"
                    "*ជំហាន 2 — ផ្ញើ confirm*\n"
                    "Screenshot → ឈ្មោះ + phone + package → ផ្ញើ bot\n\n"
                    "*ជំហាន 3 — NiMo confirm & ផ្ញើ*\n"
                    "NiMo verify + ផ្ញើ product ក្នុង 30 នាទី\n\n"
                    "*ជំហាន 4 — ទទួល + ចាប់ផ្ដើម*\n"
                    "Kit + guide PDF + video + group support 🚀\n\n"
                    "*VIP:* ក្រោយទទួល Kit NiMo ណាត់ Zoom ។"
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "🔍 ស្វែងយល់អំពី Cambodia Biz Agent",
                "questions": ["q_nimo", "q_system", "q_different", "q_save", "q_location"],
            },
            "cat_price": {
                "label": "💰 តម្លៃ & កញ្ចប់",
                "questions": ["q_price", "q_which_plan", "q_worth", "q_warranty"],
            },
            "cat_tech": {
                "label": "🛠️ ការដំឡើង & បច្ចេកវិទ្យា",
                "questions": ["q_tech", "q_time", "q_device", "q_internet", "q_team"],
            },
            "cat_support": {
                "label": "🔒 ការធានា & ជំនួយ",
                "questions": ["q_data", "q_after_warranty", "q_update", "q_community"],
            },
            "cat_doubt": {
                "label": "🤔 នៅតែស្ទាក់ស្ទើរ",
                "questions": ["q_competitor", "q_think", "q_try"],
            },
            "cat_buy": {
                "label": "🛍️ ការទិញ",
                "questions": ["q_claude_pro", "q_riel", "q_industry", "q_delivery"],
            },
        },
        "s": {
            "welcome": (
                "👋 សួស្តី! ខ្ញុំជាជំនួយការរបស់ *NiMo Team*។\n\n"
                "បងមានសំណួរអ្វីអំពី *Cambodia Biz Agent*?\n"
                "ជ្រើសសំណួរខាងក្រោម — ខ្ញុំឆ្លើយភ្លាមៗ 👇"
            ),
            "choose_cat":       "ជ្រើសសំណួរដែលបងចង់ដឹង:",
            "buy_title": (
                "🎉 *ល្អណាស់! បងចង់ជ្រើសកញ្ចប់ណា?*\n\n"
                "🟦 *Basic $97* — សាកល្បងមុន\n"
                "⭐ *Pro $297* — ស្វ័យប្រវត្តិ 24/7\n"
                "🟡 *VIP $597* — NiMo ដំឡើងជំនួស\n\n"
                "ជ្រើសកញ្ចប់ 👇"
            ),
            "buy_btn":          "💳 ខ្ញុំចង់ទិញឥឡូវ",
            "consult_btn":      "💬 សួរ NiMo ដោយផ្ទាល់",
            "back_btn":         "⬅️ ត្រឡប់ទៅម៉ឺនុយ",
            "back_cat":         "⬅️ សំណួរផ្សេងទៀត",
            "unsure_btn":       "🤔 ខ្ញុំមិនទាន់ប្រាកដ — ត្រូវការពិគ្រោះ",
            "consult_msg": (
                f"💬 <b>សួស្តី! NiMo រីករាយជួយបង</b> ❤️\n\n"
                f"ចុចលីងខាងក្រោម ដើម្បីទំនាក់ទំនងផ្ទាល់ជាមួយអ្នកប្រឹក្សា:\n\n"
                f"👉 <a href='https://t.me/{STAFF_USERNAME}'>Chat with NiMo Advisor</a>\n\n"
                f"<i>បន្ទាប់ពីទទួលការប្រឹក្សា សូមត្រឡប់មកទិញដោយប្រើ /start</i> 🛒"
            ),
            "end_consult_btn":  "🔚 បញ្ចប់ — ត្រឡប់ទៅម៉ឺនុយ",
            "end_consult_msg":  "✅ បានបញ្ចប់។ អរគុណបង ❤️\n\nចុច /start ដើម្បីបើកម៉ឺនុយ។",
            "confirm_paid_btn": "✅ ខ្ញុំបានផ្ទេរប្រាក់រួចហើយ",
            "ask_more_btn":     "❓ ខ្ញុំត្រូវការសួរបន្ថែម",
            "view_payment_btn": "💳 មើលព័ត៌មានផ្ទេរប្រាក់",
            "unknown_msg":      "ខ្ញុំទទួលបានសារបងហើយ ❤️\n\nបងចង់:",
            "ask_bill":         "📸 *ជំហានទី 1/3: ផ្ញើរូបភាពបង្កាន់ដៃ*\n\nសូម *ថតអេក្រង់* ការផ្ទេរប្រាក់ 👇",
            "need_photo":       "⚠️ សូមផ្ញើ *រូបភាព* បង្កាន់ដៃ 📸",
            "ask_name":         "✅ ទទួលបានរូបភាពហើយ!\n\n👤 *ជំហានទី 2/3: ឈ្មោះពេញ*\n\nសូមវាយឈ្មោះរបស់បង:",
            "need_text":        "⚠️ សូមវាយជាអក្សរ។",
            "ask_phone":        "✅ ទទួលបានឈ្មោះហើយ!\n\n📱 *ជំហានទី 3/3: លេខទូរស័ព្ទ*\n\nសូមបញ្ចូលលេខទូរស័ព្ទ:",
            "complete_msg": (
                "🎉 *ទទួលបានព័ត៌មានគ្រប់គ្រាន់ហើយ!*\n\n"
                "📋 *សង្ខេបការបញ្ជាទិញ:*\n"
                "• លេខកូដ: `{order_id}`\n"
                "• ឈ្មោះ: {name}\n"
                "• ទូរស័ព្ទ: {phone}\n"
                "• កញ្ចប់: {label} ({price_usd})\n\n"
                "NiMo នឹងពិនិត្យ និងបញ្ជាក់ក្នុង *30 នាទី* ⏰\n\n"
                "អរគុណបងដែលទុកចិត្ត NiMo ❤️"
            ),
            "package_msg": (
                "🎉 *បងបានជ្រើស {label} — {price_usd}* ({price_riel})\n\n"
                "📲 *សូម Scan QR ABA ខាងលើ ដើម្បីបង់ប្រាក់*\n\n"
                "💵 *ចំនួនទឹកប្រាក់: {price_usd}*\n\n"
                "បន្ទាប់ពីផ្ទេរប្រាក់ហើយ សូមចុចប៊ូតុងខាងក្រោម 👇"
            ),
        },
    },

    "en": {
        "faq": {
            "q_nimo": {
                "label": "👤 Who is NiMo?",
                "answer": (
                    "👤 *Who is NiMo?*\n\n"
                    "NiMo was created from a simple desire:\n\n"
                    "_To contribute something meaningful to the business community in Cambodia._\n\n"
                    "While neighboring countries have used AI to automate businesses for years — "
                    "many business owners in Cambodia are still doing everything manually every day. "
                    "Not because they don't want to change — but because no tool has truly fit them.\n\n"
                    "NiMo was born to bridge that gap — "
                    "helping Cambodian shop owners access AI practically, easily, in their own language."
                ),
            },
            "q_system": {
                "label": "💬 I don't understand how this system works",
                "answer": (
                    "💬 *How does Cambodia Biz Agent work?*\n\n"
                    "Simply put: you get *5 AI Employees* — each does 1 job:\n\n"
                    "🔍 Market research & competitor analysis\n"
                    "📣 Create content for FB/TikTok/Instagram\n"
                    "💰 Write sales pages & close orders\n"
                    "📦 Auto-receive orders & send delivery notifications\n"
                    "📊 Revenue reports & weekly optimization\n\n"
                    "You give commands in Khmer or English — AI works instantly.\n\n"
                    "No coding needed. 🚀"
                ),
            },
            "q_different": {
                "label": "🆚 How is this different from other AI agents?",
                "answer": (
                    "🆚 *How is Cambodia Biz Agent different from other agents?*\n\n"
                    "Most AI Agents are built for Western markets — "
                    "English, Stripe payments, US/EU business styles.\n\n"
                    "*Cambodia Biz Agent is different: built specifically for Cambodian business owners.*\n\n"
                    "🇰🇭 *Language:* Natural Khmer — not machine translation\n\n"
                    "💳 *Payments:* ABA Pay, Wing Money, Bakong KHQR — no international card needed\n\n"
                    "📱 *Platforms:* Facebook, TikTok, Telegram — where Cambodian customers buy\n\n"
                    "🤝 *Support:* NiMo is based in Cambodia, understands the market, gives direct support\n\n"
                    "Built from the real realities of this market — not copied from elsewhere."
                ),
            },
            "q_save": {
                "label": "💰 What will I save?",
                "answer": (
                    "💰 *What specifically will I save?*\n\n"
                    "What you save most — not money. *Time.*\n\n"
                    "Average shop owners spend ~3 hours/day on repetitive tasks: "
                    "writing captions, replying messages, posting, compiling orders.\n\n"
                    "*3 hours × 30 days = 90 hours/month* — Cambodia Biz Agent handles all that.\n\n"
                    "─────────\n\n"
                    "On money — real numbers:\n\n"
                    "🔍 Market research: $100–200/time\n"
                    "📣 Content writing: $50–150/month\n"
                    "💬 Order closing: $200–300/month\n"
                    "📦 Order processing: $150–250/month\n"
                    "📊 Reporting: $100–200/month\n\n"
                    "*Hiring people: ~$700–1,200/month*\n\n"
                    "Cambodia Biz Agent: one-time only\n"
                    "🟦 Basic $97 · ⭐ Pro $297 · 🟡 VIP $597\n\n"
                    "Year 1: save *$8,000–14,000* compared to hiring 💰"
                ),
            },
            "q_location": {
                "label": "🏢 Where is NiMo's office?",
                "answer": (
                    "🏢 *Where is NiMo's office?*\n\n"
                    "NiMo operates fully online — no physical office. "
                    "This is a modern digital business model, like buying an app or online course "
                    "— you don't need to know where the office is to use it.\n\n"
                    "What matters more than an address: NiMo offers a *30-day 100% money-back guarantee* "
                    "if you're not satisfied. That's a clearer commitment than any address. ❤️"
                ),
            },
            "q_price": {
                "label": "💵 How much does Cambodia Biz Agent cost?",
                "answer": (
                    "💵 *How much does Cambodia Biz Agent cost? Monthly fees?*\n\n"
                    "Buy once — use forever. 3 plans to choose from:\n\n"
                    "🟦 *Basic $97* (≈ 400,000 Riel)\n"
                    "First-time trial — lowest risk\n\n"
                    "⭐ *Pro $297* (≈ 1,200,000 Riel)\n"
                    "Full automation 24/7\n\n"
                    "🟡 *VIP $597* (≈ 2,400,000 Riel)\n"
                    "NiMo installs directly via Zoom — done and ready to use immediately\n\n"
                    "─────────\n\n"
                    "Only ongoing cost: Claude Pro account ~$20/month.\n\n"
                    "*No hidden fees. No renewals. No surprises.*"
                ),
            },
            "q_which_plan": {
                "label": "🤔 I don't know which plan fits me",
                "answer": (
                    "🤔 *Which plan fits your shop?*\n\n"
                    "🟦 *Basic $97* — New to AI, want to try first\n"
                    "→ 5 AI Employees + Khmer guide + 30-day support\n\n"
                    "⭐ *Pro $297* — Shop running, want full automation 24/7\n"
                    "→ Chatbot + auto-post + auto-booking\n\n"
                    "🟡 *VIP $597* — Don't want to install yourself\n"
                    "→ NiMo installs everything, ready to use, 90-day support\n\n"
                    "Not sure? Tell NiMo about your shop — we'll recommend the right plan in 5 mins 👇"
                ),
            },
            "q_worth": {
                "label": "💎 Is $297 worth it?",
                "answer": (
                    "💎 *Is $297 (or whatever I spend) worth it?*\n\n"
                    "Let the numbers answer.\n\n"
                    "*Inbox staff in Cambodia:* $200–300/month\n"
                    "→ 8 hours/day. Takes holidays. Asks for raises. Gets sick.\n\n"
                    "*Cambodia Biz Agent Pro $297* — one-time\n"
                    "→ 24/7. No holidays. No raises. Never quits.\n\n"
                    "─────────\n\n"
                    "$297 = less than one month of inbox staff.\n\n"
                    "But Cambodia Biz Agent works for you *forever*.\n\n"
                    "─────────\n\n"
                    "If AI helps you close just *5 extra orders/month* — $297 already paid for itself."
                ),
            },
            "q_warranty": {
                "label": "🛡️ Is there a warranty / refund policy?",
                "answer": (
                    "🛡️ *Is there a warranty? Can I get a refund?*\n\n"
                    "Yes — and NiMo is confident about this.\n\n"
                    "*30-day guarantee — 100% refund, no questions asked.*\n\n"
                    "Buy Cambodia Biz Agent. Follow the guide for 30 days. "
                    "If the system doesn't work as NiMo described — "
                    "message NiMo on Telegram. Refund within 24 hours.\n\n"
                    "─────────\n\n"
                    "*The risk is on NiMo. Not on you.* ❤️"
                ),
            },
            "q_tech": {
                "label": "😰 I'm afraid I can't install it",
                "answer": (
                    "😰 *Not tech-savvy — can I still install it?*\n\n"
                    "Yes! Here's why:\n\n"
                    "✅ Step-by-step guide in Khmer with images\n"
                    "✅ Video tutorials to follow\n"
                    "✅ Bot support 24/7\n"
                    "✅ NiMo personally answers when needed\n\n"
                    "VIP plan: NiMo installs it with you via Zoom in 2 hours — "
                    "you just watch and click. 🎯"
                ),
            },
            "q_time": {
                "label": "⏰ How long does setup take?",
                "answer": (
                    "⏰ *How long before I can start using it?*\n\n"
                    "*Basic & Pro:* Self-install following the guide ~2–3 hours — "
                    "do it in the evening or when free, no need to stop selling. "
                    "Day 2 you can create content. Day 3 the system runs on its own.\n\n"
                    "*VIP:* Just 1 Zoom session 2 hours with NiMo — "
                    "you watch, NiMo does everything, tests and hands over. Done.\n\n"
                    "Many NiMo customers buy in the morning — by evening they already have their first content to post 🚀"
                ),
            },
            "q_device": {
                "label": "📱 What devices do I need?",
                "answer": (
                    "📱 *What devices do I need to use this?*\n\n"
                    "Both computer and smartphone work — use whatever you have 😊\n\n"
                    "💻 *Computer:* Recommended for initial setup and viewing reports — bigger screen is easier.\n\n"
                    "📱 *Smartphone only:* After NiMo helps with setup, you can run everything by phone — "
                    "reply to customers, post content, check revenue, all on app.\n\n"
                    "If it can scroll Facebook smoothly — it can run Cambodia Biz Agent. No upgrades needed."
                ),
            },
            "q_internet": {
                "label": "🌐 Do I need fast internet?",
                "answer": (
                    "🌐 *Do I need high-speed internet?*\n\n"
                    "No — just internet good enough for Facebook and Telegram.\n\n"
                    "Home WiFi or 4G both work fine. The system runs on cloud servers — "
                    "your device only needs to send commands, not do heavy processing 🚀"
                ),
            },
            "q_team": {
                "label": "👥 Can my staff use it too?",
                "answer": (
                    "👥 *Can my shop staff use it together?*\n\n"
                    "Absolutely! NiMo designed Cambodia Biz Agent for the whole shop — not just one person 😊\n\n"
                    "✅ Inbox staff use AI to reply customers faster\n"
                    "✅ Content staff use AI to create daily posts\n"
                    "✅ Managers use AI to view revenue reports\n\n"
                    "Everyone accesses one account — easy collaboration, no user limit.\n\n"
                    "💡 Claude Pro $20/month can be shared across the whole team — split the cost, no need for individual accounts."
                ),
            },
            "q_data": {
                "label": "🔒 Will my shop data be leaked?",
                "answer": (
                    "🔒 *Will my shop data be leaked?*\n\n"
                    "NiMo understands your concern — and here's NiMo's clear commitment: your data is completely safe.\n\n"
                    "✅ *Your data belongs to you:* Customers, orders, messages — all stored in your own account, no one else can access.\n\n"
                    "✅ *NiMo doesn't touch your shop data:* NiMo doesn't collect, sell, or share your data with anyone.\n\n"
                    "✅ *International security standards:* Built on Anthropic's platform (US) — same security standard as banks.\n\n"
                    "Your shop → your data → your control. NiMo keeps nothing. ❤️"
                ),
            },
            "q_after_warranty": {
                "label": "🤝 What happens after the warranty?",
                "answer": (
                    "🤝 *What support after the 30-day warranty?*\n\n"
                    "The 30-day warranty is just the refund policy — NiMo supports you with no time limit 😊\n\n"
                    "✅ Message NiMo on Telegram anytime — bugs, advice, optimization, NiMo is there.\n\n"
                    "✅ Join community group — learn from other shop owners using Cambodia Biz Agent.\n\n"
                    "✅ Receive updates when NiMo upgrades the system — completely free.\n\n"
                    "NiMo sells you the system — but doesn't abandon you after receiving payment. ❤️"
                ),
            },
            "q_update": {
                "label": "🆙 Are there updates?",
                "answer": (
                    "🆙 *Are there future updates/upgrades? Do they cost extra?*\n\n"
                    "Regular updates — completely free for existing customers 🎁\n\n"
                    "NiMo continually improves Cambodia Biz Agent based on real feedback. When there are:\n\n"
                    "✅ New features\n"
                    "✅ Better AI commands\n"
                    "✅ Speed & effectiveness improvements\n\n"
                    "→ You receive updates automatically via group, no extra payment.\n\n"
                    "Buy once — get upgraded forever."
                ),
            },
            "q_community": {
                "label": "👥 Is there a community group?",
                "answer": (
                    "👥 *Does NiMo have a community group?*\n\n"
                    "Yes! This is one of the values NiMo is most proud of 💛\n\n"
                    "After purchasing, NiMo adds you to a *private Telegram community* where you:\n\n"
                    "✅ Meet other Cambodian shop owners — share real daily experiences.\n\n"
                    "✅ Learn more effective AI usage from those who went before.\n\n"
                    "✅ Receive new tips & AI commands NiMo updates weekly.\n\n"
                    "✅ Get quick answers — NiMo and community are ready to help.\n\n"
                    "You never go alone — the whole community goes with you ❤️"
                ),
            },
            "q_competitor": {
                "label": "⚔️ What if competitors use it too?",
                "answer": (
                    "⚔️ *If competitors use it too, do I still have an advantage?*\n\n"
                    "Yes — even a bigger advantage if you start earlier.\n\n"
                    "─────────\n\n"
                    "*Right now most Cambodian shop owners don't use AI.* "
                    "Every day you wait is a day competitors get ahead.\n\n"
                    "─────────\n\n"
                    "*Same tool ≠ same results.*\n\n"
                    "Two shops using Cambodia Biz Agent — but:\n"
                    "• Different products\n"
                    "• Different brand styles\n"
                    "• Different customer approaches\n\n"
                    "AI learns your shop's specific characteristics — nobody has an exact copy.\n\n"
                    "─────────\n\n"
                    "Real advantage = using the tool *earlier, better, more consistently*."
                ),
            },
            "q_think": {
                "label": "🤔 Let me think about it",
                "answer": (
                    "🤔 *Let me think about it*\n\n"
                    "Of course — this is a business decision 😊\n\n"
                    "But before thinking, 3 things NiMo wants you to know:\n\n"
                    "*One — Current price is early bird.*\n"
                    "After launch, price goes up. Buying today = best price.\n\n"
                    "*Two — 30-day 100% money-back guarantee.*\n"
                    "You're trying with virtually zero real risk. Not happy → refund.\n\n"
                    "*Three — Every day you wait is a day lost.*\n"
                    "Not money — but time, orders, opportunities. Those can't be refunded.\n\n"
                    "─────────\n\n"
                    "Need more info to decide? NiMo is here 😊"
                ),
            },
            "q_try": {
                "label": "🧪 I want to try before buying",
                "answer": (
                    "🧪 *I want to try before buying*\n\n"
                    "NiMo understands — and doesn't blame that 😊\n\n"
                    "But think: trying before buying means you want real results, on your real shop, with your real products.\n\n"
                    "*There's no way to do that without actually starting.*\n\n"
                    "─────────\n\n"
                    "That's why NiMo has *Basic $97* — this is essentially a \"try with refund\" option:\n\n"
                    "✅ Full 5 AI Employees experience\n"
                    "✅ Run on your real shop\n"
                    "✅ See real results in 30 days\n"
                    "✅ Not satisfied → 100% refund\n\n"
                    "─────────\n\n"
                    "*The real risk isn't buying. The real risk is continuing alone — when there's another way.*"
                ),
            },
            "q_claude_pro": {
                "label": "💳 What is Claude Pro $20/month?",
                "answer": (
                    "💳 *What is Claude Pro $20/month? Is it required?*\n\n"
                    "Cambodia Biz Agent runs on Claude AI (by Anthropic — US). "
                    "To use it, you need a Claude Pro account at *$20/month* — "
                    "paid directly to Anthropic, not through NiMo.\n\n"
                    "─────────\n\n"
                    "But look at the real cost:\n\n"
                    "✅ $20/month = 1 employee working 24/7, no holidays, no raises\n"
                    "✅ All 5 AI Agents run on 1 account — whole team shares\n"
                    "✅ Cancel anytime — no commitment\n\n"
                    "─────────\n\n"
                    "Inbox staff in Cambodia = $200–300/month.\n"
                    "Claude Pro = $20/month. *Save $180–280 every month.*"
                ),
            },
            "q_riel": {
                "label": "💵 Can I pay in Riel?",
                "answer": (
                    "💵 *Can I pay in Riel?*\n\n"
                    "Yes! Transfer in Riel normally — "
                    "ABA Bank automatically converts to USD.\n\n"
                    "🟦 *Basic $97* ≈ 400,000 Riel\n"
                    "⭐ *Pro $297* ≈ 1,200,000 Riel\n"
                    "🟡 *VIP $597* ≈ 2,400,000 Riel"
                ),
            },
            "q_industry": {
                "label": "🛍️ Does my business type work?",
                "answer": (
                    "🛍️ *I sell [food/beauty/fashion/services]… will it work?*\n\n"
                    "NiMo's short answer: *if you sell online in Cambodia, your shop works.*\n\n"
                    "NiMo has tested Cambodia Biz Agent across many industries:\n\n"
                    "👗 Fashion & accessories\n"
                    "💄 Beauty & skincare\n"
                    "🍱 Food & specialty\n"
                    "📚 Courses & consulting\n"
                    "💆 Spa, salon, studio\n"
                    "🏠 Furniture & home goods\n"
                    "🌸 Flowers & gifts\n\n"
                    "AI learns according to your shop's products and style — not a rigid formula.\n\n"
                    "Not sure? Tell NiMo your specific industry — free consultation 👇"
                ),
            },
            "q_delivery": {
                "label": "📦 How do I receive after paying?",
                "answer": (
                    "📦 *After transferring, how do I receive the product?*\n\n"
                    "Simple — just 4 steps:\n\n"
                    "*Step 1 — Transfer*\n"
                    "Choose a plan → transfer to the info NiMo provides\n\n"
                    "*Step 2 — Send confirmation*\n"
                    "Screenshot the transfer → send with name + phone + chosen plan to bot\n\n"
                    "*Step 3 — NiMo confirms & delivers*\n"
                    "NiMo verifies and sends the full product within 30 minutes\n\n"
                    "*Step 4 — Receive & begin*\n"
                    "Get the Kit + guide PDF + videos + support group — start setup 🚀\n\n"
                    "*VIP:* After receiving the Kit, NiMo contacts you to schedule a Zoom session."
                ),
            },
        },
        "cats": {
            "cat_intro": {
                "label": "🔍 Learn about Cambodia Biz Agent",
                "questions": ["q_nimo", "q_system", "q_different", "q_save", "q_location"],
            },
            "cat_price": {
                "label": "💰 Pricing & Plans",
                "questions": ["q_price", "q_which_plan", "q_worth", "q_warranty"],
            },
            "cat_tech": {
                "label": "🛠️ Setup & Technology",
                "questions": ["q_tech", "q_time", "q_device", "q_internet", "q_team"],
            },
            "cat_support": {
                "label": "🔒 Warranty & Support",
                "questions": ["q_data", "q_after_warranty", "q_update", "q_community"],
            },
            "cat_doubt": {
                "label": "🤔 Still Hesitating",
                "questions": ["q_competitor", "q_think", "q_try"],
            },
            "cat_buy": {
                "label": "🛍️ Buying",
                "questions": ["q_claude_pro", "q_riel", "q_industry", "q_delivery"],
            },
        },
        "s": {
            "welcome": (
                "👋 Hello! I'm the assistant of *NiMo Team*.\n\n"
                "What are you wondering about *Cambodia Biz Agent*?\n"
                "Choose a question below — I'll answer right away 👇"
            ),
            "choose_cat":       "Choose a question:",
            "buy_title": (
                "🎉 *Great! Which plan do you want?*\n\n"
                "🟦 *Basic $97* — Try it first\n"
                "⭐ *Pro $297* — Full automation 24/7\n"
                "🟡 *VIP $597* — NiMo installs it for you\n\n"
                "Choose a plan 👇"
            ),
            "buy_btn":          "💳 I WANT TO BUY NOW",
            "consult_btn":      "💬 Chat directly with NiMo",
            "back_btn":         "⬅️ Back to main menu",
            "back_cat":         "⬅️ Other questions",
            "unsure_btn":       "🤔 I'm not sure — need advice",
            "consult_msg": (
                f"💬 <b>Hi! NiMo is happy to help you</b> ❤️\n\n"
                f"Click the link below to chat directly with our advisor:\n\n"
                f"👉 <a href='https://t.me/{STAFF_USERNAME}'>Chat with NiMo Advisor</a>\n\n"
                f"<i>After consulting, come back here to place your order with /start</i> 🛒"
            ),
            "end_consult_btn":  "🔚 End consultation — back to menu",
            "end_consult_msg":  "✅ Consultation ended. Thank you ❤️\n\nType /start to open the menu again.",
            "confirm_paid_btn": "✅ I have transferred — send receipt",
            "ask_more_btn":     "❓ I have more questions",
            "view_payment_btn": "💳 View payment details",
            "unknown_msg":      "I received your message ❤️\n\nWhat would you like to do?",
            "ask_bill":         "📸 *Step 1/3: Send payment receipt*\n\nPlease *screenshot* the bank transfer confirmation 👇",
            "need_photo":       "⚠️ Please send a *photo* of your receipt 📸",
            "ask_name":         "✅ Receipt received!\n\n👤 *Step 2/3: Full name*\n\nPlease enter your full name:",
            "need_text":        "⚠️ Please enter text.",
            "ask_phone":        "✅ Name received!\n\n📱 *Step 3/3: Phone number*\n\nPlease enter your phone number:",
            "complete_msg": (
                "🎉 *All information received!*\n\n"
                "📋 *Order summary:*\n"
                "• Order ID: `{order_id}`\n"
                "• Name: {name}\n"
                "• Phone: {phone}\n"
                "• Plan: {label} ({price_usd})\n\n"
                "NiMo will verify and confirm within *30 minutes* ⏰\n\n"
                "Thank you for trusting NiMo ❤️"
            ),
            "package_msg": (
                "🎉 *You selected {label} — {price_usd}* ({price_riel})\n\n"
                "📲 *Scan the ABA QR code above to pay*\n\n"
                "💵 *Amount: {price_usd}*\n\n"
                "After transferring, tap the button below to send your receipt 👇"
            ),
        },
    },
}

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def get_lang(context) -> str:
    return context.user_data.get("lang", "km")

def C(context):
    return CONTENT[get_lang(context)]

# ─── KEYBOARDS ───────────────────────────────────────────────────────────────

def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇰🇭 ភាសាខ្មែរ", callback_data="lang_km"),
        InlineKeyboardButton("🇬🇧 English",    callback_data="lang_en"),
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
        [InlineKeyboardButton("🟦 Basic $97  (≈ 400,000 Riel)",   callback_data="buy_basic")],
        [InlineKeyboardButton("⭐ Pro $297   (≈ 1,200,000 Riel)", callback_data="buy_pro")],
        [InlineKeyboardButton("🟡 VIP $597  (≈ 2,400,000 Riel)",  callback_data="buy_vip")],
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

# ─── HANDLERS ────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🇰🇭 ជ្រើសភាសា  |  🇬🇧 Choose language:",
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
            parse_mode="HTML",
            reply_markup=end_consult_keyboard(context)
        )
        user = query.from_user
        if ADMIN_ID and user.id != ADMIN_ID:
            lang = get_lang(context)
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=(
                        f"💬 *Khách cần tư vấn [{lang.upper()}]*\n"
                        f"👤 {user.full_name} (@{user.username or 'no username'})\n"
                        f"`#cid:{user.id}`"
                    ),
                    parse_mode="Markdown"
                )
            except Exception as e:
                logging.error(f"Admin notify error: {e}")
            # Ghi vào Sheet CRM
            asyncio.create_task(_post_to_sheet({
                "name":     user.full_name,
                "telegram": f"@{user.username}" if user.username else str(user.id),
                "cid":      str(user.id),
                "source":   "consult-request",
                "lang":     lang
            }))
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

# ─── MESSAGE HANDLER ─────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    awaiting   = context.user_data.get("awaiting")
    consulting = context.user_data.get("consulting", False)
    user       = update.effective_user
    s          = C(context)["s"]

    # Admin reply → forward to customer
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
                text=f"💬 *NiMo:*\n\n{update.message.text}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("✅ Sent.")
        except Exception as e:
            await update.message.reply_text(f"❌ {e}")
        return

    # Consulting mode → forward to admin
    if consulting and not awaiting:
        text = update.message.text or "(media)"
        if ADMIN_ID:
            try:
                fwd = (
                    f"💬 *{user.full_name}* (@{user.username or 'no username'})\n"
                    f"━━━━━━━━━━━━━\n{text}\n━━━━━━━━━━━━━\n`#cid:{user.id}`"
                )
                await context.bot.send_message(chat_id=ADMIN_ID, text=fwd, parse_mode="Markdown")
                if update.message.photo:
                    await context.bot.send_photo(
                        chat_id=ADMIN_ID,
                        photo=update.message.photo[-1].file_id,
                        caption=f"📸 {user.full_name}\n`#cid:{user.id}`",
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logging.error(f"Forward error: {e}")
        await update.message.reply_text("✅", reply_markup=end_consult_keyboard(context))
        return

    # No active flow → show options
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

        # OCR: extract APV from bill screenshot and match against PayWay store
        apv_info = None
        if ANTHROPIC_API_KEY:
            lang = get_lang(context)
            checking_msg = "🔍 កំពុងផ្ទៀងផ្ទាត់ការបង់ប្រាក់..." if lang == "km" else "🔍 Verifying payment..."
            checking = await update.message.reply_text(checking_msg)
            try:
                photo_file  = await update.message.photo[-1].get_file()
                photo_bytes = bytes(await photo_file.download_as_bytearray())
                ocr_apv     = await _ocr_bill_image(photo_bytes)
                if ocr_apv and ocr_apv in _apv_store:
                    apv_info = _apv_store.pop(ocr_apv)
                    context.user_data["apv_verified"] = True
                    context.user_data["apv_code"]     = ocr_apv
                    context.user_data["apv_amount"]   = apv_info["amount"]
                    logging.info(f"APV {ocr_apv} matched for user {user.id}")
                else:
                    context.user_data["apv_verified"] = False
                    logging.info(f"OCR APV={ocr_apv!r} not found in store for user {user.id}")
            except Exception as e:
                logging.error(f"OCR bill error: {e}")
                context.user_data["apv_verified"] = False
            try:
                await checking.delete()
            except Exception:
                pass

        context.user_data["awaiting"] = "name"
        if apv_info:
            lang = get_lang(context)
            verified_prefix = (
                "✅ *ការបង់ប្រាក់ត្រូវបានផ្ទៀងផ្ទាត់! 🎉*\n\n"
                if lang == "km" else
                "✅ *Payment verified! 🎉*\n\n"
            )
            await update.message.reply_text(verified_prefix + s["ask_name"], parse_mode="Markdown")
        else:
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

    # Phone step → complete
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

        # Ghi đơn vào Google Sheet CRM
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
            lang         = get_lang(context)
            apv_verified = context.user_data.get("apv_verified", False)
            apv_code     = context.user_data.get("apv_code", "")
            apv_line     = (
                f"✅ *APV {apv_code} — PAYMENT VERIFIED*\n"
                if apv_verified else
                "⚠️ *APV not matched — manual check needed*\n"
            )
            msg  = (
                f"🔴 *ĐƠN MỚI [{lang.upper()}]*\n\n"
                f"{apv_line}\n"
                f"📋 Mã đơn: `{context.user_data['order_id']}`\n"
                f"👤 Tên: {context.user_data['name']}\n"
                f"📱 SĐT: {context.user_data['phone']}\n"
                f"📦 Gói: *{info['label']}* — {info['price_usd']}\n"
                f"🆔 Telegram ID: `{user.id}`\n\n"
                f"👉 Lệnh xác nhận:\n"
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

# ─── ADMIN COMMANDS ──────────────────────────────────────────────────────────

async def xacnhan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Syntax: `/xacnhan NIMO-ID package`", parse_mode="Markdown")
        return
    await update.message.reply_text(
        f"✅ Confirmed order `{context.args[0]}` — plan `{context.args[1]}`.\n"
        "_Auto-delivery will be added in the next step._",
        parse_mode="Markdown"
    )

async def tra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin replies to customer: /tra <customer_id> <message>"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Syntax: `/tra <customer_id> <message>`", parse_mode="Markdown")
        return
    try:
        cid  = int(context.args[0])
        text = " ".join(context.args[1:])
        await context.bot.send_message(
            chat_id=cid,
            text=f"💬 *NiMo:*\n\n{text}",
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Sent.")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("xacnhan", xacnhan))
    app.add_handler(CommandHandler("tra",     tra))
    app.add_handler(CallbackQueryHandler(handle_callback))
    # Group handler: captures PayWay APV notifications from DONE Money group
    app.add_handler(MessageHandler(
        filters.ChatType.GROUPS & (filters.TEXT | filters.CAPTION),
        handle_group_message
    ))
    # Private chat handler: buy flow + FAQ + consulting
    app.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & (filters.PHOTO | filters.TEXT & ~filters.COMMAND),
        handle_message
    ))
    print("✅ Bot (KM + EN) đang chạy... /start để test!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
