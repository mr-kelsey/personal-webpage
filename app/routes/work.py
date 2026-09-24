from fasthtml import common as Fast

from app.db import site_db
from app.layout import site_layout

router = Fast.APIRouter()


def _project_card(project) -> Fast.Div:
    return Fast.Div(
        Fast.A(project.title, href=f"/work/{project.slug}"),
        Fast.P(project.description),
        cls="project-card",
    )


@router("/work")
def get():
    projects = site_db.projects(order_by="id")
    return site_layout(
        "Work",
        Fast.H1("Work"),
        *(_project_card(project) for project in projects),
    )


@router("/work/{slug}")
def get(slug: str):
    found = site_db.projects(where="slug=?", where_args=[slug])
    if not found:
        raise Fast.HTTPException(status_code=404)
    project = found[0]
    return site_layout(
        project.title,
        Fast.H1(project.title),
        Fast.P(project.description),
        Fast.A(project.url, href=project.url) if project.url else None,
    )
