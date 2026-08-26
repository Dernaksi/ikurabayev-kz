#!/usr/bin/env python3
"""Build the deterministic server-side public AI grounding module."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from check_public_ai import validate_contract


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "public-ai-contract.json"
REGISTRY_PATH = ROOT / "data" / "public-facts.json"
GRAPH_PATH = ROOT / "data" / "public-research-graph.json"
OUTPUT_PATH = ROOT / "functions" / "api" / "ai" / "_grounding.js"
PROVENANCE_PATH = ROOT / "data" / "public-ai-grounding-provenance.json"

CLAIM_FIELDS = (
    "id",
    "kind",
    "status",
    "value",
    "evidence",
    "verified_at",
    "languages",
    "presentation_notes",
)
SOURCE_FIELDS = (
    "id",
    "kind",
    "url",
    "checked_at",
    "authority",
    "source_role",
    "public_safe_note",
)
RELATION_FIELDS = ("id", "from", "predicate", "to", "status", "evidence", "note")
TOPIC_FIELDS = ("id", "kind", "public", "labels")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise SystemExit(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc


def load_json(path: Path) -> tuple[bytes, dict[str, object]]:
    raw = read_bytes(path)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"Top level must be an object in {path.relative_to(ROOT)}")
    return raw, value


def item_index(items: object, label: str) -> dict[str, dict[str, object]]:
    if not isinstance(items, list):
        raise SystemExit(f"{label} must be an array")
    result: dict[str, dict[str, object]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise SystemExit(f"{label} contains an item without a string id")
        item_id = item["id"]
        if item_id in result:
            raise SystemExit(f"{label} contains duplicate id {item_id}")
        result[item_id] = item
    return result


def project(item: dict[str, object], fields: tuple[str, ...]) -> dict[str, object]:
    return {field: item[field] for field in fields if field in item}


def string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SystemExit(f"{label} must be an array of strings")
    return value


def ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def build_artifacts() -> tuple[bytes, bytes, dict[str, object]]:
    contract_raw, contract = load_json(CONTRACT_PATH)
    registry_raw, registry = load_json(REGISTRY_PATH)
    graph_raw, graph = load_json(GRAPH_PATH)

    validation_errors = validate_contract(contract, registry, graph)
    if validation_errors:
        details = "\n".join(f"- {error}" for error in validation_errors)
        raise SystemExit(f"Public AI contract is invalid:\n{details}")

    grounding = contract.get("grounding")
    if not isinstance(grounding, dict):
        raise SystemExit("Contract grounding must be an object")

    claim_ids = string_list(grounding.get("allowed_claim_ids"), "allowed_claim_ids")
    relation_ids = string_list(
        grounding.get("allowed_relation_ids"), "allowed_relation_ids"
    )
    claims = item_index(registry.get("claims"), "registry claims")
    sources = item_index(registry.get("sources"), "registry sources")
    topics = item_index(graph.get("topics"), "graph topics")
    relations = item_index(graph.get("relations"), "graph relations")

    selected_claims = [project(claims[claim_id], CLAIM_FIELDS) for claim_id in claim_ids]
    selected_relations = [
        project(relations[relation_id], RELATION_FIELDS) for relation_id in relation_ids
    ]

    source_ids: list[str] = []
    for item in [*selected_claims, *selected_relations]:
        source_ids.extend(string_list(item.get("evidence"), f"{item['id']}.evidence"))
    source_ids = ordered_unique(source_ids)
    selected_sources = [project(sources[source_id], SOURCE_FIELDS) for source_id in source_ids]

    topic_ids: list[str] = []
    for relation in selected_relations:
        for endpoint in (relation.get("from"), relation.get("to")):
            if isinstance(endpoint, str) and endpoint in topics:
                topic_ids.append(endpoint)
    topic_ids = ordered_unique(topic_ids)
    selected_topics = [project(topics[topic_id], TOPIC_FIELDS) for topic_id in topic_ids]

    source_hashes = {
        "data/public-ai-contract.json": sha256_bytes(contract_raw),
        "data/public-facts.json": sha256_bytes(registry_raw),
        "data/public-research-graph.json": sha256_bytes(graph_raw),
    }
    payload: dict[str, object] = {
        "schema_version": "0.1",
        "artifact_id": "public-ai-grounding-v0",
        "contract_id": contract.get("contract_id"),
        "reviewed_at": contract.get("reviewed_at"),
        "source_hashes": source_hashes,
        "subject": graph.get("subject"),
        "policy": {
            "allowed_claim_statuses": grounding.get("allowed_claim_statuses"),
            "status_language_rules": grounding.get("status_language_rules"),
            "refusal_categories": contract.get("refusal_categories"),
            "citations_must_match_request_context": grounding.get(
                "citations_must_match_request_context"
            ),
            "citation_source_ids_must_match_claim_evidence": grounding.get(
                "citation_source_ids_must_match_claim_evidence"
            ),
        },
        "claims": selected_claims,
        "sources": selected_sources,
        "topics": selected_topics,
        "relations": selected_relations,
    }
    payload_json = json.dumps(
        payload, ensure_ascii=False, indent=2, sort_keys=True
    ).encode("utf-8")
    payload_sha256 = sha256_bytes(payload_json)
    module = (
        "/* Generated by tools/build_public_ai_grounding.py. Do not edit manually. */\n"
        f'export const PUBLIC_AI_GROUNDING_SHA256 = "{payload_sha256}";\n'
        "export const PUBLIC_AI_GROUNDING = Object.freeze(\n"
        + payload_json.decode("utf-8")
        + "\n);\n"
    ).encode("utf-8")

    provenance: dict[str, object] = {
        "schema_version": "0.1",
        "artifact_id": "public-ai-grounding-provenance-v0",
        "reviewed_at": contract.get("reviewed_at"),
        "runtime_boundary": "server_side_only",
        "sources": [
            {"path": path, "sha256": digest}
            for path, digest in source_hashes.items()
        ],
        "output": {
            "path": "functions/api/ai/_grounding.js",
            "sha256": sha256_bytes(module),
            "payload_sha256": payload_sha256,
        },
        "counts": {
            "claims": len(selected_claims),
            "sources": len(selected_sources),
            "topics": len(selected_topics),
            "relations": len(selected_relations),
        },
    }
    provenance_bytes = (
        json.dumps(provenance, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return module, provenance_bytes, provenance


def check_file(path: Path, expected: bytes) -> bool:
    try:
        actual = path.read_bytes()
    except OSError:
        print(f"MISSING: {path.relative_to(ROOT)}", file=sys.stderr)
        return False
    if actual != expected:
        print(f"DRIFT: {path.relative_to(ROOT)}", file=sys.stderr)
        return False
    return True


def write_file(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write generated artifacts")
    mode.add_argument("--check", action="store_true", help="check byte-identical artifacts")
    args = parser.parse_args()

    module, provenance_bytes, provenance = build_artifacts()
    if args.write:
        write_file(OUTPUT_PATH, module)
        write_file(PROVENANCE_PATH, provenance_bytes)
        print(
            "Public AI grounding write PASS: "
            f"{provenance['counts']['claims']} claims, "
            f"{provenance['counts']['relations']} relations, "
            f"{provenance['counts']['sources']} sources, and "
            f"{provenance['counts']['topics']} topics."
        )
        return 0

    valid = check_file(OUTPUT_PATH, module) and check_file(
        PROVENANCE_PATH, provenance_bytes
    )
    if not valid:
        return 1
    print("Public AI grounding check PASS: generated artifacts are byte-identical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
