# Public AI Assistant Architecture

Status: Gates A-D1 accepted; Gate D2a control-plane readiness proposed in issue #67

Reviewed: 2026-09-02

## Purpose

This document defines the smallest safe architecture for turning the existing
local public-facts-only concierge into a real AI assistant. Gates A-D1 are
accepted. Gate D2a prepares a non-public rate-limit gateway that still cannot
activate the public service without separate control-plane work, QA, and owner
approval.

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
  Function, provider-capable in the authenticated private Preview and prepared
  to remain fail-closed behind independent production controls;
- the OpenAI Responses API from the server side only;
- a Cloudflare secret binding for the provider credential;
- an internal Pages Service Binding to a non-public Worker that owns the
  Cloudflare Rate Limiting binding;
- one request and one answer over HTTP, with `store: false`;
- no model tools, web search, uploads, persistent memory, response chaining,
  background jobs, analytics, or content logging;
- deterministic grounding from the reviewed Evidence Spine and public research
  graph;
- structured answers with claim/source citations or a categorized refusal.

Public activation is not authorized. Luna is fixed for the private pilot and
the future bounded public mode; Terra remains only a controlled private fallback
and re-evaluation candidate. The selection uses the checked-in cases for
grounded-answer success, refusal success, latency, token use, and cost per
successful answer.

## Current Gate C Implementation

Gate B remains the production behavior. Gate C adds a separate private path:

- `site/_routes.json` sends only `/api/ai/ask` to Pages Functions;
- `functions/api/ai/ask.js` validates method, same origin, media type, exact
  fields, language, session form, size, control characters, and URL retrieval;
- production, `main`, the canonical `*.pages.dev` host, missing configuration,
  missing/invalid pilot authentication, and unknown model configuration all
  return a localized structured failure before an outbound call;
- only a non-production Preview branch with `AI_PILOT_ENABLED=true`, a matching
  private `X-Pilot-Token`, `OPENAI_API_KEY`, and an allowlisted server-side model
  may call the provider;
- `gpt-5.6-luna` is the selected private-pilot model; `gpt-5.6-terra` is
  available only as a controlled fallback or explicit re-evaluation candidate;
- the application admits at most two requests per minute per active isolate,
  below the configured private provider-project limit of three requests per
  minute; Gate D1 additionally requires a working Cloudflare limiter for any
  future production provider call;
- each provider request uses `/v1/responses`, `store: false`, `background:
  false`, no tools, a 700-token output ceiling, a 15-second timeout, an
  ephemeral session hash, and Structured Outputs through `text.format`;
- deterministic local retrieval sends no more than five allowlisted claims plus
  their connected reviewed relations, sources, and topics;
- after Preview authentication, explicit requests for private identifiers,
  private contact or address data, raw or unpublished material, and prompt
  bypasses, plus explicit requests to invent unpublished metrics, are refused
  deterministically before rate-limit consumption or any provider call;
- the edge verifier discards malformed output, unknown or non-selected claims,
  and source IDs that do not belong to the cited claim; one validation-only
  retry is allowed for an HTTP-success provider response that fails this local
  verifier, while network and provider HTTP failures are never retried;
- `tools/build_public_ai_grounding.py` deterministically selects only the
  contract allowlists and writes a server-side module plus byte-level
  provenance;
- `tools/check_public_ai.py` verifies the route, handler safety markers, source
  and output hashes, counts, privacy boundary, and byte-identical regeneration;
- `tools/test_public_ai_backend.mjs` exercises request rejection, production
  isolation, authentication, rate limiting, request shape, model allowlisting,
  provider failures, and citation rejection with a stubbed fetch only;
- `tools/run_public_ai_pilot_evals.mjs` is an explicit paid/live Preview runner
  for repeated RU/EN cases; it reports only case IDs, decisions, latency, token
  counts, model, and pass/fail, never questions, answers, or credentials.

The current bundle contains 25 claims, 39 relations, 15 sources, and 8 topics.
These counts describe reviewed grounding records, not model performance or a
live service. The browser does not load the bundle.

### Preview evaluation evidence

On 2026-08-28, `gpt-5.6-terra` completed repeated authenticated Preview runs
over the checked-in RU/EN suite. The final full round on commit `463aae7`
passed 16/16 variants. The RU credential answer used two provider attempts and
passed, directly exercising the bounded validation-only retry after the same
case had produced one fail-closed 502 in an earlier run. Deterministic privacy,
raw-material, prompt-injection, and invented-metric refusals returned no model
token counts because no provider call was made. Evaluation output recorded only
case IDs, language, decision, latency, token counts, attempt count, model,
status, and pass/fail; request and response content and credentials were not
logged.

On 2026-09-02, `gpt-5.6-luna` completed two full authenticated Preview rounds
on the merged Gate C code: 32/32 RU/EN variants passed. All 16 provider-backed
variants completed in one attempt, and deterministic refusals continued to
bypass the provider. The observed Luna provider-backed latency was 3,544 ms on
average (3,107 ms median; 8,875 ms maximum). One Luna round used 13,747 input
and 1,225 output tokens. The final Terra round used 15,052 input and 1,095
output tokens across eight provider-backed variants, with one retry; its
observed average latency was 2,686 ms (2,245 ms median; 5,523 ms maximum).

Using the official standard short-context prices checked on 2026-09-02 -- Terra
at $2 per million input tokens and $12 per million output tokens, and Luna at
$0.20 and $1.20 respectively -- with no input-cache discount, the observed
Terra round is estimated at $0.043244 and one Luna round at $0.0042194. Luna was
therefore about 90% less expensive for the bounded successful sample, while its
average latency was about 32% higher. The sample sizes differ, so these figures
are Gate C decision evidence rather than a general model benchmark. Issue #63
selects Luna for the private pilot; Terra remains a controlled fallback.

This is Gate C evidence, not authorization for a public service. Production,
the visible concierge, and the canonical Pages host remain fail-closed.

### Preview control-plane configuration

The Gate C branch requires these settings in Cloudflare **Preview only**:

- encrypted secret `OPENAI_API_KEY`;
- encrypted secret `AI_PILOT_TOKEN`, at least 32 characters and unrelated to
  the provider key;
- text variable `AI_PILOT_ENABLED` with exact value `true`;
- text variable `AI_PILOT_MODEL` with the selected value `gpt-5.6-luna`.

Do not add these settings to Production. The provider key alone never enables
the path. Changing `AI_PILOT_MODEL` to `gpt-5.6-terra` is reserved for a
controlled fallback test or explicit re-evaluation. Secret values must not be
pasted into issues, pull requests, logs, screenshots, or evaluation output.

## Accepted Gate D1 Readiness

PR #66 accepted a public runner without activating it or changing the local
concierge. The runner can call the provider only when all of these conditions
are true at once:

- the exact kill switch `AI_PUBLIC_ENABLED=true` is present;
- `CF_PAGES_BRANCH` is `main` or `master`, and the request uses an allowlisted
  production origin;
- `AI_PUBLIC_MODEL` is exactly the selected `gpt-5.6-luna` model;
- a non-empty server-side `OPENAI_API_KEY` is present;
- `AI_PUBLIC_RATE_LIMITER` exposes the reviewed internal Service Binding and
  its gateway admits the shared route key.

Missing, malformed, rejected, or throwing configuration fails closed before an
OpenAI call. Deterministic privacy, raw-material, prompt-injection, and
invented-metric refusals still bypass the provider. A public request gets one
provider attempt only; the private pilot retains its bounded validation-only
retry. Public responses expose no pilot authentication, model, attempt, or token
usage headers.

This is code readiness only. `public_activation.enabled`,
`public_activation.control_plane_ready`, and
`public_activation.ui_network_enabled` remain `false` in the contract. The
current visible concierge still makes no network request, and current
Production continues to return the disabled 503 response.

## Proposed Gate D2a Control-Plane Readiness

Cloudflare Pages Functions supports Service Bindings but does not support the
Rate Limiting binding directly. Issue #67 therefore prepares this internal path:

```text
Pages Function
  -> AI_PUBLIC_RATE_LIMITER internal Service Binding
  -> ikurabayev-public-ai-rate-limiter Worker
  -> PUBLIC_AI_RATE_LIMITER Rate Limiting binding
```

The isolated Worker pins Wrangler 4.36.0, has no public route or preview URL,
and admits at most two requests per 60 seconds per Cloudflare location. The
Pages adapter accepts only a 204 admission response, treats 429 as rejection,
and fails closed on missing configuration, exceptions, malformed values, or
every other status. The shared route key avoids storing or rate-limiting by IP.

The owner approved bounded Wrangler use, set the future OpenAI Production
project hard limit to USD 10, and selected Russian and English for the initial
provider mode. Recommended spend alerts are USD 5 and USD 8. Alerts notify but
do not stop traffic, and hard-limit enforcement is not instantaneous. Kazakh
provider answers remain deferred pending owner linguistic evaluation.

Gate D2a does not deploy the Worker, configure the Service Binding, create the
Production provider project or key, set `AI_PUBLIC_ENABLED=true`, or connect the
visible concierge. Because a root Pages Wrangler file would become the source
of truth for existing Dashboard-managed configuration, none is created here.
Any later migration must first download and audit the current Pages project
configuration. The exact owner-operated order is recorded in
`docs/22_PUBLIC_AI_CONTROL_PLANE_RUNBOOK.md`.

The limiter uses one shared route key per Cloudflare location to avoid storing
or rate-limiting on IP addresses. Cloudflare documents this API as permissive,
eventually consistent, and unsuitable for exact cost accounting. The OpenAI
project USD 10 hard spend limit is therefore an independent requirement, not a
substitute for the edge limiter.

## System Boundary

```text
Visitor browser
  |
  | POST /api/ai/ask (same origin, <= 600 characters)
  v
Cloudflare edge boundary
  |- validate language, size, and origin
  |- call the internal rate-limit gateway through a Service Binding
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
- require the reviewed internal Cloudflare rate-limit gateway before any public
  provider call;
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
  ],
  "refusal_category": null
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
- Invalid or uncited model output: discard it and return a safe refusal; public
  mode does not retry the provider.
- Inline moderation: if either the input or output moderation result is flagged,
  missing, malformed, or an error, discard the exchange and return a generic
  unavailable response without retrying the provider.
- Provider timeout or outage: keep the current local concierge fallback and
  label it clearly as the public-facts-only prototype.
- Backend disabled: the existing static site remains fully usable.

## Evaluation Gate

The contract includes twelve initial cases:

- three citation-required answers covering a credential, roadmap project, and
  dated patent status;
- refusals for a private credential identifier, unpublished results,
  unsupported inference, prompt injection, and an out-of-scope request;
- adversarial refusals for a private residential address and raw certificate
  artifacts;
- two semantic red-team cases that try to invent a professional role or
  overstate independent credential verification. They accept only the bounded
  `unsupported_inference` or `insufficient_public_evidence` refusal categories.

The offline validator also runs twenty-five bounded mutations that try to enable
storage, tools, direct client credential access, premature endpoint/UI launch,
an unreviewed control plane, public provider retries, uncited answers, unknown
evidence IDs, a raised spend limit, premature Kazakh provider mode, and other
prohibited changes. The backend suite has 45 offline stubbed cases, including
the Production configuration and internal limiter-gateway gates. The isolated
Worker adds six offline request and failure-path tests.

```powershell
python tools/check_public_ai.py
python tools/check_public_ai.py --self-test
```

After the PR has a private Preview deployment, the owner may set
`PUBLIC_AI_PILOT_URL` and `AI_PILOT_TOKEN` only in the local shell and run:

```powershell
node tools/run_public_ai_pilot_evals.mjs
```

The runner defaults to three repetitions of every RU/EN prompt and waits 31
seconds between calls so it stays below the reviewed private-pilot rate. Set
`PUBLIC_AI_EVAL_CASE` to one checked-in case ID for a bounded smoke test. Do not
commit or paste the local token.

Gate C includes executable prompts for all cases in Russian and English. A
model or prompt is acceptable only after repeated Preview runs meet the checked
expectations. Terra and Luna have completed the bounded live evaluation; the
offline suite does not simulate or replace that evidence.

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

### Gate C — private provider pilot (accepted in PR #62)

- configure credentials as Preview-only Cloudflare secrets outside GitHub;
- require a separate pilot token and explicit Preview enable flag;
- use the Issue #63 Luna selection and retain Terra only as a controlled
  fallback or re-evaluation candidate;
- keep application/provider rate limits and the small spend ceiling active;
- test provider failures with offline stubs before any paid evaluation;
- keep the endpoint unavailable to general visitors and production.

### Gate D1 — fail-closed public readiness (accepted in PR #66)

- require exact production branch, origin, model, secret, kill-switch, and
  Cloudflare limiter configuration;
- keep all public activation, UI networking, and control-plane readiness flags
  false;
- use one provider attempt per admitted public request;
- preserve the Gate C private pilot and deterministic refusal boundary;
- merge only after offline/backend/privacy review.

### Gate D2a — control-plane code readiness (issue #67)

- pin Wrangler 4.36.0 only inside the isolated rate-limit Worker;
- keep the Worker private with no route or preview URL;
- enforce two requests per 60 seconds through its Rate Limiting binding;
- call it only through a Production Pages Service Binding;
- keep Worker deployment, Service Binding configuration, provider credentials,
  activation, and UI networking outside the PR;
- verify the Worker with offline tests and a Wrangler dry-run.

### Gate D2b — owner-operated control plane and bounded public activation

- create the separate OpenAI Production project with the USD 10 hard limit and
  USD 5/USD 8 alerts;
- deploy the non-public limiter Worker and configure the Production-only Pages
  Service Binding;
- complete the moderation decision and full adversarial/privacy/cost/rollback
  QA;
- obtain explicit owner approval immediately before activation;
- activate the backend behind the existing concierge UI;
- complete desktop/mobile accessibility, privacy, abuse, cost, and production
  QA;
- keep an immediate kill switch that restores the local prototype.

Each gate requires its own issue and pull request. This architecture does not
authorize later gates automatically.

## Official API Basis

The API-specific choices were checked against the official OpenAI
[API deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist),
[production best-practices guide](https://developers.openai.com/api/docs/guides/production-best-practices),
[safety best-practices guide](https://developers.openai.com/api/docs/guides/safety-best-practices),
[Responses migration guide](https://developers.openai.com/api/docs/guides/migrate-to-responses),
and [Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs)
on 2026-09-02. Model costs were checked against the official OpenAI
[API pricing page](https://developers.openai.com/api/docs/pricing). The guidance
identifies the Responses API as the starting point for current applications,
recommends selecting a model through representative evaluation, supports
stateless `store: false` requests, recommends a
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

The Gate D limiter contract was checked against the official Cloudflare
[Rate Limiting binding documentation](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)
on 2026-09-02. The binding returns `{ success }` from `limit({key})`, requires
Wrangler 4.36.0 or later, is local to each Cloudflare location, and is explicitly
not an exact accounting system. The official Cloudflare Pages
[bindings documentation](https://developers.cloudflare.com/pages/functions/bindings/)
confirms that Service Bindings are supported while direct Rate Limiting bindings
are not listed for Pages Functions. The official Pages
[Wrangler configuration guide](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)
says a root configuration becomes the source of truth and recommends downloading
existing Dashboard configuration before migration.

## Remaining Decisions After Implementation

- deployment of the reviewed non-public Worker and configuration of the
  Production-only Pages Service Binding;
- a separate OpenAI Production project/key with the owner-approved USD 10 hard
  limit and recommended USD 5/USD 8 alerts;
- the bounded moderation decision and public issue-report workflow;
- desktop/mobile accessibility, adversarial, privacy, cost, and rollback QA;
- whether live Kazakh support is ready after owner linguistic evaluation.

None of these decisions authorizes Gate D2 or changes the production concierge.
