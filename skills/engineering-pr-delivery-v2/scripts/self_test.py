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
    "self_test_policy_controls.py",
    "self_test_chain_concurrency.py",
    "self_test_roadmap_governance.py",
]

SUITE_TIMEOUT_SECONDS = 20


def main():
    failed = []
    for suite in SUITES:
        print(f"=== {suite} ===", flush=True)
        try:
            result = subprocess.run(
                [sys.executable, str(HERE / suite)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=SUITE_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as exc:
            if exc.stdout:
                print(exc.stdout, end="")
            print(f"FAIL: {suite} exceeded {SUITE_TIMEOUT_SECONDS}s")
            failed.append(suite)
            continue

        print(result.stdout, end="")
        if result.returncode != 0:
            failed.append(suite)

    if failed:
        print("FAIL: relay self-test suites:", ", ".join(failed))
        return 1

    print(f"PASS: all {len(SUITES)} relay self-test suites")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
