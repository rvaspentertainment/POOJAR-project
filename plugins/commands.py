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
import string
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from gtts import gTTS
from langdetect import detect

# Bot Configuration

# Store user session data
user_data = {}

# All supported languages by gTTS
from gtts.lang import tts_langs

gtts_languages = tts_langs()
# Start command

# Cancel command
@Client.on_callback_query(filters.regex("cancel"))
async def cancel_button(_, query: CallbackQuery):
    user_data.pop(query.from_user.id, None)
    await query.message.edit("Cancelled. Send me text again to start over.")

# Handle text
@Client.on_message(filters.text)
async def handle_text(_, message: Message):
    text = message.text
    user_id = message.from_user.id
    try:
        lang = detect(text)
        user_data[user_id] = {"text": text, "lang": lang}

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="lang_yes"),
             InlineKeyboardButton("No", callback_data="lang_no")],
            [InlineKeyboardButton("Cancel", callback_data="cancel")]
        ])
        await message.reply(f"Detected Language: {gtts_languages.get(lang, 'Unknown')} ({lang})\nDo you want to proceed?", reply_markup=buttons)
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

# Handle Yes
@Client.on_callback_query(filters.regex("lang_yes"))
async def confirm_lang(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in user_data:
        return await query.answer("Session expired. Send text again.", show_alert=True)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Slow", callback_data="speed_slow"),
         InlineKeyboardButton("Medium", callback_data="speed_medium"),
         InlineKeyboardButton("Fast", callback_data="speed_fast")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    await query.message.edit("Choose voice speed:", reply_markup=buttons)

# Handle No
@Client.on_callback_query(filters.regex("lang_no"))
async def lang_no(_, query: CallbackQuery):
    alphabet = list(string.ascii_uppercase)
    rows = [[InlineKeyboardButton(letter, callback_data=f"letter_{letter}") for letter in alphabet[i:i+5]] for i in range(0, 26, 5)]
    rows.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
    await query.message.edit("Select starting letter of your language:", reply_markup=InlineKeyboardMarkup(rows))

# Handle letter selection
@Client.on_callback_query(filters.regex(r"letter_([A-Z])"))
async def handle_letter(_, query: CallbackQuery):
    letter = query.data.split("_")[1].lower()
    matches = [(k, v) for k, v in gtts_languages.items() if v.lower().startswith(letter)]

    if not matches:
        return await query.message.edit("No languages found. Please contact the owner.")

    rows = [
        [InlineKeyboardButton(name, callback_data=f"langpick_{code}")]
        for code, name in matches
    ]
    rows.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
    await query.message.edit("Choose your language:", reply_markup=InlineKeyboardMarkup(rows))

# Handle language pick
@Client.on_callback_query(filters.regex(r"langpick_(.+)"))
async def handle_lang_pick(_, query: CallbackQuery):
    lang_code = query.data.split("_")[1]
    user_data[query.from_user.id]["lang"] = lang_code

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Slow", callback_data="speed_slow"),
         InlineKeyboardButton("Medium", callback_data="speed_medium"),
         InlineKeyboardButton("Fast", callback_data="speed_fast")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    await query.message.edit("Choose voice speed:", reply_markup=buttons)

# Handle speed
@Client.on_callback_query(filters.regex(r"speed_(slow|medium|fast)"))
async def handle_speed(_, query: CallbackQuery):
    speed = query.data.split("_")[1]
    user_id = query.from_user.id
    if user_id not in user_data:
        return await query.message.edit("Session expired. Send text again.")

    text = user_data[user_id]["text"]
    lang = user_data[user_id]["lang"]
    tts = gTTS(text=text, lang=lang, slow=(speed == "slow"))
    filename = f"audios/audio_{user_id}.mp3"
    os.makedirs("audios", exist_ok=True)
    tts.save(filename)

    progress = "⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪"
    await query.message.edit(f"{progress}\nSending voice...")

    caption = f"Language: {gtts_languages.get(lang, lang)} ({lang}) | Characters: {len(text)} | Speed: {speed.title()}"
    await query.message.reply_voice(voice=filename, caption=caption)
    os.remove(filename)
    user_data.pop(user_id, None)

