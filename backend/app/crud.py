import re
import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Project


def slugify(title: str) -> str:
    # normaliza acentos (ex: "Gestão" -> "Gestao") antes de remover o resto,
    # já que os títulos são em português.
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.strip().lower()).strip("-")
    return slug or "projeto"


def unique_slug(db: Session, title: str, ignore_id: int | None = None) -> str:
    base = slugify(title)
    slug = base
    suffix = 2
    while True:
        query = select(Project).where(Project.slug == slug)
        if ignore_id is not None:
            query = query.where(Project.id != ignore_id)
        if db.execute(query).scalar_one_or_none() is None:
            return slug
        slug = f"{base}-{suffix}"
        suffix += 1
