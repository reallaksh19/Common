#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_all_stress_tests import compile_all  # noqa: E402


def test_batch_compiles_governed_receipts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        manifest = compile_all(out)
        assert manifest["request_count"] >= 1
        assert (out / "manifest.json").exists()
        ids = {row["stress_test_id"] for row in manifest["receipts"]}
        governed = json.loads(
            (ROOT / "fixtures" / "stress-tests" / "relative-motion-grade9-cbse.request.v1.json").read_text(encoding="utf-8")
        )
        assert governed["stress_test_id"] in ids
        for row in manifest["receipts"]:
            assert row["final_verdict"] == "STRESS_TEST_PASS"
            assert row["receipt_digest"].startswith("sha256:")
            receipt_path = out / row["receipt_file"]
            assert receipt_path.exists()
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            assert receipt["stress_test_id"] == row["stress_test_id"]
            assert receipt["receipt_digest"] == row["receipt_digest"]


def test_batch_is_deterministic() -> None:
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        ma = compile_all(Path(a))
        mb = compile_all(Path(b))
        assert ma == mb
        assert (Path(a) / "manifest.json").read_bytes() == (Path(b) / "manifest.json").read_bytes()


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"Blueprint V10 stress batch tests: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
