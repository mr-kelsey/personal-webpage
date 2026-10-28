from fasthtml.common import fast_app

from app.config import SiteConfig
from app.errors import not_found
from app.routes import about, admin, blog, contact, health, home, resume, work

config = SiteConfig()
app, route = fast_app(
    pico=False, exception_handlers={404: not_found}, secret_key=config.session_secret
)

for routes_module in (home, about, resume, work, blog, contact, health, admin):
    routes_module.router.to_app(app)

# fast_app() registers a catch-all static route (any path ending in a
# recognized extension, including pdf) before we get `route` back, so it
# would otherwise intercept /resume.pdf ahead of our dedicated route below
# (Starlette matches in registration order). Move it to the end so our
# explicit routes win.
static_catch_all = next(r for r in app.routes if r.name == "static_route_exts_get")
app.routes.remove(static_catch_all)
app.routes.append(static_catch_all)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
