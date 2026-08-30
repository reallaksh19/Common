#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_handover_readiness.py"


def state(status="PASS", ready="TRUE", evidence="receipt:1", content="TRUE"):
    return f"""HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: {content}
HANDOVER_VALIDATION_STATUS: {status}
HANDOVER_VALIDATION_EVIDENCE: {evidence}
HANDOVER_READY: {ready}
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
"""


def write(root, active_state, endpoint_state=None):
    d = root / "agents/chains/T/endpoints"
    d.mkdir(parents=True)
    endpoint_state = endpoint_state or active_state
    (d / "EP.md").write_text(endpoint_state, encoding="utf-8")
    (d.parent / "ACTIVE.md").write_text(
        "CHAIN_STATE_VERSION: 3\nCHAIN_ID: T\nSTATE: ACTIVE\nACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP.md\n" + active_state,
        encoding="utf-8",
    )


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
        r = Path(td); write(r, state()); ok &= expect("validated content is ready", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write(r, state(status="NOT_RUN", ready="FALSE", evidence="NONE")); ok &= expect("NOT_RUN truthfully not ready", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write(r, state(status="NOT_RUN", ready="TRUE", evidence="NONE")); ok &= expect("NOT_RUN cannot self-declare ready", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); write(r, state(status="PASS", ready="TRUE", evidence="NONE")); ok &= expect("PASS without evidence not ready", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        d = r / "agents/chains/OLD"; d.mkdir(parents=True)
        (d / "ACTIVE.md").write_text("CHAIN_STATE_VERSION: 3\nCHAIN_ID: OLD\nSTATE: ACTIVE\n", encoding="utf-8")
        ok &= expect("historical endpoint grandfathered", run(r), 0)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
