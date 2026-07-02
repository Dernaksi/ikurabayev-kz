# Active Tasks

## Current Phase

Substantive public profile content v0.3 and portrait integration.

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

1. Review and approve the public contact route before launch.
2. Domain activation and DNS verification after `ikurabayev.kz` becomes active.
3. Continue public-source audit for publication metadata.
4. Verify patent registry details before publishing final patent claims.
5. Complete Kazakh language review.
6. Add downloadable public CV later only after a sanitized CV is created.

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
