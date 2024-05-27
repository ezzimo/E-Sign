import logging
import os
import random
import string
from pathlib import Path
from typing import Optional
from jose import JWTError, jwt
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.utils import send_email
from datetime import datetime, timedelta
from typing import List


logger = logging.getLogger(__name__)

otp_store = {}

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "static" / "document_files"


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
        logger.info(f"the decoded token is:  {payload}")
        return payload
    except JWTError:
        logger.error("Failed to decode JWT token")
        return None


def generate_otp() -> str:
    return ''.join(random.choices(string.digits, k=6))


def send_otp_code(email: str, otp: int) -> bool:
    subject = "Your OTP Code"
    html_content = f"<p>Your OTP code is: {otp}</p>"
    response = send_email(email_to=email, subject=subject, html_content=html_content)
    return response.status_code == 250


def generate_secure_link(email: str, document_ids: List[int], signatory_id: int) -> str:
    expiration = datetime.now() + timedelta(hours=24)
    payload = {
        "sub": email,
        "exp": expiration,
        "document_ids": document_ids,
        "signatory_id": signatory_id,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    secure_link = f"{settings.FRONTEND_URL}/sign_document?token={token}"
    return secure_link


def verify_secure_link(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except JWTError:
        return None
