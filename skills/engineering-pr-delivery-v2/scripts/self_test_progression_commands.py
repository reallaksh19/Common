#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_progression_command.py"


def make(root: Path, *, cmd, action, status, display, takeover, chain="TRUE", source="OWNER_DIRECT", sync=None):
    d = root / "agents/chains/T"
    (d / "endpoints").mkdir(parents=True)
    common = f"""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
ACTIVE_ENDPOINT: EP-1
ACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP-1.md
OWNER_PROGRESSION_COMMAND: {cmd}
QUALIFICATION_SCOPE_ID: QSCOPE-T-1
QUESTION_SET_ID: QS-T-1
QUESTION_SET_STATUS: {status}
QUESTION_PACK_ACTION: {action}
QUESTION_DISPLAY: {display}
CHAIN_HANDOVER_READY: {chain}
TAKEOVER_QUALIFICATION_READY: {takeover}
WORK_ITEM_SOURCE: {source}
HANDOVER_VALIDATION_STATUS: PASS
"""
    if sync is not None:
        common += f"ISSUE_HANDOVER_SYNC_STATUS: {sync}\n"
    (d / "ACTIVE.md").write_text(common, encoding="utf-8")
    (d / "endpoints/EP-1.md").write_text(common, encoding="utf-8")


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def case(name, expected, **kwargs):
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        make(root, **kwargs)
        r = run(root)
        ok = r.returncode == expected
        print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
        if not ok:
            print(r.stdout + r.stderr)
        return ok


def main():
    ok = True
    ok &= case("proceed next reuses current set", 0, cmd="PROCEED_NEXT", action="REUSED", status="CURRENT", display="HIDE", takeover="TRUE")
    ok &= case("proceed next refresh shows questions", 0, cmd="PROCEED_NEXT", action="REFRESHED", status="CURRENT", display="SHOW", takeover="TRUE")
    ok &= case("no-Q current set remains takeover-ready", 0, cmd="PROCEED_NEXT_NO_QS", action="SUPPRESSED_BY_OWNER", status="CURRENT", display="HIDE", takeover="TRUE")
    ok &= case("no-Q stale set preserves chain but blocks takeover", 0, cmd="PROCEED_NEXT_NO_QS", action="SUPPRESSED_BY_OWNER", status="STALE", display="HIDE", takeover="FALSE")
    ok &= case("no-Q stale cannot claim takeover ready", 1, cmd="PROCEED_NEXT_NO_QS", action="SUPPRESSED_BY_OWNER", status="STALE", display="HIDE", takeover="TRUE")
    ok &= case("handover ready shows current questions", 0, cmd="PROCEED_NEXT_HANDOVER_READY", action="REUSED", status="CURRENT", display="SHOW", takeover="TRUE")
    ok &= case("handover ready cannot hide questions", 1, cmd="PROCEED_NEXT_HANDOVER_READY", action="REUSED", status="CURRENT", display="HIDE", takeover="TRUE")
    ok &= case("fourth command rejected", 1, cmd="CONTINUE", action="REUSED", status="CURRENT", display="HIDE", takeover="TRUE")
    ok &= case("issue handover ready requires sync", 1, cmd="PROCEED_NEXT_HANDOVER_READY", action="REUSED", status="CURRENT", display="SHOW", takeover="TRUE", source="GITHUB_ISSUE", sync="STALE")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
