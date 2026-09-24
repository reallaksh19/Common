---
name: engineering-github-issue-authoring
description: Create implementation-grade GitHub engineering issues from live repository truth. Supports a durable parent programme specification, Owner-authorized amendment chronology, a dedicated non-authoritative [Relay Handover] operational ledger, bounded child implementation issues, parallel-focused issues, revision/integration issues, explicit producer-consumer contracts, falsifiers, exact evidence, and V3.1 recorder-first interoperability without engineering permission gates.
---

# Engineering GitHub Issue Authoring

## 1. Purpose

Turn an Owner request into a durable programme specification and bounded engineering issue set that survives multiple agents, revisions and session loss without losing human intent, source truth, ownership, producer-consumer relationships, evidence, negative knowledge or current operational context.

Reference quality: `reallaksh19/Advanced_Analysis#1371` for engineering depth and `XML_Compare_Utilities#980` for reuse/ownership clarity. Reuse their durable engineering intelligence, not their qualification or blocking machinery.

This skill interoperates with **Engineering Relay V3.1 only**. V3.1 records/reconstructs reality; it does not grant engineering permission. Do not use V3 or V2.5 for live issue topology, gating, takeover, recovery, status, handover or Owner-command semantics.

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
live Common engineering-pr-delivery-v3.1 when Relay context is useful; never V3 or V2.5 for current semantics
```

Reference issues are depth/style examples, not automatically current engineering authority.

## 4. Classify issue topology first

Record internally:

```text
ISSUE_TOPOLOGY: SINGLE_ISSUE | PROGRAM_ISSUE_SET
CHILD_PROFILE: WORK_PACKAGE | PARALLEL_FOCUSED | REVISION | INTEGRATION | RELAY_HANDOVER
```

Use `PROGRAM_ISSUE_SET` when the work has multiple meaningful workstreams/agents, shared source truth, producer-consumer relationships, integration work, or a durable programme outcome that must survive several PRs.

Use `PARALLEL_FOCUSED` for bounded independent work such as a falsifier, stale expectation, source-derived oracle correction, guardrail debt or focused integration finding. Do not inflate those issues into heavyweight work packs.

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
  = governing human/programme contract
  + durable Programme Specification

  ├─ [Relay Handover] child
  │    = current operational ledger / reconstruction index
  │
  ├─ WORK_PACKAGE or PARALLEL_FOCUSED child
  ├─ WORK_PACKAGE or PARALLEL_FOCUSED child
  ├─ REVISION child when completed work is materially revised
  └─ INTEGRATION/VALIDATION child when cross-workstream closure is required
```

Owner-authorized comments/amendments on the parent preserve semantic changes, transfers, decisions and evidence chronology. The parent should maintain a compact effective-amendment index so a coordinator does not need to replay all comments to reconstruct current programme meaning.

### Parent/program issue

Use `references/program-issue-template.md`.

The parent is the durable **Programme Specification + Coordination Record** and owns stable programme semantics:

```text
TASK-### original Owner requirements
RM-###   Owner/other roadmap bindings
INPUT-### common input/source authority
BM-###    common benchmark/oracle authority
VAL-###   common validation criteria
workstream ownership registry
producer/consumer output contracts
dependency contracts expressed as required production outputs
programme exclusions / invariants / exit criteria
effective Owner/programme amendment index
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

Each child is one bounded engineering responsibility with explicit ownership boundary, canonical inputs, producer/consumer contract, real production dependencies, falsifier, success oracle, implementation plan and expected handoff. A write fence is a conflict-avoidance/ownership boundary, not execution permission. Use `references/parallel-focused-issue-template.md` for small parallel workstreams.

### Revision child

A later material revision of a completed/frozen child gets a new `REVISION` issue linked to the predecessor and carrying the same `PARTITION_KEY` plus `REVISION_SEQUENCE`.

Do **not** create a new issue merely because the current agent is replaced while an unfinished child remains active. That is a V3.1 takeover on the same child/chain.

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

## 8. Ownership / overlap observation before child creation

Every child should state:

```text
OWNED_RESPONSIBILITY
OWNED_PATHS_OR_COMPONENTS where useful
READ_DEPENDENCIES
NEIGHBOURING_OWNERS
POTENTIAL_SHARED_SURFACES
```

Compare planned/active siblings and open PRs. Report:

```text
DISJOINT
MAY_CONFLICT
SHARED_INTEGRATION_SURFACE
UNKNOWN
```

This is coordination information, not a write-authority gate.

Read overlap is normal. Shared file edits may be handled through isolated branches/worktrees and integration. Escalate only when concurrent work would create a genuine semantic/interface conflict that cannot be safely reconciled locally.

## 9. Program creation sequence

When actual issue creation is requested:

1. Draft/audit the parent Programme Specification with stable `PROGRAM_ID`, basis revision, Owner outcome, canonical inputs, workstream registry, producer/consumer contracts, dependency contracts and programme exit criteria.
2. Create the parent issue.
3. Resolve the parent GitHub reference.
4. Create one dedicated child issue titled `[Relay Handover] <programme title>` using the coordinator's Handover template.
5. Create bounded child issues with `WORK_PACKAGE` or `PARALLEL_FOCUSED` profiles as appropriate.
6. Record each child in the parent workstream registry.
7. Put agent-authored implementation plans in the child issue/comment once available; plan absence is visible but never an execution gate.
8. Use PRs/commits/tests/artifacts as material truth and carry every nonterminal PR in the Handover ledger.
9. Maintain current operational context in the Handover child rather than rewriting the parent contract for ordinary churn.
10. Use Owner-authorized parent amendments for real semantic changes; update the effective-amendment index.
11. Use V3.1 only for recorder/reconstruction/reporting semantics when needed.

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
11. parent/common-set drift must be made visible and reconciled where it affects engineering meaning, but stale coordination metadata alone never blocks production;
12. active sibling overlap is reported and coordinated according to actual semantic/file conflict; it is not an automatic permission denial.

## 16. Five human-like implementation questions

For complex/engineering-critical issues, use five implementation questions when they materially improve problem understanding, falsification or exact reconstruction. They are reasoning aids, **not qualification or permission gates**. Focused parallel issues do not need five questions unless the task genuinely benefits from them.

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

## 17. Relay V3.1 interoperability — recorder-first

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

The parent programme and Handover issue are not execution-authority stores. V3.1 may record/reconstruct child material and handoffs, but its lease/custody/checkpoint/control data are advisory. Useful production evidence remains valid regardless of coordinator freshness.

## 18. Quality audit before issue creation

Verify at minimum:

```text
[ ] topology classified correctly
[ ] mission/original task not diluted
[ ] live creation-time SHA recorded
[ ] Owner/roadmap/source authority explicit
[ ] INPUT/BM/VAL/RM ledgers itemized where applicable
[ ] program common sets versioned for multi-agent work
[ ] child ownership, consumers, dependencies and potential overlap recorded
[ ] children inherit exact common-set IDs and parent TASK rows
[ ] production path traced
[ ] minimum-to-code skeleton exists where coding is expected
[ ] expected changed + protected domains named
[ ] PASS/FAIL/NOT_RUN concrete
[ ] independent oracle separated from product regression
[ ] negative tests/falsifiers exist
[ ] anti-drift/falsifiers and sibling-conflict observations explicit without becoming permission gates
[ ] revision links predecessor evidence when applicable
[ ] five implementation questions included only where they materially improve a complex/critical task
[ ] >=2 hand-calculation questions for numerical engineering
[ ] V3.1 linkage fields present for program children
```

Run `scripts/validate_issue_workorder.py` on drafts when a repository-capable environment is available. Structural PASS never substitutes for engineering review.

## 19. User-visible result

When actual creation is requested, return parent/child issue numbers and links, the partition/dependency plan, common input/benchmark/validation summary, overlap disposition, and the five implementation questions for the child being handed to an agent. Do not merge implementation PRs or mutate Owner roadmaps as a side effect of issue creation.
