#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_issue_workorder.py"

BASE = r'''# Mission
Implement the exact retained production route from governed source to accepted output.

# 0. Ground truth at issue creation
Observed main: `0123456789012345678901234567890123456789`.
Do not assume this SHA is current when implementation begins. Re-ground first.

# 1. Owner intent, authority and scope
Owner intent is to close the bounded route without changing the Owner roadmap or source/oracle authority.

# 2. Definition of Done
The retained source, produced artifact, calculation and output all share the current authority identity.

# 3. Input/source inventory
| ID | Source | Authority | Data | Status |
|---|---|---|---|---|
| INPUT-001 | `fixtures/case.json` | PRODUCTION_INPUT | coordinates, load, material | AVAILABLE |

# 4. Current production/repository path to preserve
`fixtures/case.json` -> `normalizeCase()` -> `bindCase()` -> `runCase()` -> result.

# 5. Technical implementation instructions
Use the live public APIs. Do not duplicate architecture.
```js
const input = loadCase('fixtures/case.json');
const normalized = normalizeCase(input);
const retained = bindCase(normalized);
const result = runCase(retained);
assert(result.caseId === retained.caseId);
```

# 6. PASS / FAIL / NOT_RUN criteria
PASS means the focused route executes and the retained ID matches. FAIL means a numerical/state assertion fails. NOT_RUN means it did not execute.

# 7. Benchmark / independent oracle criteria
| ID | Type | Source | Inputs | Expected | Tolerance | Independent | Status |
|---|---|---|---|---|---|---|---|
| BM-001 | FROZEN_ANALYTICAL | `validation/case.md` | L=200, E=200000, P=1000 | delta=4.0 | 1e-6 mm | YES | READY |
| BM-002 | PRODUCT_REGRESSION | `tests/case.test.js` | sample | state=READY | exact | NO | READY |
A product regression is not an independent oracle. Never choose expected values or tolerance from current production output.

# 8. Anti-drift / fail-closed logic
Re-ground main before coding. If production output disagrees with the independent oracle, do not weaken tolerance or regenerate expected values. A stale parent must block execution.

# 9. Negative tests and falsifiers
Mutate source revision without regenerating the retained artifact; execution must reject the stale parent. The hypothesis is falsified if the current public route already rejects the observed failure before the proposed patch.

# 10. Explicit exclusions / non-goals
NO roadmap mutation. NO benchmark re-baselining. NO direct-core bypass. NO merge without Owner authorization.

# 11. Validation matrix
| Boundary | PASS | Independent | Negative | Status |
|---|---|---|---|---|
| source custody | required | N/A | yes | NOT_RUN |
| numerical result | required | yes | yes | NOT_RUN |

# Appendix A — implementation qualification
QUESTION_PROFILE: NUMERICAL_ENGINEERING

## Q1 — Walk me through the actual case
Take `fixtures/case.json` and trace the real case through `normalizeCase()`, `bindCase()`, `runCase()` and result publication. Tell me which current case/source IDs should survive each boundary, what exact retained object the solver consumes, and what single mismatch would falsify your trace before you propose any code change.

## Q2 — Do this calculation before touching the code
For the actual benchmark values L=200 mm, E=200000 MPa, P=1000 N and I=6666.6667 mm^4, calculate the Euler-Bernoulli tip deflection by hand, show the numerator and denominator separately, then point to the first production function in `src/solver/beam.js` whose result should be compared with your independent value and explain the first-wrong-boundary interpretation if they disagree.

## Q3 — Show me where stale state gets stopped
Change `sourceRevision` from 17 to 18 while deliberately keeping retained mesh revision 17 and execution parent 17. Walk through the exact authority/invariant checks that should reject Run, name the expected stale state/error, and give one falsifier test that would prove your understanding of the current custody boundary is wrong.

## Q4 — Prove the benchmark independently
Using a=10 mm, R=100 mm and sigma=50 MPa from `validation/kirsch.json`, independently derive the expected hoop stress at the hole boundary and the remote-boundary traction components at theta=0 and theta=90 before looking at production output. State units, sign convention and tolerance, then explain why `tests/product-regression.js` cannot serve as the oracle for this comparison.

## Q5 — What is the smallest patch you would make?
Assume the hand result and current repository trace show the first wrong boundary is `bindCase()` retaining an obsolete parent ID. Name the smallest exact patch and files you would change, the failing evidence expected before it, PASS evidence after it, the neighbor regression that must remain unchanged, your rollback/falsifier condition, and the explicit NO-PATCH case if live main already rejects the stale parent correctly.
'''

PROGRAM = r'''ISSUE_ROLE: PROGRAM_ROOT
PROGRAM_ID: PGM-AA-LAFEA
PROGRAM_WORK_ITEM_KEY: SELF_AFTER_CREATION
PROGRAM_BASIS_REVISION: PB-0001
COMMON_INPUT_SET_ID: PGM-AA-LAFEA-INPUTS-v1
COMMON_BENCHMARK_SET_ID: PGM-AA-LAFEA-BENCH-v1
COMMON_VALIDATION_SET_ID: PGM-AA-LAFEA-VALID-v1
COMMON_ROADMAP_SET_ID: PGM-AA-LAFEA-ROADMAP-v1

# Mission
Close the Owner program without losing common engineering authority across agents.

# 0. Ground truth at program creation
Observed main `0123456789012345678901234567890123456789`. Re-ground every child before work.

# 1. Original task ledger
TASK-001 | complete production route | OPEN | Owner issue

# 2. Roadmap ledger
RM-001 | `docs/roadmap.md` | abc | PRIMARY | ALIGNED | OWNER_ONLY

# 3. Common inputs
INPUT-001 | `input/model.json` | PRODUCTION_INPUT | geometry/material | AVAILABLE | invalidates mesh/result

# 4. Common benchmark / oracle
BM-001 | FROZEN_ANALYTICAL | `validation/ref.json` | actual values | stress | 2% | YES | READY
Product regression is not an independent oracle; production output may not select expected values or tolerance.

# 5. Common validation
VAL-001 | `node scripts/check.mjs` | PASS | WP-001 | NOT_RUN

# 6. Program Definition of Done
PASS requires TASK-001 satisfied, required child work complete, common oracle current, and NOT_RUN never promoted.

# 7. Work-package partition registry
| WP | Relation | Child | Scope | Owned paths | Depends | Rows | Status | Chain/PR | Overlap |
|---|---|---|---|---|---|---|---|---|---|
| WP-001 | IMPLEMENTATION | PENDING | route | `src/a/**` | NONE | INPUT-001; BM-001; VAL-001 | PLANNED | PENDING | SAFE_DISJOINT |

# 8. Anti-drift / overlap
Re-ground parent/main. UNKNOWN or BLOCKED_ACTIVE_SIBLING receives no write authority. Oracle/tolerance authority stays in parent.
'''

CHILD_HEADER = r'''ISSUE_ROLE: WORK_PACKAGE
PROGRAM_ID: PGM-AA-LAFEA
PARENT_WORK_ITEM_KEY: github:reallaksh19/Advanced_Analysis#100
WORK_PACKAGE_ID: WP-001
PARTITION_KEY: PGM-AA-LAFEA/WP-001
PREDECESSOR_WORK_ITEM_KEY: NONE
REVISION_SEQUENCE: 0
INHERITED_PROGRAM_BASIS_REVISION: PB-0001
INHERITED_INPUT_SET_ID: PGM-AA-LAFEA-INPUTS-v1
INHERITED_BENCHMARK_SET_ID: PGM-AA-LAFEA-BENCH-v1
INHERITED_VALIDATION_SET_ID: PGM-AA-LAFEA-VALID-v1
INHERITED_ROADMAP_SET_ID: PGM-AA-LAFEA-ROADMAP-v1
PARENT_TASK_ROWS: TASK-001
USES_INPUT_ROWS: INPUT-001
USES_BENCHMARK_ROWS: BM-001
USES_VALIDATION_ROWS: VAL-001
OVERLAP_CLASSIFICATION: SAFE_DISJOINT
OWNED_AUTHORITY_DOMAINS: route-orchestration
OWNED_PATHS_OR_COMPONENTS: src/route/**
READ_DEPENDENCIES: input/model.json
PROTECTED_SIBLING_DOMAINS: solver-formulation
DEPENDENCY_PREDECESSORS: NONE
'''


def run(text):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "issue.md"
        p.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True, text=True)


def expect(name, text, expected):
    r = run(text)
    ok = r.returncode == expected
    print(("PASS" if ok else "FAIL") + ": " + name)
    if not ok:
        print(r.stdout + r.stderr)
    return ok


def main():
    ok = True
    ok &= expect("strong single numerical workorder", BASE, 0)
    ok &= expect("strong program root", PROGRAM, 0)
    ok &= expect("strong work-package child", CHILD_HEADER + "\n" + BASE, 0)
    ok &= expect("program missing common validation set rejected", PROGRAM.replace("COMMON_VALIDATION_SET_ID: PGM-AA-LAFEA-VALID-v1\n", ""), 1)
    ok &= expect("child missing inherited benchmark set rejected", (CHILD_HEADER + "\n" + BASE).replace("INHERITED_BENCHMARK_SET_ID: PGM-AA-LAFEA-BENCH-v1\n", ""), 1)
    ok &= expect("child unknown overlap is structurally recorded", (CHILD_HEADER + "\n" + BASE).replace("OVERLAP_CLASSIFICATION: SAFE_DISJOINT", "OVERLAP_CLASSIFICATION: UNKNOWN"), 0)
    ok &= expect("child invalid overlap value rejected", (CHILD_HEADER + "\n" + BASE).replace("OVERLAP_CLASSIFICATION: SAFE_DISJOINT", "OVERLAP_CLASSIFICATION: MAYBE"), 1)
    revision = (CHILD_HEADER + "\n" + BASE).replace("ISSUE_ROLE: WORK_PACKAGE", "ISSUE_ROLE: REVISION").replace("PREDECESSOR_WORK_ITEM_KEY: NONE", "PREDECESSOR_WORK_ITEM_KEY: github:reallaksh19/Advanced_Analysis#101").replace("REVISION_SEQUENCE: 0", "REVISION_SEQUENCE: 1")
    ok &= expect("strong revision child", revision, 0)
    ok &= expect("revision without predecessor rejected", revision.replace("PREDECESSOR_WORK_ITEM_KEY: github:reallaksh19/Advanced_Analysis#101", "PREDECESSOR_WORK_ITEM_KEY: NONE"), 1)
    ok &= expect("textbook question rejected", BASE.replace("Take `fixtures/case.json` and trace the real case through `normalizeCase()`, `bindCase()`, `runCase()` and result publication. Tell me which current case/source IDs should survive each boundary, what exact retained object the solver consumes, and what single mismatch would falsify your trace before you propose any code change.", "Explain the architecture."), 1)
    ok &= expect("missing input ledger rejected", BASE.replace("INPUT-001", "SOURCE-A"), 1)
    ok &= expect("missing benchmark row rejected", BASE.replace("BM-001", "BENCH-A").replace("BM-002", "BENCH-B"), 1)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
