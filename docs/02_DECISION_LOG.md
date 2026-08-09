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

Execution note:
The neutral-gateway wording for `/` was superseded by the accepted 2026-07-03
Russian-first public-entry decision. The remaining dependency-free deployment
decision stays current.

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

Execution note:
Subsequent v1.1 production QA verified the Cloudflare Pages project as healthy
and both `https://ikurabayev.kz` and `https://www.ikurabayev.kz` as active with
SSL.

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

### 2026-07-04 - Port Claude Design refinement v1.1 faithfully

Status: accepted

Context:
The owner provided a newer Claude Design export after PR #29 and approved the
data visibly displayed in those pages for public display. The export includes a
clean static `site/` source plus preview/runtime files and raw uploads that must
not be committed.

Decision:
Port the clean static `site/` design as a v1.1 visual refinement. Preserve the
Claude layout, chapter rhythm, portrait station, QR badge, AI console,
signal-chain, field-flow, phasor/DSP modules, local visual assets, and
Russian-first route. Sanitize only for security, privacy, accessibility,
routing, and Cloudflare Pages compatibility.

Consequences:
The implementation may add approved local static assets and local vanilla
JavaScript for visual behavior. Google Fonts, preview runtime files, raw
uploads, provider AI hooks, network/API calls, storage, tracking, and real AI
service claims remain excluded. Any deviation from the export should be listed
in the pull request with the exact reason.

Execution note:
Implemented and merged through PR #31. Claude Design v1.1 is the current
production visual baseline, and production-domain QA was completed after
deployment.

### 2026-08-08 - Keep production analytics-free and protect the approved public professional mailbox

Status: accepted

Context:
Production QA found that Cloudflare Web Analytics could add automatic analytics
and beacon behavior outside the repository-managed static site. The owner
disabled Web Analytics. The owner has also explicitly approved the public
professional mailbox shown in the v1.1 design and chose to retain Cloudflare
Email Address Obfuscation as anti-harvesting protection for that mailbox.

Decision:
Keep Cloudflare Web Analytics intentionally disabled. Automatic analytics or
beacon injection is not part of the approved production architecture, and
analytics, tracking, and beacons remain prohibited. Allow Cloudflare Email
Address Obfuscation only as the narrowly approved edge transformation for the
explicitly approved public professional mailbox. This protection does not make
the mailbox private. Private or personal email, phone numbers, addresses, and
other private contact data remain prohibited.

Consequences:
Repository-managed public site code must remain free of external runtime
dependencies and telemetry requests. Cloudflare edge configuration remains
outside Git and should be rechecked after relevant production configuration
changes. Do not record provider account identifiers, analytics tokens,
credentials, or other private control-plane data in the repository.

### 2026-08-09 - Establish the public Evidence Spine

Status: accepted

Context:
High-value public facts are duplicated across presentation and planning files,
while future SEO, CV, and AI work needs a small, reviewable provenance layer.

Decision:
Maintain `data/public-facts.json` as the canonical public-safe provenance layer
for high-value public facts. Registry inclusion does not automatically authorize
publication; `docs/04_PUBLIC_CONTENT_POLICY.md` remains authoritative, and the
dependency-free static HTML remains the presentation layer.

Consequences:
Update claims and sources through the issue, branch, verification, and pull
request workflow. Evidence Spine v0.1 does not auto-generate the site or
introduce a framework, dependency, backend, API, storage, or AI behavior
change.

### 2026-08-10 - Use the apex canonical metadata host and an offline public-release contract

Status: accepted

Context:
Read-only production checks found that `https://ikurabayev.kz` and
`https://www.ikurabayev.kz` both return HTTP 200 without redirecting and serve
equivalent site content after normalizing Cloudflare email obfuscation. The apex
form is the established project identity, while the repository previously had
no canonical metadata, sitemap, or automated guard against reintroducing known
truth and privacy defects.

Decision:
Use `https://ikurabayev.kz` as the repository-level canonical metadata host for
self-canonicals, hreflang, social metadata, JSON-LD, robots, and sitemap. Keep
the static presentation manually maintained and add a Python-standard-library
release validator that checks bounded Evidence Spine states, privacy exclusions,
patent presentation, semantic metadata, sitemap, robots, and the local concierge
architecture without making network requests.

Consequences:
The working `www` host may remain operational. Enforcing a `www`-to-apex redirect
is a separate optional Cloudflare control-plane action and is not implemented or
claimed here. The validator is an offline repository contract, not runtime
Evidence Spine loading, live legal-status monitoring, analytics, or an AI
backend; future routes or contract changes must update it intentionally.
