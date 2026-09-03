---
name: engineering-github-issue-authoring
description: Create implementation-grade GitHub engineering issues from live repository truth. Use when the Owner asks to create/draft a GitHub issue, create detailed work instructions, or create an issue similar in depth to an existing issue. Produces code-ready technical guidance, source/input inventory, benchmark/oracle criteria, PASS/FAIL/NOT_RUN gates, anti-drift controls, and exactly five human-like implementation qualification questions that require live-repository evidence and hand calculation or exact reconstruction.
---

# Engineering GitHub Issue Authoring

## 1. Purpose

Turn an Owner request into a durable **implementation work order**, not a short ticket and not a design essay.

The issue must be specific enough that a competent implementation agent can start from it without reconstructing the Owner's intent from chat, while still requiring the implementing agent to re-ground the live repository before coding.

Reference quality: issues such as `reallaksh19/Advanced_Analysis#1371` demonstrate the desired depth: mission, creation-time ground truth, explicit authority/scope, Definition of Done, phased execution, concrete source/API guidance, code skeletons, PASS criteria, frozen benchmarks, anti-drift rules, exclusions, validation matrix, and takeover questions.

Do **not** copy product-specific facts from a reference issue into a new issue unless the live target repository independently supports them.

## 2. Trigger phrases

Use this skill for requests such as:

```text
create github issue similar to <issue-url>
create a detailed github issue for this work
create implementation work instruction in an issue
make an engineering issue with code snippets and tests
create issue and show me 5 implementation questions
```

If the Owner asks only for a draft, do not create the GitHub issue. Otherwise create it once the draft passes the issue-quality audit.

## 3. Target repository resolution

1. If the Owner names the target repository, use it.
2. If only a reference issue URL is supplied and the task clearly belongs to that repository, use the reference repository.
3. If task context points to another repository, use that repository and treat the supplied issue only as a structural/depth reference.
4. Do not silently create an issue in Common merely because this skill lives in Common.

Report the resolved target repository before mutation when there is genuine ambiguity.

## 4. Required grounding before drafting

Read enough live evidence to make the issue executable.

Minimum grounding:

```text
target repository AGENTS.md / local instructions
live target default-branch SHA
applicable Owner Roadmap(s)
reference issue(s), if supplied
relevant production/source files
relevant public APIs / orchestration boundaries
existing tests / validation scripts
input/source fixtures
benchmark/oracle definitions
open PRs/WIPs that may overlap the requested work
```

For engineering-critical repositories, also read the live Common `engineering-pr-delivery-v2` policy so the issue does not invent conflicting custody/merge/qualification rules.

Never rely on the reference issue's creation-time SHA as current truth.

## 5. Internal evidence pack before writing

Before composing prose, form an internal evidence pack containing:

```text
TARGET_REPO
ISSUE_CREATION_MAIN_SHA
OWNER_TASK
APPLICABLE_ROADMAPS
CURRENT_PRODUCTION_PATH
KNOWN_GAPS
INPUT_SOURCE_ROWS
BENCHMARK_ROWS
TEST_ENTRYPOINTS
EXPECTED_CHANGED_DOMAINS
PROTECTED_DOMAINS
OVERLAP_RISKS
REFERENCE_ISSUES
```

If a claimed implementation fact is not supported by the live repository, mark it `UNRESOLVED` or write it as a required investigation. Do not turn a placeholder into a fact.

## 6. Required issue architecture

Use `references/engineering-issue-template.md` as the base structure. Adapt section depth to the task, but preserve these semantic layers:

```text
MISSION
GROUND TRUTH AT ISSUE CREATION
OWNER INTENT / AUTHORITY / SCOPE
DEFINITION OF DONE
INPUT / SOURCE INVENTORY
CURRENT PRODUCTION OR REPOSITORY PATH
TECHNICAL IMPLEMENTATION INSTRUCTIONS
MINIMUM CODE SKELETON
PHASED EXECUTION / PATCH BOUNDARY
PASS / FAIL / NOT_RUN CRITERIA
BENCHMARK / ORACLE CRITERIA
ANTI-DRIFT / FAIL-CLOSED LOGIC
NEGATIVE TESTS / FALSIFIERS
EXPLICIT EXCLUSIONS
VALIDATION MATRIX
APPENDIX A — 5 IMPLEMENTATION QUESTIONS
```

A section may be combined with a neighboring section only if none of its custody information is lost.

## 7. Ground truth at issue creation

Always record the live default-branch SHA actually observed while creating the issue:

```text
Issue created against observed main:
<40-hex SHA>
```

Immediately state:

```text
Do not assume this SHA is still current when implementation begins. Re-ground first.
```

Also record material facts that explain the present implementation boundary: registered route, current limitation, active contract, missing seam, known open PR overlap, or equivalent repository truth.

Do not claim a limitation merely because an old roadmap or reference issue says so; confirm it against current production code where feasible.

## 8. Input/source inventory is mandatory

The issue must identify the actual inputs the implementation depends on.

Use stable IDs:

```text
INPUT-001
INPUT-002
...
```

For each input record:

```text
source path / URL / authority
what data is required
engineering or semantic meaning
current status: AVAILABLE | UNRESOLVED | NOT_APPLICABLE
whether it is mutable or frozen
what invalidates dependent artifacts
```

Distinguish:

```text
production input
sample/regression fixture
reference data
master data
Owner-provided data
external source
```

A sample fixture must never silently become production source authority.

## 9. Technical work instructions must be code-ready

Do not stop at architecture prose.

Provide enough concrete structure that an implementation agent can start coding after re-grounding:

- actual live file paths and function/class/API names where known;
- intended data/control flow;
- exact state/contract transitions;
- expected files/domains to change;
- protected files/domains that should not change;
- at least one code skeleton for the central path when coding is part of the task;
- concrete assertions or expected outputs adjacent to the skeleton.

### Code-skeleton rule

Use current public APIs when known. Where an exact signature still requires live resolution, use explicit placeholders such as:

```text
<resolve-current-public-api>
<existing-store-action>
<current-result-contract-field>
```

Never invent a second orchestration/store/solver/parser path merely to make the issue snippet compile.

Every structural snippet should carry this meaning:

```text
Use the existing live public API if names/signatures differ.
Do not duplicate architecture to satisfy this example.
```

The skeleton should be **minimum-to-code**, not a full speculative implementation. The implementing agent may improve the approach if live evidence supports a better solution inside the same Owner/roadmap/source boundary.

## 10. PASS/FAIL/NOT_RUN criteria

Acceptance criteria must be executable or objectively inspectable.

Prefer exact conditions:

```text
state == READY
count == 0
hash A == retained hash B
residual <= 1e-9
output row contains source/case/location custody
parser cursor ends at exact expected offset
workflow job executed non-zero steps
```

For every material gate distinguish:

```text
PASS
FAIL
NOT_RUN
NOT_APPLICABLE
```

If a test command is known, name it. If not known, instruct the agent to resolve the existing test entrypoint rather than inventing a command.

Include, where applicable:

```text
expected failing behavior before patch
expected PASS after patch
negative/falsifier case
neighbor regression that must remain unchanged
build/typecheck/import checks
end-to-end product route
```

Never describe a test as already PASS unless it was actually executed during issue creation and that fact matters to the issue.

## 11. Benchmark/oracle programme

Use stable benchmark IDs:

```text
BM-001
BM-002
...
```

Classify every benchmark:

```text
FROZEN_ANALYTICAL
AUTHORITATIVE_REFERENCE
EXPERIMENTAL
CROSS_SOLVER
FROZEN_EXTERNAL_DATA
PRODUCT_REGRESSION
```

For each benchmark state:

```text
source/definition path
input values
expected quantities
units/sign convention
acceptance tolerance
independence classification
current status: READY | PASS | FAIL | NOT_RUN | BLOCKED
```

Critical invariant:

```text
PRODUCT_REGRESSION != INDEPENDENT_ORACLE
```

Expected benchmark values must not be regenerated from the production output being validated.

If a new benchmark must be frozen, define/freeze the benchmark before using production observation to choose expected values or tolerances. If that cannot be done, mark the oracle `UNRESOLVED` and make it a prerequisite.

## 12. Anti-drift / fail-closed requirements

Every implementation-grade issue must contain explicit anti-drift logic.

At minimum:

1. re-ground live main before implementation;
2. compare issue-creation assumptions with current code;
3. preserve Owner Roadmap/source/oracle authority;
4. do not widen capability claims beyond proven behavior;
5. do not change tolerances/expected values merely to obtain PASS;
6. do not regenerate an independent oracle from current production output;
7. do not replace a governed public path with a direct core-call shortcut in an end-to-end issue;
8. do not manufacture hidden mock/default engineering inputs;
9. classify unavailable execution as `NOT_RUN`, not PASS;
10. if a code skeleton differs from live API, use the live existing API rather than creating duplicate architecture;
11. if current main proves the issue assumption obsolete, correct the implementation plan and record the evidence instead of implementing the stale assumption;
12. Owner roadmap mutation and merge authority remain separately Owner-controlled.

Where stale-state hazards matter, state the exact parent IDs/hashes/revisions that must agree and name a negative test that deliberately breaks one parent.

## 13. Explicit exclusions and protected domains

Write the non-goals explicitly.

Examples:

```text
NO new solver formulation
NO benchmark re-baselining
NO source schema widening
NO UI-derived engineering authority
NO workflow changes without authorization
NO roadmap mutation
NO release/merge without Owner authority
```

Use task-specific exclusions. Do not paste irrelevant exclusions from the reference issue.

## 14. Five human-like implementation questions

The issue ends with exactly five questions under:

```text
# Appendix A — implementation qualification
```

Read `references/implementation-question-standard.md` before generating them.

The questions are written as a senior engineer would ask another engineer before giving them the implementation baton.

They must test **implementation competence**, not textbook memory.

Required pattern:

```text
Q1 actual production trace using real object/case/file/function IDs
Q2 hand calculation or exact reconstruction using actual issue inputs
Q3 authority/stale-state/failure isolation with an explicit falsifier
Q4 independent benchmark/oracle reconstruction, preferably hand calculation
Q5 smallest coherent patch, before/after evidence, negative test, rollback and NO-PATCH case
```

For numerical engineering work, at least **two** of Q1-Q5 require real hand calculations from concrete numbers supplied by the issue/repository.

For non-numerical software work, use equivalent exact reconstruction: byte offsets, parser cursor arithmetic, hash/state derivation, deterministic transformation, protocol transition, database row evolution, or another check that cannot be answered by generic prose.

Never ask only:

```text
Explain the architecture.
What is a Jacobian?
Describe the benchmark.
Which file would you edit?
What tests would you run?
```

A strong question names the actual data and asks for a predicted value, boundary, or falsifier before the agent reads production output.

## 15. Reference issue handling

When the Owner says `similar to <issue-url>`:

1. read the reference issue completely enough to identify its structure, evidence style and depth;
2. optionally inspect important comments if they changed the issue's accepted basis;
3. extract reusable authoring patterns only;
4. re-ground the target repository independently;
5. preserve the requested depth while replacing stale/product-specific facts with live target evidence.

Reference issues are style/depth examples, not automatically authoritative engineering sources for the new issue.

## 16. Issue quality audit before creation

Before calling GitHub issue creation, verify:

```text
[ ] mission is implementation-specific
[ ] creation-time main SHA recorded
[ ] Owner/roadmap/source authority is explicit
[ ] original task is not diluted
[ ] input/source rows are itemized
[ ] current production/repository path is traced
[ ] code-ready skeleton exists where coding is expected
[ ] expected changed + protected domains are named
[ ] PASS/FAIL/NOT_RUN criteria are concrete
[ ] benchmark/oracle rows are classified
[ ] production regression is not mislabeled independent
[ ] oracle anti-circularity is explicit
[ ] stale/main drift behavior is explicit
[ ] negative tests/falsifiers exist
[ ] explicit exclusions exist
[ ] exactly five implementation questions exist
[ ] >=2 hand-calculation questions for numerical engineering work
[ ] questions require live-repository evidence
```

Use `scripts/validate_issue_workorder.py` on a draft file when a repository-capable environment is available. Structural PASS does not replace engineering review.

## 17. Creation and user-visible response

When the Owner requested actual creation:

1. perform the quality audit;
2. create the GitHub issue in the resolved target repository;
3. return the issue number/title/link;
4. summarize the key input sources and benchmark programme;
5. show the same five implementation questions exactly as posted in the issue.

Do not merge implementation PRs or mutate Owner roadmaps as a side effect of creating an issue.
