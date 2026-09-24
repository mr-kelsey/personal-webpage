from fasthtml import common as Fast

from app.db import site_db
from app.layout import site_layout

router = Fast.APIRouter()


def _post_card(post) -> Fast.Div:
    return Fast.Div(
        Fast.A(post.title, href=f"/blog/{post.slug}"),
        cls="post-card",
    )


@router("/blog")
def get():
    posts = site_db.posts(order_by="id")
    return site_layout(
        "Blog",
        Fast.H1("Blog"),
        *(_post_card(post) for post in posts),
    )


@router("/blog/{slug}")
def get(slug: str):
    found = site_db.posts(where="slug=?", where_args=[slug])
    if not found:
        raise Fast.HTTPException(status_code=404)
    post = found[0]
    return site_layout(
        post.title,
        Fast.H1(post.title),
        Fast.P(post.body),
    )
