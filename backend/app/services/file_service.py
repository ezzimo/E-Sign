import os

from fastapi import UploadFile


BASE_DIR = os.path.dirname(os.path.abspath(__name__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static/document_files/")


def save_file(file: UploadFile, user_id: int) -> str:
    directory = "static/document_files"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    new_filename = f"{user_id}_{file.filename}"
    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)
    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(file.file.read())

    return SAVE_FILE_PATH
