#!/usr/bin/env python3
"""Validate the disabled public AI backend and readiness contract."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
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
    "service_unavailable",
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


def sha256_file(path: Path, errors: list[str], label: str) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        errors.append(f"{label}: cannot read {path}: {exc}")
        return ""


def validate_backend_files(
    root: Path, contract: dict[str, object], errors: list[str]
) -> None:
    routes = load_json(root / "site" / "_routes.json", errors, "Pages routes")
    if routes != {"version": 1, "include": ["/api/ai/ask"], "exclude": []}:
        errors.append("Pages routes: only /api/ai/ask may invoke a Function")

    handler_path = root / "functions" / "api" / "ai" / "ask.js"
    try:
        handler = handler_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"backend skeleton: cannot read handler: {exc}")
        handler = ""
    for marker in (
        'from "./_grounding.js"',
        'from "./_pilot.js"',
        "export async function handleRequest",
        "export function onRequestPost",
        '"same_origin_required"',
        '"Cache-Control": "no-store"',
    ):
        if marker not in handler:
            errors.append(f"backend skeleton: required marker missing: {marker}")
    forbidden_handler = {
        r"\bconsole\.(?:log|info|warn|error)\b": "content logging",
        r"\b(?:localStorage|sessionStorage|indexedDB)\b": "browser storage",
        r"document\s*\.\s*cookie": "cookies",
    }
    for pattern, label in forbidden_handler.items():
        if re.search(pattern, handler, flags=re.IGNORECASE):
            errors.append(f"backend handler: prohibited {label} construct")

    pilot_path = root / "functions" / "api" / "ai" / "_pilot.js"
    try:
        pilot = pilot_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"private pilot: cannot read provider adapter: {exc}")
        pilot = ""
    for marker in (
        'https://api.openai.com/v1/responses',
        'const DEFAULT_MODEL = "gpt-5.6-luna"',
        '"gpt-5.6-terra"',
        "store: false",
        "background: false",
        "tools: []",
        'type: "json_schema"',
        'request.headers.get("X-Pilot-Token")',
        'env?.AI_PILOT_ENABLED === "true"',
        'env?.AI_PUBLIC_ENABLED !== "true"',
        'env.AI_PUBLIC_RATE_LIMITER.limit',
        'export async function runPublicAssistant',
        'maxProviderAttempts: PUBLIC_MAX_PROVIDER_ATTEMPTS',
        '"service_unavailable"',
        "PRODUCTION_BRANCHES",
        "validateProviderOutput",
    ):
        if marker not in pilot:
            errors.append(f"private pilot: required marker missing: {marker}")
    forbidden_pilot = {
        r"\bconsole\.(?:log|info|warn|error)\b": "content logging",
        r"\b(?:localStorage|sessionStorage|indexedDB)\b": "browser storage",
        r"document\s*\.\s*cookie": "cookies",
        r"previous_response_id": "response chaining",
        r'"type"\s*:\s*"(?:web_search|file_search|computer_use|code_interpreter)"': "provider tools",
    }
    for pattern, label in forbidden_pilot.items():
        if re.search(pattern, pilot, flags=re.IGNORECASE):
            errors.append(f"private pilot: prohibited {label} construct")

    eval_path = root / "tools" / "run_public_ai_pilot_evals.mjs"
    try:
        eval_runner = eval_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"private pilot evals: cannot read runner: {exc}")
        eval_runner = ""
    for marker in (
        "PUBLIC_AI_PILOT_URL",
        "AI_PILOT_TOKEN",
        "PUBLIC_AI_EVAL_ROUNDS",
        "PUBLIC_AI_EVAL_INTERVAL_MS",
        "PUBLIC_AI_EVAL_CASE",
        'for (const language of ["ru", "en"])',
    ):
        if marker not in eval_runner:
            errors.append(f"private pilot evals: required marker missing: {marker}")
    if "body?.answer" in eval_runner or "question:" in re.sub(
        r"question:\s*testCase\.prompts\[language\]", "", eval_runner
    ):
        errors.append("private pilot evals: response text or prompt logging boundary changed")

    grounding_path = root / "functions" / "api" / "ai" / "_grounding.js"
    try:
        grounding_module = grounding_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"grounding output: cannot read module: {exc}")
        grounding_module = ""
    for label, pattern in PRIVACY_PATTERNS.items():
        if pattern.search(grounding_module):
            errors.append(f"grounding privacy scan: {label} found in generated module")

    provenance_path = root / "data" / "public-ai-grounding-provenance.json"
    provenance = load_json(
        provenance_path, errors, "public AI grounding provenance"
    )
    if provenance.get("schema_version") != "0.1":
        errors.append("grounding provenance: schema_version must remain 0.1")
    if provenance.get("runtime_boundary") != "server_side_only":
        errors.append("grounding provenance: runtime boundary must remain server_side_only")
    if provenance.get("reviewed_at") != contract.get("reviewed_at"):
        errors.append("grounding provenance: reviewed_at must match the contract")

    expected_sources = {
        "data/public-ai-contract.json": root / "data" / "public-ai-contract.json",
        "data/public-facts.json": root / "data" / "public-facts.json",
        "data/public-research-graph.json": root / "data" / "public-research-graph.json",
    }
    source_entries = provenance.get("sources")
    source_map: dict[str, str] = {}
    if not isinstance(source_entries, list):
        errors.append("grounding provenance: sources must be an array")
    else:
        for entry in source_entries:
            if not isinstance(entry, dict):
                errors.append("grounding provenance: invalid source entry")
                continue
            path = entry.get("path")
            digest = entry.get("sha256")
            if not isinstance(path, str) or not isinstance(digest, str):
                errors.append("grounding provenance: source path/hash must be strings")
                continue
            if path in source_map:
                errors.append(f"grounding provenance: duplicate source path {path}")
            source_map[path] = digest
    if set(source_map) != set(expected_sources):
        errors.append("grounding provenance: source path set is not exact")
    for relative, path in expected_sources.items():
        if source_map.get(relative) != sha256_file(
            path, errors, f"grounding provenance source {relative}"
        ):
            errors.append(f"grounding provenance: source hash mismatch for {relative}")

    output = provenance.get("output")
    if not isinstance(output, dict):
        errors.append("grounding provenance: output must be an object")
    else:
        if output.get("path") != "functions/api/ai/_grounding.js":
            errors.append("grounding provenance: unexpected output path")
        expected_output_hash = sha256_file(
            grounding_path,
            errors,
            "grounding output",
        )
        if output.get("sha256") != expected_output_hash:
            errors.append("grounding provenance: output hash mismatch")
        if not re.fullmatch(r"[a-f0-9]{64}", str(output.get("payload_sha256", ""))):
            errors.append("grounding provenance: payload hash must be SHA-256")

    grounding = contract.get("grounding")
    counts = provenance.get("counts")
    if not isinstance(grounding, dict) or not isinstance(counts, dict):
        errors.append("grounding provenance: counts or contract grounding missing")
    else:
        if counts.get("claims") != len(grounding.get("allowed_claim_ids", [])):
            errors.append("grounding provenance: claim count mismatch")
        if counts.get("relations") != len(grounding.get("allowed_relation_ids", [])):
            errors.append("grounding provenance: relation count mismatch")
        for key in ("sources", "topics"):
            if not isinstance(counts.get(key), int) or counts[key] <= 0:
                errors.append(f"grounding provenance: {key} count must be positive")


def run_grounding_check(root: Path, errors: list[str]) -> None:
    builder = root / "tools" / "build_public_ai_grounding.py"
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(builder), "--check"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        errors.append(f"grounding generator check could not run: {exc}")
        return
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip().replace("\n", " | ")
        errors.append(f"grounding generator drift check failed: {details}")


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
        if lifecycle.get("status") != "public_activation_readiness":
            errors.append("lifecycle.status must remain public_activation_readiness")
        false_flags(
            lifecycle,
            ("public_endpoint_enabled",),
            "lifecycle",
            errors,
        )
        if lifecycle.get("paid_api_calls_enabled") is not True:
            errors.append("lifecycle.paid_api_calls_enabled must remain true for the private pilot")
        if lifecycle.get("disabled_route_deployed") is not True:
            errors.append("lifecycle.disabled_route_deployed must remain true")
        if lifecycle.get("next_gate") != (
            "owner-approved control-plane configuration and activation PR"
        ):
            errors.append("lifecycle.next_gate must retain the separate activation approval")

    backend = contract.get("backend_skeleton")
    if not isinstance(backend, dict):
        errors.append("backend_skeleton: expected an object")
    else:
        expected_backend = {
            "adapter": "Cloudflare Pages Functions",
            "function_path": "functions/api/ai/ask.js",
            "routes_path": "site/_routes.json",
            "runtime_mode": "private_preview_plus_fail_closed_public_readiness",
            "provider_call_enabled": True,
            "grounding_bundle_path": "functions/api/ai/_grounding.js",
            "grounding_provenance_path": "data/public-ai-grounding-provenance.json",
            "rate_limit_status": "private_fixed_window_plus_required_public_cloudflare_binding",
        }
        for key, expected in expected_backend.items():
            if backend.get(key) != expected:
                errors.append(f"backend_skeleton.{key} must remain {expected!r}")

    private_pilot = contract.get("private_pilot")
    if not isinstance(private_pilot, dict):
        errors.append("private_pilot: expected an object")
    else:
        expected_pilot = {
            "issue": 61,
            "cloudflare_environment": "Preview",
            "production_branch": "main",
            "enable_variable": "AI_PILOT_ENABLED",
            "model_variable": "AI_PILOT_MODEL",
            "authentication_header": "X-Pilot-Token",
            "default_model": "gpt-5.6-luna",
            "application_requests_per_minute": 2,
            "provider_project_requests_per_minute": 3,
            "provider_project_tokens_per_minute": 10000,
            "provider_timeout_ms": 15000,
            "max_output_tokens": 700,
            "public_activation_authorized": False,
            "live_evaluation_status": "luna_selected_after_ru_en_comparison",
        }
        for key, expected in expected_pilot.items():
            if private_pilot.get(key) != expected:
                errors.append(f"private_pilot.{key} must remain {expected!r}")
        if private_pilot.get("secret_bindings") != ["OPENAI_API_KEY", "AI_PILOT_TOKEN"]:
            errors.append("private_pilot.secret_bindings must retain the two reviewed binding names")
        if private_pilot.get("allowed_models") != ["gpt-5.6-luna", "gpt-5.6-terra"]:
            errors.append("private_pilot.allowed_models must remain Luna and Terra")

    public_activation = contract.get("public_activation")
    if not isinstance(public_activation, dict):
        errors.append("public_activation: expected an object")
    else:
        expected_public_activation = {
            "issue": 65,
            "status": "code_readiness_only",
            "enable_variable": "AI_PUBLIC_ENABLED",
            "model_variable": "AI_PUBLIC_MODEL",
            "rate_limiter_binding": "AI_PUBLIC_RATE_LIMITER",
            "rate_limiter_key": "public-ai:/api/ai/ask",
            "rate_limit_scope": "shared_route_key_per_cloudflare_location",
            "rate_limit_accuracy": "permissive_eventually_consistent_not_cost_accounting",
            "fixed_model": "gpt-5.6-luna",
            "max_provider_attempts": 1,
            "current_pages_wrangler": "3.114.17",
            "minimum_rate_limit_binding_wrangler": "4.36.0",
            "explicit_owner_activation_required": True,
        }
        for key, expected in expected_public_activation.items():
            if public_activation.get(key) != expected:
                errors.append(f"public_activation.{key} must remain {expected!r}")
        false_flags(
            public_activation,
            ("enabled", "ui_network_enabled", "control_plane_ready"),
            "public_activation",
            errors,
        )
        if public_activation.get("secret_bindings") != ["OPENAI_API_KEY"]:
            errors.append("public_activation.secret_bindings must contain only OPENAI_API_KEY")
        if public_activation.get("production_branches") != ["main", "master"]:
            errors.append("public_activation.production_branches must remain main and master")
        if public_activation.get("production_origins") != [
            "https://ikurabayev.kz",
            "https://www.ikurabayev.kz",
            "https://ikurabayev-kz.pages.dev",
        ]:
            errors.append("public_activation.production_origins must retain the reviewed hosts")
        required_prerequisites = {
            "separate_openai_production_project_and_key",
            "small_hard_spend_limit_and_alerts",
            "cloudflare_rate_limiter_binding",
            "moderation_risk_decision",
            "adversarial_privacy_accessibility_mobile_and_rollback_qa",
            "explicit_owner_activation_approval",
        }
        prerequisites = set(string_list(
            public_activation.get("activation_prerequisites"),
            "public_activation.activation_prerequisites",
            errors,
        ))
        if not required_prerequisites <= prerequisites:
            errors.append("public_activation: required control-plane prerequisites missing")
        if public_activation.get("references") != [
            "https://developers.openai.com/api/docs/guides/production-best-practices",
            "https://developers.openai.com/api/docs/guides/safety-best-practices",
            "https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/",
        ]:
            errors.append("public_activation.references must retain the reviewed official guides")

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
    if provider.get("implementation_references") != [
        "https://developers.openai.com/api/docs/guides/migrate-to-responses",
        "https://developers.openai.com/api/docs/guides/structured-outputs",
    ]:
        errors.append("provider: current Responses and Structured Outputs references are required")
    if provider.get("reference_checked_at") != contract.get("reviewed_at"):
        errors.append("provider: reference_checked_at must match reviewed_at")

    model_selection = provider.get("model_selection")
    if not isinstance(model_selection, dict):
        errors.append("provider.model_selection: expected an object")
    else:
        if model_selection.get("policy") != (
            "private_pilot_luna_selected_with_controlled_terra_fallback"
        ):
            errors.append("provider.model_selection.policy must retain the reviewed pilot selection")
        if model_selection.get("fixed_model") != "gpt-5.6-luna":
            errors.append("provider.model_selection.fixed_model must remain gpt-5.6-luna")
        if model_selection.get("default_model") != "gpt-5.6-luna":
            errors.append("provider.model_selection.default_model must remain gpt-5.6-luna")
        if model_selection.get("allowed_models") != ["gpt-5.6-luna", "gpt-5.6-terra"]:
            errors.append("provider.model_selection.allowed_models must remain Luna and Terra")
        if model_selection.get("selection_issue") != 63:
            errors.append("provider.model_selection.selection_issue must remain 63")
        if model_selection.get("selected_at") != "2026-09-02":
            errors.append("provider.model_selection.selected_at must remain 2026-09-02")
        if model_selection.get("pricing_reference") != (
            "https://developers.openai.com/api/docs/pricing"
        ):
            errors.append("provider.model_selection.pricing_reference must use the official pricing page")
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
        if request_contract.get("structured_output") is not True:
            errors.append("provider.request_contract.structured_output must remain true")

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
    ) != {"decision", "language", "answer", "citations", "refusal_category"}:
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
        prompts = case.get("prompts")
        if not isinstance(prompts, dict) or set(prompts) != set(INITIAL_LANGUAGES):
            errors.append(f"{case_id}: executable RU/EN prompts are required")
        else:
            for prompt_language, prompt in prompts.items():
                if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 600:
                    errors.append(f"{case_id}: invalid {prompt_language} evaluation prompt")
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
    errors = validate_contract(contract, registry, graph)
    validate_backend_files(root, contract, errors)
    run_grounding_check(root, errors)
    return errors


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
    mutation["public_activation"]["enabled"] = True
    tests.append(("premature public activation", mutation, registry, graph, "public_activation.enabled must remain false"))

    mutation = copy.deepcopy(contract)
    mutation["public_activation"]["control_plane_ready"] = True
    tests.append(("unreviewed control plane", mutation, registry, graph, "control_plane_ready must remain false"))

    mutation = copy.deepcopy(contract)
    mutation["public_activation"]["ui_network_enabled"] = True
    tests.append(("premature UI networking", mutation, registry, graph, "ui_network_enabled must remain false"))

    mutation = copy.deepcopy(contract)
    mutation["public_activation"]["rate_limiter_binding"] = ""
    tests.append(("missing public limiter", mutation, registry, graph, "rate_limiter_binding must remain"))

    mutation = copy.deepcopy(contract)
    mutation["public_activation"]["max_provider_attempts"] = 2
    tests.append(("public provider retry", mutation, registry, graph, "max_provider_attempts must remain 1"))

    mutation = copy.deepcopy(contract)
    mutation["lifecycle"]["disabled_route_deployed"] = False
    tests.append(("missing disabled route gate", mutation, registry, graph, "disabled_route_deployed must remain true"))

    mutation = copy.deepcopy(contract)
    mutation["backend_skeleton"]["provider_call_enabled"] = False
    tests.append(("missing private provider path", mutation, registry, graph, "provider_call_enabled must remain True"))

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
        f"Public AI mutation self-tests PASS: {len(tests)}/{len(tests)} bounded "
        "in-memory mutations rejected without filesystem changes."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run bounded in-memory mutation tests after baseline validation",
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
        "Public AI readiness validation PASS: private Preview lifecycle, production "
        "isolation, evidence grounding, refusal suite, and privacy boundary."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
