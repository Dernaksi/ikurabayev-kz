# AGENTS.md

Repository instructions for Codex and other AI agents working on IKurabayev.kz.

## Project Identity

IKurabayev.kz is the source of truth for a personal research website, QR landing
page, engineering portfolio, and AI-assisted project laboratory for Iskander
Kurabayev.

This repository should evolve conservatively. Treat public credibility,
provenance, privacy, and reproducibility as first-class requirements.

## Working Rules

- Work in conservative research-reproducibility mode.
- Inspect the repository structure, README, docs, issue context, and relevant
  files before editing.
- Prefer minimal, atomic changes.
- Do not create the website implementation unless the task explicitly asks for
  it.
- Do not add `package.json`, dependencies, generated assets, build output, or
  framework scaffolding without explicit approval.
- Keep governance and planning documents in Markdown unless a task explicitly
  requires another format.
- Do not add private data, phone numbers, tokens, credentials, `.env` files,
  contracts, unpublished research data, raw datasets, or confidential material.
- Do not fabricate metrics, publications, roles, affiliations, research results,
  datasets, figures, or portfolio claims.
- If information is missing, say it is missing and describe what source or
  review is required.

## Codex-First Workflow

Use the repository as an AI Lab:

1. Issue: define the task, scope, source material, and acceptance criteria.
2. Branch: create a focused branch for the issue.
3. Inspect: ask Codex to inspect and report before implementation.
4. Implement: apply a small, reviewable change.
5. PR: open a pull request with summary, checks, and risk notes.
6. Review: verify content boundaries, provenance, and diff scope.
7. Merge: squash merge after approval.

Do not push directly to `main`.

## Content Boundaries

Public content must be suitable for publication on a personal website and QR
landing page. When in doubt, keep the repository generic and leave placeholders
for later human review.

Allowed examples:

- Public biography drafts.
- Public research interests.
- Public project summaries.
- Public links that are intentionally meant to be shared.
- Governance, workflow, and content policy documents.

Disallowed examples:

- Private contact details.
- Secrets, tokens, passwords, SSH keys, or API keys.
- Unpublished research data or confidential manuscripts.
- Contracts, financial details, or private institutional documents.
- Claims that cannot be verified from public or approved sources.

## Reporting After Changes

After changing files, report:

1. Files inspected.
2. Files changed.
3. Commands run.
4. Tests or checks performed.
5. Remaining risks or TODOs.

