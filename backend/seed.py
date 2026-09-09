from app.auth import hash_password
from app.config import settings
from app.crud import slugify, unique_slug
from app.database import Base, SessionLocal, engine
from app.models import AdminUser, HeroLine, Project, SiteContent, Skill

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


SITE_CONTENT_DEFAULTS = {
    "about_heading_pt": "~# sobre",
    "about_heading_en": "~# about",
    "about_text_pt": (
        "Sou estudante de Ciência da Computação no UniMAX (Indaiatuba/SP), atualmente no 6º semestre. "
        "Meu foco tem sido desenvolvimento fullstack — trabalho com Python, Java, C++, FastAPI, TypeScript "
        "e SQL — e venho me aprofundando por conta própria em cybersecurity, explorando ferramentas como "
        "Kali Linux, Sherlock, Maigret e PhoneInfoga. Já apliquei esse conhecimento em projetos próprios e "
        "acadêmicos, como um sistema de autenticação multifator com reconhecimento facial e de voz e um "
        "sistema de rotas multimodais de transporte.\n\nEstou em busca de uma oportunidade de estágio onde "
        "eu possa aplicar essas habilidades na prática, continuar aprendendo com profissionais da área e, "
        "no futuro, seguir carreira voltada para segurança da informação."
    ),
    "about_text_en": (
        "I'm a Computer Science student at UniMAX (Indaiatuba/SP), currently in my 6th semester. My focus "
        "has been fullstack development — I work with Python, Java, C++, FastAPI, TypeScript and SQL — and "
        "I've been deepening my knowledge of cybersecurity on my own, exploring tools like Kali Linux, "
        "Sherlock, Maigret and PhoneInfoga. I've already applied this knowledge in personal and academic "
        "projects, such as a multi-factor authentication system with facial and voice recognition and a "
        "multimodal transportation routing system.\n\nI'm looking for an internship opportunity where I can "
        "apply these skills in practice, keep learning from professionals in the field and, in the future, "
        "pursue a career focused on information security."
    ),
    "about_comment_pt": "// quem sou eu",
    "about_comment_en": "// who I am",
    "about_foco_pt": "fullstack + cybersecurity",
    "about_foco_en": "fullstack + cybersecurity",
    "about_formacao_pt": "Ciência da Computação — UniMAX (6º semestre)",
    "about_formacao_en": "Computer Science — UniMAX (6th semester)",
    "contact_heading_pt": "~# contato",
    "contact_heading_en": "~# contact",
    "contact_text_pt": (
        "Tem uma vaga de estágio, quer trocar uma ideia sobre cybersecurity ou só bater um papo sobre "
        "código? Me chama."
    ),
    "contact_text_en": "Got an internship opening, want to talk cybersecurity, or just want to talk code? Reach out.",
    "contact_email": "matheus.casarin.dev@gmail.com",
    "footer_rights_pt": "Todos os direitos reservados.",
    "footer_rights_en": "All rights reserved.",
    "cv_url": "/cv-matheus.pdf",
    "linkedin_url": "https://www.linkedin.com/in/matheuscasarin",
    "github_url": "https://github.com/matheusjose04",
}

HERO_LINES_DEFAULTS = [
    {
        "cmd": "whoami",
        "output_pt": "matheus Casarin — Desenvolvedor Fullstack & Cybersecurity",
        "output_en": "matheus Casarin — Fullstack Developer & Cybersecurity",
    },
    {
        "cmd": "ls ./skills",
        "output_pt": "python typescript javascript fastapi sqlite docker git linux",
        "output_en": "python typescript javascript fastapi sqlite docker git linux",
    },
]

# Espelha frontend/src/data/skills.ts — duplicado aqui de propósito (sem
# build compartilhado entre TS e Python nesta fase do projeto).
SKILLS_DEFAULTS = [
    {
        "skill_id": "python", "category": "languages", "name": "Python",
        "icon": "devicon-python-plain", "level": 2,
        "summary_pt": "Linguagem de alto nível, muito usada em back-end, automação e ferramentas de cybersecurity.",
        "summary_en": "High-level language widely used for back-end development, automation and cybersecurity tooling.",
        "experience_pt": "Uso em projetos acadêmicos e pessoais de desenvolvimento fullstack e em scripts de segurança.",
        "experience_en": "Used in academic and personal fullstack projects and in security-related scripts.",
    },
    {
        "skill_id": "typescript", "category": "languages", "name": "TypeScript",
        "icon": "devicon-typescript-plain", "level": 2,
        "summary_pt": "Superset do JavaScript com tipagem estática, usado no front-end e em ferramentas modernas.",
        "summary_en": "JavaScript superset with static typing, used across modern front-end tooling.",
        "experience_pt": "Uso no desenvolvimento do front-end deste portfólio e em projetos pessoais.",
        "experience_en": "Used to build the front-end of this portfolio and in personal projects.",
    },
    {
        "skill_id": "javascript", "category": "languages", "name": "JavaScript",
        "icon": "devicon-javascript-plain", "level": 2,
        "summary_pt": "Linguagem principal da web, roda no navegador e também no back-end (Node.js).",
        "summary_en": "The core language of the web, running in the browser and on the back-end via Node.js.",
        "experience_pt": "Base para os projetos front-end que desenvolvi durante a faculdade e por conta própria.",
        "experience_en": "Foundation for the front-end projects built during university and on my own.",
    },
    {
        "skill_id": "sqlite", "category": "databases", "name": "SQLite",
        "icon": "devicon-sqlite-plain", "level": 2,
        "summary_pt": "Banco de dados relacional leve, roda em um único arquivo — ótimo pra projetos pequenos/médios.",
        "summary_en": "Lightweight relational database that runs from a single file — great for small/medium projects.",
        "experience_pt": "Uso como banco de dados em projetos acadêmicos e pessoais, incluindo este portfólio.",
        "experience_en": "Used as the database in academic and personal projects, including this portfolio.",
    },
    {
        "skill_id": "fastapi", "category": "frameworks", "name": "FastAPI",
        "icon": "devicon-fastapi-plain", "level": 2,
        "summary_pt": "Framework Python moderno pra construir APIs, rápido e com documentação automática.",
        "summary_en": "Modern Python framework for building APIs, fast and with automatic docs.",
        "experience_pt": "Uso pra construir APIs em projetos acadêmicos e pessoais, incluindo o back-end deste portfólio.",
        "experience_en": "Used to build APIs in academic and personal projects, including this portfolio's back-end.",
    },
    {
        "skill_id": "docker", "category": "tools", "name": "Docker",
        "icon": "devicon-docker-plain", "level": 2,
        "summary_pt": "Ferramenta de containers que empacota uma aplicação com tudo que ela precisa pra rodar igual em qualquer lugar.",
        "summary_en": "Container tool that packages an application with everything it needs to run the same anywhere.",
        "experience_pt": "Uso pra empacotar e rodar projetos pessoais, e para o deploy deste portfólio.",
        "experience_en": "Used to package and run personal projects, and for this portfolio's deployment.",
    },
    {
        "skill_id": "git", "category": "tools", "name": "Git/GitHub",
        "icon": "devicon-git-plain", "level": 3,
        "summary_pt": "Sistema de controle de versão (Git) e plataforma de hospedagem de código (GitHub).",
        "summary_en": "Version control system (Git) and code hosting platform (GitHub).",
        "experience_pt": "Uso no dia a dia pra versionar todos os meus projetos acadêmicos e pessoais.",
        "experience_en": "Used daily to version all of my academic and personal projects.",
    },
    {
        "skill_id": "linux", "category": "tools", "name": "Linux",
        "icon": "devicon-linux-plain", "level": 2,
        "summary_pt": "Sistema operacional open-source, base de grande parte das ferramentas de cybersecurity (ex: Kali Linux).",
        "summary_en": "Open-source operating system, the base of most cybersecurity tooling (e.g. Kali Linux).",
        "experience_pt": "Uso o Kali Linux pra explorar ferramentas de cybersecurity por conta própria.",
        "experience_en": "I use Kali Linux to explore cybersecurity tools on my own.",
    },
]


def seed_site_content(db) -> None:
    content = db.get(SiteContent, 1)
    if content is None:
        db.add(SiteContent(id=1, **SITE_CONTENT_DEFAULTS))
        print("Conteúdo do site (sobre/contato/links) criado.")
    else:
        print("Conteúdo do site já existe, mantido.")

    if db.query(HeroLine).count() == 0:
        for index, line in enumerate(HERO_LINES_DEFAULTS):
            db.add(HeroLine(position=index, **line))
        print("Linhas do terminal do Hero criadas.")
    else:
        print("Linhas do terminal do Hero já existem, mantidas.")


def seed_skills(db) -> None:
    for index, data in enumerate(SKILLS_DEFAULTS):
        if db.query(Skill).filter(Skill.skill_id == data["skill_id"]).first() is not None:
            print(f"Skill '{data['skill_id']}' já existe, mantida.")
            continue
        db.add(Skill(position=index, **data))
        print(f"Skill '{data['skill_id']}' criada.")


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

        seed_site_content(db)
        seed_skills(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed concluído.")
