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
    digest,
    fail,
    load,
    seal_learning_run,
    validate_ground_truth_manifest,
    validate_learning_run,
    validate_schema,
)

DIMENSIONS = (
    "scope_authority",
    "semantic_source_strength",
    "question_evidence",
    "question_resolution",
    "uncertainty",
    "conflict_index",
)
BLOCK_ACTIONS = {"BLOCK_EVIDENCE", "BLOCK_CONFLICT", "BLOCK_OWNER_REVIEW"}
ROLE_ACTION = {"CORE1": "CORE1_FIRST", "CORE2": "CORE2_FIRST"}
ACTION_ROLE = {v: k for k, v in ROLE_ACTION.items()}


def _evidence_index(manifest: dict) -> dict[str, dict]:
    return {x["evidence_id"]: x for x in manifest["evidence_items"]}


def validate_routing_spec(spec: dict, manifest: dict) -> None:
    validate_schema(spec, "math-routing-build-spec.schema.json")
    if spec["ground_truth_ref"] != manifest["manifest_id"] or spec["ground_truth_digest"] != manifest["manifest_digest"]:
        fail("ROUTING_GROUND_TRUTH_BINDING_MISMATCH")
    idx = _evidence_index(manifest)
    seen_refs = set()
    seen_seq = set()
    for row in spec["candidate_subtopics"]:
        ref = row["subtopic_ref"]
        if ref in seen_refs:
            fail("ROUTING_SUBTOPIC_DUPLICATE", ref)
        seen_refs.add(ref)
        if row["sequence"] in seen_seq:
            fail("ROUTING_SEQUENCE_DUPLICATE", str(row["sequence"]))
        seen_seq.add(row["sequence"])
        for dim in DIMENSIONS:
            d = row[dim]
            if d["score"] > 0 and not d["evidence_refs"] and dim not in {"uncertainty", "conflict_index"}:
                fail("ROUTING_DIMENSION_EVIDENCE_MISSING", f"{ref}:{dim}")
            for eid in d["evidence_refs"]:
                if eid not in idx:
                    fail("ROUTING_EVIDENCE_REF_UNKNOWN", f"{ref}:{eid}")
                if idx[eid]["availability"] == "ABSENT":
                    fail("ROUTING_ABSENT_EVIDENCE_REFERENCED_AS_SUPPORT", f"{ref}:{eid}")
        if row["question_resolution"]["score"] > 0 and row["question_evidence"]["score"] == 0:
            fail("ROUTING_QUESTION_RESOLUTION_WITHOUT_QUESTION_EVIDENCE", ref)
        if row["conflict_index"]["score"] > 0 and not row["conflict_refs"]:
            fail("ROUTING_CONFLICT_SCORE_WITHOUT_CONFLICT_REF", ref)


def validate_override_ledger(ledger: dict | None, run: dict) -> dict[str, dict]:
    if ledger is None:
        return {}
    validate_schema(ledger, "math-owner-override-ledger.schema.json")
    if ledger["ledger_digest"] != digest(ledger, "ledger_digest"):
        fail("OWNER_OVERRIDE_LEDGER_DIGEST_MISMATCH")
    if ledger["run_ref"] != run["run_id"]:
        fail("OWNER_OVERRIDE_RUN_REF_MISMATCH")
    by_target: dict[str, dict] = {}
    ids = set()
    for row in ledger["overrides"]:
        if row["override_id"] in ids:
            fail("OWNER_OVERRIDE_ID_DUPLICATE", row["override_id"])
        ids.add(row["override_id"])
        if row["target_ref"] in by_target:
            fail("OWNER_OVERRIDE_TARGET_DUPLICATE", row["target_ref"])
        by_target[row["target_ref"]] = row
    return by_target


def profile_decision(row: dict, *, referenced_conflicted: bool = False, override: dict | None = None) -> dict:
    semantic_strength = max(row["scope_authority"]["score"], row["semantic_source_strength"]["score"])
    assessment_strength = min(row["question_evidence"]["score"], row["question_resolution"]["score"])
    conflict = row["conflict_index"]["score"]

    eligible_roles = []
    if semantic_strength >= 3 and conflict <= 2 and not referenced_conflicted:
        eligible_roles.append("CORE1")
    if row["question_evidence"]["score"] >= 3 and row["question_resolution"]["score"] >= 3 and conflict <= 2 and not referenced_conflicted:
        eligible_roles.append("CORE2")

    reason_codes = []
    if referenced_conflicted or conflict >= 3:
        system_action = "BLOCK_CONFLICT"
        reason_codes.append("MATERIAL_EVIDENCE_CONFLICT")
    elif semantic_strength <= 1 and assessment_strength <= 1:
        system_action = "BLOCK_EVIDENCE"
        reason_codes.append("INSUFFICIENT_SEMANTIC_AND_ASSESSMENT_EVIDENCE")
    elif "CORE1" in eligible_roles:
        system_action = "CORE1_FIRST"
        reason_codes.append("STRONG_SEMANTIC_AUTHORITY")
        if "CORE2" in eligible_roles:
            reason_codes.append("ASSESSMENT_EVIDENCE_ALSO_STRONG")
    elif "CORE2" in eligible_roles:
        system_action = "CORE2_FIRST"
        reason_codes.append("QUESTION_CORPUS_DEFINES_SCOPE")
    else:
        system_action = "BLOCK_OWNER_REVIEW"
        reason_codes.append("PARTIAL_OR_AMBIGUOUS_EVIDENCE")

    final_action = system_action
    applied_override_ref = None
    override_mode = None
    if override is not None:
        requested = override["requested_action"]
        mode = override["mode"]
        if mode == "HARD":
            final_action = requested
            applied_override_ref = override["override_id"]
            override_mode = mode
            reason_codes.append("HARD_OWNER_OVERRIDE_APPLIED")
        elif mode == "SOFT":
            role = ACTION_ROLE.get(requested)
            if role is not None and role in eligible_roles:
                final_action = requested
                applied_override_ref = override["override_id"]
                override_mode = mode
                reason_codes.append("SOFT_OWNER_OVERRIDE_APPLIED")
            else:
                reason_codes.append("SOFT_OWNER_OVERRIDE_NOT_ADMISSIBLE")

    first_role = ACTION_ROLE.get(final_action)
    return {
        "subtopic_ref": row["subtopic_ref"],
        "display_name": row["display_name"],
        "sequence": row["sequence"],
        "coherence_group": row["coherence_group"],
        "semantic_strength": semantic_strength,
        "assessment_strength": assessment_strength,
        "eligible_roles": eligible_roles,
        "system_action": system_action,
        "final_action": final_action,
        "first_role": first_role,
        "reason_codes": list(dict.fromkeys(reason_codes)),
        "evidence_profile_digest": digest(row),
        "applied_override_ref": applied_override_ref,
        "override_mode": override_mode,
        "unresolved_issue_refs": copy.deepcopy(row["unresolved_issue_refs"]),
        "conflict_refs": copy.deepcopy(row["conflict_refs"]),
    }


def _referenced_conflicted(row: dict, idx: dict[str, dict]) -> bool:
    refs = {eid for dim in DIMENSIONS for eid in row[dim]["evidence_refs"]}
    return any(idx[eid]["availability"] == "CONFLICTED" for eid in refs)


def _build_bundles(decisions: list[dict]) -> list[dict]:
    routed = [d for d in decisions if d["first_role"] is not None]
    routed.sort(key=lambda d: (d["sequence"], d["subtopic_ref"]))
    groups: dict[tuple[str, str], list[dict]] = {}
    group_order = []
    for d in routed:
        key = (d["first_role"], d["coherence_group"])
        if key not in groups:
            groups[key] = []
            group_order.append(key)
        groups[key].append(d)

    bundles = []
    for role, coherence in group_order:
        rows = groups[(role, coherence)]
        for i in range(0, len(rows), 3):
            chunk = rows[i:i+3]
            payload = {
                "subtopic_refs": [x["subtopic_ref"] for x in chunk],
                "first_role": role,
                "coherence_group": coherence,
            }
            bundle_id = "MATH-HB-" + digest(payload)[:16]
            bundles.append({
                "bundle_id": bundle_id,
                "subtopic_refs": payload["subtopic_refs"],
                "first_role": role,
                "coherence_group": coherence,
            })
    return bundles


def _plan_status(decisions: list[dict]) -> str:
    blocked = {d["final_action"] for d in decisions if d["final_action"] in BLOCK_ACTIONS}
    if "BLOCK_CONFLICT" in blocked:
        return "BLOCKED_CONFLICT"
    if "BLOCK_EVIDENCE" in blocked:
        return "BLOCKED_EVIDENCE"
    if "BLOCK_OWNER_REVIEW" in blocked:
        return "BLOCKED_OWNER_REVIEW"
    return "ROUTED"


def build_routing_plan(manifest: dict, run: dict, spec: dict, *, override_ledger: dict | None = None) -> dict:
    validate_ground_truth_manifest(manifest)
    validate_learning_run(run)
    if run["current_state"] != "GT_READY":
        fail("ROUTING_REQUIRES_GT_READY", run["current_state"])
    if run["ground_truth_ref"] != manifest["manifest_id"] or run["ground_truth_digest"] != manifest["manifest_digest"]:
        fail("RUN_GROUND_TRUTH_BINDING_MISMATCH")
    validate_routing_spec(spec, manifest)
    overrides = validate_override_ledger(override_ledger, run)
    idx = _evidence_index(manifest)

    decisions = []
    for row in sorted(spec["candidate_subtopics"], key=lambda x: (x["sequence"], x["subtopic_ref"])):
        decisions.append(profile_decision(
            row,
            referenced_conflicted=_referenced_conflicted(row, idx),
            override=overrides.get(row["subtopic_ref"]),
        ))

    bundles = _build_bundles(decisions)
    status = _plan_status(decisions)
    plan = {
        "plan_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "ground_truth_ref": manifest["manifest_id"],
        "ground_truth_digest": manifest["manifest_digest"],
        "policy_ref": "MATH-EVIDENCE-ROUTING-v1",
        "override_ledger_ref": override_ledger["ledger_id"] if override_ledger else None,
        "decisions": decisions,
        "bundles": bundles,
        "blocked_subtopic_refs": sorted(d["subtopic_ref"] for d in decisions if d["final_action"] in BLOCK_ACTIONS),
        "status": status,
        "plan_digest": "",
    }
    plan["plan_id"] = "MATH-RP-" + digest({k: v for k, v in plan.items() if k not in {"plan_id", "plan_digest"}})[:16]
    plan["plan_digest"] = digest(plan, "plan_digest")
    validate_schema(plan, "math-routing-plan.schema.json")
    return plan


def apply_routing_plan(run: dict, plan: dict) -> dict:
    validate_learning_run(run)
    validate_schema(plan, "math-routing-plan.schema.json")
    if plan["run_ref"] != run["run_id"]:
        fail("ROUTING_PLAN_RUN_REF_MISMATCH")
    if plan["plan_digest"] != digest(plan, "plan_digest"):
        fail("ROUTING_PLAN_DIGEST_MISMATCH")

    out = copy.deepcopy(run)
    out["routing_ref"] = plan["plan_id"]
    out["bundles"] = [
        {
            "bundle_id": b["bundle_id"],
            "subtopic_refs": b["subtopic_refs"],
            "first_role": b["first_role"],
            "core1_execution_ref": None,
            "core2_execution_ref": None,
            "cross_validation_ref": None,
            "join_ref": None,
            "assimilation_plan_ref": None,
            "core1a_ref": None,
            "exposure_receipt_refs": [],
            "core2a_eligibility_ref": None,
            "core2a_ref": None,
        }
        for b in plan["bundles"]
    ]
    next_state = plan["status"]
    out["current_state"] = next_state
    out["state_history"].append({
        "sequence": len(out["state_history"]),
        "state": next_state,
        "reason_code": "ADAPTIVE_EVIDENCE_ROUTING_COMPLETE" if next_state == "ROUTED" else "ADAPTIVE_EVIDENCE_ROUTING_BLOCKED",
    })
    if plan["override_ledger_ref"]:
        refs = set(out["control_plane"]["owner_override_refs"])
        refs.add(plan["override_ledger_ref"])
        out["control_plane"]["owner_override_refs"] = sorted(refs)
    return seal_learning_run(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ground-truth", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--routing-spec", required=True)
    ap.add_argument("--override-ledger")
    ap.add_argument("--out-plan", required=True)
    ap.add_argument("--out-run", required=True)
    args = ap.parse_args()

    manifest = load(args.ground_truth)
    run = load(args.run)
    spec = load(args.routing_spec)
    ledger = load(args.override_ledger) if args.override_ledger else None
    plan = build_routing_plan(manifest, run, spec, override_ledger=ledger)
    updated = apply_routing_plan(run, plan)
    Path(args.out_plan).write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(args.out_run).write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": plan["status"],
        "routing_plan_id": plan["plan_id"],
        "run_id": updated["run_id"],
        "bundle_count": len(plan["bundles"]),
        "blocked_subtopics": plan["blocked_subtopic_refs"],
    }, indent=2))


if __name__ == "__main__":
    main()
