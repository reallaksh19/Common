#!/usr/bin/env python3
"""Multi-bucket-safe entrypoint for the bound four-producer release golden.

The underlying runner owns the integration mechanics. This entrypoint supplies the
canonical storage rule discovered by the real cold-start corpus: a source question
may participate in multiple teaching buckets, while the Registry stores it under
one deterministic primary subtopic (the first bucket in canonical bucket order).
Additional teaching memberships remain on the Core2A question spec and are not
collapsed by the Registry storage choice.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import run_bound_producer_release_golden as base


def multi_bucket_safe_subtopics(bucket_plan: dict):
    bucket_sid = {}
    cap_sid = {}
    q_sid = {}
    for bucket in bucket_plan["buckets"]:
        sid = "BOUND-SUB-" + base.production_digest(sorted(bucket["member_capability_refs"]))[:12].upper()
        bucket_sid[bucket["bucket_id"]] = sid
        for cap in bucket["member_capability_refs"]:
            if cap in cap_sid and cap_sid[cap] != sid:
                base.fail("BOUND_GOLDEN_CAPABILITY_MULTI_SUBTOPIC", cap)
            cap_sid[cap] = sid
        for qid in bucket.get("core2_question_refs") or []:
            q_sid.setdefault(qid, sid)
    return bucket_sid, cap_sid, q_sid


def main() -> None:
    base.bucket_subtopics = multi_bucket_safe_subtopics
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--study-model", required=True)
    ap.add_argument("--core2-plan", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    summary = base.run_bound(Path(args.core1_plan), Path(args.study_model), Path(args.core2_plan), Path(args.out_dir))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
