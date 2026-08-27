#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent

SUITES = [
    "self_test_relay_structure.py",
    "self_test_candidate_answer.py",
    "self_test_qualification_policy.py",
    "self_test_verdict_uniqueness.py",
]


def main():
    failed = []
    for suite in SUITES:
        print(f"=== {suite} ===")
        result = subprocess.run([sys.executable, str(HERE / suite)])
        if result.returncode != 0:
            failed.append(suite)

    if failed:
        print("FAIL: relay self-test suites:", ", ".join(failed))
        return 1

    print(f"PASS: all {len(SUITES)} relay self-test suites")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
