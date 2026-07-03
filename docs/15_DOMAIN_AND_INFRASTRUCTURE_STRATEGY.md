# Domain and Infrastructure Strategy

Status: planning and operations note for human review.

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
- `https://www.ikurabayev.kz` is also reported by the owner as working.

This document does not claim final public-launch completion. Public contact
routing, SEO metadata, Kazakh language review, patent-registry verification,
and final launch review remain pending.

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

## Future Design Workflow

The owner is separately improving page design through Claude Design. Those
outputs may be reviewed later, but they should be integrated only through a
separate design-intake pull request after owner approval.

Future design intake should check:

- privacy boundaries and absence of private contact details;
- factual claim boundaries;
- accessibility and readable contrast;
- mobile and desktop responsiveness;
- no external scripts, analytics, cookies, or unapproved dependencies;
- consistency with the Russian-first route priority and multilingual strategy.

This infrastructure task intentionally does not redesign or integrate Claude
Design pages.

## Next Safe Tasks

Recommended next tasks:

1. Review and approve the public contact route.
2. Finalize SEO metadata after Russian-first route priority is accepted.
3. Decide and configure whether `www` should redirect to apex, apex should
   redirect to `www`, or both should remain directly served.
4. Complete Kazakh language review.
5. Verify patent registry details before strengthening patent wording.
6. Create and review a sanitized public CV before adding any downloadable CV.
7. Perform final mobile and desktop launch review on the production domain.
8. Review future Claude Design pages in a separate design-intake PR.
