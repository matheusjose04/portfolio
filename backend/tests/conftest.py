import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("ADMIN_USER", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "admin123")
os.environ.setdefault("DATABASE_URL", "sqlite:///./data/test.db")
os.environ.setdefault("ORIGINS", "http://localhost:4321")

import pytest
from fastapi.testclient import TestClient

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import AdminUser, Skill

from seed import SKILLS_DEFAULTS


@pytest.fixture(autouse=True)
def _reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(
        AdminUser(
            username=os.environ["ADMIN_USER"],
            password_hash=hash_password(os.environ["ADMIN_PASSWORD"]),
        )
    )
    for index, data in enumerate(SKILLS_DEFAULTS):
        db.add(Skill(position=index, **data))
    db.commit()
    db.close()
    yield


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
