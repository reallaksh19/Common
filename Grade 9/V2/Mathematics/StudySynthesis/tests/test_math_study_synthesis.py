#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(MATH / "LearnerIntelligence/engine"))
from synthesize_math_study_model import build_study_scope, canon, synthesize
from derive_math_learner_state import derive as derive_learner_state


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def plan_map(model):
    return {x["capability_ref"]: x for x in model["capability_plans"]}


def state_map(snapshot):
    return {x["capability_ref"]: x for x in snapshot["capability_states"]}


def keys_recursive(value):
    if isinstance(value, dict):
        out = set(value)
        for v in value.values():
            out |= keys_recursive(v)
        return out
    if isinstance(value, list):
        out = set()
        for v in value:
            out |= keys_recursive(v)
        return out
    return set()


questions = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-question-set.fixture.json")
attempts = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-attempt-set.fixture.json")
reviews = load(MATH / "AssessmentReview/registry/assessment-item-validity-registry.json")
authority = load(MATH / "AssessmentScope/authority/math-assessment-scope-authority.json")
bindings = load(MATH / "AssessmentScope/registry/mixed-grade9-question-scope-bindings.json")
item_semantics = load(MATH / "ProblemSemantics/registry/mixed-grade9-item-semantics.json")
obs_registry = load(MATH / "LearnerIntelligence/registry/math-observation-type-registry.json")
reviewed = load(MATH / "LearnerIntelligence/fixtures/reviewed-observations.fixture.json")
policy = load(ROOT / "policies/math-treatment-policy.json")

present = derive_learner_state(questions, reviews, authority, item_semantics, obs_registry, attempts, reviewed)["learner_state_snapshot"]
absent = derive_learner_state(questions, reviews, authority, item_semantics, obs_registry)["learner_state_snapshot"]
scope = build_study_scope(bindings, authority)
present_model = synthesize(scope, present, policy)
absent_model = synthesize(scope, absent, policy)
pm = plan_map(present_model)
am = plan_map(absent_model)

# 1. Learner state cannot change WHAT is in assessment scope.
assert present_model["study_scope_digest"] == absent_model["study_scope_digest"] == scope["scope_digest"]
assert set(pm) == set(am) == {x["capability_ref"] for x in scope["capability_scope_records"]}

# 2. Every source item/subpart remains visible. Scope exceptions do not disappear.
binding_items = {x["item_ref"] for x in bindings["bindings"]}
assert set(scope["required_item_refs"]) == binding_items
assert {"Q6", "Q9"} <= set(scope["scope_exception_item_refs"])
assert "MATH-UNORDERED-PAIR-COUNT" in scope["direct_assessed_capability_refs"], "outside-declared-scope assessment evidence was silently deleted"

# 3. NO_ATTEMPT != WEAK and does not force repair/probe.
assert absent["attempt_mode"] == "ABSENT"
assert all(x["learner_state_readiness"] == "UNKNOWN" for x in absent_model["capability_plans"])
assert all(x["treatment"] == "ACTIVE_STUDY" for x in absent_model["capability_plans"])

# 4. READY capabilities are verified, not expanded into full reteaching.
for cap in ["MATH-EQUIDISTANCE-COORDINATE-MODEL", "MATH-RIVER-CURRENT-MODEL", "MATH-LINEAR-PARAMETER-CONDITION"]:
    assert pm[cap]["learner_state_readiness"] == "READY"
    assert pm[cap]["treatment"] == "VERIFY_ONLY"

# 5. Demonstrated downstream execution weaknesses stay localized.
assert pm["MATH-BINOMIAL-SQUARE-EXPANSION"]["learner_state_readiness"] == "DEVELOPING"
assert pm["MATH-BINOMIAL-SQUARE-EXPANSION"]["treatment"] == "REPAIR_IN_UNIT"
assert pm["MATH-ARITHMETIC-DIVISION"]["learner_state_readiness"] == "DEVELOPING"
assert pm["MATH-RIVER-CURRENT-MODEL"]["treatment"] == "VERIFY_ONLY"

# 6. Unknown high-reach prerequisites are not silently diagnosed as weak.
assert pm["MATH-EQUALITY-PRESERVATION"]["learner_state_readiness"] == "UNKNOWN"
assert pm["MATH-EQUALITY-PRESERVATION"]["treatment"] == "ACTIVE_STUDY"

# 7. PROBE_FIRST requires unresolved evidence, not mere absence of evidence.
probe_snapshot = copy.deepcopy(present)
probe_snapshot["diagnostic_cases"].append({
    "diagnostic_case_id": "MATH-DC-SYNTHETIC-PROBE",
    "target_capability_ref": "MATH-ORDERED-PAIR-SEMANTICS",
    "observation_refs": ["OBS-SYNTHETIC-AMBIGUOUS"],
    "hypothesis_status": "UNRESOLVED",
    "evidence_strength": "AMBIGUOUS_OBSERVATION",
    "probe_required": True,
    "probe_target_capability_refs": ["MATH-ORDERED-PAIR-SEMANTICS"],
    "alternative_explanations": ["TRANSCRIPTION_ERROR", "WRONG_MODEL"],
    "diagnostic_policy_version": "MATH-ME-DIAGNOSTIC-v1",
})
probe_model = synthesize(scope, probe_snapshot, policy)
assert plan_map(probe_model)["MATH-ORDERED-PAIR-SEMANTICS"]["treatment"] == "PROBE_FIRST"

# 8. One current success never closes delayed/transfer/fluency/timed obligations.
river = pm["MATH-RIVER-CURRENT-MODEL"]
longitudinal = {x["dimension"]: x for x in river["future_evidence_obligations"]}
for dim in ["delayed_retention", "near_transfer", "far_transfer", "mixed_discrimination", "fluency", "timed_performance"]:
    assert longitudinal[dim]["status"] == "OPEN_FUTURE_EVIDENCE"

# 9. Every StudyModel capability has explicit trace back to StudyScope.
scope_map = {x["capability_ref"]: x for x in scope["capability_scope_records"]}
for cap, plan in pm.items():
    assert cap in scope_map
    assert plan["assessment_question_refs"] == scope_map[cap]["assessment_question_refs"]
    assert plan["prerequisite_refs"] == scope_map[cap]["prerequisite_refs"]

# 10. Treatment changes depth/order, never scope membership.
assert len(pm) == len(am) == len(scope_map)
assert set(present_model["capability_plans"][i]["capability_ref"] for i in range(len(pm))) == set(scope_map)

# 11. Longitudinal dimensions are separate, complete, and non-scalar.
assert present_model["longitudinal_initialization"]["dimensions"] == [
    "acquisition", "independent_reconstruction", "delayed_retention", "near_transfer",
    "far_transfer", "mixed_discrimination", "fluency", "timed_performance",
]
assert "mastery" not in keys_recursive(present_model)
assert "probability" not in keys_recursive(present_model)

# 12. Study Synthesis stops before teaching choreography/publication.
for forbidden in {"hint", "hint_ladder", "page", "layout", "renderer", "worked_example", "lesson_sequence", "practice_count"}:
    assert forbidden not in keys_recursive(present_model)

# 13. Representation/problem-family/verification obligations survive into treatment plans.
assert "GEOMETRIC_DISTANCE_RELATION" in pm["MATH-BINOMIAL-SQUARE-EXPANSION"]["representation_requirements"]
assert "MATH-PF-EQUILATERAL-COORDINATE" in pm["MATH-BINOMIAL-SQUARE-EXPANSION"]["problem_family_refs"]
assert "VERIFY_EQUILATERAL_EQUAL_DISTANCES" in pm["MATH-BINOMIAL-SQUARE-EXPANSION"]["verification_requirements"]

# 14. Learner weakness cannot shrink required assessment scope.
weak_snapshot = copy.deepcopy(present)
for state in weak_snapshot["capability_states"]:
    if state["capability_ref"] == "MATH-BINOMIAL-SQUARE-EXPANSION":
        state["readiness"] = "DEVELOPING"
weak_model = synthesize(scope, weak_snapshot, policy)
assert set(plan_map(weak_model)) == set(scope_map)
assert weak_model["study_scope_digest"] == scope["scope_digest"]

# 15. Deterministic replay.
assert canon(synthesize(scope, present, policy)) == canon(synthesize(scope, present, policy))
assert canon(build_study_scope(bindings, authority)) == canon(build_study_scope(bindings, authority))

print("MATH M-F Study Synthesis falsifiers PASS (15 groups)")
