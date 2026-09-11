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
        "figure_refs": question["figure_refs"],
        "units": question["units"],
        "answer_key": question["answer_key"],
        "source_locator": question["source_provenance"]["source_locator"],
    }

def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)

def validate_question(question):
    prov = question["source_provenance"]
    shape = prov["source_shape"]
    if len(question["options"]) != shape["option_count"]:
        fail("MCQ_OPTION_LOST", question["question_id"])
    if len(question["subparts"]) != shape["part_count"]:
        fail("QUESTION_PART_MERGED", question["question_id"])
    if len(question["figure_refs"]) != shape["figure_count"]:
        fail("FIGURE_COUNT_MISMATCH", question["question_id"])
    expected = digest(source_payload(question))
    if expected != prov["source_digest"]:
        fail("SOURCE_GIVEN_CHANGED", question["question_id"])

    option_ids = [x["option_id"] for x in question["options"]]
    part_ids = [x["part_id"] for x in question["subparts"]]
    if len(option_ids) != len(set(option_ids)):
        fail("DUPLICATE_OPTION_ID", question["question_id"])
    if len(part_ids) != len(set(part_ids)):
        fail("DUPLICATE_PART_ID", question["question_id"])

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

def build_intake(question_set, topic_scope, attempt_set=None, intake_id="MATH-ASSESSMENT-INTAKE"):
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
    corrections = sum(len(q["source_provenance"]["human_correction_events"]) for q in questions)
    subparts = sum(len(q["subparts"]) for q in questions)
    attempt_count = len(attempt_set["attempts"]) if attempt_set is not None else 0
    envelope = {
        "intake_id": intake_id,
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
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
        },
        "source_quality_summary": {
            "minimum_extraction_confidence": min_conf,
            "low_confidence_question_refs": low,
            "human_correction_event_count": corrections,
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
    ap.add_argument("--intake-id", default="MATH-ASSESSMENT-INTAKE")
    args = ap.parse_args()
    envelope = build_intake(
        load(args.questions),
        load(args.topic_scope),
        load(args.attempts) if args.attempts else None,
        args.intake_id,
    )
    Path(args.out).write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
