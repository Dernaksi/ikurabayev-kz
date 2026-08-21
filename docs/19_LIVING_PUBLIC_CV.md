# Living Public CV

## Purpose

The Living Public CV is a deterministic, sanitized presentation derived from
the reviewed public facts and relationship graph. It provides equivalent
Russian and English Markdown drafts without making those drafts the canonical
source of truth.

Canonical facts remain in `data/public-facts.json`. Canonical relationships
remain in `data/public-research-graph.json`. Generated CV files must never be
edited as independent source material.

## Inputs And Outputs

Generator:

- `tools/build_public_cv.py`

Exact inputs:

- `data/public-facts.json`
- `data/public-research-graph.json`

Generated outputs:

- `cv/IKurabayev_Public_CV_RU.md`
- `cv/IKurabayev_Public_CV_EN.md`
- `cv/IKurabayev_Public_CV_PROVENANCE.json`

The outputs are public drafts for human review. They are not deployed under
`site/`, not advertised as a download, and not automatically published.

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
- compare all three generated artifacts byte-for-byte in `--check` mode.

Unchanged inputs therefore produce byte-identical RU, EN, and provenance
outputs.

## Selected Public Content

The current generated drafts include only reviewed public-safe blocks:

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
claim retains that conflict for review, but the CV renderer never reads or
prints the claim's `since` value.

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

## No Manual Editing

Do not manually correct generated Markdown or provenance files. Instead:

1. update the canonical fact, relationship, or bounded renderer;
2. run `python tools/build_public_cv.py --write`;
3. review the generated diff;
4. run `python tools/build_public_cv.py --check` and the validators.

Manual output drift is rejected both by the generator and by provenance document
hash checks.

## Validation

Run:

```powershell
python tools/check_public_release.py
python tools/check_public_knowledge.py
python tools/check_public_knowledge.py --self-test
python tools/build_public_cv.py --check
python -m json.tool data/public-facts.json
python -m json.tool data/public-research-graph.json
python -m json.tool cv/IKurabayev_Public_CV_PROVENANCE.json
```

The knowledge validator checks IDs, evidence references, status inheritance,
topic and predicate contracts, privacy patterns, input/output hashes, block
coverage, RU/EN structure, disputed-date omission, dated patent status, roadmap
wording, and generated-file drift. Its self-test performs eight bounded in-memory
mutations and confirms that each is rejected without changing the filesystem.

## Human Review And Future Exports

Generation does not authorize publication. A human must review factual
currentness, language, tone, and privacy before any CV is linked from the site or
offered as a download.

PDF, DOCX, print styling, website integration, and additional languages require
separate approved tasks. Any future export should consume the same canonical
JSON and provenance model rather than treating a generated Markdown file as the
new evidence source.

## Privacy And Runtime Boundary

The generated CV uses `https://ikurabayev.kz/` as the public professional contact
route and does not copy the approved mailbox. It includes no phone number,
personal email, private address, civil identifier, private source path, raw
document, other-person record, unpublished data, or confidential project detail.

The generator and validators are offline repository tools. They add no website
runtime loading, framework, dependency, backend, API, storage, analytics,
tracking, network request, or real-AI behavior.
