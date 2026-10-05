"""Exact question projections with the original source retained separately."""

from __future__ import annotations

from .contracts import digest, load, require, strings, text, unique, verify_file


SOURCE_FIELDS = ("question_id", "stem", "options", "subparts", "figures", "conditions", "source_locator")


def source_projection(question: dict) -> dict:
    return {field: question.get(field, [] if field in {"options", "subparts", "figures", "conditions"} else None)
            for field in SOURCE_FIELDS}


def source_questions(manifest: dict, source_root) -> dict:
    result = {}
    for item in manifest["items"]:
        if item["kind"] != "QUESTIONS" or item["availability"] not in {"PRESENT", "PARTIAL"}:
            continue
        normalized = item.get("normalized_questions")
        if normalized is None:
            require(item.get("format") == "QUESTION_RECORDS_JSON", "QUESTION_NORMALIZATION_REQUIRED")
            path = verify_file(source_root, item["file"])
        else:
            path = verify_file(source_root, normalized["file"])
            review = normalized.get("review", {})
            for key in ("reviewer_instance_id", "original_locator_check", "figure_options_check"):
                text(review.get(key), "QUESTION_NORMALIZATION_REVIEW_REQUIRED")
            require(review.get("normalized_sha256") == normalized["file"]["sha256"], "NORMALIZATION_REVIEW_STALE")
        document = load(path)
        rows = unique(document.get("questions", []), "question_id", "SOURCE_QUESTION_DUPLICATE")
        for qid, row in rows.items():
            require(qid not in result, "SOURCE_QUESTION_DUPLICATE", qid)
            text(row.get("stem"), "SOURCE_QUESTION_STEM_REQUIRED")
            text(row.get("source_locator"), "SOURCE_QUESTION_LOCATOR_REQUIRED")
            result[qid] = {"record": source_projection(row), "source_id": item["source_id"],
                           "record_digest": digest(source_projection(row))}
    return result


def validate_question_custody(questions: list[dict], context: dict) -> None:
    indexed = unique(questions, "question_id", "QUESTION_ID_DUPLICATE")
    expected = set()
    for topic in context["manifest"]["subtopics"]:
        if topic["subtopic_id"] in context["subtopic_ids"]:
            expected.update(strings(topic.get("question_ids", []), "SUBTOPIC_QUESTION_IDS_INVALID", allow_empty=True))
    require(set(indexed) == expected, "CORE2_QUESTION_DENOMINATOR_MISMATCH")
    all_sources = source_questions(context["manifest"], context["source_root"])
    for qid, question in indexed.items():
        require(qid in all_sources, "QUESTION_NOT_IN_SOURCE_CORPUS", qid)
        source = all_sources[qid]
        require(source_projection(question) == source["record"], "SOURCE_QUESTION_REWRITTEN", qid)
        binding = question.get("source_record", {})
        require(binding.get("source_id") == source["source_id"] and
                binding.get("sha256") == source["record_digest"], "SOURCE_QUESTION_BINDING_MISMATCH", qid)
