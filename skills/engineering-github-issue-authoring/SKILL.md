---
name: engineering-github-issue-authoring
description: Create implementation-grade GitHub engineering issues from live repository truth. Supports single issues and multi-agent program issue sets with an immutable parent Owner/common-custody contract, exclusive work-package child issues, revision child issues, relay-chain interoperability, overlap prevention, source/input and benchmark/validation custody, anti-drift gates, code-ready guidance, and five human-like implementation qualification questions requiring hand calculation or exact reconstruction.
---

# Engineering GitHub Issue Authoring

## 1. Purpose

Turn an Owner request into a durable implementation work order that survives multiple agents and revisions without losing original intent, common inputs, benchmark/oracle authority, validation criteria, roadmap bindings, or overlap ownership.

Reference quality: `reallaksh19/Advanced_Analysis#1371` for depth and implementation specificity. Do not copy its product-specific facts into another task unless the live target repository independently supports them.

This skill interoperates with `engineering-pr-delivery-v2`. Authoring defines the durable GitHub work topology; relay-v2 governs execution/takeover/custody of each material work item.

## 2. Trigger phrases

Use for requests such as:

```text
create github issue similar to <issue-url>
create detailed implementation issue
create issue with technical instructions/code snippets/tests
create issue with inputs/benchmark/anti-drift
split this complicated task into parent/sub-issues for multiple agents
```

If the Owner asks only for a draft, do not create issues.

## 3. Resolve target repository and live authority

Before drafting, read enough live evidence to make the issue executable:

```text
target AGENTS.md / local instructions
live target default-branch SHA
applicable Owner Roadmap(s)
reference issue(s), if supplied
relevant production/source files
public APIs / orchestration boundaries
existing tests / validation scripts
input/source fixtures
benchmark/oracle definitions
open PRs/WIPs/claims that can overlap
live Common engineering-pr-delivery-v2 for engineering-critical issue work
```

Reference issues are depth/style examples, not automatically current engineering authority.

## 4. Classify issue topology first

Record internally:

```text
ISSUE_TOPOLOGY: SINGLE_ISSUE | PROGRAM_ISSUE_SET
```

Use `PROGRAM_ISSUE_SET` when the work is expected to require multiple coherent PRs/agents/revisions, independent authority domains, shared input/benchmark/validation custody, integration work, or material sibling-overlap control. Owner-requested parent/sub-issues is an explicit program trigger.

Do not split a naturally atomic task just to increase issue count.

Read `references/multi-agent-program-issues.md` for program topology.

## 5. Single-issue architecture

For a bounded single issue, use `references/engineering-issue-template.md` and preserve these layers:

```text
MISSION
GROUND TRUTH AT ISSUE CREATION
OWNER INTENT / ROADMAP / AUTHORITY / SCOPE
DEFINITION OF DONE
INPUT / SOURCE INVENTORY
CURRENT PRODUCTION/REPOSITORY PATH
TECHNICAL IMPLEMENTATION INSTRUCTIONS
MINIMUM-TO-CODE SKELETON
EXPECTED CHANGED + PROTECTED DOMAINS
PASS / FAIL / NOT_RUN CRITERIA
BENCHMARK / ORACLE PROGRAMME
ANTI-DRIFT / FAIL-CLOSED LOGIC
NEGATIVE TESTS / FALSIFIERS
EXPLICIT EXCLUSIONS
VALIDATION MATRIX
APPENDIX A — FIVE IMPLEMENTATION QUESTIONS
```

## 6. Program issue-set architecture

For complicated multi-agent work, use:

```text
PARENT / PROGRAM ISSUE
  ├─ WORK_PACKAGE child WP-001
  ├─ WORK_PACKAGE child WP-002
  ├─ WORK_PACKAGE child WP-003
  ├─ REVISION child of completed WP-001 when later material revision is required
  └─ INTEGRATION/VALIDATION child when cross-package closure is required
```

### Parent/program issue

Use `references/program-issue-template.md`.

The parent is the durable Owner/common-custody contract and owns stable ledgers:

```text
TASK-### original Owner requirements
RM-###   Owner/other roadmap bindings
INPUT-### common input/source authority
BM-###    common benchmark/oracle authority
VAL-###   common validation criteria
work-package partition/dependency registry
program-level exclusions / Definition of Done / integration gates
```

Version common sets explicitly:

```text
PROGRAM_BASIS_REVISION
COMMON_INPUT_SET_ID
COMMON_BENCHMARK_SET_ID
COMMON_VALIDATION_SET_ID
COMMON_ROADMAP_SET_ID
```

Children may reference these rows; they may not silently redefine, omit, re-baseline, or weaken them.

### Work-package child

Use `references/work-package-issue-template.md`.

Each child is one bounded material-write partition with its own GitHub `WORK_ITEM_KEY`, relay-v2 chain, exclusive current agent instance, explicit owned domains/paths, dependencies, and inherited common-set IDs.

### Revision child

A later material revision of a completed/frozen child gets a new `REVISION` issue linked to the predecessor and carrying the same `PARTITION_KEY` plus `REVISION_SEQUENCE`.

Do **not** create a new issue merely because the current agent is replaced while an unfinished child remains active. That is a relay-v2 takeover on the same child/chain.

## 7. Parent-child inheritance contract

Every child/revision records:

```text
ISSUE_ROLE: WORK_PACKAGE | REVISION
PROGRAM_ID:
PARENT_WORK_ITEM_KEY:
WORK_PACKAGE_ID:
PARTITION_KEY:
PREDECESSOR_WORK_ITEM_KEY:
REVISION_SEQUENCE:
INHERITED_PROGRAM_BASIS_REVISION:
INHERITED_INPUT_SET_ID:
INHERITED_BENCHMARK_SET_ID:
INHERITED_VALIDATION_SET_ID:
INHERITED_ROADMAP_SET_ID:
PARENT_TASK_ROWS:
USES_INPUT_ROWS:
USES_BENCHMARK_ROWS:
USES_VALIDATION_ROWS:
```

A child can add local rows for genuinely child-specific data, but parent common rows retain their IDs/meaning/authority. If parent common authority is wrong/stale, stop and revise the parent program basis rather than fixing it locally.

## 8. Partition and overlap gate before child creation

Every work package must state:

```text
OWNED_AUTHORITY_DOMAINS
OWNED_PATHS_OR_COMPONENTS
READ_DEPENDENCIES
PROTECTED_SIBLING_DOMAINS
DEPENDENCY_PREDECESSORS
```

Compare against planned/active sibling issues and open PR/WIP claims. Classify:

```text
SAFE_DISJOINT
SAFE_SERIALIZED
COORDINATION_REQUIRED
BLOCKED_ACTIVE_SIBLING
UNKNOWN
```

`BLOCKED_ACTIVE_SIBLING` or `UNKNOWN` must not be authored as immediately write-ready.

Read overlap is not write ownership. Shared writes require one explicit integration/serialization owner.

## 9. Two-pass program creation

When actual issue creation is requested:

1. Draft/audit the parent and partition registry with stable `PROGRAM_ID`, `WP-*`, `TASK-*`, `INPUT-*`, `BM-*`, `VAL-*`, `RM-*` IDs.
2. Create the parent issue.
3. Resolve `PROGRAM_WORK_ITEM_KEY = github:<owner>/<repo>#<parent>`.
4. Create each child issue with exact parent key/common-set inheritance and bounded partition.
5. Where native GitHub sub-issue linking is available through the execution environment, register it; otherwise keep explicit parent/child links and parent work-package registry.
6. Publish/update a mutable parent program-status projection containing child issue numbers, chain/PR state, dependencies and overlap status. Do not rewrite the original Owner contract for operational churn.
7. Do not activate a blocked-overlap child.

## 10. Ground truth at issue creation

Every issue records the live default-branch SHA actually observed:

```text
Issue created against observed main:
<40-hex SHA>

Do not assume this SHA is still current when implementation begins. Re-ground first.
```

For children, also record current parent program basis/common-set IDs and active sibling/PR state.

## 11. Input/source inventory

Use stable `INPUT-###` IDs and state source/path/authority, required data, semantic meaning, status, mutability/frozen state, and invalidation rule.

Distinguish production input, sample/regression fixture, master/reference data, Owner data, and external source. A sample fixture must not silently become production authority.

In a program, common inputs live in the parent; children reference row IDs instead of paraphrasing them.

## 12. Technical instructions must be minimum-to-code

Provide current live paths/APIs where known, intended data/control flow, state/contract transitions, expected changed/protected files, one central code skeleton when coding is expected, and concrete adjacent assertions.

If an exact live API requires resolution, use explicit placeholders such as:

```text
<resolve-current-public-api>
<existing-store-action>
<current-result-contract-field>
```

Never create duplicate stores/orchestrators/solvers/parsers merely to make the issue snippet compile. If live names differ, use the existing live public path.

## 13. PASS / FAIL / NOT_RUN criteria

Acceptance criteria must be executable or objectively inspectable. Preserve:

```text
PASS
FAIL
NOT_RUN
NOT_APPLICABLE
```

Prefer exact assertions/commands/states/hashes/residuals/offsets. Include expected failing behavior before patch, expected PASS after patch, a negative/falsifier case, neighboring regression and end-to-end route where applicable.

In a program, `VAL-###` common gates are defined at parent level and children produce evidence against them without rewriting the requirement.

## 14. Benchmark/oracle programme

Use stable `BM-###` IDs and classify:

```text
FROZEN_ANALYTICAL
AUTHORITATIVE_REFERENCE
EXPERIMENTAL
CROSS_SOLVER
FROZEN_EXTERNAL_DATA
PRODUCT_REGRESSION
```

Record source, inputs, expected quantities, units/sign, tolerance, independence and status.

Invariant:

```text
PRODUCT_REGRESSION != INDEPENDENT_ORACLE
```

Expected values/tolerances must not be chosen from the production output being validated. Common program benchmarks belong to the parent and are inherited by ID.

## 15. Anti-drift / fail-closed rules

Every issue requires:

1. re-ground live main before implementation;
2. re-read current Owner instructions/roadmaps;
3. compare issue assumptions with current code;
4. preserve source/oracle/roadmap authority;
5. never weaken tolerances or regenerate oracle values to obtain PASS;
6. never promote `NOT_RUN` to PASS;
7. never bypass a governed public route with a direct core call for an end-to-end task;
8. never invent hidden engineering defaults;
9. if an issue assumption is obsolete, prove it and correct the plan within Owner intent instead of implementing stale work;
10. Owner roadmap mutation and merge remain separately Owner-controlled;
11. for program children, parent basis/common-set drift blocks further material mutation until reconciled;
12. active sibling partition/write overlap blocks material authority.

## 16. Five human-like implementation questions

Every material implementation/revision child and every single implementation issue ends with exactly five questions under `# Appendix A — implementation qualification`.

Read `references/implementation-question-standard.md`.

Pattern:

```text
Q1 actual production trace using real objects/files/functions/IDs
Q2 hand calculation or exact deterministic reconstruction from actual issue values
Q3 stale/authority/failure isolation with explicit falsifier
Q4 independent benchmark/oracle reconstruction, preferably hand calculation
Q5 smallest coherent patch + before/after evidence + negative test + rollback/falsifier + NO-PATCH case
```

For numerical engineering, at least two questions require real hand calculations using concrete numbers supplied by the issue/repository. For software engineering, use exact byte/pointer/cursor/hash/state reconstruction rather than generic prose.

The parent program issue may carry Owner qualification baseline questions, but child questions must be tailored to the child partition and may not downgrade inherited Owner technical obligations.

## 17. Relay-v2 interoperability

For each child/revision issue, relay state binds:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE
WORK_ITEM_KEY: github:<owner>/<repo>#<child>
WORK_ITEM_MODE: EXCLUSIVE
PROGRAM_ID:
PROGRAM_WORK_ITEM_KEY: github:<owner>/<repo>#<parent>
ISSUE_ROLE:
WORK_PACKAGE_ID:
PARTITION_KEY:
PREDECESSOR_WORK_ITEM_KEY:
INHERITED_PROGRAM_BASIS_REVISION:
INHERITED_INPUT_SET_ID:
INHERITED_BENCHMARK_SET_ID:
INHERITED_VALIDATION_SET_ID:
INHERITED_ROADMAP_SET_ID:
```

The parent program is not a shared multi-writer production chain. Each material child owns its own canonical chain. Takeover of unfinished child stays on that chain; revision of frozen work uses a revision child/new chain.

## 18. Quality audit before issue creation

Verify at minimum:

```text
[ ] topology classified correctly
[ ] mission/original task not diluted
[ ] live creation-time SHA recorded
[ ] Owner/roadmap/source authority explicit
[ ] INPUT/BM/VAL/RM ledgers itemized where applicable
[ ] program common sets versioned for multi-agent work
[ ] child partitions/dependencies/overlap classified
[ ] children inherit exact common-set IDs and parent TASK rows
[ ] production path traced
[ ] minimum-to-code skeleton exists where coding is expected
[ ] expected changed + protected domains named
[ ] PASS/FAIL/NOT_RUN concrete
[ ] independent oracle separated from product regression
[ ] negative tests/falsifiers exist
[ ] anti-drift and sibling-overlap gates explicit
[ ] revision links predecessor evidence when applicable
[ ] exactly five implementation questions for material child/single issue
[ ] >=2 hand-calculation questions for numerical engineering
[ ] relay-v2 linkage fields present for program children
```

Run `scripts/validate_issue_workorder.py` on drafts when a repository-capable environment is available. Structural PASS never substitutes for engineering review.

## 19. User-visible result

When actual creation is requested, return parent/child issue numbers and links, the partition/dependency plan, common input/benchmark/validation summary, overlap disposition, and the five implementation questions for the child being handed to an agent. Do not merge implementation PRs or mutate Owner roadmaps as a side effect of issue creation.
