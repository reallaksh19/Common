#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_qualification_profile.py"


def pack(profile="FEA", weak=False):
    def q(n, title, challenge, calc="reconstruct actual values from repository data"):
        body = [
            f"#### Q{n} — {title}",
            "Repository anchors: src/solver.js; tests/case.test.js",
            f"Domain challenge: {challenge}",
            "Exact repository data required: actual element E17, nodes N1/N2, load LC1, mesh hash H1 and solver/result values.",
        ]
        if n in {2,4}:
            body.append(f"Calculation/reconstruction: {calc}")
        if n == 1:
            body += ["Production object/case: retained element E17 and LC1", "Required technical work: trace mesh node element stiffness recovery transform result.", "Required numerical/technical evidence: exact node coordinates, DOF ordering, reaction and hash.", "First authority/ownership boundaries: mesh adapter solver recovery presentation."]
        if n == 2:
            body += ["Required numerical/technical evidence: compute Jacobian det(J) and predicted reaction.", "Predicted intermediate values: J11 J12 J21 J22 detJ.", "First wrong boundary: element mapping function.", "Falsifier: solver node order matches hand order but detJ still differs."]
        if n == 3:
            body += ["Required technical work: prove source and solver ownership.", "Authority/source trace: source -> canonical -> solver.", "Protected invariant: oracle independent.", "First wrong boundary: first owner changing geometry.", "Falsifier: exact source coordinate disproves ownership.", "Invalid shortcut: production output as oracle."]
        if n == 4:
            body += ["Required technical work: derive independent beam/element result.", "Independent oracle: closed-form equilibrium independent of production.", "Required numerical/technical evidence: equations inputs result delta.", "Units/sign/tolerance: N mm Pa and explicit sign convention.", "Falsifier: independent result outside tolerance."]
        if n == 5:
            body += ["Required technical work: identify smallest function-level correction.", "Safe patch boundary: one mapping/recovery function and focused regression.", "Expected before/after evidence: wrong detJ -> hand-derived detJ.", "Protected unchanged domains: source oracle solver formulation unrelated paths.", "Validation required: focused then aggregate.", "Negative test: reversed ordering remains rejected.", "Rollback/falsifier boundary: revert if first wrong boundary differs.", "No-patch condition: benchmark/source/environment error."]
        body.append("Fail if: answer is generic or lacks exact repository evidence and arithmetic.")
        return "\n".join(body)
    challenge1 = "Explain the solver." if weak else "Trace actual element E17 through mesh, stiffness assembly, recovery and presentation and prove the same identity/hash."
    challenge2 = "Describe the benchmark." if weak else "Calculate the T6/element Jacobian or equivalent stiffness/equilibrium quantity from actual node data and isolate the first wrong boundary."
    challenge3 = "List the claims." if weak else "Trace geometry and solver authority and falsify one incorrect ownership hypothesis using an exact repository value."
    challenge4 = "Re-read the test." if weak else "Reconstruct an independent equilibrium/beam oracle and compare its reaction/recovery value to production."
    challenge5 = "What would you change?" if weak else "Prove the minimal element mapping/recovery patch boundary and the exact NO-PATCH condition."
    return "\n".join([
        "### Takeover qualification pack",
        "PURPOSE: QUALIFICATION_ONLY",
        "NOT_AN_IMPLEMENTATION_TASK: TRUE",
        "QUALIFICATION_PROTOCOL_VERSION: 3",
        f"QUALIFICATION_PROFILE: {profile}",
        "QUALIFICATION_BASIS_HEAD: abc",
        "QUESTION_SET_ID: QS-T-1",
        "QUESTION_SET_STATUS: CURRENT",
        "QUESTION_SET_AUTHOR: prior-agent",
        "QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER",
        q(1, "Production Trace", challenge1),
        q(2, "Current Unresolved Problem / Failure Isolation", challenge2),
        q(3, "Authority / Invariant", challenge3),
        q(4, "Independent Validation", challenge4),
        q(5, "Next Contribution / Minimal Patch", challenge5),
    ])


def make(root, content):
    c = root / "agents/chains/T"; (c / "endpoints").mkdir(parents=True)
    (c / "ACTIVE.md").write_text("CHAIN_STATE_VERSION: 3\nCHAIN_ID: T\nACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP-0001.md\n")
    (c / "endpoints/EP-0001.md").write_text("STATE: ACTIVE\nQUALIFICATION_PROFILE: FEA\n" + content)


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, result, rc):
    ok = result.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok: print(result.stdout, result.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, pack()); ok &= expect("FEA profile strong pack", run(root), 0)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, pack(weak=True)); ok &= expect("weak descriptive FEA pack rejected", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); make(root, pack(profile="UNKNOWN")); ok &= expect("unknown profile rejected", run(root), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
