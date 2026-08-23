# Visual Design System

Status: accepted/current workflow, documented through PR #30 and validated by
the merged PR #31 v1.1 production port.

## Purpose

This document defines how major visual changes for IKurabayev.kz should move
from Claude Design into the dependency-free static site.

The goal is not to make Codex invent a competing design system. The goal is to
preserve the approved visual direction, remove incompatible implementation
details, and keep the public site safe, accessible, static, and reviewable.

## Source Of Truth And Roles

Claude Design is the visual source of truth for major visual changes.
Claude Design v1.1 from PR #31 is the current production visual baseline.

Codex role:

- faithful porter;
- sanitizer of exported code and assets;
- accessibility checker;
- privacy and security checker;
- engineering implementer for static HTML, CSS, local assets, and approved
  local progressive enhancement.

Codex must not creatively redesign the website unless the owner explicitly asks
for a redesign. If a Claude Design detail cannot be ported, Codex should explain
the exact reason: security, privacy, routing, accessibility, static-hosting
compatibility, or public-content policy.

ChatGPT role:

- architecture and workflow planning;
- prompt design;
- safety and public-content review;
- pull request review.

## Design Intake Workflow

Use this sequence for major visual updates:

```text
Claude Design export
-> Codex inspect-only review
-> owner / ChatGPT review
-> faithful port pull request
-> Cloudflare Pages preview
-> squash merge after approval
```

The inspect-only review should identify reusable visual ideas, layout
differences, incompatible runtime code, external dependencies, privacy risks,
content changes, and the smallest safe implementation plan.

## Preferred Export Package

When asking Codex to inspect a Claude Design direction, provide:

- project archive ZIP;
- standalone HTML export;
- key screenshots for the intended desktop and mobile states.

Do not commit the raw export package, screenshots, generated bundles, or design
archives unless a later task explicitly approves that repository addition.

## What May Be Ported

Codex may manually adapt or faithfully port approved visual design elements such
as:

- layout;
- spacing;
- visual rhythm;
- dark engineering palette;
- portrait station;
- command-center blocks;
- QR badge;
- signal-chain modules;
- field-flow modules;
- AI Lab modules;
- local visual assets that are safe, intentional, and repository-appropriate.

Porting must preserve the approved public content boundaries. Visual work must
not strengthen biography, publication, patent, product, service, role, or metric
claims.

## What Must Be Sanitized

Claude Design exports and other design exports must be reviewed and sanitized
before integration. Remove or replace:

- external fonts;
- CDN links;
- React, Babel, framework wrappers, and preview runtimes;
- generated support files;
- preview-only runtime code;
- external requests;
- forms and data-submission behavior;
- tracking, analytics, cookies, and beacons;
- private identifiers.

## Allowed Implementation

The current public site may use:

- static HTML;
- static CSS;
- local image and SVG assets;
- local vanilla JavaScript for animation, reveal behavior, and progressive
  enhancement;
- reduced-motion support;
- Cloudflare Pages static hosting.

Local JavaScript must not call external services, collect private data, submit
forms, store analytics, or imply that a real public AI service exists unless a
separate approved backend/API pull request implements that service.

## Forbidden Implementation

Do not add:

- `package.json`;
- dependency manifests or lockfiles;
- frameworks;
- bundlers;
- external scripts;
- external fonts;
- analytics;
- cookies;
- tracking;
- real AI API keys;
- direct OpenAI or other AI-provider calls from frontend code.

Repository-managed public site code must remain free of external runtime
dependencies. Analytics, tracking, and beacon requests remain prohibited, and
Cloudflare Web Analytics is intentionally disabled. Cloudflare Email Address
Obfuscation is the narrow approved edge transformation for the explicitly
approved public professional mailbox; it is not a repository runtime dependency
and does not authorize other external scripts or requests.

## AI Panel Rule

An AI console, AI concierge, IK Lab Console, or similar interface is a prototype,
static demo, or curated public-facts module unless a separate Cloudflare
Function or Worker API pull request is approved.

Any such panel must be labelled as prototype or public-facts-only. It must not
imply that a live AI assistant, paid service, production AI lab, or private-data
assistant is currently operating.

## Future AI Integration Boundary

Real AI functionality must be designed as a separate architecture phase.

Minimum boundary:

- backend or edge function;
- secrets stored outside GitHub;
- no API keys in frontend code;
- public-facts-only retrieval unless a future privacy review approves more;
- explicit content, logging, rate-limit, and abuse-prevention review.

Do not combine a real AI/API launch with a visual port unless the owner
explicitly approves that combined scope.

## Route Rules

Future visual ports must preserve these public routes unless a later decision
changes the information architecture:

- `/`
- `/qr`
- `/ru`
- `/en`
- `/kk`

The root and QR routes currently follow Russian-first public entry. English
remains the international profile layer. Kazakh remains supported and has
received a bounded language pass. Its exact owner-approved full name is
`Қорабаев Ескендір Қазбекұлы`; visual ports must preserve this spelling and
order unless the owner explicitly changes it.

## Privacy Boundaries

Do not add:

- private phone numbers;
- private addresses;
- private or personal email addresses;
- professional mailboxes not explicitly approved for public display;
- IIN or other private identity numbers;
- Cloudflare Account ID or Zone ID;
- EPP code;
- tokens, passwords, API keys, SSH keys, or `.env` values;
- raw or unpublished research data;
- family or private files.

The current public professional mailbox is explicitly approved for public
display. Cloudflare Email Address Obfuscation may protect it from basic
harvesting, but does not make it private or confidential.

If a design export includes private identifiers or contact details not
explicitly approved for public display, stop and report the issue before
porting that material.

## QA Checklist

Every faithful visual port should verify:

- all key routes: `/`, `/qr`, `/ru`, `/en`, `/kk`;
- viewport widths: 390, 430, 768, 1024, and 1440 px;
- no horizontal overflow;
- local assets resolve;
- CSP remains compatible with `site/_headers`;
- reduced-motion behavior exists for animation-heavy sections;
- repository-managed public site code has no external runtime dependencies and
  makes no analytics, tracking, or beacon requests;
- QR page remains mobile-first and fast to scan;
- AI panel does not imply a live AI service;
- privacy and public-content scans are clean except for policy-only references.

## Faithfulness Report

Future design PRs should include a short faithfulness report:

- source design package inspected;
- sections ported faithfully;
- deviations from Claude Design;
- exact reason for each deviation;
- sanitized items removed;
- accessibility and responsive checks;
- privacy and public-content review.
