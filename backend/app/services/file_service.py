import hashlib
import io
import logging
import os
import random
import string
from datetime import datetime
from pathlib import Path

from app.services.file_utils import convert_pdf_to_images
from sqlmodel import select

import PyPDF2
from fastapi import HTTPException, UploadFile, status
from jose import JWTError, jwt
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from app.core.config import settings
from app.crud import audit_log_crud, document_crud, signed_document_crud
from app.models.models import (
    AuditLogAction,
    DocumentStatus,
    FieldType,
    RequestSignatoryLink,
    Signatory,
    SignatureRequest,
    SignatureRequestStatus,
)
from app.schemas.schemas import AuditLogCreate, DocumentSignatureDetailsCreate
from app.utils import (
    send_email,
    # send_signature_request_email,
    send_signature_request_notification_email,
)

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


def handle_single_signatory(signature_request_data, db, request):
    signatory = signature_request_data.signatories[0]
    secure_link, token = generate_secure_link(
        signature_request_data.expiry_date,
        signature_request_data.id,
        signatory.email,
        [document.id for document in signature_request_data.documents],
        signatory.id,
        signature_request_data.require_otp,
    )
    send_email_and_update_status(
        email=signatory.email,
        link=secure_link,
        message=signature_request_data.message,
        documents=signature_request_data.documents,
        db=db,
        signature_request_data=signature_request_data,
        request=request,
        token=token,
    )


def handle_multiple_signatories(signature_request_data, db, request):
    signature_request_data.signatories.sort(key=lambda s: s.signing_order)
    if signature_request_data.ordered_signers:
        first_signatory = signature_request_data.signatories[0]
        secure_link, token = generate_secure_link(
            signature_request_data.expiry_date,
            signature_request_data.id,
            first_signatory.email,
            [document.id for document in signature_request_data.documents],
            first_signatory.id,
            signature_request_data.require_otp,
        )
        send_email_and_update_status(
            email=first_signatory.email,
            link=secure_link,
            message=signature_request_data.message,
            documents=signature_request_data.documents,
            db=db,
            signature_request_data=signature_request_data,
            request=request,
            token=token,
        )
    else:
        for signatory in signature_request_data.signatories:
            secure_link, token = generate_secure_link(
                signature_request_data.expiry_date,
                signature_request_data.id,
                signatory.email,
                [document.id for document in signature_request_data.documents],
                signatory.id,
                signature_request_data.require_otp,
            )
            send_email_and_update_status(
                email=signatory.email,
                link=secure_link,
                message=signature_request_data.message,
                documents=signature_request_data.documents,
                db=db,
                signature_request_data=signature_request_data,
                request=request,
                token=token,
            )


def send_email_and_update_status(
    email, link, message, documents, db, signature_request_data, request, token
):
    """
    email_response = send_signature_request_email(
        email_to=email,
        document_title="signature request",
        link=link,
        message=message,
    )

    if email_response and email_response.status_code == 250:
        update_document_statuses(documents, db)
        update_signature_request_status(signature_request_data, db, token, request)
    else:
        handle_email_failure(email_response)
    """
    update_document_statuses(documents, db)
    update_signature_request_status(signature_request_data, db, token, request)


def update_document_statuses(documents, db):
    for document_element in documents:
        document = document_crud.get_document_by_id(db, document_element.id)
        if document:
            document.status = DocumentStatus.SENT_FOR_SIGNATURE
            db.add(document)
    db.commit()


def update_signature_request_status(signature_request_data, db, token, request):
    signature_request_data.status = SignatureRequestStatus.SENT
    signature_request_data.token = token
    db.add(signature_request_data)
    db.commit()
    db.refresh(signature_request_data)

    audit_log_crud.create_audit_log(
        db,
        AuditLogCreate(
            description="Signature request initiated",
            ip_address=request.client.host,
            action=AuditLogAction.SIGNATURE_REQUESTED,
            signature_request_id=signature_request_data.id,
        ),
    )

    send_notification_email(signature_request_data)


def send_notification_email(signature_request_data):
    notification_email_response = send_signature_request_notification_email(
        signature_request_data.sender.email,
        signature_request_data.name,
        signature_request_data.id,
        signature_request_data.status.value,
    )

    if (
        notification_email_response is not None
        and notification_email_response.status_code == 250
    ):
        logging.info("Notification email sent successfully.")
    else:
        error_detail = "Failed to send notification email due to server error."
        if notification_email_response:
            error_detail += f" Server responded with status: {notification_email_response.status_code}."
        logging.error(error_detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail,
        )


def handle_email_failure(email_response):
    error_message = f"""
        Failed to send email: {email_response.status_text if email_response else 'No response'}
    """
    logging.error(error_message)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=error_message,
    )


def get_signature_request(session, signature_request_id):
    signature_request = session.get(SignatureRequest, signature_request_id)
    if not signature_request:
        raise HTTPException(status_code=404, detail="Signature request not found")
    return signature_request


def get_signatory(session, email, signature_request_id):
    statement = (
        select(Signatory)
        .join(RequestSignatoryLink)
        .where(
            Signatory.email == email,
            RequestSignatoryLink.signature_request_id == signature_request_id,
        )
    )
    signatory = session.exec(statement).first()
    if not signatory:
        raise HTTPException(status_code=404, detail="Signatory not found")
    return signatory


def verify_otp_code(email, otp, otp_store):
    logger.info(f"Verifying OTP for email: {email}")
    if email not in otp_store:
        logger.error("OTP not found for email: {email}")
        raise HTTPException(status_code=400, detail="OTP not found")
    otp_data = otp_store[email]
    if otp_data["expires"] < datetime.now():
        del otp_store[email]
        logger.error("OTP expired for email: {email}")
        raise HTTPException(status_code=400, detail="OTP expired")
    if otp_data["otp"] != otp:
        logger.error("Invalid OTP for email: {email}")
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[email]
    logger.info("OTP verified successfully for email: {email}")


def log_otp_verification(session, ip_address, signature_request_id, signatory_id):
    logger.info(
        f"Logging OTP verification for signatory {signatory_id} in signature request {signature_request_id}"
    )
    audit_log_crud.create_audit_log(
        session,
        AuditLogCreate(
            description="OTP verified",
            ip_address=ip_address,
            action=AuditLogAction.DOCUMENT_SIGNED,
            signature_request_id=signature_request_id,
            signatory_id=signatory_id,
        ),
    )


def process_signatory_signature(
    session, signatory, signature_request, ip_address, static_files_dir
):
    logger.info(f"Processing signature for signatory {signatory.id}")
    signatory.signed_at = datetime.now()
    session.commit()

    for document in signature_request.documents:
        document_path = process_document_for_signatory(
            session, document, signatory, ip_address, static_files_dir
        )
        if len(signature_request.signatories) == 1:
            apply_pdf_security(str(document_path))
    logger.info(f"Signature processed for signatory {signatory.id}")


def process_document_for_signatory(
    session, document, signatory, ip_address, static_files_dir
):
    logger.info(f"Processing document {document.id} for signatory {signatory.id}")
    document.status = DocumentStatus.SIGNED
    session.commit()

    final_pdf_path = static_files_dir / "signed_documents" / f"{document.file}"
    for field in signatory.fields:
        if field.document_id == document.id:
            add_fields_to_pdf(document.file, field, signatory, document.owner_id)

    # Convert the updated PDF to images and replace old images
    folder_name = f"{document.owner_id}_{document.title}"
    image_folder = static_files_dir / folder_name
    if image_folder.exists():
        # Remove old images
        for img_file in image_folder.glob("*.png"):
            img_file.unlink()

    # Convert the updated PDF to images
    convert_pdf_to_images(final_pdf_path, image_folder)

    pdf_hash = generate_pdf_hash(str(final_pdf_path))
    logger.info(f"Generated hash for document {document.id}: {pdf_hash}")

    document_signature_details = DocumentSignatureDetailsCreate(
        document_id=document.id,
        signed_hash=pdf_hash,
        timestamp=datetime.now(),
        ip_address=ip_address,
    )
    signed_document_crud.create_document_signature_details(
        session, document_signature_details
    )

    return final_pdf_path


def all_signatories_signed(signatories):
    signed_status = all(signatory.signed_at is not None for signatory in signatories)
    logger.info(f"All signatories signed status: {signed_status}")
    return signed_status


def finalize_document(session, signature_request, ip_address, static_files_dir):
    signature_request.status = SignatureRequestStatus.SIGNED
    logger.info(f"Finalizing document for signature request {signature_request.id}")
    for document in signature_request.documents:
        final_pdf_path = static_files_dir / "signed_documents" / f"{document.file}"
        apply_pdf_security(str(final_pdf_path))
        document.status = DocumentStatus.SIGNED

        pdf_hash = generate_pdf_hash(str(final_pdf_path))
        logger.info(f"Generated hash for document {document.id}: {pdf_hash}")

        document_signature_details = DocumentSignatureDetailsCreate(
            document_id=document.id,
            signed_hash=pdf_hash,
            timestamp=datetime.now(),
            ip_address=ip_address,
        )
        signed_document_crud.create_document_signature_details(
            session, document_signature_details
        )
    session.commit()
    logger.info(f"Document finalized for signature request {signature_request.id}")


def send_final_notifications(signature_request, static_files_dir):
    logger.info(f"Sending final notifications for signature request {signature_request.id}")
    signed_documents = [
        static_files_dir / "signed_documents" / f"{document.file}"
        for document in signature_request.documents
    ]
    recipients = [signature_request.sender.email] + [
        signatory.email for signatory in signature_request.signatories
    ]
    for recipient in recipients:
        send_signature_request_notification_email(
            email_to=recipient,
            signature_request_name=signature_request.name,
            signature_request_id=signature_request.id,
            status=signature_request.status.value,
            documents=signed_documents,
        )
    logger.info(f"Final notifications sent for signature request {signature_request.id}")


def send_next_ordered_signatory_email(signature_request, session, request):
    logger.info(f"Sending email to next ordered signatory for signature request {signature_request.id}")
    for signatory in sorted(signature_request.signatories, key=lambda s: s.signing_order):
        if not signatory.signed_at:
            secure_link, token = generate_secure_link(
                signature_request.expiry_date,
                signature_request.id,
                signatory.email,
                [document.id for document in signature_request.documents],
                signatory.id,
                signature_request.require_otp,
            )
            send_email_and_update_status(
                email=signatory.email,
                link=secure_link,
                message=signature_request.message,
                documents=signature_request.documents,
                db=session,
                signature_request_data=signature_request,
                request=request,
                token=token,
            )
            break

    signature_request.status = SignatureRequestStatus.PARTIALLY_SIGNED
    for document in signature_request.documents:
        document.status = DocumentStatus.PARTIALLY_SIGNED
        session.add(document)
    session.add(signature_request)
    session.commit()
    logger.info(f"Email sent to next ordered signatory for signature request {signature_request.id}")


def send_remaining_signatories_email(signature_request, session, request):
    logger.info(f"Sending email to remaining signatories for signature request {signature_request.id}")
    for signatory in signature_request.signatories:
        if not signatory.signed_at:
            secure_link, token = generate_secure_link(
                signature_request.expiry_date,
                signature_request.id,
                signatory.email,
                [document.id for document in signature_request.documents],
                signatory.id,
                signature_request.require_otp,
            )
            send_email_and_update_status(
                email=signatory.email,
                link=secure_link,
                message=signature_request.message,
                documents=signature_request.documents,
                db=session,
                signature_request_data=signature_request,
                request=request,
                token=token,
            )

    signature_request.status = SignatureRequestStatus.PARTIALLY_SIGNED
    for document in signature_request.documents:
        document.status = DocumentStatus.PARTIALLY_SIGNED
        session.add(document)
    session.add(signature_request)
    session.commit()
    logger.info(f"Emails sent to remaining signatories for signature request {signature_request.id}")
