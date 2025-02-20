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

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image

# Temporary storage for images
IMAGE_FOLDER = "downloads"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Dictionary to store images by user
user_images = {}

@Client.on_message(filters.private & (filters.photo | filters.document.mime_type("image/jpeg") | filters.document.mime_type("image/png")) & filters.incoming)
async def collect_images(bot, message):
    try:
        user_id = message.from_user.id
        if user_id not in user_images:
            user_images[user_id] = []

        # Downloading the image
        file_path = await message.download(folder=IMAGE_FOLDER)
        user_images[user_id].append(file_path)

        # Reply with options to add more images or create a PDF
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Add More Image", callback_data="add_more_image"),
                InlineKeyboardButton("Create PDF", callback_data="create_pdf")
            ]
        ])
        
        await message.reply_text(
            f"Image added! You have {len(user_images[user_id])} image(s) ready.\n\n"
            "You can either add more images or create a PDF.",
            reply_markup=buttons
        )
                 
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")





@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()



    elif callback_query.data == "add_more_image":
        await callback_query.message.reply_text(
            "Please send more images now.\nWhen you're ready, click 'Create PDF'."
        )
        # Waiting for more images
        while True:
            new_message = await bot.listen(callback_query.message.chat.id, timeout=60)
            if new_message.photo or (new_message.document and new_message.document.mime_type in ["image/jpeg", "image/png"]):
                file_path = await new_message.download(folder=IMAGE_FOLDER)
                user_images[user_id].append(file_path)
                await callback_query.message.reply_text(
                    f"Image added! Now you have {len(user_images[user_id])} image(s).\n"
                    "Send more images or click 'Create PDF'."
                )
            else:
                await callback_query.message.reply_text("Only images are allowed. Please send a valid image.")
    
    elif callback_query.data == "create_pdf":
        if user_id not in user_images or not user_images[user_id]:
            await callback_query.message.reply_text("No images available to create a PDF.")
            return

        try:
            pdf_path = os.path.join(IMAGE_FOLDER, f"{user_id}_output.pdf")
            image_list = []

            # Open images and convert to RGB mode for PDF
            for image_path in user_images[user_id]:
                img = Image.open(image_path).convert("RGB")
                image_list.append(img)

            # Save as PDF if there are images
            if image_list:
                image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
                await callback_query.message.reply_document(pdf_path)
                await callback_query.message.reply_text("PDF created successfully!")

                # Clean up
                for img_path in user_images[user_id]:
                    os.remove(img_path)
                os.remove(pdf_path)
                user_images[user_id] = []

        except Exception as e:
            await callback_query.message.reply_text(f"Failed to create PDF: {e}")
