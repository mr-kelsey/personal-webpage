from starlette.testclient import TestClient

from conftest import ADMIN_PASSWORD_FOR_TESTS


def test_admin_login_page_returns_200(client: TestClient) -> None:
    response = client.get("/admin/login")
    assert response.status_code == 200


def test_admin_login_page_shows_password_field(client: TestClient) -> None:
    response = client.get("/admin/login")
    assert 'name="password"' in response.text


def test_post_admin_login_with_correct_password_redirects_to_dashboard(
    client: TestClient,
) -> None:
    response = client.post(
        "/admin/login",
        data={"password": ADMIN_PASSWORD_FOR_TESTS},
        follow_redirects=False,
    )
    assert response.headers["location"] == "/admin"


def test_post_admin_login_with_wrong_password_shows_error(client: TestClient) -> None:
    response = client.post("/admin/login", data={"password": "wrong"})
    assert "Incorrect password" in response.text


def test_post_admin_login_with_wrong_password_does_not_set_session(
    client: TestClient,
) -> None:
    client.post("/admin/login", data={"password": "wrong"})
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code in (302, 303, 307)


def test_get_admin_dashboard_redirects_when_not_authenticated(
    client: TestClient,
) -> None:
    response = client.get("/admin", follow_redirects=False)
    assert response.headers["location"] == "/admin/login"


def test_get_admin_dashboard_returns_200_when_authenticated(
    admin_client: TestClient,
) -> None:
    response = admin_client.get("/admin")
    assert response.status_code == 200


def test_post_admin_logout_clears_session(admin_client: TestClient) -> None:
    admin_client.post("/admin/logout")
    response = admin_client.get("/admin", follow_redirects=False)
    assert response.headers["location"] == "/admin/login"
