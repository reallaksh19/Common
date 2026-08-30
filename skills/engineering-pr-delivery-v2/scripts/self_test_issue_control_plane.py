#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_issue_control_plane.py"

BASIS = """ISSUE_BASIS_ID: IB-1
WORK_ITEM_KEY: github:o/r#1535
ISSUE_SOURCE: github:o/r#1535
ISSUE_SOURCE_SNAPSHOT_AT: abc
PREVIOUS_ISSUE_BASIS: NONE
CHANGE_AUTHORITY: INITIAL_CAPTURE
ISSUE_BASIS_STATUS: CURRENT
### Original task / acceptance ledger
TASK-001 | task one | OPEN | issue
TASK-002 | task two | COMPLETE | issue
### Input ledger
INPUT-001 | geometry | AVAILABLE | issue
INPUT-002 | executor | UNRESOLVED | issue
### Benchmark / oracle ledger
BM-001 | T6 | PASS | ep
BM-002 | Kirsch | NOT_RUN | issue
### Roadmap ledger
RM-001 | roadmap@abc | OWNER_ROADMAP | PRIMARY | ALIGNED | owner
### Owner qualification baseline
BASE-1 | current
"""

CURRENT = """ISSUE_BASIS_ID: IB-1
CURRENT_ENDPOINT: EP-1
UPDATED_AT_HEAD: abc
### Original task / acceptance ledger
TASK-001 | task one | PARTIAL | EP-1
TASK-002 | task two | COMPLETE | issue
### Input ledger
INPUT-001 | geometry | AVAILABLE | issue
INPUT-002 | executor | UNRESOLVED | EP-1
### Benchmark / oracle ledger
BM-001 | T6 | PASS | EP-1
BM-002 | Kirsch | NOT_RUN | issue
### Roadmap ledger
RM-001 | roadmap@abc | OWNER_ROADMAP | PRIMARY | ALIGNED | owner
### Owner qualification baseline
BASE-1 | current
"""


def make(root: Path, *, current=CURRENT, sync="IN_SYNC", active_ep="EP-1", latest="103", endpoint_comment="103", source="GITHUB_ISSUE"):
    d = root / "agents/chains/T"
    (d / "endpoints").mkdir(parents=True)
    (d / "issue-basis").mkdir(parents=True)
    (d / "issue-state").mkdir(parents=True)
    (d / "issue-basis/IB-1.md").write_text(BASIS, encoding="utf-8")
    (d / "issue-state/CURRENT.md").write_text(current, encoding="utf-8")
    active = f"""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
ACTIVE_ENDPOINT: {active_ep}
ACTIVE_ENDPOINT_FILE: agents/chains/T/endpoints/EP-1.md
WORK_ITEM_SOURCE: {source}
WORK_ITEM_KEY: github:o/r#1535
ISSUE_BASIS_ID: IB-1
ISSUE_BASIS_FILE: agents/chains/T/issue-basis/IB-1.md
ISSUE_BASIS_STATUS: CURRENT
ISSUE_CURRENT_STATE_FILE: agents/chains/T/issue-state/CURRENT.md
ISSUE_CURRENT_STATE_BASIS: IB-1
ISSUE_CURRENT_STATE_ENDPOINT: {active_ep}
ISSUE_CHAIN_ROOT_COMMENT_ID: 101
ISSUE_ACTIVE_HANDOVER_COMMENT_ID: 102
ISSUE_LATEST_ENDPOINT_COMMENT_ID: {latest}
ISSUE_HANDOVER_SYNC_STATUS: {sync}
"""
    (d / "ACTIVE.md").write_text(active, encoding="utf-8")
    (d / "endpoints/EP-1.md").write_text(f"ISSUE_ENDPOINT_COMMENT_ID: {endpoint_comment}\nPREVIOUS_ISSUE_ENDPOINT_COMMENT_ID: 99\n", encoding="utf-8")


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, expected, **kwargs):
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
    ok &= expect("valid issue control plane", 0)
    diluted = CURRENT.replace("INPUT-002 | executor | UNRESOLVED | EP-1\n", "")
    ok &= expect("basis input row cannot disappear", 1, current=diluted)
    ok &= expect("IN_SYNC requires matching endpoint comment id", 1, latest="104", endpoint_comment="103")
    ok &= expect("current-state endpoint must match active", 1, active_ep="EP-2")
    ok &= expect("non-issue work has no Issue control-plane requirement", 0, source="OWNER_DIRECT", sync="NOT_RUN")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
