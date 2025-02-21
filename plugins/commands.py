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
from PyPDF2 import PdfReader, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from pypdf import PdfReader, PdfWriter
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

        
import os
from io import BytesIO
import img2pdf
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Store images and PDFs separately
user_images = {}
user_pdfs = {}
last_message = {}

# Supported formats
IMAGE_FORMATS = (".jpg", ".jpeg", ".png")
PDF_FORMATS = (".pdf",)

# Handle both images and PDFs
@Client.on_message(
    filters.private & 
    (filters.photo | 
     (filters.document & filters.regex(r"\.(jpg|jpeg|png|pdf)$", flags=2))) & 
    filters.incoming
)
async def collect_files(bot, message):
    try:
        user_id = message.from_user.id

        # Initialize user storage if not present
        if user_id not in user_images:
            user_images[user_id] = []
        if user_id not in user_pdfs:
            user_pdfs[user_id] = []

        # Download the file
        file_path = await message.download()

        # Categorize the file
        if file_path.lower().endswith(IMAGE_FORMATS):
            user_images[user_id].append(file_path)
        elif file_path.lower().endswith(PDF_FORMATS):
            user_pdfs[user_id].append(file_path)

        # Create dynamic buttons based on uploaded files
        buttons = []
        
        if user_images[user_id]:
            buttons.append([InlineKeyboardButton("Create PDF", callback_data="create_pdf")])
        
        if user_pdfs[user_id]:
            buttons.append([InlineKeyboardButton("Extract Images", callback_data="extract_images")])
            buttons.append([InlineKeyboardButton("Watermark PDF", callback_data="watermark_pdf")])
        
        if len(user_pdfs[user_id]) > 1:
            buttons.append([InlineKeyboardButton("Merge PDFs", callback_data="merge_pdfs")])
        
        sent_message = await message.reply_text(
            f"You have {len(user_images[user_id])} image(s) and {len(user_pdfs[user_id])} PDF(s) ready.\n\n"
            "Choose an action to proceed.", 
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        if user_id not in last_message:
            last_message[user_id] = []
        last_message[user_id].append(sent_message)

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


# Handle button actions
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id

    if query.data == "create_pdf":
        await create_pdf(client, query, user_id)

    elif query.data == "extract_images":
        await select_image_format(client, query, user_id)

    elif query.data.startswith("extract_format_"):
        image_format = query.data.split("_")[-1]
        await extract_images(client, query, user_id, image_format)

    elif query.data == "watermark_pdf":
        await select_watermark_position(client, query, user_id)

    elif query.data.startswith("watermark_position_"):
        position = query.data.split("_")[-1]
        await watermark_pdf(client, query, user_id, position)

    elif query.data == "merge_pdfs":
        await merge_pdfs(client, query, user_id)


# Create PDF from images
async def create_pdf(client, query, user_id):
    await query.message.edit_text("Creating your PDF, please wait...")

    image_files = user_images.get(user_id, [])
    if not image_files:
        await query.answer("No images available for PDF creation.", show_alert=True)
        return

    try:
        response = await client.ask(user_id, "**Send the PDF name (without extension):**")
        pdf_name = "".join(char for char in response.text if char.isalnum() or char in " _-").strip()
        pdf_file_name = f"{pdf_name or 'converted'}.pdf"

        pdf_bytes = img2pdf.convert(image_files)
        pdf_output = BytesIO(pdf_bytes)
        pdf_output.seek(0)

        await client.send_document(
            chat_id=user_id,
            document=pdf_output,
            file_name=pdf_file_name,
            caption=f"Here is your PDF: **{pdf_file_name}**"
        )

        clear_user_data(user_id, "images")

    except Exception as e:
        await query.answer(f"Error while creating PDF: {str(e)}", show_alert=True)


# Ask image format for extraction
async def select_image_format(client, query, user_id):
    buttons = [
        [InlineKeyboardButton("JPG", callback_data="extract_format_jpg")],
        [InlineKeyboardButton("PNG", callback_data="extract_format_png")]
    ]
    await query.message.edit_text(
        "Select the image format for extraction:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Extract images from PDFs
async def extract_images(client, query, user_id, image_format):
    pdf_files = user_pdfs.get(user_id, [])
    await query.message.edit_text("Extracting images, please wait...")

    try:
        for pdf_path in pdf_files:
            images = convert_from_path(pdf_path, fmt=image_format, thread_count=4)
            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
            for idx, img in enumerate(images):
                img_bytes = BytesIO()
                img.save(img_bytes, format=image_format.upper())
                img_bytes.seek(0)

                await client.send_document(
                    chat_id=user_id,
                    document=img_bytes,
                    file_name=f"{pdf_name}_page_{idx+1}.{image_format}"
                )

    except Exception as e:
        await query.answer(f"Error during extraction: {str(e)}", show_alert=True)


# Watermark position selection
async def select_watermark_position(client, query, user_id):
    buttons = [
        [InlineKeyboardButton("Top", callback_data="watermark_position_top")],
        [InlineKeyboardButton("Center", callback_data="watermark_position_center")],
        [InlineKeyboardButton("Bottom", callback_data="watermark_position_bottom")]
    ]
    await query.message.edit_text(
        "Select where you want the watermark:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Apply watermark to PDFs
async def watermark_pdf(client, query, user_id, position):
    await query.message.edit_text("Watermarking PDF, please wait...")
    response = await client.ask(user_id, "Send watermark text:")
    watermark_text = response.text or "WATERMARK"

    for pdf_path in user_pdfs.get(user_id, []):
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_path = f"{pdf_path}_watermarked.pdf"
        with open(output_path, "wb") as f_out:
            writer.write(f_out)

        await client.send_document(user_id, document=output_path)
        os.remove(output_path)


# Merge PDFs
async def merge_pdfs(client, query, user_id):
    await query.message.edit_text("Merging PDFs, please wait...")
    merger = PdfMerger()

    for pdf_path in user_pdfs.get(user_id, []):
        merger.append(pdf_path)

    output_path = "merged_output.pdf"
    merger.write(output_path)
    merger.close()

    await client.send_document(user_id, document=output_path)
    os.remove(output_path)


# Clear user data utility
def clear_user_data(user_id, data_type="all"):
    if data_type in ("all", "images"):
        for file_path in user_images.get(user_id, []):
            if os.path.exists(file_path):
                os.remove(file_path)
        user_images[user_id] = []

    if data_type in ("all", "pdfs"):
        for file_path in user_pdfs.get(user_id, []):
            if os.path.exists(file_path):
                os.remove(file_path)
        user_pdfs[user_id] = []
