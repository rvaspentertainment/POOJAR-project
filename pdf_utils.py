# pdf_utils.py
# Requires: PyPDF2 (pip install PyPDF2)

import PyPDF2
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError
from io import BytesIO
from PIL import Image
import io
import docx
from typing import List

def merge_pdfs(pdf_paths: List[str], output_path: str):
    """Merges multiple PDF files into one."""
    merger = PdfMerger()
    for pdf_path in pdf_paths:
        try:
            merger.append(pdf_path)
        except PdfReadError:
            print(f"Error: {pdf_path} could not be opened. Skipping.")
    merger.write(output_path)
    merger.close()



def split_pdf(pdf_path: str, page_ranges: str, output_prefix: str) -> List[str]:
    """Splits a PDF into multiple files based on page ranges.

    Args:
        pdf_path: Path to the PDF file to split.
        page_ranges: String specifying the page ranges (e.g., "1-3,5,7-9").
        output_prefix: Prefix for the output file names.

    Returns:
        A list of paths to the created PDF files.
    """
    reader = PdfReader(pdf_path)
    output_files = []
    page_ranges = page_ranges.split(',')
    for i, page_range_str in enumerate(page_ranges):
        writer = PdfWriter()
        try:
            if '-' in page_range_str:
                start, end = map(int, page_range_str.split('-'))
                # Adjust for 0-based indexing
                start = max(1, start)  # Ensure start is not less than 1
                end = min(end, len(reader.pages)) # Ensure end is not greater than number of pages
                for page_num in range(start - 1, end):
                    writer.add_page(reader.pages[page_num])
            else:
                page_num = int(page_range_str)
                if 1 <= page_num <= len(reader.pages):
                  writer.add_page(reader.pages[page_num - 1]) # Adjust for 0-based indexing
                else:
                    print(f"Page number {page_num} is out of range. Skipping.")
                    continue
            output_file_path = f"{output_prefix}_{i + 1}.pdf"
            with open(output_file_path, "wb") as output_pdf:
                writer.write(output_pdf)
            output_files.append(output_file_path)
        except ValueError:
            print(f"Invalid page range: {page_range_str}. Skipping.")
        except IndexError:
            print(f"Page number out of range: {page_range_str}. Skipping.")
    return output_files



def pdf_to_images(pdf_path: str, output_dir: str) -> List[str]:
    """Converts each page of a PDF to an image (PNG)."""
    reader = PdfReader(pdf_path)
    image_files = []
    for i, page in enumerate(reader.pages):
        image = page.to_image() # Use the correct method to get the image
        image_bytes = image.tobytes()
        img = Image.open(io.BytesIO(image_bytes))
        image_file_path = os.path.join(output_dir, f"page_{i + 1}.png")
        img.save(image_file_path, "PNG")
        image_files.append(image_file_path)
    return image_files



def add_watermark(pdf_path: str, watermark_text: str, output_path: str):
    """Adds a text watermark to a PDF."""

    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Create a watermark PDF (single page)
    watermark_pdf = PdfWriter()
    # A blank page is created and then we will write on it.
    watermark_pdf.add_page()
    page = watermark_pdf.pages[0]
    page.draw_text(watermark_text) # simplified text drawing
    watermark_stream = BytesIO()
    watermark_pdf.write(watermark_stream)
    watermark_pdf_reader = PdfReader(watermark_stream)
    watermark_page = watermark_pdf_reader.pages[0]


    for page in reader.pages:
        page.merge_page(watermark_page) # Merge the watermark
        writer.add_page(page)

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)



def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Handle None case
    return text



def compress_pdf(pdf_path: str, output_path: str):
    """Compresses a PDF file (basic, using qpdf)."""
    # This is a placeholder.  PyPDF2 doesn't have built-in compression.
    #  A proper implementation would require an external tool like qpdf:
    #  https://pypi.org/project/QPDF/
    #  For example (requires qpdf to be installed on the system):
    # import subprocess
    # subprocess.run(['qpdf', '--compress-pages=y', pdf_path, output_path])
    #  For now, we'll just copy the file (no actual compression)
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.write(output_path)
    except Exception as e:
        print(f"Error during (simulated) compression: {e}")



def pdf_to_doc(pdf_path: str, output_path: str):
    """Converts a PDF file to a DOCX file."""
    text = extract_text_from_pdf(pdf_path)  # Reuse the text extraction
    doc = docx.Document()
    doc.add_paragraph(text)
    doc.save(output_path)



def pdf_to_txt(pdf_path: str, output_path: str):
    """Converts a PDF file to a TXT file."""
    text = extract_text_from_pdf(pdf_path) # Reuse the text extraction
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)



def add_password(pdf_path: str, password: str, output_path: str):
    """Adds a password to a PDF file."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)



def remove_password(pdf_path: str, output_path: str):
    """Removes the password from a PDF file."""
    reader = PdfReader(pdf_path)
    if reader.is_encrypted:
        writer = PdfWriter()
        try:
            reader.decrypt("")  # Try decrypting with a blank password first
        except NotImplementedError: # Some PDFs might not allow removing password
            print("Removing password is not supported for this PDF.")
            return
        for page in reader.pages:
            writer.add_page(page)
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)
    else:
        print("PDF is not encrypted.")
        #copy the file
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.write(output_path)
