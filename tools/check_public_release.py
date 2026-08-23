#!/usr/bin/env python3
"""Validate the bounded truth, privacy, and semantic contract for the public site."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REGISTRY = ROOT / "data" / "public-facts.json"
CANONICAL_HOST = "ikurabayev.kz"
OG_IMAGE = "https://ikurabayev.kz/assets/og-image.png"
SITEMAP_URL = "https://ikurabayev.kz/sitemap.xml"

ROUTES = {
    "/": (SITE / "index.html", "https://ikurabayev.kz/"),
    "/ru/": (SITE / "ru" / "index.html", "https://ikurabayev.kz/ru/"),
    "/en/": (SITE / "en" / "index.html", "https://ikurabayev.kz/en/"),
    "/kk/": (SITE / "kk" / "index.html", "https://ikurabayev.kz/kk/"),
    "/qr/": (SITE / "qr" / "index.html", "https://ikurabayev.kz/qr/"),
}
CV_ROUTES = {
    "/cv/": (
        SITE / "cv" / "index.html",
        "https://ikurabayev.kz/cv/",
        "ru",
    ),
    "/en/cv/": (
        SITE / "en" / "cv" / "index.html",
        "https://ikurabayev.kz/en/cv/",
        "en",
    ),
}
PDF_EXPORTS = {
    "/cv/": (
        SITE / "output" / "pdf" / "IKurabayev_Public_CV_RU.pdf",
        "/output/pdf/IKurabayev_Public_CV_RU.pdf",
        "Скачать PDF",
    ),
    "/en/cv/": (
        SITE / "output" / "pdf" / "IKurabayev_Public_CV_EN.pdf",
        "/output/pdf/IKurabayev_Public_CV_EN.pdf",
        "Download PDF",
    ),
}
PROFILE_ROUTES = {"/", "/ru/", "/en/", "/kk/"}
HREFLANG = {
    "ru": "https://ikurabayev.kz/ru/",
    "en": "https://ikurabayev.kz/en/",
    "kk": "https://ikurabayev.kz/kk/",
    "x-default": "https://ikurabayev.kz/",
}
CV_HREFLANG = {
    "ru": "https://ikurabayev.kz/cv/",
    "en": "https://ikurabayev.kz/en/cv/",
    "x-default": "https://ikurabayev.kz/cv/",
}
PATENTS = {
    "patent.ea041128": ("not_in_force", "source.eapo.patent_041128"),
    "patent.kz35922": ("not_in_force", "source.qazpatent.patent_35922"),
    "patent.kz37923": ("active", "source.qazpatent.patent_37923"),
}
CREDENTIAL_SOURCE_ID = "source.owner_supplied.energy_auditor_certificate_review"
KAZAKH_IDENTITY_SOURCE_ID = "source.owner_approval.kazakh_display_name"
KAZAKH_FULL_NAME = "Қорабаев Ескендір Қазбекұлы"
PUBLIC_TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".svg", ".txt", ".xml"}
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class PageParser(HTMLParser):
    """Collect only the source-level facts needed by this release contract."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.meta: dict[str, list[str]] = defaultdict(list)
        self.script_srcs: list[str] = []
        self.json_ld_text: list[str] = []
        self.visible_parts: list[str] = []
        self.patent_cards: list[dict[str, object]] = []
        self._json_buffer: list[str] | None = None
        self._hidden_depth = 0
        self._patent_depth = 0
        self._patent_parts: list[str] = []
        self._patent_anchors: list[dict[str, str]] = []

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key: value or "" for key, value in attrs}

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = self._attrs(attrs)
        classes = set(values.get("class", "").split())
        if self._patent_depth:
            if tag not in VOID_TAGS:
                self._patent_depth += 1
        elif tag == "article" and "patent-item" in classes:
            self._patent_depth = 1
            self._patent_parts = []
            self._patent_anchors = []
        if tag == "link":
            self.links.append(values)
        elif tag == "meta":
            key = values.get("property") or values.get("name")
            if key:
                self.meta[key].append(values.get("content", ""))
        elif tag == "a":
            self.anchors.append(values)
            if self._patent_depth:
                self._patent_anchors.append(values)
        elif tag == "script":
            if values.get("src"):
                self.script_srcs.append(values["src"])
            if values.get("type", "").lower() == "application/ld+json":
                self._json_buffer = []
            self._hidden_depth += 1
        elif tag == "style":
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            if self._json_buffer is not None:
                self.json_ld_text.append("".join(self._json_buffer))
                self._json_buffer = None
            self._hidden_depth = max(0, self._hidden_depth - 1)
        elif tag == "style":
            self._hidden_depth = max(0, self._hidden_depth - 1)
        if self._patent_depth:
            self._patent_depth -= 1
            if self._patent_depth == 0:
                self.patent_cards.append(
                    {
                        "text": " ".join(" ".join(self._patent_parts).split()),
                        "anchors": self._patent_anchors,
                    }
                )

    def handle_data(self, data: str) -> None:
        if self._json_buffer is not None:
            self._json_buffer.append(data)
        elif self._hidden_depth == 0:
            self.visible_parts.append(data)
        if self._patent_depth and self._hidden_depth == 0:
            self._patent_parts.append(data)

    @property
    def visible_text(self) -> str:
        return " ".join(" ".join(self.visible_parts).split())


errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def unique_index(items: object, label: str) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    if not isinstance(items, list):
        fail(f"Evidence Spine {label} must be an array")
        return result
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            fail(f"Evidence Spine {label} contains an item without a string id")
            continue
        item_id = item["id"]
        if item_id in result:
            fail(f"Evidence Spine has duplicate {label} id: {item_id}")
        result[item_id] = item
    return result


def parse_page(route: str, path: Path) -> PageParser:
    parser = PageParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as exc:
        fail(f"{route}: cannot read HTML: {exc}")
    return parser


def one_meta(parser: PageParser, route: str, key: str) -> str:
    values = parser.meta.get(key, [])
    if len(values) != 1 or not values[0]:
        fail(f"{route}: expected one non-empty {key} meta value")
        return ""
    return values[0]


def validate_evidence() -> tuple[
    dict[str, dict[str, object]], dict[str, dict[str, object]], dict[str, str]
]:
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"Evidence Spine is not valid readable JSON: {exc}")
        return {}, {}, {}

    claims = unique_index(registry.get("claims"), "claims")
    sources = unique_index(registry.get("sources"), "sources")

    for claim_id, claim in claims.items():
        evidence = claim.get("evidence", [])
        if not isinstance(evidence, list):
            fail(f"{claim_id}: evidence must be an array")
            continue
        for source_id in evidence:
            if source_id not in sources:
                fail(f"{claim_id}: unresolved evidence reference {source_id}")

    identity = claims.get("identity.name", {})
    identity_value = identity.get("value")
    if identity.get("status") != "partially_verified":
        fail("identity.name: mixed public and owner evidence must remain partially_verified")
    if not isinstance(identity_value, dict) or identity_value.get("kk_full_name") != KAZAKH_FULL_NAME:
        fail("identity.name: approved Kazakh full name is missing or changed")
    if KAZAKH_IDENTITY_SOURCE_ID not in identity.get("evidence", []):
        fail("identity.name: Kazakh owner-approval evidence is missing")
    identity_source = sources.get(KAZAKH_IDENTITY_SOURCE_ID, {})
    if identity_source.get("kind") != "owner_approval":
        fail(f"{KAZAKH_IDENTITY_SOURCE_ID}: unexpected source kind")
    if "url" in identity_source:
        fail(f"{KAZAKH_IDENTITY_SOURCE_ID}: owner approval must not have a URL")

    official_urls: dict[str, str] = {}
    for claim_id, (legal_status, source_id) in PATENTS.items():
        claim = claims.get(claim_id)
        if not claim:
            fail(f"Missing required patent claim: {claim_id}")
            continue
        value = claim.get("value")
        if claim.get("status") != "verified_public" or claim.get("public") is not True:
            fail(f"{claim_id}: expected public verified_public evidence state")
        if not isinstance(value, dict):
            fail(f"{claim_id}: value must be an object")
            continue
        if value.get("legal_status") != legal_status:
            fail(f"{claim_id}: expected legal_status {legal_status}")
        if value.get("legal_status_checked_at") != "2026-08-09":
            fail(f"{claim_id}: expected legal-status check date 2026-08-09")
        if source_id not in claim.get("evidence", []):
            fail(f"{claim_id}: missing official registry evidence {source_id}")
        source = sources.get(source_id)
        if not source or source.get("kind") != "official_patent_registry":
            fail(f"{source_id}: missing official patent-registry source")
            continue
        url = source.get("url")
        if not isinstance(url, str) or urlparse(url).scheme != "https":
            fail(f"{source_id}: expected a public HTTPS registry URL")
        else:
            official_urls[claim_id] = url

    credential = claims.get("credential.energy_auditor", {})
    credential_value = credential.get("value")
    if credential.get("status") != "partially_verified":
        fail("credential.energy_auditor: status must remain partially_verified")
    if not isinstance(credential_value, dict):
        fail("credential.energy_auditor: value must be an object")
    else:
        expected_credential = {
            "credential": "Certified energy auditor",
            "practice_area": "energy saving and energy efficiency improvement",
            "certificate_issued_on": "2026-08-14",
            "certificate_valid_until": "2029-08-06",
        }
        for key, expected in expected_credential.items():
            if credential_value.get(key) != expected:
                fail(f"credential.energy_auditor: expected {key} {expected}")
    if CREDENTIAL_SOURCE_ID not in credential.get("evidence", []):
        fail("credential.energy_auditor: sanitized term evidence is missing")
    credential_source = sources.get(CREDENTIAL_SOURCE_ID, {})
    if credential_source.get("kind") != "owner_supplied_document_review":
        fail(f"{CREDENTIAL_SOURCE_ID}: unexpected source kind")
    if "url" in credential_source:
        fail(f"{CREDENTIAL_SOURCE_ID}: private evidence must not have a URL")

    return claims, sources, official_urls


def validate_public_files() -> None:
    credential_identifier = re.compile(rb"KZ55VWE[0-9]{8}")
    text_only_patterns = {
        "12-digit civil identifier": re.compile(
            rb"(?<![A-Za-z0-9])[0-9]{12}(?![A-Za-z0-9])"
        ),
        "absolute Windows path": re.compile(rb"[A-Za-z]:\\"),
        "private file URL": re.compile(rb"file://", re.IGNORECASE),
        "accreditation identifier": re.compile(rb"KZ\.S\.", re.IGNORECASE),
    }
    for path in SITE.rglob("*"):
        if path.is_file():
            try:
                content = path.read_bytes()
                if credential_identifier.search(content):
                    fail(
                        "Prohibited legacy credential identifier found in "
                        f"{path.relative_to(ROOT)}"
                    )
                if path.suffix.lower() not in PUBLIC_TEXT_SUFFIXES:
                    continue
                for label, pattern in text_only_patterns.items():
                    if pattern.search(content):
                        fail(f"Prohibited {label} found in {path.relative_to(ROOT)}")
            except OSError as exc:
                fail(f"Cannot scan {path.relative_to(ROOT)}: {exc}")


def validate_html(
    claims: dict[str, dict[str, object]],
    sources: dict[str, dict[str, object]],
    official_urls: dict[str, str],
) -> None:
    identity = claims.get("identity.name", {}).get("value", {})
    orcid = claims.get("profile.orcid", {}).get("value", {})
    scopus = claims.get("profile.scopus", {}).get("value", {})
    expected_person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": "https://ikurabayev.kz/#person",
        "name": (
            identity.get("preferred_public_name")
            if isinstance(identity, dict)
            else None
        ),
        "url": "https://ikurabayev.kz/",
        "sameAs": [
            orcid.get("url") if isinstance(orcid, dict) else None,
            scopus.get("url") if isinstance(scopus, dict) else None,
            sources.get("source.katru.faculty_profile", {}).get("url"),
            sources.get("source.astana_energy.board_profile", {}).get("url"),
        ],
    }

    legacy_visible = (
        "Действует в 8 странах ЕАПК",
        "Valid in 8 EAPO states",
        "8 елде қолданылады (ЕАПВ)",
        "Выдан 16.09.2022",
        "Granted 16.09.2022",
        "Тіркелді 16.09.2022",
    )
    patent_card_markers = {
        "/": {
            "patent.ea041128": (
                "№ 041128",
                "Опубл. B1 16.09.2022",
                "Статус: не действует (проверено 09.08.2026)",
            ),
            "patent.kz35922": (
                "№ 35922",
                "Опубл. 21.10.2022",
                "Статус: не действует (проверено 09.08.2026)",
            ),
            "patent.kz37923": (
                "№ 37923",
                "Опубл. 27.03.2026",
                "Статус: действует по состоянию на 09.08.2026",
            ),
        },
        "/ru/": {
            "patent.ea041128": (
                "№ 041128",
                "Опубл. B1 16.09.2022",
                "Статус: не действует (проверено 09.08.2026)",
            ),
            "patent.kz35922": (
                "№ 35922",
                "Опубл. 21.10.2022",
                "Статус: не действует (проверено 09.08.2026)",
            ),
            "patent.kz37923": (
                "№ 37923",
                "Опубл. 27.03.2026",
                "Статус: действует по состоянию на 09.08.2026",
            ),
        },
        "/en/": {
            "patent.ea041128": (
                "№ 041128",
                "Published B1 16.09.2022",
                "Status: not in force (checked 9 Aug 2026)",
            ),
            "patent.kz35922": (
                "№ 35922",
                "Published 21.10.2022",
                "Status: not in force (checked 9 Aug 2026)",
            ),
            "patent.kz37923": (
                "№ 37923",
                "Published 27.03.2026",
                "Status: active as of 9 Aug 2026",
            ),
        },
        "/kk/": {
            "patent.ea041128": (
                "№ 041128",
                "B1 жарияланды 16.09.2022",
                "Мәртебесі: күшінде емес (2026 жылғы 9 тамызда тексерілді)",
            ),
            "patent.kz35922": (
                "№ 35922",
                "Жарияланды 21.10.2022",
                "Мәртебесі: күшінде емес (2026 жылғы 9 тамызда тексерілді)",
            ),
            "patent.kz37923": (
                "№ 37923",
                "Жарияланды 27.03.2026",
                "Мәртебесі: 2026 жылғы 9 тамыздағы тексеру бойынша күшінде",
            ),
        },
    }
    certification_markers = {
        "/": (
            "Сертифицированный энергоаудитор",
            "сертификат выдан 14 августа 2026 года",
            "действителен до 6 августа 2029 года",
        ),
        "/ru/": (
            "Сертифицированный энергоаудитор",
            "сертификат выдан 14 августа 2026 года",
            "действителен до 6 августа 2029 года",
        ),
        "/en/": (
            "Certified energy auditor",
            "certificate issued 14 August 2026",
            "valid until 6 August 2029",
        ),
        "/kk/": (
            "Сертификатталған энергоаудитор",
            "сертификат 2026 жылғы 14 тамызда берілді",
            "2029 жылғы 6 тамызға дейін жарамды",
        ),
        "/qr/": ("сертифицированный энергоаудитор",),
    }
    obsolete_certification_wording = (
        "аккредитованный энергоаудитор",
        "accredited energy auditor",
        "аккредиттелген энергоаудитор",
        "аккредитация",
        "accreditation",
        "аккредиттеу",
    )

    for route, (path, canonical) in ROUTES.items():
        parser = parse_page(route, path)
        visible_text = parser.visible_text
        for marker in certification_markers[route]:
            if marker not in visible_text:
                fail(f"{route}: certification marker is missing: {marker}")
        visible_casefold = visible_text.casefold()
        for obsolete in obsolete_certification_wording:
            if obsolete.casefold() in visible_casefold:
                fail(f"{route}: obsolete personal-accreditation wording remains: {obsolete}")
        canonicals = [
            link.get("href", "")
            for link in parser.links
            if link.get("rel", "").lower() == "canonical"
        ]
        if canonicals != [canonical]:
            fail(f"{route}: self-canonical must be exactly {canonical}")
        parsed_canonical = urlparse(canonical)
        if parsed_canonical.scheme != "https" or parsed_canonical.hostname != CANONICAL_HOST:
            fail(f"{route}: canonical must use HTTPS apex host {CANONICAL_HOST}")

        alternate_pairs = [
            (link.get("hreflang", ""), link.get("href", ""))
            for link in parser.links
            if link.get("rel", "").lower() == "alternate" and link.get("hreflang")
        ]
        alternates = dict(alternate_pairs)
        if route in PROFILE_ROUTES and (
            len(alternate_pairs) != len(HREFLANG) or alternates != HREFLANG
        ):
            fail(f"{route}: reciprocal hreflang set does not match the route contract")
        if route == "/qr/" and alternate_pairs:
            fail("/qr/: QR page must not join the profile hreflang cluster")

        description = one_meta(parser, route, "description")
        og_title = one_meta(parser, route, "og:title")
        og_description = one_meta(parser, route, "og:description")
        og_type = one_meta(parser, route, "og:type")
        og_url = one_meta(parser, route, "og:url")
        og_image = one_meta(parser, route, "og:image")
        twitter_card = one_meta(parser, route, "twitter:card")
        twitter_title = one_meta(parser, route, "twitter:title")
        twitter_description = one_meta(parser, route, "twitter:description")
        twitter_image = one_meta(parser, route, "twitter:image")
        if not description:
            fail(f"{route}: description must be non-empty")
        if og_type != ("website" if route == "/qr/" else "profile"):
            fail(f"{route}: unexpected og:type")
        if og_url != canonical:
            fail(f"{route}: og:url must equal its canonical")
        if og_image != OG_IMAGE or twitter_image != OG_IMAGE:
            fail(f"{route}: social images must use the absolute approved OG image")
        if twitter_card != "summary_large_image":
            fail(f"{route}: expected summary_large_image Twitter card")
        if twitter_title != og_title or twitter_description != og_description:
            fail(f"{route}: Twitter title/description must match localized OG metadata")

        for src in parser.script_srcs:
            parsed_src = urlparse(src)
            if src.startswith("//") or parsed_src.scheme or parsed_src.netloc:
                fail(f"{route}: external runtime script is not allowed: {src}")

        json_objects: list[object] = []
        for block in parser.json_ld_text:
            try:
                json_objects.append(json.loads(block))
            except json.JSONDecodeError as exc:
                fail(f"{route}: invalid JSON-LD: {exc}")
        people = [
            item
            for item in json_objects
            if isinstance(item, dict) and item.get("@type") == "Person"
        ]
        if route in PROFILE_ROUTES:
            if len(people) != 1:
                fail(f"{route}: expected exactly the minimal evidence-backed Person JSON-LD")
            else:
                person = people[0]
                scalar_keys = ("@context", "@type", "@id", "name", "url")
                if set(person) != set(expected_person):
                    fail(f"{route}: Person JSON-LD must remain minimal")
                for key in scalar_keys:
                    if person.get(key) != expected_person[key]:
                        fail(f"{route}: unexpected Person JSON-LD {key}")
                same_as = person.get("sameAs")
                if (
                    not isinstance(same_as, list)
                    or not all(isinstance(item, str) for item in same_as)
                    or len(same_as) != len(expected_person["sameAs"])
                    or set(same_as) != set(expected_person["sameAs"])
                ):
                    fail(f"{route}: Person sameAs must match the reviewed identity sources")
        elif people:
            fail("/qr/: QR page must not duplicate the Person identity block")

        if route in PROFILE_ROUTES:
            anchor_index = defaultdict(list)
            for anchor in parser.anchors:
                anchor_index[anchor.get("href", "")].append(anchor)
            for claim_id, url in official_urls.items():
                matches = anchor_index.get(url, [])
                if len(matches) != 1:
                    fail(f"{route}: expected one direct link to official registry {url}")
                    continue
                rel_tokens = set(matches[0].get("rel", "").split())
                if matches[0].get("target") != "_blank" or not {
                    "noopener",
                    "noreferrer",
                }.issubset(rel_tokens):
                    fail(
                        f"{route}: official registry links require target=_blank "
                        "and noopener noreferrer"
                    )
                cards = [
                    card
                    for card in parser.patent_cards
                    if any(anchor.get("href") == url for anchor in card["anchors"])
                ]
                if len(cards) != 1:
                    fail(f"{route}: official registry link must identify one patent card: {url}")
                    continue
                card_text = cards[0]["text"]
                for marker in patent_card_markers[route][claim_id]:
                    if marker not in card_text:
                        fail(f"{route}: {claim_id} card is missing: {marker}")
        for legacy in legacy_visible:
            if legacy in parser.visible_text:
                fail(f"{route}: stale patent-validity wording remains: {legacy}")


def validate_cv_html() -> None:
    markers = {
        "/cv/": (
            "Искандер Курабаев — публичное CV",
            "Сертифицированный энергоаудитор",
            "Сертификат выдан 2026-08-14 и действителен до 2029-08-06",
            "2023. «Заслуженный энергетик»",
            "2018. «Почётный энергетик»",
            "2016. «Почётный энергетик»",
            "AI Energy Auditor — в разработке",
        ),
        "/en/cv/": (
            "Iskander Kurabayev — Public CV",
            "Certified energy auditor",
            "Certificate issued on 2026-08-14 and valid until 2029-08-06",
            "2023. Distinguished Power Engineer",
            "2018. Honoured Energy Worker",
            "2016. Honoured Energy Worker",
            "AI Energy Auditor — in development",
        ),
    }
    obsolete_certification_wording = (
        "аккредитованный энергоаудитор",
        "accredited energy auditor",
        "аккредиттелген энергоаудитор",
        "аккредитация",
        "accreditation",
        "аккредиттеу",
    )

    for route, (path, canonical, language) in CV_ROUTES.items():
        parser = parse_page(route, path)
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            fail(f"{route}: cannot read generated HTML source: {exc}")
            raw = ""
        visible_text = parser.visible_text

        if (
            'data-generated-public-cv="true"' not in raw
            or "Generated by tools/build_public_cv.py; do not edit manually."
            not in raw
        ):
            fail(f"{route}: generated Living Public CV ownership marker is missing")
        for marker in markers[route]:
            if marker not in visible_text:
                fail(f"{route}: public CV marker is missing: {marker}")
        visible_casefold = visible_text.casefold()
        for obsolete in obsolete_certification_wording:
            if obsolete.casefold() in visible_casefold:
                fail(f"{route}: obsolete personal-accreditation wording remains: {obsolete}")

        pdf_path, pdf_href, pdf_label = PDF_EXPORTS[route]
        pdf_links = [
            anchor for anchor in parser.anchors if anchor.get("href") == pdf_href
        ]
        if len(pdf_links) != 1:
            fail(f"{route}: expected one localized PDF download link")
        elif "download" not in pdf_links[0]:
            fail(f"{route}: PDF link must use the download attribute")
        if pdf_label not in visible_text:
            fail(f"{route}: localized PDF download label is missing")
        try:
            pdf_bytes = pdf_path.read_bytes()
        except OSError as exc:
            fail(f"{route}: PDF export cannot be read: {exc}")
        else:
            if not pdf_bytes.startswith(b"%PDF-") or not pdf_bytes.rstrip().endswith(b"%%EOF"):
                fail(f"{route}: PDF export has an invalid file envelope")
            if not 50_000 <= len(pdf_bytes) <= 1_000_000:
                fail(f"{route}: PDF export has an unexpected file size")
            if b"/JavaScript" in pdf_bytes or b"/AcroForm" in pdf_bytes:
                fail(f"{route}: PDF export must remain static and script-free")

        canonicals = [
            link.get("href", "")
            for link in parser.links
            if link.get("rel", "").lower() == "canonical"
        ]
        if canonicals != [canonical]:
            fail(f"{route}: self-canonical must be exactly {canonical}")
        parsed_canonical = urlparse(canonical)
        if parsed_canonical.scheme != "https" or parsed_canonical.hostname != CANONICAL_HOST:
            fail(f"{route}: canonical must use HTTPS apex host {CANONICAL_HOST}")

        alternate_pairs = [
            (link.get("hreflang", ""), link.get("href", ""))
            for link in parser.links
            if link.get("rel", "").lower() == "alternate" and link.get("hreflang")
        ]
        if len(alternate_pairs) != len(CV_HREFLANG) or dict(alternate_pairs) != CV_HREFLANG:
            fail(f"{route}: reciprocal CV hreflang set does not match the route contract")

        stylesheets = [
            link.get("href", "")
            for link in parser.links
            if link.get("rel", "").lower() == "stylesheet"
        ]
        if stylesheets != ["/assets/styles.css", "/assets/cv.css"]:
            fail(f"{route}: expected the reviewed base and CV stylesheets")

        description = one_meta(parser, route, "description")
        og_title = one_meta(parser, route, "og:title")
        og_description = one_meta(parser, route, "og:description")
        og_type = one_meta(parser, route, "og:type")
        og_url = one_meta(parser, route, "og:url")
        og_image = one_meta(parser, route, "og:image")
        twitter_card = one_meta(parser, route, "twitter:card")
        twitter_title = one_meta(parser, route, "twitter:title")
        twitter_description = one_meta(parser, route, "twitter:description")
        twitter_image = one_meta(parser, route, "twitter:image")
        if not description:
            fail(f"{route}: description must be non-empty")
        if og_type != "profile":
            fail(f"{route}: unexpected og:type")
        if og_url != canonical:
            fail(f"{route}: og:url must equal its canonical")
        if og_image != OG_IMAGE or twitter_image != OG_IMAGE:
            fail(f"{route}: social images must use the absolute approved OG image")
        if twitter_card != "summary_large_image":
            fail(f"{route}: expected summary_large_image Twitter card")
        if twitter_title != og_title or twitter_description != og_description:
            fail(f"{route}: Twitter title/description must match localized OG metadata")

        if parser.script_srcs:
            fail(f"{route}: generated CV must not load runtime scripts")
        json_objects: list[object] = []
        for block in parser.json_ld_text:
            try:
                json_objects.append(json.loads(block))
            except json.JSONDecodeError as exc:
                fail(f"{route}: invalid JSON-LD: {exc}")
        expected_page = {
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "@id": f"{canonical}#page",
            "url": canonical,
            "inLanguage": language,
            "mainEntity": {"@id": "https://ikurabayev.kz/#person"},
        }
        if json_objects != [expected_page]:
            fail(f"{route}: ProfilePage JSON-LD must match the reviewed minimal contract")

    profile_cv_links = {
        "/": (SITE / "index.html", "cv/"),
        "/ru/": (SITE / "ru" / "index.html", "../cv/"),
        "/en/": (SITE / "en" / "index.html", "cv/"),
    }
    for route, (path, expected_href) in profile_cv_links.items():
        parser = parse_page(route, path)
        matches = [
            anchor for anchor in parser.anchors if anchor.get("href") == expected_href
        ]
        if len(matches) != 1:
            fail(f"{route}: expected one profile link to the localized public CV")


def validate_sitemap_and_robots() -> None:
    expected = [canonical for _, canonical in ROUTES.values()] + [
        canonical for _, canonical, _ in CV_ROUTES.values()
    ]
    sitemap_path = SITE / "sitemap.xml"
    try:
        root = ET.parse(sitemap_path).getroot()
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = [
            (node.findtext(f"{namespace}loc") or "").strip()
            for node in root.findall(f"{namespace}url")
        ]
        if root.tag != f"{namespace}urlset":
            fail("sitemap.xml must use the standard sitemap namespace")
        if (
            set(locs) != set(expected)
            or len(locs) != len(expected)
            or len(locs) != len(set(locs))
        ):
            fail("sitemap.xml must contain exactly the seven canonical routes without duplicates")
    except (OSError, ET.ParseError) as exc:
        fail(f"sitemap.xml is not valid readable XML: {exc}")

    try:
        robots_lines = [
            line.strip()
            for line in (SITE / "robots.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        required = {"User-agent: *", "Allow: /", f"Sitemap: {SITEMAP_URL}"}
        if len(robots_lines) != len(required) or set(robots_lines) != required:
            fail("robots.txt must allow public indexing and reference the canonical sitemap")
    except (OSError, UnicodeError) as exc:
        fail(f"robots.txt is not readable UTF-8: {exc}")


def validate_concierge() -> None:
    path = SITE / "assets" / "concierge.js"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"concierge.js is not readable UTF-8: {exc}")
        return

    stale = (
        "Полная проверка реестров частично ожидается.",
        "Full registry verification is partly pending.",
        "Тізілімдерді толық тексеру ішінара күтілуде.",
    )
    for phrase in stale:
        if phrase in text:
            fail(f"concierge.js contains stale patent-verification wording: {phrase}")

    certification_markers = (
        "сертифицированный энергоаудитор",
        "Сертификат выдан 14 августа 2026 года",
        "действителен до 6 августа 2029 года",
        "certified energy auditor",
        "issued on 14 August 2026",
        "valid until 6 August 2029",
        "сертификатталған энергоаудитор",
        "2026 жылғы 14 тамызда берілді",
        "2029 жылғы 6 тамызға дейін жарамды",
    )
    text_casefold = text.casefold()
    for marker in certification_markers:
        if marker.casefold() not in text_casefold:
            fail(f"concierge.js certification marker is missing: {marker}")
    for obsolete in (
        "аккредитованный энергоаудитор",
        "accredited energy auditor",
        "аккредиттелген энергоаудитор",
    ):
        if obsolete.casefold() in text_casefold:
            fail(f"concierge.js contains obsolete wording: {obsolete}")

    kazakh_markers = (
        KAZAKH_FULL_NAME,
        "Зертханаға сұрақ қойыңыз",
        "Прототиптік интерфейс · Дереккөз режимі: тек ашық деректер",
        "Тек жергілікті",
        "Нақты AI интеграциясы қосылмаған",
        "құжаттың өзге деректемелері әдейі жарияланбайды",
        "Бірнеше жұмыстың DOI-ы тексерілген",
    )
    for marker in kazakh_markers:
        if marker not in text:
            fail(f"concierge.js Kazakh language marker is missing: {marker}")
    for stale in (
        'title: "Зертханадан сұраңыз"',
        "Төмендегі кеңесті басыңыз",
        "ИИ-ассистенттік",
        "электртехника саласының зерттеушісі",
        "Электртехникалық кешендер мен жүйелер",
    ):
        if stale in text:
            fail(f"concierge.js contains stale mixed-language Kazakh UI: {stale}")

    forbidden_runtime = {
        r"\bfetch\s*\(": "fetch",
        r"\bXMLHttpRequest\b": "XMLHttpRequest",
        r"\bWebSocket\b": "WebSocket",
        r"\bEventSource\b": "EventSource",
        r"\bsendBeacon\b": "sendBeacon",
        r"document\s*\.\s*cookie": "cookies",
        r"\blocalStorage\b": "localStorage",
        r"\bsessionStorage\b": "sessionStorage",
        r"\bindexedDB\b": "IndexedDB",
        r"public-facts\.json": "runtime Evidence Spine loading",
    }
    for pattern, label in forbidden_runtime.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            fail(f"concierge.js contains prohibited {label} construct")


def validate_kazakh_language_contract() -> None:
    path = SITE / "kk" / "index.html"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"/kk/: cannot read Kazakh HTML for language validation: {exc}")
        return

    markers = (
        f"<h1>{KAZAKH_FULL_NAME}</h1>",
        f'<title>{KAZAKH_FULL_NAME} | Ашық профиль</title>',
        'aria-label="Сенім белгілері"',
        "AI-дан сұрау",
        "Қазіргі ашық мәлімет",
        "Электротехникалық кешендер мен жүйелер",
        "жоспарлы-профилактикалық жөндеу жұмыстарын",
        "Аналогтық кіріс сатысы",
        "Инженерлік тәжірибе жариялауға қауіпсіз деңгейде берілген",
    )
    for marker in markers:
        if marker not in text:
            fail(f"/kk/: reviewed Kazakh language marker is missing: {marker}")
    for stale in (
        'aria-label="Trust markers"',
        "ИИ-ден сұрау",
        "электртехникалық",
        "Электртехникалық",
        "Ағымдағы ашық тұжырым",
        "Ашық түрде қауіпсіз тәжірибе",
        "жөндеу-профилактикалық жұмыстарды",
        "Аналогтық фронт",
    ):
        if stale in text:
            fail(f"/kk/: stale or mixed-language wording remains: {stale}")


def main() -> int:
    claims, sources, official_urls = validate_evidence()
    validate_public_files()
    validate_html(claims, sources, official_urls)
    validate_cv_html()
    validate_sitemap_and_robots()
    validate_concierge()
    validate_kazakh_language_contract()

    if errors:
        print("Public release validation FAILED:", file=sys.stderr)
        for message in errors:
            print(f"- {message}", file=sys.stderr)
        return 1

    print(
        "Public release validation PASS: evidence states, privacy exclusions, "
        "localized patent and certification truth, generated Living Public CV routes "
        "and PDF downloads, "
        "Kazakh language markers, semantic metadata, sitemap, robots, and concierge "
        "architecture match the bounded v1.2 contract."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
