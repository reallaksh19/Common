#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(HERE / script), *map(str, args)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


VALID_CHAIN = """# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|
| TEST-1 | test relay | EP-0001 | #1 | QUALIFICATION_REQUIRED | test | inspect live path |

# ENDPOINTS

## EP-0001

CHAIN_ID: TEST-1
LEG_ID: LEG-001
ENDPOINT_ID: EP-0001
PREVIOUS_ENDPOINT: NONE — chain start
ENDPOINT_REASON: CHAIN_START
CHECKPOINT_HEAD: abc123
MAIN_HEAD_OBSERVED: abc123
STATE: QUALIFICATION_REQUIRED

### Mission
Test mission.
### This leg completed
Initial grounding.
### Currently in progress
Qualification.
### Remaining work
One production trace.
### Exact next action
Inspect the live production path before mutation.
### Known / proven
Repository exists.
### Not proven
Production behavior.
### NOT_RUN
Runtime validation.
### Active hypothesis
Current mapping is correct.
### Falsifier
Independent trace disagrees.
### Protected invariants
Frozen benchmark.
### Do not redo
Initial source pin.
### Do not change
Benchmark expected value.
### Expected next-leg files / domains
src/example.py
### Inputs
input/example.json @ abc123
### Benchmarks
validation/example.json @ abc123
### Common / governing documents
AGENTS.md @ abc123
### Authoritative sources
source/example.md @ abc123
### Production paths
src/example.py
### Validation / test paths
tests/test_example.py
### Changed during this leg
NONE — chain start.
### Validation summary
NOT_RUN — pre-qualification.
### Open risks / questions
Current mapping not independently reproduced.
### Next-agent qualification
QUALIFICATION_BASIS_HEAD: abc123
QUESTION_SET_ID: QS-0001
QUESTION_SET_STATUS: CURRENT
#### Q1 — Production Trace
Trace src/example.py from input to output.
#### Q2 — Current Unresolved Problem / Failure Isolation
Isolate the current mapping and state a falsifier.
#### Q3 — Authority / Invariant
Identify the frozen benchmark authority and protected invariant.
#### Q4 — Independent Validation
Reproduce one value independently.
#### Q5 — Next Contribution / Minimal Patch
Name the smallest legitimate patch and protected files.
"""

VALID_ANSWER = """# Relay Qualification Answer
CHAIN_ID: TEST-1
ENDPOINT_ID: EP-0001
QUESTION_SET_ID: QS-0001
QUALIFICATION_BASIS_HEAD: abc123
CANDIDATE_ID: agent-b
LIVE_PR_HEAD_OBSERVED: abc123
LIVE_MAIN_HEAD_OBSERVED: abc123
RECONCILIATION: MATCH
## Q1 — Production Trace
Repository-grounded answer.
## Q2 — Current Unresolved Problem / Failure Isolation
Repository-grounded answer.
## Q3 — Authority / Invariant
Repository-grounded answer.
## Q4 — Independent Validation
Repository-grounded answer.
## Q5 — Next Contribution / Minimal Patch
Repository-grounded answer.
"""

VALID_VERDICT = """# Relay Qualification Verdict
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

SELF_VERDICT = VALID_VERDICT.replace("VERIFIER_ID: agent-c", "VERIFIER_ID: agent-b")


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
        chain = root / "agentchain.md"
        answer = root / "answer.md"
        verdict = root / "verdict.md"
        self_verdict = root / "self-verdict.md"
        bad_chain = root / "bad-agentchain.md"

        chain.write_text(VALID_CHAIN, encoding="utf-8")
        answer.write_text(VALID_ANSWER, encoding="utf-8")
        verdict.write_text(VALID_VERDICT, encoding="utf-8")
        self_verdict.write_text(SELF_VERDICT, encoding="utf-8")
        bad_chain.write_text(
            VALID_CHAIN.replace("validation/example.json @ abc123", ""),
            encoding="utf-8",
        )

        checks = [
            expect(run("validate_agentchain.py", chain), True, "valid agentchain"),
            expect(
                run("validate_qualification.py", answer, verdict),
                True,
                "valid independent qualification",
            ),
            expect(
                run("validate_qualification.py", answer, self_verdict),
                False,
                "self-verification rejected",
            ),
            expect(
                run("validate_agentchain.py", bad_chain),
                False,
                "empty benchmark inventory rejected",
            ),
            expect(
                run("check_relay.py", chain, answer, verdict),
                True,
                "composite relay gate",
            ),
        ]

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
