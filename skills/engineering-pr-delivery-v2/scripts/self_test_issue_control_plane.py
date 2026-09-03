#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_issue_control_plane.py"

BASE_BASIS = """ISSUE_BASIS_ID: IB-1
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

PROGRAM_FIELDS = """PROGRAM_ID: PGM-A
PROGRAM_WORK_ITEM_KEY: github:o/r#100
ISSUE_ROLE: WORK_PACKAGE
WORK_PACKAGE_ID: WP-001
PARTITION_KEY: PGM-A/WP-001
PREDECESSOR_WORK_ITEM_KEY: NONE
REVISION_SEQUENCE: 0
INHERITED_PROGRAM_BASIS_REVISION: PB-0001
INHERITED_INPUT_SET_ID: PGM-A-INPUTS-v1
INHERITED_BENCHMARK_SET_ID: PGM-A-BENCH-v1
INHERITED_VALIDATION_SET_ID: PGM-A-VALID-v1
INHERITED_ROADMAP_SET_ID: PGM-A-ROADMAP-v1
PARENT_TASK_ROWS: TASK-001
USES_INPUT_ROWS: INPUT-001
USES_BENCHMARK_ROWS: BM-001
USES_VALIDATION_ROWS: VAL-001
PROGRAM_OVERLAP_CLASSIFICATION: SAFE_DISJOINT
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


def make(root: Path, *, current=CURRENT, sync="IN_SYNC", active_ep="EP-1", latest="103", endpoint_comment="103", source="GITHUB_ISSUE", program=False, overlap="SAFE_DISJOINT", write="WRITE_ALLOWED", auto="PAUSED", role="WORK_PACKAGE", predecessor="NONE", revision="0", serialization="NONE"):
    d = root / "agents/chains/T"
    (d / "endpoints").mkdir(parents=True)
    (d / "issue-basis").mkdir(parents=True)
    (d / "issue-state").mkdir(parents=True)
    basis = BASE_BASIS
    if program:
        pf = PROGRAM_FIELDS.replace("ISSUE_ROLE: WORK_PACKAGE", f"ISSUE_ROLE: {role}").replace("PROGRAM_OVERLAP_CLASSIFICATION: SAFE_DISJOINT", f"PROGRAM_OVERLAP_CLASSIFICATION: {overlap}").replace("PREDECESSOR_WORK_ITEM_KEY: NONE", f"PREDECESSOR_WORK_ITEM_KEY: {predecessor}").replace("REVISION_SEQUENCE: 0", f"REVISION_SEQUENCE: {revision}")
        basis = pf + basis
    (d / "issue-basis/IB-1.md").write_text(basis, encoding="utf-8")
    (d / "issue-state/CURRENT.md").write_text(current, encoding="utf-8")
    program_active = ""
    if program:
        program_active = PROGRAM_FIELDS.replace("ISSUE_ROLE: WORK_PACKAGE", f"ISSUE_ROLE: {role}").replace("PROGRAM_OVERLAP_CLASSIFICATION: SAFE_DISJOINT", f"PROGRAM_OVERLAP_CLASSIFICATION: {overlap}").replace("PREDECESSOR_WORK_ITEM_KEY: NONE", f"PREDECESSOR_WORK_ITEM_KEY: {predecessor}").replace("REVISION_SEQUENCE: 0", f"REVISION_SEQUENCE: {revision}") + f"PROGRAM_SERIALIZATION_EVIDENCE: {serialization}\nWRITE_AUTHORITY: {write}\nAUTO_STATE: {auto}\n"
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
{program_active}"""
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
    ok &= expect("valid ordinary issue control plane", 0)
    diluted = CURRENT.replace("INPUT-002 | executor | UNRESOLVED | EP-1\n", "")
    ok &= expect("basis input row cannot disappear", 1, current=diluted)
    ok &= expect("IN_SYNC requires matching endpoint comment id", 1, latest="104", endpoint_comment="103")
    ok &= expect("current-state endpoint must match active", 1, active_ep="EP-2")
    ok &= expect("non-issue work has no Issue control-plane requirement", 0, source="OWNER_DIRECT", sync="NOT_RUN")
    ok &= expect("valid program work-package child", 0, program=True)
    ok &= expect("blocked sibling cannot retain write authority", 1, program=True, overlap="BLOCKED_ACTIVE_SIBLING", write="WRITE_ALLOWED")
    ok &= expect("unknown overlap read-only is valid", 0, program=True, overlap="UNKNOWN", write="READ_ONLY", auto="BLOCKED")
    ok &= expect("serialized child requires evidence before write", 1, program=True, overlap="SAFE_SERIALIZED", write="WRITE_ALLOWED", serialization="NONE")
    ok &= expect("serialized child with predecessor evidence can write", 0, program=True, overlap="SAFE_SERIALIZED", write="WRITE_ALLOWED", serialization="github:o/r#1490 terminal EP-9")
    ok &= expect("revision requires predecessor", 1, program=True, role="REVISION", predecessor="NONE", revision="1")
    ok &= expect("valid revision child", 0, program=True, role="REVISION", predecessor="github:o/r#1490", revision="1")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
