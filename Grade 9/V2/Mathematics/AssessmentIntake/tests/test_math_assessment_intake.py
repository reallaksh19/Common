#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(D/"engine"))
from build_math_assessment_intake import build_intake, digest, digest_without_field, source_payload

load = lambda name: json.loads((D/"fixtures"/name).read_text(encoding="utf-8"))
qs = load("mixed-grade9-question-set.fixture.json")
scope = load("mixed-grade9-topic-scope.fixture.json")
attempts = load("mixed-grade9-attempt-set.fixture.json")
example = load("math-assessment-intake.example.json")

# Positive path, attempts present.
result = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), copy.deepcopy(attempts), "MATH-G9-MIXED-PT2-INTAKE-EXAMPLE")
assert result == example
assert result["attempt_mode"] == "PRESENT"
assert result["binding_summary"] == {
    "question_count": 14,
    "subpart_count": 3,
    "attempt_count": 5,
    "explicit_binding_count": 5,
}
# Low confidence is preserved and surfaced rather than silently promoted.
assert result["source_quality_summary"]["minimum_extraction_confidence"] == 0.88
assert result["source_quality_summary"]["low_confidence_question_refs"] == ["Q14"]

# AttemptSet is actually optional.
cold = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), None, "NO-ATTEMPT")
assert cold["attempt_mode"] == "ABSENT"
assert cold["attempt_set_ref"] is None and cold["attempt_set_digest"] is None
assert cold["binding_summary"]["attempt_count"] == 0

# MCQ options survive exactly.
q5 = next(q for q in qs["questions"] if q["question_id"] == "Q5")
assert [o["label"] for o in q5["options"]] == ["a","b","c","d"]
assert q5["options"][3]["text"] == "y=(2/3)x-11/3"

# Multi-part structure survives exactly.
q14 = next(q for q in qs["questions"] if q["question_id"] == "Q14")
assert [p["part_id"] for p in q14["subparts"]] == ["Q14.a","Q14.b","Q14.c"]

# Falsifier: MCQ option lost, even if question-set digest is recomputed.
bad = copy.deepcopy(qs)
q5b = next(q for q in bad["questions"] if q["question_id"] == "Q5")
q5b["options"].pop()
q5b["source_provenance"]["source_digest"] = digest(source_payload(q5b))
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
try:
    build_intake(bad, scope, None)
    raise AssertionError("MCQ_OPTION_LOST accepted")
except ValueError as e:
    assert "MCQ_OPTION_LOST" in str(e)

# Falsifier: question parts merged.
bad = copy.deepcopy(qs)
q14b = next(q for q in bad["questions"] if q["question_id"] == "Q14")
q14b["subparts"] = [q14b["subparts"][0]]
q14b["source_provenance"]["source_digest"] = digest(source_payload(q14b))
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
try:
    build_intake(bad, scope, None)
    raise AssertionError("QUESTION_PART_MERGED accepted")
except ValueError as e:
    assert "QUESTION_PART_MERGED" in str(e)

# Falsifier: a source given changes without the immutable source digest changing.
bad = copy.deepcopy(qs)
q7b = next(q for q in bad["questions"] if q["question_id"] == "Q7")
q7b["givens"][1]["text"] = "B=(3,2)"
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
try:
    build_intake(bad, scope, None)
    raise AssertionError("SOURCE_GIVEN_CHANGED accepted")
except ValueError as e:
    assert "SOURCE_GIVEN_CHANGED" in str(e)

# Falsifier: attempt bound to a part that does not belong to its question.
bad_attempts = copy.deepcopy(attempts)
bad_attempts["attempts"][3]["question_ref"] = "Q13"
bad_attempts["attempt_set_digest"] = digest_without_field(bad_attempts, "attempt_set_digest")
try:
    build_intake(qs, scope, bad_attempts)
    raise AssertionError("ATTEMPT_BOUND_TO_WRONG_ITEM accepted")
except ValueError as e:
    assert "ATTEMPT_BOUND_TO_WRONG_ITEM" in str(e)

# Falsifier: page-order binding is forbidden.
bad_attempts = copy.deepcopy(attempts)
bad_attempts["attempts"][0]["binding_method"] = "PAGE_ORDER"
bad_attempts["attempt_set_digest"] = digest_without_field(bad_attempts, "attempt_set_digest")
try:
    build_intake(qs, scope, bad_attempts)
    raise AssertionError("page-order identity accepted")
except ValueError as e:
    assert "SOURCE_IDENTITY_DEPENDS_ON_PAGE_ORDER" in str(e)

# Reordering source list cannot break explicit attempt identity.
reordered = copy.deepcopy(qs)
reordered["questions"] = list(reversed(reordered["questions"]))
reordered["question_set_digest"] = digest_without_field(reordered, "question_set_digest")
replay = build_intake(reordered, scope, attempts, "REORDERED")
assert replay["binding_summary"]["explicit_binding_count"] == 5

# Deterministic replay.
a = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), copy.deepcopy(attempts), "DET")
b = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), copy.deepcopy(attempts), "DET")
assert json.dumps(a, sort_keys=True, separators=(",",":")) == json.dumps(b, sort_keys=True, separators=(",",":"))

print("MATH M-A assessment-intake falsifiers = 10 PASS")
