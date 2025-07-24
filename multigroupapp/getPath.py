from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import aiofiles
import os
from datetime import datetime

BASE_TEXT_DIR = os.getenv("GROUP_TEXT_DIR", "/home/Praveen_ZT/IBComm_RAG/multigroupapp/group_texts")
os.makedirs(BASE_TEXT_DIR, exist_ok=True)


def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in ('-', '_'))

def get_group_file_path(group_id: str) -> str:
    safe_group_id = sanitize_filename(group_id)
    return os.path.join(BASE_TEXT_DIR, f"{safe_group_id}.txt")