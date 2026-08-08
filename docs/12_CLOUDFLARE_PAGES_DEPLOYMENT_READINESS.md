# Cloudflare Pages Deployment Readiness v0.1

Status: historical deployment-readiness record with current post-deployment
verification.

## Purpose

This document preserves the original v0.1 Cloudflare Pages deployment-readiness
path and records the current verified production baseline for the existing
dependency-free static site.

## Current Site State

The site is implemented as static HTML and CSS under `site/`.

Current routes:

- `/`
- `/en`
- `/ru`
- `/kk`
- `/qr`

The `/qr` route is the direct QR-code target for business cards, slides, and
professional sharing. The root route `/` is the Russian-first public entry.

The current production site has no `package.json`, dependency installation,
framework preset, build pipeline, server-side JavaScript runtime, contact form,
redirect layer, Worker, or Pages Function. It uses approved local vanilla
JavaScript for dependency-free progressive enhancement. Analytics, cookies,
tracking, and beacon requests are not part of the approved production
architecture. Cloudflare Email Address Obfuscation is the narrow approved edge
transformation for the approved public professional mailbox.

## Current / Post-Deployment Status

Cloudflare Pages preview is live:

- `https://ikurabayev-kz.pages.dev`
- `https://ikurabayev-kz.pages.dev/qr`

The Cloudflare Pages project is healthy. The production branch is `main`, and
`https://ikurabayev.kz` and `https://www.ikurabayev.kz` were verified active
with SSL. Claude Design v1.1 from PR #31 is the current production visual
baseline, and production-domain QA has been completed for this release.

## Cloudflare Pages Settings

Use the Cloudflare Pages GitHub integration.

- Production branch: `main`
- Framework preset: none
- Root directory: repository root
- Build command: blank, or `exit 0` only if the Cloudflare UI requires an
  explicit command
- Build output directory: `site`

Domain binding and DNS are configured in Cloudflare. Any future control-plane
changes should be made in the Cloudflare UI only. Do not store domain
credentials, API secrets, deployment tokens, or private configuration in this
repository.

## Original Pre-Deploy Checklist (Historical)

This checklist records the v0.1 readiness process before production activation.

- Confirm the deployment branch is `main`.
- Confirm the build output directory is `site`.
- Confirm the build command is blank, or `exit 0` only if required by the UI.
- Confirm no framework preset is selected.
- Confirm there are no dependency or package-manager files required for deploy.
- Confirm `site/_headers` is present in the published output.
- Confirm public content boundaries are still respected before launch.

## Post-Deploy Smoke Checklist

After deployment, check:

- `/` loads and links to language routes and `/qr`.
- `/en` loads.
- `/ru` loads.
- `/kk` loads.
- `/qr` loads and remains suitable as the QR-code target.
- `site/assets/styles.css` is served and applied.
- ORCID and Scopus links on `/qr` navigate normally.
- The approved public professional contact route remains available without
  exposing private contact data.
- Publication metadata and patent-registry details remain pending where
  applicable.
- Response headers include the security headers documented below.

## Security Headers

Production applies the headers in `site/_headers`; production QA verified an
exact match for the current release:

```text
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  X-Frame-Options: DENY
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'self'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; object-src 'none';
```

These headers are intentionally conservative for the current static site. The
headers themselves do not add redirects, HSTS, noindex rules, analytics,
cookies, tracking, contact forms, Workers, or Pages Functions.

The Content Security Policy limits resource loading for the static site. It
does not block normal top-level navigation from links such as ORCID and Scopus.

## Current Edge Configuration

- Cloudflare Web Analytics is intentionally disabled.
- Automatic analytics or beacon injection is not approved; analytics,
  tracking, and beacons remain prohibited.
- Cloudflare Email Address Obfuscation is intentionally enabled only as
  anti-harvesting edge protection for the approved public professional mailbox.
  It does not make the mailbox private.
- `site/_headers` remains the repository source of truth for production
  security headers.

## Domain / DNS Notes

The production domains and DNS records are already configured. Keep future DNS
and Pages binding changes in the Cloudflare UI unless an approved task requires
a sanitized documentation update.

## Privacy and Secret Boundaries

Do not store Cloudflare API secrets, deployment tokens, credentials, private
contact details, private identifiers, unpublished research data, raw evidence,
or private configuration in this repository.

## Rollback Notes

Rollback should use Cloudflare Pages deployment history or a Git revert PR. Do
not rewrite `main` history. If deployment configuration changes are needed,
record them in a small follow-up PR.

## Original v0.1 Readiness Scope (Historical)

The original readiness change did not add:

- Website content changes.
- Existing HTML or CSS edits.
- `package.json`.
- Dependencies.
- Framework files.
- GitHub Actions.
- JavaScript.
- Analytics, cookies, or tracking.
- Contact forms.
- Redirects.
- HSTS.
- `noindex` headers.
- Workers or Pages Functions.
- Secrets, tokens, or private data.

## Remaining Risks

- Publication metadata and patent-registry details remain subject to their
  respective verification tasks.
- Kazakh language review, SEO metadata, and a sanitized public CV remain
  pending.
- Production QA should be repeated after future visual, deployment, DNS, or
  relevant edge-configuration changes.
