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



import datetime 
import requests 
from transformers import pipeline
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from bs4 import BeautifulSoup






classifier = pipeline("zero-shot-classification",
model="facebook/bart-large-mnli")
EVENT_TYPES = [ "Birthday", "Death", "Historical Event", "Sports Event", "Invention & Discovery", "Political Event", "Space Event", "Scientific Breakthrough", "Technology Milestone", "Cultural Event", "Natural Disaster", "Religious Event", "Economic Event", "Military Event", "Famous Speech", "Entertainment Milestone", "Social Movement", "Literary Event", "Transportation & Infrastructure", "Scientific Mission", "First-time Event", "Unknown" ]


def classify_event(event_text):
    result = classifier(event_text, EVENT_TYPES) 
    best_label = result["labels"][0] 
    return best_label 
    if result["scores"][0] >= 0.75
    else "Unknown"



def fetch_events_from_wikipedia(date): 
    url = f"https://en.wikipedia.org/wiki/{date}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser") 
        events = [] for li in soup.select("#mw-content-text ul > li"): 
            events.append(li.text) 
            return events 
            return [] 
            
def store_events(date, events): 
    formatted_events = [] for event in events: 
        category = classify_event(event) 
        formatted_events.append({"event": event, "category": category})
        events_collection.update_one({"date": date}, {"$set": {"events": formatted_events}}, upsert=True) 

def get_stored_events(date): 
    data = events_collection.find_one({"date": date}) 
        if data:
            return data["events"] 
        else:
            None
 

async def post_daily_events(): 
    today = datetime.datetime.now().strftime("%B_%d")
    events = get_stored_events(today)
    if events: message = f"📅 **Events on {today.replace('_', ' ')}**\n\n" for event in events:
        message += f"📝 {event['event']}\n🔹 Category: {event['category']}\n\n"
        await Client.send_message(CHANNEL_ID, message) 


@Client.on_message(filters.command("events")) 
async def send_events(client, message): 
    today = datetime.datetime.now().strftime("%B_%d")
    events = get_stored_events(today)
    if events: 
        buttons = [[InlineKeyboardButton(category, callback_data=category.lower().replace(" ", "_"))] for category in EVENT_TYPES] 
        await message.reply_text("Choose an event category:", reply_markup=InlineKeyboardMarkup(buttons)) 
    else: 
        await message.reply_text("No events found for today.") 

@Client.on_callback_query() 
async def callback_handler(client: Client, query: CallbackQuery): 
    today = datetime.datetime.now().strftime("%B_%d") events = get_stored_events(today)
    if not events: 
        await query.message.edit_text("No events found.") 
        return category = query.data.replace("_", " ").title()
        filtered_events = [e for e in events if e["category"] == category] 
        if filtered_events: 
            response = f"📅 **{category} on {today.replace('_', ' ')}**\n\n" for event in filtered_events: 
                response += f"📝 {event['event']}\n\n" 
        else: 
            response = "No events found for this category." 
            await query.message.edit_text(response)  

@Client.on_message(filters.command("daily_task()")) 
async def daily_task(client, message):  
    today = datetime.datetime.now().strftime("%B_%d") 
    events = fetch_events_from_wikipedia(today), store_events(today, events)

Client.run(daily_task()) 
Client.run(post_daily_events()) 
