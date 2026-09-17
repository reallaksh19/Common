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

from blueprint_common import ROOT, digest, fail, load, seal_learning_run, validate_learning_run, validate_schema
from run_dual_intelligence import validate_specialist_package

POLICY = load(ROOT / "policies" / "math-assimilation-join-policy.json")
ADMISSIBLE_FIRST = {"CONFIRMED", "REFINED"}
CONFLICT_CLASSES = {"UNSUPPORTED", "CONTRADICTED", "OUT_OF_SCOPE"}
GAP_MAP = POLICY["learner_gap_mapping"]


def _bundle(run: dict, bundle_ref: str) -> dict:
    for bundle in run["bundles"]:
        if bundle["bundle_id"] == bundle_ref:
            return bundle
    fail("ASSIMILATION_BUNDLE_UNKNOWN", bundle_ref)


def validate_learner_state(state: dict, run: dict, bundle_ref: str) -> None:
    validate_schema(state, "math-learner-capability-state.schema.json")
    if state["state_digest"] != digest(state, "state_digest"):
        fail("LEARNER_CAPABILITY_STATE_DIGEST_MISMATCH")
    if state["run_ref"] != run["run_id"] or state["bundle_ref"] != bundle_ref:
        fail("LEARNER_CAPABILITY_STATE_BINDING_MISMATCH")
    if state["prior_percent"] != run["control_plane"]["learner_prior_percent"]:
        fail("LEARNER_PRIOR_PROVENANCE_MISMATCH")
    seen = set()
    for row in state["capabilities"]:
        ref = row["capability_ref"]
        if ref in seen:
            fail("LEARNER_CAPABILITY_DUPLICATE", ref)
        seen.add(ref)
        if row["basis"] == "UNKNOWN" and row["readiness"] != "UNKNOWN":
            fail("UNKNOWN_BASIS_CANNOT_ASSERT_READINESS", ref)
        if row["basis"] == "LEARNER_EVIDENCE" and not row["evidence_refs"]:
            fail("LEARNER_EVIDENCE_BASIS_WITHOUT_EVIDENCE", ref)
        if row["basis"] == "OWNER_DECLARED_BASELINE" and not row["owner_control_ref"]:
            fail("OWNER_BASELINE_WITHOUT_CONTROL_REF", ref)


def seal_learner_state(run: dict, bundle_ref: str, draft: dict) -> dict:
    _bundle(run, bundle_ref)
    capabilities = copy.deepcopy(draft.get("capabilities") or [])
    state = {
        "state_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": bundle_ref,
        "prior_percent": run["control_plane"]["learner_prior_percent"],
        "capabilities": sorted(capabilities, key=lambda x: x["capability_ref"]),
        "state_digest": "",
    }
    identity = {k: v for k, v in state.items() if k not in {"state_id", "state_digest"}}
    state["state_id"] = "MATH-LCS-" + digest(identity)[:16]
    state["state_digest"] = digest(state, "state_digest")
    validate_learner_state(state, run, bundle_ref)
    return state


def _validate_cross_validation(validation: dict, run: dict, bundle_ref: str, first: dict, independent: dict) -> None:
    validate_schema(validation, "math-cross-validation.schema.json")
    if validation["validation_digest"] != digest(validation, "validation_digest"):
        fail("ASSIMILATION_CROSS_VALIDATION_DIGEST_MISMATCH")
    if validation["run_ref"] != run["run_id"] or validation["bundle_ref"] != bundle_ref:
        fail("ASSIMILATION_CROSS_VALIDATION_BINDING_MISMATCH")
    if validation["first_package_ref"] != first["package_id"] or validation["first_package_digest"] != first["package_digest"]:
        fail("ASSIMILATION_FIRST_PACKAGE_BINDING_MISMATCH")
    if validation["independent_package_ref"] != independent["package_id"] or validation["independent_package_digest"] != independent["package_digest"]:
        fail("ASSIMILATION_INDEPENDENT_PACKAGE_BINDING_MISMATCH")


def _resolved_intelligence(first: dict, independent: dict, validation: dict):
    first_claims = {x["claim_id"]: x for x in first["claims"]}
    second_claims = {x["claim_id"]: x for x in independent["claims"]}
    records = {x["first_claim_ref"]: x for x in validation["records"]}
    missing = {x["second_claim_ref"]: x for x in validation["missing_findings"]}

    requirements = []
    unknowns = []
    conflicts = []
    admissible_claims: dict[str, dict] = {}

    for claim_ref, claim in first_claims.items():
        if claim_ref not in records:
            fail("ASSIMILATION_FIRST_CLAIM_UNVALIDATED", claim_ref)
        rec = records[claim_ref]
        cls = rec["classification"]
        if cls in ADMISSIBLE_FIRST:
            statement = rec["refined_statement"] if cls == "REFINED" else claim["statement"]
            evidence_refs = sorted(set(claim["evidence_refs"] + rec["ground_truth_evidence_refs"]))
            row = {
                "claim_ref": claim_ref,
                "claim_type": claim["claim_type"],
                "statement": statement,
                "resolution": cls,
                "evidence_refs": evidence_refs,
                "role": first["role"],
            }
            requirements.append(row)
            admissible_claims[claim_ref] = row
        elif cls == "UNKNOWN":
            unknowns.append({
                "unknown_type": "CLAIM",
                "ref": claim_ref,
                "statement": claim["statement"],
            })
        elif cls in CONFLICT_CLASSES:
            conflicts.append({
                "record_ref": rec["record_id"],
                "classification": cls,
                "claim_ref": claim_ref,
                "rationale": rec["rationale"],
            })
        else:
            fail("ASSIMILATION_VALIDATION_CLASS_UNKNOWN", cls)

    for claim_ref, claim in second_claims.items():
        if claim_ref in missing:
            rec = missing[claim_ref]
            resolution = "MISSING"
            evidence_refs = sorted(set(claim["evidence_refs"] + rec["ground_truth_evidence_refs"]))
        else:
            resolution = "INDEPENDENT_GROUNDED"
            evidence_refs = sorted(set(claim["evidence_refs"]))
        row = {
            "claim_ref": claim_ref,
            "claim_type": claim["claim_type"],
            "statement": claim["statement"],
            "resolution": resolution,
            "evidence_refs": evidence_refs,
            "role": independent["role"],
        }
        requirements.append(row)
        admissible_claims[claim_ref] = row

    requirements.sort(key=lambda x: (x["role"], x["claim_type"], x["claim_ref"]))
    unknowns.sort(key=lambda x: x["ref"])
    conflicts.sort(key=lambda x: x["record_ref"])
    return requirements, unknowns, conflicts, admissible_claims


def _learner_gap(capability_ref: str, state_index: dict[str, dict]) -> dict:
    row = state_index.get(capability_ref)
    if row is None:
        return {
            "capability_ref": capability_ref,
            "readiness": "UNKNOWN",
            "gap_state": GAP_MAP["UNLISTED"],
            "basis": "UNKNOWN",
            "evidence_refs": [],
            "owner_control_ref": None,
        }
    return {
        "capability_ref": capability_ref,
        "readiness": row["readiness"],
        "gap_state": GAP_MAP[row["readiness"]],
        "basis": row["basis"],
        "evidence_refs": copy.deepcopy(row["evidence_refs"]),
        "owner_control_ref": row["owner_control_ref"],
    }


def build_assimilation_demand(
    run: dict,
    first_package: dict,
    independent_package: dict,
    validation: dict,
    spec: dict,
    *,
    learner_state: dict | None = None,
) -> dict:
    validate_learning_run(run)
    validate_schema(spec, "math-assimilation-demand-build-spec.schema.json")
    if run["current_state"] != "CROSS_VALIDATED":
        fail("ASSIMILATION_REQUIRES_CROSS_VALIDATED", run["current_state"])
    if spec["run_ref"] != run["run_id"]:
        fail("ASSIMILATION_SPEC_RUN_MISMATCH")
    bundle_ref = spec["bundle_ref"]
    bundle = _bundle(run, bundle_ref)
    if not bundle["cross_validation_ref"]:
        fail("ASSIMILATION_BUNDLE_NOT_CROSS_VALIDATED", bundle_ref)
    if bundle["cross_validation_ref"] != validation["validation_id"]:
        fail("ASSIMILATION_BUNDLE_VALIDATION_REF_MISMATCH")

    validate_specialist_package(first_package)
    validate_specialist_package(independent_package)
    _validate_cross_validation(validation, run, bundle_ref, first_package, independent_package)
    if {first_package["role"], independent_package["role"]} != {"CORE1", "CORE2"}:
        fail("ASSIMILATION_ROLE_PAIR_INCOMPLETE")
    by_role = {first_package["role"]: first_package, independent_package["role"]: independent_package}

    if learner_state is not None:
        validate_learner_state(learner_state, run, bundle_ref)
        if spec["learner_capability_state_ref"] != learner_state["state_id"]:
            fail("ASSIMILATION_LEARNER_STATE_REF_MISMATCH")
        state_index = {x["capability_ref"]: x for x in learner_state["capabilities"]}
    else:
        if spec["learner_capability_state_ref"] is not None:
            fail("ASSIMILATION_LEARNER_STATE_NOT_SUPPLIED")
        state_index = {}

    purpose = run["control_plane"]["learning_purpose"]
    if purpose is None:
        fail("ASSIMILATION_LEARNING_PURPOSE_REQUIRED")
    if purpose not in POLICY["purpose_requirements"]:
        fail("ASSIMILATION_LEARNING_PURPOSE_UNKNOWN", purpose)

    requirements, claim_unknowns, raw_conflicts, admissible = _resolved_intelligence(
        first_package, independent_package, validation
    )
    semantic = [{k: v for k, v in r.items() if k != "role"} for r in requirements if r["role"] == "CORE1"]
    assessment = [{k: v for k, v in r.items() if k != "role"} for r in requirements if r["role"] == "CORE2"]

    conflict_by_ref = {x["record_ref"]: x for x in raw_conflicts}
    blocking = set(spec["blocking_conflict_record_refs"])
    deferred_rows = {x["record_ref"]: x["reason"] for x in spec["deferred_conflicts"]}
    declared = blocking | set(deferred_rows)
    actual = set(conflict_by_ref)
    if declared != actual:
        missing = actual - declared
        extra = declared - actual
        if missing:
            fail("ASSIMILATION_CONFLICT_DISPOSITION_MISSING", sorted(missing)[0])
        fail("ASSIMILATION_CONFLICT_DISPOSITION_UNKNOWN", sorted(extra)[0])

    conflicts = []
    for ref, row in sorted(conflict_by_ref.items()):
        conflicts.append({
            **row,
            "blocking": ref in blocking,
            "defer_reason": None if ref in blocking else deferred_rows[ref],
        })

    owner_constraints = []
    owner_ids = set()
    for row in spec["owner_constraints"]:
        if row["constraint_id"] in owner_ids:
            fail("ASSIMILATION_OWNER_CONSTRAINT_DUPLICATE", row["constraint_id"])
        owner_ids.add(row["constraint_id"])
        owner_constraints.append({**copy.deepcopy(row), "authority_class": "OWNER_CONTROL"})
    owner_constraints.sort(key=lambda x: x["constraint_id"])

    obligation_keys = set()
    obligations = []
    all_capability_refs = set()
    for raw in spec["obligations"]:
        key = raw["local_key"]
        if key in obligation_keys:
            fail("ASSIMILATION_OBLIGATION_LOCAL_KEY_DUPLICATE", key)
        obligation_keys.add(key)
        origin_refs = sorted(set(raw["origin_claim_refs"]))
        unknown_origin = set(origin_refs) - set(admissible)
        if unknown_origin:
            fail("ASSIMILATION_OBLIGATION_ORIGIN_NOT_ADMISSIBLE", sorted(unknown_origin)[0])
        evidence_refs = sorted({e for ref in origin_refs for e in admissible[ref]["evidence_refs"]})
        if not evidence_refs:
            fail("ASSIMILATION_OBLIGATION_EVIDENCE_EMPTY", key)
        capability_refs = sorted(set(raw["capability_refs"]))
        all_capability_refs.update(capability_refs)
        gaps = [_learner_gap(ref, state_index) for ref in capability_refs]
        gap_states = sorted({x["gap_state"] for x in gaps})
        identity = {
            "obligation_type": raw["obligation_type"],
            "statement": raw["statement"],
            "origin_claim_refs": origin_refs,
            "capability_refs": capability_refs,
            "required_before_core2a": raw["required_before_core2a"],
        }
        obligations.append({
            "obligation_id": "MATH-OBL-" + digest(identity)[:16],
            "obligation_type": raw["obligation_type"],
            "statement": raw["statement"],
            "origin_claim_refs": origin_refs,
            "origin_evidence_refs": evidence_refs,
            "capability_refs": capability_refs,
            "learner_gap_states": gap_states,
            "required_before_core2a": raw["required_before_core2a"],
            "notes": raw["notes"],
        })
    obligations.sort(key=lambda x: (x["obligation_type"], x["obligation_id"]))

    learner_gaps = [_learner_gap(ref, state_index) for ref in sorted(all_capability_refs)]
    learner_unknowns = [
        {
            "unknown_type": "LEARNER_CAPABILITY",
            "ref": row["capability_ref"],
            "statement": "Learner readiness is unknown; absence of evidence is not weakness.",
        }
        for row in learner_gaps if row["readiness"] == "UNKNOWN"
    ]

    status = "BLOCKED_CONFLICT" if blocking else "JOIN_READY"
    demand = {
        "assimilation_demand_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": bundle_ref,
        "core1_package_ref": by_role["CORE1"]["package_id"],
        "core1_package_digest": by_role["CORE1"]["package_digest"],
        "core2_package_ref": by_role["CORE2"]["package_id"],
        "core2_package_digest": by_role["CORE2"]["package_digest"],
        "cross_validation_ref": validation["validation_id"],
        "cross_validation_digest": validation["validation_digest"],
        "learner_capability_state_ref": learner_state["state_id"] if learner_state else None,
        "learner_capability_state_digest": learner_state["state_digest"] if learner_state else None,
        "learning_purpose": purpose,
        "semantic_requirements": semantic,
        "assessment_requirements": assessment,
        "learner_gaps": learner_gaps,
        "purpose_requirements": copy.deepcopy(POLICY["purpose_requirements"][purpose]),
        "owner_constraints": owner_constraints,
        "unknowns": sorted(claim_unknowns + learner_unknowns, key=lambda x: (x["unknown_type"], x["ref"])),
        "conflicts": conflicts,
        "assimilation_obligations": obligations,
        "unresolved_issue_refs": sorted(set(spec["unresolved_issue_refs"])),
        "status": status,
        "demand_digest": "",
    }
    identity = {k: v for k, v in demand.items() if k not in {"assimilation_demand_id", "demand_digest"}}
    demand["assimilation_demand_id"] = "MATH-AD-" + digest(identity)[:16]
    demand["demand_digest"] = digest(demand, "demand_digest")
    validate_schema(demand, "math-assimilation-demand.schema.json")
    return demand


def apply_assimilation_demand(run: dict, demand: dict) -> dict:
    validate_learning_run(run)
    validate_schema(demand, "math-assimilation-demand.schema.json")
    if demand["demand_digest"] != digest(demand, "demand_digest"):
        fail("ASSIMILATION_DEMAND_DIGEST_MISMATCH")
    if demand["run_ref"] != run["run_id"]:
        fail("ASSIMILATION_DEMAND_RUN_MISMATCH")
    if run["current_state"] != "CROSS_VALIDATED":
        fail("ASSIMILATION_APPLY_REQUIRES_CROSS_VALIDATED", run["current_state"])

    out = copy.deepcopy(run)
    target = _bundle(out, demand["bundle_ref"])
    target["join_ref"] = demand["assimilation_demand_id"]
    if demand["status"] == "BLOCKED_CONFLICT":
        out["current_state"] = "BLOCKED_CONFLICT"
        out["state_history"].append({
            "sequence": len(out["state_history"]),
            "state": "BLOCKED_CONFLICT",
            "reason_code": "ASSIMILATION_JOIN_BLOCKING_CONFLICT",
        })
    elif all(b["join_ref"] for b in out["bundles"]):
        out["current_state"] = "JOIN_READY"
        out["state_history"].append({
            "sequence": len(out["state_history"]),
            "state": "JOIN_READY",
            "reason_code": "ASSIMILATION_DEMANDS_READY",
        })
    return seal_learning_run(out)


def _write(path: str, value: dict) -> None:
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Mathematics Join / AssimilationDemand from cross-validated Core1/Core2 intelligence.")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("seal-learner-state")
    p.add_argument("--run", required=True)
    p.add_argument("--bundle-ref", required=True)
    p.add_argument("--draft", required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("build")
    p.add_argument("--run", required=True)
    p.add_argument("--first-package", required=True)
    p.add_argument("--independent-package", required=True)
    p.add_argument("--cross-validation", required=True)
    p.add_argument("--spec", required=True)
    p.add_argument("--learner-state")
    p.add_argument("--out-demand", required=True)
    p.add_argument("--out-run", required=True)

    args = ap.parse_args()
    run = load(args.run)
    if args.command == "seal-learner-state":
        state = seal_learner_state(run, args.bundle_ref, load(args.draft))
        _write(args.out, state)
        print(json.dumps({"status": "PASS", "learner_state_id": state["state_id"]}, indent=2))
        return

    demand = build_assimilation_demand(
        run,
        load(args.first_package),
        load(args.independent_package),
        load(args.cross_validation),
        load(args.spec),
        learner_state=load(args.learner_state) if args.learner_state else None,
    )
    updated = apply_assimilation_demand(run, demand)
    _write(args.out_demand, demand)
    _write(args.out_run, updated)
    print(json.dumps({
        "status": demand["status"],
        "assimilation_demand_id": demand["assimilation_demand_id"],
        "run_state": updated["current_state"],
        "obligations": len(demand["assimilation_obligations"]),
        "unknowns": len(demand["unknowns"]),
        "conflicts": len(demand["conflicts"]),
    }, indent=2))


if __name__ == "__main__":
    main()
