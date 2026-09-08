from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_login_wrong_password_returns_401(client: TestClient) -> None:
    res = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert res.status_code == 401


def test_login_correct_password_returns_token(client: TestClient) -> None:
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_create_project_without_token_returns_401(client: TestClient) -> None:
    res = client.post(
        "/api/projects",
        json={
            "title": "Teste",
            "category": "small",
            "skills": ["python"],
            "description_pt": "desc",
            "why_pt": "motivo",
        },
    )
    assert res.status_code == 401


def test_create_project_with_token_returns_201_and_appears_in_list(client: TestClient) -> None:
    login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login.json()["access_token"]

    res = client.post(
        "/api/projects",
        json={
            "title": "Projeto Teste",
            "category": "small",
            "skills": ["python"],
            "description_pt": "desc",
            "why_pt": "motivo",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    assert res.json()["slug"] == "projeto-teste"

    listing = client.get("/api/projects", params={"category": "small"})
    assert any(p["title"] == "Projeto Teste" for p in listing.json())


def test_create_project_rejects_invalid_skill(client: TestClient) -> None:
    login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login.json()["access_token"]

    res = client.post(
        "/api/projects",
        json={
            "title": "Projeto Inválido",
            "category": "small",
            "skills": ["cobol"],
            "description_pt": "desc",
            "why_pt": "motivo",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422
