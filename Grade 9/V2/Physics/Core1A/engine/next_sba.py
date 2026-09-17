#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-v1.json"
STATE = ROOT / "registry" / "physics-core1a-motion-in-a-plane-build-state-v1.json"

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
state = json.loads(STATE.read_text(encoding="utf-8"))

buckets = registry["buckets"]
by_id = {b["bucket_id"]: b for b in buckets}
completed = set(state["completed_active_buckets"])

active_ids = [b["bucket_id"] for b in buckets if b["production_status"] == "ACTIVE"]
remaining = [bid for bid in active_ids if bid not in completed]
expected = remaining[0] if remaining else None
recorded = state["next_active_bucket"]

if recorded != expected:
    raise SystemExit(f"BUILD STATE DRIFT: recorded next_active_bucket={recorded!r}, derived={expected!r}")

if recorded is None:
    print("No remaining ACTIVE SBA buckets.")
else:
    bucket = by_id[recorded]
    print(f"NEXT_ACTIVE_BUCKET={recorded}")
    print(f"TITLE={bucket['learner_title']}")
    print(f"DIFFICULTY={bucket['intrinsic_difficulty']}")
    print("PRIMARY_CORE2=" + ",".join(bucket["core2_primary_questions"]))
    print("PREREQUISITES=" + ",".join(bucket["prerequisite_buckets"]))
    print("START_WITH=G0_INDEX_SYNC")
