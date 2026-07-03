# Active Tasks

## Current Phase

Faithful Claude Design port v1.0.

## Recently Completed

- PR #1: Establish AI Lab foundation.
- PR #2: Codex publish-flow smoke test, closed without merge.
- PR #9: Sanitized public content inventory.
- PR #11: Public biography draft.
- PR #13: QR landing page draft.
- PR #14: Website information architecture.
- PR #15: Static website skeleton.
- PR #16: Reconcile blitz plan with dependency-free static HTML path.
- PR #17: Add verified QR profile links and Russian QR copy.
- PR #18: Add Cloudflare Pages deployment readiness and `site/_headers`.
- PR #21: Add portrait and substantive profile content v0.3.
- PR #22: Add Neutral Shift Lab visual system v0.4.
- PR #23: Add public web evidence audit v0.5.
- PR #24: Integrate visual assets for Neutral Shift Lab v0.6.
- PR #25: Make Russian-first public experience v0.7.
- Domain activation and Cloudflare DNS verification for `ikurabayev.kz`.

## Current Design Note

Earlier design-polish and Claude-like redesign attempts in PR #27 / #28 are
not treated as the visual baseline for v1.0. The active task uses the supplied
Claude Design export as the source of truth, with public-site sanitization only.

## Next Recommended Tasks

1. Review PR for the faithful Claude Design port v1.0 and verify that the
   unavoidable deviations are limited to sanitization, routing, accessibility,
   and public-content policy.
2. Review and approve the public contact route before launch.
3. Finalize SEO / metadata after Russian-first route priority is accepted.
4. Decide and configure the `www` to apex redirect policy, or document why both
   hostnames should remain directly served.
5. Verify patent registry details before publishing final patent claims.
6. Complete Kazakh language review.
7. Create and review a sanitized public CV before any downloadable CV is added.
8. Perform final mobile and desktop launch review on the production domain.

## Active Branch Convention

- Start from `main`.
- Pull latest.
- Create a focused branch.
- Never work directly on `main`.

## Commands

```powershell
git switch main
git pull --ff-only
git switch -c codex/<task-name>
```

## Done Definition

- Branch pushed.
- PR opened.
- No direct `main` push.
- Working tree clean.
- Privacy boundary reviewed.
