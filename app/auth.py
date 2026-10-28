from hmac import compare_digest

from fasthtml import common as Fast

from app.config import SiteConfig
from app.layout import site_layout

SESSION_KEY = "is_admin"


def verify_password(candidate: str) -> bool:
    expected = SiteConfig().admin_password
    if not expected:
        return False
    return compare_digest(candidate, expected)


def is_authenticated(session) -> bool:
    return bool(session.get(SESSION_KEY))


def require_admin(session) -> Fast.Redirect | None:
    if not is_authenticated(session):
        return Fast.Redirect("/admin/login")
    return None


def admin_nav() -> Fast.Div:
    """A small bar of admin-only controls (back to dashboard, log out),
    shared across every /admin/* page."""
    return Fast.Div(
        Fast.A("Admin", href="/admin"),
        Fast.Form(
            Fast.Button("Log out", type="submit"),
            method="post",
            action="/admin/logout",
        ),
        cls="admin-nav",
    )


def admin_layout(title: str, *content) -> tuple:
    """The shared page shell for authenticated /admin/* pages — always
    includes admin_nav(), so a new admin route can't render without it
    by omission the way a bare content helper could."""
    return site_layout(title, admin_nav(), *content)
