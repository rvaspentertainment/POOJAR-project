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


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    await message.reply(hi)




@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    


import os
from pyrogram import Client, filters
from pyrogram.types import Message
from gtts import gTTS
from langdetect import detect



# Mapping detected languages to gTTS supported languages
LANGUAGE_MAP = {
    "kn": "kn",  # Kannada
    "en": "en",  # English
    "hi": "hi",  # Hindi
    "ta": "ta",  # Tamil
    "te": "te",  # Telugu
    "mr": "mr",  # Marathi
    "bn": "bn",  # Bengali
    "gu": "gu",  # Gujarati
    "pa": "pa",  # Punjabi
    "ml": "ml",  # Malayalam
    "or": "or",  # Odia
    "ur": "ur",  # Urdu
    "as": "as",  # Assamese
    "sa": "sa"   # Sanskrit
}



# Text Message Handler
@Client.on_message(filters.text)
async def handle_text(client, message: Message):
    text = message.text
    try:
        detected_lang = detect(text)
        lang_code = LANGUAGE_MAP.get(detected_lang, "en")  # Default to English if unsupported
        
        tts = gTTS(text, lang=lang_code)
        file_path = f"tts_{message.chat.id}.mp3"
        tts.save(file_path)
        await message.reply_voice(voice=file_path, caption=f"Detected language: {detected_lang} ({lang_code})\nHere is your audio!")
        os.remove(file_path)
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
