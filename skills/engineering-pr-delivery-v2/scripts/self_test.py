#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(HERE / script), *map(str, args)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def endpoint_text(
    endpoint="EP-0001",
    chain="TEST-1",
    leg="LEG-001",
    head="abc123",
    state="QUALIFICATION_REQUIRED",
    previous="NONE — chain start",
    benchmark="validation/example.json @ abc123",
    qsid="QS-0001",
):
    return f"""# {endpoint} — test endpoint

CHAIN_ID: {chain}
LEG_ID: {leg}
ENDPOINT_ID: {endpoint}
PREVIOUS_ENDPOINT: {previous}
CREATED_AT: 2026-08-27
ENDPOINT_REASON: NORMAL_CHECKPOINT
TASK / ISSUE: test relay
PR: #1
BRANCH: test
CHECKPOINT_HEAD: {head}
MAIN_HEAD_OBSERVED: main123
MERGE_BASE: main123
STATE: {state}

### Mission
Test mission.
### This leg completed
Initial grounding.
### Currently in progress
Qualification.
### Remaining work
One production trace.
### Exact next action
Inspect the live production path before mutation.
### Known / proven
Repository exists.
### Not proven
Production behavior.
### NOT_RUN
Runtime validation.
### Active hypothesis
Current mapping is correct.
### Falsifier
Independent trace disagrees.
### Protected invariants
Frozen benchmark.
### Do not redo
Initial source pin.
### Do not change
Benchmark expected value.
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
NONE — chain start.
### Validation summary
NOT_RUN — pre-qualification.
### Open risks / questions
Current mapping not independently reproduced.
### Next-agent qualification
QUALIFICATION_BASIS_HEAD: {head}
QUESTION_SET_ID: {qsid}
QUESTION_SET_STATUS: CURRENT
#### Q1 — Production Trace
Trace src/example.py from input to output.
#### Q2 — Current Unresolved Problem / Failure Isolation
Isolate the current mapping and state a falsifier.
#### Q3 — Authority / Invariant
Identify the frozen benchmark authority and protected invariant.
#### Q4 — Independent Validation
Reproduce one value independently.
#### Q5 — Next Contribution / Minimal Patch
Name the smallest legitimate patch and protected files.
"""


def index_text(active_rows, log_rows):
    active = "\n".join(active_rows)
    log = "\n".join(log_rows)
    return f"""# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | Endpoint file | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|---|
{active}

## ENDPOINT LOG

| Endpoint | Chain | Leg | Checkpoint head | State | Locator |
|---|---|---|---|---|---|
{log}
"""


def locator(chain, endpoint):
    return f"agents/agentchain/{chain}/{endpoint}.md"


def active_row(chain, endpoint, state="QUALIFICATION_REQUIRED", endpoint_file=None):
    endpoint_file = endpoint_file or locator(chain, endpoint)
    return (
        f"| {chain} | test relay | {endpoint} | {endpoint_file} | #1 | "
        f"{state} | test | inspect live path |"
    )


def log_row(
    endpoint,
    chain="TEST-1",
    leg="LEG-001",
    head="abc123",
    state="QUALIFICATION_REQUIRED",
    endpoint_locator=None,
):
    endpoint_locator = endpoint_locator or locator(chain, endpoint)
    return (
        f"| {endpoint} | {chain} | {leg} | {head} | {state} | {endpoint_locator} |"
    )


def write_endpoint(repo, chain, endpoint, text):
    path = repo / "agents" / "agentchain" / chain / f"{endpoint}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


VALID_ANSWER = """# Relay Qualification Answer
CHAIN_ID: TEST-1
ENDPOINT_ID: EP-0001
QUESTION_SET_ID: QS-0001
QUALIFICATION_BASIS_HEAD: abc123
CANDIDATE_ID: agent-b
LIVE_PR_HEAD_OBSERVED: abc123
LIVE_MAIN_HEAD_OBSERVED: main123
RECONCILIATION: MATCH
## Q1 — Production Trace
Repository-grounded answer.
## Q2 — Current Unresolved Problem / Failure Isolation
Repository-grounded answer.
## Q3 — Authority / Invariant
Repository-grounded answer.
## Q4 — Independent Validation
Repository-grounded answer.
## Q5 — Next Contribution / Minimal Patch
Repository-grounded answer.
"""

VALID_VERDICT = """# Relay Qualification Verdict
CHAIN_ID: TEST-1
ENDPOINT_ID: EP-0001
QUESTION_SET_ID: QS-0001
QUALIFICATION_BASIS_HEAD: abc123
CANDIDATE_ID: agent-b
VERIFIER_ID: agent-c
VERDICT_BASIS_HEAD: abc123
Q1 19/20
Q2 19/20
Q3 19/20
Q4 18/20
Q5 19/20
TOTAL 94/100
MINIMUM_QUESTION 18/20
AUTOMATIC_FAILURE_REASON: NONE
VERDICT: PASS_WRITE_ALLOWED
"""

SELF_VERDICT = VALID_VERDICT.replace("VERIFIER_ID: agent-c", "VERIFIER_ID: agent-b")
LOW_SCORE_PASS = (
    VALID_VERDICT.replace("Q4 18/20", "Q4 16/20")
    .replace("TOTAL 94/100", "TOTAL 92/100")
    .replace("MINIMUM_QUESTION 18/20", "MINIMUM_QUESTION 16/20")
)
UNJUSTIFIED_FAIL = VALID_VERDICT.replace(
    "VERDICT: PASS_WRITE_ALLOWED", "VERDICT: FAIL_READ_ONLY"
)


def expect(result, should_pass, label):
    ok = result.returncode == 0
    if ok != should_pass:
        print(f"FAIL SELF-TEST: {label}")
        print(result.stdout)
        return False
    print(f"PASS SELF-TEST: {label}")
    return True


def validate_index(repo):
    return run("validate_agentchain.py", repo / "agents" / "agentchain.md")


def main():
    checks = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        # 1. Valid single split endpoint.
        repo = root / "valid-single"
        (repo / "agents").mkdir(parents=True)
        write_endpoint(repo, "TEST-1", "EP-0001", endpoint_text())
        (repo / "agents" / "agentchain.md").write_text(
            index_text(
                [active_row("TEST-1", "EP-0001")],
                [log_row("EP-0001")],
            ),
            encoding="utf-8",
        )
        checks.append(expect(validate_index(repo), True, "valid split agentchain"))

        # 2. Valid two-endpoint chain with current active pointer.
        repo2 = root / "valid-two"
        (repo2 / "agents").mkdir(parents=True)
        write_endpoint(repo2, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(
            repo2,
            "TEST-1",
            "EP-0002",
            endpoint_text(
                endpoint="EP-0002",
                head="def456",
                previous="EP-0001",
                qsid="QS-0002",
            ),
        )
        (repo2 / "agents" / "agentchain.md").write_text(
            index_text(
                [active_row("TEST-1", "EP-0002")],
                [log_row("EP-0001"), log_row("EP-0002", head="def456")],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(repo2), True, "valid two-endpoint split chain")
        )

        # 3. Stale active pointer must fail.
        stale = root / "stale-active"
        (stale / "agents").mkdir(parents=True)
        write_endpoint(stale, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(
            stale,
            "TEST-1",
            "EP-0002",
            endpoint_text(
                endpoint="EP-0002",
                head="def456",
                previous="EP-0001",
                qsid="QS-0002",
            ),
        )
        (stale / "agents" / "agentchain.md").write_text(
            index_text(
                [active_row("TEST-1", "EP-0001")],
                [log_row("EP-0001"), log_row("EP-0002", head="def456")],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(stale), False, "stale ACTIVE CHAINS pointer rejected")
        )

        # 4. Cross-chain predecessor must fail.
        cross = root / "cross-chain"
        (cross / "agents").mkdir(parents=True)
        write_endpoint(cross, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(
            cross,
            "TEST-2",
            "EP-0002",
            endpoint_text(
                endpoint="EP-0002",
                chain="TEST-2",
                head="ghi789",
                previous="EP-0001",
                qsid="QS-0002",
            ),
        )
        (cross / "agents" / "agentchain.md").write_text(
            index_text(
                [
                    active_row("TEST-1", "EP-0001"),
                    active_row("TEST-2", "EP-0002"),
                ],
                [
                    log_row("EP-0001"),
                    log_row("EP-0002", chain="TEST-2", head="ghi789"),
                ],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(cross), False, "cross-chain PREVIOUS_ENDPOINT rejected")
        )

        # 5. Missing endpoint file must fail.
        missing = root / "missing-endpoint"
        (missing / "agents").mkdir(parents=True)
        (missing / "agents" / "agentchain.md").write_text(
            index_text(
                [active_row("TEST-1", "EP-0001")],
                [log_row("EP-0001")],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(missing), False, "missing endpoint file rejected")
        )

        # 6. Orphan durable endpoint after crash must be detected.
        orphan = root / "orphan-endpoint"
        (orphan / "agents").mkdir(parents=True)
        write_endpoint(orphan, "TEST-1", "EP-0001", endpoint_text())
        write_endpoint(
            orphan,
            "TEST-1",
            "EP-0002",
            endpoint_text(
                endpoint="EP-0002",
                head="def456",
                previous="EP-0001",
                qsid="QS-0002",
            ),
        )
        (orphan / "agents" / "agentchain.md").write_text(
            index_text(
                [active_row("TEST-1", "EP-0001")],
                [log_row("EP-0001")],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(orphan), False, "orphan endpoint file detected")
        )

        # 7. Historical legacy blob plus current split endpoint is valid migration.
        legacy = root / "legacy-history"
        (legacy / "agents").mkdir(parents=True)
        legacy_locator = "git-blob:" + ("a" * 40) + "#EP-0000"
        write_endpoint(
            legacy,
            "TEST-1",
            "EP-0001",
            endpoint_text(previous="EP-0000"),
        )
        (legacy / "agents" / "agentchain.md").write_text(
            index_text(
                [active_row("TEST-1", "EP-0001")],
                [
                    log_row("EP-0000", endpoint_locator=legacy_locator),
                    log_row("EP-0001"),
                ],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(legacy), True, "historical legacy blob locator accepted")
        )

        # 8. A legacy blob cannot be the active baton.
        active_legacy = root / "active-legacy"
        (active_legacy / "agents").mkdir(parents=True)
        legacy_locator = "git-blob:" + ("b" * 40) + "#EP-0001"
        (active_legacy / "agents" / "agentchain.md").write_text(
            index_text(
                [
                    active_row(
                        "TEST-1",
                        "EP-0001",
                        endpoint_file=legacy_locator,
                    )
                ],
                [log_row("EP-0001", endpoint_locator=legacy_locator)],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(active_legacy), False, "active legacy blob rejected")
        )

        # 9. Empty benchmark inventory must fail.
        bad_benchmark = root / "empty-benchmark"
        (bad_benchmark / "agents").mkdir(parents=True)
        write_endpoint(
            bad_benchmark,
            "TEST-1",
            "EP-0001",
            endpoint_text(benchmark=""),
        )
        (bad_benchmark / "agents" / "agentchain.md").write_text(
            index_text(
                [active_row("TEST-1", "EP-0001")],
                [log_row("EP-0001")],
            ),
            encoding="utf-8",
        )
        checks.append(
            expect(validate_index(bad_benchmark), False, "empty benchmark inventory rejected")
        )

        answer = root / "answer.md"
        verdict = root / "verdict.md"
        self_verdict = root / "self-verdict.md"
        low_score_pass = root / "low-score-pass.md"
        unjustified_fail = root / "unjustified-fail.md"
        answer.write_text(VALID_ANSWER, encoding="utf-8")
        verdict.write_text(VALID_VERDICT, encoding="utf-8")
        self_verdict.write_text(SELF_VERDICT, encoding="utf-8")
        low_score_pass.write_text(LOW_SCORE_PASS, encoding="utf-8")
        unjustified_fail.write_text(UNJUSTIFIED_FAIL, encoding="utf-8")

        # 10-13. Qualification gates.
        checks.append(
            expect(
                run("validate_qualification.py", answer, verdict),
                True,
                "valid independent qualification",
            )
        )
        checks.append(
            expect(
                run("validate_qualification.py", answer, self_verdict),
                False,
                "self-verification rejected",
            )
        )
        checks.append(
            expect(
                run("validate_qualification.py", answer, low_score_pass),
                False,
                "PASS_WRITE_ALLOWED rejected when any question is below 17/20",
            )
        )
        checks.append(
            expect(
                run("validate_qualification.py", answer, unjustified_fail),
                False,
                "numeric pass cannot be failed with AUTOMATIC_FAILURE_REASON=NONE",
            )
        )

        # 14. Composite relay gate.
        checks.append(
            expect(
                run(
                    "check_relay.py",
                    repo / "agents" / "agentchain.md",
                    answer,
                    verdict,
                ),
                True,
                "composite split relay gate",
            )
        )

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
