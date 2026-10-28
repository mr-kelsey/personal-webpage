# mr-kelsey

Personal resume/portfolio site for Johnathan Kelsey (BS Cybersecurity, MS Applied AI): resume, portfolio/work, blog, admin, and contact pages. Built with [FastHTML](https://www.fastht.ml/). Live at https://mr.kelseys.site — this is an established, deployed site, not a greenfield build. The original build plan (`.claude/PLAN.md`) has been removed now that it's fully executed; its hosting details (Fly.io) were no longer accurate.

## Current stack and key decisions (do not re-litigate without asking)

- Content (Work/Blog/contact messages) in **SQLite via `fastlite`**.
- Hosted on a **DigitalOcean droplet**: `docker-compose.yml` runs the FastHTML `app` container plus `caddy` for TLS/reverse proxy.
- Deploys via GitHub Actions (`.github/workflows/deploy.yml`): a test gate, then SSH (a forced-command-restricted key — it can only run the deploy script, even with the private key in hand) to `deploy.sh` on the server, which health-checks `/healthz` and rolls back the image/commit on failure.
- Content management (create/edit/delete Work & Blog entries) lives at `/admin` — single shared-password auth, deliberate simplification for a single-owner site (no multi-user, no MFA). No SSH needed for routine content edits.
- Visual style: minimal, whitespace-heavy, typography-led, dark "case file" theme — see the header comment in `static/css/site.css` for the design rationale; the `design-v1-minimal-paper` branch holds the earlier light/minimal direction as a fallback.
- The (gitignored, local-only) `README.md` has dev setup, deploy mechanics, and operational notes the user didn't want public.

## Content still to add (not yet written — confirm details with the user, don't invent)

- National Weather Service contract work.
- The hospital-waste computer vision project.
- Only one school AI project (composer classification) is live so far; more exist.

This file, plus the user's own global `~/.claude/` rules (TDD, no wildcard imports, OOP where it fits, no `global` keyword, descriptive names), govern how work on this repo should proceed.
