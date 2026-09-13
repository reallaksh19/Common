from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Any

from common import BlueprintError, digest, load_json, write_json


REQUIRED_EVIDENCE = ("syllabus", "authoritative_sources", "question_corpus", "answer_keys", "figures")


def freeze_ground_truth(manifest: dict[str, Any]) -> dict[str, Any]:
    evidence = manifest.get("evidence") or {}
    for key in REQUIRED_EVIDENCE:
        if key not in evidence:
            raise BlueprintError("GROUND_TRUTH_EVIDENCE_CLASS_MISSING", key)
        entry = evidence[key]
        state = entry.get("state")
        refs = entry.get("refs") or []
        if state == "ABSENT" and refs:
            raise BlueprintError("ABSENT_EVIDENCE_HAS_SOURCE_REFS", key)
        if state in {"PRESENT", "PARTIAL"} and not refs:
            raise BlueprintError("PRESENT_EVIDENCE_WITHOUT_SOURCE_REFS", key)
        if "count" in entry and "retained_count" in entry and entry["retained_count"] > entry["count"]:
            raise BlueprintError("GROUND_TRUTH_RETAINED_COUNT_EXCEEDS_TOTAL", key)

    q = evidence["question_corpus"]
    q_state = q.get("state")
    q_count = q.get("retained_count", q.get("count"))
    if q_state in {"ABSENT", "UNKNOWN"}:
        assessment_interpretation = "NO_ASSESSMENT_EVIDENCE"
    elif q_count == 0:
        assessment_interpretation = "NO_ASSESSMENT_ITEMS_IN_SUPPLIED_CORPUS"
    else:
        assessment_interpretation = "ASSESSMENT_EVIDENCE_PRESENT"

    frozen_manifest = deepcopy(manifest)
    manifest_digest = digest(frozen_manifest)
    return {
        "ground_truth_manifest": frozen_manifest,
        "manifest_digest": manifest_digest,
        "assessment_evidence_interpretation": assessment_interpretation,
        "forbidden_inferences": [
            "NO_QUESTIONS_DOES_NOT_IMPLY_ZERO_TOPIC_IMPORTANCE",
            "SPARSE_QUESTIONS_DO_NOT_ESTABLISH_EXAM_FREQUENCY_OR_DIFFICULTY_DISTRIBUTION"
        ],
        "status": "FROZEN"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze a Learning Blueprint ground-truth manifest")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    write_json(Path(args.out), freeze_ground_truth(load_json(args.input)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
