# IKurabayev.kz

Source of truth for the personal research website, QR landing page, engineering
portfolio, and AI-assisted project laboratory for Iskander Kurabayev.

## AI Session Quick Start

New ChatGPT/Codex sessions should begin with START_HERE.md. It defines the
mandatory reading order, current mission, active task queue, branch rules, and
safety boundaries.

This repository is not yet a website implementation. It currently defines the
project context, governance, public content boundaries, and Codex-first workflow
that future website work should follow.

## Repository Purpose

- Maintain public-facing content strategy for `ikurabayev.kz`.
- Track research and engineering portfolio decisions with clear provenance.
- Provide repeatable instructions for AI-assisted work.
- Keep website implementation work separate from governance decisions until the
  initial direction is reviewed.

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

The repository contains only Markdown governance and planning files. Do not add a
website framework, `package.json`, dependencies, private data, or unpublished
research data until a specific issue and pull request justify that change.

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
