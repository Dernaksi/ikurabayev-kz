# IKurabayev.kz

Source of truth for the personal research website, QR landing page, engineering
portfolio, and AI-assisted project laboratory for Iskander Kurabayev.

## AI Session Quick Start

New ChatGPT/Codex sessions should begin with START_HERE.md. It defines the
mandatory reading order, current mission, active task queue, branch rules, and
safety boundaries.

This repository contains the project governance documents and a
dependency-free static HTML site under `site/`. The Cloudflare Pages preview is
working, while the production custom domain `ikurabayev.kz` remains pending
activation and DNS completion.

## Repository Purpose

- Maintain public-facing content strategy for `ikurabayev.kz`.
- Track research and engineering portfolio decisions with clear provenance.
- Provide repeatable instructions for AI-assisted work.
- Keep website implementation work conservative, reviewable, framework-free,
  and dependency-free until a future approved issue and pull request justify a
  different technical path.

## AI Lab Workflow

Work should follow an issue to branch to pull request flow:

1. Create or select a GitHub issue that describes the task.
2. Create a focused branch for the issue.
3. Ask Codex to inspect first, then implement only the approved scope.
4. Open a pull request with a clear summary and checks.
5. Review the diff, content boundaries, and provenance.
6. Squash merge after approval.

Do not push directly to `main`.

## Current Status

The repository contains Markdown governance and planning files plus the current
dependency-free static HTML site in `site/`.

Cloudflare Pages preview is live at `https://ikurabayev-kz.pages.dev`. The
custom production domain `ikurabayev.kz` is not active yet and still requires
domain activation and DNS verification.

The project remains framework-free and dependency-free for now. Do not add a
website framework, `package.json`, dependencies, private contact details,
unsupported public claims, or unpublished research data until a specific issue
and pull request justify that change.

## Key Documents

- [AGENTS.md](AGENTS.md) - repository instructions for Codex and other agents.
- [docs/00_PROJECT_CONTEXT.md](docs/00_PROJECT_CONTEXT.md) - project identity,
  goals, audiences, and boundaries.
- [docs/01_AI_LAB_WORKFLOW.md](docs/01_AI_LAB_WORKFLOW.md) - AI-assisted task
  workflow.
- [docs/02_DECISION_LOG.md](docs/02_DECISION_LOG.md) - project decisions.
- [docs/03_ROADMAP.md](docs/03_ROADMAP.md) - staged roadmap.
- [docs/04_PUBLIC_CONTENT_POLICY.md](docs/04_PUBLIC_CONTENT_POLICY.md) - public
  content rules and privacy boundaries.
