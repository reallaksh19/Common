#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_qualification_questions.py"


def strong_pack(q5_prefix="Repository anchors:"):
    return f"""### Takeover qualification pack
PURPOSE: QUALIFICATION_ONLY
NOT_AN_IMPLEMENTATION_TASK: TRUE
QUALIFICATION_BASIS_HEAD: abc
QUESTION_SET_ID: QS-T-1
QUESTION_SET_STATUS: CURRENT
QUESTION_SET_AUTHOR: prior-agent
#### Q1 — Production Trace
Repository anchors: src/a.js; tests/a.test.js
Production object/case: element E17 / load case LC1 / result hash H1
Required technical work: Extract exact IDs/data and trace the same object through source, compiled model, solver and result publication.
Required numerical/technical evidence: Give the retained coordinates/order and the value/hash observed at each boundary.
First authority/ownership boundaries: source authority, solver model, result consumer.
Fail if: answer is generic or invents an ID.
#### Q2 — Current Unresolved Problem / Failure Isolation
Repository anchors: src/element.js; tests/element.test.js
Calculation/reconstruction: Compute the Jacobian or equivalent exact transformation for the pinned case by hand.
Required numerical/technical evidence: Show inputs, arithmetic and at least one predicted numerical intermediate.
Predicted intermediate values: J11/J12/J21/J22 and detJ or equivalent exact fields.
First wrong boundary: identify one exact function/value.
Falsifier: state the observation that disproves the diagnosis.
Fail if: no arithmetic/reconstruction or no first wrong boundary.
#### Q3 — Authority / Invariant
Repository anchors: docs/source.md; src/authority.js
Required technical work: Trace ownership of the governing input and distinguish derived from authoritative data.
Authority/source trace: source document -> canonical field -> consumer.
Protected invariant: benchmark/oracle and source authority remain independent.
First wrong boundary: first owner that could legally change the value.
Falsifier: exact source/value that disproves the claimed owner.
Invalid shortcut: replacing the oracle with production output.
Fail if: authority is inferred from convenience or test location.
#### Q4 — Independent Validation
Repository anchors: benchmarks/b.json; src/solver.js
Required technical work: Independently derive the expected result and compare with the implementation result.
Independent oracle: closed-form/hand calculation independent of production output.
Required numerical/technical evidence: equations, inputs, expected result and delta.
Units/sign/tolerance: state units, coordinate/sign convention and justified tolerance.
Falsifier: independent result outside tolerance or wrong sign/units.
Fail if: expected value is copied from production output.
#### Q5 — Next Contribution / Minimal Patch
{q5_prefix} src/first-wrong.js; tests/regression.test.js
Required technical work: Explain the smallest patch that would be authorized only after the first wrong boundary is proven.
Safe patch boundary: one named function plus focused regression; no source/oracle changes.
Expected before/after evidence: exact failing value -> independently expected value.
Protected unchanged domains: roadmap, source authority, benchmark oracle, unrelated solver paths.
Validation required: focused regression then unchanged public route.
Negative test: falsifier case must still fail closed.
Rollback/falsifier boundary: revert/supersede if predicted boundary is not the first wrong one.
No-patch condition: environment/materialization/source-data error rather than production defect.
Fail if: candidate proposes a shotgun change or patches before evidence.
"""


def make(root, pack):
    c = root / "agents/chains/T"; (c / "endpoints").mkdir(parents=True)
    (c / "ACTIVE.md").write_text("CHAIN_STATE_VERSION: 3\nCHAIN_ID: T\nACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP-0001.md\n")
    (c / "endpoints/EP-0001.md").write_text("STATE: ACTIVE\n" + pack)


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, r, rc):
    ok = r.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok: print(r.stdout, r.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, strong_pack()); ok &= expect("strong expert pack", run(root), 0)
    weak = """### Takeover qualification pack
PURPOSE: QUALIFICATION_ONLY
NOT_AN_IMPLEMENTATION_TASK: TRUE
QUALIFICATION_BASIS_HEAD: a
QUESTION_SET_ID: q
QUESTION_SET_AUTHOR: a
""" + "\n".join([f"#### Q{i} — {t}\nRepository anchors: repo\nFail if: wrong" for i,t in [(1,'Production Trace'),(2,'Current Unresolved Problem / Failure Isolation'),(3,'Authority / Invariant'),(4,'Independent Validation'),(5,'Next Contribution / Minimal Patch')]])
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, weak); ok &= expect("generic shallow pack rejected", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, strong_pack("Implement the fix now.\nRepository anchors:")); ok &= expect("Q5 task imperative rejected", run(root), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
