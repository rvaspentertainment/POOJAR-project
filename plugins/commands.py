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
import os
from PIL import Image
from fpdf import FPDF
import img2pdf
from io import BytesIO
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
    await message.reply("hi")

user_images = {}
last_message = {}

@Client.on_message(
    filters.private & 
    (filters.photo | 
     (filters.document & filters.regex(r"\.(jpg|jpeg|png)$", flags=2))) & 
    filters.incoming
)
async def collect_images(bot, message):
    try:
        user_id = message.from_user.id

        # Initialize user storage if not present
        if user_id not in user_images:
            user_images[user_id] = []

        # Download the new image
        file_path = await message.download()

        # Append the new image without deleting previous images
        user_images[user_id].append(file_path)

        # Delete the old "Create PDF" button message if exists
        
        # Send a new message with the "Create PDF" button
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Create PDF", callback_data="create_pdf")]
        ])
        
        sent_message = await message.reply_text(
            f"Image added! You have {len(user_images[user_id])} image(s) ready.\n\n"
            "Click 'Create PDF' to generate your PDF file.", 
            reply_markup=buttons
        )
        
        # Store the reference to the latest message with a button
        last_message[user_id].append(sent_message)
                 
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id

    if query.data == "create_pdf":
        # Edit the message to remove the button and show progress
        msg1 = await query.message.edit_text("Creating your PDF, please wait...")

        # Check if user has images
        if user_id not in user_images or len(user_images[user_id]) == 0:
            await query.answer("You have no images to create a PDF.", show_alert=True)
            return

        try:
            # Ask the user for the PDF file name (without extension)
            response = await client.ask(user_id, "**Send the PDF name (without extension):**")
            pdf_name = response.text if response.text else "converted"

            # Sanitize the file name
            pdf_name = "".join(char for char in pdf_name if char.isalnum() or char in " _-").strip()
            if not pdf_name:
                pdf_name = "converted"

            # Add the .pdf extension
            pdf_file_name = f"{pdf_name}.pdf"

            # Convert images to a PDF using img2pdf
            pdf_bytes = img2pdf.convert(user_images[user_id])

            # Save to BytesIO
            pdf_output = BytesIO(pdf_bytes)
            pdf_output.seek(0)

            await msg1.delete()
            await response.delete()
            # Send the PDF to the user
            await client.send_document(
                chat_id=user_id,
                document=pdf_output,
                file_name=pdf_file_name,
                caption=f"Here is your PDF: **{pdf_file_name}**"
            )

            # Delete user images from the server
            for file_path in user_images[user_id]:
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Clear the image list and last message for the user
            user_images[user_id].clear()
            if user_id in last_message:
                del last_message[user_id]

            # Send a confirmation message
            

            await query.answer("Your PDF has been created.", show_alert=True)

        except Exception as e:
            await query.answer(f"An error occurred while creating the PDF: {str(e)}", show_alert=True)
