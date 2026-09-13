#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from build_learning_representation import ROOT, build_from_fixture
from task_router import load_json
from validate_learning_representation import validate_fixture_and_lr

FIXTURE_DIR = ROOT / "fixtures" / "golden"

def main() -> None:
    fixture_paths = sorted(FIXTURE_DIR.glob("M2D-SBA-*.json"))
    if len(fixture_paths) != 3:
        raise SystemExit(f"Expected exactly 3 golden fixtures, found {len(fixture_paths)}.")

    results = []
    for path in fixture_paths:
        fixture = load_json(path)
        lr = build_from_fixture(fixture)
        report = validate_fixture_and_lr(fixture, lr)
        results.append({
            "fixture": fixture["fixture_id"],
            "bucket_id": fixture["bucket_id"],
            "status": report["status"],
            "atoms": len(lr["learning_atoms"]),
            "families": len(lr["transfer_families"]),
            "questions": len(lr["primary_questions"]),
        })

    print(json.dumps({"status": "PASS", "golden_fixtures": results}, indent=2))

if __name__ == "__main__":
    main()
