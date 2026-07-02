# Cloudflare Pages Deployment Readiness v0.1

Status: deployment-readiness note for human review.

## Purpose

This document records the smallest safe Cloudflare Pages deployment path for
the existing dependency-free static HTML site.

## Current Site State

The site is implemented as static HTML and CSS under `site/`.

Current routes:

- `/`
- `/en`
- `/ru`
- `/kk`
- `/qr`

The `/qr` route is the direct QR-code target for business cards, slides, and
professional sharing. The root route `/` remains a neutral gateway.

There is no `package.json`, dependency installation, framework preset, build
pipeline, JavaScript runtime, analytics, cookies, tracking, contact form,
redirect layer, Worker, or Pages Function in the current deployment path.

## Cloudflare Pages Settings

Use the Cloudflare Pages GitHub integration.

- Production branch: `main`
- Framework preset: none
- Root directory: repository root
- Build command: blank, or `exit 0` only if the Cloudflare UI requires an
  explicit command
- Build output directory: `site`

Domain binding and DNS should be configured in the Cloudflare UI only. Do not
store domain credentials, API secrets, deployment tokens, or private
configuration in this repository.

## Pre-Deploy Checklist

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
- Contact route, publications, and patents remain pending where applicable.
- Response headers include the security headers documented below.

## Security Headers

Cloudflare Pages should apply the headers in `site/_headers`:

```text
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  X-Frame-Options: DENY
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'self'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; object-src 'none';
```

These headers are intentionally conservative for the current static site. They
do not add redirects, HSTS, noindex rules, analytics, cookies, tracking,
scripts, contact forms, Workers, or Pages Functions.

The Content Security Policy limits resource loading for the static site. It
does not block normal top-level navigation from links such as ORCID and Scopus.

## Domain / DNS Notes

Configure the production domain and DNS records in the Cloudflare UI. Keep DNS
and Pages binding changes outside the repository unless a future approved task
requires documentation updates.

## Privacy and Secret Boundaries

Do not store Cloudflare API secrets, deployment tokens, credentials, private
contact details, private identifiers, unpublished research data, raw evidence,
or private configuration in this repository.

## Rollback Notes

Rollback should use Cloudflare Pages deployment history or a Git revert PR. Do
not rewrite `main` history. If deployment configuration changes are needed,
record them in a small follow-up PR.

## Out Of Scope

This readiness step does not add:

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

- `README.md` still contains stale pre-implementation wording and should be
  cleaned up in a later documentation PR.
- Contact route, publication metadata, and patent registry details remain
  pending review.
- Cloudflare UI settings and domain binding must be verified manually after the
  Pages project is configured.
