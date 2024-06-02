import io
import logging
import os
import PyPDF2
import random
import string
import hashlib
from app.models.models import FieldType
from pathlib import Path
from typing import Optional, List
from jose import JWTError, jwt
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.utils import send_email
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.colors import black

# Register a handwriting-like font
registerFont(TTFont("Handwriting", "static/fonts/Allura-Regular.ttf"))

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("/app/static/document_files")


def save_file(file: UploadFile, user_id: int) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    new_filename = f"{user_id}_{file.filename}"
    save_path = UPLOAD_DIR / new_filename
    with open(save_path, "wb") as f:
        f.write(file.file.read())
    return str(save_path)


def file_existence(file_path: str) -> bool:
    file_abs_path = UPLOAD_DIR / file_path
    if not file_abs_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return True


def verify_secure_link_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        expiration = payload.get("exp")
        if expiration and datetime.fromtimestamp(expiration) < datetime.now():
            logger.error("Token has expired")
            return None
        logger.info(f"the decoded token is:  {payload}")
        return payload
    except JWTError:
        logger.error("Failed to decode JWT token")
        return None


def generate_otp() -> str:
    return "".join(random.choices(string.digits, k=6))


def send_otp_code(email: str, otp: int) -> bool:
    subject = "Your OTP Code"
    html_content = f"<p>Your OTP code is: {otp}</p>"
    response = send_email(email_to=email, subject=subject,
                          html_content=html_content)
    return response.status_code == 250


def generate_secure_link(
    expiry_date: datetime,
    signature_request_id: int,
    email: str,
    document_ids: List[int],
    signatory_id: int,
) -> str:
    expiration = expiry_date
    payload = {
        "signature_request_id": signature_request_id,
        "sub": email,
        "exp": expiration,
        "document_ids": document_ids,
        "signatory_id": signatory_id,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    secure_link = f"{settings.FRONTEND_URL}/api/v1/signe/sign_document?token={token}"
    return secure_link


def apply_pdf_security(pdf_path: str):
    """
    Apply security settings to a PDF to allow only printing and printing in high resolution.
    """
    reader = PyPDF2.PdfReader(pdf_path)
    writer = PyPDF2.PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Combine permissions for printing and high-resolution printing
    permissions_flag = (
        0b0100 | 0b0001_0000_0000_0000  # Printing  # Printing in High Resolution
    )

    writer.encrypt(
        user_password="",
        owner_password=settings.SECRET_KEY,
        use_128bit=True,
        permissions_flag=permissions_flag,
    )

    with open(pdf_path, "wb") as f:
        writer.write(f)


def draw_signature_field(c, field, signatory):
    logger.info(
        f"""
        Drawing signature field for signatory:
        {signatory.first_name} {signatory.last_name} at ({field.x}, {field.y})
        with dimensions ({field.width}, {field.height})
        """
    )
    if signatory.signature_image:
        logger.info(f"Using signature image at {signatory.signature_image}")
        c.drawImage(
            signatory.signature_image, field.x, field.y, field.width, field.height
        )
    else:
        logger.info("Using handwritten font for signature")
        c.setFont("Handwriting", 24)
        c.setFillColor(black)
        c.drawString(field.x, field.y,
                     f"{signatory.first_name} {signatory.last_name}")
    c.rect(field.x, field.y - 10, field.width, field.height)


def draw_text_field(c, field):
    c.drawString(field.x, field.y, field.text)


def draw_mention_field(c, field):
    c.drawString(field.x, field.y, field.mention)


def draw_read_only_text_field(c, field):
    c.drawString(field.x, field.y, field.text)


def draw_checkbox_field(c, field):
    c.rect(field.x, field.y, field.width, field.height)
    if field.checked:
        c.line(field.x, field.y, field.x + field.width, field.y + field.height)
        c.line(field.x + field.width, field.y, field.x, field.y + field.height)


def draw_radio_group_field(c, field):
    for radio in field.radios:
        c.circle(radio.x, radio.y, radio.size / 2)
        if radio.checked:
            c.circle(radio.x, radio.y, radio.size / 4, fill=1)


def draw_doc_field(c, field, signatory):
    logger.info(f"Drawing field type: {field.type}")
    if field.type == FieldType.SIGNATURE:
        draw_signature_field(c, field, signatory)
    elif field.type == FieldType.TEXT:
        draw_text_field(c, field)
    elif field.type == FieldType.MENTION:
        draw_mention_field(c, field)
    elif field.type == FieldType.READ_ONLY_TEXT:
        draw_read_only_text_field(c, field)
    elif field.type == FieldType.CHECKBOX:
        draw_checkbox_field(c, field)
    elif field.type == FieldType.RADIO_GROUP:
        draw_radio_group_field(c, field)


def add_fields_to_pdf(file_path, field, signatory):
    logger.info(f"Adding fields to PDF: {file_path}")
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 12)

    draw_doc_field(can, field, signatory)
    can.save()

    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    existing_pdf = PyPDF2.PdfReader(open(file_path, "rb"))
    output = PyPDF2.PdfWriter()

    # Define new folder path
    new_folder_path = UPLOAD_DIR / "signed_documents"
    new_folder_path.mkdir(exist_ok=True)  # Make sure the directory exists

    # Create new file path in the signed_documents folder
    new_file_path = new_folder_path / Path(file_path).name

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        if i == field.page - 1:
            logger.info(f"Merging new content to page {i}")
            page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    logger.info(f"Writing updated PDF to {new_file_path}")
    with open(new_file_path, "wb") as outputStream:
        output.write(outputStream)


def generate_pdf_hash(file_path):
    with open(file_path, "rb") as f:
        file_content = f.read()
    return hashlib.sha256(file_content).hexdigest()
