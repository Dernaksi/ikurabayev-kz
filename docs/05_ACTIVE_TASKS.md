# Active Tasks

## Current Phase

Claude Design v1.1 faithful refinement.

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
- PR #29: Add faithful Claude Design port v1.0.
- PR #30: Document Claude Design faithful-port workflow.
- Domain activation and Cloudflare DNS verification for `ikurabayev.kz`.

## Current Design Note

Earlier design-polish and Claude-like redesign attempts in PR #27 / #28 are
not treated as the visual baseline for v1.0. PR #29 is the accepted visual
direction. Future major visual changes should start in Claude Design, then move
through a faithful Codex port with public-site sanitization only.

The active implementation task is a faithful Claude Design v1.1 refinement.
Sanitization is limited to security, privacy, accessibility, route cleanliness,
and Cloudflare Pages compatibility.

## Next Recommended Tasks

1. Perform production-domain visual QA after the Claude Design v1.1 refinement.
2. Review the public contact route and confirm the intended public email policy.
3. Finalize SEO / metadata after Russian-first route priority is accepted.
4. Decide and configure the `www` to apex redirect policy, or document why both
   hostnames should remain directly served.
5. Complete Kazakh language review.
6. Verify patent registry details before publishing final patent claims.
7. Create and review a sanitized public CV before any downloadable CV is added.
8. Draft an AI public assistant architecture document before any real API work.

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
