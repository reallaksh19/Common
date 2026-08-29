#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_engineering_question_payload.py"


def endpoint(profile="FEA", strong=True):
    def q(n, payload, derivation):
        return f"""#### Q{n} — Test
Domain challenge: reconstruct bounded engineering quantity
Exact repository data required: live bounded case
Concrete payload: {payload}
Required derivation: {derivation}
"""
    if strong:
        payloads = [
            ("N1=(0,0), N2=(40,0), N3=(0,30) mm", "derive shape derivatives and Jacobian"),
            ("N4=(22,2), xi=0.166667, eta=0.166667", "compute J and det J numerically"),
            ("element=17, node=6, load=1000 N", "trace ownership and falsifier"),
            ("a=10 mm, R=100 mm, sigma=50 MPa", "derive Kirsch boundary traction"),
            ("before=0, after=1, tolerance=0", "derive minimal safe patch boundary"),
        ]
    else:
        payloads = [
            ("mesh", "explain solver"),
            ("distorted T6", "reconstruct Jacobian"),
            ("hole topology", "describe ownership"),
            ("Kirsch reference", "reconstruct oracle"),
            ("safe patch", "describe rollback"),
        ]
    bodies = "\n".join(q(i + 1, *payloads[i]) for i in range(5))
    return f"""# EP
QUALIFICATION_PROFILE: {profile}
QUALIFICATION_PROFILE_VERSION: 2
### Takeover qualification pack
QUALIFICATION_PROFILE: {profile}
QUALIFICATION_PROFILE_VERSION: 2
{bodies}
"""


def write(root, text):
    d = root / "agents/chains/T/endpoints"
    d.mkdir(parents=True)
    (d / "EP.md").write_text(text, encoding="utf-8")
    (d.parent / "ACTIVE.md").write_text("""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
STATE: ACTIVE
ACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP.md
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
        r = Path(td); write(r, endpoint(strong=True)); ok &= expect("concrete FEA payload", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write(r, endpoint(strong=False)); ok &= expect("topic-label FEA payload rejected", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write(r, endpoint(profile="GENERAL_ENGINEERING", strong=True)); ok &= expect("general exact reconstruction", run(r), 0)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
