#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(D / "engine"))
from build_physics_assessment_intake import (
    build_intake, digest_without_field, representation_payload, source_payload, digest
)

load = lambda name: json.loads((D / "fixtures" / name).read_text(encoding="utf-8"))
qs = load("motion-question-set.fixture.json")
scope = load("motion-topic-scope.fixture.json")
attempts = load("motion-attempt-set.fixture.json")
example = load("physics-assessment-intake.example.json")

def must_fail(code, fn):
    try:
        fn()
        raise AssertionError(f"{code} accepted")
    except ValueError as e:
        assert code in str(e), (code, str(e))

# Positive path.
result = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), copy.deepcopy(attempts), "PHY-G9-MOTION-INTAKE-EXAMPLE")
assert result == example
assert result["binding_summary"] == {
    "question_count": 14,
    "subpart_count": 3,
    "attempt_count": 5,
    "explicit_binding_count": 5,
    "attempt_representation_binding_count": 3,
}
assert result["source_quality_summary"]["minimum_extraction_confidence"] == 0.86
assert result["source_quality_summary"]["low_confidence_question_refs"] == ["Q13", "Q14"]
assert result["source_quality_summary"]["representation_count"] == 8
assert result["source_quality_summary"]["graph_representation_count"] == 6
assert result["source_quality_summary"]["missing_or_truncated_representation_refs"] == ["FIG-Q13-MISSING"]

# AttemptSet is truly optional.
cold = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), None, "NO-ATTEMPT")
assert cold["attempt_mode"] == "ABSENT"
assert cold["attempt_set_ref"] is None and cold["attempt_set_digest"] is None
assert cold["binding_summary"]["attempt_count"] == 0

# MCQ options survive.
q5 = next(q for q in qs["questions"] if q["question_id"] == "Q5")
assert [o["label"] for o in q5["options"]] == ["a", "b", "c", "d"]

# Multi-part identity survives.
q14 = next(q for q in qs["questions"] if q["question_id"] == "Q14")
assert [p["part_id"] for p in q14["subparts"]] == ["Q14.a", "Q14.b", "Q14.c"]

# Graph semantics survive.
q8 = next(q for q in qs["questions"] if q["question_id"] == "Q8")
g = q8["figure_refs"][0]
assert [(a["quantity"], a["unit"], a["positive_direction"]) for a in g["axes"]] == [
    ("time", "s", "right"), ("velocity", "m/s", "up")
]

# Falsifier: MCQ option lost.
bad = copy.deepcopy(qs)
next(q for q in bad["questions"] if q["question_id"] == "Q5")["options"].pop()
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("MCQ_OPTION_LOST", lambda: build_intake(bad, scope, None))

# Falsifier: question parts merged.
bad = copy.deepcopy(qs)
next(q for q in bad["questions"] if q["question_id"] == "Q14")["subparts"] = q14["subparts"][:1]
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("QUESTION_PART_MERGED", lambda: build_intake(bad, scope, None))

# Falsifier: source given changed.
bad = copy.deepcopy(qs)
next(q for q in bad["questions"] if q["question_id"] == "Q3")["givens"][0]["text"] = "u = 25 m/s"
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("SOURCE_GIVEN_CHANGED", lambda: build_intake(bad, scope, None))

# Falsifier: source unit lost.
bad = copy.deepcopy(qs)
next(q for q in bad["questions"] if q["question_id"] == "Q3")["units"].pop()
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("SOURCE_UNIT_CHANGED", lambda: build_intake(bad, scope, None))

# Falsifier: figure dependency dropped.
bad = copy.deepcopy(qs)
next(q for q in bad["questions"] if q["question_id"] == "Q8")["figure_refs"] = []
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("FIGURE_DEPENDENCY_DROPPED", lambda: build_intake(bad, scope, None))

# Falsifier: graph sign/axis semantics drift.
bad = copy.deepcopy(qs)
rep = next(q for q in bad["questions"] if q["question_id"] == "Q8")["figure_refs"][0]
rep["axes"][1]["positive_direction"] = "down"
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("GRAPH_AXIS_OR_SIGN_LOST", lambda: build_intake(bad, scope, None))

# Falsifier: vector direction changed.
bad = copy.deepcopy(qs)
rep = next(q for q in bad["questions"] if q["question_id"] == "Q9")["figure_refs"][0]
rep["vectors"][0]["direction_text"] = "downward"
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("VECTOR_DIRECTION_CHANGED", lambda: build_intake(bad, scope, None))

# Falsifier: missing/truncated figure silently reconstructed.
bad = copy.deepcopy(qs)
rep = next(q for q in bad["questions"] if q["question_id"] == "Q13")["figure_refs"][0]
rep["status"] = "PRESENT"
bad["question_set_digest"] = digest_without_field(bad, "question_set_digest")
must_fail("MISSING_FIGURE_SILENTLY_RECONSTRUCTED", lambda: build_intake(bad, scope, None))

# Falsifier: attempt bound to wrong part.
bad_attempts = copy.deepcopy(attempts)
bad_attempts["attempts"][-1]["question_ref"] = "Q10"
bad_attempts["attempt_set_digest"] = digest_without_field(bad_attempts, "attempt_set_digest")
must_fail("ATTEMPT_BOUND_TO_WRONG_ITEM", lambda: build_intake(qs, scope, bad_attempts))

# Falsifier: attempt bound to representation from another question.
bad_attempts = copy.deepcopy(attempts)
bad_attempts["attempts"][1]["representation_refs"] = ["FIG-Q10-PHASE"]
bad_attempts["attempt_set_digest"] = digest_without_field(bad_attempts, "attempt_set_digest")
must_fail("ATTEMPT_BOUND_TO_WRONG_REPRESENTATION", lambda: build_intake(qs, scope, bad_attempts))

# Falsifier: page-order binding forbidden.
bad_attempts = copy.deepcopy(attempts)
bad_attempts["attempts"][0]["binding_method"] = "PAGE_ORDER"
bad_attempts["attempt_set_digest"] = digest_without_field(bad_attempts, "attempt_set_digest")
must_fail("SOURCE_IDENTITY_DEPENDS_ON_PAGE_ORDER", lambda: build_intake(qs, scope, bad_attempts))

# Reordering source list cannot break explicit attempt identity.
reordered = copy.deepcopy(qs)
reordered["questions"] = list(reversed(reordered["questions"]))
reordered["question_set_digest"] = digest_without_field(reordered, "question_set_digest")
replay = build_intake(reordered, scope, attempts, "REORDERED")
assert replay["binding_summary"]["explicit_binding_count"] == 5

# Deterministic replay.
a = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), copy.deepcopy(attempts), "DET")
b = build_intake(copy.deepcopy(qs), copy.deepcopy(scope), copy.deepcopy(attempts), "DET")
assert json.dumps(a, sort_keys=True, separators=(",", ":")) == json.dumps(b, sort_keys=True, separators=(",", ":"))

print("PHYSICS P-A assessment-intake falsifiers = 14 PASS")
