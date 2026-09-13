#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import ROOT, digest, fail, load, seal_learning_run, validate_learning_run, validate_schema

POLICY = load(ROOT / "policies" / "math-assimilation-compiler-policy.json")
FADE_GAPS = set(POLICY["fading_required_gap_states"])
FADE_ORDER = POLICY["fading_stage_order"]
COMPONENT_REQUIREMENTS = POLICY["obligation_component_requirements"]


def _bundle(run: dict, bundle_ref: str) -> dict:
    for bundle in run["bundles"]:
        if bundle["bundle_id"] == bundle_ref:
            return bundle
    fail("ASSIMILATION_COMPILER_BUNDLE_UNKNOWN", bundle_ref)


def _id(prefix: str, payload: dict) -> str:
    return prefix + digest(payload)[:16]


def _validate_demand(demand: dict, run: dict, bundle_ref: str) -> None:
    validate_schema(demand, "math-assimilation-demand.schema.json")
    if demand["demand_digest"] != digest(demand, "demand_digest"):
        fail("ASSIMILATION_COMPILER_DEMAND_DIGEST_MISMATCH")
    if demand["run_ref"] != run["run_id"] or demand["bundle_ref"] != bundle_ref:
        fail("ASSIMILATION_COMPILER_DEMAND_BINDING_MISMATCH")
    if demand["status"] != "JOIN_READY":
        fail("ASSIMILATION_COMPILER_DEMAND_NOT_READY", demand["status"])
    if demand["learning_purpose"] != run["control_plane"]["learning_purpose"]:
        fail("ASSIMILATION_COMPILER_PURPOSE_MISMATCH")
    bundle = _bundle(run, bundle_ref)
    if bundle["join_ref"] != demand["assimilation_demand_id"]:
        fail("ASSIMILATION_COMPILER_JOIN_REF_MISMATCH")


def _unique_local(rows: list[dict], code: str) -> dict[str, dict]:
    out = {}
    for row in rows:
        key = row["local_key"]
        if key in out:
            fail(code, key)
        out[key] = row
    return out


def _ensure_obligation_refs(rows: list[dict], valid: set[str], code: str) -> None:
    for row in rows:
        for ref in row["obligation_refs"]:
            if ref not in valid:
                fail(code, ref)


def _assert_acyclic(edges: dict[str, set[str]], code: str) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            fail(code, node)
        visiting.add(node)
        for parent in edges.get(node, set()):
            visit(parent)
        visiting.remove(node)
        visited.add(node)

    for node in edges:
        visit(node)


def validate_assimilation_plan(plan: dict) -> None:
    validate_schema(plan, "math-assimilation-plan.schema.json")
    if plan["plan_digest"] != digest(plan, "plan_digest"):
        fail("ASSIMILATION_PLAN_DIGEST_MISMATCH")

    obligation_refs = [x["obligation_ref"] for x in plan["obligation_coverage"]]
    if len(obligation_refs) != len(set(obligation_refs)):
        fail("ASSIMILATION_PLAN_COVERAGE_DUPLICATE")

    atom_refs = {x["atom_id"] for x in plan["learning_atoms"]}
    for atom in plan["learning_atoms"]:
        missing = set(atom["prerequisite_atom_refs"]) - atom_refs
        if missing:
            fail("ASSIMILATION_PLAN_PREREQUISITE_REF_UNKNOWN", sorted(missing)[0])

    rr = {x["representation_requirement_id"] for x in plan["representation_requirements"]}
    rc = {x["representation_candidate_id"]: x for x in plan["representation_candidates"]}
    for cand in rc.values():
        if cand["requirement_ref"] not in rr:
            fail("ASSIMILATION_PLAN_REPRESENTATION_REQUIREMENT_UNKNOWN", cand["requirement_ref"])
    for dec in plan["representation_decisions"]:
        if dec["requirement_ref"] not in rr:
            fail("ASSIMILATION_PLAN_REPRESENTATION_DECISION_REQUIREMENT_UNKNOWN", dec["requirement_ref"])
        selected = rc.get(dec["selected_candidate_ref"])
        if selected is None or selected["requirement_ref"] != dec["requirement_ref"]:
            fail("ASSIMILATION_PLAN_REPRESENTATION_SELECTION_INVALID", dec["selected_candidate_ref"])
        if not selected["admissible"]:
            fail("ASSIMILATION_PLAN_REPRESENTATION_SELECTED_INADMISSIBLE", dec["selected_candidate_ref"])


def compile_assimilation_plan(run: dict, demand: dict, spec: dict) -> dict:
    validate_learning_run(run)
    validate_schema(spec, "math-assimilation-plan-build-spec.schema.json")
    if run["current_state"] != "JOIN_READY":
        fail("ASSIMILATION_COMPILER_REQUIRES_JOIN_READY", run["current_state"])
    if spec["run_ref"] != run["run_id"]:
        fail("ASSIMILATION_COMPILER_SPEC_RUN_MISMATCH")
    bundle_ref = spec["bundle_ref"]
    _bundle(run, bundle_ref)
    if spec["assimilation_demand_ref"] != demand["assimilation_demand_id"]:
        fail("ASSIMILATION_COMPILER_SPEC_DEMAND_MISMATCH")
    _validate_demand(demand, run, bundle_ref)

    obligation_rows = {x["obligation_id"]: x for x in demand["assimilation_obligations"]}
    obligation_ids = set(obligation_rows)
    if not obligation_ids:
        fail("ASSIMILATION_COMPILER_NO_OBLIGATIONS")

    for key in (
        "cognitive_transformations", "learning_atoms", "inference_chains",
        "equation_assimilations", "representation_requirements",
        "misconception_contrasts", "symbol_bridges", "fading_plans",
        "transfer_bridges",
    ):
        _ensure_obligation_refs(spec[key], obligation_ids, "ASSIMILATION_COMPILER_OBLIGATION_REF_UNKNOWN")

    transforms_raw = _unique_local(
        spec["cognitive_transformations"], "ASSIMILATION_COMPILER_TRANSFORMATION_KEY_DUPLICATE"
    )
    atoms_raw = _unique_local(spec["learning_atoms"], "ASSIMILATION_COMPILER_ATOM_KEY_DUPLICATE")
    infer_raw = _unique_local(spec["inference_chains"], "ASSIMILATION_COMPILER_INFERENCE_KEY_DUPLICATE")
    eq_raw = _unique_local(spec["equation_assimilations"], "ASSIMILATION_COMPILER_EQUATION_KEY_DUPLICATE")
    rr_raw = _unique_local(
        spec["representation_requirements"], "ASSIMILATION_COMPILER_REPRESENTATION_REQUIREMENT_KEY_DUPLICATE"
    )
    rc_raw = _unique_local(
        spec["representation_candidates"], "ASSIMILATION_COMPILER_REPRESENTATION_CANDIDATE_KEY_DUPLICATE"
    )
    mc_raw = _unique_local(
        spec["misconception_contrasts"], "ASSIMILATION_COMPILER_MISCONCEPTION_KEY_DUPLICATE"
    )
    sb_raw = _unique_local(spec["symbol_bridges"], "ASSIMILATION_COMPILER_SYMBOL_BRIDGE_KEY_DUPLICATE")
    fp_raw = _unique_local(spec["fading_plans"], "ASSIMILATION_COMPILER_FADING_KEY_DUPLICATE")
    tb_raw = _unique_local(spec["transfer_bridges"], "ASSIMILATION_COMPILER_TRANSFER_KEY_DUPLICATE")

    atom_keys = set(atoms_raw)
    prereq_edges: dict[str, set[str]] = {}
    for key, atom in atoms_raw.items():
        refs = set(atom["prerequisite_atom_keys"])
        missing = refs - atom_keys
        if missing:
            fail("ASSIMILATION_COMPILER_PREREQUISITE_ATOM_UNKNOWN", sorted(missing)[0])
        if key in refs:
            fail("ASSIMILATION_COMPILER_PREREQUISITE_SELF_CYCLE", key)
        prereq_edges[key] = refs
    _assert_acyclic(prereq_edges, "ASSIMILATION_COMPILER_PREREQUISITE_CYCLE")

    component_refs: dict[str, list[str]] = defaultdict(list)
    component_types: dict[str, set[str]] = defaultdict(set)

    transformations = []
    transform_ids = {}
    for key, raw in transforms_raw.items():
        payload = {k: copy.deepcopy(v) for k, v in raw.items() if k != "local_key"}
        cid = _id("MATH-CT-", payload)
        transform_ids[key] = cid
        row = {"transformation_id": cid, **payload}
        transformations.append(row)
        for obl in raw["obligation_refs"]:
            component_refs[obl].append(cid)
            component_types[obl].add("COGNITIVE_TRANSFORMATION")

    atom_ids = {}
    for key, raw in atoms_raw.items():
        identity = {
            "atom_type": raw["atom_type"], "statement": raw["statement"],
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "capability_refs": sorted(set(raw["capability_refs"])),
        }
        atom_ids[key] = _id("MATH-LA-", identity)
    atoms = []
    for key, raw in atoms_raw.items():
        row = {
            "atom_id": atom_ids[key],
            "atom_type": raw["atom_type"],
            "statement": raw["statement"],
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "capability_refs": sorted(set(raw["capability_refs"])),
            "prerequisite_atom_refs": sorted(atom_ids[x] for x in raw["prerequisite_atom_keys"]),
        }
        atoms.append(row)
        for obl in raw["obligation_refs"]:
            component_refs[obl].append(atom_ids[key])
            component_types[obl].add("LEARNING_ATOM")

    symbol_bridges = []
    symbol_ids = {}
    for key, raw in sb_raw.items():
        missing_atoms = set(raw["atom_keys"]) - atom_keys
        if missing_atoms:
            fail("ASSIMILATION_COMPILER_SYMBOL_BRIDGE_ATOM_UNKNOWN", sorted(missing_atoms)[0])
        payload = {
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "atom_refs": sorted(atom_ids[x] for x in raw["atom_keys"]),
            "symbol": raw["symbol"], "meaning": raw["meaning"],
            "bridge_statement": raw["bridge_statement"],
        }
        cid = _id("MATH-SB-", payload)
        symbol_ids[key] = cid
        symbol_bridges.append({"symbol_bridge_id": cid, **payload})
        for obl in raw["obligation_refs"]:
            component_refs[obl].append(cid)
            component_types[obl].add("SYMBOL_BRIDGE")

    inference_chains = []
    for key, raw in infer_raw.items():
        declared = set(raw["atom_keys"])
        missing_atoms = declared - atom_keys
        if missing_atoms:
            fail("ASSIMILATION_COMPILER_INFERENCE_ATOM_UNKNOWN", sorted(missing_atoms)[0])
        edge_map: dict[str, set[str]] = {x: set() for x in declared}
        steps = []
        for step in raw["steps"]:
            a, b = step["from_atom_key"], step["to_atom_key"]
            if a not in declared or b not in declared:
                fail("ASSIMILATION_COMPILER_INFERENCE_STEP_OUTSIDE_CHAIN", f"{a}->{b}")
            if a == b:
                fail("ASSIMILATION_COMPILER_INFERENCE_SELF_CYCLE", a)
            edge_map[b].add(a)
            steps.append({
                "from_atom_ref": atom_ids[a],
                "to_atom_ref": atom_ids[b],
                "inference": step["inference"],
            })
        _assert_acyclic(edge_map, "ASSIMILATION_COMPILER_INFERENCE_CYCLE")
        payload = {
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "atom_refs": sorted(atom_ids[x] for x in raw["atom_keys"]),
            "steps": steps,
        }
        cid = _id("MATH-IC-", payload)
        inference_chains.append({"inference_chain_id": cid, **payload})
        for obl in raw["obligation_refs"]:
            component_refs[obl].append(cid)
            component_types[obl].add("INFERENCE_CHAIN")

    equation_assimilations = []
    for key, raw in eq_raw.items():
        missing_atoms = set(raw["atom_keys"]) - atom_keys
        if missing_atoms:
            fail("ASSIMILATION_COMPILER_EQUATION_ATOM_UNKNOWN", sorted(missing_atoms)[0])
        missing_symbols = set(raw["symbol_bridge_keys"]) - set(symbol_ids)
        if missing_symbols:
            fail("ASSIMILATION_COMPILER_EQUATION_SYMBOL_BRIDGE_UNKNOWN", sorted(missing_symbols)[0])
        for sk in raw["symbol_bridge_keys"]:
            if not (set(sb_raw[sk]["obligation_refs"]) & set(raw["obligation_refs"])):
                fail("ASSIMILATION_COMPILER_EQUATION_SYMBOL_BRIDGE_UNGROUNDED", sk)
        payload = {
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "atom_refs": sorted(atom_ids[x] for x in raw["atom_keys"]),
            "equation_text": raw["equation_text"],
            "meaning": raw["meaning"],
            "symbol_bridge_refs": sorted(symbol_ids[x] for x in raw["symbol_bridge_keys"]),
            "validity_conditions": copy.deepcopy(raw["validity_conditions"]),
        }
        cid = _id("MATH-EA-", payload)
        equation_assimilations.append({"equation_assimilation_id": cid, **payload})
        for obl in raw["obligation_refs"]:
            component_refs[obl].append(cid)
            component_types[obl].add("EQUATION_ASSIMILATION")

    representation_requirements = []
    rr_ids = {}
    for key, raw in rr_raw.items():
        missing_atoms = set(raw["atom_keys"]) - atom_keys
        if missing_atoms:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_ATOM_UNKNOWN", sorted(missing_atoms)[0])
        payload = {
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "atom_refs": sorted(atom_ids[x] for x in raw["atom_keys"]),
            "purpose": raw["purpose"], "must_externalize": raw["must_externalize"],
        }
        rr_ids[key] = _id("MATH-RR-", payload)
        representation_requirements.append({"representation_requirement_id": rr_ids[key], **payload})

    candidates_by_req: dict[str, list[str]] = defaultdict(list)
    representation_candidates = []
    rc_ids = {}
    for key, raw in rc_raw.items():
        req_key = raw["requirement_key"]
        if req_key not in rr_raw:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_REQUIREMENT_UNKNOWN", req_key)
        payload = {
            "requirement_ref": rr_ids[req_key],
            "representation_type": raw["representation_type"],
            "description": raw["description"],
            "affordances": copy.deepcopy(raw["affordances"]),
            "limitations": copy.deepcopy(raw["limitations"]),
            "admissible": raw["admissible"],
        }
        rc_ids[key] = _id("MATH-RC-", payload)
        candidates_by_req[req_key].append(key)
        representation_candidates.append({"representation_candidate_id": rc_ids[key], **payload})

    decisions_by_req = {}
    for raw in spec["representation_decisions"]:
        req_key = raw["requirement_key"]
        if req_key in decisions_by_req:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_DECISION_DUPLICATE", req_key)
        decisions_by_req[req_key] = raw

    representation_decisions = []
    for req_key, req in rr_raw.items():
        candidate_keys = candidates_by_req.get(req_key, [])
        if len(candidate_keys) < POLICY["representation_min_candidates"]:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_CANDIDATES_INSUFFICIENT", req_key)
        decision = decisions_by_req.get(req_key)
        if decision is None:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_DECISION_MISSING", req_key)
        selected = decision["selected_candidate_key"]
        if selected not in candidate_keys:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_SELECTED_OUTSIDE_REQUIREMENT", selected)
        if not rc_raw[selected]["admissible"]:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_SELECTED_INADMISSIBLE", selected)
        expected_rejected = set(candidate_keys) - {selected}
        if set(decision["rejected_candidate_keys"]) != expected_rejected:
            fail("ASSIMILATION_COMPILER_REPRESENTATION_REJECTIONS_INCOMPLETE", req_key)
        payload = {
            "requirement_ref": rr_ids[req_key],
            "selected_candidate_ref": rc_ids[selected],
            "rationale": decision["rationale"],
            "rejected_candidate_refs": sorted(rc_ids[x] for x in decision["rejected_candidate_keys"]),
        }
        cid = _id("MATH-RD-", payload)
        representation_decisions.append({"representation_decision_id": cid, **payload})
        for obl in req["obligation_refs"]:
            component_refs[obl].extend([rr_ids[req_key], cid])
            component_types[obl].add("REPRESENTATION_DECISION")

    extra_decisions = set(decisions_by_req) - set(rr_raw)
    if extra_decisions:
        fail("ASSIMILATION_COMPILER_REPRESENTATION_DECISION_REQUIREMENT_UNKNOWN", sorted(extra_decisions)[0])

    misconception_contrasts = []
    for key, raw in mc_raw.items():
        missing_atoms = set(raw["atom_keys"]) - atom_keys
        if missing_atoms:
            fail("ASSIMILATION_COMPILER_MISCONCEPTION_ATOM_UNKNOWN", sorted(missing_atoms)[0])
        payload = {
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "atom_refs": sorted(atom_ids[x] for x in raw["atom_keys"]),
            "misconception": raw["misconception"], "contrast": raw["contrast"],
            "diagnostic_cue": raw["diagnostic_cue"],
        }
        cid = _id("MATH-MC-", payload)
        misconception_contrasts.append({"misconception_contrast_id": cid, **payload})
        for obl in raw["obligation_refs"]:
            component_refs[obl].append(cid)
            component_types[obl].add("MISCONCEPTION_CONTRAST")

    fading_plans = []
    fade_by_obligation: set[str] = set()
    for key, raw in fp_raw.items():
        missing_atoms = set(raw["atom_keys"]) - atom_keys
        if missing_atoms:
            fail("ASSIMILATION_COMPILER_FADING_ATOM_UNKNOWN", sorted(missing_atoms)[0])
        if raw["stages"] != FADE_ORDER:
            fail("ASSIMILATION_COMPILER_FADING_ORDER_INVALID", key)
        payload = {
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "atom_refs": sorted(atom_ids[x] for x in raw["atom_keys"]),
            "stages": copy.deepcopy(raw["stages"]),
            "support_notes": copy.deepcopy(raw["support_notes"]),
        }
        cid = _id("MATH-FP-", payload)
        fading_plans.append({"fading_plan_id": cid, **payload})
        for obl in raw["obligation_refs"]:
            fade_by_obligation.add(obl)
            component_refs[obl].append(cid)
            component_types[obl].add("FADING_PLAN")

    gap_by_cap = {x["capability_ref"]: x["gap_state"] for x in demand["learner_gaps"]}
    for obl_id, obl in obligation_rows.items():
        needs_fade = any(gap_by_cap.get(cap) in FADE_GAPS for cap in obl["capability_refs"])
        if needs_fade and obl_id not in fade_by_obligation:
            fail("ASSIMILATION_COMPILER_FADING_REQUIRED", obl_id)

    transfer_bridges = []
    for key, raw in tb_raw.items():
        missing_atoms = set(raw["atom_keys"]) - atom_keys
        if missing_atoms:
            fail("ASSIMILATION_COMPILER_TRANSFER_ATOM_UNKNOWN", sorted(missing_atoms)[0])
        allowed_types = {obligation_rows[x]["obligation_type"] for x in raw["obligation_refs"]}
        if not (allowed_types & {"TRANSFER", "ASSESSMENT_RECOGNITION"}):
            fail("ASSIMILATION_COMPILER_TRANSFER_WITHOUT_DEMAND_AUTHORITY", key)
        payload = {
            "obligation_refs": sorted(set(raw["obligation_refs"])),
            "atom_refs": sorted(atom_ids[x] for x in raw["atom_keys"]),
            "source_structure": raw["source_structure"],
            "changed_surface": raw["changed_surface"],
            "invariant_to_preserve": raw["invariant_to_preserve"],
            "target_demand": raw["target_demand"],
        }
        cid = _id("MATH-TB-", payload)
        transfer_bridges.append({"transfer_bridge_id": cid, **payload})
        for obl in raw["obligation_refs"]:
            component_refs[obl].append(cid)
            component_types[obl].add("TRANSFER_BRIDGE")

    if demand["learning_purpose"] == "COMPETITIVE_EXAM" and not transfer_bridges:
        fail("ASSIMILATION_COMPILER_COMPETITION_TRANSFER_REQUIRED")

    expected_constraints = {x["constraint_id"]: x for x in demand["owner_constraints"]}
    supplied_compliance = {}
    for row in spec["owner_constraint_compliance"]:
        cid = row["constraint_id"]
        if cid in supplied_compliance:
            fail("ASSIMILATION_COMPILER_OWNER_COMPLIANCE_DUPLICATE", cid)
        if cid not in expected_constraints:
            fail("ASSIMILATION_COMPILER_OWNER_CONSTRAINT_UNKNOWN", cid)
        if expected_constraints[cid]["mode"] == "HARD" and row["disposition"] != "SATISFIED":
            fail("ASSIMILATION_COMPILER_HARD_OWNER_CONSTRAINT_UNSATISFIED", cid)
        supplied_compliance[cid] = copy.deepcopy(row)
    missing_constraints = set(expected_constraints) - set(supplied_compliance)
    if missing_constraints:
        fail("ASSIMILATION_COMPILER_OWNER_COMPLIANCE_MISSING", sorted(missing_constraints)[0])

    obligation_coverage = []
    for obl_id, obl in obligation_rows.items():
        required = set(COMPONENT_REQUIREMENTS[obl["obligation_type"]])
        missing = required - component_types[obl_id]
        if missing:
            fail("ASSIMILATION_COMPILER_OBLIGATION_COMPONENT_MISSING", f"{obl_id}:{sorted(missing)[0]}")
        refs = sorted(set(component_refs[obl_id]))
        if len(refs) < 2:
            fail("ASSIMILATION_COMPILER_OBLIGATION_UNDERDECOMPOSED", obl_id)
        obligation_coverage.append({
            "obligation_ref": obl_id,
            "component_refs": refs,
            "coverage_status": "COVERED",
        })

    if {x["obligation_ref"] for x in obligation_coverage} != obligation_ids:
        fail("ASSIMILATION_COMPILER_COVERAGE_INCOMPLETE")

    plan = {
        "assimilation_plan_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "run_ref": run["run_id"],
        "bundle_ref": bundle_ref,
        "assimilation_demand_ref": demand["assimilation_demand_id"],
        "assimilation_demand_digest": demand["demand_digest"],
        "learning_purpose": demand["learning_purpose"],
        "cognitive_transformations": sorted(transformations, key=lambda x: x["transformation_id"]),
        "learning_atoms": sorted(atoms, key=lambda x: x["atom_id"]),
        "inference_chains": sorted(inference_chains, key=lambda x: x["inference_chain_id"]),
        "equation_assimilations": sorted(equation_assimilations, key=lambda x: x["equation_assimilation_id"]),
        "representation_requirements": sorted(representation_requirements, key=lambda x: x["representation_requirement_id"]),
        "representation_candidates": sorted(representation_candidates, key=lambda x: x["representation_candidate_id"]),
        "representation_decisions": sorted(representation_decisions, key=lambda x: x["representation_decision_id"]),
        "misconception_contrasts": sorted(misconception_contrasts, key=lambda x: x["misconception_contrast_id"]),
        "symbol_bridges": sorted(symbol_bridges, key=lambda x: x["symbol_bridge_id"]),
        "fading_plans": sorted(fading_plans, key=lambda x: x["fading_plan_id"]),
        "transfer_bridges": sorted(transfer_bridges, key=lambda x: x["transfer_bridge_id"]),
        "owner_constraint_compliance": sorted(supplied_compliance.values(), key=lambda x: x["constraint_id"]),
        "obligation_coverage": sorted(obligation_coverage, key=lambda x: x["obligation_ref"]),
        "unresolved_issue_refs": sorted(set(demand["unresolved_issue_refs"] + spec["unresolved_issue_refs"])),
        "status": "ASSIMILATION_READY",
        "plan_digest": "",
    }
    identity = {k: v for k, v in plan.items() if k not in {"assimilation_plan_id", "plan_digest"}}
    plan["assimilation_plan_id"] = "MATH-AP-" + digest(identity)[:16]
    plan["plan_digest"] = digest(plan, "plan_digest")
    validate_assimilation_plan(plan)
    return plan


def apply_assimilation_plan(run: dict, plan: dict) -> dict:
    validate_learning_run(run)
    validate_assimilation_plan(plan)
    if run["current_state"] != "JOIN_READY":
        fail("ASSIMILATION_PLAN_APPLY_REQUIRES_JOIN_READY", run["current_state"])
    if plan["run_ref"] != run["run_id"]:
        fail("ASSIMILATION_PLAN_RUN_MISMATCH")
    if plan["status"] != "ASSIMILATION_READY":
        fail("ASSIMILATION_PLAN_NOT_READY", plan["status"])

    out = copy.deepcopy(run)
    target = _bundle(out, plan["bundle_ref"])
    if target["join_ref"] != plan["assimilation_demand_ref"]:
        fail("ASSIMILATION_PLAN_JOIN_BINDING_MISMATCH")
    target["assimilation_plan_ref"] = plan["assimilation_plan_id"]
    if all(b["assimilation_plan_ref"] for b in out["bundles"]):
        out["current_state"] = "ASSIMILATION_COMPILED"
        out["state_history"].append({
            "sequence": len(out["state_history"]),
            "state": "ASSIMILATION_COMPILED",
            "reason_code": "ASSIMILATION_PLANS_COMPILED",
        })
    return seal_learning_run(out)


def _write(path: str, value: dict) -> None:
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Compile Mathematics AssimilationDemand into a validated Core1A AssimilationPlan."
    )
    ap.add_argument("--run", required=True)
    ap.add_argument("--demand", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out-plan", required=True)
    ap.add_argument("--out-run", required=True)
    args = ap.parse_args()

    run = load(args.run)
    plan = compile_assimilation_plan(run, load(args.demand), load(args.spec))
    updated = apply_assimilation_plan(run, plan)
    _write(args.out_plan, plan)
    _write(args.out_run, updated)
    print(json.dumps({
        "status": plan["status"],
        "assimilation_plan_id": plan["assimilation_plan_id"],
        "run_state": updated["current_state"],
        "obligations": len(plan["obligation_coverage"]),
        "learning_atoms": len(plan["learning_atoms"]),
        "representation_decisions": len(plan["representation_decisions"]),
        "transfer_bridges": len(plan["transfer_bridges"]),
    }, indent=2))


if __name__ == "__main__":
    main()
