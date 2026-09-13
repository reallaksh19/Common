#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate():
    names = [
        "architecture-blueprint.schema.json",
        "packet-envelope.schema.json",
        "evidence-state.schema.json",
        "routing-decision.schema.json",
        "independent-validation-session.schema.json",
        "join-packet.schema.json",
        "role-bindings.schema.json",
        "learner-purpose-control-state.schema.json",
        "core1a-stage-run.schema.json",
        "topic-blueprint.schema.json",
        "publication-ir.schema.json",
        "render-custody.schema.json",
        "render-preflight-report.schema.json",
    ]
    schemas = {n: load(ROOT / "contracts" / n) for n in names}
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)

    Draft202012Validator(schemas["architecture-blueprint.schema.json"]).validate(load(ROOT / "policy" / "architecture.v1.json"))
    bindings = load(ROOT / "policy" / "role-bindings.v1.json")
    Draft202012Validator(schemas["role-bindings.schema.json"]).validate(bindings)

    ev = Draft202012Validator(schemas["evidence-state.schema.json"])
    for f in sorted((ROOT / "fixtures" / "golden").glob("*.json")):
        ev.validate(load(f)["evidence"])

    architecture = load(ROOT / "policy" / "architecture.v1.json")
    if (
        architecture["role_lifecycle"]["CORE2A"] != "ACTIVE"
        or not architecture["invariants"]["core2a_requires_taught_state_receipts"]
        or not architecture["invariants"]["core2a_may_not_infer_learner_mastery"]
    ):
        raise AssertionError("CORE2A_BLUEPRINT_GUARD_DRIFT")
    if architecture["invariants"]["max_subtopics_per_handoff"] != 3 or not architecture["invariants"]["learning_atoms_unbounded"]:
        raise AssertionError("TRANSPORT_PEDAGOGY_BOUND_DRIFT")
    if bindings["canonical_root"] != "Grade 9/V2/Physics/Blueprint" or bindings["roles"]["JOIN"]["ownership"] != "BLUEPRINT_NATIVE":
        raise AssertionError("PHYSICS_BLUEPRINT_ROLE_BINDING_DRIFT")

    independent = load(ROOT / "policy" / "independent-validation.v1.json")
    join = load(ROOT / "policy" / "join-policy.v1.json")
    purpose = load(ROOT / "policy" / "purpose-contracts.v1.json")
    c1a = load(ROOT / "policy" / "core1a-stage-machine.v1.json")
    pub = load(ROOT / "policy" / "publication-boundary.v1.json")
    render = load(ROOT / "policy" / "render-preflight.v1.json")

    if not independent["self_validation_forbidden"] or not independent["fresh_validator_instance_required"]:
        raise AssertionError("INDEPENDENT_VALIDATION_POLICY_DISABLED")
    if join["coverage_rule"] != "EVERY_CORE2_DEMAND_CLAIM_EXACTLY_ONCE" or not join["critical_conflict_blocks_core1a"]:
        raise AssertionError("JOIN_POLICY_DRIFT")
    if purpose["invariant"] != "PURPOSE_CANNOT_BYPASS_REQUIRED_PREREQUISITES" or set(purpose["purposes"]) != {"FIRST_STUDY","PRACTICE","REVISION","COMPETITIVE_EXAM"}:
        raise AssertionError("PURPOSE_POLICY_DRIFT")
    if len(c1a["pre_manuscript_stages"]) != 12 or c1a["manuscript_stage"] != "1A12_MANUSCRIPT" or c1a["rules"]["unresolved_required_jump_count_must_equal"] != 0:
        raise AssertionError("CORE1A_STAGE_MACHINE_DRIFT")
    if pub["semantic_authority"] != "UPSTREAM_ONLY" or pub["renderer_authority"] != "COMPOSITION_ONLY" or not pub["renderer_semantic_generation_forbidden"]:
        raise AssertionError("PUBLICATION_AUTHORITY_BOUNDARY_DRIFT")
    if render["release_rule"]["machine_preflight_can_authorize_release"] or not render["release_rule"]["human_visual_review_required"]:
        raise AssertionError("RENDER_RELEASE_GATE_DRIFT")
    if render["page_geometry"]["format"] != "A4_PORTRAIT" or render["sample_raster_dpi"] < 144:
        raise AssertionError("RENDER_PHYSICAL_QA_POLICY_DRIFT")

    print("Blueprint contracts: PASS")


if __name__ == "__main__":
    validate()
