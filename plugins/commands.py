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
from gtts.lang import tts_langs

# Store user session data
user_data = {}

# All supported languages
gtts_languages = tts_langs()

# Cancel Button
@Client.on_callback_query(filters.regex("cancel"))
async def cancel_button(_, query: CallbackQuery):
    try:
        user_data.pop(query.from_user.id, None)
        await query.message.edit("❌ Cancelled. Send me new text to start again.")
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `cancel`: `{str(e)}`")

# Handle Incoming Text
@Client.on_message(filters.text)
async def handle_text(_, message: Message):
    try:
        text = message.text
        user_id = message.from_user.id
        lang = detect(text)
        user_data[user_id] = {"text": text, "lang": lang}

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Yes", callback_data="lang_yes"),
             InlineKeyboardButton("✏️ No", callback_data="lang_no")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
        await message.reply(
            f"Detected Language: {gtts_languages.get(lang, 'Unknown')} ({lang})\nDo you want to proceed?",
            reply_markup=buttons
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: `{str(e)}`")

# User accepted detected language
@Client.on_callback_query(filters.regex("lang_yes"))
async def confirm_lang(_, query: CallbackQuery):
    try:
        await query.message.delete()
        user_id = query.from_user.id
        if user_id not in user_data:
            return await query.answer("Session expired. Send new text.", show_alert=True)

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🐢 Slow", callback_data="speed_slow"),
             InlineKeyboardButton("⚡ Medium", callback_data="speed_medium"),
             InlineKeyboardButton("🚀 Fast", callback_data="speed_fast")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
        await query.message.edit("Select your voice speed:", reply_markup=buttons)
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `lang_yes`: `{str(e)}`")

@Client.on_callback_query(filters.regex("lang_no"))
async def lang_no(_, query: CallbackQuery):
    try:
        await query.message.delete()
        rows = [
            [InlineKeyboardButton("🇮🇳 Indian", callback_data="region_indian")],
            [InlineKeyboardButton("🇪🇺 European", callback_data="region_europe")],
            [InlineKeyboardButton("🌏 Asian & Far-East", callback_data="region_asia")],
            [InlineKeyboardButton("🌍 African", callback_data="region_africa")],
            [InlineKeyboardButton("🌙 Middle Eastern", callback_data="region_middleeast")],
            [InlineKeyboardButton("🔤 All Languages A-Z", callback_data="region_all")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ]
        await query.message.edit("Choose a language group:", reply_markup=InlineKeyboardMarkup(rows))
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `lang_no`: `{str(e)}`")
@Client.on_callback_query(filters.regex("region_indian"))
async def region_indian(_, query: CallbackQuery):
    try:
        await query.message.delete()
        indian_langs = {
            'hi': 'Hindi', 'kn': 'Kannada', 'ta': 'Tamil', 'te': 'Telugu',
            'ml': 'Malayalam', 'gu': 'Gujarati', 'bn': 'Bengali', 'mr': 'Marathi',
            'pa': 'Punjabi', 'ur': 'Urdu'
        }
        buttons = [[InlineKeyboardButton(name, callback_data=f"langpick_{code}")] for code, name in indian_langs.items()]
        buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="lang_no")])
        await query.message.edit("Choose an Indian language:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `region_indian`: `{str(e)}`")

@Client.on_callback_query(filters.regex("region_africa"))
async def region_africa(_, query: CallbackQuery):
    try:
        await query.message.delete()
        african_langs = {
            'af': 'Afrikaans',
            'sw': 'Swahili',
            'yo': 'Yoruba',
            'ig': 'Igbo',
            'am': 'Amharic',
            'ha': 'Hausa',
            'st': 'Sesotho',
            'zu': 'Zulu',
        }
        buttons = [[InlineKeyboardButton(name, callback_data=f"langpick_{code}")] for code, name in african_langs.items()]
        buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="lang_no")])
        await query.message.edit("Choose an African language:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await query.message.reply_text(f"Error in `region_africa`: `{str(e)}`")

@Client.on_callback_query(filters.regex("region_middleeast"))
async def region_middleeast(_, query: CallbackQuery):
    try:
        await query.message.delete()
        mid_langs = {
            'ar': 'Arabic',
            'fa': 'Persian (Farsi)',
            'he': 'Hebrew',
            'ku': 'Kurdish',
            'tr': 'Turkish',
        }
        buttons = [[InlineKeyboardButton(name, callback_data=f"langpick_{code}")] for code, name in mid_langs.items()]
        buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="lang_no")])
        await query.message.edit("Choose a Middle Eastern language:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await query.message.reply_text(f"Error in `region_middleeast`: `{str(e)}`")

@Client.on_callback_query(filters.regex("region_asia"))
async def region_asia(_, query: CallbackQuery):
    try:
        await query.message.delete()
        asian_langs = {
            'ja': 'Japanese', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)',
            'ko': 'Korean', 'id': 'Indonesian', 'th': 'Thai', 'vi': 'Vietnamese', 'ms': 'Malay'
        }
        buttons = [[InlineKeyboardButton(name, callback_data=f"langpick_{code}")] for code, name in asian_langs.items()]
        buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="lang_no")])
        await query.message.edit("Choose an Asian language:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await query.message.reply_text(f"Error in `region_asia`: `{str(e)}`")
     
@Client.on_callback_query(filters.regex("region_europe"))
async def region_europe(_, query: CallbackQuery):
    try:
        await query.message.delete()
        euro_langs = {
            'en': 'English', 'fr': 'French', 'de': 'German', 'es': 'Spanish',
            'it': 'Italian', 'ru': 'Russian', 'pt': 'Portuguese', 'pl': 'Polish',
            'nl': 'Dutch', 'sv': 'Swedish', 'ro': 'Romanian'
        }
        buttons = [[InlineKeyboardButton(name, callback_data=f"langpick_{code}")] for code, name in euro_langs.items()]
        buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="lang_no")])
        await query.message.edit("Choose a European language:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `region_europe`: `{str(e)}`")





# Save language selected manually
@Client.on_callback_query(filters.regex(r"langpick_(.+)"))
async def handle_lang_pick(_, query: CallbackQuery):
    try:
        await query.message.delete()
        lang_code = query.data.split("_")[1]
        user_data[query.from_user.id]["lang"] = lang_code

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🐢 Slow", callback_data="speed_slow"),
             InlineKeyboardButton("⚡ Medium", callback_data="speed_medium"),
             InlineKeyboardButton("🚀 Fast", callback_data="speed_fast")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
        await query.message.edit("Select your voice speed:", reply_markup=buttons)
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `langpick`: `{str(e)}`")

# Generate voice
@Client.on_callback_query(filters.regex(r"speed_(slow|medium|fast)"))
async def handle_speed(_, query: CallbackQuery):
    try:
        await query.message.delete()
        speed = query.data.split("_")[1]
        user_id = query.from_user.id

        if user_id not in user_data:
            return await query.message.edit("Session expired. Send new text.")

        text = user_data[user_id]["text"]
        lang = user_data[user_id]["lang"]
        os.makedirs("audios", exist_ok=True)
        filepath = f"audios/audio_{user_id}.mp3"

        tts = gTTS(text=text, lang=lang, slow=(speed == "slow"))
        tts.save(filepath)

        
        await query.message.edit("Sending voice...")

        caption = f"🌐 Language: {gtts_languages.get(lang, lang)} ({lang})\n✍️ Characters: {len(text)}\n🎵 Speed: {speed.title()}"
        await query.message.reply_voice(voice=filepath, caption=caption)

        os.remove(filepath)
        user_data.pop(user_id, None)

    except Exception as e:
        await query.message.reply_text(f"An error occurred in `speed`: `{str(e)}`")














