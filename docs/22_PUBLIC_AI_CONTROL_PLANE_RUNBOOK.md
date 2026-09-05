# Public AI Control-Plane Runbook

Status: Gate D2a code readiness under Issue #67; no public activation

Reviewed: 2026-09-02

## Purpose

This runbook records the safe order for preparing the public AI control plane.
It does not authorize a Production provider call or a network-enabled concierge.
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
  -> PUBLIC_AI_RATE_LIMITER Rate Limiting binding
```

The Worker has `workers_dev: false`, `preview_urls: false`, no public route, and
a shared `public-ai:/api/ai/ask` key. It admits at most two calls per 60 seconds
per Cloudflare location. Cloudflare describes these counters as permissive and
eventually consistent, so the OpenAI hard spend limit remains the cost backstop.

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
- Wrangler 4.36.0 deployed the non-public rate-limit Worker. Deployment output
  confirmed `PUBLIC_AI_RATE_LIMITER` at 2 requests/60 seconds and no deploy
  targets. The active Worker version was verified through Wrangler.
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
2. Verify the deployed internal binding and key end-to-end under a separately
   approved bounded test procedure; do not enable public traffic as a shortcut.
3. Complete adversarial, privacy, accessibility, mobile, cost, and live rollback
   QA for the actual network-enabled UI. The current local-only UI cannot stand
   in for those checks.
4. Obtain explicit owner activation approval. Keep `AI_PUBLIC_ENABLED` absent
   and the machine-readable activation/readiness flags false until the remaining
   gates are closed and recorded through review.

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

## Later Owner-Operated Sequence

Complete these steps only after the Gate D2a PR is reviewed and merged.

1. Create a separate OpenAI project for Production.
2. Restrict the project to the selected `gpt-5.6-luna` model.
3. Configure an enforced USD 10 monthly project hard limit.
4. Configure recommended USD 5 and USD 8 email alerts.
5. Create a project-scoped API key and copy it directly into a Cloudflare
   Production secret named `OPENAI_API_KEY`. Do not expose the value elsewhere.
6. Deploy `ikurabayev-public-ai-rate-limiter` from its isolated Wrangler
   project. The deployment must retain no public route or preview URL.
7. Add a Production-only Pages Service Binding named
   `AI_PUBLIC_RATE_LIMITER` targeting that Worker.
8. Add the Production text variable `AI_PUBLIC_MODEL=gpt-5.6-luna`.
9. Do not add `AI_PUBLIC_ENABLED=true` yet.
10. Complete moderation, adversarial, privacy, mobile, accessibility, cost, and
    rollback QA in a separate issue and PR.
11. Obtain explicit owner approval immediately before enabling the kill switch
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

The primary rollback remains omission or removal of `AI_PUBLIC_ENABLED`.
Removing the Pages Service Binding or the Production key also fails closed, but
the kill switch is the intended first response. The static site and local
public-facts concierge remain usable without either Worker or OpenAI.

## Official References

- [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [OpenAI spend limits](https://developers.openai.com/api/docs/guides/spend-limits)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [Cloudflare Pages bindings](https://developers.cloudflare.com/pages/functions/bindings/)
- [Cloudflare Pages Wrangler configuration](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)
- [Cloudflare Rate Limiting binding](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)
