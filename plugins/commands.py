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
    await message.reply(hi)


user_images = {}

@Client.on_message(
    filters.private & 
    (filters.photo | 
     (filters.document & filters.regex(r"\.(jpg|jpeg|png)$", flags=2))) & 
    filters.incoming
)
async def collect_images(bot, message):
    try:
        user_id = message.from_user.id
        if user_id not in user_images:
            user_images[user_id] = []

        # Downloading the image
        file_path = await message.download()
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
    user_id = query.from_user.id

    if query.data == "close_data":
        await query.message.delete()

    elif query.data == "create_pdf":
        # Check if user has images
        if user_id not in user_images or len(user_images[user_id]) == 0:
            await query.answer("You have no images to create a PDF.", show_alert=True)
            return

        try:
            # Convert images to a PDF using img2pdf
            pdf_bytes = img2pdf.convert(user_images[user_id])

            # Save to BytesIO
            pdf_output = BytesIO(pdf_bytes)
            pdf_output.seek(0)

            # Send the PDF to the user
            await client.send_document(
                chat_id=user_id,
                document=pdf_output,
                file_name="converted.pdf",
                caption="Here is your PDF with the images you uploaded!"
            )

            # Delete user images from the server
            for file_path in user_images[user_id]:
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Clear the image list for the user
            user_images[user_id] = []

            await query.answer("Your PDF has been created and images have been deleted.", show_alert=True)

        except Exception as e:
            await query.answer(f"An error occurred while creating the PDF: {str(e)}", show_alert=True)
