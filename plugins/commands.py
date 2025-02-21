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



user_pdfs = {}
last_message = {}

# Watermark settings
WATERMARK_TEXT = "poojar project"
WATERMARK_POSITION = "bottom_right"

@Client.on_message(
    filters.private & 
    filters.document & 
    filters.regex(r"\.pdf$", flags=2) & 
    filters.incoming
)
async def collect_pdfs(bot, message):
    try:
        user_id = message.from_user.id

        
        # Download the PDF file
        file_path = await message.download()
        user_pdfs[user_id] = file_path

        # Send options for PDF editing
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Watermark", callback_data="add_watermark")],
            [InlineKeyboardButton("Protect with Password", callback_data="protect_pdf")],
            [InlineKeyboardButton("Extract Images (JPEG)", callback_data="extract_jpeg")],
            [InlineKeyboardButton("Extract Images (PNG)", callback_data="extract_png")]
        ])
        
        await message.reply_text(
            "PDF received! Choose an action to perform on this PDF:",
            reply_markup=buttons
        )

        

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")




    


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    pdf_path = user_pdfs.get(user_id)

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

    elif query.data == "add_watermark":
        await query.message.edit_text("Adding watermark to your PDF...")
        
        try:
            # Apply watermark to each page
            watermarked_path = f"{os.path.splitext(pdf_path)[0]}_watermarked.pdf"
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                page.merge_page(create_watermark_page(page))
                writer.add_page(page)

            with open(watermarked_path, "wb") as f:
                writer.write(f)

            await client.send_document(
                chat_id=user_id,
                document=watermarked_path,
                file_name="watermarked.pdf",
                caption="Here is your watermarked PDF!"
            )

            os.remove(watermarked_path)

        except Exception as e:
            await query.answer(f"Failed to add watermark: {e}", show_alert=True)

    elif query.data == "protect_pdf":
        await query.message.edit_text("Send the password to protect the PDF:")
        
        response = await client.ask(user_id, "**Send the password for the PDF:**")
        pdf_password = response.text

        try:
            # Protect PDF with password
            protected_path = f"{os.path.splitext(pdf_path)[0]}_protected.pdf"
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(pdf_password)

            with open(protected_path, "wb") as f:
                writer.write(f)

            await client.send_document(
                chat_id=user_id,
                document=protected_path,
                file_name="protected.pdf",
                caption="Here is your password-protected PDF!"
            )

            os.remove(protected_path)

        except Exception as e:
            await query.answer(f"Failed to protect PDF: {e}", show_alert=True)

    elif query.data in ["extract_jpeg", "extract_png"]:
        await query.message.edit_text("Extracting images from your PDF...")

        try:
            image_format = "JPEG" if query.data == "extract_jpeg" else "PNG"
            reader = PdfReader(pdf_path)
            images = []

            for page_number, page in enumerate(reader.pages, start=1):
                for image_index, image_file in enumerate(page.images, start=1):
                    image_data = image_file.data
                    image_name = f"page_{page_number}_img_{image_index}.{image_format.lower()}"
                    image_path = os.path.join("/tmp", image_name)

                    with open(image_path, "wb") as img_file:
                        img_file.write(image_data)

                    images.append(image_path)

            if images:
                for image_path in images:
                    await client.send_document(
                        chat_id=user_id,
                        document=image_path,
                        file_name=os.path.basename(image_path)
                    )
                    os.remove(image_path)
            else:
                await query.answer("No images found in the PDF.", show_alert=True)

        except Exception as e:
            await query.answer(f"Failed to extract images: {e}", show_alert=True)

    elif query.data == "delete_pdf":
        await query.message.edit_text("Deleting your PDF...")

        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        user_pdfs[user_id] = None

        await query.answer("Your PDF has been deleted.", show_alert=True)




def create_watermark_page(page):
    """Creates a watermark page for merging."""
    from PyPDF2.pdf import PageObject
    watermark = PageObject.create_blank_page(width=page.mediaBox.getWidth(), height=page.mediaBox.getHeight())

    # Adding simple text as watermark
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    from reportlab.lib.pagesizes import letter

    c = canvas.Canvas("watermark.pdf", pagesize=letter)
    c.setFont("Helvetica", 20)
    c.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.5)
    c.drawString(100, 100, WATERMARK_TEXT)
    c.save()

    watermark.merge_page(PageObject.create_from_file("watermark.pdf"))
    os.remove("watermark.pdf")
    
    return watermark


