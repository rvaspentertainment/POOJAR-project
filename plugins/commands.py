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
import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient # Import MongoClient
from transformers import pipeline
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# --- Configuration ---
# Load environment variables from a .env file (recommended)

# Check if essential config is missing
if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URI]):
    raise ValueError("Missing essential configuration (API_ID, API_HASH, BOT_TOKEN, MONGO_URI). Please set them.")

# --- MongoDB Setup ---
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["event_bot"] # Consider a more descriptive DB name if needed
    events_collection = db["daily_events"] # Use a descriptive collection name
    # Test connection
    mongo_client.admin.command('ping')
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # Depending on your needs, you might want to exit or handle this differently
    exit() # Exit if DB connection fails

# --- Classification Model ---
try:
    print("Loading classification model...")
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading Hugging Face model: {e}")
    # Decide how to handle model loading failure (e.g., exit, run without classification)
    classifier = None # Set classifier to None if loading fails
    print("Warning: Classification will be disabled.")

EVENT_TYPES = [
    "Birthday", "Death", "Historical Event", "Sports Event", "Invention & Discovery",
    "Political Event", "Space Event", "Scientific Breakthrough", "Technology Milestone",
    "Cultural Event", "Natural Disaster", "Religious Event", "Economic Event",
    "Military Event", "Famous Speech", "Entertainment Milestone", "Social Movement",
    "Literary Event", "Transportation & Infrastructure", "Scientific Mission",
    "First-time Event", "Unknown"
]
CLASSIFICATION_THRESHOLD = 0.75 # Confidence threshold for classification

# --- Helper Functions ---
def classify_event(event_text):
    """Classifies event text using the zero-shot model."""
    if not classifier: # Check if classifier loaded successfully
        return "Unknown (Classifier unavailable)"
    try:
        result = classifier(event_text, EVENT_TYPES, multi_label=False) # multi_label=False is often better for single classification
        if result["scores"][0] >= CLASSIFICATION_THRESHOLD:
            return result["labels"][0]
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error during classification for text '{event_text[:50]}...': {e}")
        return "Unknown (Classification Error)"

def fetch_events_from_wikipedia(date_str_wikipedia):
    """Fetches events for a given date from Wikipedia (e.g., 'January_1')."""
    # Note: Wikipedia structure can change, breaking this scraper. API is more robust.
    url = f"https://en.wikipedia.org/wiki/{date_str_wikipedia}"
    headers = {'User-Agent': 'MyCoolTelegramBot/1.0 (contact@example.com)'} # Be a good citizen
    print(f"Fetching events from: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10) # Added headers and timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        soup = BeautifulSoup(response.text, "html.parser")
        # Try to find the 'Events' section more reliably
        events_heading = soup.find(id='Events')
        if not events_heading:
            print("Could not find 'Events' section heading.")
            return []

        # Look for the first <ul> *after* the 'Events' heading
        event_list = events_heading.find_next('ul')
        if not event_list:
            print("Could not find event list (<ul>) after 'Events' heading.")
            return []

        events = []
        # Iterate through list items (li) directly under the found ul
        for li in event_list.find_all('li', recursive=False):
            # Basic cleaning: remove potential sub-lists, references etc.
            for sub_ul in li.find_all('ul'):
                sub_ul.decompose()
            for sup in li.find_all('sup', class_='reference'):
                sup.decompose()
            event_text = li.get_text(strip=True)
            if event_text: # Ensure it's not an empty list item
                 events.append(event_text)

        print(f"Fetched {len(events)} raw events.")
        return events

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia page: {e}")
        return [] # Return empty list on error
    except Exception as e:
        print(f"Error parsing Wikipedia page: {e}")
        return []

def store_events(date_str_db, events):
    """Classifies and stores events in MongoDB."""
    if not events:
        print(f"No events provided to store for {date_str_db}.")
        return

    print(f"Classifying and preparing {len(events)} events for storage...")
    formatted_events = []
    for event in events:
        category = classify_event(event)
        formatted_events.append({"event": event, "category": category})

    try:
        # Use update_one with upsert=True: inserts if date doesn't exist, updates if it does
        result = events_collection.update_one(
            {"date": date_str_db},
            {"$set": {"events": formatted_events, "last_updated": datetime.datetime.utcnow()}},
            upsert=True
        )
        if result.upserted_id:
            print(f"Inserted new events for {date_str_db}.")
        elif result.modified_count > 0:
            print(f"Updated events for {date_str_db}.")
        else:
             print(f"Events for {date_str_db} are already up-to-date.")

    except Exception as e:
        print(f"Error storing events in MongoDB: {e}")

def get_stored_events(date_str_db):
    """Retrieves stored events for a specific date from MongoDB."""
    try:
        data = events_collection.find_one({"date": date_str_db})
        if data:
            return data.get("events", []) # Use .get for safety
        else:
            return None # Explicitly return None if no document found for the date
    except Exception as e:
        print(f"Error retrieving events from MongoDB: {e}")
        return None

# --- Bot Instance ---

async def run_daily_fetch_and_store():
    """Fetches events from Wikipedia, classifies, and stores them."""
    # Use format like "January_1" for Wikipedia and DB consistency
    today_str = datetime.datetime.now().strftime("%B_%d")
    print(f"\n--- Running Daily Fetch for {today_str} ---")
    events = fetch_events_from_wikipedia(today_str)
    if events:
        store_events(today_str, events)
    else:
        print(f"No events fetched for {today_str}.")
    print(f"--- Daily Fetch for {today_str} Complete ---\n")

# --- Bot Command Handlers ---
@Client.on_message(filters.command("events"))
async def send_events_command(client, message):
    """Handles the /events command, showing category buttons."""
    today_str = datetime.datetime.now().strftime("%B_%d")
    today_display = today_str.replace('_', ' ') # For display

    print(f"Received /events command from user {message.from_user.id}")
    events = get_stored_events(today_str)

    if events:
        # Create buttons dynamically from the *actual* categories found for the day + "Unknown"
        # This avoids showing buttons for categories with no events today
        categories_today = sorted(list(set(e.get("category", "Unknown") for e in events)))
        buttons = [
             # Use callback data like "category:birthday"
            [InlineKeyboardButton(cat, callback_data=f"category:{cat.lower().replace(' ', '_')}")]
            for cat in categories_today if cat != "Unknown" # Show known categories first
        ]
        if any(e.get("category") == "Unknown" for e in events): # Add Unknown button if present
             buttons.append([InlineKeyboardButton("Unknown", callback_data="category:unknown")])

        if not buttons: # Should not happen if events exist, but as a safeguard
             await message.reply_text(f"Found events for {today_display}, but couldn't process categories.")
             return

        await message.reply_text(
            f"🗓️ **Events for {today_display}**\n\nChoose a category to view events:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_text(f"🤔 No events found stored for {today_display}. Maybe the daily fetch hasn't run yet or failed?")
        # Optionally trigger the fetch here if desired, but be careful about limits/timing
        # await run_daily_fetch_and_store() # Example: Trigger fetch if missing

@Client.on_callback_query(filters.regex("^category:")) # Filter callbacks starting with "category:"
async def category_callback_handler(client, query: CallbackQuery):
    """Handles button presses for specific categories."""
    today_str = datetime.datetime.now().strftime("%B_%d")
    today_display = today_str.replace('_', ' ')

    # Extract category from callback data ("category:birthday" -> "birthday")
    try:
        requested_category_slug = query.data.split(":", 1)[1]
        # Convert slug back to title case used in storage (e.g., "birthday" -> "Birthday")
        requested_category = requested_category_slug.replace("_", " ").title()
        if requested_category_slug == "unknown": # Handle special case
             requested_category = "Unknown"

        print(f"Received category callback for '{requested_category}' from user {query.from_user.id}")

    except IndexError:
        await query.answer("Invalid callback data.", show_alert=True)
        print(f"Error: Invalid callback data received: {query.data}")
        return

    events = get_stored_events(today_str)

    if not events:
        await query.message.edit_text(f"😥 Sorry, event data for {today_display} seems to be missing.")
        await query.answer()
        return

    filtered_events = [e for e in events if e.get("category") == requested_category]

    response_parts = []
    if filtered_events:
        response_parts.append(f"📅 **{requested_category} Events on {today_display}**\n")
        for event in filtered_events:
            response_parts.append(f"\n📝 {event['event']}") # Add newline before event for better spacing
    else:
        response_parts.append(f"🤷 No events found for the category '{requested_category}' on {today_display}.")

    full_response = "".join(response_parts)

    # --- Message Splitting (Basic Example) ---
    max_length = 4096 # Telegram message length limit
    if len(full_response) > max_length:
        await query.answer("Sending events in multiple parts...", show_alert=False)
        parts = []
        current_part = response_parts[0] # Start with the header
        for item in response_parts[1:]: # Iterate through event items
            if len(current_part) + len(item) <= max_length:
                current_part += item
            else:
                parts.append(current_part)
                current_part = response_parts[0] + item # Start new part with header + current item
        parts.append(current_part) # Add the last part

        # Edit the original message with the first part
        await query.message.edit_text(parts[0])
        # Send subsequent parts as new messages
        for part in parts[1:]:
             await client.send_message(query.message.chat.id, part)

    else:
         # Edit the original message with the full response
        try:
            await query.message.edit_text(full_response)
            await query.answer() # Acknowledge callback
        except Exception as e:
             print(f"Error editing message: {e}")
             await query.answer("Error updating message.", show_alert=True)


# --- Manual Trigger Command (for testing/admin) ---
@Client.on_message(filters.command("update_events") & filters.user(ADMIN_ID) if ADMIN_ID else filters.command("update_events"))
async def update_events_command(client, message):
    """Manually triggers the event fetching and storing process (Admin only if ADMIN_ID is set)."""
    await message.reply_text("🔄 Starting manual event fetch and store process...")
    print(f"Manual update triggered by user {message.from_user.id}")
    try:
        await run_daily_fetch_and_store()
        await message.reply_text("✅ Event fetch and store process completed.")
    except Exception as e:
        await message.reply_text(f"❌ An error occurred during manual update: {e}")
        print(f"Error during manual update: {e}")
        # Optionally notify admin via message if needed


# --- Function to post daily summary (can be scheduled) ---
async def post_daily_summary():
    """Posts a summary of all events for the day to the designated channel."""
    if not CHANNEL_ID:
        print("CHANNEL_ID not set. Cannot post daily summary.")
        return

    today_str = datetime.datetime.now().strftime("%B_%d")
    today_display = today_str.replace('_', ' ')
    events = get_stored_events(today_str)

    if not events:
        message = f"📅 **Events for {today_display}**\n\nNo events found or fetched for today."
        print(f"Attempted to post daily summary for {today_display}, but no events found.")
    else:
        message_parts = [f"📅 **Events Summary for {today_display}**\n"]
        # Group by category for better readability
        events_by_category = {}
        for event in events:
            category = event.get("category", "Unknown")
            if category not in events_by_category:
                events_by_category[category] = []
            events_by_category[category].append(event['event'])

        # Sort categories (optional)
        sorted_categories = sorted(events_by_category.keys())

        for category in sorted_categories:
             message_parts.append(f"\n--- {category} ---")
             for event_text in events_by_category[category]:
                 message_parts.append(f"\n- {event_text}") # Use bullet points

        message = "".join(message_parts)

    # Handle message length for channel post
    max_length = 4096
    async with app: # Ensure client is started for sending message
        try:
            if len(message) > max_length:
                 # Basic split, consider more sophisticated splitting if needed
                 await app.send_message(CHANNEL_ID, message[:max_length-5] + "\n...")
                 # You might need to send remaining parts too
                 print(f"Warning: Daily summary for {today_display} was truncated.")
            else:
                 await app.send_message(CHANNEL_ID, message)
            print(f"Successfully posted daily summary to channel {CHANNEL_ID}.")
        except Exception as e:
            print(f"Error sending daily summary to channel {CHANNEL_ID}: {e}")
            if ADMIN_ID:
                 try:
                      await app.send_message(ADMIN_ID, f"Failed to post daily summary to channel {CHANNEL_ID}. Error: {e}")
                 except Exception as admin_err:
                      print(f"Failed to notify admin about summary posting error: {admin_err}")

