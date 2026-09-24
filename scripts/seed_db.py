from datetime import datetime, timezone

from app.db import site_db
from app.models import Post, Project

PLACEHOLDER_PROJECTS = (
    Project(
        slug="placeholder-project",
        title="Placeholder Project",
        description="Real portfolio entries are added in the content pass (PLAN.md step 9).",
        url="",
        created_at=datetime.now(timezone.utc).isoformat(),
    ),
)

PLACEHOLDER_POSTS = (
    Post(
        slug="placeholder-post",
        title="Placeholder Post",
        body="Real posts are added in the content pass (PLAN.md step 9).",
        created_at=datetime.now(timezone.utc).isoformat(),
    ),
)


def seed() -> None:
    for project in PLACEHOLDER_PROJECTS:
        site_db.projects.insert(project)
    for post in PLACEHOLDER_POSTS:
        site_db.posts.insert(post)


if __name__ == "__main__":
    seed()
