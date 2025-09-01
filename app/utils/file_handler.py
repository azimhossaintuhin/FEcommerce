from  fastapi import UploadFile,File
import os 
from  uuid import uuid4

UPLOAD_DIR = "uploads/"

# Create The upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile,folder:str="") -> str:
    save_folder = os.path.join(UPLOAD_DIR,folder) if folder else UPLOAD_DIR
    os.makedirs(save_folder, exist_ok=True)
    ext = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(save_folder, unique_filename)

    with open(file_path,'wb') as  f:
        f.write(upload_file.file.read())
    return file_path


