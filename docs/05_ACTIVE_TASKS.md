# Active Tasks

## Current Phase

Full public profile site v0.2 after Cloudflare Pages preview became available.

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

## Next Recommended Tasks

1. Domain activation and DNS verification after `ikurabayev.kz` becomes active.
2. Photo upload and public-use review for `site/assets/iskander-portrait.jpg`.
3. Review and approve the public contact route before launch.
4. Verify publication metadata before publishing final publication claims.
5. Verify patent registry details before publishing final patent claims.
6. Complete Kazakh language review.
7. Later visual refinements if review finds usability or tone issues.

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
