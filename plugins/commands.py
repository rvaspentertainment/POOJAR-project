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



import asyncio 
import requests 
import datetime 
import pymongo 
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from bs4 import BeautifulSoup


client = pymongo.MongoClient("mongodb://localhost:27017/") db = client["on_this_day_db"] collection = db["events"]



def get_on_this_day_events(): 
    try:
        today = datetime.datetime.now() 
        url = f"https://en.wikipedia.org/wiki/{today.strftime('%B')}_{today.day}" 
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, 'html.parser')
        events = {
            "Birthdays": [], "Deaths": [], "Historical Events": [], "Inventions & Discoveries": [],
            "Sports Events": [], "Political Events": [], "Cultural Events": [], "Natural Disasters": [],
            "Space Events": [], "Scientific Breakthroughs": [], "Technology Milestones": [], "Economic Events": [],
            "Military Events": [], "Religious Events": [], "Famous Speeches": [], "Awards & Achievements": [],
            "Environmental Events": [], "Legal & Justice Events": [], "Social Movements": [], "Entertainment Milestones": [],
            "Literary Events": [], "Aviation & Space Milestones": [], "Sports Records & Championships": [], "Cultural & Artistic Events": [],
            "Transportation & Infrastructure": [], "Historical Accidents & Tragedies": [], "Political Assassinations": [],
            "Scientific Missions": [], "First-time Events": []
        }
        sections = soup.find_all("h2")
        for section in sections:
            title = section.text.strip()
            for category in events.keys():
                if category in title:
                    event_list = section.find_next_sibling("ul")
                    events[category] = [li.text for li in event_list.find_all("li")[:5]]

collection.delete_many({})  # Clear previous day's data
collection.insert_one(events)  # Store new events
return events

Function to fetch stored events

def get_stored_events(): return collection.find_one({}, {"_id": 0})

Command to get today's events

@app.on_message(filters.command("today")) async def send_today_events(client, message): events = get_stored_events() if not events: await message.reply("No data available. Try again later.") return

keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(category, callback_data=category.replace(" ", "_"))] for category in events.keys()]
)
await message.reply("📅 Select a category:", reply_markup=keyboard)

Callback to show event details

@app.on_callback_query() async def cb_handler(client: Client, query: CallbackQuery): try: events = get_stored_events() category = query.data.replace("_", " ") text = "\n".join(events.get(category, [])) await query.message.edit(f"📜 {category} Today:\n{text}") except Exception as e: await client.send_message(query.from_user.id, f"An error occurred: {str(e)}")

Auto-update function

async def auto_update(): while True: get_on_this_day_events() await asyncio.sleep(86400)  # Update every 24 hours

