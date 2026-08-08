# IKurabayev.kz

Source of truth for the personal research website, QR landing page, engineering
portfolio, and AI-assisted project laboratory for Iskander Kurabayev.

## AI Session Quick Start

New ChatGPT/Codex sessions should begin with START_HERE.md. It defines the
mandatory reading order, current mission, active task queue, branch rules, and
safety boundaries.

This repository contains the project governance documents and a
dependency-free static HTML site under `site/`. The Cloudflare Pages preview is
working, and the production custom domain `ikurabayev.kz` is active through
Cloudflare Pages.

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

Claude Design v1.1, merged through PR #31, is the current production visual
baseline. Production-domain QA has been completed for this release.

Cloudflare Pages preview is live at `https://ikurabayev-kz.pages.dev`. The
custom production domains `https://ikurabayev.kz` and
`https://www.ikurabayev.kz` were verified active with SSL through Cloudflare
Pages. The approved public professional contact route is live. Remaining work
includes reconciling the local AI concierge public-email wording with the
approved public professional contact route, accessibility and QR-payload
follow-ups, patent-registry verification, SEO metadata, the `www` versus apex
policy, Kazakh language review, a sanitized public CV, and a separate real-AI
backend architecture.

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
- [docs/16_VISUAL_DESIGN_SYSTEM.md](docs/16_VISUAL_DESIGN_SYSTEM.md) - Claude
  Design to Codex faithful-port workflow.
