# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
import aiohttp 
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
from gtts.lang import tts_langs
BATCH_FILES = {}
from datetime import datetime, timedelta
import pytz
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
async def dati():
    try:
        kolkata_timezone = pytz.timezone('Asia/Kolkata')
        kolkata_time = datetime.now(kolkata_timezone)
        formatted_time = kolkata_time.strftime('%d/%m/%Y %H:%M:%S')  
        return formatted_time 
    except Exception as e:
        # Handle exceptions appropriately, e.g., logging or raising
        raise RuntimeError(f"Error in dati function: {str(e)}")


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

@Client.on_message(filters.command("user_details"))
async def user_details(client, message):
    try:
        if len(message.command) > 1:
            # Command with user_id argument: /user_details 12345
            user_id = int(message.command[1])
        else:
            # Command without user_id argument: /user_details
            user_id = message.from_user.id
            
        user_data = await db.ud.find_one({"id": user_id})            

        if user_data:
            details_message = (
                f"User Details:\n\n"
                f"Joined on: {user_data['joined']}\n"          
                f"ID: {user_data['id']}\n"
                f"Total Text to Speech converted: {user_data['mp3']}\n"          

                f"Total text characters used: {user_data['char']}\n"
                                  
            )
            await message.reply(details_message)
        else:
            await message.reply("User details not found.")
            
    except ValueError:
        await message.reply("Invalid user ID. Please provide a valid numerical user ID.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")



@Client.on_message(filters.command("start"))
async def start(client, message: Message):
    try:
        user_id = message.from_user.id 
        if not await db.ud.find_one({"id": user_id}):
            user_data = {
                "id": user_id,
                "mp3": 0,
                "char": 0,
                "joined": await dati()
            }    
            await db.ud.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)
            
        button = [[
            InlineKeyboardButton("PP Bots", url="https://t.me/pp_bots"),
            InlineKeyboardButton("Support", url="https://t.me/+39yIpl-sKcU1NDU1")
        ]]
        reply_markup = InlineKeyboardMarkup(button)

        await query.message.reply_text(
            "Send me any text, and I'll convert it to speech using detected language(s)!/n/nPowered by PP Bots and GTtS",
            reply_markup=reply_markup
        )
    except Exception as e:
        await message.reply_text(f"An error occurred in `cancel`: `{str(e)}`")


        
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





# Store this globally or dynamically cache as needed
ALL_LANGS = sorted(tts_langs().items(), key=lambda x: x[1])
CHUNK_SIZE = 20

def get_lang_buttons(page: int = 0):
    start = page * CHUNK_SIZE
    end = start + CHUNK_SIZE
    rows = []
    for i in range(start, min(end, len(ALL_LANGS)), 2):
        row = []
        for j in range(2):
            if i + j < len(ALL_LANGS):
                code, name = ALL_LANGS[i + j]
                row.append(InlineKeyboardButton(name, callback_data=f"langpick_{code}"))
        rows.append(row)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"region_page_{page - 1}"))
    if end < len(ALL_LANGS):
        nav_buttons.append(InlineKeyboardButton("➡️ More", callback_data=f"region_page_{page + 1}"))
    if nav_buttons:
        rows.append(nav_buttons)
    return InlineKeyboardMarkup(rows)

@Client.on_callback_query(filters.regex("region_all"))
async def region_all(_, query: CallbackQuery):
    try:
        
        await query.message.reply("Select a language:", reply_markup=get_lang_buttons(0))
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `region_all`: `{str(e)}`")

@Client.on_callback_query(filters.regex(r"region_page_(\d+)"))
async def region_page(_, query: CallbackQuery):
    try:
        page = int(query.data.split("_")[-1])
        await query.message.edit_text("Select a language:", reply_markup=get_lang_buttons(page))
    except Exception as e:
        await query.message.reply_text(f"An error occurred in `region_page`: `{str(e)}`")


# Save language selected manually
@Client.on_callback_query(filters.regex(r"langpick_(.+)"))
async def handle_lang_pick(_, query: CallbackQuery):
    try:
        
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

        caption = (
            f"🌐 Language: {gtts_languages.get(lang, lang)} ({lang})\n"
            f"✍️ Characters: {len(text)}\n"
            f"🎵 Speed: {speed.title()}"
        )
        await query.message.reply_voice(voice=filepath, caption=caption)
        envs_url = await upload_to_uguu(filepath)
        if not envs_url:
            return await query.message.reply_text("❌ Failed to upload voice file. Please try again.")

        # Inline download button
        button = [[
            InlineKeyboardButton("• ᴅᴏᴡɴʟᴏᴀᴅ •", url=envs_url)
        ]]
        reply_markup = InlineKeyboardMarkup(button)

        await query.message.reply_text(
            "Use this link to download and save the voice file to your phone storage or streaming online(in chrome):",
            reply_markup=reply_markup
        )
        
        data = await db.ud.find_one({"id": user_id})            

        user_data1 = {
            "id": user_id,     # unique user ID
            "mp3": data.get("mp3", 0) + 1,
            "char": data.get("char", 0) + len(text)
        }
        await db.ud.update_one(
            {"id": user_data1["id"]},
            {"$set": {
                "mp3": user_data1["mp3"],
                "char": user_data1["char"]
            }},
            upsert=True
        )
        os.remove(filepath)
        user_data.pop(user_id, None)

    except Exception as e:
        await query.message.reply_text(f"An error occurred in `speed`: `{str(e)}`")



import aiohttp
import os

async def upload_to_uguu(file_path):
    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as f:
                form = aiohttp.FormData()
                form.add_field(
                    'files[]',
                    f,
                    filename=os.path.basename(file_path),
                    content_type='application/octet-stream'
                )

                async with session.post("https://uguu.se/upload.php", data=form) as response:
                    text = await response.text()
                    print("Raw response:", text)

                    if response.status == 200:
                        try:
                            data = await response.json()
                            if isinstance(data, dict) and "files" in data:
                                return data["files"][0].get("url")
                            else:
                                print("Unexpected JSON structure:", data)
                        except Exception as json_error:
                            print("JSON decode error:", str(json_error))
                    else:
                        print(f"Upload failed. HTTP Status: {response.status}")
    except Exception as e:
        print("Upload error:", str(e))
    
    return None
