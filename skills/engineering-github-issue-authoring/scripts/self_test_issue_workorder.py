#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_issue_workorder.py"
SHA = "0123456789012345678901234567890123456789"

PROGRAM = f"""ISSUE_ROLE: PROGRAM_ROOT
PROGRAM_ID: PGM-DEMO
PROGRAMME_BASIS_REVISION: PB-0001
RELAY_PROTOCOL: V3.1_ONLY

# Owner outcome
Deliver one coherent programme result.

# Why now / governing witnesses
Current integration evidence shows a real gap.
Observed main: {SHA}

# Non-goals
No unrelated architecture expansion.

# Effective amendment index
CURRENT_BASIS_REVISION: PB-0001
No amendments yet.

# Canonical inputs
INPUT-001 | src/contracts.json | canonical contract | PRODUCTION

# Workstream registry
A | #1 | producer output | owns producer | consumer B

# Producer / consumer contracts
A produces exact contract X for B.

# Dependency contracts
B requires contract X. B may continue unrelated UI work independently.

# Programme exit criteria
EXIT-001 | integrated result works | A,B | PR/test evidence | OPEN

# Dedicated Relay Handover operational ledger
[Relay Handover] demo programme will be created as the current operational index.
"""

FOCUSED = f"""ISSUE_ROLE: PARALLEL_FOCUSED
PROGRAMME: github:owner/repo#100
WORKSTREAM_ID: F
RELAY_PROTOCOL: V3.1_ONLY
Observed main: {SHA}

# Outcome
Make the declared falsifier executable.

# Why now / concrete witness
A focused test currently fails.

# Owned responsibility
Focused mutation helper and assertions.

# Ownership boundary / conflict-avoidance fence
Do not change unrelated production architecture.

# Canonical inputs / source truth
The canonical declaration is the source truth.

# Preserve / invariants
Do not rewrite the declaration merely to make the test pass.

# Producer / consumer contract
Produces executable falsifier evidence. No downstream semantic contract change expected.

# Dependencies
NONE.

# Falsifier
If the proposed mutation does not produce the declared violation, the assumed path is wrong.

# Success oracle
Exact focused test passes with the declared violation.

# Implementation Plan
Agent-authored and revisable. Proposed approach, changed files, validation, uncertainties and next observable are recorded here.

# Expected handoff
Return exact head, evidence, proved/not-proved and limitations.

# Semantic escalation
Escalate only if canonical source truth or programme ownership changes.
"""

HANDOVER = f"""ISSUE_ROLE: RELAY_HANDOVER
PARENT_PROGRAMME: github:owner/repo#100
PROGRAMME_BASIS_REVISION: PB-0001
RELAY_PROTOCOL: V3.1_ONLY
Observed main: {SHA}

# Non-authority rule
This ledger is an index, not production authority.

# Programme basis
Parent #100 / PB-0001.

# Workstreams
F | #232 | plan present | expected falsifier result.

# Dependency ledger
No real dependency currently.

# Nonterminal PRs
Carry all draft/open PRs until terminal.

# Pending items
Focused test evidence.

# Known issues
None.

# Negative knowledge / do-not-reopen
Do not change canonical declaration merely to silence a test.

# Recent handoffs
None yet.

# Owner decisions needed
NONE.

# Next coordinator action
Observe F result and route only if programme-significant.

# Next useful observation
Watch for PR/test evidence.
"""


def run(text):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "issue.md"
        p.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True, text=True)


def expect(name, text, expected):
    r = run(text)
    ok = r.returncode == expected
    print(("PASS" if ok else "FAIL") + ": " + name)
    if not ok:
        print(r.stdout + r.stderr)
    return ok


def main():
    ok = True
    ok &= expect("programme specification", PROGRAM, 0)
    ok &= expect("parallel focused child", FOCUSED, 0)
    ok &= expect("relay handover ledger", HANDOVER, 0)
    ok &= expect("focused child without parent rejected", FOCUSED.replace("PROGRAMME: github:owner/repo#100\n", ""), 1)
    ok &= expect("programme without handover reference rejected", PROGRAM.replace("# Dedicated Relay Handover operational ledger\n[Relay Handover] demo programme will be created as the current operational index.\n", ""), 1)
    ok &= expect("legacy protocol path rejected", FOCUSED + "\nengineering-pr-delivery-v2.5\n", 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
