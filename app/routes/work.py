from fasthtml import common as Fast

from app.db import site_db
from app.layout import site_layout

router = Fast.APIRouter()


def _project_row(index: int, project) -> Fast.Li:
    return Fast.Li(
        Fast.A(
            Fast.Span(f"{index:03d}", cls="row-index"),
            Fast.Span(project.title, cls="row-title"),
            Fast.Span(project.description, cls="row-detail"),
            href=f"/work/{project.slug}",
            cls="row-link",
        )
    )


@router("/work")
def get():
    projects = site_db.projects(order_by="id")
    return site_layout(
        "Work",
        Fast.H1("Work"),
        Fast.Ul(
            *(_project_row(i, project) for i, project in enumerate(projects, start=1)),
            cls="row-list",
        ),
    )


@router("/work/{slug}")
def get(slug: str):
    found = site_db.projects(where="slug=?", where_args=[slug])
    if not found:
        raise Fast.HTTPException(status_code=404)
    project = found[0]
    return site_layout(
        project.title,
        Fast.A("Work", href="/work", cls="back-link"),
        Fast.H1(project.title),
        Fast.P(project.description, cls="lede"),
        *(Fast.P(paragraph) for paragraph in project.body.split("\n\n") if paragraph),
        Fast.Div(
            Fast.A(project.url, href=project.url) if project.url else None,
            Fast.A("Download Report (PDF)", href=project.report_pdf)
            if project.report_pdf
            else None,
            cls="project-links",
        ),
    )
