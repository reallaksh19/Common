#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent

ANSWER = """# Relay Qualification Answer
CHAIN_ID: TEST-1
ENDPOINT_ID: EP-0001
QUESTION_SET_ID: QS-0001
QUALIFICATION_BASIS_HEAD: abc123
CANDIDATE_ID: agent-b
LIVE_PR_HEAD_OBSERVED: def456
LIVE_MAIN_HEAD_OBSERVED: ghi789
RECONCILIATION: MATCH
QUALIFICATION_STATUS: DEFERRED_VERIFICATION
TAKEOVER_AUTHORITY: READ_ONLY
## Q1 — Production Trace
Repository trace.
## Q2 — Current Unresolved Problem / Failure Isolation
Failure isolation.
## Q3 — Authority / Invariant
Authority trace.
## Q4 — Independent Validation
Independent validation.
## Q5 — Next Contribution / Minimal Patch
Minimal patch.
"""

VERDICT = """# Relay Qualification Verdict
CHAIN_ID: TEST-1
ENDPOINT_ID: EP-0001
QUESTION_SET_ID: QS-0001
QUALIFICATION_BASIS_HEAD: abc123
CANDIDATE_ID: agent-b
VERIFIER_ID: agent-c
VERDICT_BASIS_HEAD: abc123
Q1 19/20
Q2 19/20
Q3 19/20
Q4 18/20
Q5 19/20
TOTAL 94/100
MINIMUM_QUESTION 18/20
AUTOMATIC_FAILURE_REASON: NONE
VERDICT: PASS_WRITE_ALLOWED
"""

DUPLICATE_VERDICT = VERDICT + "VERDICT: FAIL_READ_ONLY\n"
DUPLICATE_SCORE = VERDICT + "Q1 1/20\n"
DUPLICATE_VERIFIER = VERDICT.replace(
    "VERIFIER_ID: agent-c", "VERIFIER_ID: agent-c\nVERIFIER_ID: agent-d"
)


def run(answer, verdict):
    return subprocess.run(
        [
            sys.executable,
            str(HERE / "validate_qualification.py"),
            str(answer),
            str(verdict),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def expect(result, should_pass, label):
    ok = result.returncode == 0
    if ok != should_pass:
        print(f"FAIL SELF-TEST: {label}")
        print(result.stdout)
        return False
    print(f"PASS SELF-TEST: {label}")
    return True


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        answer = root / "answer.md"
        valid = root / "valid.md"
        duplicate_verdict = root / "duplicate-verdict.md"
        duplicate_score = root / "duplicate-score.md"
        duplicate_verifier = root / "duplicate-verifier.md"

        answer.write_text(ANSWER, encoding="utf-8")
        valid.write_text(VERDICT, encoding="utf-8")
        duplicate_verdict.write_text(DUPLICATE_VERDICT, encoding="utf-8")
        duplicate_score.write_text(DUPLICATE_SCORE, encoding="utf-8")
        duplicate_verifier.write_text(DUPLICATE_VERIFIER, encoding="utf-8")

        checks = [
            expect(run(answer, valid), True, "valid unique-field verdict"),
            expect(run(answer, duplicate_verdict), False, "duplicate VERDICT rejected"),
            expect(run(answer, duplicate_score), False, "duplicate Q1 score rejected"),
            expect(run(answer, duplicate_verifier), False, "duplicate VERIFIER_ID rejected"),
        ]

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
