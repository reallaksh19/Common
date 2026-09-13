#!/usr/bin/env python3
"""Compile the durable Chemistry Core1A bucket build queue from a bucket plan."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

PRE_REALIZATION_GATES = [
    "INDEX_SYNC",
    "SOURCE_AND_CORE2_AUDIT",
    "LEARNER_BINDING",
    "LEARNING_ATOM_DECOMPOSITION",
    "HINT_PRETEACH_CLOSURE",
    "PROBLEM_FAMILY_ASSIMILATION",
    "REPRESENTATION_PLAN",
    "READINESS_GATE_DEFINED",
]


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    value = copy.deepcopy(obj)
    if field:
        value.pop(field, None)
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def compile_build_state(bucket_plan, build_state_id="CHEM-C1A-BUILD-STATE-PILOT-v1"):
    if bucket_plan.get("coverage", {}).get("status") != "PASS":
        fail("CORE1A_BUILD_STATE_REQUIRES_CLOSED_BUCKET_PLAN")
    entries = []
    for bucket in bucket_plan["buckets"]:
        count = len(bucket["core2_primary_question_refs"])
        if count == 0:
            state = "SKIP_NO_PRIMARY_CORE2"
            reason = "No primary Core2 question in the current governed transfer plan; bucket remains available as prerequisite support."
        else:
            state = "READY_FOR_REALIZATION"
            reason = None
        entries.append(
            {
                "bucket_id": bucket["bucket_id"],
                "primary_core2_question_count": count,
                "publication_state": state,
                "completed_gates": list(PRE_REALIZATION_GATES),
                "blocking_reason": reason,
            }
        )
    active = [row["bucket_id"] for row in entries if row["publication_state"] == "READY_FOR_REALIZATION"]
    out = {
        "build_state_id": build_state_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "bucket_plan_ref": bucket_plan["plan_id"],
        "bucket_plan_digest": bucket_plan["plan_digest"],
        "entries": entries,
        "next_active_bucket": active[0] if active else None,
        "summary": {
            "bucket_count": len(entries),
            "active_count": sum(row["publication_state"] in {"READY_FOR_REALIZATION", "REALIZATION_IN_PROGRESS"} for row in entries),
            "skipped_count": sum(row["publication_state"] == "SKIP_NO_PRIMARY_CORE2" for row in entries),
            "complete_count": sum(row["publication_state"] == "COMPLETE" for row in entries),
            "blocked_count": sum(row["publication_state"] == "BLOCKED" for row in entries),
        },
        "build_state_digest": "",
    }
    out["build_state_digest"] = digest(out, "build_state_digest")
    validate_build_state(out, bucket_plan)
    return out


def validate_build_state(state, bucket_plan):
    if state.get("build_state_digest") != digest(state, "build_state_digest"):
        fail("CORE1A_BUILD_STATE_DIGEST_MISMATCH")
    if state.get("bucket_plan_ref") != bucket_plan.get("plan_id") or state.get("bucket_plan_digest") != bucket_plan.get("plan_digest"):
        fail("CORE1A_BUILD_STATE_PLAN_BINDING_MISMATCH")
    bucket_ids = [bucket["bucket_id"] for bucket in bucket_plan["buckets"]]
    state_ids = [row["bucket_id"] for row in state["entries"]]
    if state_ids != bucket_ids:
        fail("CORE1A_BUILD_STATE_INDEX_DRIFT")
    for bucket, row in zip(bucket_plan["buckets"], state["entries"]):
        expected_count = len(bucket["core2_primary_question_refs"])
        if row["primary_core2_question_count"] != expected_count:
            fail("CORE1A_BUILD_STATE_QUESTION_COUNT_DRIFT", row["bucket_id"])
        if expected_count == 0 and row["publication_state"] != "SKIP_NO_PRIMARY_CORE2":
            fail("CORE1A_BUILD_STATE_ZERO_PRIMARY_NOT_SKIPPED", row["bucket_id"])
        if expected_count > 0 and row["publication_state"] == "SKIP_NO_PRIMARY_CORE2":
            fail("CORE1A_BUILD_STATE_ACTIVE_BUCKET_SKIPPED", row["bucket_id"])
        if not set(PRE_REALIZATION_GATES).issubset(row["completed_gates"]):
            fail("CORE1A_BUILD_STATE_PRE_REALIZATION_GATES_MISSING", row["bucket_id"])
    eligible = [row["bucket_id"] for row in state["entries"] if row["publication_state"] in {"READY_FOR_REALIZATION", "REALIZATION_IN_PROGRESS"}]
    if state["next_active_bucket"] != (eligible[0] if eligible else None):
        fail("CORE1A_BUILD_STATE_NEXT_BUCKET_DRIFT")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket-plan", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--build-state-id", default="CHEM-C1A-BUILD-STATE-PILOT-v1")
    args = parser.parse_args()
    state = compile_build_state(load(args.bucket_plan), args.build_state_id)
    Path(args.out).write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
