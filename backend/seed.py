from app.auth import hash_password
from app.config import settings
from app.crud import slugify, unique_slug
from app.database import Base, SessionLocal, engine
from app.models import AdminUser, Project

# CONTENT.md não tinha projetos preenchidos ainda — usamos os placeholders
# sugeridos em docs/backend/seed.md. Troque pelos seus projetos reais
# (via CONTENT.md + re-seed, ou direto pelo painel /admin).
PLACEHOLDER_DESCRIPTION_PT = (
    "Projeto de exemplo (placeholder) — substitua pelos seus projetos reais "
    "no CONTENT.md ou pelo painel /admin."
)
PLACEHOLDER_DESCRIPTION_EN = (
    "Example (placeholder) project — replace it with your real projects "
    "via CONTENT.md or the /admin panel."
)
PLACEHOLDER_WHY_PT = "Placeholder — adicione a motivação real deste projeto."
PLACEHOLDER_WHY_EN = "Placeholder — add the real motivation behind this project."

PLACEHOLDER_PROJECTS = [
    {
        "title": "Sistema de Gestão X",
        "category": "complete",
        "skills": ["python", "fastapi", "sqlite"],
        "image_url": "/images/projects/placeholder-complete-1.svg",
    },
    {
        "title": "API de Autenticação Y",
        "category": "complete",
        "skills": ["python", "fastapi", "sqlite", "git"],
        "image_url": "/images/projects/placeholder-complete-2.svg",
    },
    {
        "title": "CLI de Automação Z",
        "category": "small",
        "skills": ["python", "git"],
        "image_url": "/images/projects/placeholder-small-1.svg",
    },
    {
        "title": "Bot de Discord W",
        "category": "small",
        "skills": ["python", "docker"],
        "image_url": "/images/projects/placeholder-small-2.svg",
    },
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(AdminUser).filter(AdminUser.username == settings.admin_user).first()
        if admin is None:
            db.add(AdminUser(username=settings.admin_user, password_hash=hash_password(settings.admin_password)))
            db.commit()
            print(f"Admin '{settings.admin_user}' criado.")
        else:
            print(f"Admin '{settings.admin_user}' já existe, mantido.")

        for data in PLACEHOLDER_PROJECTS:
            expected_slug = slugify(data["title"])
            if db.query(Project).filter(Project.slug == expected_slug).first() is not None:
                print(f"Projeto '{data['title']}' já existe, mantido.")
                continue

            db.add(
                Project(
                    title=data["title"],
                    slug=unique_slug(db, data["title"]),
                    description_pt=PLACEHOLDER_DESCRIPTION_PT,
                    description_en=PLACEHOLDER_DESCRIPTION_EN,
                    why_pt=PLACEHOLDER_WHY_PT,
                    why_en=PLACEHOLDER_WHY_EN,
                    category=data["category"],
                    skills=data["skills"],
                    github_url=None,
                    demo_url=None,
                    image_url=data["image_url"],
                    featured=False,
                )
            )
            print(f"Projeto '{data['title']}' criado.")
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed concluído.")
