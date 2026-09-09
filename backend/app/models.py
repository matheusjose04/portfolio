from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (CheckConstraint("category IN ('complete', 'small')", name="ck_project_category"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True, nullable=False)
    description_pt: Mapped[str] = mapped_column(Text, nullable=False)
    description_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    why_pt: Mapped[str] = mapped_column(Text, nullable=False)
    why_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    skills: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    github_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    demo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_utcnow)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_utcnow)


class SiteContent(Base):
    """Linha única (id=1) com o conteúdo editável fora dos projetos: sobre,
    contato, links e o rodapé. Uma tabela singleton em vez de key-value pra
    manter os campos tipados e validáveis pelo Pydantic."""

    __tablename__ = "site_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    about_heading_pt: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    about_heading_en: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    about_text_pt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    about_text_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    about_comment_pt: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    about_comment_en: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    about_foco_pt: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    about_foco_en: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    about_formacao_pt: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    about_formacao_en: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    contact_heading_pt: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    contact_heading_en: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    contact_text_pt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    contact_text_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    contact_email: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    footer_rights_pt: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    footer_rights_en: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    cv_url: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    linkedin_url: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    github_url: Mapped[str] = mapped_column(String(255), nullable=False, default="")


class HeroLine(Base):
    """Linhas digitadas no terminal do Hero. `cmd` não é traduzido (é um
    comando de shell, ex: 'whoami') — só o `output` varia por idioma."""

    __tablename__ = "hero_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cmd: Mapped[str] = mapped_column(String(120), nullable=False)
    output_pt: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    output_en: Mapped[str] = mapped_column(String(255), nullable=False, default="")


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = (
        CheckConstraint("category IN ('languages', 'databases', 'frameworks', 'tools')", name="ck_skill_category"),
        CheckConstraint("level BETWEEN 1 AND 5", name="ck_skill_level"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    icon: Mapped[str] = mapped_column(String(80), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    summary_pt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    summary_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    experience_pt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    experience_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
