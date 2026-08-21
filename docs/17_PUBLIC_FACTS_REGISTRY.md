# Public Facts Registry

## Purpose

`data/public-facts.json` is the public-safe provenance layer for a bounded set
of high-value facts used by IKurabayev.kz. It keeps evidence status and review
dates separate from presentation wording so future website, SEO, CV, concierge,
and AI work can reuse the same reviewed foundation.

The v0.1 chain is:

`claim → evidence → status → verification date → presentation → future answer`

The registry is intentionally small. It is not a full CV, database server, CMS,
API, backend, RAG system, or replacement for public-content review.

## Three Layers

1. **Evidence layer:** `data/public-facts.json` stores public-safe claims,
   sources, statuses, and review dates.
2. **Presentation layer:** the dependency-free static HTML under `site/` and the
   local concierge remain manually maintained public presentation.
3. **Future AI/agent layer:** any later evidence-grounded assistant must be a
   separate approved architecture and may consume only reviewed public facts.

The current Cloudflare Pages site deploys `site/`; the registry is not
automatically deployed or read at runtime.

## Registry Contract

Top-level fields:

- `schema_version`: small schema revision.
- `subject`: stable subject identity and canonical identity claim.
- `generated_or_reviewed_at`: date of the registry review.
- `claims`: bounded public-safe facts.
- `sources`: public-safe provenance records.

Claim fields:

- `id`: stable, human-readable identifier.
- `kind`: broad fact category.
- `public`: confirms that the registry record itself is public-safe.
- `status`: evidence status defined below.
- `value`: the bounded fact value or structured value.
- `evidence[]`: source IDs from `sources`.
- `verified_at`: required for publicly verified or partially verified claims.
- `presentation_notes`: limits, gaps, currentness, or presentation mismatch.
- `languages`: included only where locale handling materially affects identity.

Source fields contain only public-safe provenance: `id`, `kind`, optional
public `url`, `checked_at`, `authority`, `source_role`, and an optional
`public_safe_note`. Generic owner approval and sanitized owner-supplied document
review deliberately omit private artifact names, paths, identifiers, and
metadata. A sanitized private-evidence source never receives a URL and does not
count as independent public verification.

`public: true` means the registry entry is safe to review publicly. It does not
automatically authorize every field for every presentation. The public-content
policy remains authoritative.

## Statuses

| Status | Meaning |
| --- | --- |
| `verified_public` | All recorded fields were checked against suitable public, authoritative evidence. |
| `owner_approved` | The fact is approved for public display, but independent public verification is not complete. |
| `partially_verified` | Some recorded fields are publicly verified and the material gap is explicit. |
| `needs_verification` | Adequate evidence review has not yet been completed. |
| `roadmap_only` | A public direction in development, not a launched product or validated result. |

Evidence status is distinct from a patent's legal status. For example, a
historical patent can be `verified_public` while its structured value correctly
records `not_in_force`.

## Source Authority Hierarchy

Use the strongest available source for the field being verified:

1. Qazpatent, EAPO, and other official registries.
2. Official institutional or issuer records.
3. DOI, publisher metadata, ORCID, and curated academic identity records.
4. Reputable secondary databases only as supporting evidence.
5. Sanitized review of owner-supplied evidence for specifically approved
   public-safe fields where no suitable public source is available.
6. Generic owner approval.

The current website is a presentation reference, not independent evidence.
Search snippets and visual copies of documents are not authoritative registry
sources.

## Privacy Boundary

The registry must not contain private contact details, addresses, civil
identifiers, certificate or attestation identifiers, private file names or
paths, raw scans, QR or EDS content, signatures, seals, contracts, unpublished
research data, confidential project details, or information about other private
individuals.

The owner may explicitly approve a minimal public-safe fact learned from private
evidence, such as credential issue and validity dates. In that case, record only
the approved fact, a generic sanitized source, and the independent-verification
gap. Never record or link the private artifact or its identifying metadata.

An official public record may expose fields outside this boundary. Record only
the minimum fact needed for the reviewed claim. Patent entries therefore store
the subject's verified relationship and publicly relevant institutional
ownership without reproducing other-person or correspondence metadata.

## Update Workflow

1. Open a focused Issue and define the claim, source, presentation impact, and
   privacy boundary.
2. Check the strongest available source and record the check date.
3. Update the smallest possible claim and source entries.
4. Validate JSON, unique IDs, evidence references, status values, privacy, and
   unsupported strengthening.
5. Review the diff through a focused pull request.
6. Reconcile website or concierge presentation in a separate bounded PR when
   the evidence layer exposes a mismatch.

Fast-changing roles and legal statuses must be rechecked before future public
copy changes. Owner approval must never be silently promoted to independent
verification.

## Consumers

- **Website HTML:** may later use registry facts as reviewed input, but v0.1
  does not generate or modify HTML.
- **Concierge:** may later replace duplicated curated facts after a separate
  behavior-preserving review.
- **JSON-LD / SEO:** may use only claims whose status and presentation policy
  support the intended metadata.
- **Sanitized CV:** may select reviewed public facts without importing private
  source artifacts.
- **Future AI/RAG:** must remain a separate architecture with public-facts-only
  retrieval, citations, privacy controls, and no automatic publication.

## v0.1 Non-Generation Rule

Evidence Spine v0.1 does not automatically generate the site, alter the local
concierge, introduce runtime loading, or add a framework, dependency, backend,
API, storage, analytics, or network behavior. Static HTML remains the current
presentation layer.
