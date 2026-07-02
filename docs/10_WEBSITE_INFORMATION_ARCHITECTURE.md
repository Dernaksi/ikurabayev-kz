# Website Information Architecture v0.1

Status: planning draft for human review.

## Current Status Note

This is a historical v0.1 planning document created before implementation. A
dependency-free static implementation and Cloudflare Pages deployment readiness
now exist in later PRs. Older "pending" wording in this document should be read
in that historical context unless superseded by later documents or merged PRs.
The privacy, provenance, and conservative publication boundaries remain active.

The v0.2 site expands the placeholder static skeleton into a fuller public
profile and QR landing experience while preserving the same route model:
`/`, `/en`, `/ru`, `/kk`, and `/qr`. The technical path remains static HTML and
CSS without framework or dependency migration.

The v0.7 route priority makes the public entry experience Russian-first:
`/` and `/qr` lead in Russian, `/ru` is the primary detailed profile, `/en` is
the international research profile, and `/kk` remains a conservative supported
route pending language review. This supersedes older English-first
language-priority wording in this planning document without changing the
privacy and evidence boundaries.

## Purpose

This document defines the information architecture for IKurabayev.kz before any
website implementation. It describes the trust model, route model, content
structure, multilingual strategy, privacy boundaries, and publication-readiness
rules that should guide a future static website.

This is not a design system, frontend implementation, framework decision, or
deployment plan.

## Source Documents

The current approved source base is:

- `START_HERE.md`
- `AGENTS.md`
- `README.md`
- `docs/00_PROJECT_CONTEXT.md`
- `docs/01_AI_LAB_WORKFLOW.md`
- `docs/02_DECISION_LOG.md`
- `docs/03_ROADMAP.md`
- `docs/04_PUBLIC_CONTENT_POLICY.md`
- `docs/05_ACTIVE_TASKS.md`
- `docs/06_PUBLIC_CONTENT_INVENTORY.md`
- `docs/07_PUBLIC_SOURCE_AUDIT_AND_POSITIONING.md`
- `docs/08_PUBLIC_BIOGRAPHY_DRAFT.md`
- `docs/09_QR_LANDING_PAGE_DRAFT.md`

Publication, patent, project, and contact details remain subject to human review
and public metadata verification before launch.

## Site Principles

- Credibility before decoration.
- QR-first access for real-world meetings, business cards, and professional
  introductions.
- Multilingual by design, with Russian as the primary public entry language and
  English as the international research profile.
- Privacy-safe publication and conservative contact routing.
- Evidence-first claims: unsupported claims remain pending, not final.
- Simple static-site readiness without choosing a framework yet.
- No language auto-detection, cookies, analytics, or redirects in v0.1.
- No private identifiers, exact private contact details, raw evidence scans, or
  unpublished research data.

## Audience Model

The site should serve several distinct visitor types without fragmenting the
public identity:

- QR/business-card visitors who need a fast, trustworthy first contact point.
- Research collaborators and reviewers who need academic context, research
  themes, and public identifiers.
- Engineering collaborators who need applied technical orientation and portfolio
  signals.
- Energy-efficiency and energy-audit contacts who need a conservative public
  professional profile.
- AI Lab and future maintainers who need provenance, boundaries, and a stable
  content model.

## Top-Level Route Model

The v0.1 route model should be explicit:

- `/`
- `/en`
- `/ru`
- `/kk`
- `/qr`

The first version should not assume automatic language detection, cookies,
analytics, redirects, or visitor tracking. Route behavior should be predictable
and reviewable.

## Route Definitions

### `/`

Purpose:
Provide a Russian-first gateway into the public identity and language
structure.

Expected content:

- Russian identity line and public trajectory.
- Route selector for Russian profile, QR card, English international profile,
  and Kazakh.
- Link to the stable QR landing route.
- Navigation to research/profile/projects/contact sections.
- No private contact details.

Privacy risks:

- Do not expose private contact routes.
- Do not present unverified publication, patent, role, or project claims as
  final.

### `/en`

Purpose:
Serve as the international / academic public profile page.

Expected structure:

- Profile.
- Research.
- Projects / Engineering Portfolio.
- Publications and Patents.
- Contact.

Content rules:

- English remains available for international research and academic readers.
- Final claims must be supported by approved public-safe source material.
- Pending publication, patent, contact, and project details must remain marked
  as pending.

### `/ru`

Purpose:
Serve as the primary detailed public profile page.

Content rules:

- Use the same conservative factual boundaries as `/en`.
- Russian text requires owner tone review before launch.
- No Russian claim may be stronger than the approved public source base.
- Pending items remain pending in Russian.

### `/kk`

Purpose:
Serve as the Kazakh localized public profile page with parity to `/en`.

Content rules:

- Use the same structure as `/en`.
- Kazakh text requires human review before launch.
- No Kazakh claim may be stronger than the approved English source.
- Pending items remain pending in Kazakh.

### `/qr`

Purpose:
Provide the stable QR landing route for business cards, events, professional
sharing, and direct introductions.

Expected content:

- Display name.
- Russian one-line positioning.
- Short English note that the international profile is available in English.
- Three primary actions:
  1. Research profile.
  2. Engineering portfolio.
  3. Contact route pending approval.
- Secondary links:
  - ORCID pending exact link review.
  - Publications pending metadata verification.
  - Patents pending registry verification.

Privacy risks:

- Do not add phone numbers, private email, messenger links, private addresses,
  personal identifiers, or document-derived metadata.
- Keep the contact route pending until explicitly approved.

## Core Page Sections

### Profile

Purpose:
Establish a concise public professional identity.

Allowed content:

- Public-safe name and positioning.
- Electrical engineering and energy-efficiency orientation.
- Kazakhstan context.
- Academic background when phrased conservatively.

Pending content:

- Exact role names and dates pending reconciliation.
- Public contact route pending approval.
- Public academic identifier URL pending exact link review.

Privacy risks:

- Private identifiers, private contact details, document numbers, raw scans, and
  unsupported role claims.

### Research

Purpose:
Show academic credibility and research direction without overstating
publication status.

Allowed content:

- Insulation parameters.
- Ungrounded and isolated-neutral AC systems.
- Earth-fault current.
- Admittance.
- Conductance.
- Susceptance.
- Voltage diagnostics.
- Electrical power systems.
- Mining facilities.
- Measurement and diagnostic methods.

Pending content:

- Publication pages pending DOI, publisher, or public metadata verification.
- Patent references pending public patent-registry verification.

Privacy risks:

- Unpublished research data.
- Confidential manuscripts or datasets.
- Claims that imply final publication, patent, or method validation status
  before verification.

### Projects / Engineering Portfolio

Purpose:
Represent applied engineering depth without exposing private client, employer,
or unpublished project details.

Allowed content:

- High-level engineering portfolio.
- Energy-efficiency and energy-audit work.
- Electrical measurement and diagnostics.
- AI-assisted engineering laboratory.

Pending content:

- STM32 / measurement laboratory pending public-content review.
- AI Energy Auditor pending public-content review.
- Specific project entries pending source and privacy review.

Privacy risks:

- Client names, contracts, financial data, internal documents, private facility
  details, and unpublished technical data.

### Publications and Patents

Purpose:
Provide a future home for verified academic and patent metadata.

Allowed content:

- Placeholder status explaining that publication metadata must be verified.
- Placeholder status explaining that patent metadata must be verified through
  public registries.
- ORCID as a possible academic identifier after exact link review.

Pending content:

- Publication titles, DOI links, publisher pages, and citation metadata.
- Patent titles, registry links, and jurisdiction details.

Privacy risks:

- Final publication or patent claims before verification.
- Non-public document details copied from private evidence.

### Contact

Purpose:
Provide a privacy-safe route for professional contact after approval.

Allowed content:

- A statement that the public contact route is pending approval.
- Future public contact destination after explicit review.

Pending content:

- Exact public contact route.
- Whether contact should be email-based, profile-based, form-based, or routed
  through another approved public channel.

Privacy risks:

- Private phone numbers.
- Private email addresses.
- Messenger links.
- Private addresses.
- Personal identifiers.

## Research/Profile/Projects/Contact Content Model

The content model should use only conservative public-safe concepts from
`docs/06_PUBLIC_CONTENT_INVENTORY.md`,
`docs/08_PUBLIC_BIOGRAPHY_DRAFT.md`, and
`docs/09_QR_LANDING_PAGE_DRAFT.md`.

Research themes:

- Insulation parameters.
- Ungrounded and isolated-neutral AC systems.
- Earth-fault current.
- Admittance.
- Conductance.
- Susceptance.
- Voltage diagnostics.
- Electrical power systems.
- Mining facilities.
- Measurement and diagnostic methods.

Profile concepts:

- Electrical engineering.
- Energy efficiency.
- Kazakhstan.
- Academic background in industrial power supply, electrical power engineering,
  and electrical complexes and systems.
- Public biography wording pending human review.

Project concepts:

- Engineering portfolio.
- Energy-efficiency and energy-audit work.
- Electrical measurement and diagnostics.
- AI-assisted engineering laboratory.
- STM32 / measurement laboratory, pending public-content review.
- AI Energy Auditor, pending public-content review.

Contact concepts:

- Contact route pending approval.
- No private contact details until explicitly approved.
- QR route safe for broad professional sharing.

## Multilingual Strategy

- Russian is the primary public entry language for the first launch.
- English is the international research profile, not the default local route.
- Russian, English, and Kazakh routes share the same approved public source
  base; no language may introduce stronger claims than the approved source
  material.
- If a translation is not reviewed, mark it as pending human review.
- Maintain route parity across `/en`, `/ru`, and `/kk`.
- A language switch should preserve section intent conceptually, but this
  document does not define implementation details.

## Privacy and Publication Boundaries

Do not publish or store website-facing copies of:

- IIN or other civil identifiers.
- Private phone numbers.
- Private email addresses.
- Private addresses.
- Date of birth.
- Passport data.
- Identity-card data.
- Document numbers.
- Raw scans.
- Signatures, seals, QR/EDS blocks.
- Labor-book data.
- Contracts or financial records.
- Documents or personal data about other people.
- Unpublished research data.
- Confidential manuscripts or datasets.

If a useful public claim depends on private evidence, publish only a
conservative public-safe wording after human approval. Do not copy the private
source into the repository.

## Content Status Model

Use explicit status labels for future content:

- Approved public-safe draft: usable as draft website source after human review.
- Pending human review: plausible but not launch-ready.
- Pending public metadata verification: requires DOI, publisher, registry, or
  other public source confirmation.
- Excluded/private: must not be published or copied into the website.
- Future idea, not publication-ready: may guide planning but must not appear as
  a public claim.

## What We Do Not Implement Yet

This task does not implement:

- Website files.
- Framework decision.
- Astro, Next, Vue, React, or any other framework choice.
- `package.json`.
- Dependencies.
- CSS or design system.
- Deployment.
- Cloudflare Pages setup.
- Analytics.
- Contact form.
- Downloadable CV.
- Document scans.
- Exact ORCID URL until reviewed.
- Publication or patent pages until verified.
- Private contact route.

## Future Implementation Notes

This IA should make a future static-site implementation easier without choosing
the stack. A later implementation should stay simple, static, multilingual, and
privacy-preserving. It should keep content source files reviewable, preserve
route parity, and make pending content visibly distinct from launch-ready
content.

Any future technical decision should be recorded separately and should not
weaken the publication, provenance, or privacy boundaries defined here.

## Review Checklist

- [ ] No private identifiers.
- [ ] No private contact details.
- [ ] No unsupported claims.
- [ ] No unverified publication or patent final claims.
- [ ] Multilingual consistency reviewed.
- [ ] QR route safe for public sharing.
- [ ] Implementation-free.
- [ ] Human approval required before launch.

## Open Questions

- What public contact route is approved?
- What exact ORCID URL is approved for publication?
- What source should verify publication metadata?
- What source should verify patent registry metadata?
- Which project entries are public-safe?
- Should `/qr` later have language-specific variants such as `/qr/en`,
  `/qr/ru`, and `/qr/kk`?
