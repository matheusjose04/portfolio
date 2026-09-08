import re
import time
from io import BytesIO
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from ..auth import get_current_admin
from ..models import AdminUser

router = APIRouter(prefix="/api/upload", tags=["upload"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_CONTENT_TYPES = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}
MAX_SIZE_BYTES = 2 * 1024 * 1024


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_image(
    admin: Annotated[AdminUser, Depends(get_current_admin)],
    file: UploadFile = File(...),
) -> dict[str, str]:
    ext = ALLOWED_CONTENT_TYPES.get(file.content_type or "")
    if ext is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato não suportado. Use png, jpg ou webp.")

    contents = await file.read()
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo maior que 2MB.")

    try:
        Image.open(BytesIO(contents)).verify()
    except UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo não é uma imagem válida.")

    stem = (file.filename or "imagem").rsplit(".", 1)[0]
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "imagem"
    filename = f"{slug}-{int(time.time())}.{ext}"
    (UPLOAD_DIR / filename).write_bytes(contents)

    return {"url": f"/uploads/{filename}"}
