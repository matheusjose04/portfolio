from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..auth import get_current_admin
from ..database import get_db
from ..lang import resolve_lang
from ..models import AdminUser, HeroLine, SiteContent
from ..schemas import (
    HeroLineAdminOut,
    HeroLineOut,
    SiteContentAdminOut,
    SiteContentOut,
    SiteContentUpdate,
)

router = APIRouter(prefix="/api/site-content", tags=["content"])


def _get_or_create(db: Session) -> SiteContent:
    content = db.get(SiteContent, 1)
    if content is None:
        content = SiteContent(id=1)
        db.add(content)
        db.commit()
        db.refresh(content)
    return content


def _pick(content: SiteContent, field: str, lang: str) -> str:
    en_value = getattr(content, f"{field}_en", "")
    pt_value = getattr(content, f"{field}_pt", "")
    return en_value if lang == "en" and en_value else pt_value


@router.get("", response_model=SiteContentOut)
def get_site_content(
    db: Annotated[Session, Depends(get_db)],
    lang: str | None = None,
    accept_language: Annotated[str | None, Header()] = None,
) -> SiteContentOut:
    content = _get_or_create(db)
    resolved = resolve_lang(accept_language, lang)
    lines = db.query(HeroLine).order_by(HeroLine.position, HeroLine.id).all()
    return SiteContentOut(
        about_heading=_pick(content, "about_heading", resolved),
        about_text=_pick(content, "about_text", resolved),
        about_comment=_pick(content, "about_comment", resolved),
        about_foco=_pick(content, "about_foco", resolved),
        about_formacao=_pick(content, "about_formacao", resolved),
        contact_heading=_pick(content, "contact_heading", resolved),
        contact_text=_pick(content, "contact_text", resolved),
        contact_email=content.contact_email,
        footer_rights=_pick(content, "footer_rights", resolved),
        cv_url=content.cv_url,
        linkedin_url=content.linkedin_url,
        github_url=content.github_url,
        hero_lines=[
            HeroLineOut(cmd=line.cmd, output=line.output_en if resolved == "en" and line.output_en else line.output_pt)
            for line in lines
        ],
    )


@router.get("/admin", response_model=SiteContentAdminOut)
def get_site_content_admin(
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> SiteContentAdminOut:
    content = _get_or_create(db)
    lines = db.query(HeroLine).order_by(HeroLine.position, HeroLine.id).all()
    return SiteContentAdminOut(
        **{field: getattr(content, field) for field in SiteContentAdminOut.model_fields if field != "hero_lines"},
        hero_lines=[HeroLineAdminOut.model_validate(line) for line in lines],
    )


@router.put("/admin", response_model=SiteContentAdminOut)
def update_site_content(
    payload: SiteContentUpdate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> SiteContentAdminOut:
    content = _get_or_create(db)
    data = payload.model_dump(exclude={"hero_lines"})
    for field, value in data.items():
        setattr(content, field, value)

    db.query(HeroLine).delete()
    for index, line in enumerate(payload.hero_lines):
        db.add(HeroLine(position=index, cmd=line.cmd, output_pt=line.output_pt, output_en=line.output_en))

    db.commit()
    db.refresh(content)
    return get_site_content_admin(db, admin)
