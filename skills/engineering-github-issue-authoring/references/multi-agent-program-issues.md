# Multi-Agent Program Issues — parent, work-package and revision topology

Use this model when the Owner's task is too large/risky for one bounded implementation issue or is expected to require multiple implementation/revision agents.

## 1. Topology decision

Classify the requested work before issue creation:

```text
ISSUE_TOPOLOGY: SINGLE_ISSUE | PROGRAM_ISSUE_SET
```

Choose `PROGRAM_ISSUE_SET` when one or more are true:

- more than one coherent PR/material phase is expected;
- multiple agents/revision passes are expected;
- two or more engineering authority domains can progress independently;
- common inputs/benchmarks/validation must be reused by several work packages;
- overlap between agents is a material risk;
- an integration/review agent must consume outputs from earlier agents;
- Owner explicitly asks for parent/sub-issues or multi-agent execution.

Do not split a naturally atomic change merely to create more issues.

## 2. Parent/program issue — durable Owner contract

The parent issue is the program contract, not an agent's local implementation note.

Header:

```text
ISSUE_ROLE: PROGRAM_ROOT
PROGRAM_ID: PGM-<repo>-<short-task>
PROGRAM_WORK_ITEM_KEY: SELF_AFTER_CREATION | github:<owner>/<repo>#<parent>
PROGRAM_BASIS_REVISION: PB-0001
COMMON_INPUT_SET_ID: <PROGRAM_ID>-INPUTS-v1
COMMON_BENCHMARK_SET_ID: <PROGRAM_ID>-BENCH-v1
COMMON_VALIDATION_SET_ID: <PROGRAM_ID>-VALID-v1
COMMON_ROADMAP_SET_ID: <PROGRAM_ID>-ROADMAP-v1
```

The parent issue owns the no-dilution common state:

```text
Original Owner task / TASK-### ledger
Owner Roadmap bindings / RM-###
Common inputs / INPUT-###
Common benchmark-oracle programme / BM-###
Common validation gates / VAL-###
Global exclusions/protected domains
Program-level Definition of Done
Work-package partition/dependency registry
Program-level integration/closure gates
Owner qualification baseline when supplied
```

The parent issue must not be rewritten by children. A material Owner change creates a successor program-basis revision; preserve the previous basis for provenance.

## 3. Work-package child issue — one exclusive implementation partition

Each independently executable work package gets one child issue.

Required child header:

```text
ISSUE_ROLE: WORK_PACKAGE
PROGRAM_ID: <PROGRAM_ID>
PARENT_WORK_ITEM_KEY: github:<owner>/<repo>#<parent>
WORK_PACKAGE_ID: WP-001
WORK_PACKAGE_RELATION: IMPLEMENTATION | VALIDATION | INTEGRATION
PARTITION_KEY: <PROGRAM_ID>/WP-001
PREDECESSOR_WORK_ITEM_KEY: NONE
REVISION_SEQUENCE: 0

INHERITED_PROGRAM_BASIS_REVISION: PB-0001
INHERITED_INPUT_SET_ID: <exact parent set ID>
INHERITED_BENCHMARK_SET_ID: <exact parent set ID>
INHERITED_VALIDATION_SET_ID: <exact parent set ID>
INHERITED_ROADMAP_SET_ID: <exact parent set ID>
PARENT_TASK_ROWS: TASK-001,TASK-004
USES_INPUT_ROWS: INPUT-001,INPUT-003
USES_BENCHMARK_ROWS: BM-001,BM-004
USES_VALIDATION_ROWS: VAL-002,VAL-005
```

A child may add child-specific inputs/benchmarks/tests with new local IDs, but it must not redefine inherited parent rows. If a parent row is wrong or obsolete, block and propose a parent basis revision.

Every active child maps to exactly one canonical relay chain and one exclusive current agent instance. A child is the normal material-write unit.

## 4. Revision child issue — later agent materially revises completed work

Do not reopen/rewrite a frozen completed work package to hide revision history. Create a revision child when a later agent materially changes an accepted/completed work-package result.

Required revision header:

```text
ISSUE_ROLE: REVISION
PROGRAM_ID: <PROGRAM_ID>
PARENT_WORK_ITEM_KEY: github:<owner>/<repo>#<parent>
WORK_PACKAGE_ID: WP-001
PARTITION_KEY: <PROGRAM_ID>/WP-001
PREDECESSOR_WORK_ITEM_KEY: github:<owner>/<repo>#<original-child>
REVISION_SEQUENCE: 1
REVISION_REASON: <defect / failed benchmark / Owner change / integration finding>
PREDECESSOR_ACCEPTED_ENDPOINT: <EP-ID>
PREDECESSOR_PR: #<number>
```

The revision inherits the same parent common-set IDs unless the Owner/program basis itself changed. It must state exactly what predecessor evidence is being revised and what remains valid.

A revision on the same `PARTITION_KEY` may start only when the predecessor material writer is terminal/frozen, unless the Owner explicitly authorizes a partitioned concurrent repair.

## 5. Agent takeover is not automatically a new issue

If an agent disappears or is replaced while a child is still unfinished:

```text
same child issue
same WORK_ITEM_KEY
same canonical relay chain
new AGENT_INSTANCE_ID
qualification-first takeover
```

Do **not** create a duplicate child merely because the agent changed. The relay endpoint/Issue Active Handover preserves agent-to-agent history.

Create a new `REVISION` child only for a material revision of a completed/frozen predecessor or when the Owner explicitly requests a separately reviewable revision package.

## 6. Parent work-package registry

The parent contains a partition/dependency plan with stable IDs:

| WP | Relation | Child | Scope / deliverable | Owned authority/paths | Depends on | Common rows used | Status | Chain / PR | Overlap disposition |
|---|---|---|---|---|---|---|---|---|---|
| WP-001 | IMPLEMENTATION | `<created #>` | ... | ... | NONE | INPUT-001; BM-001; VAL-001 | PLANNED | PENDING | SAFE |
| WP-002 | VALIDATION | `<created #>` | ... | ... | WP-001 | ... | BLOCKED_DEPENDENCY | PENDING | SAFE |

Status vocabulary:

```text
PLANNED
READY
ACTIVE
BLOCKED_DEPENDENCY
BLOCKED_OVERLAP
HANDOVER_READY
COMPLETE
SUPERSEDED
```

The parent issue body is the immutable baseline. Maintain current program/child status in a mutable program-status comment or repository program-state artifact; do not repeatedly rewrite the Owner contract to reflect operational churn.

## 7. Overlap prevention

Partition before child creation. Every work package states:

```text
OWNED_AUTHORITY_DOMAINS:
OWNED_PATHS_OR_COMPONENTS:
READ_DEPENDENCIES:
PROTECTED_SIBLING_DOMAINS:
DEPENDENCY_PREDECESSORS:
```

Before creating/activating a child:

1. compare `PARTITION_KEY` against active siblings;
2. compare owned authority domains;
3. compare expected changed paths/components;
4. inspect open PR/WIP claims in the same parent program;
5. classify overlap:

```text
SAFE_DISJOINT
SAFE_SERIALIZED
COORDINATION_REQUIRED
BLOCKED_ACTIVE_SIBLING
UNKNOWN
```

`BLOCKED_ACTIVE_SIBLING` or `UNKNOWN` does not receive material write authority.

Two children may read the same common input/benchmark files. Read overlap is not write ownership. Shared writes require explicit integration/serialization ownership.

## 8. Common-set inheritance and anti-dilution

The parent is the single common source for:

```text
COMMON_INPUT_SET_ID
COMMON_BENCHMARK_SET_ID
COMMON_VALIDATION_SET_ID
COMMON_ROADMAP_SET_ID
```

Children reference row IDs; they do not paraphrase them into new authority.

Example:

```text
Parent:
INPUT-003 = material master v7 @ <path/blob>
BM-002    = frozen Kirsch oracle @ <path/blob>
VAL-004   = fixed-probe error <= 2.0 %

Child WP-003:
USES_INPUT_ROWS: INPUT-003
USES_BENCHMARK_ROWS: BM-002
USES_VALIDATION_ROWS: VAL-004
```

Forbidden child behavior:

```text
rename INPUT-003 and change its meaning
replace BM-002 with production regression
relax VAL-004 locally
switch Owner Roadmap revision silently
omit parent task rows that the child was allocated
```

If a common row changes legitimately, revise the parent program basis and issue a new set ID/version. All active children must re-ground that drift before further material mutation.

## 9. Relay integration contract

This authoring topology is designed to map directly to `engineering-pr-delivery-v2`.

For each child/revision issue:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE
WORK_ITEM_KEY: github:<owner>/<repo>#<child>
WORK_ITEM_MODE: EXCLUSIVE
PROGRAM_ID: <PROGRAM_ID>
PROGRAM_WORK_ITEM_KEY: github:<owner>/<repo>#<parent>
ISSUE_ROLE: WORK_PACKAGE | REVISION
WORK_PACKAGE_ID: WP-001
PARTITION_KEY: <PROGRAM_ID>/WP-001
PREDECESSOR_WORK_ITEM_KEY: NONE | github:<owner>/<repo>#<predecessor>
INHERITED_PROGRAM_BASIS_REVISION: PB-0001
INHERITED_INPUT_SET_ID: ...
INHERITED_BENCHMARK_SET_ID: ...
INHERITED_VALIDATION_SET_ID: ...
INHERITED_ROADMAP_SET_ID: ...
```

The child relay Issue Basis captures these values. They are checked again before write authority.

The parent program issue is not a shared multi-writer engineering chain. Each material child has its own chain. An optional program/integration chain may aggregate status/evidence but must not write inside a child's active exclusive partition.

## 10. Program closure

The parent program closes only when:

- every required `TASK-###` row is satisfied or Owner-disposed;
- required work packages/revisions are COMPLETE;
- no active overlap/blocker remains;
- common input/benchmark/validation/roadmap sets are current;
- child PASS/FAIL/NOT_RUN evidence has been reconciled without promotion;
- integration child/gate, if required, passes;
- Owner merge/release authority is satisfied separately.

A child PR merge is not by itself evidence that the parent program is complete.
