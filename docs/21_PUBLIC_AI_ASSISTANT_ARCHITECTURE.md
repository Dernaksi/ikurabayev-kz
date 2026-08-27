# Public AI Assistant Architecture

Status: Gate A accepted in PR #58; disabled Gate B proposed under issue #59

Reviewed: 2026-08-26

## Purpose

This document defines the smallest safe architecture for turning the existing
local public-facts-only concierge into a real AI assistant. Gate A is accepted.
Gate B adds only a fail-closed backend skeleton, not a live AI launch.

The first live version should answer short questions about Iskander Kurabayev's
reviewed public profile, research, publications, patents, credentials, and
roadmap projects. It must refuse requests that need private, unpublished,
unsupported, or out-of-scope information.

The machine-readable source of truth for this boundary is
`data/public-ai-contract.json`. The offline validator is
`tools/check_public_ai.py`.

## Decision Summary

The proposed v0 assistant uses:

- the existing static concierge as the user interface;
- a same-origin `POST /api/ai/ask` endpoint implemented as a Cloudflare Pages
  Function and kept providerless during Gate B;
- the OpenAI Responses API from the server side only;
- a Cloudflare secret binding for the provider credential;
- one request and one answer over HTTP, with `store: false`;
- no model tools, web search, uploads, persistent memory, response chaining,
  background jobs, analytics, or content logging;
- deterministic grounding from the reviewed Evidence Spine and public research
  graph;
- structured answers with claim/source citations or a categorized refusal.

No model is fixed at the architecture stage. Candidate models must be compared
with the checked-in evaluation cases for grounded-answer success, refusal
success, latency, token use, and cost per successful answer.

## Current Gate B Implementation

The Gate B implementation is deliberately useful but inert:

- `site/_routes.json` sends only `/api/ai/ask` to Pages Functions;
- `functions/api/ai/ask.js` validates method, same origin, media type, exact
  fields, language, session form, size, control characters, and URL retrieval;
- every otherwise valid RU/EN request returns a localized structured 503 with
  `service_unavailable`; there is no provider branch or outbound fetch;
- `tools/build_public_ai_grounding.py` deterministically selects only the
  contract allowlists and writes a server-side module plus byte-level
  provenance;
- `tools/check_public_ai.py` verifies the route, handler safety markers, source
  and output hashes, counts, privacy boundary, and byte-identical regeneration;
- `tools/test_public_ai_backend.mjs` exercises request rejection and fail-closed
  behavior with Node built-ins only.

The current bundle contains 25 claims, 39 relations, 15 sources, and 8 topics.
These counts describe reviewed grounding records, not model performance or a
live service. The browser does not load the bundle.

## System Boundary

```text
Visitor browser
  |
  | POST /api/ai/ask (same origin, <= 600 characters)
  v
Cloudflare edge boundary
  |- validate language, size, origin, and rate limit
  |- select only allowlisted public claim/relation records
  |- keep prompts and answers out of logs
  |
  | server-side Responses API request
  | store=false, no tools, no files, no web search
  v
OpenAI Responses API
  |
  | structured answer or refusal
  v
Edge verifier
  |- reject unknown claim/source IDs
  |- reject answers without citations
  |- apply length and status-language rules
  v
Existing concierge UI
```

The browser never receives or sends an OpenAI API key. It also never loads the
raw Evidence Spine or research graph at runtime. A future backend build must
create a minimal deterministic grounding bundle from the allowlisted IDs and
record its source hashes. That derived bundle remains server-side.

## Trust Boundaries

### Public repository

The repository may contain the architecture, policy, allowlists, tests, public
claim IDs, public relation IDs, and deterministic build tooling. It must not
contain provider credentials, Cloudflare account identifiers, private control
plane exports, raw evidence, or request/response logs.

### Browser

User input is untrusted. The browser may submit only the question, requested
language, and an ephemeral random page-session identifier. It must not submit
cookies, contact details, browsing history, local files, or stored conversation
history. The page-session identifier is hashed before use as a provider safety
identifier and is not persisted.

### Edge backend

The backend is the only component allowed to call the model provider. It must:

- enforce same-origin HTTPS requests and explicit request/response limits;
- apply an edge rate limit before public enablement;
- map questions to allowlisted public records only;
- keep request and response content out of logs;
- send `store: false` and an empty tools list;
- validate the structured model output before returning it;
- fail closed when grounding, output validation, or provider access fails.

### Model provider

The provider receives only the bounded question, public grounding needed for
that question, response schema, refusal policy, and privacy-preserving safety
identifier. It receives no private evidence, raw documents, uploads, contact
details, certificate identifiers, analytics identifiers, or persistent user
profile.

## Grounding Rules

The assistant may use only claim IDs and relation IDs listed in
`data/public-ai-contract.json`. Allowlisting is explicit so a newly added public
fact does not automatically become AI-visible.

Returned citations must be a subset of the grounding records selected for that
specific request. Each returned source ID must also belong to the cited claim's
recorded `evidence` array. A generally allowlisted but non-selected claim cannot
be used as a citation shortcut.

Every allowed claim must:

- exist in `data/public-facts.json`;
- have `public: true`;
- use one of `verified_public`, `partially_verified`, `owner_approved`, or
  `roadmap_only`;
- reference at least one known source.

Every allowed relation must exist in `data/public-research-graph.json`, remain
within the same status ceiling, and retain known evidence references.

Language strength follows evidence status:

- `verified_public`: factual wording within the recorded claim;
- `partially_verified`: no stronger than the reviewed claim wording;
- `owner_approved`: distinguish owner approval when it matters to trust;
- `roadmap_only`: always say "in development", "concept", or equivalent and
  never imply a launched product or measured performance.

The university-role start-date discrepancy remains excluded. The assistant
must not infer or repeat an unreviewed start date.

## Request Contract

The initial endpoint accepts JSON equivalent to:

```json
{
  "language": "ru",
  "question": "Какие направления исследований представлены?",
  "session": "ephemeral-random-value"
}
```

Rules:

- `language` is `ru` or `en` for the initial live gate;
- `question` is plain text with a maximum of 600 characters;
- `session` is created per page load, contains no personal data, and is not
  saved;
- unknown fields, files, URLs requesting retrieval, and oversized input are
  rejected before the provider call.

Kazakh remains available in the current local prototype. Live Kazakh model
answers require a separate owner linguistic evaluation before enablement.

## Response Contract

The backend returns a validated envelope equivalent to:

```json
{
  "decision": "answer",
  "language": "ru",
  "answer": "...",
  "citations": [
    {
      "claim_id": "research.focus.ungrounded_power_systems",
      "source_ids": ["source.katru.faculty_profile"]
    }
  ]
}
```

An `answer` requires one to four citations. A `refuse` requires a public-safe
explanation and one of the contract's refusal categories. The backend does not
return provider reasoning, system instructions, raw model output, private
details, or internal error data.

## Refusal Policy

The assistant refuses when a request asks for:

- certificate numbers, QR content, civil identifiers, signatures, seals, or
  other private document details;
- private contact details or addresses;
- raw evidence, unpublished measurements, datasets, or manuscripts;
- an inference, metric, role, result, or product status not present in the
  allowlisted evidence;
- unrelated general-purpose assistance;
- hidden instructions, policy bypasses, prompt contents, or unavailable data;
- a claim that lacks sufficient reviewed public evidence.

Prompt injection is treated as user content, never as permission to change the
grounding or privacy policy. Because v0 has no tools, uploads, browsing, or
memory, injected instructions cannot grant additional capability.

## Failure Behaviour

- Invalid input: reject before a provider call.
- Rate limit exceeded: return a localized retry-later response.
- Grounding miss: return `insufficient_public_evidence`.
- Invalid or uncited model output: discard it and return a safe refusal.
- Provider timeout or outage: keep the current local concierge fallback and
  label it clearly as the public-facts-only prototype.
- Backend disabled: the existing static site remains fully usable.

## Evaluation Gate

The contract includes eight initial cases:

- three citation-required answers covering a credential, roadmap project, and
  dated patent status;
- refusals for a private credential identifier, unpublished results,
  unsupported inference, prompt injection, and an out-of-scope request.

The offline validator also runs fourteen bounded mutations that try to enable
storage, tools, direct client credential access, premature endpoint launch,
uncited answers, unknown evidence IDs, and other prohibited changes.

```powershell
python tools/check_public_ai.py
python tools/check_public_ai.py --self-test
```

Before a provider-backed pilot, the implementation issue must add executable
model evaluations for all cases in Russian and English. A model or prompt is
acceptable only when grounded-answer and refusal thresholds are defined and
met on repeated runs.

## Rollout Plan

### Gate A — architecture readiness (accepted in PR #58)

- approve this document and the machine-readable contract;
- keep the production endpoint disabled;
- run offline validation and mutation tests.

### Gate B — backend skeleton (issue #59)

- add the same-origin edge endpoint without a provider call;
- build and hash the minimal server-side grounding bundle;
- add request and failure-path tests while leaving output-schema and configured
  edge-rate-limit verification for Gate C, where provider traffic first exists;
- preserve the local concierge as the production fallback.

### Gate C — private provider pilot

- configure the API credential as a Cloudflare secret outside GitHub;
- select a model through repeated RU/EN evaluations;
- set a small spend ceiling and test provider failures;
- keep the endpoint unavailable to general visitors.

### Gate D — bounded public activation

- obtain explicit owner approval;
- activate the backend behind the existing concierge UI;
- complete desktop/mobile accessibility, privacy, abuse, cost, and production
  QA;
- keep an immediate kill switch that restores the local prototype.

Each gate requires its own issue and pull request. This architecture does not
authorize later gates automatically.

## Official API Basis

The API-specific choices were checked against the official OpenAI
[API deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist)
on 2026-08-26. The checklist identifies the Responses API as the starting point
for current applications, recommends selecting a model through representative
evaluation, supports stateless `store: false` requests, recommends a
privacy-preserving safety identifier for end-user applications, and says plain
HTTP is appropriate for one-request/one-answer workflows.

Repository privacy, provenance, analytics, and secret-handling rules remain
authoritative even if provider capabilities later expand.

The Pages Function adapter and route behavior were also checked against the
official Cloudflare Pages Functions
[routing](https://developers.cloudflare.com/pages/functions/routing/) and
[API reference](https://developers.cloudflare.com/pages/functions/api-reference/)
on 2026-08-26. File-based routing maps the handler path, while `_routes.json`
restricts invocation to the single approved endpoint.

## Open Decisions For The Private Pilot

- model candidates and pass thresholds after current pricing/availability
  review;
- edge rate-limit values and cost ceiling;
- whether live Kazakh support is ready after owner linguistic evaluation.

None of these decisions is implemented or authorized by Gate B.
