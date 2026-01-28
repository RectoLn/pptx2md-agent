# app/utils/file_ops.py
import os
import uuid
from pathlib import Path

# 定义基础路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
IMG_OUTPUT_DIR = OUTPUT_DIR / "images"
MD_OUTPUT_DIR = OUTPUT_DIR / "md"

def init_directories():
    """初始化所需的文件夹"""
    for folder in [UPLOAD_DIR, IMG_OUTPUT_DIR, MD_OUTPUT_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

def save_upload_file(file_content: bytes, filename: str) -> str:
    """保存上传的文件并返回路径"""
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        f.write(file_content)
    return str(file_path)

def get_unique_image_path(original_ext: str = "png") -> str:
    """生成唯一的图片保存路径"""
    filename = f"{uuid.uuid4()}.{original_ext}"
    return str(IMG_OUTPUT_DIR / filename), filename