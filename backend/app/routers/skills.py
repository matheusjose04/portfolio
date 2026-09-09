from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_admin
from ..database import get_db
from ..models import AdminUser, Skill
from ..schemas import LEVEL_LABELS, SkillCreate, SkillOut, SkillUpdate

router = APIRouter(prefix="/api/skills", tags=["skills"])


def to_out(s: Skill) -> SkillOut:
    return SkillOut(
        id=s.id,
        skill_id=s.skill_id,
        category=s.category,
        name=s.name,
        icon=s.icon,
        level=s.level,
        level_label=LEVEL_LABELS.get(s.level, LEVEL_LABELS[3]),
        summary={"pt": s.summary_pt, "en": s.summary_en},
        experience={"pt": s.experience_pt, "en": s.experience_en},
        position=s.position,
    )


@router.get("", response_model=list[SkillOut])
def list_skills(db: Annotated[Session, Depends(get_db)]) -> list[SkillOut]:
    items = db.query(Skill).order_by(Skill.position, Skill.id).all()
    return [to_out(s) for s in items]


@router.get("/{skill_id}", response_model=SkillOut)
def get_skill(
    skill_id: int,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> SkillOut:
    skill = db.get(Skill, skill_id)
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill não encontrada")
    return to_out(skill)


@router.post("", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
def create_skill(
    payload: SkillCreate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> SkillOut:
    if db.query(Skill).filter(Skill.skill_id == payload.skill_id).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="skill_id já existe")
    skill = Skill(**payload.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return to_out(skill)


@router.put("/{skill_id}", response_model=SkillOut)
def update_skill(
    skill_id: int,
    payload: SkillUpdate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> SkillOut:
    skill = db.get(Skill, skill_id)
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill não encontrada")

    data = payload.model_dump(exclude_unset=True)
    if "skill_id" in data and data["skill_id"] != skill.skill_id:
        clash = db.query(Skill).filter(Skill.skill_id == data["skill_id"]).first()
        if clash is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="skill_id já existe")
    for field, value in data.items():
        setattr(skill, field, value)

    db.commit()
    db.refresh(skill)
    return to_out(skill)


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[AdminUser, Depends(get_current_admin)],
) -> None:
    skill = db.get(Skill, skill_id)
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill não encontrada")
    db.delete(skill)
    db.commit()
