from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ProjectCategory = Literal["complete", "small"]
SkillCategory = Literal["languages", "databases", "frameworks", "tools"]

# Duplicado de frontend/src/data/skills.ts (LEVEL_LABEL) de propósito — sem
# build compartilhado entre TS e Python nesta fase do projeto.
LEVEL_LABELS: dict[int, dict[str, str]] = {
    1: {"pt": "básico", "en": "basic"},
    2: {"pt": "básico", "en": "basic"},
    3: {"pt": "intermediário", "en": "intermediate"},
    4: {"pt": "avançado", "en": "advanced"},
    5: {"pt": "especialista", "en": "expert"},
}


def _validate_url(value: str | None) -> str | None:
    if value is not None and not value.startswith(("http://", "https://")):
        raise ValueError("URL deve começar com http:// ou https://")
    return value


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    category: ProjectCategory
    skills: list[str] = Field(default_factory=list)
    github_url: str | None = None
    demo_url: str | None = None
    image_url: str | None = None
    featured: bool = False

    _validate_github_url = field_validator("github_url")(_validate_url)
    _validate_demo_url = field_validator("demo_url")(_validate_url)


class ProjectCreate(ProjectBase):
    description_pt: str = Field(min_length=1)
    description_en: str = ""
    why_pt: str = Field(min_length=1)
    why_en: str = ""


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    category: ProjectCategory | None = None
    skills: list[str] | None = None
    github_url: str | None = None
    demo_url: str | None = None
    image_url: str | None = None
    featured: bool | None = None
    description_pt: str | None = None
    description_en: str | None = None
    why_pt: str | None = None
    why_en: str | None = None

    _validate_github_url = field_validator("github_url")(_validate_url)
    _validate_demo_url = field_validator("demo_url")(_validate_url)


class ProjectOut(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    why: str
    category: str
    skills: list[str]
    github_url: str | None
    demo_url: str | None
    image_url: str | None
    featured: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectAdminOut(BaseModel):
    """Igual ao Project do banco, sem resolver idioma — só pro form de edição do admin."""

    id: int
    title: str
    slug: str
    description_pt: str
    description_en: str
    why_pt: str
    why_en: str
    category: str
    skills: list[str]
    github_url: str | None
    demo_url: str | None
    image_url: str | None
    featured: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SkillBase(BaseModel):
    skill_id: str = Field(min_length=1, max_length=50, pattern=r"^[a-z0-9-]+$")
    category: SkillCategory
    name: str = Field(min_length=1, max_length=60)
    icon: str = Field(min_length=1, max_length=80)
    level: int = Field(ge=1, le=5)
    summary_pt: str = ""
    summary_en: str = ""
    experience_pt: str = ""
    experience_en: str = ""
    position: int = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    skill_id: str | None = Field(default=None, min_length=1, max_length=50, pattern=r"^[a-z0-9-]+$")
    category: SkillCategory | None = None
    name: str | None = Field(default=None, min_length=1, max_length=60)
    icon: str | None = Field(default=None, min_length=1, max_length=80)
    level: int | None = Field(default=None, ge=1, le=5)
    summary_pt: str | None = None
    summary_en: str | None = None
    experience_pt: str | None = None
    experience_en: str | None = None
    position: int | None = None


class SkillOut(BaseModel):
    id: int
    skill_id: str
    category: str
    name: str
    icon: str
    level: int
    level_label: dict[str, str]
    summary: dict[str, str]
    experience: dict[str, str]
    position: int


class HeroLineInput(BaseModel):
    cmd: str = Field(min_length=1, max_length=120)
    output_pt: str = ""
    output_en: str = ""


class HeroLineOut(BaseModel):
    cmd: str
    output: str


class HeroLineAdminOut(BaseModel):
    id: int
    position: int
    cmd: str
    output_pt: str
    output_en: str

    model_config = ConfigDict(from_attributes=True)


_SITE_CONTENT_FIELDS = (
    "about_heading_pt", "about_heading_en",
    "about_text_pt", "about_text_en",
    "about_comment_pt", "about_comment_en",
    "about_foco_pt", "about_foco_en",
    "about_formacao_pt", "about_formacao_en",
    "contact_heading_pt", "contact_heading_en",
    "contact_text_pt", "contact_text_en",
    "contact_email",
    "footer_rights_pt", "footer_rights_en",
    "cv_url", "linkedin_url", "github_url",
)


class SiteContentUpdate(BaseModel):
    about_heading_pt: str = ""
    about_heading_en: str = ""
    about_text_pt: str = ""
    about_text_en: str = ""
    about_comment_pt: str = ""
    about_comment_en: str = ""
    about_foco_pt: str = ""
    about_foco_en: str = ""
    about_formacao_pt: str = ""
    about_formacao_en: str = ""
    contact_heading_pt: str = ""
    contact_heading_en: str = ""
    contact_text_pt: str = ""
    contact_text_en: str = ""
    contact_email: str = ""
    footer_rights_pt: str = ""
    footer_rights_en: str = ""
    cv_url: str = ""
    linkedin_url: str = ""
    github_url: str = ""
    hero_lines: list[HeroLineInput] = Field(default_factory=list)


class SiteContentAdminOut(BaseModel):
    about_heading_pt: str
    about_heading_en: str
    about_text_pt: str
    about_text_en: str
    about_comment_pt: str
    about_comment_en: str
    about_foco_pt: str
    about_foco_en: str
    about_formacao_pt: str
    about_formacao_en: str
    contact_heading_pt: str
    contact_heading_en: str
    contact_text_pt: str
    contact_text_en: str
    contact_email: str
    footer_rights_pt: str
    footer_rights_en: str
    cv_url: str
    linkedin_url: str
    github_url: str
    hero_lines: list[HeroLineAdminOut]


class SiteContentOut(BaseModel):
    about_heading: str
    about_text: str
    about_comment: str
    about_foco: str
    about_formacao: str
    contact_heading: str
    contact_text: str
    contact_email: str
    footer_rights: str
    cv_url: str
    linkedin_url: str
    github_url: str
    hero_lines: list[HeroLineOut]
