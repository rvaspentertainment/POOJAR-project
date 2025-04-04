# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import logging
import random
import asyncio
from validators import domain
from Script import script
from plugins.dbusers import db
from pyrogram import Client, filters, enums
from plugins.users_api import get_user, update_user_info
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from utils import verify_user, check_token, check_verification, get_token
from config import *
import re
import json
import base64
from urllib.parse import quote_plus
from TechVJ.utils.file_properties import get_name, get_hash, get_media_file_size
logger = logging.getLogger(__name__)

BATCH_FILES = {}

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def formate_file_name(file_name):
    chars = ["[", "]", "(", ")"]
    for c in chars:
        file_name.replace(c, "")
    file_name = '@VJ_Botz ' + ' '.join(filter(lambda x: not x.startswith('http') and not x.startswith('@') and not x.startswith('www.'), file_name.split()))
    return file_name

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ0




@Client.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("Send me any text, and I'll convert it to speech using detected language(s)!")


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from gtts import gTTS
from langdetect import detect
import os
import random
import string
import subprocess

# MANUAL LANGUAGES
_langs = {
    "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali",
    "bs": "Bosnian", "ca": "Catalan", "cs": "Czech", "cy": "Welsh", "da": "Danish",
    "de": "German", "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian",
    "eu": "Basque", "fi": "Finnish", "fr": "French", "fr-CA": "French (Canada)", "gl": "Galician",
    "gu": "Gujarati", "ha": "Hausa", "hi": "Hindi", "hr": "Croatian", "hu": "Hungarian",
    "id": "Indonesian", "is": "Icelandic", "it": "Italian", "iw": "Hebrew", "ja": "Japanese",
    "jw": "Javanese", "km": "Khmer", "kn": "Kannada", "ko": "Korean", "la": "Latin",
    "lt": "Lithuanian", "lv": "Latvian", "ml": "Malayalam", "mr": "Marathi", "ms": "Malay",
    "my": "Myanmar (Burmese)", "ne": "Nepali", "nl": "Dutch", "no": "Norwegian", "pa": "Punjabi (Gurmukhi)",
    "pl": "Polish", "pt": "Portuguese (Brazil)", "pt-PT": "Portuguese (Portugal)", "ro": "Romanian",
    "ru": "Russian", "si": "Sinhala", "sk": "Slovak", "sq": "Albanian", "sr": "Serbian",
    "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", "ta": "Tamil", "te": "Telugu",
    "th": "Thai", "tl": "Filipino", "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu",
    "vi": "Vietnamese", "yue": "Cantonese", "zh-CN": "Chinese (Simplified)", "zh-TW": "Chinese (Traditional)"
}


def progress_bar(pct):
    filled = int(pct / 10)
    symbol = random.choice([("⚫", "⚪"), ("❤", "💛")])
    return f"{symbol[0]*filled}{symbol[1]*(10-filled)} {pct}%"

# /start and /help

@Client.on_message(filters.command("help"))
async def help(_, m: Message):
    await m.reply(
        "**Text-to-Speech Help**\n\n"
        "1. Send me any text.\n"
        "2. I detect the language.\n"
        "3. You confirm or pick a new one.\n"
        "4. Choose voice speed.\n"
        "5. I send back the audio!\n\n"
        "Supported Languages:\n" + ", ".join([f"`{k}`" for k in _langs.keys()])
    )

@Client.on_message(filters.text)
async def tts_detect_language(_, m: Message):
    try:
        text = m.text
        lang = detect(text)
        lang_name = _langs.get(lang, lang)
        await m.reply(
            f"Detected language: **{lang_name}** (`{lang}`)\nIs this correct?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Yes", callback_data=f"yes|{lang}|{text}")],
                [InlineKeyboardButton("❌ No", callback_data=f"no|{text}")]
            ])
        )
    except Exception as e:
        await m.reply(f"Error: {e}")

@Client.on_callback_query(filters.regex("^no\\|"))
async def choose_language(_, c: CallbackQuery):
    _, text = c.data.split("|", 1)
    buttons = [[InlineKeyboardButton(name, callback_data=f"lang|{code}|{text}")]
               for code, name in list(_langs.items())[:100]]
    await c.message.reply("Choose your language:", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^lang\\|"))
async def after_language(_, c: CallbackQuery):
    _, lang, text = c.data.split("|", 2)
    await c.message.reply("Select voice speed:", reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐢 Slow", callback_data=f"speed|{lang}|slow|{text}"),
            InlineKeyboardButton("🚶 Medium", callback_data=f"speed|{lang}|medium|{text}"),
            InlineKeyboardButton("⚡ Fast", callback_data=f"speed|{lang}|fast|{text}")
        ]
    ]))

@Client.on_callback_query(filters.regex("^yes\\|"))
async def confirm_detected_lang(_, c: CallbackQuery):
    _, lang, text = c.data.split("|", 2)
    await c.message.reply("Select voice speed:", reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐢 Slow", callback_data=f"speed|{lang}|slow|{text}"),
            InlineKeyboardButton("🚶 Medium", callback_data=f"speed|{lang}|medium|{text}"),
            InlineKeyboardButton("⚡ Fast", callback_data=f"speed|{lang}|fast|{text}")
        ]
    ]))

@Client.on_callback_query(filters.regex("^speed\\|"))
async def generate_audio(_, c: CallbackQuery):
    try:
        _, lang, speed, text = c.data.split("|", 3)
        tld_speed = {"slow": True, "medium": False, "fast": False}
        pct = 30
        prog = await c.message.reply(f"{progress_bar(pct)} Generating voice...")
        tts = gTTS(text=text, lang=lang, slow=tld_speed[speed])
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        filepath = f"audios/{filename}.mp3"
        tts.save(filepath)

        output = f"audios/{filename}.ogg"
        await prog.edit(f"{progress_bar(70)} Converting to OGG format...")
        subprocess.run(["ffmpeg", "-i", filepath, "-c:a", "libopus", output, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        await bot.send_voice(
            c.message.chat.id,
            voice=output,
            caption=f"**Language**: `{lang}`\n**Chars**: {len(text)}\n**Speed**: {speed.title()}"
        )

        await prog.edit(progress_bar(100) + " Done!")

        os.remove(filepath)
        os.remove(output)
    except Exception as e:
        await c.message.reply(f"An error occurred: {e}")

