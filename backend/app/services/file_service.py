import os
from fastapi import UploadFile


def save_file(file: UploadFile, user_id: int) -> str:
    directory = "static/document_files"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists

    file_location = f"{directory}/{user_id}_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    return file_location
