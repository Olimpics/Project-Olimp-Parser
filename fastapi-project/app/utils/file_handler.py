import os
import uuid
import shutil
from fastapi import UploadFile
from app.core.config import settings

async def save_upload_file_temporarily(upload_file: UploadFile) -> str:
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    
    file_id = uuid.uuid4()
    extension = os.path.splitext(upload_file.filename)[1]
    temp_file = os.path.join(settings.UPLOAD_FOLDER, f"{file_id}{extension}")
    
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return temp_file

async def remove_temp_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)