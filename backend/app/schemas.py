from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Ids válidos de frontend/src/data/skills.ts (duplicado aqui de propósito —
# sem build compartilhado entre TS e Python nesta fase do projeto).
VALID_SKILL_IDS = {
    "python",
    "typescript",
    "javascript",
    "sqlite",
    "fastapi",
    "docker",
    "git",
    "linux",
}

ProjectCategory = Literal["complete", "small"]


def _validate_url(value: str | None) -> str | None:
    if value is not None and not value.startswith(("http://", "https://")):
        raise ValueError("URL deve começar com http:// ou https://")
    return value


def _validate_skills(value: list[str]) -> list[str]:
    invalid = sorted(set(value) - VALID_SKILL_IDS)
    if invalid:
        raise ValueError(f"skills inválidas: {', '.join(invalid)}")
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
    _validate_skills_subset = field_validator("skills")(_validate_skills)


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

    @field_validator("skills")
    @classmethod
    def _validate_skills_subset(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        return _validate_skills(value)


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
