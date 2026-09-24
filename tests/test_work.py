from starlette.testclient import TestClient

from app.db import Database
from app.models import Project


def test_returns_200_for_work_index(client: TestClient) -> None:
    response = client.get("/work")
    assert response.status_code == 200


def test_work_index_lists_seeded_project_title(client: TestClient, db: Database) -> None:
    db.projects.insert(Project(slug="hospital-cv", title="Hospital CV", description="d", url=""))
    response = client.get("/work")
    assert "Hospital CV" in response.text


def test_returns_200_for_known_project_slug(client: TestClient, db: Database) -> None:
    db.projects.insert(Project(slug="hospital-cv", title="Hospital CV", description="d", url=""))
    response = client.get("/work/hospital-cv")
    assert response.status_code == 200


def test_project_detail_shows_description(client: TestClient, db: Database) -> None:
    db.projects.insert(
        Project(slug="hospital-cv", title="Hospital CV", description="Reduces hospital waste via CV", url="")
    )
    response = client.get("/work/hospital-cv")
    assert "Reduces hospital waste via CV" in response.text


def test_returns_404_for_unknown_project_slug(client: TestClient) -> None:
    response = client.get("/work/does-not-exist")
    assert response.status_code == 404
