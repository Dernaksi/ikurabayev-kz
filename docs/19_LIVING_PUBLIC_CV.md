# Living Public CV

## Purpose

The Living Public CV is a deterministic, sanitized presentation derived from
the reviewed public facts and relationship graph. It provides equivalent
Russian and English Markdown review documents, published HTML routes, and
downloadable static PDF exports without making any generated document the
canonical source of truth.

Canonical facts remain in `data/public-facts.json`. Canonical relationships
remain in `data/public-research-graph.json`. Generated CV files must never be
edited as independent source material.

## Inputs And Outputs

Generator:

- `tools/build_public_cv.py`
- `tools/build_public_cv_pdf.py`

Exact inputs:

- `data/public-facts.json`
- `data/public-research-graph.json`

Generated outputs:

- `cv/IKurabayev_Public_CV_RU.md`
- `cv/IKurabayev_Public_CV_EN.md`
- `site/cv/index.html`
- `site/en/cv/index.html`
- `cv/IKurabayev_Public_CV_PROVENANCE.json`
- `site/output/pdf/IKurabayev_Public_CV_RU.pdf`
- `site/output/pdf/IKurabayev_Public_CV_EN.pdf`
- `cv/IKurabayev_Public_CV_PDF_PROVENANCE.json`

The Markdown outputs remain public review artifacts. The equivalent HTML
outputs are published at `/cv/` and `/en/cv/`. The generator owns only those two
site documents. Each page links to its matching static PDF under `/output/pdf/`;
all other static profile pages remain manually maintained.

## Deterministic Build Contract

The generator uses only the Python standard library and supports:

```powershell
python tools/build_public_cv.py --write
python tools/build_public_cv.py --check
```

Determinism rules:

- read exact source bytes and hash those bytes;
- use one ordered bilingual block model for both languages;
- use explicit allowlists instead of exporting every registry claim;
- use fixed sorting for repeated items;
- use the registry review date, never wall-clock time;
- use no random values, locale-dependent formatting, or machine paths;
- write UTF-8 with LF line endings;
- serialize JSON with stable indentation and a final newline;
- compare all five generated artifacts byte-for-byte in `--check` mode.

Unchanged inputs therefore produce byte-identical RU Markdown, EN Markdown, RU
HTML, EN HTML, and provenance outputs.

The PDF generator is a separate offline build step using ReportLab and pypdf.
It uses the same `build_blocks()` allowlist, fixed A4 layout, invariant PDF
metadata, fixed punctuation normalization, and a reviewed Unicode font pair.
Its manifest records the ReportLab version and exact SHA-256 hashes of the
regular and bold font bytes. Byte-identical PDF regeneration therefore requires
that recorded environment; the deployed PDF files have no runtime dependency.
The accepted Issue #55 build uses the bundled workspace Python runtime with
ReportLab 4.4.9, pypdf 6.10.0, and the bundled Ubuntu Regular/Bold font pair.
Visual QA uses Poppler 26.05.0 at 140 DPI. System Python is not assumed to
contain these build-time packages.

```powershell
python tools/build_public_cv_pdf.py --write
python tools/build_public_cv_pdf.py --check
```

## Selected Public Content

The current generated documents include only reviewed public-safe blocks:

- public identity;
- broad research focus;
- two current roles with point-in-time wording;
- three bounded education records;
- energy-auditor credential;
- the public AP22787517 project record;
- five selected publications;
- three patent records with dated legal status;
- four selected awards;
- two roadmap projects explicitly in development;
- ORCID, Scopus, and the public website/contact route.

The publication section is selected, not complete. Coauthor lists, citation
metrics, h-index, and completeness claims are omitted. Patent entries distinguish
historical inventor relationships from current legal status and omit termination
reasons and other-person metadata.

## Conflicting University Start Date

Official sources disagree on the university-role start date. The canonical
claim retains the employer-source value and the public source discrepancy, but
the CV renderer never reads or prints the claim's `since` value. Reconciliation
is deferred until the external Astana-Energy profile is corrected and rechecked;
it is not an active content task.

The generated role block includes role, organization, and point-in-time
currentness only. Its provenance contains the structured exclusion:

`start_date_omitted_due_to_source_conflict`

The knowledge validator rejects a generated current-role section that introduces
either disputed 2023 date.

## Credential Boundary

The general public energy-auditor status is supported by an official
institutional profile. The certified-energy-auditor wording and the current
certificate term, issued `2026-08-14` and valid until `2029-08-06`, come from a
sanitized review of owner-supplied private evidence and are not independently
verified through a public registry or issuer page. The
`professional_practice_since` value remains owner-approved within the same
`partially_verified` claim.

The generated credential block records the private-evidence limitation and the
following exclusions:

- certificate and accreditation identifiers;
- civil identifier;
- QR content;
- address;
- signature and seal;
- raw document, file name, and path.

When the generated CV includes `2010`, the corresponding provenance block also
records:

`professional_practice_since_is_owner_approved`

## Block-Level Provenance

`cv/IKurabayev_Public_CV_PROVENANCE.json` contains:

- `schema_version` and `cv_version`;
- `source_registry_sha256`;
- `source_graph_sha256`;
- `source_review_date`;
- generated document paths, languages, SHA-256 values, section IDs, and block
  IDs;
- an ordered `blocks[]` map from each presentation block to claim IDs, relation
  IDs, effective evidence statuses, exclusions, and limitation notes.

Every provenance block references at least one canonical claim. Russian and
English documents contain the same ordered section and block IDs. SHA-256 values
cover exact bytes for reproducibility; they are not a legal or digital
signature. The manifest intentionally does not contain its own hash because a
self-hash would be recursive.

`cv/IKurabayev_Public_CV_PDF_PROVENANCE.json` separately records the same input
hashes and review date, exact RU/EN PDF hashes, page counts, ordered section and
block IDs, ReportLab version, font filenames and hashes, portability limitation,
and PDF-specific privacy boundary. Machine-absolute font paths are never stored.

## No Manual Editing

Do not manually correct generated Markdown, HTML, PDF, or provenance files.
Instead:

1. update the canonical fact, relationship, or bounded renderer;
2. run `python tools/build_public_cv.py --write`;
3. review the generated diff;
4. run `python tools/build_public_cv.py --check` and the validators.

For PDF-affecting changes, also run the PDF generator with `--write`, render all
pages through Poppler, inspect every page, then run `--check`.

Manual output drift is rejected both by the generator and by provenance document
hash checks.

## Validation

Run:

```powershell
python tools/check_public_release.py
python tools/check_public_knowledge.py
python tools/check_public_knowledge.py --self-test
python tools/build_public_cv.py --check
python tools/build_public_cv_pdf.py --check
python -m json.tool data/public-facts.json
python -m json.tool data/public-research-graph.json
python -m json.tool cv/IKurabayev_Public_CV_PROVENANCE.json
python -m json.tool cv/IKurabayev_Public_CV_PDF_PROVENANCE.json
```

The knowledge validator checks IDs, evidence references, status inheritance,
topic and predicate contracts, privacy patterns, input/output hashes, block
coverage, RU/EN structure, disputed-date omission, dated patent status, roadmap
wording, and generated-file drift. Its self-test performs nine bounded in-memory
mutations, including manual PDF drift, and confirms that each is rejected
without changing the filesystem.

The Issue #55 visual QA renders both two-page A4 PDFs to PNG at 140 DPI and
reviews all four pages. The reviewed layout has no clipped text, overlap,
missing glyphs, broken section transition, form field, JavaScript, or unreadable
footer. Patent sections begin on page two in both languages to preserve heading
context.

## Human Review And Future Exports

Generation alone does not authorize publication. Factual currentness, language,
tone, and privacy must be reviewed before a generated route or download is
published.

The publication-readiness audit on 2026-08-22 checked RU/EN section parity,
block provenance, privacy exclusions, credential limitations, current-role date
handling, patent status wording, award translation mapping, and roadmap-only
project language. It corrected the bounded Russian award labels in the renderer
and the Russian provenance-footer terminology. The English CV intentionally
retains official Russian-language patent titles until approved English
translations exist.

The owner reviewed the corrected artifacts and delegated selection of public
formats. HTML remains the primary accessible, responsive, and indexable format.
Issue #55 adds PDF as a static professional-use download from the same canonical
block model; it does not replace HTML or become an evidence source.

DOCX and additional languages require separate approved tasks. Any future
export must consume the same canonical JSON and provenance model rather than
treating generated Markdown, HTML, or PDF as a new evidence source.

## Privacy And Runtime Boundary

The generated CV uses `https://ikurabayev.kz/` as the public professional contact
route and does not copy the approved mailbox. It includes no phone number,
personal email, private address, civil identifier, private source path, raw
document, other-person record, unpublished data, or confidential project detail.

The generators and validators are offline repository tools. The published HTML
and PDF contain no runtime JSON loading or runtime script and add no framework,
runtime dependency, backend, API, storage, analytics, tracking, network request,
or real-AI behavior.
