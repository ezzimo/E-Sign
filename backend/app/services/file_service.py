import logging
import os

from fastapi import UploadFile, HTTPException
from pathlib import Path

# Create a logger for your application
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static/document_files/")


def save_file(file: UploadFile, user_id: int) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    new_filename = f"{user_id}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, new_filename)
    with open(save_path, "wb") as f:
        f.write(file.file.read())
    return new_filename


def file_existance(file_path: str) -> bool:
    file_abs_path = Path(BASE_DIR) / "static" / "document_files" / file_path
    logger.info(f"display the path==========>: {file_abs_path}")
    if not file_abs_path.exists():
        raise HTTPException(status_code=404, detail="File end point not found")
    return True
