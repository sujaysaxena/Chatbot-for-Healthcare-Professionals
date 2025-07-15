import uuid
import os
from PIL import Image
from fastapi import UploadFile
from typing import Tuple
import io

# Save uploaded file temporarily and return the path
async def save_upload_file(uploaded_file: UploadFile, folder: str = "temp") -> str:
    os.makedirs(folder, exist_ok=True)
    unique_name = generate_unique_filename(uploaded_file.filename)
    file_path = os.path.join(folder, unique_name)

    contents = await uploaded_file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path

# Generate unique filename to avoid collisions
def generate_unique_filename(filename: str) -> str:
    ext = get_file_extension(filename)
    return f"{uuid.uuid4().hex}.{ext}"

# Get the file extension (even from .tar.gz)
def get_file_extension(filename: str) -> str:
    return filename.split('.')[-1].lower()

# Convert bytes to PIL Image
def load_image_pil(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")

if __name__ == "__main__":
    print("✅ utils.py loaded successfully!")
    print("Available function:", save_upload_file)
