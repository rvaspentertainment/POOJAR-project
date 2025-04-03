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



import requests 
from datetime 
import datetime 
from pymongo 
 

client = MongoClient("mongodb://localhost:27017/") db = client["event_bot"] events_collection = db["events"]

 

EVENT_CATEGORIES = [ "Birthdays", "Deaths", "Historical Events", "Inventions & Discoveries", "Sports Events", "Political Events", "Cultural Events", "Natural Disasters", "Space Events", "Scientific Breakthroughs", "Technology Milestones", "Economic Events", "Military Events", "Religious Events", "Famous Speeches", "Awards & Achievements", "Environmental Events", "Legal & Justice Events", "Social Movements", "Entertainment Milestones", "Literary Events", "Aviation & Space Milestones", "Sports Records & Championships", "Cultural & Artistic Events", "Transportation & Infrastructure", "Historical Accidents & Tragedies", "Political Assassinations", "Scientific Missions", "First-time Events" ]

def fetch_events(): today = datetime.today().strftime("%m-%d") response = requests.get(f"https://example.com/api/events/{today}") # Replace with actual API data = response.json() events_collection.update_one({"date": today}, {"$set": {"events": data}}, upsert=True)

def get_events(update, context): today = datetime.today().strftime("%m-%d") data = events_collection.find_one({"date": today}) if not data: update.message.reply_text("No events found. Updating database...") fetch_events() data = events_collection.find_one({"date": today})

keyboard = [[InlineKeyboardButton(category, callback_data=category)] for category in EVENT_CATEGORIES] reply_markup = InlineKeyboardMarkup(keyboard) update.message.reply_text("Choose an event type:", reply_markup=reply_markup) 

def button_callback(update, context): query = update.callback_query query.answer() today = datetime.today().strftime("%m-%d") data = events_collection.find_one({"date": today}) category = query.data events = data.get("events", {}).get(category, ["No data available."]) message = f"{category} on this day:\n" + "\n".join(events) query.edit_message_text(text=message)

def main(): updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True) dp = updater.dispatcher dp.add_handler(CommandHandler("events", get_events)) dp.add_handler(CallbackQueryHandler(button_callback)) updater.start_polling() updater.idle()

if name == "main": main()


    
