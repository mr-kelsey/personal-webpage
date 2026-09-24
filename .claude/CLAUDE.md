# mr-kelsey

Personal resume/portfolio site for a recent grad (BS Cybersecurity, MS Applied AI) entering the job market: resume, portfolio/work, blog, and contact pages. Built with [FastHTML](https://www.fastht.ml/).

**The implementation plan lives at [`.claude/PLAN.md`](.claude/PLAN.md) — read it before writing any code.** It covers project structure, build order (TDD, step by step), FastHTML/fastlite/Fly.io conventions to follow, and where to pause and check in with the user rather than pushing ahead solo (visual direction, resume/bio content, and anything that touches real cloud resources or DNS).

## Key decisions already made (do not re-litigate without asking)

- Content (projects/posts) is stored in **SQLite via `fastlite`**, not flat files.
- Hosting is **Fly.io**, against a domain the user already owns but hasn't pointed anywhere yet.
- Visual style targets the feel of [alishaselena.com](https://www.alishaselena.com/) — minimal, whitespace-heavy, typography-led — adapted to a cybersecurity/applied-AI tone, not copied verbatim.

## Notable background to reflect in content (do not invent beyond this — confirm details with the user)

- BS in Cybersecurity, MS in Applied AI.
- Non-traditional career path: mostly self-employed/contract rather than a conventional job history.
- Contract work for the **National Weather Service**.
- A large-scale **computer vision project reducing hospital waste**.
- Several **school projects in AI** worth presenting as portfolio pieces.

This CLAUDE.md file, plus the user's own global `~/.claude/` rules (TDD, no wildcard imports, OOP where it fits, no `global` keyword, descriptive names), govern how work on this repo should proceed.
