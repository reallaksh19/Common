#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent

VALID = """# Relay Qualification Answer
CHAIN_ID: TEST-1
ENDPOINT_ID: EP-0001
QUESTION_SET_ID: QS-0001
QUALIFICATION_BASIS_HEAD: abc123
CANDIDATE_ID: agent-b
LIVE_PR_HEAD_OBSERVED: def456
LIVE_MAIN_HEAD_OBSERVED: ghi789
RECONCILIATION: METADATA_DRIFT
QUALIFICATION_STATUS: DEFERRED_VERIFICATION
TAKEOVER_AUTHORITY: READ_ONLY

## Q1 — Production Trace
Concrete repository trace with file and function anchors.
## Q2 — Current Unresolved Problem / Failure Isolation
Prediction, isolating experiment, falsifier, and first wrong boundary.
## Q3 — Authority / Invariant
Authoritative source, protected invariant, and invalid shortcut.
## Q4 — Independent Validation
Independent evidence with limitations and provenance.
## Q5 — Next Contribution / Minimal Patch
Exact patch boundary, protected files, validation, and rollback trigger.
"""

SELF_AUTH = VALID.replace("TAKEOVER_AUTHORITY: READ_ONLY", "TAKEOVER_AUTHORITY: WRITE_ALLOWED")
SELF_SCORE = VALID + "\nQ1 20/20\nQ2 20/20\nQ3 20/20\nQ4 20/20\nQ5 20/20\nTOTAL 100/100\n"
MISSING_Q4 = VALID.replace(
    "## Q4 — Independent Validation\nIndependent evidence with limitations and provenance.\n",
    "",
)


def run(path):
    return subprocess.run(
        [sys.executable, str(HERE / "validate_candidate_answer.py"), str(path)],
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
        valid = root / "valid.md"
        self_auth = root / "self-auth.md"
        self_score = root / "self-score.md"
        missing_q4 = root / "missing-q4.md"
        valid.write_text(VALID, encoding="utf-8")
        self_auth.write_text(SELF_AUTH, encoding="utf-8")
        self_score.write_text(SELF_SCORE, encoding="utf-8")
        missing_q4.write_text(MISSING_Q4, encoding="utf-8")

        checks = [
            expect(run(valid), True, "valid deferred/read-only candidate answer"),
            expect(run(self_auth), False, "candidate self-authorization rejected"),
            expect(run(self_score), False, "candidate self-scoring rejected"),
            expect(run(missing_q4), False, "missing Q4 response rejected"),
        ]

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
