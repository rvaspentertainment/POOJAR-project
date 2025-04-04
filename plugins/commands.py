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





import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment


# Create directory for audio
VOICE_DIR = "voices"
os.makedirs(VOICE_DIR, exist_ok=True)

user_texts = {}

def split_by_language(text):
    words = text.split()
    segments = []
    current_lang = None
    current_segment = []

    for word in words:
        try:
            lang = detect(word)
        except:
            lang = 'en'
        if lang != current_lang:
            if current_segment:
                segments.append((' '.join(current_segment), current_lang))
            current_segment = [word]
            current_lang = lang
        else:
            current_segment.append(word)
    if current_segment:
        segments.append((' '.join(current_segment), current_lang))
    return segments



@Client.on_message(filters.text)
async def text_handler(client, message: Message):
    user_texts[message.chat.id] = message.text
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Generate Audio", callback_data="generate")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ])
    await message.reply_text("Choose an action:", reply_markup=keyboard)

@Client.on_callback_query()
async def button_handler(client, query: CallbackQuery):
    user_id = query.message.chat.id
    data = query.data

    if data == "cancel":
        user_texts.pop(user_id, None)
        await query.message.edit_text("Cancelled.")
        return

    text = user_texts.get(user_id)
    if not text:
        await query.message.edit_text("No text found. Please send text first.")
        return

    try:
        segments = split_by_language(text)
        combined_audio = AudioSegment.empty()

        for i, (segment_text, lang_code) in enumerate(segments):
            tts = gTTS(segment_text, lang=lang_code)
            file_path = os.path.join(VOICE_DIR, f"temp_{user_id}_{i}.mp3")
            tts.save(file_path)
            audio = AudioSegment.from_mp3(file_path)
            combined_audio += audio
            os.remove(file_path)

        final_path = os.path.join(VOICE_DIR, f"tts_{user_id}.mp3")
        combined_audio.export(final_path, format="mp3")

        langs_used = ', '.join(set(lang for _, lang in segments))
        await query.message.reply_voice(voice=final_path, caption=f"Languages Detected: {langs_used}")
        os.remove(final_path)
        user_texts.pop(user_id, None)

    except Exception as e:
        await query.message.edit_text(f"Error: {str(e)}")

