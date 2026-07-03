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

### 2026-07-03 - Use Cloudflare Pages as production host for ikurabayev.kz

Status: accepted

Context:
The domain `ikurabayev.kz` has been purchased and activated through Cloudflare.
Cloudflare DNS is active for the domain, and the dependency-free static site is
already deployed through the Cloudflare Pages project `ikurabayev-kz`. The owner
reports both `https://ikurabayev.kz` and `https://www.ikurabayev.kz` as working.

Decision:
Keep the public production QR/profile website on Cloudflare Pages. Use IDHost
as the domain registrar and only as sandbox, learning, or backup hosting if
needed. Reserve any future home mini PC for lab/private infrastructure rather
than the public production website.

Consequences:
Do not migrate the public site to virtual/shared hosting as the production core.
Do not introduce a framework, dependency, or hosting architecture change for
this decision. Do not directly expose a home server for the public QR/profile
site.

### 2026-07-03 - Port Claude Design faithfully with public-site sanitization

Status: accepted

Context:
The owner approved a faithful Claude Design port after earlier visual-polish
attempts diverged from the supplied design. The export includes usable static
HTML, CSS, local assets, and local enhancement scripts, but it also includes
Google Fonts links, Claude preview runtime files, React/Babel support code, and
a design-environment assistant hook.

Decision:
Treat the Claude Design static `site/` export as the visual source of truth for
the v1.0 redesign, while removing incompatible runtime pieces. Keep the public
site dependency-free and Cloudflare Pages compatible. Allow only local,
self-contained JavaScript for decorative motion, reveal behavior, and a
prototype AI panel that uses curated public facts only and makes no external
requests.

Consequences:
The port may closely reuse exported section structure, class names, CSS, and
local assets. External fonts, React/Babel, `support.js`, `.dc.html` runtime
files, real AI/API calls, analytics, cookies, forms that submit data, and
unapproved content claims remain excluded. Any visual deviation from Claude
Design should be explained as required by security, routing, accessibility, or
public-content policy.

### 2026-07-03 - Treat Claude Design as the visual source of truth

Status: accepted

Context:
Earlier Codex visual-polish and redesign attempts diverged from the owner's
intended Claude Design direction. The owner prefers to continue major visual
iteration in Claude Design. PR #29 established a faithful-port approach for the
accepted v1.0 redesign.

Decision:
Major visual changes should start in Claude Design. Codex should faithfully
port and sanitize the approved design, then verify accessibility, static-hosting
compatibility, security, and privacy boundaries. Codex must not creatively
redesign the site unless explicitly asked.

Consequences:
Future design PRs should include a faithfulness report that identifies the
source design, ported sections, deviations, and reasons for deviations. Export
code must be sanitized before integration. Real AI/API functionality remains a
separate phase and must not be implied by visual design ports.
