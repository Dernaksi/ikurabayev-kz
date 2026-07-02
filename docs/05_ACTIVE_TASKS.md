# Active Tasks

## Current Phase

Static site deployment readiness after PR #14 and PR #15.

## Recently Completed

- PR #1: Establish AI Lab foundation.
- PR #2: Codex publish-flow smoke test, closed without merge.
- PR #9: Sanitized public content inventory.
- PR #11: Public biography draft.
- PR #13: QR landing page draft.
- PR #14: Website information architecture.
- PR #15: Static website skeleton.

## Next Recommended Tasks

1. Reconcile blitz plan with current static HTML path.
2. Add verified QR links and Russian QR copy in a small content PR.
3. Prepare Cloudflare Pages readiness for existing `site/`.
4. Review public contact route before launch.
5. Clean up stale README/status wording in a later documentation PR.

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
