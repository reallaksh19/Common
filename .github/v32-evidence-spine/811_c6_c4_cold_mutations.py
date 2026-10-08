#!/usr/bin/env python3
"""Local negative mutations of transferred two-file handover. No GitHub network."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import yaml

VERIFY = Path(__file__).with_name("811_c6_c4_cold_successor.py")


def required(ok, label):
    if not ok:
        raise RuntimeError(label)


def check(bundle):
    context = yaml.safe_load((bundle / "HANDOVER_CONTEXT.yaml").read_text(encoding="utf-8"))
    events = [json.loads(row) for row in
              (bundle / "EVENTS.jsonl").read_text(encoding="utf-8").splitlines() if row.strip()]
    target = next(i for i, e in enumerate(events) if
                  e.get("type") == "HANDOVER_PLANNED"
                  and "source_graph_pinned_location" in (e.get("details") or {}))
    cases = [
        ("CONTEXT", "COLD_CONTEXT_DIGEST_MISMATCH"),
        ("INPUT", "COLD_EVENT_SOURCE_DIGEST_MISMATCH"),
        ("PERMALINK", "COLD_SOURCE_LOCATION_LINK_MISMATCH"),
        ("REVISION", "COLD_SOURCE_REVISION_NOT_IMMUTABLE"),
    ]
    for name, expected in cases:
        with tempfile.TemporaryDirectory() as td:
            current = Path(td)
            ctx, ev = copy.deepcopy(context), copy.deepcopy(events)
            if name == "CONTEXT":
                ctx["successor_entry"]["mode"] = "UNAUTHORIZED_EXECUTION"
            elif name == "INPUT":
                ev[target]["details"]["source_bound_input_digest"] = "sha256:" + "0" * 64
            elif name == "PERMALINK":
                ev[target]["details"]["source_graph_pinned_location"]["permalink"] += "?wrong=1"
            elif name == "REVISION":
                ev[target]["details"]["source_graph_pinned_location"]["revision"] = "main"
            (current / "HANDOVER_CONTEXT.yaml").write_text(
                yaml.safe_dump(ctx, sort_keys=False), encoding="utf-8")
            (current / "EVENTS.jsonl").write_text(
                "".join(json.dumps(e, sort_keys=True) + "\n" for e in ev), encoding="utf-8")
            environment = os.environ.copy()
            environment.pop("GH_TOKEN", None)
            environment.pop("GITHUB_TOKEN", None)
            result = subprocess.run(
                [sys.executable, str(VERIFY), "--bundle", str(current), "--local-only"],
                capture_output=True, text=True, timeout=40, env=environment,
            )
            required(result.returncode != 0 and expected in result.stderr,
                     "COLD_MUTATION_UNDETECTED:" + name + ":" + result.stderr[-700:])
            print("COLD_TAMPER_" + name + "=REJECTED_BEFORE_NETWORK")
    print("COLD_FOUR_DURABLE_TAMPERS_FAIL_CLOSED=PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    args = parser.parse_args()
    check(Path(args.bundle).resolve())
