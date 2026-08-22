#!/usr/bin/env python3
"""Validate the bounded public knowledge graph and deterministic Living Public CV."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
SUBJECT_ID = "person.iskander_kurabayev"
GRAPH_STATUSES = {
    "verified_public",
    "partially_verified",
    "owner_approved",
    "roadmap_only",
}
FACT_STATUSES = GRAPH_STATUSES | {"needs_verification"}
PREDICATE_KINDS = {
    "holds_role": {"professional_role"},
    "authored": {"publication"},
    "inventor_on": {"patent"},
    "leads": {"research_grant"},
    "holds_credential": {"professional_credential", "education"},
    "received_award": {"award"},
    "develops": {"roadmap_project"},
}
ALLOWED_PREDICATES = set(PREDICATE_KINDS) | {"addresses_topic"}
STATUS_ORDER = {
    "verified_public": 0,
    "partially_verified": 1,
    "owner_approved": 2,
    "roadmap_only": 3,
    "needs_verification": 4,
}
EXPECTED_PATENTS = {
    "patent.ea041128": "not_in_force",
    "patent.kz35922": "not_in_force",
    "patent.kz37923": "active",
}
EXPECTED_PUBLICATIONS = {
    "publication.isolated_neutral_experimental_studies",
    "publication.gtd2_12436",
    "publication.icecet_9873012",
    "publication.yiuh4401",
    "publication.kazatc_error_estimation",
}
EXPECTED_PROJECTS = {"project.ai_energy_auditor", "project.stm32_lab"}
CREDENTIAL_SOURCE_ID = "source.owner_supplied.energy_auditor_certificate_review"
CREDENTIAL_VALUE_KEYS = {
    "credential",
    "practice_area",
    "professional_practice_since",
    "certificate_issued_on",
    "certificate_valid_until",
}
OWNER_CONTROLLED_SOURCE_KINDS = {
    "owner_approval",
    "owner_supplied_document_review",
}
EXPECTED_DOCUMENTS = {
    "cv.ru": ("ru", "cv/IKurabayev_Public_CV_RU.md"),
    "cv.en": ("en", "cv/IKurabayev_Public_CV_EN.md"),
    "cv.site.ru": ("ru", "site/cv/index.html"),
    "cv.site.en": ("en", "site/en/cv/index.html"),
}
RELATION_KEYS = {"id", "from", "predicate", "to", "status", "evidence", "note"}
PAYLOAD_KEYS = {
    "value",
    "title",
    "year",
    "role",
    "organization",
    "doi",
    "legal_status",
    "description",
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_json(path: Path, errors: list[str], label: str) -> tuple[bytes, dict[str, object]]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: invalid or unreadable JSON: {exc}")
        return b"", {}
    if not isinstance(value, dict):
        errors.append(f"{label}: top level must be an object")
        return raw, {}
    return raw, value


def unique_index(items: object, label: str, errors: list[str]) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    if not isinstance(items, list):
        errors.append(f"{label}: expected an array")
        return result
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append(f"{label}: item without a string id")
            continue
        item_id = item["id"]
        if item_id in result:
            errors.append(f"{label}: duplicate id {item_id}")
        result[item_id] = item
    return result


def ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def parse_iso_date(value: object, label: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{label}: expected an ISO date")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: invalid ISO date {value}")
        return None


def markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    start += len(marker)
    end = text.find("\n## ", start)
    return text[start:] if end < 0 else text[start:end]


def validate_privacy(paths: list[Path], errors: list[str], root: Path) -> None:
    patterns = {
        "credential identifier": re.compile(r"KZ55VWE[0-9]{8}", re.IGNORECASE),
        "email address": re.compile(
            r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])",
            re.IGNORECASE,
        ),
        "mailto URL": re.compile(r"mailto:", re.IGNORECASE),
        "Kazakhstan phone number": re.compile(
            r"(?:\+7|\b8)[\s(.-]*[0-9]{3}[\s).-]*[0-9]{3}[\s.-]*[0-9]{2}[\s.-]*[0-9]{2}"
        ),
        "12-digit civil identifier": re.compile(
            r"(?<![A-Za-z0-9])[0-9]{12}(?![A-Za-z0-9])"
        ),
        "absolute Windows path": re.compile(r"[A-Za-z]:\\"),
        "user-home path": re.compile(r"(?:/Users/|file://)", re.IGNORECASE),
        "private-key material": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    }
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"privacy scan: cannot read {path}: {exc}")
            continue
        for label, pattern in patterns.items():
            if pattern.search(text):
                try:
                    shown = path.relative_to(root)
                except ValueError:
                    shown = path
                errors.append(f"privacy scan: {label} found in {shown}")


def validate_registry(
    registry: dict[str, object], errors: list[str]
) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    subject = registry.get("subject")
    if not isinstance(subject, dict) or subject.get("id") != SUBJECT_ID:
        errors.append("registry: unexpected subject id")
    if isinstance(subject, dict) and subject.get("canonical_claim") != "identity.name":
        errors.append("registry: canonical identity claim must remain identity.name")

    claims = unique_index(registry.get("claims"), "registry claims", errors)
    sources = unique_index(registry.get("sources"), "registry sources", errors)
    if not 21 <= len(claims) <= 29:
        errors.append("registry: v0.2 must contain 21 to 29 bounded claims")
    review_date = registry.get("generated_or_reviewed_at")
    if not isinstance(review_date, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", review_date):
        errors.append("registry: generated_or_reviewed_at must be an ISO date")

    for claim_id, claim in claims.items():
        if claim.get("public") is not True:
            errors.append(f"{claim_id}: public must be true")
        status = claim.get("status")
        if status not in FACT_STATUSES:
            errors.append(f"{claim_id}: unsupported claim status {status}")
        if status in {"verified_public", "partially_verified"} and not isinstance(
            claim.get("verified_at"), str
        ):
            errors.append(f"{claim_id}: verified_at required for {status}")
        evidence = claim.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{claim_id}: evidence must be a non-empty array")
            continue
        for source_id in evidence:
            if source_id not in sources:
                errors.append(f"{claim_id}: unresolved evidence reference {source_id}")

    university = claims.get("role.university.current", {})
    university_value = university.get("value")
    if university.get("status") != "partially_verified":
        errors.append("role.university.current: conflict must remain partially_verified")
    if not isinstance(university_value, dict) or university_value.get("since") != "2023-09-01":
        errors.append("role.university.current: canonical source-conflict value changed")
    university_note = str(university.get("presentation_notes", "")).lower()
    if "conflict" not in university_note or set(university.get("evidence", [])) != {
        "source.katru.faculty_profile",
        "source.astana_energy.board_profile",
    }:
        errors.append("role.university.current: official-source conflict is not preserved")

    for claim_id, legal_status in EXPECTED_PATENTS.items():
        claim = claims.get(claim_id)
        value = claim.get("value") if claim else None
        if not isinstance(value, dict):
            errors.append(f"{claim_id}: missing structured patent claim")
            continue
        if value.get("legal_status") != legal_status:
            errors.append(f"{claim_id}: legal_status must remain {legal_status}")
        if value.get("legal_status_checked_at") != "2026-08-09":
            errors.append(f"{claim_id}: legal status must remain dated 2026-08-09")

    for claim_id in EXPECTED_PROJECTS:
        value = claims.get(claim_id, {}).get("value")
        if not isinstance(value, dict) or value.get("stage") != "in_development":
            errors.append(f"{claim_id}: roadmap project must remain in_development")

    credential = claims.get("credential.energy_auditor", {})
    credential_value = credential.get("value")
    if not isinstance(credential_value, dict):
        errors.append("credential.energy_auditor: missing structured value")
    else:
        unexpected_fields = set(credential_value) - CREDENTIAL_VALUE_KEYS
        missing_fields = CREDENTIAL_VALUE_KEYS - set(credential_value)
        if unexpected_fields:
            errors.append(
                "credential.energy_auditor: unexpected value fields: "
                + ", ".join(sorted(unexpected_fields))
            )
        if missing_fields:
            errors.append(
                "credential.energy_auditor: missing value fields: "
                + ", ".join(sorted(missing_fields))
            )
        expected_values = {
            "credential": "Certified energy auditor",
            "practice_area": "energy saving and energy efficiency improvement",
            "professional_practice_since": 2010,
            "certificate_issued_on": "2026-08-14",
            "certificate_valid_until": "2029-08-06",
        }
        for key, expected in expected_values.items():
            if credential_value.get(key) != expected:
                errors.append(
                    f"credential.energy_auditor: value.{key} must remain {expected}"
                )
        issued_on = parse_iso_date(
            credential_value.get("certificate_issued_on"),
            "credential.energy_auditor: certificate_issued_on",
            errors,
        )
        valid_until = parse_iso_date(
            credential_value.get("certificate_valid_until"),
            "credential.energy_auditor: certificate_valid_until",
            errors,
        )
        if issued_on and valid_until and issued_on >= valid_until:
            errors.append(
                "credential.energy_auditor: certificate issue date must precede validity end"
            )
    if credential.get("status") != "partially_verified":
        errors.append("credential.energy_auditor: status must remain partially_verified")
    if credential.get("verified_at") != "2026-08-21":
        errors.append("credential.energy_auditor: verified_at must remain 2026-08-21")
    expected_credential_evidence = {
        "source.katru.faculty_profile",
        "source.owner_approval.v1_1_public_content",
        CREDENTIAL_SOURCE_ID,
    }
    credential_evidence = credential.get("evidence")
    if not isinstance(credential_evidence, list) or set(
        credential_evidence
    ) != expected_credential_evidence:
        errors.append("credential.energy_auditor: unexpected evidence set")
    credential_note = str(credential.get("presentation_notes", "")).lower()
    for marker in (
        "not been independently verified",
        "civil identifier",
        "raw document",
        "file name",
        "path",
    ):
        if marker not in credential_note:
            errors.append(
                f"credential.energy_auditor: presentation limitation missing: {marker}"
            )

    credential_source = sources.get(CREDENTIAL_SOURCE_ID)
    expected_source = {
        "id": CREDENTIAL_SOURCE_ID,
        "kind": "owner_supplied_document_review",
        "checked_at": "2026-08-21",
        "authority": "repository_owner",
        "source_role": "credential_issue_and_validity",
        "public_safe_note": (
            "Sanitized review confirms only the certified-energy-auditor wording, "
            "issue date, and validity end date approved for public display. Private "
            "artifact and document metadata are intentionally excluded; this is not "
            "independent public verification."
        ),
    }
    if credential_source != expected_source:
        errors.append(
            f"{CREDENTIAL_SOURCE_ID}: sanitized source contract changed or includes private fields"
        )
    return claims, sources


def validate_graph(
    graph: dict[str, object],
    claims: dict[str, dict[str, object]],
    sources: dict[str, dict[str, object]],
    errors: list[str],
) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    if graph.get("schema_version") != "0.2":
        errors.append("graph: schema_version must be 0.2")
    if graph.get("subject") != SUBJECT_ID:
        errors.append("graph: subject does not match the registry subject")
    topics = unique_index(graph.get("topics"), "graph topics", errors)
    relations = unique_index(graph.get("relations"), "graph relations", errors)
    if not 5 <= len(topics) <= 9:
        errors.append("graph: expected 5 to 9 bounded public topics")

    for topic_id, topic in topics.items():
        if set(topic) != {"id", "kind", "public", "labels"}:
            errors.append(f"{topic_id}: topic contains unsupported fields")
        if topic.get("kind") != "research_topic" or topic.get("public") is not True:
            errors.append(f"{topic_id}: expected public research_topic")
        labels = topic.get("labels")
        if (
            not isinstance(labels, dict)
            or set(labels) != {"en", "ru"}
            or not all(isinstance(labels.get(key), str) and labels[key] for key in ("en", "ru"))
        ):
            errors.append(f"{topic_id}: labels must contain non-empty en and ru only")

    semantic_edges: set[tuple[object, object, object]] = set()
    for relation_id, relation in relations.items():
        keys = set(relation)
        if not {"id", "from", "predicate", "to", "status", "evidence"}.issubset(keys):
            errors.append(f"{relation_id}: missing required relation fields")
        if not keys.issubset(RELATION_KEYS) or keys & PAYLOAD_KEYS:
            errors.append(f"{relation_id}: relation duplicates claim payload or has unsupported fields")
        source = relation.get("from")
        predicate = relation.get("predicate")
        target = relation.get("to")
        status = relation.get("status")
        edge = (source, predicate, target)
        if edge in semantic_edges:
            errors.append(f"{relation_id}: duplicate semantic relation")
        semantic_edges.add(edge)
        if predicate not in ALLOWED_PREDICATES:
            errors.append(f"{relation_id}: unsupported predicate {predicate}")
            continue
        if status not in GRAPH_STATUSES:
            errors.append(f"{relation_id}: unsupported relation status {status}")

        linked_claim: dict[str, object] | None = None
        if predicate == "addresses_topic":
            if source not in claims:
                errors.append(f"{relation_id}: unresolved claim endpoint {source}")
            else:
                linked_claim = claims[str(source)]
            if target not in topics:
                errors.append(f"{relation_id}: unresolved topic endpoint {target}")
        else:
            if source != SUBJECT_ID:
                errors.append(f"{relation_id}: achievement relation must start at subject")
            if target not in claims:
                errors.append(f"{relation_id}: unresolved claim endpoint {target}")
            else:
                linked_claim = claims[str(target)]
                if linked_claim.get("kind") not in PREDICATE_KINDS[str(predicate)]:
                    errors.append(
                        f"{relation_id}: {predicate} cannot target "
                        f"{linked_claim.get('kind')}"
                    )

        evidence = relation.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{relation_id}: evidence must be a non-empty array")
            evidence = []
        for source_id in evidence:
            if source_id not in sources:
                errors.append(f"{relation_id}: unresolved evidence reference {source_id}")
        if linked_claim:
            claim_evidence = linked_claim.get("evidence", [])
            if not set(evidence).issubset(set(claim_evidence)):
                errors.append(f"{relation_id}: relation evidence exceeds linked claim evidence")
            claim_status = linked_claim.get("status")
            if status != claim_status:
                errors.append(
                    f"{relation_id}: relation status must match claim status {claim_status}"
                )
            if claim_status == "roadmap_only" and status != "roadmap_only":
                errors.append(f"{relation_id}: roadmap relation must remain roadmap_only")
        if status == "verified_public":
            non_owner_sources = [
                item
                for item in evidence
                if sources.get(item, {}).get("kind")
                not in OWNER_CONTROLLED_SOURCE_KINDS
            ]
            if not non_owner_sources:
                errors.append(
                    f"{relation_id}: verified_public cannot rely only on owner approval"
                )

    authored_targets = {
        str(item.get("to"))
        for item in relations.values()
        if item.get("predicate") == "authored"
    }
    if authored_targets != EXPECTED_PUBLICATIONS:
        errors.append("graph: authored relations must cover exactly the five selected publications")
    inventor_targets = {
        str(item.get("to"))
        for item in relations.values()
        if item.get("predicate") == "inventor_on"
    }
    if inventor_targets != set(EXPECTED_PATENTS):
        errors.append("graph: inventor_on relations must cover exactly the three patent claims")
    develops_targets = {
        str(item.get("to"))
        for item in relations.values()
        if item.get("predicate") == "develops"
    }
    if develops_targets != EXPECTED_PROJECTS:
        errors.append("graph: develops relations must cover exactly the two roadmap projects")

    conflict_pattern = re.compile(
        r"2023-09-01|2023-01|01/2023|09/2023|January 2023|September 2023|"
        r"январ\w*\s+2023|сентябр\w*\s+2023",
        re.IGNORECASE,
    )
    if conflict_pattern.search(json.dumps(graph, ensure_ascii=False)):
        errors.append("graph: disputed university start date must not be resolved or copied")
    return topics, relations


def validate_manifest_source_contract(
    manifest: dict[str, object],
    registry_raw: bytes,
    graph_raw: bytes,
    registry: dict[str, object],
    errors: list[str],
) -> None:
    if manifest.get("schema_version") != "0.1" or manifest.get("cv_version") != "0.2":
        errors.append("provenance: unexpected schema or CV version")
    if manifest.get("source_registry_sha256") != sha256_bytes(registry_raw):
        errors.append("provenance: source registry SHA-256 mismatch")
    if manifest.get("source_graph_sha256") != sha256_bytes(graph_raw):
        errors.append("provenance: source graph SHA-256 mismatch")
    if manifest.get("source_review_date") != registry.get("generated_or_reviewed_at"):
        errors.append("provenance: source review date does not match registry")
    hash_note = str(manifest.get("hash_scope_note", "")).lower()
    if "not a legal or digital signature" not in hash_note:
        errors.append("provenance: hashes must be described as non-signatures")
    if any("provenance_sha" in key.lower() for key in manifest):
        errors.append("provenance: recursive self-hash is not allowed")


def validate_document_hash(
    document_id: str,
    document: dict[str, object],
    content: bytes,
    errors: list[str],
) -> None:
    if document.get("sha256") != sha256_bytes(content):
        errors.append(f"{document_id}: document SHA-256 mismatch")


def validate_cv_semantics(document_text: dict[str, str], errors: list[str]) -> None:
    ru = document_text.get("cv.ru", "")
    en = document_text.get("cv.en", "")
    if not ru or not en:
        return
    ru_roles = markdown_section(ru, "Текущие роли")
    en_roles = markdown_section(en, "Current roles")
    if not ru_roles or not en_roles:
        errors.append("CV: current-role sections are missing")
    if "2023" in ru_roles or "2023" in en_roles:
        errors.append("CV: disputed university role start date must be omitted")

    required_patent_markers = {
        "cv.ru": (
            "37923",
            "действует по состоянию на 2026-08-09",
            "35922",
            "не действует; проверено 2026-08-09",
            "EA 041128",
        ),
        "cv.en": (
            "37923",
            "active as of 2026-08-09",
            "35922",
            "not in force; checked 2026-08-09",
            "EA 041128",
        ),
    }
    for document_id, markers in required_patent_markers.items():
        text = document_text.get(document_id, "")
        for marker in markers:
            if marker not in text:
                errors.append(f"{document_id}: inactive/active patent marker missing: {marker}")

    required_credential_markers = {
        "cv.ru": (
            "Сертифицированный энергоаудитор",
            "Сертификат выдан 2026-08-14",
            "действителен до 2029-08-06",
        ),
        "cv.en": (
            "Certified energy auditor",
            "Certificate issued on 2026-08-14",
            "valid until 2029-08-06",
        ),
    }
    for document_id, markers in required_credential_markers.items():
        text = document_text.get(document_id, "")
        for marker in markers:
            if marker not in text:
                errors.append(f"{document_id}: certification marker missing: {marker}")
    if "Аккредитованный энергоаудитор" in ru:
        errors.append("cv.ru: obsolete personal-accreditation wording is prohibited")
    if "Accredited energy auditor" in en:
        errors.append("cv.en: obsolete personal-accreditation wording is prohibited")

    required_ru_award_markers = (
        "**2023.** «Заслуженный энергетик» — Министерство энергетики Республики Казахстан.",
        "**2018.** «Почётный энергетик» — Министерство энергетики Республики Казахстан.",
        "**2016.** «Почётный энергетик» — Казахстанская электроэнергетическая ассоциация.",
    )
    for marker in required_ru_award_markers:
        if marker not in ru:
            errors.append(f"cv.ru: award translation mapping is incorrect: {marker}")
    if "сопроводительном манифесте" not in ru:
        errors.append("cv.ru: provenance footer must use the Russian term манифест")

    if "AI Energy Auditor" not in ru or "в разработке" not in ru:
        errors.append("cv.ru: AI Energy Auditor must remain in development")
    if "STM32 / измерительная лаборатория" not in ru or ru.count("в разработке") < 2:
        errors.append("cv.ru: STM32 lab must remain in development")
    if "AI Energy Auditor" not in en or en.count("in development") < 2:
        errors.append("cv.en: both roadmap projects must remain in development")
    for text_id, text in (("cv.ru", ru), ("cv.en", en)):
        if "https://ikurabayev.kz/" not in text:
            errors.append(f"{text_id}: public contact route is missing")
    url_pattern = re.compile(r"https://[^\s)]+")
    if set(url_pattern.findall(ru)) != set(url_pattern.findall(en)):
        errors.append("CV: RU and EN public URL sets differ")


def validate_manifest_and_documents(
    root: Path,
    manifest: dict[str, object],
    registry_raw: bytes,
    graph_raw: bytes,
    registry: dict[str, object],
    claims: dict[str, dict[str, object]],
    relations: dict[str, dict[str, object]],
    errors: list[str],
) -> None:
    validate_manifest_source_contract(
        manifest, registry_raw, graph_raw, registry, errors
    )

    documents = unique_index(manifest.get("documents"), "provenance documents", errors)
    blocks = unique_index(manifest.get("blocks"), "provenance blocks", errors)
    if set(documents) != set(EXPECTED_DOCUMENTS):
        errors.append("provenance: expected RU/EN Markdown and HTML documents")
    block_order = [
        item.get("id")
        for item in manifest.get("blocks", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ] if isinstance(manifest.get("blocks"), list) else []
    section_order = ordered_unique(
        [
            str(blocks[item].get("section_id"))
            for item in block_order
            if item in blocks
        ]
    )

    document_text: dict[str, str] = {}
    for document_id, (language, relative_path) in EXPECTED_DOCUMENTS.items():
        document = documents.get(document_id)
        if not document:
            continue
        if document.get("language") != language or document.get("path") != relative_path:
            errors.append(f"{document_id}: unexpected language or path")
        if Path(str(document.get("path", ""))).is_absolute():
            errors.append(f"{document_id}: path must be repository-relative")
        path = root / relative_path
        try:
            content = path.read_bytes()
            document_text[document_id] = content.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{document_id}: unreadable generated document: {exc}")
            continue
        validate_document_hash(document_id, document, content, errors)
        if document.get("block_ids") != block_order:
            errors.append(f"{document_id}: block order differs from provenance blocks")
        if document.get("section_ids") != section_order:
            errors.append(f"{document_id}: section order differs from provenance blocks")

    for block_id, block in blocks.items():
        claim_ids = block.get("claim_ids")
        relation_ids = block.get("relation_ids")
        if not isinstance(claim_ids, list) or not claim_ids:
            errors.append(f"{block_id}: every provenance block needs at least one claim")
            claim_ids = []
        if not isinstance(relation_ids, list):
            errors.append(f"{block_id}: relation_ids must be an array")
            relation_ids = []
        for claim_id in claim_ids:
            if claim_id not in claims:
                errors.append(f"{block_id}: unresolved claim reference {claim_id}")
        for relation_id in relation_ids:
            if relation_id not in relations:
                errors.append(f"{block_id}: unresolved relation reference {relation_id}")
        if block.get("document_ids") != [
            "cv.ru",
            "cv.en",
            "cv.site.ru",
            "cv.site.en",
        ]:
            errors.append(f"{block_id}: block must support all four CV documents")
        statuses = {
            str(claims[item].get("status")) for item in claim_ids if item in claims
        }
        statuses.update(
            str(relations[item].get("status")) for item in relation_ids if item in relations
        )
        expected_statuses = sorted(
            statuses, key=lambda item: (STATUS_ORDER.get(item, 99), item)
        )
        if block.get("effective_evidence_statuses") != expected_statuses:
            errors.append(f"{block_id}: effective evidence statuses are incorrect")

    university_block = blocks.get("cv.roles.university", {})
    if "start_date_omitted_due_to_source_conflict" not in university_block.get(
        "exclusions", []
    ):
        errors.append("provenance: university start-date conflict exclusion is required")
    credential_block = blocks.get("cv.credential.energy_auditor", {})
    combined_cv = "\n".join(document_text.values())
    if "2010" in combined_cv and "professional_practice_since_is_owner_approved" not in credential_block.get(
        "notes", []
    ):
        errors.append("provenance: the 2010 practice start needs an owner-approved note")
    required_credential_exclusions = {
        "certificate_identifier_omitted",
        "civil_identifier_omitted",
        "qr_content_omitted",
        "address_omitted",
        "signature_and_seal_omitted",
        "raw_document_and_path_omitted",
    }
    if not required_credential_exclusions.issubset(
        set(credential_block.get("exclusions", []))
    ):
        errors.append("provenance: credential privacy exclusions are incomplete")
    required_credential_notes = {
        "certificate_dates_from_sanitized_owner_supplied_document_review",
        "certificate_dates_not_independently_verified_publicly",
        "professional_practice_since_is_owner_approved",
    }
    if not required_credential_notes.issubset(set(credential_block.get("notes", []))):
        errors.append("provenance: credential evidence limitations are incomplete")

    validate_cv_semantics(document_text, errors)


def run_generator_check(root: Path, errors: list[str]) -> None:
    builder = root / "tools" / "build_public_cv.py"
    try:
        result = subprocess.run(
            [sys.executable, str(builder), "--check"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        errors.append(f"generator check could not run: {exc}")
        return
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip().replace("\n", " | ")
        errors.append(f"generator drift check failed: {details}")


def validate_repository(root: Path, *, run_generator: bool = True) -> list[str]:
    errors: list[str] = []
    registry_path = root / "data" / "public-facts.json"
    graph_path = root / "data" / "public-research-graph.json"
    provenance_path = root / "cv" / "IKurabayev_Public_CV_PROVENANCE.json"
    registry_raw, registry = load_json(registry_path, errors, "registry")
    graph_raw, graph = load_json(graph_path, errors, "graph")
    _, manifest = load_json(provenance_path, errors, "provenance")
    claims, sources = validate_registry(registry, errors)
    _, relations = validate_graph(graph, claims, sources, errors)
    validate_manifest_and_documents(
        root,
        manifest,
        registry_raw,
        graph_raw,
        registry,
        claims,
        relations,
        errors,
    )
    validate_privacy(
        [
            registry_path,
            graph_path,
            provenance_path,
            root / "cv" / "IKurabayev_Public_CV_RU.md",
            root / "cv" / "IKurabayev_Public_CV_EN.md",
        ],
        errors,
        root,
    )
    if run_generator:
        run_generator_check(root, errors)
    return errors


def run_mutation_self_tests(root: Path) -> int:
    baseline = validate_repository(root)
    if baseline:
        print("Mutation self-test setup FAILED: baseline is not valid", file=sys.stderr)
        for item in baseline:
            print(f"- {item}", file=sys.stderr)
        return 1

    setup_errors: list[str] = []
    registry_raw, registry = load_json(
        root / "data" / "public-facts.json", setup_errors, "registry"
    )
    graph_raw, graph = load_json(
        root / "data" / "public-research-graph.json", setup_errors, "graph"
    )
    _, manifest = load_json(
        root / "cv" / "IKurabayev_Public_CV_PROVENANCE.json",
        setup_errors,
        "provenance",
    )
    claims = unique_index(registry.get("claims"), "registry claims", setup_errors)
    sources = unique_index(registry.get("sources"), "registry sources", setup_errors)
    documents = unique_index(
        manifest.get("documents"), "provenance documents", setup_errors
    )
    try:
        document_text = {
            "cv.ru": (root / EXPECTED_DOCUMENTS["cv.ru"][1]).read_text(
                encoding="utf-8"
            ),
            "cv.en": (root / EXPECTED_DOCUMENTS["cv.en"][1]).read_text(
                encoding="utf-8"
            ),
        }
    except (OSError, UnicodeError) as exc:
        setup_errors.append(f"cannot read generated documents: {exc}")
        document_text = {}
    if setup_errors:
        print("Mutation self-test setup FAILED:", file=sys.stderr)
        for item in setup_errors:
            print(f"- {item}", file=sys.stderr)
        return 1

    failures: list[str] = []

    def record(name: str, mutation_errors: list[str], expected: str) -> None:
        if any(expected in item for item in mutation_errors):
            print(f"Mutation PASS: {name}")
        else:
            failures.append(
                f"{name}: validator did not emit expected diagnostic: {expected}"
            )

    missing_claim_graph = copy.deepcopy(graph)
    missing_claim_graph["relations"][0]["to"] = "claim.missing"
    mutation_errors: list[str] = []
    validate_graph(missing_claim_graph, claims, sources, mutation_errors)
    record("graph missing claim reference", mutation_errors, "unresolved claim endpoint")

    roadmap_graph = copy.deepcopy(graph)
    for relation in roadmap_graph["relations"]:
        if relation["id"] == "relation.person.develops.ai_energy_auditor":
            relation["status"] = "verified_public"
            break
    mutation_errors = []
    validate_graph(roadmap_graph, claims, sources, mutation_errors)
    record(
        "roadmap relation upgraded",
        mutation_errors,
        "relation status must match claim status roadmap_only",
    )

    invalid_term_registry = copy.deepcopy(registry)
    for claim in invalid_term_registry["claims"]:
        if claim["id"] == "credential.energy_auditor":
            claim["value"]["certificate_valid_until"] = "2026-08-01"
            break
    mutation_errors = []
    validate_registry(invalid_term_registry, mutation_errors)
    record(
        "credential validity before issue date",
        mutation_errors,
        "certificate issue date must precede validity end",
    )

    credential_number_registry = copy.deepcopy(registry)
    for claim in credential_number_registry["claims"]:
        if claim["id"] == "credential.energy_auditor":
            claim["value"]["certificate_number"] = "prohibited"
            break
    mutation_errors = []
    validate_registry(credential_number_registry, mutation_errors)
    record(
        "credential identifier field inserted",
        mutation_errors,
        "unexpected value fields: certificate_number",
    )

    dated_documents = dict(document_text)
    dated_documents["cv.en"] = dated_documents["cv.en"].replace(
        "## Education", "Start: 2023-09-01\n\n## Education", 1
    )
    mutation_errors = []
    validate_cv_semantics(dated_documents, mutation_errors)
    record(
        "disputed university date inserted into generated CV",
        mutation_errors,
        "disputed university role start date must be omitted",
    )

    patent_documents = dict(document_text)
    patent_documents["cv.en"] = patent_documents["cv.en"].replace(
        "not in force; checked 2026-08-09", "status checked 2026-08-09"
    )
    mutation_errors = []
    validate_cv_semantics(patent_documents, mutation_errors)
    record(
        "inactive patent status removed from generated CV",
        mutation_errors,
        "not in force; checked 2026-08-09",
    )

    changed_hash_manifest = copy.deepcopy(manifest)
    changed_hash_manifest["source_graph_sha256"] = "0" * 64
    mutation_errors = []
    validate_manifest_source_contract(
        changed_hash_manifest, registry_raw, graph_raw, registry, mutation_errors
    )
    record(
        "provenance source hash changed",
        mutation_errors,
        "source graph SHA-256 mismatch",
    )

    manually_edited = document_text["cv.en"].encode("utf-8") + b"\nManual drift test.\n"
    mutation_errors = []
    validate_document_hash("cv.en", documents["cv.en"], manually_edited, mutation_errors)
    record(
        "generated CV manually edited",
        mutation_errors,
        "document SHA-256 mismatch",
    )

    if failures:
        print("Public knowledge mutation self-tests FAILED:", file=sys.stderr)
        for item in failures:
            print(f"- {item}", file=sys.stderr)
        return 1
    print(
        "Public knowledge mutation self-tests PASS: 8/8 bounded in-memory "
        "mutations rejected without filesystem changes."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run eight bounded temporary mutation tests after baseline validation",
    )
    args = parser.parse_args()
    if args.self_test:
        return run_mutation_self_tests(DEFAULT_ROOT)

    errors = validate_repository(DEFAULT_ROOT)
    if errors:
        print("Public knowledge validation FAILED:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    print(
        "Public knowledge validation PASS: registry, graph, deterministic CV, "
        "block provenance, privacy, credential term, dated patent status, "
        "disputed-role omission, and roadmap boundaries match the bounded "
        "v0.2 contract."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
