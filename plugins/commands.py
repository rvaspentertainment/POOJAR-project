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



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    


import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment
import imageio_ffmpeg
import asyncio

# Set ffmpeg and ffprobe paths using imageio
AudioSegment.converter = str(imageio_ffmpeg.get_ffmpeg_exe())
AudioSegment.ffprobe = str(imageio_ffmpeg.get_ffprobe_exe())

# Bot Configuration

# Keep track of active jobs
active_jobs = {}

# Language Splitter
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

# /start Command

# Cancel Handler
@Client.on_callback_query(filters.regex("cancel"))
async def cancel_handler(client, query: CallbackQuery):
    chat_id = query.message.chat.id
    active_jobs[chat_id] = "cancelled"
    await query.message.edit_text("❌ Task cancelled.")

# TTS Handler
@Client.on_message(filters.text)
async def handle_text(client, message: Message):
    text = message.text
    chat_id = message.chat.id

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])

    progress = await message.reply_text("Detecting language(s)...", reply_markup=keyboard)
    active_jobs[chat_id] = "running"

    try:
        segments = split_by_language(text)
        if not segments:
            await progress.edit_text("No valid text detected.")
            return

        await progress.edit_text("Generating audio...", reply_markup=keyboard)
        combined_audio = AudioSegment.empty()
        langs_used = set()

        for i, (segment_text, lang_code) in enumerate(segments):
            if active_jobs.get(chat_id) == "cancelled":
                return  # Stop processing if user canceled

            try:
                tts = gTTS(segment_text, lang=lang_code)
                temp_path = f"temp_{chat_id}_{i}.mp3"
                tts.save(temp_path)

                audio = AudioSegment.from_mp3(temp_path)
                combined_audio += audio
                langs_used.add(lang_code)

                os.remove(temp_path)
            except Exception as e:
                print(f"Error with segment '{segment_text}': {e}")
                continue

        if combined_audio.duration_seconds == 0:
            await progress.edit_text("Could not generate audio.")
            return

        final_path = f"tts_{chat_id}.mp3"
        combined_audio.export(final_path, format="mp3")

        caption = f"Detected languages: {', '.join(langs_used)}"
        await progress.edit_text("Uploading audio...", reply_markup=None)
        await message.reply_voice(voice=final_path, caption=caption)

        os.remove(final_path)
        await progress.delete()
        active_jobs.pop(chat_id, None)

    except Exception as e:
        await progress.edit_text(f"Error: {str(e)}", reply_markup=None)
        active_jobs.pop(chat_id, None)

