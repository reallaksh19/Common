#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_handover_snapshot.py"

ACTIVE = """CHAIN_STATE_VERSION: 3
CHAIN_ID: T
MISSION: test
ACTIVE_ENDPOINT: EP-1
ACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP-1.md
PR: 1
BRANCH: b
HEAD: h
STATE: ACTIVE
ENGINEERING_STATE: READY
CUSTODY_STATE: HELD
QUALIFICATION_STATE: NOT_REQUIRED
WRITE_AUTHORITY: WRITE_ALLOWED
AUTO_STATE: NOT_APPLICABLE
MERGE_AUTHORITY: OWNER_ONLY
AUTHORITY_DOMAIN: TEST
ACTIVE_CUSTODIAN: test
CUSTODY_EPOCH: 1
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
ROADMAPS: NONE — test
ROADMAP_REVIEW_STATUS: NOT_APPLICABLE
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_READY: TRUE
"""

CARD = """### Active handover snapshot
Repo: R
Task: T
Chain: T
Endpoint: EP-1
PR: 1
PR status: DRAFT
Branch / PR head / main: b / h / m
Merge authority: OWNER_ONLY
Engineering / custody / qualification / write state: READY / HELD / NOT_REQUIRED / WRITE_ALLOWED
AUTO: NOT_APPLICABLE
Protocol basis / status: x / CURRENT
Roadmap: NONE
Inputs: I
Benchmarks: B
Governing docs / authoritative sources: S
Current blocker: NONE
Leg diagnosis: READY
Exact next action: execute bounded test
"""

FULL_Q = """### Active qualification questions
Q1: Trace the actual production case through source, canonical model, solver and result boundaries with exact identifiers and values.
Q2: Using N1=(0,0), N2=(40,0), N3=(0,30), compute the Jacobian determinant and identify the first falsifying intermediate.
Q3: Prove the authority boundary with exact repository evidence, protected invariant and one observation that would falsify the diagnosis.
Q4: For a=10 mm, R=100 mm and sigma=50 MPa, derive an independent oracle without using production output as expected truth.
Q5: Specify the smallest legal patch, exact before/after evidence, regression, negative test, rollback and NO-PATCH condition.
"""


def write(root, card=CARD, questions=FULL_Q):
    d = root / "agents/chains/T/endpoints"; d.mkdir(parents=True)
    (d / "EP-1.md").write_text("HANDOVER_PROTOCOL_VERSION: 2\n" + card + questions, encoding="utf-8")
    (d.parent / "ACTIVE.md").write_text(ACTIVE, encoding="utf-8")


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, result, rc):
    ok = result.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok:
        print(result.stdout, result.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write(r); ok &= expect("state card + full questions", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write(r, card=CARD + "Q1: compressed inside card\n"); ok &= expect("questions inside state-card limit rejected", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); bad = """### Active qualification questions
Q1: Trace solver.
Q2: Calculate Jacobian.
Q3: Prove authority.
Q4: Reconstruct oracle.
Q5: Safe patch.
"""; write(r, questions=bad); ok &= expect("topic-label visible questions rejected", run(r), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
