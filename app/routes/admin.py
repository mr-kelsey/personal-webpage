from fasthtml import common as Fast

from app.auth import SESSION_KEY, require_admin, verify_password
from app.layout import site_layout

router = Fast.APIRouter()


def _login_form(error: str | None = None) -> Fast.Form:
    return Fast.Form(
        Fast.Label("Password", Fast.Input(name="password", type="password", required=True)),
        Fast.P(error, cls="error") if error else None,
        Fast.Button("Log in", type="submit"),
        method="post",
        action="/admin/login",
    )


@router("/admin/login")
def get():
    return site_layout("Admin Login", Fast.H1("Admin Login"), _login_form())


@router("/admin/login")
def post(password: str, session):
    if not verify_password(password):
        return site_layout(
            "Admin Login",
            Fast.H1("Admin Login"),
            _login_form(error="Incorrect password."),
        )
    session[SESSION_KEY] = True
    return Fast.Redirect("/admin")


@router("/admin/logout")
def post(session):
    session.pop(SESSION_KEY, None)
    return Fast.Redirect("/admin/login")


@router("/admin")
def get(session):
    if (redirect := require_admin(session)) is not None:
        return redirect
    return site_layout(
        "Admin",
        Fast.H1("Admin"),
        Fast.Div(
            Fast.A("Manage Work", href="/admin/work"),
            Fast.A("Manage Blog", href="/admin/blog"),
            cls="admin-links",
        ),
    )
