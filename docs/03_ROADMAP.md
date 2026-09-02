# Roadmap

## Phase 0 - Repository Foundation

Status: completed

- Add repository governance.
- Add AI Lab workflow.
- Add public content policy.
- Add Codex prompts.
- Add issue and pull request templates.
- Establish conservative public-content and AI Lab boundaries before website
  implementation work.

## Phase 1 - Public Content Inventory And Drafts

Status: in progress / partially completed

- Public content inventory exists as a draft for human review.
- Public source audit and positioning skeleton exists.
- Public biography and QR landing page drafts exist.
- Verified QR profile links and Russian QR copy have been added.
- The public professional contact route is explicitly approved and published;
  private contact data remains excluded.
- Evidence Spine v0.1 provides a machine-readable, public-safe evidence layer
  for a bounded set of high-value facts.
- Public Knowledge System v0.2 adds a compact claim-referenced research graph,
  deterministic RU/EN public CV documents, and block-level provenance. The
  generator owns only the two dedicated HTML CV routes and does not change the
  manually maintained profile routes.
- Official registry verification is complete for the three displayed patent
  records, and v1.2 reconciles their publication and dated legal-status wording
  with direct official-registry links.
- The owner-approved certified-energy-auditor status and 2026-08-14 to
  2029-08-06 term are published through the Evidence Spine, generated RU/EN CV
  drafts, and localized site presentation. Private credential details and the
  source document remain excluded, and the claim remains partially verified.
- Conflicting official university-role start dates remain explicit and require
  owner review before the production timeline changes.
- Publication, grant, credential, award, and project entries retain explicit
  evidence-status gaps where applicable.
- Private or unpublished source material remains excluded.

## Phase 2 - Information Architecture

Status: completed for v0.1

- Define site sections.
- Define QR landing page content.
- Define portfolio page structure.
- Define research page structure.
- Decide multilingual strategy for English, Russian, and Kazakh content.

## Phase 3 - Static Website Implementation

Status: completed through Claude Design v1.1 / maintenance pending

- Dependency-free static HTML implementation exists under `site/`.
- Maintain the current dependency-free static HTML path for production.
- Keep Astro as a future option only if complexity or multilingual duplication
  later justifies it.
- Do not add dependencies unless a future approved issue and PR justify them.
- PR #31 is the current production visual baseline.
- Static HTML remains manually maintained except for `/cv/` and `/en/cv/`,
  which are generated offline from the reviewed facts and graph.

## Phase 4 - Deployment Readiness

Status: completed for Cloudflare Pages production and current production QA

- Cloudflare Pages deployment readiness is complete for the existing `site/`
  directory.
- Cloudflare Pages preview is live at `https://ikurabayev-kz.pages.dev`.
- Production custom domains `https://ikurabayev.kz` and
  `https://www.ikurabayev.kz` were verified active with SSL through Cloudflare
  Pages, with Cloudflare DNS active for the domain.
- Production-domain QA was completed for the v1.1 release; it should be
  repeated after future visual or infrastructure changes.
- Evidence-backed release v1.2 adds apex self-canonicals, reciprocal profile
  hreflang, normalized social metadata, minimal Person JSON-LD, robots, sitemap,
  and a dependency-free offline release validator.
- The apex canonical metadata decision is complete. An optional actual
  `www`-to-apex redirect remains a separate Cloudflare control-plane task.
- The reviewed deterministic RU/EN public CV is published as dependency-free
  HTML at `/cv/` and `/en/cv/`. Issue #55 adds reproducible, static RU/EN PDF
  downloads from the same block model with separate hashes and visual QA.
- Production QA on 2026-08-22 confirmed the certified-energy-auditor update on
  the apex, `www`, and Cloudflare Pages preview hosts across desktop and mobile
  route checks, with apex canonical metadata retained.
- A bounded Kazakh language pass has corrected interface, terminology, and
  copy defects. The owner-approved exact display name
  `Қорабаев Ескендір Қазбекұлы` is canonical in the Evidence Spine; the semantic
  roles of `/` and `/ru/` remain open.
- Production QA on 2026-08-23 confirmed the merged Kazakh language and identity
  release on the apex, `www`, and Cloudflare Pages preview hosts. The external
  university start-date discrepancy is deferred until its source page is
  corrected; generated CVs continue to omit the disputed date.
- Keep launch checks privacy-safe and dependency-free unless a future PR changes
  the technical decision.

## Phase 5 - Publication And Maintenance

Status: in progress / post-launch maintenance

- Follow the ordered maintenance queue in `docs/05_ACTIVE_TASKS.md`.
- Review public content before each production release or claim update.
- Use `docs/16_VISUAL_DESIGN_SYSTEM.md` as the workflow for major visual
  changes.
- Start future major design changes in Claude Design, then integrate them
  through design-intake pull requests with a faithfulness report.
- Track content updates through issues and pull requests.
- Regenerate Living Public CV artifacts from canonical facts and relationships;
  do not manually maintain generated Markdown as a separate evidence source.
- Maintain decision log and roadmap as the project evolves.

## Phase 6 - Public AI Assistant Architecture

Status: in progress / Gates A-C accepted; Gate D1 readiness under issue #65

- Keep the visible AI console prototype/static/public-facts-only. Production
  continues to return a fail-closed response and does not expose the Gate C
  provider path to general visitors.
- Ground any future AI/agent layer in reviewed public Evidence Spine claims,
  and use only conservative reviewed graph relationships while keeping that
  integration a separate future phase.
- Design any real AI integration through a backend or edge function with secrets
  outside GitHub.
- Treat `docs/21_PUBLIC_AI_ASSISTANT_ARCHITECTURE.md` and the machine-readable
  `data/public-ai-contract.json` as the accepted Gate A boundary.
- Gate B builds and hashes an allowlisted server-side grounding module and tests
  the disabled Pages Function without credentials, external calls, storage, or
  runtime dependencies.
- Gate C permits a provider call only on an authenticated non-production Preview
  branch with explicit variables, a private token, the reviewed model allowlist,
  `store: false`, no tools, bounded retrieval, and strict output validation.
- Repeated Terra and Luna Preview evaluations pass the checked-in RU/EN suite.
  Issue #63 selects Luna for the private pilot after 32/32 Luna variants passed
  without provider retries; Terra remains a controlled fallback. The comparison
  is bounded evidence, not a general benchmark.
- Gate D1 prepares a fail-closed production runner that requires an exact
  kill-switch, production branch/origin, Luna, server-side key, and Cloudflare
  limiter. Contract flags for activation, control-plane readiness, and UI
  networking remain false.
- Gate D2 remains separate work and requires a distinct OpenAI production
  project/key, hard spend cap and alerts, configured durable limiter, moderation
  decision, full QA, and explicit owner approval. Gate D1 does not authorize
  Production provider traffic or a public UI.
- Require the offline public-AI validator, refusal suite, and repeated live
  model evaluations to pass before any bounded public endpoint is proposed.
- Do not combine real AI/API launch work with visual design ports unless a
  future approved task explicitly combines that scope.
