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
from pdf_utils import (
    merge_pdfs,
    split_pdf,
    pdf_to_images,
    add_watermark,
    extract_text_from_pdf,
    compress_pdf,
    pdf_to_doc,
    pdf_to_txt,
    add_password,
    remove_password,
)

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
        file_name = file_name.replace(c, "")
    file_name = '@VJ_Botz ' + ' '.join(filter(lambda x: not x.startswith('http') and not x.startswith('@') and not x.startswith('www.'), file_name.split()))
    return file_name

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    await message.reply(script.START_MESSAGE.format(message.from_user.mention))


@Client.on_message(filters.command("help") & filters.incoming)
async def help_command(client, message):
    await message.reply(script.HELP_MESSAGE)


@Client.on_message(filters.command("merge") & filters.incoming)
async def merge_command(client, message):
    await message.reply(script.MERGE_INSTRUCTIONS)


@Client.on_message(filters.command("split") & filters.incoming)
async def split_command(client, message):
    await message.reply(script.SPLIT_INSTRUCTIONS)


@Client.on_message(filters.command("topdf") & filters.incoming)
async def topdf_command(client, message):
    await message.reply(script.TOPDF_INSTRUCTIONS)


@Client.on_message(filters.command("watermark") & filters.incoming)
async def watermark_command(client, message):
    await message.reply(script.WATERMARK_INSTRUCTIONS)


@Client.on_message(filters.command("extracttext") & filters.incoming)
async def extracttext_command(client, message):
    await message.reply(script.EXTRACTTEXT_INSTRUCTIONS)


@Client.on_message(filters.command("compress") & filters.incoming)
async def compress_command(client, message):
    await message.reply(script.COMPRESS_INSTRUCTIONS)


@Client.on_message(filters.command("topng") & filters.incoming)
async def topng_command(client, message):
    await message.reply(script.TOPNG_INSTRUCTIONS)


@Client.on_message(filters.command("totxt") & filters.incoming)
async def totxt_command(client, message):
    await message.reply(script.TOTXT_INSTRUCTIONS)


@Client.on_message(filters.command("addpassword") & filters.incoming)
async def addpassword_command(client, message):
    await message.reply(script.ADDPASSWORD_INSTRUCTIONS)


@Client.on_message(filters.command("removepassword") & filters.incoming)
async def removepassword_command(client, message):
    await message.reply(script.REMOVEPASSWORD_INSTRUCTIONS)


@Client.on_message(filters.document & filters.private)
async def handle_document(client, message):
    if not message.document.mime_type.startswith("application/pdf"):
        await message.reply("Please send a PDF file for processing.")
        return

    file_name = message.document.file_name
    file_id = message.document.file_id
    file_size = message.document.file_size

    if file_size > 20 * 1024 * 1024:  # Limit to 20MB for processing
        await message.reply("File size is too large. Please send a file under 20MB.")
        return

    await message.reply(f"Received file: `{file_name}` ({get_size(file_size)}). What do you want to do with it?",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Merge with another PDF", callback_data=f"merge_{file_id}"),
                                    InlineKeyboardButton("Split PDF", callback_data=f"split_{file_id}")
                                ],
                                [
                                    InlineKeyboardButton("Convert to Images", callback_data=f"topng_{file_id}"),
                                    InlineKeyboardButton("Extract Text", callback_data=f"extracttext_{file_id}")
                                ],
                                [
                                    InlineKeyboardButton("Add Watermark", callback_data=f"watermark_{file_id}"),
                                    InlineKeyboardButton("Compress PDF", callback_data=f"compress_{file_id}")
                                ],
                                [
                                    InlineKeyboardButton("Convert to DOC", callback_data=f"todoc_{file_id}"),
                                    InlineKeyboardButton("Convert to TXT", callback_data=f"totxt_{file_id}")
                                ],
                                [
                                    InlineKeyboardButton("Add Password", callback_data=f"addpassword_{file_id}"),
                                    InlineKeyboardButton("Remove Password", callback_data=f"removepassword_{file_id}")
                                ],
                                [InlineKeyboardButton("Close", callback_data="close_data")]
                            ]
                        ))


@Client.on_callback_query(filters.regex(r"^merge_"))
async def merge_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    if query.message.chat.id not in BATCH_FILES:
        BATCH_FILES[query.message.chat.id] = []
    BATCH_FILES[query.message.chat.id].append(file_id)
    await query.answer("Added file for merging. Send another PDF or press 'Merge Now'.")
    if len(BATCH_FILES[query.message.chat.id]) > 1:
        await query.message.edit_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("Merge Now", callback_data="merge_now")]])
        )


@Client.on_callback_query(filters.regex("^merge_now$"))
async def merge_now_callback(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    if chat_id not in BATCH_FILES or len(BATCH_FILES[chat_id]) < 2:
        await query.answer("Please send at least two PDF files to merge.", show_alert=True)
        return

    file_ids = BATCH_FILES[chat_id]
    del BATCH_FILES[chat_id]

    await query.message.edit("Downloading files for merging...")
    file_paths = []
    for file_id in file_ids:
        file_path = await client.download_media(file_id)
        file_paths.append(file_path)

    await query.message.edit("Merging PDF files...")
    try:
        output_path = f"merged_{random.randint(1000, 9999)}.pdf"
        await merge_pdfs(file_paths, output_path)
        await client.send_document(chat_id, output_path, caption="Merged PDF")
    except Exception as e:
        await query.message.edit(f"Error during merging: {e}")
    finally:
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(output_path):
            os.remove(output_path)
        await query.message.delete()


@Client.on_callback_query(filters.regex(r"^split_"))
async def split_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Please specify the page numbers to split (e.g., 1,3-5,7).")
    try:
        response = await client.listen(query.message.chat.id, filters=filters.text, timeout=30)
        if response:
            pages = response.text
            await query.message.edit("Downloading PDF for splitting...")
            file_path = await client.download_media(file_id)
            await query.message.edit(f"Splitting PDF at pages: {pages}...")
            output_prefix = f"split_{random.randint(1000, 9999)}"
            try:
                output_files = await split_pdf(file_path, pages, output_prefix)
                for output_file in output_files:
                    await client.send_document(query.message.chat.id, output_file, caption=f"Split part: {os.path.basename(output_file)}")
            except Exception as e:
                await query.message.edit(f"Error during splitting: {e}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                for file in output_files:
                    if os.path.exists(file):
                        os.remove(file)
            await query.message.delete()
        else:
            await query.message.edit("Split process cancelled due to timeout.")
    except asyncio.TimeoutError:
        await query.message.edit("Split process cancelled due to timeout.")


@Client.on_callback_query(filters.regex(r"^topng_"))
async def topng_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Downloading PDF for conversion to images...")
    file_path = await client.download_media(file_id)
    await query.message.edit("Converting PDF to images...")
    try:
        output_dir = f"images_{random.randint(1000, 9999)}"
        os.makedirs(output_dir)
        image_files = await pdf_to_images(file_path, output_dir)
        for image_file in image_files:
            await client.send_photo(query.message.chat.id, image_file, caption=os.path.basename(image_file))
    except Exception as e:
        await query.message.edit(f"Error during conversion to images: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)
        await query.message.delete()


@Client.on_callback_query(filters.regex(r"^watermark_"))
async def watermark_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Please send the watermark text.")
    try:
        response = await client.listen(query.message.chat.id, filters=filters.text, timeout=30)
        if response:
            watermark_text = response.text
            await query.message.edit("Downloading PDF for adding watermark...")
            file_path = await client.download_media(file_id)
            await query.message.edit(f"Adding watermark: '{watermark_text}'...")
            output_path = f"watermarked_{random.randint(1000, 9999)}.pdf"
            try:
                await add_watermark(file_path, watermark_text, output_path)
                await client.send_document(query.message.chat.id, output_path, caption=f"PDF with watermark: '{watermark_text}'")
            except Exception as e:
                await query.message.edit(f"Error adding watermark: {e}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            await query.message.delete()
        else:
            await query.message.edit("Watermark process cancelled due to timeout.")
    except asyncio.TimeoutError:
        await query.message.edit("Watermark process cancelled due to timeout.")


@Client.on_callback_query(filters.regex(r"^extracttext_"))
async def extracttext_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Downloading PDF for text extraction...")
    file_path = await client.download_media(file_id)
    await query.message.edit("Extracting text...")
    try:
        text = await extract_text_from_pdf(file_path)
        if len(text) > 4096:
            # Split text into chunks and send as separate messages
            for i in range(0, len(text), 4096):
                await client.send_message(query.message.chat.id, text[i:i + 4096])
        else:
            await client.send_message(query.message.chat.id, text)
    except Exception as e:
        await query.message.edit(f"Error during text extraction: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        await query.message.delete()


@Client.on_callback_query(filters.regex(r"^compress_"))
async def compress_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Downloading PDF for compression...")
    file_path = await client.download_media(file_id)
    await query.message.edit("Compressing PDF...")
    output_path = f"compressed_{random.randint(1000, 9999)}.pdf"
    try:
        await compress_pdf(file_path, output_path)
        await client.send_document(query.message.chat.id, output_path, caption="Compressed PDF")
    except Exception as e:
        await query.message.edit(f"Error during compression: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        await query.message.delete()


@Client.on_callback_query(filters.regex(r"^todoc_"))
async def todoc_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Downloading PDF for conversion to DOC...")
    file_path = await client.download_media(file_id)
    await query.message.edit("Converting to DOC...")
    output_path = f"converted_{random.randint(1000, 9999)}.docx"
    try:
        await pdf_to_doc(file_path, output_path)
        await client.send_document(query.message.chat.id, output_path, caption="Converted to DOC")
    except Exception as e:
        await query.message.edit(f"Error during conversion to DOC: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        await query.message.delete()


@Client.on_callback_query(filters.regex(r"^totxt_"))
async def totxt_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Downloading PDF for conversion to TXT...")
    file_path = await client.download_media(file_id)
    await query.message.edit("Converting to TXT...")
    output_path = f"converted_{random.randint(1000, 9999)}.txt"
    try:
        await pdf_to_txt(file_path, output_path)
        await client.send_document(query.message.chat.id, output_path, caption="Converted to TXT")
    except Exception as e:
        await query.message.edit(f"Error during conversion to TXT: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        await query.message.delete()



@Client.on_callback_query(filters.regex(r"^addpassword_"))
async def addpassword_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Please send the password to add to the PDF.")
    try:
        response = await client.listen(query.message.chat.id, filters=filters.text, timeout=30)  # Adjust timeout as needed
        if response:
            password = response.text
            await query.message.edit("Downloading PDF...")
            file_path = await client.download_media(file_id)
            await query.message.edit("Adding password...")
            output_path = f"protected_{random.randint(1000, 9999)}.pdf"
            try:
                await add_password(file_path, password, output_path)
                await client.send_document(query.message.chat.id, output_path, caption="PDF with password protection added.")
            except Exception as e:
                await query.message.edit(f"Error adding password: {e}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            await query.message.delete()
        else:
            await query.message.edit("Add password process cancelled due to timeout.")
    except asyncio.TimeoutError:
        await query.message.edit("Add password process cancelled due to timeout.")



@Client.on_callback_query(filters.regex(r"^removepassword_"))
async def removepassword_callback(client: Client, query: CallbackQuery):
    file_id = query.data.split("_")[1]
    await query.message.edit("Downloading PDF...")
    file_path = await client.download_media(file_id)
    await query.message.edit("Removing password...")
    output_path = f"unprotected_{random.randint(1000, 9999)}.pdf"
    try:
        await remove_password(file_path, output_path)
        await client.send_document(query.message.chat.id, output_path, caption="PDF password protection removed.")
    except Exception as e:
        await query.message.edit(f"Error removing password: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        await query.message.delete()
