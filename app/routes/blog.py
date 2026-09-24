from fasthtml import common as Fast

from app.db import site_db
from app.layout import site_layout

router = Fast.APIRouter()


def _post_row(post) -> Fast.Li:
    return Fast.Li(
        Fast.A(
            Fast.Span(post.title, cls="row-title"),
            href=f"/blog/{post.slug}",
            cls="row-link",
        )
    )


@router("/blog")
def get():
    posts = site_db.posts(order_by="id")
    return site_layout(
        "Blog",
        Fast.H1("Blog"),
        Fast.Ul(*(_post_row(post) for post in posts), cls="row-list"),
    )


@router("/blog/{slug}")
def get(slug: str):
    found = site_db.posts(where="slug=?", where_args=[slug])
    if not found:
        raise Fast.HTTPException(status_code=404)
    post = found[0]
    return site_layout(
        post.title,
        Fast.A("Blog", href="/blog", cls="back-link"),
        Fast.H1(post.title),
        Fast.P(post.body, cls="lede"),
    )
