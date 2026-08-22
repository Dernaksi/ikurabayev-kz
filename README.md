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

The project now separates evidence, presentation, release validation, future AI,
relationships, deterministic public-CV generation, and block-level provenance.
Canonical facts remain in `data/public-facts.json`; the compact relationship
layer is `data/public-research-graph.json`; the manually maintained static
presentation remains under `site/`, except for the generated RU/EN Living
Public CV routes at `/cv/` and `/en/cv/`. The CV generator owns only those two
site documents; it does not modify the main profile routes.

Cloudflare Pages preview is live at `https://ikurabayev-kz.pages.dev`. The
custom production domains `https://ikurabayev.kz` and
`https://www.ikurabayev.kz` were verified active with SSL through Cloudflare
Pages. The approved public professional contact route is live. Evidence-backed
public release v1.2 reconciles patent legal-status presentation and credential
privacy, establishes apex canonical metadata, adds dependency-free semantic
publishing, and introduces an offline public-release validator. PRs #45 and #46
publish the owner-approved certified-energy-auditor status and 2026-08-14 to
2029-08-06 term through the Evidence Spine, generated RU/EN public CV,
localized site routes, and the local public-facts-only concierge. Production QA
on 2026-08-22 confirmed the update on the apex, `www`, and Cloudflare Pages
preview hosts without publishing private credential details. The reviewed
Living Public CV is published as dependency-free RU/EN HTML at `/cv/` and
`/en/cv/`; PDF remains a separate future export. Remaining work includes Kazakh
language review, owner review of conflicting university-role start dates, the
long-term semantic roles of `/` and `/ru/`, an optional Cloudflare
`www`-to-apex redirect, and a separate real-AI backend architecture.

Public Knowledge System v0.2 adds a bounded research graph, deterministic RU/EN
Living Public CV documents, block-level provenance, and offline validators. The
Markdown artifacts remain review documents; equivalent generated HTML is
published without runtime JSON loading, scripts, or private evidence.

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
- [docs/17_PUBLIC_FACTS_REGISTRY.md](docs/17_PUBLIC_FACTS_REGISTRY.md) - Evidence
  Spine schema, status model, source hierarchy, privacy boundary, and workflow.
- [docs/18_PUBLIC_RESEARCH_GRAPH.md](docs/18_PUBLIC_RESEARCH_GRAPH.md) - bounded
  relationship model, topics, predicates, status inheritance, and anti-inference
  rules.
- [docs/19_LIVING_PUBLIC_CV.md](docs/19_LIVING_PUBLIC_CV.md) - deterministic
  RU/EN CV generation, block provenance, privacy, and publication workflow.
