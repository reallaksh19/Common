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

VALID = """# Relay Qualification Verdict
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

SELF_VERIFIED = VALID.replace("VERIFIER_ID: agent-c", "VERIFIER_ID: agent-b")
BELOW_MINIMUM = (
    VALID.replace("Q4 18/20", "Q4 16/20")
    .replace("TOTAL 94/100", "TOTAL 92/100")
    .replace("MINIMUM_QUESTION 18/20", "MINIMUM_QUESTION 16/20")
)
UNJUSTIFIED_FAIL = VALID.replace("VERDICT: PASS_WRITE_ALLOWED", "VERDICT: FAIL_READ_ONLY")


def run(answer, verdict):
    return subprocess.run(
        [sys.executable, str(HERE / "validate_qualification.py"), str(answer), str(verdict)],
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
        answer.write_text(ANSWER, encoding="utf-8")
        cases = [
            ("valid.md", VALID, True, "valid independent qualification"),
            ("self.md", SELF_VERIFIED, False, "self-verification rejected"),
            ("below.md", BELOW_MINIMUM, False, "PASS_WRITE_ALLOWED below per-question minimum rejected"),
            ("fail.md", UNJUSTIFIED_FAIL, False, "numeric pass cannot fail with AUTOMATIC_FAILURE_REASON=NONE"),
        ]
        checks = []
        for filename, text, expected, label in cases:
            verdict = root / filename
            verdict.write_text(text, encoding="utf-8")
            checks.append(expect(run(answer, verdict), expected, label))

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
