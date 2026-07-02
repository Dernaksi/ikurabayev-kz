# Blitz Plan Reconciliation v0.1

Status: Accepted planning note for human review.

## Purpose

This note reconciles a later blitz-launch plan with the current repository
state. The blitz plan was useful for launch sequencing, but it assumed an
earlier empty-repository state.

## Context

- PR #14 already added `docs/10_WEBSITE_INFORMATION_ARCHITECTURE.md`.
- PR #15 already added a dependency-free static HTML skeleton under `site/`.
- The current repository path is therefore no longer a framework-selection
  blank slate.

## Reconciled Decision

Continue with the current dependency-free static HTML path for first Cloudflare
Pages readiness.

Do not adopt Astro now. Astro remains a future option only, useful later if
site complexity or multilingual HTML duplication becomes painful enough to
justify a framework migration.

## Route Decision

QR codes for business cards, slides, and direct professional sharing should
target `ikurabayev.kz/qr` directly.

Because `/qr` is the practical QR-code target, `/` can remain a neutral gateway
for language selection and broad public orientation. The gateway route does not
block QR usage.

## What This PR Does Not Do

This reconciliation does not:

- Modify `site/` implementation files.
- Add `package.json`, lockfiles, dependencies, Astro, Vite, or framework
  scaffolding.
- Add generated build output.
- Add analytics, cookies, tracking, contact forms, redirects, secrets, tokens,
  private data, or private contact details.
- Add unsupported public claims, fabricated metrics, or unpublished research
  data.
- Verify ORCID, Scopus, publication, patent, project, or contact links.
- Prepare Cloudflare Pages deployment configuration.

## Follow-up Tasks

1. Completed by PR #17: verified QR links and Russian QR copy.
2. Completed by PR #18: Cloudflare Pages readiness for the existing `site/`
   directory.
3. Review and approve the public contact route before launch.
4. Verify publication metadata before publishing final publication claims.
5. Verify patent registry details before publishing final patent claims.
6. Complete production custom domain activation and DNS verification.

## Privacy and Reproducibility Boundaries

Keep private identifiers, private contact details, secrets, tokens, `.env`
files, unsupported claims, fabricated metrics, unpublished research data,
analytics, cookies, and tracking out of the repository and website.

Any public claim that depends on private evidence must remain conservatively
phrased and subject to human review before publication.

## Remaining Risks

- `docs/10_WEBSITE_INFORMATION_ARCHITECTURE.md` remains a historical
  pre-implementation IA document.
- Public contact route remains pending approval.
- Publication metadata remains pending verification.
- Patent registry details remain pending verification.
- Production custom domain activation remains pending.
