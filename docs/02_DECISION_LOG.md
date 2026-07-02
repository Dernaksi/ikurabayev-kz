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

### 2026-07-02 - Continue dependency-free static HTML for first deployment

Status: accepted

Context:
A later blitz plan proposed Astro and a different launch path, but it assumed an
earlier repository state. The repository already has PR #14 website information
architecture and PR #15 dependency-free static HTML skeleton.

Decision:
Continue the dependency-free static HTML site for first Cloudflare Pages
readiness. Do not migrate to Astro for the first deployment. Keep Astro as a
future option if site complexity or multilingual duplication justifies it. Use
`/qr` as the direct QR-code target for business cards and slides while `/`
remains a neutral gateway.

Consequences:
Next work should focus on reconciliation, verified QR links/Russian QR copy, and
Cloudflare Pages readiness. No `package.json` or dependencies are needed for the
current deployment path. Framework migration requires a separate future decision
and PR.

### 2026-07-03 - Make Russian the primary public entry language

Status: accepted

Context:
The first practical audience for the public site includes Kazakhstan energy
sector contacts, production and engineering contacts, energy-audit clients, and
real-world QR visitors who are more likely to work in Russian. English remains
important for international research and academic review. Kazakh remains
supported, but its text still requires language review before stronger launch
use.

Decision:
Make `/` and `/qr` Russian-first for the initial public experience. Keep `/ru`
as the primary full profile, keep `/en` as the international research profile,
and keep `/kk` as a conservative supported route pending language review.

Consequences:
Navigation, route cards, QR actions, and homepage copy should lead with Russian
while preserving multilingual access. This decision does not add new biography,
publication, patent, contact, metric, role, product, or affiliation claims.
