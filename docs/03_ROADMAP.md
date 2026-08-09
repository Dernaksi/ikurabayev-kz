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
- Official registry verification is complete for the three displayed patent
  records; the resulting presentation mismatches remain pending reconciliation.
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
- Static HTML remains the manually maintained presentation layer and is not
  generated from Evidence Spine v0.1.

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
- Remaining polish includes SEO metadata, the `www` versus apex policy, Kazakh
  language review, patent presentation reconciliation, and a sanitized public
  CV.
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
- Maintain decision log and roadmap as the project evolves.

## Phase 6 - Public AI Assistant Architecture

Status: future / separate phase

- Treat AI console or AI assistant UI as prototype/static/public-facts-only
  until a separate architecture decision and pull request approve real backend
  functionality.
- Ground any future AI/agent layer in reviewed public Evidence Spine claims,
  while keeping that integration a separate future phase.
- Design any real AI integration through a backend or edge function with secrets
  outside GitHub.
- Do not combine real AI/API launch work with visual design ports unless a
  future approved task explicitly combines that scope.
