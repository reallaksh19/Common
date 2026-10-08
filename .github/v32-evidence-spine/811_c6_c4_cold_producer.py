#!/usr/bin/env python3
"""Generate a native GitHub source-bound handover, export two durable files.

The process that generates them exits BEFORE the cold successor process starts.
No graph SHA, repo, source leaf or secret is included in successor arguments.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
NATIVE = Path(__file__).with_name("811_c6_c3_native_transaction.py")


def run(out):
    spec = importlib.util.spec_from_file_location("v32_c6_real_native", NATIVE)
    if not spec or not spec.loader:
        raise RuntimeError("COLD_PRODUCER_NATIVE_SOURCE_ABSENT")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise RuntimeError("COLD_PRODUCER_OUTPUT_NOT_EMPTY")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        base, target = native.new_fixture(root)
        res = native.command(root, base, target, "TX-C6-C4-COLD-001", "EVT-C6-C4-COLD-001")
        if res.returncode != 0 or "COMMITTED" not in res.stdout:
            raise RuntimeError("COLD_PRODUCER_NATIVE_TRANSACTION_FAILED: " + res.stderr[-1400:])
        for source, name in (
            (root / "relay/GENERATED/HANDOVER_CONTEXT.yaml", "HANDOVER_CONTEXT.yaml"),
            (root / "relay/EVENTS.jsonl", "EVENTS.jsonl"),
        ):
            if not source.is_file():
                raise RuntimeError("COLD_PRODUCER_DURABLE_OUTPUT_MISSING:" + name)
            shutil.copyfile(source, out / name)
    if {p.name for p in out.iterdir()} != {"HANDOVER_CONTEXT.yaml", "EVENTS.jsonl"}:
        raise RuntimeError("COLD_PRODUCER_UNEXPECTED_BUNDLE_FILES")
    print("COLD_PRODUCER_FRESH_PROCESS_EXIT=PASS_TWO_FILES_ONLY")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    run(Path(args.out).resolve())
