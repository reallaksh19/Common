#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REPO = ROOT.parents[3]
SHARED_GATE = REPO / "Grade 9" / "V2" / "Shared" / "EngineeringGate"
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(SHARED_GATE / "engine"))

from compile_domain_prerequisite_closure import compile_domain_prerequisite_closure  # noqa: E402
from compile_engineering_closure import compile_closure  # noqa: E402
from compile_join import compile_join  # noqa: E402
from compile_scoped_evidence import compile_scoped_evidence  # noqa: E402
from evaluate_readiness import build_envelope  # noqa: E402
from governor import route_scoped  # noqa: E402


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        raise AssertionError("STRESS_TEST_REF_MISSING:" + rel)
    return json.loads(path.read_text(encoding="utf-8"))


def load_repo(ref: str) -> dict[str, Any]:
    rel = Path(ref)
    if rel.is_absolute() or ".." in rel.parts:
        raise AssertionError("STRESS_TEST_REPO_REF_OUTSIDE_REPOSITORY:" + ref)
    path = REPO / rel
    if not path.exists() or not path.is_file():
        raise AssertionError("STRESS_TEST_REPO_REF_MISSING:" + ref)
    return json.loads(path.read_text(encoding="utf-8"))


def exists_ref(rel: str | None) -> bool:
    return bool(rel and (ROOT / rel).exists())


def core(status: str, blockers: list[str] | None = None) -> dict[str, Any]:
    return {"status": status, "blockers": sorted(set(blockers or []))}


def compile_stress_test(request: dict[str, Any]) -> dict[str, Any]:
    Draft202012Validator(load("contracts/seven-core-stress-test-request.schema.json")).validate(request)

    envelope = load(request["scope_envelope_ref"])
    if int(request["grade"]) != int(envelope["grade"]) or request["requested_curriculum"] != envelope["requested_curriculum"]:
        raise AssertionError("STRESS_TEST_SCOPE_REQUEST_MISMATCH")

    scoped = compile_scoped_evidence(envelope)
    routing = route_scoped(scoped)["routing_decision"]

    engineering_request = load(request["engineering_request_ref"])
    engineering_manifest = load(request["engineering_manifest_ref"])
    engineering = compile_closure(engineering_request, engineering_manifest)
    if set(scoped["required_gate_ids"]) != set(engineering_manifest["required_gate_ids"]):
        raise AssertionError("STRESS_TEST_SCOPE_ENGINEERING_GATE_MISMATCH")

    authority_refs = list(request["domain_authority_refs"])
    authority_receipts = [load_repo(ref) for ref in authority_refs]
    domain = compile_domain_prerequisite_closure(engineering, authority_receipts, authority_refs)
    readiness = build_envelope(engineering_request, engineering_manifest, engineering, domain)
    join = compile_join(load(request["join_spec_ref"]), assessment_coverage=scoped["assessment_coverage"])

    route_value = routing["final_route"]
    engineering_ready = readiness["dimensions"]["technical"] == "READY"
    semantic_present = scoped["evidence"]["sources"]["semantic_source"]["availability"] != "ABSENT"
    curriculum_ready = scoped["curriculum_status"] == "SUPPORTED_BY_REPOSITORY_AUTHORITY"
    domain_ready = readiness["dimensions"]["external_prerequisites"] == "READY"
    control_present = exists_ref(request.get("control_state_ref"))
    core1a_release = exists_ref(request.get("core1a_release_ref"))
    core1b_release = exists_ref(request.get("core1b_release_ref"))
    core2a_pool = exists_ref(request.get("core2a_legal_pool_ref"))
    exact_product = exists_ref(request.get("exact_product_ref"))
    coverage_state = scoped["assessment_coverage"]["state"]

    cores: dict[str, Any] = {}
    cores["CORE0"] = core("PASS_ROUTING_ONLY" if route_value != "BLOCK" else "BLOCKED_ROUTING", [] if route_value != "BLOCK" else ["ROUTING_BLOCK"])

    blockers: list[str] = []
    if not engineering_ready:
        blockers.append("TECHNICAL_ENGINEERING_NOT_READY")
    if not semantic_present:
        blockers.append("TARGET_SEMANTIC_AUTHORITY_ABSENT")
    if not curriculum_ready:
        blockers.append("G_DOMAIN_CURRICULUM_AUTHORITY_HELD")
    cores["CORE1"] = core("PREPARED_NOT_RELEASED" if engineering_ready and semantic_present else "BLOCKED", blockers)

    blockers = []
    if not engineering_ready:
        blockers.append("TECHNICAL_ENGINEERING_NOT_READY")
    if not join["assimilation_ready"]:
        blockers.append("JOIN_NOT_ASSIMILATION_READY")
    if not domain_ready:
        blockers.append("EXTERNAL_DOMAIN_PREREQUISITES_HELD")
    if not control_present:
        blockers.append("MISSING_GOVERNED_CONTROL_STATE")
    if not curriculum_ready:
        blockers.append("G_DOMAIN_CURRICULUM_AUTHORITY_HELD")
    cores["CORE1A"] = core("READY_FOR_STAGE_MACHINE" if not blockers else "BLOCKED_BEFORE_STAGE_RELEASE", blockers)

    cores["CORE1B"] = core(
        "READY_FOR_RUNTIME" if core1a_release and core1b_release else "NOT_INSTANTIATED",
        [] if core1a_release and core1b_release else ["NO_RELEASED_CORE1A_AUTHORITY"],
    )

    if coverage_state == "VERIFIED_NO_TARGET_DEMAND":
        cores["CORE2"] = core("HELD_VERIFIED_NO_TARGET_DEMAND")
    elif coverage_state == "DEMANDS_PRESENT":
        cores["CORE2"] = core("READY_FOR_CUSTODY")
    else:
        cores["CORE2"] = core("BLOCKED_COVERAGE_UNKNOWN", ["TARGET_ASSESSMENT_COVERAGE_UNKNOWN"])

    core2_has_item = coverage_state == "DEMANDS_PRESENT"
    cores["CORE2A"] = core(
        "READY_FOR_LEGAL_POOL" if core2_has_item and core2a_pool else "NOT_INSTANTIATED_NO_LEGAL_ITEM",
        [] if core2_has_item and core2a_pool else ["NO_LEGAL_TARGET_ITEM"],
    )
    cores["CORE2B"] = core(
        "READY_FOR_TRANSFER" if core2a_pool and core1b_release else "NOT_INSTANTIATED_UPSTREAM",
        [] if core2a_pool and core1b_release else ["CORE2A_OR_CORE1B_RELEASE_MISSING"],
    )

    def technical_downstream(consumer: str, locally_instantiated: bool, absent_state: str) -> str:
        if not locally_instantiated:
            return absent_state
        permission = readiness["consumer_permissions"].get(consumer)
        return "READY" if permission and permission["status"] == "ALLOWED" else "BLOCKED"

    publication_permission = readiness["consumer_permissions"].get("PUBLICATION")
    publication_state = (
        "NOT_AUTHORIZED"
        if publication_permission and publication_permission["status"] == "NOT_AUTHORIZED"
        else "BLOCKED"
    )

    downstream = {
        "CCU": technical_downstream("CCU", core1a_release or core2a_pool, "NOT_INSTANTIATED"),
        "CDAU": technical_downstream("CDAU", (core1a_release and core1b_release) or core2a_pool, "NOT_INSTANTIATED"),
        "SDU": technical_downstream("SDU", core1a_release, "NOT_ISSUED"),
        "LAU": technical_downstream("LAU", core2a_pool, "NOT_ISSUED"),
        "CONCEPT_TTU": technical_downstream("TTU", core1a_release, "NOT_INSTANTIATED"),
        "PROBLEM_TTU": technical_downstream("TTU", core2a_pool, "NOT_INSTANTIATED"),
        "PUBLICATION": publication_state,
        "HUMAN_REVIEW": "READY" if exact_product else "NOT_RUN",
    }

    violations: list[str] = []
    forbidden = {"PASS_BY_NONFABRICATION", "PASS_FAIL_CLOSED_DIFFERENTIATION"}
    for name, state in cores.items():
        if state["status"] in forbidden:
            violations.append("FORBIDDEN_SURROGATE_PASS_LABEL:" + name)
    if cores["CORE2A"]["status"] == "READY_FOR_LEGAL_POOL" and cores["CORE2"]["status"] != "READY_FOR_CUSTODY":
        violations.append("CORE2A_READY_WITHOUT_CORE2_CUSTODY")
    if cores["CORE2B"]["status"] == "READY_FOR_TRANSFER" and (not core2a_pool or not core1b_release):
        violations.append("CORE2B_READY_WITHOUT_REQUIRED_UPSTREAM")
    if readiness["publication_authorization"] != "NOT_IMPLIED":
        violations.append("ENGINEERING_GATE_PUBLICATION_AUTHORIZATION_NOT_INDEPENDENT")
    if publication_permission and publication_permission["status"] != "NOT_AUTHORIZED":
        violations.append("ENGINEERING_GATE_PUBLICATION_CONSUMER_AUTHORIZED")
    if downstream["PUBLICATION"] in {"PASS", "READY"}:
        violations.append("PUBLICATION_AUTHORIZATION_INFERRED")
    if route_value == "CORE2_FIRST" and coverage_state == "VERIFIED_NO_TARGET_DEMAND" and scoped["scope_kind"] != "TOPIC":
        violations.append("TARGET_ROUTE_REUSED_TOPIC_QUESTION_RICHNESS")

    receipt = {
        "schema_version": "1.0.0",
        "stress_test_id": request["stress_test_id"],
        "subject": "PHYSICS",
        "grade": request["grade"],
        "requested_curriculum": request["requested_curriculum"],
        "scope": {
            "kind": scoped["scope_kind"],
            "ref": scoped["scope_ref"],
            "topic_id": scoped["topic_id"],
            "scope_digest": scoped["scope_digest"],
            "scoped_evidence_receipt_digest": scoped["receipt_digest"],
        },
        "curriculum_status": scoped["curriculum_status"],
        "routing": {
            "target_route": route_value,
            "matched_rule_id": routing["matched_rule_id"],
            "scope_consistent": True,
        },
        "engineering": {
            "closure_status": engineering["closure_status"],
            "closure_digest": engineering["closure_digest"],
            "gate_states": engineering["gate_states"],
        },
        "domain_prerequisites": {
            "closure_status": domain["closure_status"],
            "closure_digest": domain["closure_digest"],
            "prerequisites": domain["prerequisites"],
            "demands": domain["demands"],
        },
        "join": {
            "join_status": join["join_status"],
            "assimilation_ready": join["assimilation_ready"],
            "assessment_coverage_state": coverage_state,
            "join_digest": join["join_digest"],
        },
        "cores": cores,
        "downstream": downstream,
        "architecture_violations": sorted(set(violations)),
        "final_verdict": "STRESS_TEST_PASS" if not violations else "STRESS_TEST_FAIL",
        "receipt_digest": "",
    }
    receipt["receipt_digest"] = digest({k: v for k, v in receipt.items() if k != "receipt_digest"})
    Draft202012Validator(load("contracts/seven-core-stress-test-receipt.schema.json")).validate(receipt)
    return receipt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("request", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    receipt = compile_stress_test(json.loads(args.request.read_text(encoding="utf-8")))
    text = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
