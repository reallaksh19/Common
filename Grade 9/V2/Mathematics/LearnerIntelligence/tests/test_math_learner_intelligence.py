#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))
from derive_math_learner_state import canon, derive


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def state_map(result):
    return {x["capability_ref"]: x for x in result["learner_state_snapshot"]["capability_states"]}


questions = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-question-set.fixture.json")
attempts = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-attempt-set.fixture.json")
reviews = load(MATH / "AssessmentReview/registry/assessment-item-validity-registry.json")
authority = load(MATH / "AssessmentScope/authority/math-assessment-scope-authority.json")
item_semantics = load(MATH / "ProblemSemantics/registry/mixed-grade9-item-semantics.json")
registry = load(ROOT / "registry/math-observation-type-registry.json")
reviewed = load(ROOT / "fixtures/reviewed-observations.fixture.json")

present = derive(questions, reviews, authority, item_semantics, registry, attempts, reviewed)
absent = derive(questions, reviews, authority, item_semantics, registry)
ps = state_map(present)
ns = state_map(absent)

# 1. AttemptSet is optional and cannot alter assessment scope.
assert present["learner_state_snapshot"]["scope_fingerprint"] == absent["learner_state_snapshot"]["scope_fingerprint"]
assert absent["evidence_ledger"]["attempt_mode"] == "ABSENT"
assert absent["observations"] == [] and absent["learner_state_snapshot"]["diagnostic_cases"] == []
assert all(x["readiness"] == "UNKNOWN" for x in ns.values()), "NO_ATTEMPT != WEAK"

# 2. Correct geometry survives the later binomial failure.
assert ps["MATH-GEOMETRIC-MODELLING"]["readiness"] == "READY"
assert ps["MATH-EQUIDISTANCE-COORDINATE-MODEL"]["readiness"] == "READY"
assert ps["MATH-BINOMIAL-SQUARE-EXPANSION"]["readiness"] == "DEVELOPING"

# 3. Correct river model survives downstream arithmetic execution failure.
assert ps["MATH-RIVER-CURRENT-MODEL"]["readiness"] == "READY"
assert ps["MATH-ARITHMETIC-DIVISION"]["readiness"] == "DEVELOPING"

# 4. One ordinary error never becomes a confirmed misconception / repair-required state.
cases = present["learner_state_snapshot"]["diagnostic_cases"]
assert cases and all(x["hypothesis_status"] in {"SUSPECTED", "UNRESOLVED", "CORROBORATED"} for x in cases)
assert all(x["readiness"] in {"UNKNOWN", "DEVELOPING", "READY"} for x in ps.values())
assert any(x["target_capability_ref"] == "MATH-BINOMIAL-SQUARE-EXPANSION" and x["hypothesis_status"] == "SUSPECTED" for x in cases)

# 5. M-B diagnostic safety wins: Q9 is POSITIVE_EVIDENCE_ONLY, so a negative observation cannot punish the learner.
q9_negative = copy.deepcopy(reviewed)
q9_negative["observations"].append({
    "observation_id": "OBS-Q9-NEGATIVE-FALSIFIER",
    "attempt_id": "ATT-Q9",
    "question_ref": "Q9",
    "part_ref": None,
    "step_ref": "Q9-S3",
    "observation_type": "INVALID_EQUALITY_TRANSFORMATION",
    "capability_refs": ["MATH-EQUALITY-PRESERVATION"],
    "expected_relation": "Use an equality-preserving transformation.",
    "observed_relation": "Synthetic negative falsifier for M-B safety.",
    "reviewer_confidence": 1.0,
})
blocked = derive(questions, reviews, authority, item_semantics, registry, attempts, q9_negative)
bobs = {x["observation_id"]: x for x in blocked["observations"]}
assert bobs["OBS-Q9-NEGATIVE-FALSIFIER"]["diagnostic_use"] == "POSITIVE_EVIDENCE_ONLY"
assert bobs["OBS-Q9-NEGATIVE-FALSIFIER"]["diagnostic_eligible"] is False
assert state_map(blocked)["MATH-EQUALITY-PRESERVATION"]["readiness"] == "UNKNOWN"
assert not any(x["target_capability_ref"] == "MATH-EQUALITY-PRESERVATION" for x in blocked["learner_state_snapshot"]["diagnostic_cases"])

# 6. Confidence can only decrease through the evidence chain, never inflate.
qconf = {q["question_id"]: q["source_provenance"]["extraction_confidence"] for q in questions["questions"]}
for obs in present["observations"]:
    attempt = next(a for a in attempts["attempts"] if a["attempt_id"] == obs["attempt_id"])
    assert obs["effective_confidence"] <= obs["reviewer_confidence"]
    assert obs["effective_confidence"] <= attempt["extraction_confidence"]
    qref = attempt["question_ref"]
    assert obs["effective_confidence"] <= qconf[qref]
for st in ps.values():
    related = [x for x in present["observations"] if x["observation_id"] in st["observation_refs"]]
    if related:
        assert st["confidence"] <= min(x["effective_confidence"] for x in related)

# 7. Copy/transcription risk is not converted into mathematical weakness.
copy_obs = next(x for x in present["observations"] if x["observation_type"] == "COPY_TRANSCRIPTION_ERROR")
assert copy_obs["polarity"] == "QUALITY_RISK"
assert copy_obs["capability_refs"] == []

# 8. Verification behavior is distinct from verification capability diagnosis.
assert present["learner_state_snapshot"]["verification_behavior"]["self_initiated_verification_observed"] is False
assert ps["MATH-SOLUTION-VERIFICATION"]["readiness"] == "UNKNOWN"

# 9. Required issue #240 observation vocabulary is present.
required_types = {
    "CORRECT_MODEL_SELECTION", "CORRECT_RELATION_SETUP", "INVALID_EQUALITY_TRANSFORMATION",
    "EXPRESSION_IDENTITY_LOSS", "INCORRECT_BINOMIAL_EXPANSION", "ORDERED_PAIR_ROLE_CONFUSION",
    "SLOPE_ORIENTATION_ERROR", "COPY_TRANSCRIPTION_ERROR", "VERIFICATION_NOT_PERFORMED", "VERIFICATION_FAILED",
}
assert required_types <= {x["observation_type"] for x in registry["types"]}

# 10. Deterministic replay.
present2 = derive(questions, reviews, authority, item_semantics, registry, attempts, reviewed)
assert canon(present) == canon(present2)

print("MATH M-E learner-evidence falsifiers PASS (10 groups)")
