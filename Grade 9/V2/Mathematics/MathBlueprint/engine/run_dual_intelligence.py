#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import (
    ROOT,
    digest,
    fail,
    load,
    seal_learning_run,
    validate_ground_truth_manifest,
    validate_learning_run,
    validate_schema,
)

POLICY = load(ROOT / "policies" / "math-dual-intelligence-policy.json")
ROLE_KIND = {r: v["intelligence_kind"] for r, v in POLICY["roles"].items()}
ROLE_CLAIM_TYPES = {r: set(v["claim_types"]) for r, v in POLICY["roles"].items()}
OPPOSITE = {"CORE1": "CORE2", "CORE2": "CORE1"}
MILESTONES = ("FIRST_CORE_COMPLETE", "SECOND_CORE_COMPLETE", "CROSS_VALIDATED")


def _bundle(run: dict, bundle_ref: str) -> dict:
    for bundle in run["bundles"]:
        if bundle["bundle_id"] == bundle_ref:
            return bundle
    fail("DUAL_INTELLIGENCE_BUNDLE_UNKNOWN", bundle_ref)


def _evidence_index(manifest: dict) -> dict[str, dict]:
    return {x["evidence_id"]: x for x in manifest["evidence_items"]}


def _validate_inputs(manifest: dict, run: dict, bundle_ref: str) -> dict:
    validate_ground_truth_manifest(manifest)
    validate_learning_run(run)
    if (run["ground_truth_ref"], run["ground_truth_digest"]) != (
        manifest["manifest_id"], manifest["manifest_digest"]
    ):
        fail("DUAL_INTELLIGENCE_GROUND_TRUTH_BINDING_MISMATCH")
    if run["current_state"].startswith("BLOCKED_"):
        fail("DUAL_INTELLIGENCE_RUN_BLOCKED", run["current_state"])
    if run["current_state"] not in {
        "ROUTED", "FIRST_CORE_COMPLETE", "SECOND_CORE_COMPLETE", "CROSS_VALIDATED"
    }:
        fail("DUAL_INTELLIGENCE_REQUIRES_ROUTED_RUN", run["current_state"])
    return _bundle(run, bundle_ref)


def _seal_work_order(order: dict) -> dict:
    out = copy.deepcopy(order)
    identity = {k: v for k, v in out.items() if k not in {"work_order_id", "work_order_digest"}}
    out["work_order_id"] = "MATH-WO-" + digest(identity)[:16]
    out["work_order_digest"] = digest(out, "work_order_digest")
    validate_schema(out, "math-specialist-work-order.schema.json")
    return out


def validate_work_order(order: dict, manifest: dict, run: dict) -> None:
    validate_schema(order, "math-specialist-work-order.schema.json")
    if order["work_order_digest"] != digest(order, "work_order_digest"):
        fail("SPECIALIST_WORK_ORDER_DIGEST_MISMATCH")
    if order["run_ref"] != run["run_id"]:
        fail("SPECIALIST_WORK_ORDER_RUN_MISMATCH")
    bundle = _bundle(run, order["bundle_ref"])
    if (order["ground_truth_ref"], order["ground_truth_digest"]) != (
        manifest["manifest_id"], manifest["manifest_digest"]
    ):
        fail("SPECIALIST_WORK_ORDER_GROUND_TRUTH_MISMATCH")
    if order["intelligence_kind"] != ROLE_KIND[order["role"]]:
        fail("SPECIALIST_WORK_ORDER_INTELLIGENCE_KIND_MISMATCH")
    if set(order["allowed_ground_truth_evidence_refs"]) != set(_evidence_index(manifest)):
        fail("SPECIALIST_WORK_ORDER_GROUND_TRUTH_CONTEXT_INCOMPLETE")
    if order["phase"] == "FIRST_ROLE_ANALYSIS" and order["role"] != bundle["first_role"]:
        fail("SPECIALIST_FIRST_ROLE_MISMATCH")
    if order["phase"] in {"SECOND_ROLE_INDEPENDENT", "SECOND_ROLE_VALIDATION"}:
        if order["role"] != OPPOSITE[bundle["first_role"]]:
            fail("SPECIALIST_SECOND_ROLE_MISMATCH")


def build_first_work_order(manifest: dict, run: dict, bundle_ref: str, agent_instance_id: str) -> dict:
    bundle = _validate_inputs(manifest, run, bundle_ref)
    if not bundle["first_role"]:
        fail("DUAL_INTELLIGENCE_BUNDLE_HAS_NO_FIRST_ROLE", bundle_ref)
    role = bundle["first_role"]
    return _seal_work_order({
        "work_order_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": bundle_ref,
        "role": role,
        "intelligence_kind": ROLE_KIND[role],
        "phase": "FIRST_ROLE_ANALYSIS",
        "agent_instance_id": agent_instance_id,
        "ground_truth_ref": manifest["manifest_id"],
        "ground_truth_digest": manifest["manifest_digest"],
        "allowed_ground_truth_evidence_refs": sorted(_evidence_index(manifest)),
        "upstream_visibility": "WITHHELD",
        "allowed_upstream_package_refs": [],
        "withheld_upstream_package_refs": [],
        "independent_package_ref": None,
        "work_order_digest": "",
    })


def validate_specialist_package(package: dict) -> None:
    validate_schema(package, "math-specialist-package.schema.json")
    if package["package_digest"] != digest(package, "package_digest"):
        fail("SPECIALIST_PACKAGE_DIGEST_MISMATCH", package.get("package_id", ""))
    if package["intelligence_kind"] != ROLE_KIND[package["role"]]:
        fail("SPECIALIST_PACKAGE_INTELLIGENCE_KIND_MISMATCH")
    seen = set()
    for claim in package["claims"]:
        if claim["claim_id"] in seen:
            fail("SPECIALIST_CLAIM_ID_DUPLICATE", claim["claim_id"])
        seen.add(claim["claim_id"])
        if claim["claim_type"] not in ROLE_CLAIM_TYPES[package["role"]]:
            fail("SPECIALIST_CLAIM_TYPE_WRONG_ROLE", claim["claim_type"])
        if claim["claim_digest"] != digest(claim, "claim_digest"):
            fail("SPECIALIST_CLAIM_DIGEST_MISMATCH", claim["claim_id"])
    for claim in package["claims"]:
        unknown = set(claim["dependency_claim_refs"]) - seen
        if unknown:
            fail("SPECIALIST_CLAIM_DEPENDENCY_UNKNOWN", sorted(unknown)[0])


def build_second_independent_work_order(
    manifest: dict,
    run: dict,
    bundle_ref: str,
    first_package: dict,
    agent_instance_id: str,
) -> dict:
    bundle = _validate_inputs(manifest, run, bundle_ref)
    validate_specialist_package(first_package)
    if (first_package["run_ref"], first_package["bundle_ref"]) != (run["run_id"], bundle_ref):
        fail("FIRST_PACKAGE_BINDING_MISMATCH")
    if first_package["phase"] != "FIRST_ROLE_ANALYSIS" or first_package["role"] != bundle["first_role"]:
        fail("FIRST_PACKAGE_ROLE_OR_PHASE_INVALID")
    if first_package["agent_instance_id"] == agent_instance_id:
        fail("SELF_VALIDATION_INSTANCE_REUSE", agent_instance_id)
    role = OPPOSITE[bundle["first_role"]]
    return _seal_work_order({
        "work_order_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": bundle_ref,
        "role": role,
        "intelligence_kind": ROLE_KIND[role],
        "phase": "SECOND_ROLE_INDEPENDENT",
        "agent_instance_id": agent_instance_id,
        "ground_truth_ref": manifest["manifest_id"],
        "ground_truth_digest": manifest["manifest_digest"],
        "allowed_ground_truth_evidence_refs": sorted(_evidence_index(manifest)),
        "upstream_visibility": "WITHHELD",
        "allowed_upstream_package_refs": [],
        "withheld_upstream_package_refs": [first_package["package_id"]],
        "independent_package_ref": None,
        "work_order_digest": "",
    })


def build_validation_work_order(
    manifest: dict,
    run: dict,
    bundle_ref: str,
    first_package: dict,
    independent_package: dict,
) -> dict:
    bundle = _validate_inputs(manifest, run, bundle_ref)
    validate_specialist_package(first_package)
    validate_specialist_package(independent_package)
    if first_package["role"] != bundle["first_role"]:
        fail("VALIDATION_FIRST_PACKAGE_ROLE_MISMATCH")
    if independent_package["role"] != OPPOSITE[bundle["first_role"]]:
        fail("VALIDATION_SECOND_PACKAGE_ROLE_MISMATCH")
    if first_package["agent_instance_id"] == independent_package["agent_instance_id"]:
        fail("SELF_VALIDATION_INSTANCE_REUSE", first_package["agent_instance_id"])
    if independent_package["phase"] != "SECOND_ROLE_INDEPENDENT":
        fail("INDEPENDENT_PACKAGE_PHASE_INVALID")
    if not independent_package["sealed_before_upstream_exposure"]:
        fail("INDEPENDENT_PACKAGE_NOT_SEALED_BEFORE_VALIDATION")
    return _seal_work_order({
        "work_order_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": bundle_ref,
        "role": independent_package["role"],
        "intelligence_kind": ROLE_KIND[independent_package["role"]],
        "phase": "SECOND_ROLE_VALIDATION",
        "agent_instance_id": independent_package["agent_instance_id"],
        "ground_truth_ref": manifest["manifest_id"],
        "ground_truth_digest": manifest["manifest_digest"],
        "allowed_ground_truth_evidence_refs": sorted(_evidence_index(manifest)),
        "upstream_visibility": "VISIBLE",
        "allowed_upstream_package_refs": sorted([
            first_package["package_id"], independent_package["package_id"]
        ]),
        "withheld_upstream_package_refs": [],
        "independent_package_ref": independent_package["package_id"],
        "work_order_digest": "",
    })


def materialize_context(
    manifest: dict,
    run: dict,
    work_order: dict,
    *,
    packages: list[dict] | None = None,
) -> dict:
    _validate_inputs(manifest, run, work_order["bundle_ref"])
    validate_work_order(work_order, manifest, run)
    supplied: dict[str, dict] = {}
    for package in packages or []:
        validate_specialist_package(package)
        supplied[package["package_id"]] = package

    upstream = []
    for ref in work_order["allowed_upstream_package_refs"]:
        if ref not in supplied:
            fail("AUTHORIZED_UPSTREAM_PACKAGE_NOT_SUPPLIED", ref)
        upstream.append({"package_ref": ref, "package_digest": supplied[ref]["package_digest"]})

    idx = _evidence_index(manifest)
    items = [{
        "evidence_id": eid,
        "evidence_type": idx[eid]["evidence_type"],
        "availability": idx[eid]["availability"],
        "ref": idx[eid]["ref"],
        "digest": idx[eid]["digest"],
    } for eid in work_order["allowed_ground_truth_evidence_refs"]]
    items.sort(key=lambda x: x["evidence_id"])
    upstream.sort(key=lambda x: x["package_ref"])

    context = {
        "context_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": work_order["bundle_ref"],
        "work_order_ref": work_order["work_order_id"],
        "work_order_digest": work_order["work_order_digest"],
        "role": work_order["role"],
        "phase": work_order["phase"],
        "agent_instance_id": work_order["agent_instance_id"],
        "context_mode": (
            "GROUND_TRUTH_PLUS_UPSTREAM_VALIDATION"
            if work_order["phase"] == "SECOND_ROLE_VALIDATION"
            else "GROUND_TRUTH_ONLY"
        ),
        "ground_truth_items": items,
        "upstream_packages": upstream,
        "withheld_upstream_package_refs": copy.deepcopy(work_order["withheld_upstream_package_refs"]),
        "context_digest": "",
    }
    identity = {k: v for k, v in context.items() if k not in {"context_id", "context_digest"}}
    context["context_id"] = "MATH-CTX-" + digest(identity)[:16]
    context["context_digest"] = digest(context, "context_digest")
    validate_schema(context, "math-agent-context-manifest.schema.json")
    if work_order["phase"] in {"FIRST_ROLE_ANALYSIS", "SECOND_ROLE_INDEPENDENT"} and upstream:
        fail("INDEPENDENCE_FIREWALL_UPSTREAM_LEAK")
    return context


def _validate_context(context: dict, work_order: dict, run: dict) -> None:
    validate_schema(context, "math-agent-context-manifest.schema.json")
    if context["context_digest"] != digest(context, "context_digest"):
        fail("AGENT_CONTEXT_DIGEST_MISMATCH")
    expected = {
        "run_ref": run["run_id"],
        "bundle_ref": work_order["bundle_ref"],
        "work_order_ref": work_order["work_order_id"],
        "work_order_digest": work_order["work_order_digest"],
        "role": work_order["role"],
        "phase": work_order["phase"],
        "agent_instance_id": work_order["agent_instance_id"],
    }
    for key, value in expected.items():
        if context[key] != value:
            fail("AGENT_CONTEXT_BINDING_MISMATCH", key)


def seal_specialist_package(
    manifest: dict,
    run: dict,
    work_order: dict,
    context: dict,
    draft: dict,
) -> dict:
    bundle = _validate_inputs(manifest, run, work_order["bundle_ref"])
    validate_work_order(work_order, manifest, run)
    _validate_context(context, work_order, run)
    if work_order["phase"] not in {"FIRST_ROLE_ANALYSIS", "SECOND_ROLE_INDEPENDENT"}:
        fail("SPECIALIST_PACKAGE_CANNOT_BE_AUTHORED_IN_VALIDATION_PHASE")
    if context["context_mode"] != "GROUND_TRUTH_ONLY" or context["upstream_packages"]:
        fail("SPECIALIST_PACKAGE_CONTEXT_NOT_INDEPENDENT")

    raw_claims = draft.get("claims")
    if not isinstance(raw_claims, list) or not raw_claims:
        fail("SPECIALIST_PACKAGE_CLAIMS_REQUIRED")
    evidence = _evidence_index(manifest)
    local_to_id: dict[str, str] = {}
    prepared = []
    for raw in raw_claims:
        local_key = str(raw.get("local_key") or "").strip()
        if not local_key or local_key in local_to_id:
            fail("SPECIALIST_CLAIM_LOCAL_KEY_INVALID", local_key)
        ctype = raw.get("claim_type")
        if ctype not in ROLE_CLAIM_TYPES[work_order["role"]]:
            fail("SPECIALIST_CLAIM_TYPE_WRONG_ROLE", str(ctype))
        subtopic = raw.get("subtopic_ref")
        if subtopic not in bundle["subtopic_refs"]:
            fail("SPECIALIST_CLAIM_SUBTOPIC_OUTSIDE_BUNDLE", str(subtopic))
        refs = sorted(set(raw.get("evidence_refs") or []))
        if not refs:
            fail("SPECIALIST_CLAIM_EVIDENCE_REQUIRED", local_key)
        unknown = set(refs) - set(evidence)
        if unknown:
            fail("SPECIALIST_CLAIM_EVIDENCE_UNKNOWN", sorted(unknown)[0])
        confidence = raw.get("confidence", "UNKNOWN")
        if confidence not in {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}:
            fail("SPECIALIST_CLAIM_CONFIDENCE_UNKNOWN", str(confidence))
        if all(evidence[x]["availability"] == "ABSENT" for x in refs) and confidence != "UNKNOWN":
            fail("ABSENT_EVIDENCE_CANNOT_SUPPORT_POSITIVE_CONFIDENCE", local_key)
        statement = str(raw.get("statement") or "").strip()
        if not statement:
            fail("SPECIALIST_CLAIM_STATEMENT_REQUIRED", local_key)
        claim_id = "MATH-CL-" + digest({
            "role": work_order["role"],
            "claim_type": ctype,
            "statement": statement,
            "subtopic_ref": subtopic,
            "evidence_refs": refs,
        })[:16]
        local_to_id[local_key] = claim_id
        prepared.append((local_key, claim_id, raw, ctype, statement, subtopic, refs, confidence))

    claims = []
    for local_key, claim_id, raw, ctype, statement, subtopic, refs, confidence in prepared:
        dep_keys = raw.get("dependency_local_keys") or []
        if len(dep_keys) != len(set(dep_keys)):
            fail("SPECIALIST_CLAIM_DEPENDENCY_DUPLICATE", local_key)
        try:
            deps = sorted(local_to_id[x] for x in dep_keys)
        except KeyError as exc:
            fail("SPECIALIST_CLAIM_DEPENDENCY_LOCAL_KEY_UNKNOWN", str(exc.args[0]))
        claim = {
            "claim_id": claim_id,
            "claim_type": ctype,
            "statement": statement,
            "subtopic_ref": subtopic,
            "evidence_refs": refs,
            "confidence": confidence,
            "dependency_claim_refs": deps,
            "unresolved_issue_refs": sorted(set(raw.get("unresolved_issue_refs") or [])),
            "claim_digest": "",
        }
        claim["claim_digest"] = digest(claim, "claim_digest")
        claims.append(claim)
    claims.sort(key=lambda x: (x["subtopic_ref"], x["claim_type"], x["claim_id"]))

    package = {
        "package_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": work_order["bundle_ref"],
        "role": work_order["role"],
        "intelligence_kind": work_order["intelligence_kind"],
        "phase": work_order["phase"],
        "agent_instance_id": work_order["agent_instance_id"],
        "work_order_ref": work_order["work_order_id"],
        "work_order_digest": work_order["work_order_digest"],
        "context_ref": context["context_id"],
        "context_digest": context["context_digest"],
        "ground_truth_ref": manifest["manifest_id"],
        "ground_truth_digest": manifest["manifest_digest"],
        "source_visibility": "GROUND_TRUTH_ONLY",
        "upstream_package_visible": False,
        "sealed_before_upstream_exposure": True,
        "claims": claims,
        "package_digest": "",
    }
    identity = {k: v for k, v in package.items() if k not in {"package_id", "package_digest"}}
    package["package_id"] = "MATH-SP-" + digest(identity)[:16]
    package["package_digest"] = digest(package, "package_digest")
    validate_specialist_package(package)
    return package


def build_cross_validation(
    manifest: dict,
    run: dict,
    first_package: dict,
    independent_package: dict,
    validation_work_order: dict,
    validation_context: dict,
    authored: dict,
) -> dict:
    _validate_inputs(manifest, run, first_package["bundle_ref"])
    validate_specialist_package(first_package)
    validate_specialist_package(independent_package)
    validate_work_order(validation_work_order, manifest, run)
    _validate_context(validation_context, validation_work_order, run)
    if first_package["agent_instance_id"] == independent_package["agent_instance_id"]:
        fail("SELF_VALIDATION_INSTANCE_REUSE", first_package["agent_instance_id"])
    if validation_work_order["phase"] != "SECOND_ROLE_VALIDATION":
        fail("CROSS_VALIDATION_WORK_ORDER_PHASE_INVALID")
    if validation_work_order["agent_instance_id"] != independent_package["agent_instance_id"]:
        fail("CROSS_VALIDATION_AGENT_NOT_SECOND_INSTANCE")
    if independent_package["phase"] != "SECOND_ROLE_INDEPENDENT":
        fail("INDEPENDENT_PACKAGE_PHASE_INVALID")
    if not independent_package["sealed_before_upstream_exposure"]:
        fail("INDEPENDENT_PACKAGE_NOT_SEALED_BEFORE_VALIDATION")
    if validation_context["context_mode"] != "GROUND_TRUTH_PLUS_UPSTREAM_VALIDATION":
        fail("CROSS_VALIDATION_CONTEXT_NOT_VISIBLE")
    visible = {x["package_ref"] for x in validation_context["upstream_packages"]}
    if visible != {first_package["package_id"], independent_package["package_id"]}:
        fail("CROSS_VALIDATION_CONTEXT_PACKAGE_SET_INVALID")

    first_claims = {x["claim_id"]: x for x in first_package["claims"]}
    second_claims = {x["claim_id"]: x for x in independent_package["claims"]}
    evidence_ids = set(_evidence_index(manifest))
    records = []
    seen = set()
    for raw in authored.get("records") or []:
        claim_ref = raw.get("first_claim_ref")
        if claim_ref not in first_claims:
            fail("CROSS_VALIDATION_FIRST_CLAIM_UNKNOWN", str(claim_ref))
        if claim_ref in seen:
            fail("CROSS_VALIDATION_FIRST_CLAIM_DUPLICATE", claim_ref)
        seen.add(claim_ref)
        classification = raw.get("classification")
        if classification not in {
            "CONFIRMED", "REFINED", "UNSUPPORTED", "CONTRADICTED", "OUT_OF_SCOPE", "UNKNOWN"
        }:
            fail("CROSS_VALIDATION_CLASSIFICATION_UNKNOWN", str(classification))
        refs = sorted(set(raw.get("ground_truth_evidence_refs") or []))
        unknown = set(refs) - evidence_ids
        if unknown:
            fail("CROSS_VALIDATION_EVIDENCE_UNKNOWN", sorted(unknown)[0])
        if classification != "UNKNOWN" and not refs:
            fail("CROSS_VALIDATION_EVIDENCE_REQUIRED", claim_ref)
        refined = raw.get("refined_statement")
        if classification == "REFINED" and not str(refined or "").strip():
            fail("CROSS_VALIDATION_REFINED_STATEMENT_REQUIRED", claim_ref)
        if classification != "REFINED" and refined is not None:
            fail("CROSS_VALIDATION_REFINED_STATEMENT_FORBIDDEN", claim_ref)
        rationale = str(raw.get("rationale") or "").strip()
        if not rationale:
            fail("CROSS_VALIDATION_RATIONALE_REQUIRED", claim_ref)
        rec = {
            "first_claim_ref": claim_ref,
            "classification": classification,
            "ground_truth_evidence_refs": refs,
            "rationale": rationale,
            "refined_statement": refined,
        }
        records.append({"record_id": "MATH-XR-" + digest(rec)[:16], **rec})
    missing_first = set(first_claims) - seen
    if missing_first:
        fail("CROSS_VALIDATION_FIRST_CLAIM_UNVALIDATED", sorted(missing_first)[0])

    missing_findings = []
    seen_missing = set()
    for raw in authored.get("missing_findings") or []:
        second_ref = raw.get("second_claim_ref")
        if second_ref not in second_claims:
            fail("CROSS_VALIDATION_SECOND_CLAIM_UNKNOWN", str(second_ref))
        if second_ref in seen_missing:
            fail("CROSS_VALIDATION_MISSING_FINDING_DUPLICATE", second_ref)
        seen_missing.add(second_ref)
        refs = sorted(set(raw.get("ground_truth_evidence_refs") or []))
        if not refs:
            fail("CROSS_VALIDATION_MISSING_EVIDENCE_REQUIRED", second_ref)
        unknown = set(refs) - evidence_ids
        if unknown:
            fail("CROSS_VALIDATION_EVIDENCE_UNKNOWN", sorted(unknown)[0])
        rationale = str(raw.get("rationale") or "").strip()
        if not rationale:
            fail("CROSS_VALIDATION_RATIONALE_REQUIRED", second_ref)
        rec = {
            "classification": "MISSING",
            "second_claim_ref": second_ref,
            "ground_truth_evidence_refs": refs,
            "rationale": rationale,
        }
        missing_findings.append({"record_id": "MATH-XR-" + digest(rec)[:16], **rec})

    records.sort(key=lambda x: x["first_claim_ref"])
    missing_findings.sort(key=lambda x: x["second_claim_ref"])
    validation = {
        "validation_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": first_package["bundle_ref"],
        "first_role": first_package["role"],
        "second_role": independent_package["role"],
        "validator_agent_instance_id": independent_package["agent_instance_id"],
        "first_package_ref": first_package["package_id"],
        "first_package_digest": first_package["package_digest"],
        "independent_package_ref": independent_package["package_id"],
        "independent_package_digest": independent_package["package_digest"],
        "validation_work_order_ref": validation_work_order["work_order_id"],
        "validation_work_order_digest": validation_work_order["work_order_digest"],
        "validation_context_ref": validation_context["context_id"],
        "validation_context_digest": validation_context["context_digest"],
        "independent_package_sealed_before_validation": True,
        "records": records,
        "missing_findings": missing_findings,
        "validation_digest": "",
    }
    identity = {k: v for k, v in validation.items() if k not in {"validation_id", "validation_digest"}}
    validation["validation_id"] = "MATH-XV-" + digest(identity)[:16]
    validation["validation_digest"] = digest(validation, "validation_digest")
    validate_schema(validation, "math-cross-validation.schema.json")
    return validation


def apply_cross_validation(run: dict, first_package: dict, independent_package: dict, validation: dict) -> dict:
    validate_learning_run(run)
    validate_specialist_package(first_package)
    validate_specialist_package(independent_package)
    validate_schema(validation, "math-cross-validation.schema.json")
    if validation["validation_digest"] != digest(validation, "validation_digest"):
        fail("CROSS_VALIDATION_DIGEST_MISMATCH")
    if validation["run_ref"] != run["run_id"]:
        fail("CROSS_VALIDATION_RUN_MISMATCH")
    if validation["first_package_ref"] != first_package["package_id"]:
        fail("CROSS_VALIDATION_FIRST_PACKAGE_BINDING_MISMATCH")
    if validation["independent_package_ref"] != independent_package["package_id"]:
        fail("CROSS_VALIDATION_SECOND_PACKAGE_BINDING_MISMATCH")

    out = copy.deepcopy(run)
    target = _bundle(out, validation["bundle_ref"])
    by_role = {first_package["role"]: first_package, independent_package["role"]: independent_package}
    if set(by_role) != {"CORE1", "CORE2"}:
        fail("DUAL_INTELLIGENCE_ROLE_PAIR_INCOMPLETE")
    target["core1_execution_ref"] = by_role["CORE1"]["package_id"]
    target["core2_execution_ref"] = by_role["CORE2"]["package_id"]
    target["cross_validation_ref"] = validation["validation_id"]

    def first_done(bundle: dict) -> bool:
        return bool(
            bundle["core1_execution_ref"]
            if bundle["first_role"] == "CORE1"
            else bundle["core2_execution_ref"]
        )

    conditions = {
        "FIRST_CORE_COMPLETE": bool(out["bundles"]) and all(first_done(b) for b in out["bundles"]),
        "SECOND_CORE_COMPLETE": bool(out["bundles"]) and all(
            b["core1_execution_ref"] and b["core2_execution_ref"] for b in out["bundles"]
        ),
        "CROSS_VALIDATED": bool(out["bundles"]) and all(b["cross_validation_ref"] for b in out["bundles"]),
    }
    existing = {x["state"] for x in out["state_history"]}
    for state in MILESTONES:
        if conditions[state] and state not in existing:
            out["current_state"] = state
            out["state_history"].append({
                "sequence": len(out["state_history"]),
                "state": state,
                "reason_code": "DUAL_INTELLIGENCE_" + state,
            })
            existing.add(state)
    return seal_learning_run(out)


def build_session(
    run: dict,
    first_work_order: dict,
    first_context: dict,
    first_package: dict,
    second_work_order: dict,
    second_context: dict,
    independent_package: dict,
    validation_work_order: dict,
    validation_context: dict,
    validation: dict,
) -> dict:
    if first_package["agent_instance_id"] == independent_package["agent_instance_id"]:
        fail("SELF_VALIDATION_INSTANCE_REUSE", first_package["agent_instance_id"])
    session = {
        "session_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": first_package["bundle_ref"],
        "first_role": first_package["role"],
        "second_role": independent_package["role"],
        "first_agent_instance_id": first_package["agent_instance_id"],
        "second_agent_instance_id": independent_package["agent_instance_id"],
        "first_work_order_ref": first_work_order["work_order_id"],
        "first_context_ref": first_context["context_id"],
        "first_package_ref": first_package["package_id"],
        "second_independent_work_order_ref": second_work_order["work_order_id"],
        "second_independent_context_ref": second_context["context_id"],
        "second_independent_package_ref": independent_package["package_id"],
        "validation_work_order_ref": validation_work_order["work_order_id"],
        "validation_context_ref": validation_context["context_id"],
        "cross_validation_ref": validation["validation_id"],
        "status": "CROSS_VALIDATED",
        "session_digest": "",
    }
    identity = {k: v for k, v in session.items() if k not in {"session_id", "session_digest"}}
    session["session_id"] = "MATH-DIS-" + digest(identity)[:16]
    session["session_digest"] = digest(session, "session_digest")
    validate_schema(session, "math-dual-intelligence-session.schema.json")
    return session


def _write(path: str, value: dict) -> None:
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Adaptive Math Blueprint dual-intelligence runtime.")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("first-order")
    p.add_argument("--ground-truth", required=True); p.add_argument("--run", required=True)
    p.add_argument("--bundle-ref", required=True); p.add_argument("--agent-instance-id", required=True); p.add_argument("--out", required=True)

    p = sub.add_parser("second-order")
    p.add_argument("--ground-truth", required=True); p.add_argument("--run", required=True)
    p.add_argument("--bundle-ref", required=True); p.add_argument("--first-package", required=True)
    p.add_argument("--agent-instance-id", required=True); p.add_argument("--out", required=True)

    p = sub.add_parser("context")
    p.add_argument("--ground-truth", required=True); p.add_argument("--run", required=True)
    p.add_argument("--work-order", required=True); p.add_argument("--package", action="append", default=[]); p.add_argument("--out", required=True)

    p = sub.add_parser("seal-package")
    p.add_argument("--ground-truth", required=True); p.add_argument("--run", required=True)
    p.add_argument("--work-order", required=True); p.add_argument("--context", required=True)
    p.add_argument("--draft", required=True); p.add_argument("--out", required=True)

    p = sub.add_parser("validation-order")
    p.add_argument("--ground-truth", required=True); p.add_argument("--run", required=True)
    p.add_argument("--bundle-ref", required=True); p.add_argument("--first-package", required=True)
    p.add_argument("--independent-package", required=True); p.add_argument("--out", required=True)

    p = sub.add_parser("cross-validate")
    p.add_argument("--ground-truth", required=True); p.add_argument("--run", required=True)
    p.add_argument("--first-work-order", required=True); p.add_argument("--first-context", required=True)
    p.add_argument("--first-package", required=True); p.add_argument("--second-work-order", required=True)
    p.add_argument("--second-context", required=True); p.add_argument("--independent-package", required=True)
    p.add_argument("--validation-work-order", required=True); p.add_argument("--validation-context", required=True)
    p.add_argument("--validation-input", required=True); p.add_argument("--out-validation", required=True)
    p.add_argument("--out-session", required=True); p.add_argument("--out-run", required=True)

    args = ap.parse_args()
    manifest, run = load(args.ground_truth), load(args.run)
    if args.command == "first-order":
        result = build_first_work_order(manifest, run, args.bundle_ref, args.agent_instance_id)
        _write(args.out, result)
    elif args.command == "second-order":
        result = build_second_independent_work_order(
            manifest, run, args.bundle_ref, load(args.first_package), args.agent_instance_id
        )
        _write(args.out, result)
    elif args.command == "context":
        result = materialize_context(
            manifest, run, load(args.work_order), packages=[load(x) for x in args.package]
        )
        _write(args.out, result)
    elif args.command == "seal-package":
        result = seal_specialist_package(
            manifest, run, load(args.work_order), load(args.context), load(args.draft)
        )
        _write(args.out, result)
    elif args.command == "validation-order":
        result = build_validation_work_order(
            manifest, run, args.bundle_ref, load(args.first_package), load(args.independent_package)
        )
        _write(args.out, result)
    else:
        first_order, first_context = load(args.first_work_order), load(args.first_context)
        first_package = load(args.first_package)
        second_order, second_context = load(args.second_work_order), load(args.second_context)
        independent_package = load(args.independent_package)
        validation_order, validation_context = load(args.validation_work_order), load(args.validation_context)
        validation = build_cross_validation(
            manifest, run, first_package, independent_package,
            validation_order, validation_context, load(args.validation_input)
        )
        updated = apply_cross_validation(run, first_package, independent_package, validation)
        session = build_session(
            updated, first_order, first_context, first_package,
            second_order, second_context, independent_package,
            validation_order, validation_context, validation
        )
        _write(args.out_validation, validation); _write(args.out_session, session); _write(args.out_run, updated)
        result = {"validation_id": validation["validation_id"], "session_id": session["session_id"], "run_state": updated["current_state"]}
    print(json.dumps({"status": "PASS", "command": args.command, "result": result}, indent=2))


if __name__ == "__main__":
    main()
