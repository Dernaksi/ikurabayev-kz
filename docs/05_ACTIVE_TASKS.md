# Active Tasks

## Current Phase

Public web evidence audit and source-backed profile layer v0.5.

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

## Next Recommended Tasks

1. Review and approve the public contact route before launch.
2. Domain activation and DNS verification after `ikurabayev.kz` becomes active.
3. Verify patent registry details before publishing final patent claims.
4. Complete Kazakh language review.
5. Create and review a sanitized public CV before any downloadable CV is added.
6. Optional SEO / metadata PR after the public evidence audit is reviewed.
7. Review the Neutral Shift Lab visual system on mobile and desktop preview.

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
