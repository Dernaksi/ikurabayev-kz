# Active Tasks

## Current Phase

Public AI assistant Gate D1 fail-closed readiness; Claude Design v1.1 remains
the visual baseline and the visible production concierge remains a local-only
prototype.

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
- Public Research Knowledge System v0.2 established a compact relationship
  graph, four bounded Evidence Spine additions, deterministic RU/EN public CV
  documents, block-level provenance, and an offline knowledge validator with
  nine bounded mutation checks. The Markdown outputs remain review artifacts.
- PR #45 recorded the owner-approved certified-energy-auditor status and
  2026-08-14 to 2029-08-06 term in the Evidence Spine and deterministic RU/EN
  public CV drafts while retaining the partially verified evidence status.
- PR #46 reconciled the same bounded certification status and term across the
  localized site and local concierge without publishing private credential
  details.
- PR #50 completed the RU/EN Living Public CV publication-readiness audit and
  corrected the bounded award mapping and Russian provenance terminology.
- PR #52 published the reviewed CV as deterministic, dependency-free RU/EN HTML
  at `/cv/` and `/en/cv/`, retained Markdown as review artifacts, and deferred
  PDF export.
- Issue #53 scopes a bounded Kazakh language pass. Clear interface,
  terminology, and copy defects are corrected, and owner review canonicalizes
  the exact full name `Қорабаев Ескендір Қазбекұлы` without rewriting
  source-specific abbreviated author strings.
- PR #54 merged that language and identity review. Production QA on 2026-08-23
  confirmed the exact Kazakh name, reviewed language markers, RU/EN CV review
  date, and privacy boundary on the apex, `www`, and Cloudflare Pages preview.
- PR #56 publishes two reproducible static PDF CV exports, localized download
  links, separate font/output provenance, and rendered-page QA without changing
  the deployed runtime architecture.
- PR #58 accepts the bounded public AI architecture, machine-readable evidence
  and refusal contract, and offline readiness validator without enabling an
  endpoint or provider call.
- PR #60 implements Gate B as a disabled providerless Pages Function with a
  deterministic server-side grounding bundle and offline failure-path tests.
- PR #62 implements and accepts Gate C as an authenticated Preview-only OpenAI
  provider pilot while keeping Production and the visible concierge fail-closed.
- PR #64 selects Luna for the private pilot after the bounded Terra/Luna
  comparison; Issue #63 is closed and Terra remains a controlled fallback.
- Production QA on 2026-08-22 confirmed the update on the apex, `www`, and
  Cloudflare Pages preview hosts across desktop and 390x844 mobile checks;
  canonical metadata, robots, sitemap, and the privacy boundary remained intact.

## Current Design Note

Earlier design-polish and Claude-like redesign attempts in PR #27 / #28 are
not treated as the visual baseline for v1.0. PR #29 is the accepted visual
direction for v1.0. PR #31 is the current accepted v1.1 production visual
baseline. Future major visual changes should start in Claude Design, then move
through a faithful Codex port with public-site sanitization only.

Production-domain QA for the v1.1 baseline is complete. Repeat it after future
visual or infrastructure changes rather than treating it as an active task for
the current release.

## Active Work

- Issue #65 prepares Gate D1 code readiness without activation. The production
  runner must require the exact kill-switch, production branch/origin, Luna,
  server-side key, and Cloudflare limiter, and must fail closed if any control
  is absent. Production provider traffic and UI networking remain disabled.

## Next Recommended Tasks

The university-role start-date discrepancy is not an active task. Retain the
employer-source canonical value and keep the start date omitted from generated
CVs until the external Astana-Energy profile is corrected and rechecked.

1. Decide the long-term semantic roles of the duplicated `/` and `/ru/` profile
   routes without changing the accepted Russian-first information architecture
   implicitly.
2. Decide whether to implement an optional `www`-to-apex redirect in the
   Cloudflare control plane; repository canonical metadata already uses apex.
3. Review the Issue #65 Gate D1 readiness PR. Keep public activation
   unauthorized until the separate OpenAI production project, spend controls,
   Cloudflare limiter, moderation decision, full QA, and owner approval are
   complete.

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
