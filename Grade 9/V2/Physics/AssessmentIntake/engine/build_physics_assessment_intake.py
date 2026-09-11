#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path

LOW_CONFIDENCE_THRESHOLD = 0.90

def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def digest_without_field(value, field):
    clone = copy.deepcopy(value)
    clone.pop(field, None)
    return digest(clone)

def representation_payload(rep):
    clone = copy.deepcopy(rep)
    clone.pop("representation_digest", None)
    return clone

def source_payload(question):
    return {
        "question_id": question["question_id"],
        "source_order": question["source_order"],
        "section": question["section"],
        "marks": question["marks"],
        "stem": question["stem"],
        "subparts": question["subparts"],
        "options": question["options"],
        "givens": question["givens"],
        "units": question["units"],
        "figure_refs": question["figure_refs"],
        "time_intervals": question["time_intervals"],
        "stated_reference_frame": question["stated_reference_frame"],
        "stated_positive_direction": question["stated_positive_direction"],
        "stated_model_assumptions": question["stated_model_assumptions"],
        "answer_key": question["answer_key"],
        "source_locator": question["source_provenance"]["source_locator"],
    }

def current_shape(question):
    reps = question["figure_refs"]
    return {
        "option_count": len(question["options"]),
        "part_count": len(question["subparts"]),
        "figure_count": len(reps),
        "unit_count": len(question["units"]),
        "graph_axis_count": sum(
            len(r.get("axes", [])) for r in reps
            if r["kind"] in ("GRAPH", "OPTION_FIGURE")
        ),
        "vector_direction_count": sum(len(r.get("vectors", [])) for r in reps),
        "missing_figure_count": sum(
            1 for r in reps if r["status"] == "MISSING_OR_TRUNCATED"
        ),
    }

def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)

def validate_representation(rep):
    expected = digest(representation_payload(rep))
    if rep["representation_digest"] != expected:
        if rep["kind"] in ("GRAPH", "OPTION_FIGURE"):
            fail("GRAPH_AXIS_OR_SIGN_LOST", rep["representation_id"])
        if rep.get("vectors"):
            fail("VECTOR_DIRECTION_CHANGED", rep["representation_id"])
        fail("SOURCE_REPRESENTATION_CHANGED", rep["representation_id"])

    if rep["status"] == "MISSING_OR_TRUNCATED":
        if rep["axes"] or rep["vectors"] or rep["labels"]:
            fail("MISSING_FIGURE_SILENTLY_RECONSTRUCTED", rep["representation_id"])
        return

    if rep["kind"] in ("GRAPH", "OPTION_FIGURE"):
        if len(rep["axes"]) < 2:
            fail("GRAPH_AXIS_OR_SIGN_LOST", rep["representation_id"])
        for axis in rep["axes"]:
            if not axis["quantity"] or not axis["label"]:
                fail("GRAPH_AXIS_OR_SIGN_LOST", rep["representation_id"])
            if axis["positive_direction"] is None:
                fail("GRAPH_AXIS_OR_SIGN_LOST", rep["representation_id"])

    for vector in rep["vectors"]:
        if not vector["direction_text"].strip():
            fail("VECTOR_DIRECTION_CHANGED", rep["representation_id"])

def validate_question(question):
    prov = question["source_provenance"]
    observed = current_shape(question)
    frozen = prov["source_shape"]

    if observed["option_count"] != frozen["option_count"]:
        fail("MCQ_OPTION_LOST", question["question_id"])
    if observed["part_count"] != frozen["part_count"]:
        fail("QUESTION_PART_MERGED", question["question_id"])
    if observed["figure_count"] != frozen["figure_count"]:
        fail("FIGURE_DEPENDENCY_DROPPED", question["question_id"])
    if observed["unit_count"] != frozen["unit_count"]:
        fail("SOURCE_UNIT_CHANGED", question["question_id"])
    if observed["graph_axis_count"] != frozen["graph_axis_count"]:
        fail("GRAPH_AXIS_OR_SIGN_LOST", question["question_id"])
    if observed["vector_direction_count"] != frozen["vector_direction_count"]:
        fail("VECTOR_DIRECTION_CHANGED", question["question_id"])
    if observed["missing_figure_count"] != frozen["missing_figure_count"]:
        fail("MISSING_FIGURE_SILENTLY_RECONSTRUCTED", question["question_id"])

    for rep in question["figure_refs"]:
        validate_representation(rep)

    expected = digest(source_payload(question))
    if expected != prov["source_digest"]:
        fail("SOURCE_GIVEN_CHANGED", question["question_id"])

    option_ids = [x["option_id"] for x in question["options"]]
    part_ids = [x["part_id"] for x in question["subparts"]]
    rep_ids = [x["representation_id"] for x in question["figure_refs"]]
    if len(option_ids) != len(set(option_ids)):
        fail("DUPLICATE_OPTION_ID", question["question_id"])
    if len(part_ids) != len(set(part_ids)):
        fail("DUPLICATE_PART_ID", question["question_id"])
    if len(rep_ids) != len(set(rep_ids)):
        fail("DUPLICATE_REPRESENTATION_ID", question["question_id"])

    valid_option_ids = set(option_ids)
    for rep in question["figure_refs"]:
        if rep["option_ref"] is not None and rep["option_ref"] not in valid_option_ids:
            fail("OPTION_FIGURE_UNBOUND", rep["representation_id"])

def validate_question_set(question_set):
    if question_set["question_set_digest"] != digest_without_field(question_set, "question_set_digest"):
        fail("QUESTION_SET_DIGEST_MISMATCH")
    ids = [q["question_id"] for q in question_set["questions"]]
    if len(ids) != len(set(ids)):
        fail("DUPLICATE_QUESTION_ID")
    orders = [q["source_order"] for q in question_set["questions"]]
    if len(orders) != len(set(orders)):
        fail("DUPLICATE_SOURCE_ORDER")
    for question in question_set["questions"]:
        validate_question(question)

def validate_topic_scope(scope):
    if scope["scope_digest"] != digest_without_field(scope, "scope_digest"):
        fail("DECLARED_TOPIC_SCOPE_DIGEST_MISMATCH")

def validate_attempt_set(attempt_set, question_set):
    if attempt_set["attempt_set_digest"] != digest_without_field(attempt_set, "attempt_set_digest"):
        fail("ATTEMPT_SET_DIGEST_MISMATCH")
    if attempt_set["question_set_ref"] != question_set["question_set_id"]:
        fail("ATTEMPT_QUESTION_SET_MISMATCH")

    by_q = {q["question_id"]: q for q in question_set["questions"]}
    seen = set()
    for attempt in attempt_set["attempts"]:
        if attempt["attempt_id"] in seen:
            fail("DUPLICATE_ATTEMPT_ID", attempt["attempt_id"])
        seen.add(attempt["attempt_id"])
        if attempt["binding_method"] != "EXPLICIT_ID":
            fail("SOURCE_IDENTITY_DEPENDS_ON_PAGE_ORDER", attempt["attempt_id"])
        qref = attempt["question_ref"]
        if qref not in by_q:
            fail("ATTEMPT_BOUND_TO_WRONG_ITEM", attempt["attempt_id"])
        pref = attempt["part_ref"]
        if pref is not None:
            valid_parts = {p["part_id"] for p in by_q[qref]["subparts"]}
            if pref not in valid_parts:
                fail("ATTEMPT_BOUND_TO_WRONG_ITEM", attempt["attempt_id"])

        valid_reps = {r["representation_id"] for r in by_q[qref]["figure_refs"]}
        for rref in attempt["representation_refs"]:
            if rref not in valid_reps:
                fail("ATTEMPT_BOUND_TO_WRONG_REPRESENTATION", attempt["attempt_id"])

def build_intake(question_set, topic_scope, attempt_set=None, intake_id="PHYSICS-ASSESSMENT-INTAKE"):
    validate_question_set(question_set)
    validate_topic_scope(topic_scope)
    if question_set["subject"] != topic_scope["subject"] or question_set["grade"] != topic_scope["grade"]:
        fail("INTAKE_SCOPE_IDENTITY_MISMATCH")
    if attempt_set is not None:
        validate_attempt_set(attempt_set, question_set)

    questions = question_set["questions"]
    min_conf = min(q["source_provenance"]["extraction_confidence"] for q in questions)
    low = sorted(
        q["question_id"] for q in questions
        if q["source_provenance"]["extraction_confidence"] < LOW_CONFIDENCE_THRESHOLD
    )
    corrections = sum(
        len(q["source_provenance"]["human_correction_events"]) for q in questions
    )
    subparts = sum(len(q["subparts"]) for q in questions)
    reps = [r for q in questions for r in q["figure_refs"]]
    graph_reps = [r for r in reps if r["kind"] in ("GRAPH", "OPTION_FIGURE")]
    missing = sorted(
        r["representation_id"] for r in reps
        if r["status"] == "MISSING_OR_TRUNCATED"
    )
    attempt_count = len(attempt_set["attempts"]) if attempt_set is not None else 0
    attempt_rep_bindings = (
        sum(len(a["representation_refs"]) for a in attempt_set["attempts"])
        if attempt_set is not None else 0
    )

    envelope = {
        "intake_id": intake_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "question_set_ref": question_set["question_set_id"],
        "question_set_digest": question_set["question_set_digest"],
        "declared_topic_scope_ref": topic_scope["declared_topic_scope_id"],
        "declared_topic_scope_digest": topic_scope["scope_digest"],
        "attempt_mode": "PRESENT" if attempt_set is not None else "ABSENT",
        "attempt_set_ref": attempt_set["attempt_set_id"] if attempt_set is not None else None,
        "attempt_set_digest": attempt_set["attempt_set_digest"] if attempt_set is not None else None,
        "binding_summary": {
            "question_count": len(questions),
            "subpart_count": subparts,
            "attempt_count": attempt_count,
            "explicit_binding_count": attempt_count,
            "attempt_representation_binding_count": attempt_rep_bindings,
        },
        "source_quality_summary": {
            "minimum_extraction_confidence": min_conf,
            "low_confidence_question_refs": low,
            "human_correction_event_count": corrections,
            "representation_count": len(reps),
            "graph_representation_count": len(graph_reps),
            "missing_or_truncated_representation_refs": missing,
        },
        "intake_digest": "",
    }
    envelope["intake_digest"] = digest_without_field(envelope, "intake_digest")
    return envelope

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--topic-scope", required=True)
    ap.add_argument("--attempts")
    ap.add_argument("--out", required=True)
    ap.add_argument("--intake-id", default="PHYSICS-ASSESSMENT-INTAKE")
    args = ap.parse_args()
    envelope = build_intake(
        load(args.questions),
        load(args.topic_scope),
        load(args.attempts) if args.attempts else None,
        args.intake_id,
    )
    Path(args.out).write_text(
        json.dumps(envelope, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

if __name__ == "__main__":
    main()
