#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def run(index):
    return subprocess.run(
        [sys.executable, str(HERE / "validate_agentchain.py"), str(index)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def expect(result, should_pass, label):
    ok = result.returncode == 0
    if ok != should_pass:
        print(f"FAIL SELF-TEST: {label}")
        print(result.stdout)
        return False
    print(f"PASS SELF-TEST: {label}")
    return True


def locator(chain, endpoint):
    return f"agents/agentchain/{chain}/{endpoint}.md"


def endpoint_text(endpoint="EP-0001", chain="TEST-1", head="abc123", previous="NONE — chain start", benchmark="validation/example.json @ abc123", qsid="QS-0001"):
    return f"""# {endpoint} — test
CHAIN_ID: {chain}
LEG_ID: LEG-001
ENDPOINT_ID: {endpoint}
PREVIOUS_ENDPOINT: {previous}
ENDPOINT_REASON: NORMAL_CHECKPOINT
CHECKPOINT_HEAD: {head}
MAIN_HEAD_OBSERVED: main123
STATE: QUALIFICATION_REQUIRED
### Mission
Test.
### This leg completed
Grounded.
### Currently in progress
Qualification.
### Remaining work
Trace.
### Exact next action
Inspect live path.
### Known / proven
Repo exists.
### Not proven
Runtime.
### NOT_RUN
Runtime.
### Active hypothesis
Mapping correct.
### Falsifier
Trace differs.
### Protected invariants
Benchmark.
### Do not redo
Source pin.
### Do not change
Benchmark.
### Expected next-leg files / domains
src/example.py
### Inputs
input/example.json @ abc123
### Benchmarks
{benchmark}
### Common / governing documents
AGENTS.md @ abc123
### Authoritative sources
source/example.md @ abc123
### Production paths
src/example.py
### Validation / test paths
tests/test_example.py
### Changed during this leg
NONE.
### Validation summary
NOT_RUN.
### Open risks / questions
Unverified.
### Next-agent qualification
QUALIFICATION_BASIS_HEAD: {head}
QUESTION_SET_ID: {qsid}
QUESTION_SET_STATUS: CURRENT
#### Q1 — Production Trace
Trace live path.
#### Q2 — Current Unresolved Problem / Failure Isolation
Isolate failure.
#### Q3 — Authority / Invariant
Trace authority.
#### Q4 — Independent Validation
Validate independently.
#### Q5 — Next Contribution / Minimal Patch
Define patch.
"""


def write_endpoint(repo, chain, endpoint, text):
    path = repo / "agents" / "agentchain" / chain / f"{endpoint}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def active_row(chain, endpoint, endpoint_file=None):
    endpoint_file = endpoint_file or locator(chain, endpoint)
    return f"| {chain} | test | {endpoint} | {endpoint_file} | #1 | QUALIFICATION_REQUIRED | test | inspect |"


def log_row(endpoint, chain="TEST-1", head="abc123", endpoint_locator=None):
    endpoint_locator = endpoint_locator or locator(chain, endpoint)
    return f"| {endpoint} | {chain} | LEG-001 | {head} | QUALIFICATION_REQUIRED | {endpoint_locator} |"


def index_text(active_rows, log_rows):
    return """# Engineering Agent Chain
AGENTCHAIN_VERSION: 2
## ACTIVE CHAINS
| Chain | Mission | Latest endpoint | Endpoint file | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|---|
%s
## ENDPOINT LOG
| Endpoint | Chain | Leg | Checkpoint head | State | Locator |
|---|---|---|---|---|---|
%s
""" % ("\n".join(active_rows), "\n".join(log_rows))


def make_repo(root, name):
    repo = root / name
    (repo / "agents").mkdir(parents=True)
    return repo


def main():
    checks = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        repo = make_repo(root, "valid-single")
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text())
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001")], [log_row("EP-0001")]))
        checks.append(expect(run(idx), True, "valid split endpoint/index"))

        repo = make_repo(root, "valid-two")
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(repo, "TEST-1", "EP-0002", endpoint_text("EP-0002", head="def456", previous="EP-0001", qsid="QS-0002"))
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0002")], [log_row("EP-0001"), log_row("EP-0002", head="def456")]))
        checks.append(expect(run(idx), True, "valid two-endpoint chain"))

        repo = make_repo(root, "stale")
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(repo, "TEST-1", "EP-0002", endpoint_text("EP-0002", head="def456", previous="EP-0001", qsid="QS-0002"))
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001")], [log_row("EP-0001"), log_row("EP-0002", head="def456")]))
        checks.append(expect(run(idx), False, "stale active pointer rejected"))

        repo = make_repo(root, "cross-chain")
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(repo, "TEST-2", "EP-0002", endpoint_text("EP-0002", chain="TEST-2", head="ghi789", previous="EP-0001", qsid="QS-0002"))
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001"), active_row("TEST-2", "EP-0002")], [log_row("EP-0001"), log_row("EP-0002", chain="TEST-2", head="ghi789")]))
        checks.append(expect(run(idx), False, "cross-chain predecessor rejected"))

        repo = make_repo(root, "missing")
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001")], [log_row("EP-0001")]))
        checks.append(expect(run(idx), False, "missing endpoint file rejected"))

        repo = make_repo(root, "orphan")
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(repo, "TEST-1", "EP-0002", endpoint_text("EP-0002", head="def456", previous="EP-0001", qsid="QS-0002"))
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001")], [log_row("EP-0001")]))
        checks.append(expect(run(idx), False, "orphan endpoint detected"))

        repo = make_repo(root, "legacy")
        legacy = "git-blob:" + "a" * 40 + "#EP-0000"
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text(previous="EP-0000"))
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001")], [log_row("EP-0000", endpoint_locator=legacy), log_row("EP-0001")]))
        checks.append(expect(run(idx), True, "historical legacy locator accepted"))

        repo = make_repo(root, "active-legacy")
        legacy = "git-blob:" + "b" * 40 + "#EP-0001"
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001", endpoint_file=legacy)], [log_row("EP-0001", endpoint_locator=legacy)]))
        checks.append(expect(run(idx), False, "active legacy locator rejected"))

        repo = make_repo(root, "empty-benchmark")
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text(benchmark=""))
        idx = repo / "agents" / "agentchain.md"
        idx.write_text(index_text([active_row("TEST-1", "EP-0001")], [log_row("EP-0001")]))
        checks.append(expect(run(idx), False, "empty benchmark inventory rejected"))

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
