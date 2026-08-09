# Active Tasks

## Current Phase

Post-v1.2 production maintenance; Claude Design v1.1 remains the visual baseline.

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
- PR #31: Port Claude Design refinement v1.1.
- Domain activation and Cloudflare DNS verification for `ikurabayev.kz`.
- Production-domain QA for v1.1, including active SSL on the apex and `www`
  domains and exact production-header verification against `site/_headers`.
- Owner production decision: Cloudflare Web Analytics disabled and Email
  Address Obfuscation retained for the approved public professional mailbox.
- Local AI concierge contact wording reconciled with the approved public
  professional contact route.
- AI concierge input given an explicit localized accessible name and prototype
  disclosure contrast brought into WCAG conformance.
- QR first-view portrait payload reduced by 87.70% without changing its source
  photograph, crop, dimensions, or aspect ratio.
- Public Evidence Spine v0.1 established for 21 bounded high-value facts, with
  the three displayed patent records verified through official EAPO and
  Qazpatent sources.
- Evidence-backed public release v1.2 reconciled dated patent legal status and
  official registry links, removed the prohibited energy-auditor document
  identifier, corrected stale concierge wording, established apex semantic
  metadata plus robots/sitemap, and added an offline release validator.

## Current Design Note

Earlier design-polish and Claude-like redesign attempts in PR #27 / #28 are
not treated as the visual baseline for v1.0. PR #29 is the accepted visual
direction for v1.0. PR #31 is the current accepted v1.1 production visual
baseline. Future major visual changes should start in Claude Design, then move
through a faithful Codex port with public-site sanitization only.

Production-domain QA for the v1.1 baseline is complete. Repeat it after future
visual or infrastructure changes rather than treating it as an active task for
the current release.

## Next Recommended Tasks

1. Resolve the conflicting official university-role start-date evidence through
   owner review before changing the production timeline.
2. Decide whether to implement an optional `www`-to-apex redirect in the
   Cloudflare control plane; repository canonical metadata already uses apex.
3. Complete Kazakh language review.
4. Create and review a sanitized public CV before any downloadable CV is added.
5. Draft a separate real-AI backend architecture before any real API work.

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
