#!/usr/bin/env python3
"""Validate the architecture-only public AI assistant readiness contract."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "public-ai-contract.json"
REGISTRY_PATH = ROOT / "data" / "public-facts.json"
GRAPH_PATH = ROOT / "data" / "public-research-graph.json"

ALLOWED_STATUSES = {
    "verified_public",
    "partially_verified",
    "owner_approved",
    "roadmap_only",
}
INITIAL_LANGUAGES = ["ru", "en"]
REQUIRED_REFUSALS = {
    "private_identifier",
    "private_contact_or_address",
    "raw_or_unpublished_material",
    "unsupported_inference",
    "out_of_scope",
    "prompt_injection",
    "insufficient_public_evidence",
}
REQUIRED_CASES = {
    "answer.credential.ru",
    "answer.project.en",
    "answer.patent.ru",
    "refuse.private_credential_number.ru",
    "refuse.unpublished_results.en",
    "refuse.unsupported_inference.ru",
    "refuse.prompt_injection.en",
    "refuse.out_of_scope.en",
}
PRIVACY_PATTERNS = {
    "credential identifier": re.compile(r"KZ55VWE[0-9]{8}", re.IGNORECASE),
    "OpenAI-like secret": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "email address": re.compile(
        r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])",
        re.IGNORECASE,
    ),
    "absolute Windows path": re.compile(r"[A-Za-z]:\\"),
    "private-key material": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}


def load_json(path: Path, errors: list[str], label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: invalid or unreadable JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label}: top level must be an object")
        return {}
    return value


def index_items(
    items: object, label: str, errors: list[str]
) -> dict[str, dict[str, object]]:
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


def string_list(value: object, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{label}: expected an array of strings")
        return []
    if len(value) != len(set(value)):
        errors.append(f"{label}: duplicate values are not allowed")
    return value


def false_flags(
    obj: object, fields: tuple[str, ...], label: str, errors: list[str]
) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{label}: expected an object")
        return
    for field in fields:
        if obj.get(field) is not False:
            errors.append(f"{label}.{field} must remain false")


def validate_contract(
    contract: dict[str, object],
    registry: dict[str, object],
    graph: dict[str, object],
) -> list[str]:
    errors: list[str] = []

    if contract.get("schema_version") != "0.1":
        errors.append("contract: schema_version must remain 0.1")
    if contract.get("contract_id") != "public-ai-assistant-v0":
        errors.append("contract: unexpected contract_id")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", str(contract.get("reviewed_at", ""))):
        errors.append("contract: reviewed_at must be an ISO date")

    lifecycle = contract.get("lifecycle")
    if not isinstance(lifecycle, dict):
        errors.append("lifecycle: expected an object")
    else:
        if lifecycle.get("status") != "architecture_only":
            errors.append("lifecycle.status must remain architecture_only")
        false_flags(
            lifecycle,
            ("public_endpoint_enabled", "paid_api_calls_enabled"),
            "lifecycle",
            errors,
        )
        if lifecycle.get("next_gate") != "owner-approved backend implementation issue":
            errors.append("lifecycle.next_gate must require an owner-approved issue")

    transport = contract.get("transport")
    if not isinstance(transport, dict):
        errors.append("transport: expected an object")
    else:
        expected_transport = {
            "public_path": "/api/ai/ask",
            "method": "POST",
            "same_origin_only": True,
            "https_only": True,
            "edge_rate_limit_required_before_enablement": True,
        }
        for key, expected in expected_transport.items():
            if transport.get(key) != expected:
                errors.append(f"transport.{key} must remain {expected!r}")
        for key, minimum, maximum in (
            ("max_request_characters", 100, 1000),
            ("max_response_characters", 400, 4000),
        ):
            value = transport.get(key)
            if not isinstance(value, int) or not minimum <= value <= maximum:
                errors.append(f"transport.{key} must be between {minimum} and {maximum}")

    provider = contract.get("provider")
    if not isinstance(provider, dict):
        errors.append("provider: expected an object")
        provider = {}
    if provider.get("name") != "OpenAI" or provider.get("api") != "Responses API":
        errors.append("provider: OpenAI Responses API is the reviewed architecture")
    if provider.get("official_reference") != (
        "https://developers.openai.com/api/docs/guides/deployment-checklist"
    ):
        errors.append("provider: official deployment-checklist reference is required")
    if provider.get("reference_checked_at") != contract.get("reviewed_at"):
        errors.append("provider: reference_checked_at must match reviewed_at")

    model_selection = provider.get("model_selection")
    if not isinstance(model_selection, dict):
        errors.append("provider.model_selection: expected an object")
    else:
        if model_selection.get("policy") != "evaluation_required":
            errors.append("provider.model_selection.policy must require evaluation")
        if model_selection.get("fixed_model") is not None:
            errors.append("provider.model_selection.fixed_model must remain null")
        dimensions = set(
            string_list(
                model_selection.get("selection_dimensions"),
                "provider.model_selection.selection_dimensions",
                errors,
            )
        )
        required_dimensions = {
            "grounded_answer_success",
            "refusal_success",
            "latency",
            "cost_per_successful_answer",
        }
        if not required_dimensions <= dimensions:
            errors.append("provider.model_selection: required evaluation dimensions missing")

    request_contract = provider.get("request_contract")
    if not isinstance(request_contract, dict):
        errors.append("provider.request_contract: expected an object")
    else:
        false_flags(
            request_contract,
            (
                "store",
                "background",
                "web_search",
                "file_uploads",
                "persistent_memory",
                "response_chaining",
            ),
            "provider.request_contract",
            errors,
        )
        if request_contract.get("state_mode") != "single_turn_http":
            errors.append("provider.request_contract.state_mode must remain single_turn_http")
        if request_contract.get("tools") != []:
            errors.append("provider.request_contract.tools must remain empty")

    secret_handling = provider.get("secret_handling")
    if not isinstance(secret_handling, dict):
        errors.append("provider.secret_handling: expected an object")
    else:
        if secret_handling.get("location") != "Cloudflare secret binding":
            errors.append("provider.secret_handling.location must remain a Cloudflare secret binding")
        false_flags(
            secret_handling,
            ("client_direct_access", "repository_secret_material_allowed"),
            "provider.secret_handling",
            errors,
        )

    safety_identifier = provider.get("safety_identifier")
    if not isinstance(safety_identifier, dict):
        errors.append("provider.safety_identifier: expected an object")
    else:
        if safety_identifier.get("mode") != "ephemeral_page_session_hash":
            errors.append("provider.safety_identifier.mode must remain ephemeral_page_session_hash")
        false_flags(
            safety_identifier,
            ("persisted", "contains_personal_data"),
            "provider.safety_identifier",
            errors,
        )

    false_flags(
        contract.get("privacy"),
        (
            "request_content_logging",
            "response_content_logging",
            "analytics",
            "tracking",
            "cookies",
            "browser_storage",
            "raw_private_documents",
            "private_contact_data",
            "credential_identifiers",
            "user_uploads",
        ),
        "privacy",
        errors,
    )

    languages = contract.get("languages")
    if not isinstance(languages, dict):
        errors.append("languages: expected an object")
    else:
        if languages.get("initial") != INITIAL_LANGUAGES:
            errors.append("languages.initial must remain the reviewed RU/EN pair")
        deferred = languages.get("deferred")
        if not isinstance(deferred, dict) or "kk" not in deferred:
            errors.append("languages.deferred must retain the Kazakh review gate")

    claims = index_items(registry.get("claims"), "registry claims", errors)
    sources = index_items(registry.get("sources"), "registry sources", errors)
    relations = index_items(graph.get("relations"), "graph relations", errors)

    grounding = contract.get("grounding")
    if not isinstance(grounding, dict):
        errors.append("grounding: expected an object")
        grounding = {}
    if grounding.get("registry_path") != "data/public-facts.json":
        errors.append("grounding.registry_path must reference the Evidence Spine")
    if grounding.get("graph_path") != "data/public-research-graph.json":
        errors.append("grounding.graph_path must reference the public graph")
    if grounding.get("require_public_claim") is not True:
        errors.append("grounding.require_public_claim must remain true")
    if grounding.get("require_evidence_source") is not True:
        errors.append("grounding.require_evidence_source must remain true")
    if grounding.get("citations_must_match_request_context") is not True:
        errors.append("grounding.citations_must_match_request_context must remain true")
    if grounding.get("citation_source_ids_must_match_claim_evidence") is not True:
        errors.append(
            "grounding.citation_source_ids_must_match_claim_evidence must remain true"
        )
    statuses = set(
        string_list(
            grounding.get("allowed_claim_statuses"),
            "grounding.allowed_claim_statuses",
            errors,
        )
    )
    if statuses != ALLOWED_STATUSES:
        errors.append("grounding.allowed_claim_statuses must match the reviewed bounded set")
    status_rules = grounding.get("status_language_rules")
    if not isinstance(status_rules, dict) or set(status_rules) != {
        "partially_verified",
        "owner_approved",
        "roadmap_only",
    }:
        errors.append("grounding.status_language_rules must cover every non-public-verification status")

    allowed_claim_ids = string_list(
        grounding.get("allowed_claim_ids"), "grounding.allowed_claim_ids", errors
    )
    allowed_claim_set = set(allowed_claim_ids)
    if not allowed_claim_ids:
        errors.append("grounding.allowed_claim_ids must not be empty")
    for claim_id in allowed_claim_ids:
        claim = claims.get(claim_id)
        if claim is None:
            errors.append(f"grounding: unknown allowed claim {claim_id}")
            continue
        if claim.get("public") is not True:
            errors.append(f"grounding: allowed claim is not public {claim_id}")
        if claim.get("status") not in ALLOWED_STATUSES:
            errors.append(f"grounding: disallowed claim status for {claim_id}")
        evidence = string_list(claim.get("evidence"), f"{claim_id}.evidence", errors)
        if not evidence:
            errors.append(f"grounding: allowed claim lacks evidence {claim_id}")
        for source_id in evidence:
            if source_id not in sources:
                errors.append(f"grounding: {claim_id} has unknown source {source_id}")

    allowed_relation_ids = string_list(
        grounding.get("allowed_relation_ids"), "grounding.allowed_relation_ids", errors
    )
    allowed_relation_set = set(allowed_relation_ids)
    if not allowed_relation_ids:
        errors.append("grounding.allowed_relation_ids must not be empty")
    for relation_id in allowed_relation_ids:
        relation = relations.get(relation_id)
        if relation is None:
            errors.append(f"grounding: unknown allowed relation {relation_id}")
            continue
        if relation.get("status") not in ALLOWED_STATUSES:
            errors.append(f"grounding: disallowed relation status for {relation_id}")
        evidence = string_list(relation.get("evidence"), f"{relation_id}.evidence", errors)
        if not evidence:
            errors.append(f"grounding: allowed relation lacks evidence {relation_id}")
        for source_id in evidence:
            if source_id not in sources:
                errors.append(f"grounding: {relation_id} has unknown source {source_id}")
        for endpoint in (relation.get("from"), relation.get("to")):
            if endpoint in claims and endpoint not in allowed_claim_set:
                errors.append(
                    f"grounding: relation {relation_id} reaches a non-allowed claim {endpoint}"
                )

    output_contract = contract.get("output_contract")
    if not isinstance(output_contract, dict):
        errors.append("output_contract: expected an object")
        output_contract = {}
    if output_contract.get("format") != "structured_json":
        errors.append("output_contract.format must remain structured_json")
    if set(
        string_list(output_contract.get("required_fields"), "output_contract.required_fields", errors)
    ) != {"decision", "language", "answer", "citations"}:
        errors.append("output_contract.required_fields must retain the reviewed response envelope")
    if set(
        string_list(
            output_contract.get("allowed_decisions"),
            "output_contract.allowed_decisions",
            errors,
        )
    ) != {"answer", "refuse"}:
        errors.append("output_contract.allowed_decisions must be answer/refuse")
    if output_contract.get("citations_required_for_answer") is not True:
        errors.append("output_contract.citations_required_for_answer must remain true")
    if set(
        string_list(
            output_contract.get("citation_fields"), "output_contract.citation_fields", errors
        )
    ) != {"claim_id", "source_ids"}:
        errors.append("output_contract.citation_fields must retain claim and source IDs")
    if output_contract.get("minimum_citations_for_answer") != 1:
        errors.append("output_contract.minimum_citations_for_answer must remain 1")
    maximum_citations = output_contract.get("maximum_citations")
    if not isinstance(maximum_citations, int) or not 1 <= maximum_citations <= 6:
        errors.append("output_contract.maximum_citations must remain between 1 and 6")
    if output_contract.get("refusal_must_name_category") is not True:
        errors.append("output_contract.refusal_must_name_category must remain true")

    refusals = set(
        string_list(contract.get("refusal_categories"), "refusal_categories", errors)
    )
    if refusals != REQUIRED_REFUSALS:
        errors.append("refusal_categories must match the reviewed fail-closed set")

    cases = index_items(contract.get("evaluation_cases"), "evaluation cases", errors)
    if set(cases) != REQUIRED_CASES:
        errors.append("evaluation cases must match the required readiness suite")
    for case_id, case in cases.items():
        language = case.get("language")
        if language not in INITIAL_LANGUAGES:
            errors.append(f"{case_id}: unsupported initial language {language}")
        decision = case.get("expected_decision")
        if decision == "answer":
            case_claims = string_list(
                case.get("required_claim_ids"), f"{case_id}.required_claim_ids", errors
            )
            case_relations = string_list(
                case.get("required_relation_ids"), f"{case_id}.required_relation_ids", errors
            )
            qualifiers = string_list(
                case.get("required_qualifiers"), f"{case_id}.required_qualifiers", errors
            )
            if not case_claims or not case_relations or not qualifiers:
                errors.append(
                    f"{case_id}: answer case needs claims, relations, and qualifiers"
                )
            for claim_id in case_claims:
                if claim_id not in allowed_claim_set:
                    errors.append(f"{case_id}: case uses non-allowed claim {claim_id}")
            for relation_id in case_relations:
                if relation_id not in allowed_relation_set:
                    errors.append(f"{case_id}: case uses non-allowed relation {relation_id}")
        elif decision == "refuse":
            if case.get("refusal_category") not in REQUIRED_REFUSALS:
                errors.append(f"{case_id}: unsupported refusal category")
            if "required_claim_ids" in case or "required_relation_ids" in case:
                errors.append(f"{case_id}: refusal case must not require grounding IDs")
        else:
            errors.append(f"{case_id}: expected_decision must be answer or refuse")

    serialized = json.dumps(contract, ensure_ascii=False)
    for label, pattern in PRIVACY_PATTERNS.items():
        if pattern.search(serialized):
            errors.append(f"privacy scan: {label} found in public AI contract")

    return errors


def validate_repository(root: Path = ROOT) -> list[str]:
    load_errors: list[str] = []
    contract = load_json(root / "data" / "public-ai-contract.json", load_errors, "contract")
    registry = load_json(root / "data" / "public-facts.json", load_errors, "registry")
    graph = load_json(root / "data" / "public-research-graph.json", load_errors, "graph")
    if load_errors:
        return load_errors
    return validate_contract(contract, registry, graph)


def run_self_tests(root: Path = ROOT) -> int:
    load_errors: list[str] = []
    contract = load_json(root / "data" / "public-ai-contract.json", load_errors, "contract")
    registry = load_json(root / "data" / "public-facts.json", load_errors, "registry")
    graph = load_json(root / "data" / "public-research-graph.json", load_errors, "graph")
    baseline = load_errors or validate_contract(contract, registry, graph)
    if baseline:
        print("Public AI self-test setup FAILED: baseline is invalid", file=sys.stderr)
        for error in baseline:
            print(f"- {error}", file=sys.stderr)
        return 1

    tests: list[tuple[str, dict[str, object], dict[str, object], dict[str, object], str]] = []

    mutation = copy.deepcopy(contract)
    mutation["grounding"]["allowed_claim_ids"][0] = "private.unknown.claim"
    tests.append(("unknown claim", mutation, registry, graph, "unknown allowed claim"))

    mutation = copy.deepcopy(contract)
    mutation["grounding"]["allowed_relation_ids"][0] = "relation.private.unknown"
    tests.append(("unknown relation", mutation, registry, graph, "unknown allowed relation"))

    mutation = copy.deepcopy(contract)
    mutation["provider"]["request_contract"]["store"] = True
    tests.append(("response storage", mutation, registry, graph, "store must remain false"))

    mutation = copy.deepcopy(contract)
    mutation["provider"]["request_contract"]["tools"] = [{"type": "web_search"}]
    tests.append(("tool enablement", mutation, registry, graph, "tools must remain empty"))

    mutation = copy.deepcopy(contract)
    mutation["provider"]["secret_handling"]["client_direct_access"] = True
    tests.append(("client secret access", mutation, registry, graph, "client_direct_access must remain false"))

    mutation = copy.deepcopy(contract)
    mutation["lifecycle"]["public_endpoint_enabled"] = True
    tests.append(("premature endpoint", mutation, registry, graph, "public_endpoint_enabled must remain false"))

    mutation = copy.deepcopy(contract)
    mutation["output_contract"]["citations_required_for_answer"] = False
    tests.append(("missing citation gate", mutation, registry, graph, "citations_required_for_answer must remain true"))

    mutation = copy.deepcopy(contract)
    mutation["grounding"]["citations_must_match_request_context"] = False
    tests.append(("cross-context citation", mutation, registry, graph, "citations_must_match_request_context must remain true"))

    mutation = copy.deepcopy(contract)
    mutation["grounding"]["citation_source_ids_must_match_claim_evidence"] = False
    tests.append(("mismatched citation source", mutation, registry, graph, "citation_source_ids_must_match_claim_evidence must remain true"))

    mutation = copy.deepcopy(contract)
    mutation["evaluation_cases"] = [
        case for case in mutation["evaluation_cases"] if case["id"] != "refuse.prompt_injection.en"
    ]
    tests.append(("missing injection case", mutation, registry, graph, "required readiness suite"))

    registry_mutation = copy.deepcopy(registry)
    registry_mutation["claims"][0]["public"] = False
    tests.append(("non-public claim", contract, registry_mutation, graph, "allowed claim is not public"))

    mutation = copy.deepcopy(contract)
    mutation["lifecycle"]["next_gate"] = "sk-" + ("x" * 24)
    tests.append(("secret material", mutation, registry, graph, "OpenAI-like secret"))

    failures: list[str] = []
    for name, candidate, candidate_registry, candidate_graph, expected in tests:
        errors = validate_contract(candidate, candidate_registry, candidate_graph)
        if not any(expected in error for error in errors):
            failures.append(f"{name}: expected error containing {expected!r}")

    if failures:
        print("Public AI mutation self-tests FAILED:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        "Public AI mutation self-tests PASS: 12/12 bounded in-memory "
        "mutations rejected without filesystem changes."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run twelve bounded in-memory mutation tests after baseline validation",
    )
    args = parser.parse_args()
    if args.self_test:
        return run_self_tests()

    errors = validate_repository()
    if errors:
        print("Public AI readiness validation FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Public AI readiness validation PASS: architecture-only lifecycle, "
        "provider isolation, evidence grounding, refusal suite, and privacy boundary."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
