# mr-kelsey: personal resume/portfolio site (FastHTML)

## Context

Greenfield project for a recent graduate (BS in Cybersecurity, MS in Applied AI) entering the job market. They have not followed a traditional career path — mostly self-employed/contract work rather than a W-2 history. Notable experience to feature:

- Contract work for the **National Weather Service**.
- A large-scale project using **computer vision to reduce hospital waste**.
- A number of **school projects in AI** worth surfacing as portfolio pieces.

The site needs to cover: **resume, portfolio/work, blog, contact**.

Style target: [alishaselena.com](https://www.alishaselena.com/) — minimal, whitespace-heavy, typography-led design; four-page nav (Home/About/Work/Contact); resume offered as a viewable/downloadable doc; personality-driven copy over heavy visual design. Adapt the *feel*, not the literal content/tone — this site should read as cybersecurity/applied-AI, not copywriting.

Decisions already made with the user (do not re-litigate without asking):
- **Content storage**: SQLite via `fastlite` (not flat markdown files) — chosen so posts/projects can be added without a redeploy later.
- **Hosting**: **Fly.io**, against a domain the user already owns (no host yet).

This plan will be executed by a Claude Code instance working **under the user's direct guidance** (not fully autonomously) — check in at the marked decision points rather than pushing straight through to the end, and stop for a real conversation when it comes to writing actual resume/bio copy (step 9): that content should come from/with the user, not be invented wholesale.

## Deviations from typical FastHTML tutorials (per the user's global coding rules)

- **No wildcard imports.** Tutorials use `from fasthtml.common import *`; import explicit names instead (`from fasthtml.common import fast_app, Titled, Div, P, ...`).
- **OOP over ad-hoc functions** where it earns its keep: resume/project/post/contact-message data as `@dataclass` models; page shell as a `Layout` class; email sending behind an `EmailSender` interface (Strategy pattern: `ResendEmailSender` for prod, `ConsoleEmailSender` for dev/test) instead of a bare function — this also sidesteps mocking a real dependency in tests.
- **No `global` keyword.** Module-level `app`, `rt`, `db` singletons from `fast_app()`/`database()` are still fine — that's how every ASGI framework wires itself up (same as `app = Flask(__name__)`), it's not mutable state manipulated via the `global` keyword inside functions.
- **Tests written before each implementation step** (TDD), one assertion per test, descriptive names (`returns_200_when_...`), integration-style against a real (temp-file) SQLite DB and Starlette `TestClient` rather than mocks. The one exception is the outbound Resend API call, swapped for `ConsoleEmailSender` in tests via dependency injection rather than mocked.
- Sign commits `-Claude`, not `Co-Authored-By:`.

## FastHTML/fastlite/Fly.io conventions to follow (researched, verified against docs where noted)

- `app, rt = fast_app(...)` — `rt` is the route decorator; HTTP method is inferred from the handler function's **name** (`def get():` / `def post():`) under the same `@rt("/path")`, not from the decorator itself.
- Handlers return **FT** (FastTags) objects — plain nested Python calls (`Div`, `P`, `Form`, `Titled(...)`) — no Jinja/templating layer. Build a `Layout` class/callable that wraps page content in shared nav+footer.
- Form fields are auto-parsed into typed handler args by matching `name` attributes: `def post(name: str, email: str, message: str):`.
- **Post/Redirect/Get**: return `Redirect("/contact")` from the POST handler after persisting. Flash messages aren't a built-in FastHTML feature — layer it on the session dict FastHTML wires up (`sess["flash"] = "..."`, popped in the GET handler). Never pass flash text via query params.
- Serve the resume PDF via a dedicated route using Starlette's `FileResponse` (PDF isn't in `fast_app()`'s default auto-served static extensions):
  ```python
  from starlette.responses import FileResponse

  @rt("/resume.pdf")
  def get():
      return FileResponse("static/resume.pdf", filename="resume.pdf", media_type="application/pdf")
  ```
- **fastlite** (MiniDataAPI spec) for the DB:
  ```python
  from fastlite import database

  db = database("data/app.db")
  projects = db.create(Project, pk="id")   # Project is a plain class with type-annotated fields
  projects.insert(Project(title=..., description=..., url=...))
  projects()                                # all rows
  projects(where="slug=?", where_args=[slug])
  ```
  No migration framework beyond `db.create(..., transform=True)` for best-effort schema sync — acceptable for this project's scale.
- **Testing**: FastHTML apps are Starlette apps — use Starlette's `TestClient` (httpx-based) directly against the `app` instance from `fast_app()`.
- **Deployment**: no official `fh-fly` CLI exists. Use plain `flyctl`:
  - `Dockerfile`: Python slim base image, `pip install` deps, then run the ASGI app directly with **`uvicorn app.main:app --host 0.0.0.0 --port 8080`** rather than FastHTML's `serve()` helper (which defaults to `reload=True`, dev-oriented file-watching — wrong for production).
  - `fly.toml`: `internal_port = 8080` must match the Dockerfile's bound port; `force_https = true`.
  - `fly launch` generates `fly.toml` from the Dockerfile; `fly deploy` ships it; `fly certs add <domain>` + the DNS records it prints (added at the user's registrar) wires up the existing domain; `fly secrets set RESEND_API_KEY=...` for the contact-form email key.
- **Email**: prefer the **Resend** API (`pip install resend`, `RESEND_API_KEY` env var) over raw `smtplib` — less to get wrong around TLS/deliverability for a simple contact form.

## Project structure

```
mr-kelsey/
  app/
    __init__.py
    main.py            # fast_app() setup, mounts routes, serve()/uvicorn entrypoint
    config.py          # SiteConfig dataclass: reads env vars (RESEND_API_KEY, CONTACT_TO_EMAIL, etc.)
    layout.py           # Layout class: shared shell (nav/footer) wrapping page content
    db.py               # database() connection + table bootstrap
    models.py           # Project, Post, ContactMessage dataclasses
    email.py            # EmailSender ABC, ResendEmailSender, ConsoleEmailSender
    routes/
      __init__.py
      home.py            # GET /
      about.py           # GET /about
      resume.py          # GET /resume (view), GET /resume.pdf (download)
      work.py            # GET /work, GET /work/{slug}
      blog.py            # GET /blog, GET /blog/{slug}
      contact.py         # GET/POST /contact
  static/
    css/site.css
    resume.pdf
  scripts/
    seed_db.py           # populates SQLite with initial Project/Post rows
  tests/
    conftest.py          # TestClient fixture against a temp SQLite file
    test_home.py
    test_about.py
    test_resume.py
    test_work.py
    test_blog.py
    test_contact.py
    test_email.py
  Dockerfile
  fly.toml
  pyproject.toml
  .env.example
  README.md
```

## Implementation order (tests first at each step)

1. **Scaffold**: `pyproject.toml` (deps: `python-fasthtml`, `fastlite`, `resend`, `pytest`, `httpx`), `.env.example`, empty package skeleton.
2. **Layout + static pages**: tests asserting `GET /` and `GET /about` return 200 and expected copy/heading; implement `Layout` class and `home.py`/`about.py` against it.
3. **Resume**: tests for `GET /resume` (200, shows resume content) and `GET /resume.pdf` (200, `Content-Type: application/pdf`, attachment disposition) via `FileResponse`; implement.
4. **Data layer**: tests for `Project`/`Post`/`ContactMessage` table creation and CRUD against a temp-file `fastlite` DB; implement `db.py`/`models.py`, then `scripts/seed_db.py` with placeholder rows.
5. **Work (portfolio)**: tests for `GET /work` (lists seeded projects) and `GET /work/{slug}` (200 for a real slug, 404 for unknown); implement DB-backed routes.
6. **Blog**: same pattern as Work (`GET /blog`, `GET /blog/{slug}`).
7. **Contact**: tests — `GET /contact` returns the form; `POST /contact` with valid data returns a redirect (PRG), persists a `ContactMessage` row, and calls the injected `EmailSender`. Implement `EmailSender` ABC + `ResendEmailSender`/`ConsoleEmailSender`; default to `ConsoleEmailSender` unless `RESEND_API_KEY` is configured.
8. **Styling pass**: single `static/css/site.css` matching the reference site's aesthetic (minimal nav, generous whitespace, strong type hierarchy) adapted to a cybersecurity/AI tone.
   ⚠️ **Check in with the user** before finalizing visual direction — "matches alishaselena.com's feel" is subjective; show them a screenshot/description before going further.
9. **Content pass — do this WITH the user, not for them.** Draft actual resume bullets and About bio together; write up the NWS contract work, the hospital-waste CV project, and the school AI projects as real Work entries; seed real data via `scripts/seed_db.py`. Do not invent employment history, dates, or metrics.
10. **Deploy**: `Dockerfile`, `fly.toml` as above, `fly launch` + `fly deploy`, `fly certs add <domain>` with DNS records added at the user's registrar, `fly secrets set RESEND_API_KEY=...`.
    ⚠️ **Check in with the user** before running `fly launch`/`fly deploy` (creates a real, billable cloud resource) and before touching their domain's DNS.
11. **README**: local dev (`pytest`, run server), deploy steps, how to add a new Work/Blog entry.

## Verification

- `pytest` (all suites green) after each step before moving to the next, per TDD.
- Manual smoke test: run the app locally (`uvicorn app.main:app --reload`), click through Home → About → Resume (view + download) → Work → Blog → Contact (submit form, confirm flash + console-logged/sent email), before considering a step done.
- After deploy: hit the live domain over HTTPS and repeat the same click-through.
