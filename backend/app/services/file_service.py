import logging
import os
from pathlib import Path
from typing import Optional
from jose import JWTError, jwt
from fastapi import UploadFile, HTTPException
from app.core.config import settings


logger = logging.getLogger(__name__)

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
