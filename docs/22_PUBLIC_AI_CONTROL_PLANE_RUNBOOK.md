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

## Current State

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
