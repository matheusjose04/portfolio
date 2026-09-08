from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_admin
from ..crud import unique_slug
from ..database import get_db
from ..models import AdminUser, Project
from ..schemas import ProjectAdminOut, ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])


def resolve_lang(accept_language: str | None, lang_query: str | None) -> str:
    if lang_query in ("pt", "en"):
        return lang_query
    if accept_language and accept_language.lower().startswith("en"):
        return "en"
    return "pt"


def to_out(project: Project, lang: str) -> ProjectOut:
    description = project.description_en if lang == "en" and project.description_en else project.description_pt
    why = project.why_en if lang == "en" and project.why_en else project.why_pt
    return ProjectOut(
        id=project.id,
        title=project.title,
        slug=project.slug,
        description=description,
        why=why,
        category=project.category,
        skills=project.skills,
        github_url=project.github_url,
        demo_url=project.demo_url,
        image_url=project.image_url,
        featured=project.featured,
        created_at=project.created_at,
    )


@router.get("", response_model=list[ProjectOut])
def list_projects(
    db: Annotated[Session, Depends(get_db)],
    category: str | None = None,
    skill: str | None = None,
    featured: bool | None = None,
    lang: str | None = None,
    accept_language: Annotated[str | None, Header()] = None,
) -> list[ProjectOut]:
    resolved_lang = resolve_lang(accept_language, lang)
    query = db.query(Project)
    if category:
        query = query.filter(Project.category == category)
    if featured is not None:
        query = query.filter(Project.featured == featured)
    projects = query.order_by(Project.created_at.desc()).all()
    if skill:
        projects = [p for p in projects if skill in p.skills]
    return [to_out(p, resolved_lang) for p in projects]


@router.get("/{slug}", response_model=ProjectOut)
def get_project(
    slug: str,
    db: Annotated[Session, Depends(get_db)],
    lang: str | None = None,
    accept_language: Annotated[str | None, Header()] = None,
) -> ProjectOut:
    project = db.query(Project).filter(Project.slug == slug).first()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")
    return to_out(project, resolve_lang(accept_language, lang))


@router.get("/id/{project_id}", response_model=ProjectAdminOut)
def get_project_admin(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")
    return project


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> ProjectOut:
    project = Project(
        title=payload.title,
        slug=unique_slug(db, payload.title),
        description_pt=payload.description_pt,
        description_en=payload.description_en,
        why_pt=payload.why_pt,
        why_en=payload.why_en,
        category=payload.category,
        skills=payload.skills,
        github_url=payload.github_url,
        demo_url=payload.demo_url,
        image_url=payload.image_url,
        featured=payload.featured,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return to_out(project, "pt")


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> ProjectOut:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")

    data = payload.model_dump(exclude_unset=True)
    if "title" in data and data["title"] != project.title:
        project.slug = unique_slug(db, data["title"], ignore_id=project.id)
    for field, value in data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return to_out(project, "pt")


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> None:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")
    db.delete(project)
    db.commit()
