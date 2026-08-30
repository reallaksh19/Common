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
    "self_test_handover_snapshot.py",
    "self_test_handover_readiness.py",
    "self_test_qualification_questions.py",
    "self_test_qualification_first_verdict.py",
    "self_test_question_set_admission.py",
    "self_test_post_basis_drift.py",
    "self_test_repository_overlay.py",
    "self_test_leg_adoption.py",
    "self_test_qualification_profiles.py",
    "self_test_engineering_question_payload.py",
    "self_test_owner_qualification_baseline.py",
    "self_test_work_item_exclusivity.py",
    "self_test_prework_history.py",
    "self_test_material_leg_history.py",
]
SUITE_TIMEOUT_SECONDS = 20


def main():
    failed = []
    for suite in SUITES:
        print(f"=== {suite} ===", flush=True)
        try:
            r = subprocess.run(
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
        print(r.stdout, end="")
        if r.returncode != 0:
            failed.append(suite)
    if failed:
        print("FAIL: relay self-test suites:", ", ".join(failed))
        return 1
    print(f"PASS: all {len(SUITES)} relay self-test suites")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
