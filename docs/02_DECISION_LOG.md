# Decision Log

This file records durable project decisions. Add entries when a decision changes
repository structure, public content policy, website architecture, deployment, or
AI Lab workflow.

## Format

```text
YYYY-MM-DD - Decision title
Status: proposed | accepted | superseded
Context:
Decision:
Consequences:
```

## Decisions

### 2026-07-01 - Establish AI Lab foundation

Status: accepted

Context:
The repository needs governance before website implementation so future AI
assisted changes are scoped, reviewable, and safe for public content.

Decision:
Create Markdown governance, project context, workflow, roadmap, public content
policy, Codex prompts, and GitHub issue and pull request templates before adding
any website framework or dependencies.

Consequences:
Future work should start from issues, proceed through branches and pull
requests, and avoid direct pushes to `main`.

