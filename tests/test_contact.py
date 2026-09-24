from starlette.testclient import TestClient

from app.db import Database
from app.email import ConsoleEmailSender

VALID_SUBMISSION = {"name": "Alex", "email": "alex@example.com", "message": "Hi there"}


def test_returns_200_for_contact_page(client: TestClient) -> None:
    response = client.get("/contact")
    assert response.status_code == 200


def test_contact_page_includes_message_field(client: TestClient) -> None:
    response = client.get("/contact")
    assert 'name="message"' in response.text


def test_post_contact_redirects(client: TestClient) -> None:
    response = client.post("/contact", data=VALID_SUBMISSION, follow_redirects=False)
    assert response.status_code == 303


def test_post_contact_redirects_to_contact_page(client: TestClient) -> None:
    response = client.post("/contact", data=VALID_SUBMISSION, follow_redirects=False)
    assert response.headers["location"] == "/contact"


def test_post_contact_persists_message(client: TestClient, db: Database) -> None:
    client.post("/contact", data=VALID_SUBMISSION, follow_redirects=False)
    assert db.contact_messages.count == 1


def test_post_contact_sends_email_via_injected_sender(
    client: TestClient, email_sender: ConsoleEmailSender
) -> None:
    client.post("/contact", data=VALID_SUBMISSION, follow_redirects=False)
    assert len(email_sender.sent_messages) == 1


def test_flash_message_shown_after_successful_submit(client: TestClient) -> None:
    response = client.post("/contact", data=VALID_SUBMISSION)
    assert "Thanks" in response.text
