# Active Tasks

## Current Phase

Claude Design-inspired AI-era redesign v0.9 for the static site.

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
- PR #26: Document production domain and infrastructure strategy.
- Domain activation and Cloudflare DNS verification for `ikurabayev.kz`.

## Next Recommended Tasks

1. Review the v0.9 AI-era redesign PR after local and PR checks.
2. Review and approve the public contact route before launch.
3. Finalize SEO / metadata after Russian-first route priority is accepted.
4. Decide and configure the `www` to apex redirect policy, or document why both
   hostnames should remain directly served.
5. Verify patent registry details before publishing final patent claims.
6. Complete Kazakh language review.
7. Create and review a sanitized public CV before any downloadable CV is added.
8. Review future Claude Design pages in a separate design-intake PR.
9. Perform final mobile and desktop launch review on the production domain.

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
