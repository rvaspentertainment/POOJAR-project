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
from PIL import Image
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

# Initialize the bot to handle both images and PDFs
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

        # Download the new file
        file_path = await message.download()

        # Categorize the file
        if file_path.lower().endswith(IMAGE_FORMATS):
            user_images[user_id].append(file_path)
        elif file_path.lower().endswith(PDF_FORMATS):
            user_pdfs[user_id].append(file_path)

        # Create dynamic buttons based on the uploaded files
        buttons = []
        
        if user_images[user_id]:
            buttons.append([InlineKeyboardButton("Create PDF", callback_data="create_pdf")])
        
        if user_pdfs[user_id]:
            buttons.append([InlineKeyboardButton("Extract Images", callback_data="extract_images")])
            buttons.append([InlineKeyboardButton("Watermark PDF", callback_data="watermark_pdf")])
        
        if len(user_pdfs[user_id]) > 1:
            buttons.append([InlineKeyboardButton("Merge PDFs", callback_data="merge_pdfs")])
        
        if not buttons:
            await message.reply_text("No valid files found. Please send images or PDFs.")
            return

        # Send the message with dynamic buttons
        sent_message = await message.reply_text(
            f"File added! You have {len(user_images[user_id])} image(s) and {len(user_pdfs[user_id])} PDF(s) ready.\n\n"
            "Choose an action to proceed.", 
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        # Store the latest message with buttons
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
        await extract_images(client, query, user_id)

    elif query.data == "watermark_pdf":
        await watermark_pdf(client, query, user_id)

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
        pdf_name = response.text if response.text else "converted"
        pdf_name = "".join(char for char in pdf_name if char.isalnum() or char in " _-").strip()
        pdf_file_name = f"{pdf_name or 'converted'}.pdf"

        pdf_bytes = img2pdf.convert(image_files)
        pdf_output = BytesIO(pdf_bytes)
        pdf_output.seek(0)

        await response.delete()
        await client.send_document(
            chat_id=user_id,
            document=pdf_output,
            file_name=pdf_file_name,
            caption=f"Here is your PDF: **{pdf_file_name}**"
        )

        clear_user_data(user_id, "images")
        await query.answer("PDF created successfully.", show_alert=True)

    except Exception as e:
        await query.answer(f"Error while creating PDF: {str(e)}", show_alert=True)


# Extract images from PDFs
async def extract_images(client, query, user_id):
    pdf_files = user_pdfs.get(user_id, [])
    if not pdf_files:
        await query.answer("No PDF files available for extraction.", show_alert=True)
        return

    await query.message.edit_text("Extracting images from PDFs, please wait...")

    try:
        for pdf_path in pdf_files:
            images = convert_from_path(pdf_path, fmt='png')
            for idx, img in enumerate(images):
                img_bytes = BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                await client.send_document(
                    chat_id=user_id,
                    document=img_bytes,
                    file_name=f"page_{idx+1}.png"
                )

        clear_user_data(user_id, "pdfs")
        await query.answer("Images extracted successfully.", show_alert=True)

    except Exception as e:
        await query.answer(f"Error during extraction: {str(e)}", show_alert=True)


# Watermark PDF
async def watermark_pdf(client, query, user_id):
    pdf_files = user_pdfs.get(user_id, [])
    if not pdf_files:
        await query.answer("No PDF files available for watermarking.", show_alert=True)
        return

    response = await client.ask(user_id, "Send watermark text:")
    watermark_text = response.text or "WATERMARK"

    await query.message.edit_text("Applying watermark, please wait...")

    try:
        for pdf_path in pdf_files:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            output_path = f"{pdf_path}_watermarked.pdf"
            with open(output_path, "wb") as f_out:
                writer.write(f_out)

            await client.send_document(user_id, document=output_path)
            os.remove(output_path)

        clear_user_data(user_id, "pdfs")
        await query.answer("Watermark applied successfully.", show_alert=True)

    except Exception as e:
        await query.answer(f"Error during watermarking: {str(e)}", show_alert=True)


# Merge PDFs
async def merge_pdfs(client, query, user_id):
    pdf_files = user_pdfs.get(user_id, [])
    if len(pdf_files) < 2:
        await query.answer("Need at least 2 PDFs to merge.", show_alert=True)
        return

    await query.message.edit_text("Merging PDFs, please wait...")

    merger = PdfMerger()

    try:
        for pdf_path in pdf_files:
            merger.append(pdf_path)

        output_path = "merged_output.pdf"
        merger.write(output_path)
        merger.close()

        await client.send_document(user_id, document=output_path)
        os.remove(output_path)

        clear_user_data(user_id, "pdfs")
        await query.answer("PDFs merged successfully.", show_alert=True)

    except Exception as e:
        await query.answer(f"Error during merging: {str(e)}", show_alert=True)


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
