# Domain and Infrastructure Strategy

Status: accepted/current architecture and operations note.

## Purpose

This document records the production-domain and infrastructure strategy for
IKurabayev.kz after the custom domain became active through Cloudflare.

It is not a credentials inventory, hosting runbook, DNS export, or private
infrastructure map. Do not add provider account IDs, API tokens, screenshots,
private contact details, research data, or family/private storage content here.

## Current Production Architecture

The public website production path is:

```text
GitHub repository -> Cloudflare Pages project -> ikurabayev.kz / www.ikurabayev.kz
```

Current public-hosting assumptions:

- Source of truth: `Dernaksi/ikurabayev-kz`.
- Static site source: `site/`.
- Production host: Cloudflare Pages.
- Current Pages project: `ikurabayev-kz`.
- Custom production domain: `https://ikurabayev.kz`.
- `https://ikurabayev.kz` and `https://www.ikurabayev.kz` were verified active
  with SSL.

Claude Design v1.1 from PR #31 is the current production visual baseline, and
production-domain QA has been completed for this release. The approved public
professional contact route is live. SEO metadata, Kazakh language review,
patent-registry verification, and a sanitized public CV have since received
bounded production work. The Kazakh display-name canonicalization, `www` versus
apex policy, and separate real-AI backend architecture remain pending.

## DNS Authority

Cloudflare DNS is the active DNS authority for the domain.

Operational notes:

- DNS changes should be made through Cloudflare unless a later approved
  decision changes the authority model.
- Do not commit DNS screenshots if they expose Cloudflare Account ID, Zone ID,
  tokens, private email addresses, or other private control-plane data.
- DNS records should be documented only at the policy/architecture level unless
  a future task explicitly requires a sanitized public record inventory.

## Registrar

IDHost remains the domain registrar.

Registrar notes:

- Keep registrar lock enabled unless a deliberate domain-transfer task requires
  temporarily disabling it.
- The EPP / transfer code is only for future domain transfer operations and
  must not be published in this repository.
- Registrar credentials, billing details, private phone numbers, and private
  addresses must stay outside the repository.

## Shared Hosting

Any IDHost shared hosting plan should be treated as sandbox, learning, or
backup infrastructure only.

It is not the production core for IKurabayev.kz while Cloudflare Pages remains
the selected public host. Do not migrate the production QR/profile website to
shared virtual hosting unless a future decision and pull request explicitly
justify that change.

Acceptable sandbox uses may include:

- learning basic hosting administration;
- testing small private experiments that do not contain secrets or private
  research data;
- keeping a temporary backup landing page outside the production path.

## Future Home Mini PC

A future home mini PC may be useful for lab and private infrastructure, but it
must remain separate from the public production website.

Potential uses:

- Docker-based lab services;
- research data ingestion and local processing;
- private visualization dashboards;
- private storage for family files;
- local backup targets;
- Cloudflare Tunnel, VPN, or similar private access patterns after separate
  security review.

The home mini PC should not become the directly exposed production host for the
public QR/profile website. Avoid direct public exposure of home services unless
a future security review, threat model, and explicit owner approval support it.

## Separation of Concerns

Keep these areas separate:

- Public website: static QR/profile/portfolio site hosted on Cloudflare Pages.
- Research and lab services: private or restricted infrastructure for data
  ingestion, experiments, dashboards, and tooling.
- Family/private storage: personal media, documents, backups, and household
  files.

Do not mix private storage, unpublished research data, or lab credentials into
the public website repository. The website can describe public-safe research
themes, but it must not store raw research datasets, private dashboards, family
photos/videos, or confidential infrastructure details.

## Security Boundaries

Do not commit:

- Cloudflare Account ID or Zone ID;
- API tokens, deployment tokens, passwords, SSH keys, or `.env` files;
- DNS screenshots containing private provider metadata;
- EPP / domain-transfer codes;
- private phone numbers, private email addresses, or private addresses;
- registrar billing details;
- raw or unpublished research data;
- family photos, videos, documents, or storage inventories;
- private service URLs, VPN credentials, tunnel tokens, or private IP plans.

Public documentation should remain architectural and reviewable. If a future
task needs operational details, create a sanitized runbook that excludes
secrets and private identifiers.

The public professional mailbox shown on the site is explicitly approved and
intentionally public. This approval does not extend to private or personal
email, phone numbers, addresses, or other private contact data.

## Current Edge Policy

- Cloudflare Web Analytics is intentionally disabled, and automatic analytics
  or beacon injection is not part of the approved production architecture.
- Analytics, tracking, and beacons remain prohibited.
- Cloudflare Email Address Obfuscation is intentionally enabled only as
  anti-harvesting edge protection for the approved public professional mailbox;
  it does not make the mailbox private.
- `site/_headers` remains the repository source of truth for security headers,
  and production QA verified an exact match for the current release.

## Future Design Workflow

Major visual changes should follow `docs/16_VISUAL_DESIGN_SYSTEM.md`. Claude
Design is the visual source of truth for approved major visual changes; Codex
ports the design faithfully, sanitizes incompatible export code, and documents
any required deviations.

Future design intake should check:

- privacy boundaries and absence of private contact details;
- factual claim boundaries;
- accessibility and readable contrast;
- mobile and desktop responsiveness;
- repository-managed public site code has no external runtime dependencies,
  analytics, cookies, tracking, or beacons;
- consistency with the Russian-first route priority and multilingual strategy.

Visual design ports remain separate from production infrastructure decisions
unless a future task explicitly combines those scopes.

## Next Safe Tasks

`docs/05_ACTIVE_TASKS.md` is the authoritative ordered maintenance queue.

The infrastructure-specific pending decision is the `www` versus apex redirect
policy. Real-AI/backend architecture remains a separate future architecture
phase.
