#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_owner_qualification_baseline.py"

MANIFEST = {
    "version": 1,
    "baselineId": "QB-ISSUE-1535-A",
    "source": "github:reallaksh19/Advanced_Analysis#1535/Appendix-A",
    "sourceAuthority": "OWNER",
    "activeQuestionSetId": "QS-1535-TEST",
    "questions": [
        {
            "baselineQuestion": "Q1",
            "coveredBy": ["Q1"],
            "requiredLiterals": ["N1=(0,0)", "N2=(40,0)", "N3=(0,30)", "N4=(22,2)", "N5=(20,15)", "N6=(0,15)", "1/3", "Hammer"],
            "requiredConcepts": ["Jacobian", "det J", "centroid", "negative"],
            "requiredObligations": ["compute", "quantify"]
        },
        {
            "baselineQuestion": "Q2",
            "coveredBy": ["Q2"],
            "requiredLiterals": ["N1 = 1/4", "N5 = 1/2", "3x3"],
            "requiredConcepts": ["partition", "constant strain", "Gauss", "polynomial degree"],
            "requiredObligations": ["verify", "derive"]
        },
        {
            "baselineQuestion": "Q3",
            "coveredBy": ["Q3"],
            "requiredLiterals": ["a=10", "R=100", "50 MPa", "theta=0", "theta=90"],
            "requiredConcepts": ["Kirsch", "traction", "1/r^2", "1/r^4", "error"],
            "requiredObligations": ["derive", "estimate"]
        },
        {
            "baselineQuestion": "Q4",
            "coveredBy": ["Q4"],
            "requiredLiterals": ["L=200", "h=20", "b=10", "E=200000", "nu=0.3", "P=1000"],
            "requiredConcepts": ["Euler-Bernoulli", "T3", "T6", "5%", "strain"],
            "requiredObligations": ["evaluate", "justify"]
        }
    ]
}

STRONG = {
    "Q1": "Use N1=(0,0), N2=(40,0), N3=(0,30), N4=(22,2), N5=(20,15), N6=(0,15) mm. Compute the T6 Jacobian and det J at the centroid 1/3 and one Hammer point; quantify the change and prove the negative det J rejection boundary.",
    "Q2": "Using N1 = 1/4(1-xi)(1-eta)(-xi-eta-1) and N5 = 1/2(1-xi^2)(1-eta), verify partition of unity and the constant strain patch at full 3x3 Gauss integration; derive the minimum order from polynomial degree.",
    "Q3": "For the Kirsch case a=10 mm, R=100 mm, sigma=50 MPa, derive boundary traction at theta=0 and theta=90, then estimate truncation error from the 1/r^2 and 1/r^4 terms.",
    "Q4": "For L=200 mm, h=20 mm, b=10 mm, E=200000 MPa, nu=0.3, P=1000 N, evaluate Euler-Bernoulli tip deflection; justify T3 versus T6 strain completeness and the mesh needed for 5% error.",
    "Q5": "Define the smallest safe patch, regression, rollback and NO-PATCH condition."
}

DEGRADED = {
    "Q1": "Trace LAFEA.3 and reconstruct distorted T6 Jacobians.",
    "Q2": "Explain Q8 patch consistency.",
    "Q3": "Trace hole topology and Kirsch references.",
    "Q4": "Compare T3 and T6 convergence.",
    "Q5": "Prove the safe next patch."
}


def write_case(root, questions, qsid="QS-1535-TEST", source=True):
    chain = root / "agents/chains/T"
    (chain / "endpoints").mkdir(parents=True)
    manifest_rel = "agents/chains/T/qualification-baselines/QB-1535.json"
    if source:
        (chain / "qualification-baselines").mkdir()
        (root / manifest_rel).write_text(json.dumps(MANIFEST), encoding="utf-8")
        source_line = "OWNER_QUALIFICATION_BASELINE_SOURCE: github:reallaksh19/Advanced_Analysis#1535/Appendix-A"
        manifest_line = f"OWNER_QUALIFICATION_BASELINE_MANIFEST: {manifest_rel}"
        status_line = "OWNER_QUALIFICATION_BASELINE_STATUS: SATISFIED"
    else:
        source_line = "OWNER_QUALIFICATION_BASELINE_SOURCE: NONE"
        manifest_line = "OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE"
        status_line = "OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE"
    qtext = "\n".join(f"Q{i}: {questions[f'Q{i}']}" for i in range(1, 6))
    ep = f"""# EP
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
{source_line}
{manifest_line}
{status_line}
### Active qualification questions
{qtext}
### Takeover qualification pack
QUESTION_SET_ID: {qsid}
"""
    (chain / "endpoints/EP-1.md").write_text(ep, encoding="utf-8")
    (chain / "ACTIVE.md").write_text("""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
STATE: ACTIVE
ACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP-1.md
""", encoding="utf-8")


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
        r = Path(td); write_case(r, STRONG); ok &= expect("1535 numerical baseline preserved", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write_case(r, DEGRADED); ok &= expect("1535 topic-label downgrade rejected", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write_case(r, STRONG, source=False); ok &= expect("no Owner baseline is explicit not-applicable", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write_case(r, STRONG, qsid="QS-WRONG"); ok &= expect("manifest question-set mismatch rejected", run(r), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
