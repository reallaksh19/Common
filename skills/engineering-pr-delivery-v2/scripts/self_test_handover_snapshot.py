#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_handover_snapshot.py"


def make(root, *, snapshot_extra="", custody="HELD", qual="NOT_REQUIRED", write="WRITE_ALLOWED", auto="NOT_APPLICABLE"):
    c = root / "agents/chains/T"
    (c / "endpoints").mkdir(parents=True)
    snap = f"""Repo: R
Task: T
Chain: T
Endpoint: EP-0001
PR: 1
PR status: open
Branch / PR head / main: b / h / m
Merge authority: OWNER_ONLY
Engineering / custody / qualification / write state: READY / {custody} / {qual} / {write}
Roadmap: NONE
Inputs: input
Benchmarks: bench
Governing docs / authoritative sources: docs
Current blocker: NONE
Exact next action: inspect next bounded implementation unit
Q1: Reconstruct actual production object and trace exact boundaries.
Q2: Calculate or reconstruct the current numerical/technical invariant and predict intermediates.
Q3: Prove authority and give the decisive falsifier.
Q4: Independently derive the expected result with units/tolerance.
Q5: Define the smallest safe patch and the NO-PATCH condition.
{snapshot_extra}"""
    ep = f"""# EP-0001
CHAIN_ID: T
ENDPOINT_ID: EP-0001
HANDOVER_READY: TRUE
STATE: ACTIVE
### Handover snapshot
{snap}
"""
    (c / "endpoints/EP-0001.md").write_text(ep)
    active = f"""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
MISSION: test
ACTIVE_ENDPOINT: EP-0001
ACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP-0001.md
PR: 1
BRANCH: b
HEAD: h
STATE: ACTIVE
ENGINEERING_STATE: READY
CUSTODY_STATE: {custody}
QUALIFICATION_STATE: {qual}
WRITE_AUTHORITY: {write}
AUTO_STATE: {auto}
MERGE_AUTHORITY: OWNER_ONLY
AUTHORITY_DOMAIN: test
ACTIVE_CUSTODIAN: a
CUSTODY_EPOCH: 1
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
ROADMAPS: NONE — test
ROADMAP_REVIEW_STATUS: NOT_APPLICABLE
HANDOVER_READY: TRUE
"""
    (c / "ACTIVE.md").write_text(active)


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, r, rc):
    ok = r.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok:
        print(r.stdout, r.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root); ok &= expect("valid snapshot/state", run(root), 0)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, snapshot_extra=" ".join(["word"] * 280)); ok &= expect("300-word limit", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, custody="TAKEOVER_REQUIRED", qual="PENDING", write="WRITE_ALLOWED", auto="PAUSED"); ok &= expect("pending takeover cannot write", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, custody="QUALIFIED_PENDING_RECONCILIATION", qual="PASS", write="WRITE_ALLOWED"); ok &= expect("PASS still read-only before reconciliation", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, custody="TAKEOVER_REQUIRED", qual="PENDING", write="READ_ONLY", auto="RUNNING"); ok &= expect("agent loss pauses AUTO", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, custody="HELD", qual="REQUALIFICATION_REQUIRED", write="WRITE_ALLOWED"); ok &= expect("requalification-required cannot write", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, custody="HELD", qual="REQUALIFICATION_REQUIRED", write="READ_ONLY"); ok &= expect("requalification-required read-only is valid", run(root), 0)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
