#!/usr/bin/env python3
"""P-G falsifiers: promoted-PCK honesty, SEE/REALIZE/UNDERSTAND completeness, Core1 scope custody."""
import copy, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
sys.path[:0] = [str(ROOT / "engine"), str(ROOT / "tests")]

from build_physics_core1 import (  # noqa: E402
    build_plan, validate_plan, validate_pck_registry, load_pck_registry,
    select_primary_family, structural_flags, digest, load,
)
from upstream import build_upstream  # noqa: E402

PASSES = []


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        PASSES.append(code)
        return
    raise AssertionError("expected " + code)


registry = load_pck_registry()
profile = load(ROOT / "registry" / "physics-instructional-authoring-profile.json")
problems = load(ROOT / "registry" / "physics-problem-authoring-profile.json")
completeness = load(ROOT / "registry" / "physics-core1-scope-completeness-policy.json")
scope, model = build_upstream(attempts=True)
scope_na, model_na = build_upstream(attempts=False)


def build(m=None, s=None, reg=None, prof=None, comp=None, prob=None, plan_id=None):
    return build_plan(
        copy.deepcopy(m or model), copy.deepcopy(s or scope), copy.deepcopy(reg or registry),
        copy.deepcopy(prof or profile), copy.deepcopy(comp or completeness),
        copy.deepcopy(prob or problems), plan_id,
    )


plan = build()
PASSES.append("CORE1_PLAN_BUILDS_FROM_REAL_P_F_MODEL")

# --- determinism -------------------------------------------------------------
assert build()["plan_digest"] == plan["plan_digest"]
PASSES.append("CORE1_PLAN_DETERMINISTIC")

# --- scope custody: every P-F capability gets a lesson ------------------------
assert {l["capability_ref"] for l in plan["lessons"]} == {
    r["capability_ref"] for r in scope["capability_scope_records"]
}
PASSES.append("CORE1_COVERS_FULL_ASSESSMENT_SCOPE")

short = copy.deepcopy(plan)
short["lessons"] = short["lessons"][:-1]
short["plan_digest"] = ""
short["plan_digest"] = digest(short, "plan_digest")
expect("CORE1_IS_ONLY_A_REPAIR_MEMO",
       lambda: validate_plan(short, model, scope, registry, profile, completeness, problems))

# --- honest PCK promotion ----------------------------------------------------
for asset in registry["assets"]:
    auth = asset["promotion_authority"]
    assert auth["promotion_state"] == "PROMOTED_PILOT"
    assert auth["subject_expert_release_state"] == "NOT_GRANTED"
    assert auth["pedagogy_expert_release_state"] == "NOT_GRANTED"
    assert auth["final_product_release_blocked"] is True
PASSES.append("NO_ASSET_CLAIMS_HUMAN_EXPERT_RELEASE")

# FAKE_HUMAN_REVIEW_STATE: a human-only PASS without an attestation is rejected.
faked = copy.deepcopy(registry)
row = next(r for r in faked["assets"][0]["review_ledger"] if r["review_class"] == "SUBJECT_EXPERT_PASS")
row["state"] = "PASS"
faked["assets"][0]["asset_digest"] = ""
faked["assets"][0]["asset_digest"] = digest(faked["assets"][0], "asset_digest")
faked["registry_digest"] = ""
faked["registry_digest"] = digest(faked, "registry_digest")
expect("FAKE_HUMAN_REVIEW_STATE", lambda: validate_pck_registry(faked))

# AI_REVIEW_COUNTED_AS_EXPERT_PASS: relabelling an AI review as an expert pass is rejected
# because the reviewer authority class no longer matches the review class.
laundered = copy.deepcopy(registry)
row = next(
    r for r in laundered["assets"][0]["review_ledger"]
    if r["review_class"] == "AI_ASSISTED_REFERENCE_REVIEW" and r["stage"] == "PEDAGOGICAL"
)
row["review_class"] = "PEDAGOGY_EXPERT_PASS"
laundered["assets"][0]["asset_digest"] = ""
laundered["assets"][0]["asset_digest"] = digest(laundered["assets"][0], "asset_digest")
laundered["registry_digest"] = ""
laundered["registry_digest"] = digest(laundered, "registry_digest")
expect("FABRICATED_EXPERT_REVIEWER_IDENTITY", lambda: validate_pck_registry(laundered))

# ... and an AI review carrying a human attestation ref is rejected outright.
attested_ai = copy.deepcopy(registry)
row = next(
    r for r in attested_ai["assets"][0]["review_ledger"]
    if r["review_class"] == "AI_ASSISTED_REFERENCE_REVIEW"
)
row["attestation_ref"] = "SUBJECT-EXPERT-2026-001"
attested_ai["assets"][0]["asset_digest"] = ""
attested_ai["assets"][0]["asset_digest"] = digest(attested_ai["assets"][0], "asset_digest")
attested_ai["registry_digest"] = ""
attested_ai["registry_digest"] = digest(attested_ai, "registry_digest")
expect("AI_REVIEW_COUNTED_AS_EXPERT_PASS", lambda: validate_pck_registry(attested_ai))

# FABRICATED_PROMOTION_STATE: promotion state is derived, so a declared upgrade is rejected.
overclaim = copy.deepcopy(registry)
overclaim["assets"][0]["promotion_authority"]["promotion_state"] = "PROMOTED_RELEASE"
overclaim["assets"][0]["asset_digest"] = ""
overclaim["assets"][0]["asset_digest"] = digest(overclaim["assets"][0], "asset_digest")
overclaim["registry_digest"] = ""
overclaim["registry_digest"] = digest(overclaim, "registry_digest")
expect("FABRICATED_PROMOTION_STATE", lambda: validate_pck_registry(overclaim))

# A plan that claims an expert pass is rejected.
claimed = copy.deepcopy(plan)
claimed["human_expert_review_states"]["SUBJECT_EXPERT_PASS"] = "PASS"
claimed["plan_digest"] = ""
claimed["plan_digest"] = digest(claimed, "plan_digest")
expect("FAKE_HUMAN_REVIEW_STATE",
       lambda: validate_plan(claimed, model, scope, registry, profile, completeness, problems))

# SEE_REALIZE_UNDERSTAND_PHASE_MISSING
no_phase = copy.deepcopy(registry)
no_phase["assets"][0]["realize_phase"] = ""
no_phase["assets"][0]["asset_digest"] = ""
no_phase["assets"][0]["asset_digest"] = digest(no_phase["assets"][0], "asset_digest")
no_phase["registry_digest"] = ""
no_phase["registry_digest"] = digest(no_phase, "registry_digest")
expect("SEE_REALIZE_UNDERSTAND_PHASE_MISSING", lambda: validate_pck_registry(no_phase))

# NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING (registry level)
naked = copy.deepcopy(registry)
naked["assets"][0]["reconstruction_route"] = ["Apply the formula."]
naked["assets"][0]["asset_digest"] = ""
naked["assets"][0]["asset_digest"] = digest(naked["assets"][0], "asset_digest")
naked["registry_digest"] = ""
naked["registry_digest"] = digest(naked, "registry_digest")
expect("NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING", lambda: validate_pck_registry(naked))

# --- generic (non topic-specific) family selection ---------------------------
# Selection must depend only on structural obligations, never on the capability id.
full = next(l for l in plan["lessons"] if l["lesson_mode"] == "FULL_LEARNING")
rec = next(r for r in model["capability_records"] if r["capability_ref"] == full["capability_ref"])
renamed = copy.deepcopy(rec)
renamed["capability_ref"] = "PHY-CAP-SOME-FUTURE-TOPIC-NOT-IN-ANY-REGISTRY"
assert select_primary_family(renamed, profile) == select_primary_family(rec, profile)
PASSES.append("TOPIC_SPECIFIC_SCHEMA_INSTEAD_OF_GENERIC_PHYSICS_REASONING_ROUTE")

# ... and changing the structure does change the family.
graph_like = copy.deepcopy(rec)
graph_like["representation_requirements"] = ["VELOCITY_TIME_GRAPH"]
assert select_primary_family(graph_like, profile)[0] == "GRAPH_SLOPE_AREA_DECODING"
PASSES.append("FAMILY_SELECTION_IS_STRUCTURAL")

# --- obligation custody ------------------------------------------------------
for l in plan["lessons"]:
    r = next(x for x in model["capability_records"] if x["capability_ref"] == l["capability_ref"])
    assert set(l["representation_requirements"]) == set(r["representation_requirements"])
    assert l["verification_steps"]
    assert l["scope_trace"]["source_scope_trace_item_refs"]
PASSES.append("CORE1_CARRIES_SOURCE_SCOPE_TRACE")

dropped = copy.deepcopy(plan)
target = next(l for l in dropped["lessons"] if l["frame_sign_required"])
target["frame_sign_required"] = False
target["see_system_frame_sign"] = ""
dropped["plan_digest"] = ""
dropped["plan_digest"] = digest(dropped, "plan_digest")
expect("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_CORE1",
       lambda: validate_plan(dropped, model, scope, registry, profile, completeness, problems))

mv = copy.deepcopy(plan)
target = next(l for l in mv["lessons"] if l["model_validity_required"])
target["model_validity_required"] = False
target["understand_relation_and_validity"] = ""
mv["plan_digest"] = ""
mv["plan_digest"] = digest(mv, "plan_digest")
expect("MODEL_VALIDITY_DROPPED_FROM_CORE1",
       lambda: validate_plan(mv, model, scope, registry, profile, completeness, problems))

repdrop = copy.deepcopy(plan)
target = next(l for l in repdrop["lessons"] if l["representation_requirements"])
target["representation_requirements"] = []
repdrop["plan_digest"] = ""
repdrop["plan_digest"] = digest(repdrop, "plan_digest")
expect("REPRESENTATION_REQUIREMENT_DROPPED_FROM_CORE1",
       lambda: validate_plan(repdrop, model, scope, registry, profile, completeness, problems))

verif = copy.deepcopy(plan)
verif["lessons"][0]["verification_steps"] = []
verif["plan_digest"] = ""
verif["plan_digest"] = digest(verif, "plan_digest")
expect("PHYSICAL_VERIFICATION_REDUCED_TO_ANSWER_ONLY",
       lambda: validate_plan(verif, model, scope, registry, profile, completeness, problems))

# --- treatment respect -------------------------------------------------------
ready = [l for l in plan["lessons"] if l["lesson_mode"] == "CONCISE_VERIFY_ONLY"]
assert ready, "fixture must exercise a READY_VERIFY_ONLY capability"
for l in ready:
    assert l["worked_example"] is None and l["guided_attempt"] is None and l["misconception_repair"] is None
PASSES.append("READY_CAPABILITY_NOT_FULLY_RETAUGHT")

padded = copy.deepcopy(plan)
target = next(l for l in padded["lessons"] if l["lesson_mode"] == "CONCISE_VERIFY_ONLY")
donor = next(l for l in padded["lessons"] if l["lesson_mode"] == "FULL_LEARNING")
target["worked_example"] = copy.deepcopy(donor["worked_example"])
padded["plan_digest"] = ""
padded["plan_digest"] = digest(padded, "plan_digest")
expect("READY_CAPABILITY_FULLY_RETAUGHT",
       lambda: validate_plan(padded, model, scope, registry, profile, completeness, problems))

# treatment may not be rewritten by the authoring layer
retreat = copy.deepcopy(plan)
retreat["lessons"][0]["treatment"] = "REPAIR_BEFORE"
retreat["plan_digest"] = ""
retreat["plan_digest"] = digest(retreat, "plan_digest")
expect("PCK_DECIDES_TREATMENT",
       lambda: validate_plan(retreat, model, scope, registry, profile, completeness, problems))

# --- new Core1 instances, not transfer leakage -------------------------------
for l in plan["lessons"]:
    if l["worked_example"]:
        assert l["worked_example"]["source_class"] == "NEW_AUTHORED_CORE1"
        assert l["worked_example"]["external_candidate_refs"] == []
        assert l["worked_example"]["problem_family_ref"]
PASSES.append("CORE1_USES_NEW_AUTHORED_INSTANCES")

leak = copy.deepcopy(plan)
target = next(l for l in leak["lessons"] if l["worked_example"])
target["worked_example"]["external_candidate_refs"] = ["EXT-PYQ-001"]
leak["plan_digest"] = ""
leak["plan_digest"] = digest(leak, "plan_digest")
expect("CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE",
       lambda: validate_plan(leak, model, scope, registry, profile, completeness, problems))

nofam = copy.deepcopy(model)
nofam["capability_records"][0]["problem_family_refs"] = []
expect("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY", lambda: build(m=nofam))

# --- misconception repair ----------------------------------------------------
warn_only = copy.deepcopy(plan)
target = next(l for l in warn_only["lessons"] if l["misconception_repair"])
target["misconception_repair"]["repair_steps"] = []
warn_only["plan_digest"] = ""
warn_only["plan_digest"] = digest(warn_only, "plan_digest")
expect("MISCONCEPTION_WARNING_WITHOUT_REPAIR",
       lambda: validate_plan(warn_only, model, scope, registry, profile, completeness, problems))

# --- appendices --------------------------------------------------------------
aps = plan["appendices"]
assert aps["appendix_a"]["present"] and aps["appendix_b"]["present"] and aps["appendix_c"]["present"]
assert len(aps["appendix_b"]["solutions"]) == len(aps["appendix_a"]["items"])
PASSES.append("APPENDICES_A_B_C_PRESENT_AND_ONE_TO_ONE")

noa = copy.deepcopy(plan)
noa["appendices"]["appendix_a"]["present"] = False
noa["plan_digest"] = ""
noa["plan_digest"] = digest(noa, "plan_digest")
expect("APPENDIX_A_MISSING",
       lambda: validate_plan(noa, model, scope, registry, profile, completeness, problems))

partial_b = copy.deepcopy(plan)
partial_b["appendices"]["appendix_b"]["solutions"] = partial_b["appendices"]["appendix_b"]["solutions"][:-1]
partial_b["plan_digest"] = ""
partial_b["plan_digest"] = digest(partial_b, "plan_digest")
expect("APPENDIX_B_INCOMPLETE",
       lambda: validate_plan(partial_b, model, scope, registry, profile, completeness, problems))

answers = copy.deepcopy(plan)
answers["appendices"]["appendix_c"]["answer_free"] = False
answers["plan_digest"] = ""
answers["plan_digest"] = digest(answers, "plan_digest")
expect("HANDOUT_CONTAINS_ANSWERS",
       lambda: validate_plan(answers, model, scope, registry, profile, completeness, problems))

newphys = copy.deepcopy(plan)
newphys["appendices"]["appendix_c"]["introduced_capability_refs"] = ["PHY-CAP-NOT-IN-SCOPE"]
newphys["plan_digest"] = ""
newphys["plan_digest"] = digest(newphys, "plan_digest")
expect("HANDOUT_INTRODUCES_NEW_PHYSICS",
       lambda: validate_plan(newphys, model, scope, registry, profile, completeness, problems))

# --- PR #156 may not be a producer input -------------------------------------
contaminated = copy.deepcopy(problems)
contaminated["pr156_reference_wording"] = "copied layout"
expect("PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON", lambda: build(prob=contaminated))

# --- no-attempt run does not invent weakness ---------------------------------
plan_na = build(m=model_na, s=scope_na)
assert all(l["lesson_mode"] == "FULL_LEARNING" for l in plan_na["lessons"])
assert all(
    r["learner_state"] == "UNKNOWN" for r in model_na["capability_records"]
)
PASSES.append("NO_ATTEMPT_RUN_INVENTS_PHYSICS_WEAKNESS")

# the assessment-derived structure must be identical with and without attempts
assert plan_na["study_scope_digest"] == plan["study_scope_digest"]
PASSES.append("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE")

print(f"PHY P-G Core1 authoring falsifiers: {len(PASSES)} PASS")
for code in PASSES:
    print("  -", code)
