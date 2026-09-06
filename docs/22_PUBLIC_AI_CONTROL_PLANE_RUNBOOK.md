# Public AI Control-Plane Runbook

Status: strict limiter deployed and rollback verified; public traffic disabled pending remaining QA

Reviewed: 2026-09-06

## Purpose

This runbook records the safe order for preparing the public AI control plane.
The owner authorized a bounded Production provider call and a network-enabled
RU/EN concierge without application text logging. The exact kill switch remains
off outside the completed bounded drill; persistent public traffic requires the
remaining QA and a fresh owner decision.
Secret values stay in the owner-operated OpenAI and Cloudflare dashboards and
must never be committed, pasted into issues, or shown in screenshots.

## Owner Decisions

- Hard OpenAI Production project limit: USD 10 per month.
- Recommended spend alerts: USD 5 and USD 8.
- Initial public provider languages: Russian and English.
- Kazakh provider mode remains deferred pending owner linguistic evaluation.
- Wrangler is allowed only as isolated build/deployment tooling for the
  non-public rate-limit Worker.

OpenAI documents that alerts notify but do not stop traffic. The USD 10 limit
must therefore be configured as an enforced hard project limit. Enforcement is
not instantaneous, so a small amount of recorded spend can exceed the limit.

## Architecture Correction

Cloudflare Pages Functions supports only a documented subset of bindings, and
the direct Rate Limiting binding is not in that subset. Gate D2a therefore uses:

```text
Pages Function
  -> AI_PUBLIC_RATE_LIMITER internal Service Binding
  -> ikurabayev-public-ai-rate-limiter Worker
  -> PUBLIC_AI_LIMITER Durable Object
```

The Worker has `workers_dev: false`, `preview_urls: false`, no public route, and
a shared `public-ai:/api/ai/ask` key. Its single named Durable Object admits at
most two calls in a rolling 60-second window globally. It persists only integer
admission timestamps: never question text, answer text, IP address, session, or
other client identifier. The OpenAI hard spend limit remains the independent
cost backstop.

## State At Gate D2a PR Creation

| Control | State after Gate D2a PR |
| --- | --- |
| Public AI kill switch | Off |
| Concierge network calls | Off |
| OpenAI Production project/key | Not configured |
| USD 10 hard limit | Owner-approved, not configured |
| Rate-limit Worker code | Prepared and locally verified |
| Rate-limit Worker deployment | Not performed |
| Pages Service Binding | Not configured |
| Moderation decision | Pending |
| Production QA and rollback drill | Pending |

## 2026-09-05 Control-Plane And Offline QA Record

PR #68 was merged. This dated record distinguishes observed configuration from
functional end-to-end evidence; it does not authorize activation.

- The separate Production OpenAI project was configured in the dashboard with
  Luna only, an enforced USD 10 monthly limit, and USD 5/USD 8 alerts. Hard-limit
  enforcement latency can still allow a small overshoot.
- The owner reported saving the Production key and the Pages Service Binding
  `AI_PUBLIC_RATE_LIMITER` with the `Default` entrypoint. Secret values were not
  inspected. The reported key and binding are not yet functionally verified in
  a Production provider request.
- Wrangler 4.36.0 deployed a non-public Worker using Cloudflare's permissive
  `PUBLIC_AI_RATE_LIMITER` binding. It had no public route or deploy target.
- Pages redeployed the merged `d4cc806` source successfully. The public homepage
  returned 200; valid RU/EN requests returned the expected disabled 503 with
  `Cache-Control: no-store`; a foreign-origin request returned 403. These checks
  do not prove that the limiter or provider key works, because the disabled
  path does not exercise them.
- Issue #69 fixes a timeout found during offline QA: the abort timer was cleared
  after headers, before JSON body consumption. A fake-clock test first failed
  against that implementation, then passed with the deadline kept active through
  body consumption. Both public and private modes return generic 503 on an
  abort and do not retry it. Ordinary malformed JSON retains one public attempt
  or at most two private attempts.
- Offline rollback checks cover RU/EN with a missing, false, uppercase, or
  boolean enable flag, missing key, and missing Service Binding. All cases
  return 503 before either the limiter or provider is called. This is not a
  live enabled-to-disabled rollback drill.

## 2026-09-06 Strict-Limit Correction

Bounded live verification showed three rapid ordinary requests receiving 200.
That does not prove the existing Service Binding was broken: the former
Cloudflare Rate Limiting binding is intentionally per-location and eventually
consistent. It is nevertheless insufficient for the strict two-request public
gate required by this project.

Issue #77 replaced that binding with one global Durable Object and a rolling
60-second counter. On 2026-09-06 the non-public Worker was deployed, the
existing Production Pages Service Binding was verified against it, and a
bounded Production drill returned 200, 200, then 429 for three rapid ordinary
requests. The third request was rejected before any provider call. The exact
`AI_PUBLIC_ENABLED=false` kill switch was then redeployed and the endpoint
returned 503. No question or answer content was logged by the application.

Remaining launch gates:

1. Review and test the implemented inline moderation policy in Issue #71. The
   existing Responses request now asks for `omni-moderation-latest` results for
   both input and output. A flagged, missing, malformed, or error result returns
   a generic unavailable response without exposing model text or retrying the
   provider. This documented Responses feature avoids a second moderation API
   request and does not broaden the key scope. It is code readiness only:
   complete adversarial live QA before treating the policy as operational.
   Deterministic phrase filters and structured citation validation remain
   complementary controls; they do not prove every sentence is semantically
   supported by its cited source.
   Issue #73 adds a twelve-case RU/EN corpus for the owner-operated private
   pilot, including privacy, raw-artifact, ungrounded-role, and false-
   verification red-team prompts. The checked-in corpus is inert: only the
   separate owner-operated runner can make a provider call after a token is
   supplied locally. Its results validate observed decisions, not hidden
   moderation scores, so they do not replace broader live QA.
2. Complete adversarial, privacy, accessibility, mobile, cost, and live rollback
   QA for the actual network-enabled UI. The bounded control-plane drill does
   not replace those checks.
3. Owner activation approval was granted on 2026-09-05. The bounded deployment
   and rollback drill is complete; request a fresh decision before leaving the
   kill switch on for persistent public traffic.

## Repository Verification

From `workers/public-ai-rate-limiter`:

```powershell
pnpm install --frozen-lockfile
pnpm test
pnpm check
```

`pnpm check` performs a Wrangler dry-run only. It does not deploy the Worker.
The main repository validators continue to confirm that Production activation,
control-plane readiness, and UI networking are false.

## Persistent-Activation Preflight

The completed control-plane steps are retained here for auditability. Future
persistent activation must start from the remaining QA gates above.

1. Reconfirm the separate Production OpenAI project remains limited to
   `gpt-5.6-luna`, with its enforced USD 10 monthly hard limit and USD 5/USD 8
   alerts.
2. Confirm the project-scoped key remains available only through the Cloudflare
   Production secret `OPENAI_API_KEY`; do not expose the value elsewhere.
3. Confirm that the deployed `ikurabayev-public-ai-rate-limiter` retains no
   public route or preview URL and stores only rolling admission timestamps.
4. Confirm the Production-only Pages Service Binding named
   `AI_PUBLIC_RATE_LIMITER` still targets that Worker.
5. Retain the Production text variable `AI_PUBLIC_MODEL=gpt-5.6-luna`.
6. Keep `AI_PUBLIC_ENABLED=false` until a persistent launch decision.
7. Complete moderation, adversarial, privacy, mobile, accessibility, cost, and
    rollback QA in a separate issue and PR.
8. Obtain explicit owner approval immediately before enabling the kill switch
    and connecting the visible concierge to the backend.

## Pages Wrangler Boundary

Do not hand-write a root Pages Wrangler file over the current Dashboard-managed
configuration. Cloudflare says a Pages Wrangler file becomes the configuration
source of truth and recommends downloading the existing project settings first:

```powershell
npx wrangler pages download config ikurabayev-kz
```

That migration is not part of Gate D2a. The Production Service Binding may be
configured through the Cloudflare dashboard, or a later reviewed change may
download, audit, and adopt the complete Pages configuration.

## Rollback

The primary rollback remains setting `AI_PUBLIC_ENABLED` to exact text `false`
and redeploying the current Production source.
Removing the Pages Service Binding or the Production key also fails closed, but
the kill switch is the intended first response. The static site and local
public-facts concierge remain usable without either Worker or OpenAI.

## Official References

- [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [OpenAI spend limits](https://developers.openai.com/api/docs/guides/spend-limits)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [Cloudflare Pages bindings](https://developers.cloudflare.com/pages/functions/bindings/)
- [Cloudflare Pages Wrangler configuration](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)
- [Cloudflare Durable Objects](https://developers.cloudflare.com/durable-objects/)
