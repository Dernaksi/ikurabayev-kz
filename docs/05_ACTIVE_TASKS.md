# Active Tasks

## Current Phase

Phase 0/1 transition — AI Lab foundation complete, public content inventory next.

## Recently Completed

- PR #1: Establish AI Lab foundation.
- PR #2: Codex publish-flow smoke test, closed without merge.

## Next Recommended Tasks

1. Create public content inventory skeleton.
2. Define QR landing page information architecture.
3. Decide static HTML vs Astro only after content structure is clear.
4. Prepare Cloudflare Pages deployment notes after first website skeleton.

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
