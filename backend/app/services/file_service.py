import hashlib
import io
import logging
import os
import random
import string
from datetime import datetime
from pathlib import Path

import PyPDF2
from fastapi import HTTPException, UploadFile
from jose import JWTError, jwt
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from app.core.config import settings
from app.models.models import FieldType
from app.utils import send_email

# Register a handwriting-like font
registerFont(TTFont("Handwriting", "static/fonts/Allura-Regular.ttf"))

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("/app/static/document_files")


def generate_unique_filename(user_id: int, original_filename: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    file_extension = Path(original_filename).suffix
    unique_filename = f"{user_id}_{timestamp}_{random_string}{file_extension}"
    return unique_filename


def save_file(file: UploadFile, user_id: int) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_filename = generate_unique_filename(user_id, file.filename)
    save_path = UPLOAD_DIR / unique_filename
    with open(save_path, "wb") as f:
        f.write(file.file.read())
    return str(save_path)


def file_existence(file_path: str) -> bool:
    file_abs_path = UPLOAD_DIR / file_path
    if not file_abs_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return True


def verify_secure_link_token(token: str) -> dict | None:
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
    response = send_email(email_to=email, subject=subject, html_content=html_content)
    return response.status_code == 250


def generate_secure_link(
    expiry_date: datetime,
    signature_request_id: int,
    email: str,
    document_ids: list[int],
    signatory_id: int,
    require_otp: bool,
) -> str:
    expiration = expiry_date
    payload = {
        "signature_request_id": signature_request_id,
        "sub": email,
        "exp": expiration,
        "document_ids": document_ids,
        "signatory_id": signatory_id,
        "require_otp": require_otp,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    secure_link = f"{settings.FRONTEND_URL}/api/v1/signe/sign_document?token={token}"
    return secure_link, token


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
        Drawing signature field for signatory {signatory.id}:
        {signatory.first_name} {signatory.last_name} at ({field.x}, {field.y})
        with dimensions ({field.width}, {field.height})
        """
    )
    if signatory.signature_image:
        logger.info(f"Using signature image at {signatory.signature_image}")
        try:
            image = ImageReader(signatory.signature_image)
            c.drawImage(
                image,
                field.x,
                field.y,
                width=field.width,
                height=field.height,
                mask="auto",
            )
        except Exception as e:
            logger.error(f"Failed to draw signature image: {e}")
            # Fallback to handwritten font if image drawing fails
            c.setFont("Handwriting", 24)
            c.setFillColor(black)
            c.drawString(
                field.x, field.y, f"{signatory.first_name} {signatory.last_name}"
            )
    else:
        logger.info("Using handwritten font for signature")
        c.setFont("Handwriting", 24)
        c.setFillColor(black)
        c.drawString(field.x, field.y, f"{signatory.first_name} {signatory.last_name}")
    # c.rect(field.x, field.y - 10, field.width, field.height)


def draw_text_field(c, field):
    c.drawString(field.x, field.y, field.text)


def draw_mention_field(c, field):
    c.drawString(field.x, field.y, f"{field.mention}")


def draw_read_only_text_field(c, field):
    c.drawString(field.x, field.y, field.text)


def draw_checkbox_field(c, field):
    if field.checked:
        # Adjusting the size for drawing the check, to fit within the expected box size
        check_mark_size = field.size / 2
        start_x = field.x
        start_y = field.y
        end_x = start_x + check_mark_size
        end_y = start_y + check_mark_size

        # Draw a simple check mark (like a tick)
        # This draws one line from bottom left to top right
        c.line(start_x, start_y, end_x, end_y)

        # Optional: Add another line from top left to bottom right to form an 'X'
        c.line(start_x, end_y, end_x, start_y)


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


def add_fields_to_pdf(document_filename, field, signatory, owner_id):
    base_path = UPLOAD_DIR / f"{document_filename}"
    signed_path = UPLOAD_DIR / "signed_documents" / f"{document_filename}"

    # Check if file exists in 'signed_documents'
    file_path = signed_path if signed_path.exists() else base_path

    logger.info(f"Adding fields to PDF: {file_path}")
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    draw_doc_field(can, field, signatory)
    can.save()

    # Process the PDF modifications
    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    existing_pdf = PyPDF2.PdfReader(open(file_path, "rb"))
    output = PyPDF2.PdfWriter()

    target_page_index = field.page - 1  # Assuming 'page' is 1-indexed
    for page_number, page in enumerate(existing_pdf.pages):
        if page_number == target_page_index:
            if new_pdf.pages:
                page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    # Saving the modified PDF
    if "signed_documents" not in str(file_path):
        new_folder_path = file_path.parent / "signed_documents"
        new_folder_path.mkdir(exist_ok=True)
        new_file_name = file_path.name
        new_file_path = new_folder_path / new_file_name
    else:
        new_file_path = file_path

    with open(new_file_path, "wb") as outputStream:
        output.write(outputStream)

    logger.info(f"Written updated PDF to {new_file_path}")


def generate_pdf_hash(file_path):
    with open(file_path, "rb") as f:
        file_content = f.read()
    return hashlib.sha256(file_content).hexdigest()
