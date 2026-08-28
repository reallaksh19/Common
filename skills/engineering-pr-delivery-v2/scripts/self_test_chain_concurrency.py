#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_chain_store.py"
OVERLAP = HERE / "detect_chain_overlap.py"

SECTIONS = [
    "Mission",
    "This leg completed",
    "Currently in progress",
    "Remaining work",
    "Exact next action",
    "Known / proven",
    "Not proven",
    "NOT_RUN",
    "Active hypothesis",
    "Falsifier",
    "Protected invariants",
    "Do not redo",
    "Do not change",
    "Expected next-leg files / domains",
    "Inputs",
    "Benchmarks",
    "Common / governing documents",
    "Authoritative sources",
    "Production paths",
    "Validation / test paths",
    "Changed during this leg",
    "Validation summary",
    "Open risks / questions",
    "Next-agent qualification",
]


def endpoint(chain, eid, previous, epoch, path_token, head=None):
    head = head or (f"{epoch:040x}"[-40:])
    lines = [
        f"# {eid} — test endpoint",
        "",
        f"CHAIN_ID: {chain}",
        "LEG_ID: LEG-001",
        f"ENDPOINT_ID: {eid}",
        f"PREVIOUS_ENDPOINT: {previous}",
        "CREATED_AT: 2026-08-28T00:00:00Z",
        "ENDPOINT_REASON: NORMAL_CHECKPOINT",
        "TASK / ISSUE: test",
        "PR: #1",
        "BRANCH: test",
        f"CHECKPOINT_HEAD: {head}",
        f"MAIN_HEAD_OBSERVED: {head}",
        f"CUSTODY_EPOCH: {epoch}",
        "STATE: READY_FOR_NEXT_LEG",
        "",
    ]
    for title in SECTIONS:
        lines.append(f"### {title}")
        if title == "Expected next-leg files / domains":
            lines.append(f"- `{path_token}`")
        elif title == "Production paths":
            lines.append(f"- `{path_token}`")
        elif title == "Next-agent qualification":
            lines.extend(
                [
                    f"QUALIFICATION_BASIS_HEAD: {head}",
                    f"QUESTION_SET_ID: QS-{chain}-{eid}",
                    "QUESTION_SET_STATUS: CURRENT",
                ]
            )
        else:
            lines.append("NONE — test fixture")
        lines.append("")

    for n, title in [
        (1, "Production Trace"),
        (2, "Current Unresolved Problem / Failure Isolation"),
        (3, "Authority / Invariant"),
        (4, "Independent Validation"),
        (5, "Next Contribution / Minimal Patch"),
    ]:
        lines.extend([f"#### Q{n} — {title}", "Repository-specific test question.", ""])
    return "\n".join(lines)


def active(chain, eid, epoch, path_token, head=None, authority=None):
    head = head or (f"{epoch:040x}"[-40:])
    authority = authority or f"{chain}-AUTH"
    return f"""CHAIN_STATE_VERSION: 1
CHAIN_ID: {chain}
MISSION: test mission
ACTIVE_ENDPOINT: {eid}
ACTIVE_ENDPOINT_FILE: agents/chains/{chain}/endpoints/{eid}.md
PR: #1
BRANCH: test
HEAD: {head}
STATE: READY_FOR_NEXT_LEG
AUTHORITY_DOMAIN: {authority}
ACTIVE_CUSTODIAN: agent-test
CUSTODY_EPOCH: {epoch}
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
"""


def write_chain(root, chain, endpoints, active_eid, active_epoch, path_token, authority=None):
    chain_dir = root / "agents" / "chains" / chain
    ep_dir = chain_dir / "endpoints"
    ep_dir.mkdir(parents=True, exist_ok=True)
    for eid, previous, epoch in endpoints:
        (ep_dir / f"{eid}.md").write_text(
            endpoint(chain, eid, previous, epoch, path_token), encoding="utf-8"
        )
    (chain_dir / "ACTIVE.md").write_text(
        active(chain, active_eid, active_epoch, path_token, authority=authority),
        encoding="utf-8",
    )


def run(script, root):
    return subprocess.run(
        [sys.executable, str(script), str(root)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def expect(name, result, expected_rc):
    if result.returncode != expected_rc:
        print(f"FAIL SELF-TEST: {name}; rc={result.returncode}; expected={expected_rc}")
        print(result.stdout)
        return False
    print(f"PASS SELF-TEST: {name}")
    return True


def main():
    ok = True

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # Same EP-0001 is intentionally valid in three different chains.
        write_chain(root, "ADV-WRC-1389", [("EP-0001", "NONE — chain start", 1)], "EP-0001", 1, "src/core/emp1")
        write_chain(root, "ADV-LAFEA-1422", [("EP-0001", "NONE — chain start", 1)], "EP-0001", 1, "src/core/lafea")
        write_chain(root, "ADV-LOADCALC-1505", [("EP-0001", "NONE — chain start", 1)], "EP-0001", 1, "src/core/loadcalc")
        ok &= expect("chain-local EP-0001 reused across independent chains", run(VALIDATOR, root), 0)
        ok &= expect("independent WRC/LAFEA/LoadCalc paths do not collide", run(OVERLAP, root), 0)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_chain(
            root,
            "ADV-WRC-1389",
            [("EP-0001", "NONE — chain start", 1), ("EP-0002", "EP-0001", 2)],
            "EP-0002",
            2,
            "src/core/emp1",
        )
        ok &= expect("same-chain sequential custody epochs", run(VALIDATOR, root), 0)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_chain(
            root,
            "ADV-WRC-1389",
            [("EP-0001", "NONE — chain start", 1), ("EP-0002", "EP-0001", 2)],
            "EP-0002",
            1,
            "src/core/emp1",
        )
        ok &= expect("stale ACTIVE custody epoch rejected", run(VALIDATOR, root), 1)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_chain(
            root,
            "ADV-WRC-1389",
            [
                ("EP-0001", "NONE — chain start", 1),
                ("EP-0002A", "EP-0001", 2),
                ("EP-0002B", "EP-0001", 2),
            ],
            "EP-0002A",
            2,
            "src/core/emp1",
        )
        ok &= expect("divergent same-chain successors rejected", run(VALIDATOR, root), 1)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_chain(root, "ADV-WRC-1389", [("EP-0001", "NONE — chain start", 1)], "EP-0001", 1, "src/core/shared")
        write_chain(root, "ADV-LAFEA-1422", [("EP-0001", "NONE — chain start", 1)], "EP-0001", 1, "src/core/shared")
        ok &= expect("real shared-path overlap requires coordination", run(OVERLAP, root), 1)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
