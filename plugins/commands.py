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
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment
from pydub import AudioSegment
from pydub.utils import which

# Set ffmpeg paths manually
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# Text Message Handler
@Client.on_message(filters.text)
async def handle_text(client, message: Message):
    text = message.text
    try:
        segments = split_by_language(text)
        combined_audio = AudioSegment.empty()

        for i, (segment_text, lang_code) in enumerate(segments):
            tts = gTTS(segment_text, lang=lang_code)
            file_path = f"temp_{message.chat.id}_{i}.mp3"
            tts.save(file_path)
            audio = AudioSegment.from_mp3(file_path)
            combined_audio += audio
            os.remove(file_path)

        final_path = f"tts_{message.chat.id}.mp3"
        combined_audio.export(final_path, format="mp3")

        langs_used = ', '.join(set(lang for _, lang in segments))
        await message.reply_voice(voice=final_path, caption=f"Detected languages: {langs_used}\nHere is your audio!")
        os.remove(final_path)

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

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
