#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_seven_core_stress_test import compile_stress_test  # noqa: E402

REQUEST_DIR = ROOT / "fixtures" / "stress-tests"
REQUEST_SUFFIX = ".request.v1.json"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compile_all(out_dir: Path) -> dict[str, Any]:
    request_paths = sorted(REQUEST_DIR.glob(f"*{REQUEST_SUFFIX}"))
    if not request_paths:
        raise AssertionError("STRESS_BATCH_NO_GOVERNED_REQUESTS")

    request_schema = load_json(ROOT / "contracts" / "seven-core-stress-test-request.schema.json")
    receipt_schema = load_json(ROOT / "contracts" / "seven-core-stress-test-receipt.schema.json")
    request_validator = Draft202012Validator(request_schema)
    receipt_validator = Draft202012Validator(receipt_schema)

    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    failed: list[str] = []

    for request_path in request_paths:
        request = load_json(request_path)
        request_validator.validate(request)
        if "final_verdict" in request:
            raise AssertionError("STRESS_BATCH_REQUEST_SELF_ASSERTS_VERDICT:" + request_path.name)

        stress_test_id = str(request["stress_test_id"])
        if stress_test_id in seen_ids:
            raise AssertionError("STRESS_BATCH_DUPLICATE_ID:" + stress_test_id)
        seen_ids.add(stress_test_id)

        receipt = compile_stress_test(request)
        receipt_validator.validate(receipt)
        if receipt["stress_test_id"] != stress_test_id:
            raise AssertionError("STRESS_BATCH_ID_DRIFT:" + stress_test_id)

        stem = request_path.name[: -len(REQUEST_SUFFIX)]
        receipt_name = f"{stem}.receipt.v1.json"
        receipt_path = out_dir / receipt_name
        receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        row = {
            "stress_test_id": stress_test_id,
            "request_ref": str(request_path.relative_to(ROOT)),
            "receipt_file": receipt_name,
            "final_verdict": receipt["final_verdict"],
            "receipt_digest": receipt["receipt_digest"],
        }
        rows.append(row)
        if receipt["final_verdict"] != "STRESS_TEST_PASS":
            failed.append(stress_test_id)

    manifest = {
        "schema_version": "1.0.0",
        "compiler": "compile_all_stress_tests.py",
        "request_count": len(rows),
        "receipts": rows,
    }
    manifest["manifest_digest"] = digest(manifest)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if failed:
        raise AssertionError("STRESS_BATCH_ARCHITECTURE_FAILURE:" + ",".join(sorted(failed)))
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile all governed Physics V10 seven-core stress-test requests.")
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    manifest = compile_all(args.out_dir)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
