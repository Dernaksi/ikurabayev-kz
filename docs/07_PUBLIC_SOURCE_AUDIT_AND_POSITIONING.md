# Public Source Audit And Positioning

## Purpose

This document is a conservative source-audit and positioning skeleton for
IKurabayev.kz. It is intended to help review public or explicitly approved
sources before QR landing page information architecture, homepage positioning,
visual style, or website implementation decisions are made.

This file must not become final biography text, final homepage copy, final
website branding, or a list of unverified claims. Add facts only when they are
grounded in public or explicitly approved sources and have been reviewed for
privacy and identity confidence.

## Source Status Legend

| Status | Meaning | Publication readiness |
| --- | --- | --- |
| `placeholder` | Structure exists, but content is not supplied yet. | Not ready |
| `source candidate` | A possible source category or source is identified but not verified. | Not ready |
| `needs public source` | A fact or claim requires public or explicitly approved evidence. | Not ready |
| `approved public source` | The source is public and reviewed for use. | Review before publication |
| `approved by owner` | The repository owner explicitly approved the fact or source for use. | Review before publication |
| `excluded` | The item must not be published or stored here. | Do not publish |
| `needs human review` | Human review is required before use. | Not ready |

Source type examples may include official university profile, ORCID, Scopus
Author ID, Web of Science profile, Google Scholar profile, DOI / publisher page,
conference proceedings page, patent database record, official grant/project
page, public GitHub repository, or explicitly approved owner-provided source.
These categories are not approved sources until the specific source is reviewed.

## Public Web Evidence Audit v0.5

This section records source-backed public evidence reviewed for the v0.5 profile
layer. It separates public verification from owner-provided facts, source
candidates, and excluded private data. It must not be read as a complete CV,
publication list, patent portfolio, or affiliation record.

| Source | URL | What it verifies | Identity confidence | Publication readiness | Website use | Risks / notes |
| --- | --- | --- | --- | --- | --- | --- |
| ORCID profile | https://orcid.org/0000-0002-4331-4726 | Display name `Iskander Kurabayev`, public ORCID URL, public keywords, and public employment / education entries visible through the ORCID public record. | `exact match` | `verified public source` | Keep as public profile link and evidence note. | Do not infer publication completeness, current role, metrics, or affiliation status from ORCID alone. |
| Scopus Author ID | https://www.scopus.com/authid/detail.uri?authorId=57473761100 | Public author profile URL containing `Kurabayev` and Author ID `57473761100`. | `exact match` | `verified public source` | Keep as public profile link. | Do not publish citation counts, h-index, affiliation claims, or completeness claims. |
| DOI / Crossref metadata: IET GTD | https://doi.org/10.1049/gtd2.12436 | 2022 publication title, venue, DOI, and author list including Iskander Kurabayev. | `exact match` | `verified public source` | Mark selected work as DOI-metadata verified. | DOI landing page access varied, but Crossref metadata resolved and is sufficient for a cautious selected-work label. |
| DOI / Crossref metadata: ICECET 2022 | https://doi.org/10.1109/ICECET55527.2022.9873012 | 2022 conference paper title, venue, DOI, and author list including Iskander Kurabayev. | `exact match` | `verified public source` | Mark selected work as DOI-metadata verified. | DOI resolved to IEEE Xplore with HTTP 202; no metrics should be copied. |
| DOI / Crossref metadata: Toraighyrov University bulletin | https://doi.org/10.48081/YIUH4401 | 2023 article title, venue, DOI, and author list including I. K. Kurabayev. | `exact match` | `verified public source` | Mark selected work as DOI-metadata verified. | Title punctuation differs slightly across metadata; keep website title readable and cautious. |
| DOI / Crossref metadata: Vestnik KazATC | https://doi.org/10.52167/1609-1817-2023-125-2-428-436 | 2023 article title, venue, DOI, and author list including Iskander Kurabayev. | `exact match` | `verified public source` | Mark selected work as DOI-metadata verified. | Author spelling varies in metadata (`Tatkeeva` / `Tatkeyeva`); avoid unnecessary coauthor detail on the website. |
| Earlier article page | https://bulletinofscience.kazatu.edu.kz/index.php/bulletinofscience/article/view/293 | Public article page with title, venue `Eurasian Agrotechnical Journal`, and author metadata including I.K. Kurabayev. | `exact match` | `verified public source` | Keep as selected work; avoid overloading public page with raw metadata. | Extracted metadata did not expose a reliable publication date in the checked fields. |
| University profile | https://kazatu.edu.kz/en/facultet/kurabaev-iskander-kazbekovic | Official university page matching `Iskander Kazbekovich Kurabayev`, research interests in insulation parameters of ungrounded systems, energy efficiency, selected publications, and patent references. | `exact match` | `verified public source` | May support broad research-topic wording and future source-backed profile notes. | Page contains contact details; do not copy phone, private email, office, address, or other private-contact fields into the repo or site. Current role wording still needs human review before strengthening website claims. |
| Eurasian patent Google Patents page | https://patents.google.com/patent/EA041128B1/en | Public Google Patents page for EA041128B1 on measuring insulation parameters of electric networks with insulated neutral using complex-plane quadrants. | `exact match` for topic; inventor identity requires full record review | `public source candidate` | Keep patent wording cautious; cite in docs only until full review. | The task asked for registry verification; Google Patents is public but secondary to the official register. |
| Kazakhstan patent KZ35922B direct lookup | https://patents.google.com/patent/KZ35922B/en | Direct Google Patents URL returned 404 during this audit. | `uncertain` | `not found` | Keep registry verification pending. | University page mentions patent 35922 RK, but a direct public registry page was not verified in this pass. |
| Technical context: earthing systems | https://en.wikipedia.org/wiki/Earthing_system | Context for isolated-neutral / ungrounded system behavior and ground-fault conditions. | N/A | `verified public source` | Documentation context only for Neutral Shift Lab visual language. | Not a personal-achievement source. |
| Technical context: electrical fault | https://en.wikipedia.org/wiki/Electrical_fault | Context for earth / ground fault as an abnormal electrical condition. | N/A | `verified public source` | Documentation context only. | Not a personal-achievement source. |
| Technical context: symmetrical components | https://en.wikipedia.org/wiki/Symmetrical_components | Context for sequence components and ground-fault analysis language. | N/A | `verified public source` | Documentation context only. | Not a personal-achievement source; do not use as support for patent ownership. |
| Private contact and civil data | N/A | Date of birth, private address, private phone, private email, civil identifiers, document numbers, contracts, private facility details, and unpublished data. | N/A | `excluded/private` | Do not publish. | Excluded even if encountered on a public-looking page unless explicitly approved and public-safe. |

## Identity Confidence Legend

| Identity confidence | Meaning | Required action |
| --- | --- | --- |
| `exact match` | The source clearly matches the reviewed public identity. | Review source and privacy status before use. |
| `probable match` | The source likely matches but needs confirmation. | Do not publish until reviewed. |
| `uncertain` | The match is ambiguous. | Keep separate from verified facts. |
| `not same person` | The source refers to another person. | Exclude from public claims. |
| `needs human review` | Identity confidence has not been assessed. | Human review required. |

## Approved Name Variants

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cyrillic full name | Курабаев Искандер Казбекович | Needs approved source | explicitly approved owner-provided source | `needs human review` | `needs public source` | Needs review | May affect multilingual identity display. | Confirm spelling, transliteration, and publication preference. |
| English display name | Iskander Kurabayev | Needs approved source | explicitly approved owner-provided source | `needs human review` | `needs public source` | Needs review | May be primary public display name. | Confirm preferred public form before use. |
| English full patronymic form | Iskander Kazbekovich Kurabayev | Needs approved source | explicitly approved owner-provided source | `needs human review` | `needs public source` | Needs review | May help source matching. | Confirm whether this form should appear publicly. |
| English initials form | Kurabayev I.K. | Needs approved source | publication metadata candidate | `needs human review` | `needs public source` | Needs review | May help publication disambiguation. | Do not link to publications until identity is verified. |
| Cyrillic initials form | Курабаев И.К. | Needs approved source | publication metadata candidate | `needs human review` | `needs public source` | Needs review | May help Cyrillic source matching. | Do not link to publications until identity is verified. |

## Verified Public Identity

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Public identity summary | Placeholder only | Needs public or owner-approved source | explicitly approved owner-provided source | `needs human review` | `placeholder` | Needs review | Establishes baseline identity for the site. | Do not draft final biography here. |
| Public affiliation wording | Placeholder only | Needs public or owner-approved source | official university profile | `needs human review` | `needs public source` | Needs review | May influence homepage credibility and audience framing. | Confirm currentness and public-safe wording. |
| Public contact route | Placeholder only | Needs approved public route | explicitly approved owner-provided source | `needs human review` | `needs human review` | Needs review | May affect QR landing page routing. | Do not add private phone numbers or private addresses. |

## Public Academic Profile Links

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORCID profile | ORCID 0000-0002-4331-4726, https://orcid.org/0000-0002-4331-4726 | Owner-approved QR profile link | ORCID | `exact match` | `approved by owner` | Yes | Supports research identity and QR profile routing. | Approved for QR use; do not infer publication completeness or metrics. |
| Scopus author profile | Scopus Author ID 57473761100, https://www.scopus.com/authid/detail.uri?authorId=57473761100 | Owner-approved QR profile link | Scopus Author ID | `exact match` | `approved by owner` | Yes | Supports publication-audit routing from the QR profile. | Approved for QR use; do not claim publication completeness, citation counts, h-index, affiliations, or metrics. |
| Web of Science profile | Placeholder only | Needs verified profile URL | Web of Science profile | `needs human review` | `source candidate` | Needs review | May support publication audit. | Confirm author identity and publication set. |
| Google Scholar profile | Placeholder only | Needs verified profile URL | Google Scholar profile | `needs human review` | `source candidate` | Needs review | May support research overview. | Confirm profile ownership and publication set. |
| University profile | Placeholder only | Needs verified profile URL | official university profile | `needs human review` | `source candidate` | Needs review | May support affiliation wording. | Confirm currentness before use. |

## Publication Source Candidates

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOI-backed publication | Placeholder only | Needs DOI or publisher page | DOI / publisher page | `needs human review` | `source candidate` | Needs review | May support research positioning. | Verify author identity before adding title or claim. |
| Conference publication | Placeholder only | Needs proceedings page | conference proceedings page | `needs human review` | `source candidate` | Needs review | May support research and speaking context. | Confirm proceedings are public and linked to the same person. |
| Publication list entry | Placeholder only | Needs public source | DOI / publisher page | `needs human review` | `needs public source` | Needs review | May inform research page structure. | Do not fabricate titles, dates, coauthors, or metrics. |

## Patent Source Candidates

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Patent database record | Placeholder only | Needs verified patent record | patent database record | `needs human review` | `source candidate` | Needs review | May support applied engineering positioning. | Verify inventor identity before adding any patent claim. |
| Patent title or topic | Placeholder only | Needs verified patent record | patent database record | `needs human review` | `needs public source` | Needs review | May inform portfolio or research summaries. | Do not add titles or topics until verified. |

## Public Engineering And Project Fact Candidates

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Public engineering project | Placeholder only | Needs public or owner-approved source | public GitHub repository | `needs human review` | `source candidate` | Needs review | May support engineering portfolio framing. | Exclude private clients, confidential systems, and unsupported metrics. |
| Open-source repository | Placeholder only | Needs reviewed public repository URL | public GitHub repository | `needs human review` | `source candidate` | Needs review | May support implementation credibility. | Confirm repository is intended for public sharing. |
| Public project page | Placeholder only | Needs verified public project page | official grant/project page | `needs human review` | `source candidate` | Needs review | May support collaboration context. | Confirm source scope and privacy status. |

## Energy Audit / Engineering Practice Source Candidates

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Energy audit practice | Placeholder only | Needs public or owner-approved source | explicitly approved owner-provided source | `needs human review` | `needs public source` | Needs review | Possible homepage positioning hypothesis. | Do not add client names, private sites, contracts, or financial details. |
| Engineering practice area | Placeholder only | Needs public or owner-approved source | explicitly approved owner-provided source | `needs human review` | `needs public source` | Needs review | May affect QR landing page audience. | Keep generic until evidence is reviewed. |

## AI Lab / Website Positioning Notes

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI Lab repository role | Repository as AI-assisted project laboratory | Repository documents | repository governance document | `exact match` | `approved public source` | Yes | Supports positioning the site-building process as reviewable and provenance-aware. | Keep wording tied to repository purpose, not personal claims. |
| Website source of truth | Repository for personal research website and portfolio | Repository documents | repository governance document | `exact match` | `approved public source` | Yes | Supports public website governance framing. | Avoid expanding this into unsupported biography. |
| Content review workflow | Issue to branch to PR workflow | Repository documents | repository governance document | `exact match` | `approved public source` | Yes | Supports conservative publication process. | Keep as process claim only. |

## Facts Requiring Evidence

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Biography claim | Placeholder only | Needs public or owner-approved source | explicitly approved owner-provided source | `needs human review` | `needs public source` | Needs review | May affect homepage headline and summary. | Do not publish without evidence. |
| Affiliation claim | Placeholder only | Needs verified public source | official university profile | `needs human review` | `needs public source` | Needs review | May affect research positioning. | Confirm currentness before use. |
| Publication claim | Placeholder only | Needs verified public source | DOI / publisher page | `needs human review` | `needs public source` | Needs review | May affect research credibility. | Verify metadata and identity. |
| Patent claim | Placeholder only | Needs verified public source | patent database record | `needs human review` | `needs public source` | Needs review | May affect applied engineering positioning. | Verify inventor identity. |
| Engineering achievement claim | Placeholder only | Needs public or owner-approved source | explicitly approved owner-provided source | `needs human review` | `needs public source` | Needs review | May affect portfolio positioning. | Do not invent metrics or outcomes. |

## Facts Excluded For Privacy

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Private phone numbers | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Private addresses | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Secrets, tokens, and `.env` files | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Contracts and financial records | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Private correspondence | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Unpublished research data | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Raw datasets | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Confidential manuscripts | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Keep out of repository and website. |
| Unsupported public claims | Do not publish | Repository policy | repository governance document | N/A | `excluded` | No | Not applicable | Require public or explicitly approved evidence. |

## Search Noise And Disambiguation Notes

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ambiguous search result | Placeholder only | Needs verification | source candidate | `uncertain` | `needs human review` | Needs review | Prevents accidental misattribution. | Keep separate from verified identity matches. |
| Unrelated person result | Placeholder only | Needs verification if relevant | source candidate | `not same person` | `excluded` | No | Prevents false claims. | Do not add unrelated person details unless necessary for disambiguation. |
| Name variant collision | Placeholder only | Needs verification | source candidate | `uncertain` | `needs human review` | Needs review | May affect publication and patent searches. | Record only reviewed disambiguation notes. |

## Style Implications

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Research-forward style | Hypothesis only | Needs reviewed content inventory | owner review | `needs human review` | `needs human review` | Needs review | Could emphasize research credibility and source traceability. | Decide only after public source audit is populated. |
| Engineering-practice style | Hypothesis only | Needs reviewed content inventory | owner review | `needs human review` | `needs human review` | Needs review | Could emphasize practical engineering work. | Avoid unsupported project or client claims. |
| AI Lab process style | Hypothesis only | Repository workflow supports process framing | repository governance document | `exact match` | `needs human review` | Needs review | Could make provenance and AI-assisted workflow visible. | Keep process-focused, not self-promotional. |
| QR-first compact style | Hypothesis only | Needs QR landing page review | owner review | `needs human review` | `needs human review` | Needs review | Could support fast scanning from events or cards. | Decide after approved public links are known. |

## Homepage Positioning Options

These options are review hypotheses only. They are not final homepage claims.

| Item | Candidate public fact | Source / evidence | Source type | Identity confidence | Status | Public-safe? | Positioning implication | Notes / next review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Research engineer | Positioning hypothesis only | Needs public or owner-approved evidence | owner review | `needs human review` | `needs human review` | Needs review | Possible broad homepage framing. | Do not use as final title until approved. |
| Electrical power systems diagnostics | Positioning hypothesis only | Needs public or owner-approved evidence | owner review | `needs human review` | `needs human review` | Needs review | Possible research/engineering focus. | Verify scope and wording before use. |
| Insulation diagnostics | Positioning hypothesis only | Needs public or owner-approved evidence | owner review | `needs human review` | `needs human review` | Needs review | Possible technical focus. | Verify scope and wording before use. |
| Energy audit and engineering practice | Positioning hypothesis only | Needs public or owner-approved evidence | owner review | `needs human review` | `needs human review` | Needs review | Possible applied practice focus. | Do not add client, contract, or financial details. |
| AI-assisted engineering workflows | Positioning hypothesis only | Needs public or owner-approved evidence | owner review | `needs human review` | `needs human review` | Needs review | Possible AI Lab / engineering bridge. | Keep claims source-backed and concrete. |
| Personal AI Lab | Positioning hypothesis only | Repository documents describe AI-assisted project laboratory | repository governance document | `exact match` | `needs human review` | Needs review | Possible process and provenance framing. | Review tone before public use. |

## Review Checklist

- [ ] PR #5 is merged before implementing this document.
- [ ] All identity and name variant entries have reviewed sources before
      publication.
- [ ] Publication, patent, academic profile, and project references are verified
      before being treated as approved.
- [ ] Search noise and unrelated persons are separated from verified identity
      matches.
- [ ] No private phone numbers, private addresses, secrets, tokens, `.env`
      files, private correspondence, contracts, financial records, unpublished
      research data, raw datasets, or confidential manuscripts are included.
- [ ] No unsupported biography, publication, affiliation, patent, research,
      engineering, energy-audit, or portfolio claims are introduced.
- [ ] Homepage positioning options remain hypotheses until reviewed and
      approved.
- [ ] QR landing page information architecture and website style are decided
      only after this audit is reviewed.
