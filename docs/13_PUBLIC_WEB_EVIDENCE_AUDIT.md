# Public Web Evidence Audit v0.5

## Purpose

This document records the public web evidence reviewed for IKurabayev.kz v0.5.
It supports source-backed profile wording without turning the website into a
full CV, citation dump, or unreviewed claims page.

The audit separates:

- verified public sources;
- owner-provided or repository-provided facts that are not externally verified;
- source candidates requiring review;
- excluded private data.

## Search strategy

The audit used direct public URLs first, then limited public search for official
profile, publication, patent, and technical-context sources. Search snippets
were not treated as evidence unless the linked page could be opened and checked.

PR #22 was checked before this work and was already merged into `main`, so this
branch was based on the latest `main`.

## Name variants searched

- Iskander Kurabayev
- Iskander K. Kurabayev
- I. Kurabayev
- Kurabayev I.K.
- Курабаев Искандер
- Курабаев Искандер Казбекович
- Курабаев И.К.

## Verified public profile links

| Source | Status | Evidence | Website implication |
| --- | --- | --- | --- |
| ORCID | Verified public source | `https://orcid.org/0000-0002-4331-4726` opened and the public ORCID API returned display name `Iskander Kurabayev`. Public keywords and public employment / education entries were visible. | Keep ORCID as a public profile link. Do not infer publication completeness, current role, metrics, or affiliation status. |
| Scopus Author ID | Verified public source | `https://www.scopus.com/authid/detail.uri?authorId=57473761100` opened and page content contained `Kurabayev` and `57473761100`. | Keep Scopus Author ID as a public profile link. Do not publish citation counts, h-index, affiliation claims, or completeness claims. |
| University profile | Verified public source with privacy exclusions | `https://kazatu.edu.kz/en/facultet/kurabaev-iskander-kazbekovic` opened and matched `Iskander Kazbekovich Kurabayev`. It also exposed research interests, selected publications, and patent references. | May support broad research-topic wording. Do not copy contact details. Current role wording still needs human review before strengthening website claims. |

## Publication metadata verification

| Work | Public source | Verified metadata | Status | Notes |
| --- | --- | --- | --- | --- |
| Mathematical description of the method for ungrounded AC systems to determine the network insulation | `https://doi.org/10.1049/gtd2.12436` and Crossref metadata | Title, venue `IET Generation, Transmission & Distribution`, year 2022, DOI, and author list including Iskander Kurabayev. | Verified public source | DOI landing access varied, but Crossref metadata resolved. |
| Experimental research of the developed method to determine the network insulation for ungrounded AC systems in laboratory conditions | `https://doi.org/10.1109/ICECET55527.2022.9873012` and Crossref metadata | Title, venue `2022 International Conference on Electrical, Computer and Energy Technologies (ICECET)`, year 2022, DOI, and author list including Iskander Kurabayev. | Verified public source | DOI resolved to IEEE Xplore with HTTP 202 during this audit. |
| Approbation of the developed method for determining network insulation parameters on an operating excavator | `https://doi.org/10.48081/YIUH4401` and Crossref metadata | Title, venue `Bulletin of Toraighyrov University. Energetics series`, year 2023, DOI, and author list including I. K. Kurabayev. | Verified public source | Metadata title contained extra quotation / spacing; website keeps readable title. |
| Error estimation of the developed method for ungrounded AC systems to determine the network insulation | `https://doi.org/10.52167/1609-1817-2023-125-2-428-436` and Crossref metadata | Title, venue `Вестник КазАТК`, year 2023, DOI, and author list including Iskander Kurabayev. | Verified public source | Avoid copying coauthor spelling variants into website copy unless needed. |
| Experimental studies of a developed method for determining the insulation parameters in a network with isolated neutral voltage up to 1000 V | `https://bulletinofscience.kazatu.edu.kz/index.php/bulletinofscience/article/view/293` | Public article page, title, venue `Eurasian Agrotechnical Journal`, and author metadata including I.K. Kurabayev. | Verified public source | Extracted citation metadata did not expose a reliable year field in this audit. |

## Patent registry verification status

| Item | Public source status | Result | Website implication |
| --- | --- | --- | --- |
| Eurasian patent EA041128B1 | Public Google Patents page opened: `https://patents.google.com/patent/EA041128B1/en` | Page title matched a method for measuring insulation parameters of electric networks with insulated neutral voltage up to and above 1000 V with account of quadrants of the complex plane. | Keep cautious patent-topic wording. Treat Google Patents as a public source candidate unless / until official registry details are reviewed. |
| Kazakhstan patent 35922 RK | Direct Google Patents lookup `https://patents.google.com/patent/KZ35922B/en` returned 404. Official registry page was not verified in this pass. | University profile mentions patent 35922 RK, but direct registry verification remains pending. | Keep `registry verification pending`; do not present a complete verified patent portfolio. |

## University / current role verification status

An official university profile page was found and opened:

`https://kazatu.edu.kz/en/facultet/kurabaev-iskander-kazbekovic`

The page matched `Iskander Kazbekovich Kurabayev` and contained public research
interests connected with insulation parameters in ungrounded systems and energy
efficiency in industrial power systems. It also listed teaching disciplines,
publications, and patent references.

Current role wording should remain cautious until a human review confirms the
exact public role field and desired website wording. The page also includes
contact details; those fields are excluded from this repository and website.

## Technical-context sources for Neutral Shift Lab

These sources support design/context language only. They are not evidence of
personal achievement, patent ownership, current role, or project results.

| Source | URL | Context supported |
| --- | --- | --- |
| Earthing system | `https://en.wikipedia.org/wiki/Earthing_system` | Public context for isolated-neutral / ungrounded systems and ground-fault behavior. |
| Electrical fault | `https://en.wikipedia.org/wiki/Electrical_fault` | Public context for earth / ground fault as an abnormal electrical condition. |
| Symmetrical components | `https://en.wikipedia.org/wiki/Symmetrical_components` | Public context for sequence-component language used in fault analysis. |
| University profile research areas | `https://kazatu.edu.kz/en/facultet/kurabaev-iskander-kazbekovic` | Public context that the reviewed identity page uses insulation parameters, ungrounded AC systems, capacitive currents, relay protection, and electrical safety language. |

Some candidate pages and PDFs were unavailable or blocked during this audit and
were not used as evidence.

## Search noise / disambiguation notes

- Public search returned ORCID, Scopus, IEEE Xplore, ResearchGate, and the
  official university profile as visible identity candidates.
- ResearchGate and IEEE author pages were not used for new website claims in
  this pass because ORCID, Scopus, DOI / Crossref, publisher pages, and the
  university page were enough for the cautious profile layer.
- Patent search was incomplete: one Eurasian Google Patents page opened, while a
  direct Kazakhstan patent page did not.
- Search result snippets were not copied as claims.

## Excluded/private data

The following must not be published or copied into the website:

- date of birth;
- private address;
- phone number;
- private email address;
- WhatsApp / Telegram;
- IIN or civil identifiers;
- document, diploma, certificate, attestation, or membership numbers;
- signatures, seals, QR / EDS blocks;
- contracts, financial records, client names, private facility details;
- unpublished research data or confidential manuscript content;
- citation counts, h-index, unsupported affiliation claims, or unsupported
  product claims.

## Recommended website updates

- Keep ORCID and Scopus links visible as public profile links.
- Add a compact public-evidence note under profile links on English and Russian
  profile pages.
- Mark DOI-linked selected works as DOI-metadata verified without adding raw
  footnotes or metrics.
- Keep patent language cautious and retain registry-verification-pending wording.
- Keep the QR page compact, with a short note that ORCID, Scopus, and
  DOI-linked works are available from the profile path.

## Remaining risks

- Official patent registry verification is still incomplete for the Kazakhstan
  patent.
- Current university role wording requires human review before it is used as a
  stronger public claim.
- The earlier 2019 article page is public and identity-matched, but the checked
  metadata did not expose a reliable publication year field.
- The website still needs approved public contact routing before launch.
