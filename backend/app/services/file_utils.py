from pathlib import Path

import fitz

STATIC_IMG_FILES_DIR = Path("/app/static/document_files_images")


def generate_file_url(file_path: str) -> str:
    return f"http://localhost/static/document_files/{file_path}"


def convert_pdf_to_images(pdf_path, output_dir):
    """
    Convert each page of a PDF to an image and save to the output directory.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Path to the directory where images will be saved.
    """
    pdf_document = fitz.open(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        output_path = output_dir / f"page_{page_num + 1}.png"
        pix.save(output_path)
