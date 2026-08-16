# Prompt Creation Schema v1

**File:** `skills/Prompt/Promptcreationschemav1.md`  
**Schema ID:** `PROMPT-CREATION-SCHEMA-V1`  
**Purpose:** Create GitHub issues/prompts that route work toward the required expertise, constrain execution, expose uncertainty, and make task drift detectable rather than merely discouraged.

---

## 1. Core design principle

A good issue is not primarily a description of what someone should remember.

It is an **execution contract** that answers, in machine-checkable form wherever possible:

```text
WHO must be capable of doing this?
WHAT is the one mission?
WHICH evidence is authoritative?
WHAT is explicitly in and out of scope?
WHAT must happen when evidence is missing or contradictory?
IN WHAT ORDER must the work proceed?
HOW will the repository prove the requested result and detect drift?
```

The minimum schema is:

```text
EXPERTISE GATE
      +
SINGLE MISSION
      +
SOURCE PRECEDENCE
      +
SCOPE LOCK
      +
FAIL-CLOSED ESCAPE
      +
EXECUTION ORDER
      +
MACHINE ACCEPTANCE TESTS
```

For high-consequence work, add:

```text
AUTHORITY BOUNDARY
STATE SEPARATION
BENCHMARK / ORACLE RULES
PROMOTION / RELEASE GATES
STOP CONDITIONS
RECOVERY / HANDOFF CONTRACT
```

The goal is not to make the issue longer. The goal is to remove discretionary decisions that the next agent does not need to make.

---

# 2. Issue classification block — always first

The first section of the issue must classify the assignment before giving implementation details.

Use:

```markdown
# TASK CLASSIFICATION — [EXPERT / SPECIALIST / STANDARD] ASSIGNMENT

This is not a generic [coding / documentation / UI / research] task.

Required disciplines:

- [discipline 1]
- [discipline 2]
- [discipline 3]

Consequence class:

- [LOW / MODERATE / HIGH / SAFETY-CRITICAL]

Working posture:

- SOURCE CONTROLLED
- FAIL CLOSED
- TRACEABILITY REQUIRED
- NO UNAUTHORIZED SCOPE EXPANSION
```

## 2.1 Expertise routing rule

Do not write only:

```text
Need an expert.
```

State the actual combination of expertise required.

Example:

```text
SENIOR DOMAIN ENGINEER
+ SOFTWARE ARCHITECT
+ QUALIFICATION / V&V ENGINEER
+ REPOSITORY GOVERNANCE SPECIALIST
```

The issue author should choose only the disciplines actually required.

## 2.2 Expertise gate must be evidence-backed

A questionnaire is useful only if it requires evidence from the current working system.

Avoid:

```text
Do you understand the authority boundary?
Explain the method.
What do you think the correct architecture is?
```

Prefer:

```text
Locate the current authority declaration.
State its value.
Provide the exact source file and current commit/blob.
Identify the test that would fail if it changed incorrectly.
```

The expertise gate should normally contain **5-8 high-signal questions**, not a long essay exam.

Template:

```markdown
## EXPERTISE GATE — NO MUTATION YET

Before changing any file, establish from current live evidence:

1. [critical fact / contract]
2. [authority state]
3. [active implementation seam]
4. [controlled source or benchmark]
5. [known exclusion / blocker]
6. [release or qualification command]
7. [current conflicting artifact, if any]

For every answer provide:

- VALUE
- SOURCE FILE / SYSTEM
- CURRENT COMMIT / REVISION / BLOB where applicable
- CONFIDENCE / STATUS

If a required answer cannot be established from controlled evidence:

`BLOCKED_SOURCE_UNRESOLVED`

Do not infer the missing answer.
```

### Expertise gate pass rule

A candidate has passed the gate only when the answers demonstrate **repository-/system-specific understanding**, not generic subject knowledge.

A plausible textual answer without evidence is not a pass.

---

# 3. Single Mission

Every issue must have one sentence that defines the mission.

Format:

```markdown
# SINGLE MISSION

Your assignment has exactly one objective:

> [one bounded outcome that can be independently verified]
```

Good mission:

```text
Make capability state have one machine-readable source of truth and make CI fail when any projection contradicts it.
```

Poor mission:

```text
Improve the module, fix remaining issues, clean up the UI, add tests and make it production ready.
```

The poor version contains many undefined decisions and invites drift.

## 3.1 Mission exclusions

Immediately state what the mission is **not**.

Template:

```markdown
You are not assigned to:

- [out-of-scope item]
- [authority change]
- [method change]
- [unrelated refactor]
- [release/merge action]

If discovered, record it as `OUT_OF_SCOPE_FINDING`; do not absorb it into this issue.
```

This is important because many agents drift while trying to be helpful.

---

# 4. Source Precedence

An issue must define what wins when artifacts disagree.

Do not allow the agent to reconcile contradictions by intuition.

Generic precedence template:

```markdown
# SOURCE PRECEDENCE

When artifacts disagree, use this precedence unless this issue explicitly defines a domain-specific override:

1. current executable / operational truth
2. current registered or machine-readable contract
3. controlled specification / adopted method
4. controlled benchmark / source fixture
5. qualification / validation evidence
6. current scoped governance documents
7. merged change records
8. active open PR proposals
9. GitHub issues / planning documents
10. historical workreports / comments / conversations

A lower-precedence artifact may reveal a defect in a higher-precedence artifact, but it may not silently override it.

Every contradiction becomes a `DRIFT_FINDING` before modification.
```

## 4.1 Domain-specific precedence

If engineering, legal, financial, medical, safety, standards, or other controlled-source work is involved, replace the generic list with the actual authority chain.

Examples may include:

```text
adopted standard
licensed source edition
project specification
approved errata
controlled master data
validated implementation
```

Do not pretend GitHub chronology determines engineering authority.

---

# 5. Scope Lock

Scope must be enforceable at the file/action level where possible.

Primary rule:

> **Every proposed file change must identify the acceptance criterion that requires it. If no acceptance criterion requires the change, do not change the file.**

Template:

```markdown
# SCOPE LOCK

For every changed file, record:

- FILE
- ACCEPTANCE CRITERION REQUIRING CHANGE
- WHY THIS FILE IS THE MINIMUM CORRECT SEAM

If no acceptance criterion requires the change:

`DO NOT CHANGE THE FILE`

Forbidden unless explicitly required:

- while-I-am-here cleanup
- broad refactor
- dependency upgrade
- formatting sweep
- speculative abstraction
- unrelated test rewrite
- authority/lifecycle promotion
- workflow/CI modification
```

## 5.1 Allowed and forbidden path sets

For high-risk work, specify path contracts:

```yaml
scope:
  allowedPaths:
    - path/a/**
    - path/b/specific-file.js
  forbiddenPaths:
    - production-registry.js
    - .github/workflows/**
    - controlled-master-data/**
```

If actual work proves another file is necessary, the agent must first record:

```text
SCOPE_EXTENSION_REQUIRED
reason
acceptance criterion
risk
```

before changing it.

---

# 6. Fail-Closed Escape

The issue must give the agent a legitimate alternative to guessing.

Without this, uncertainty often becomes improvisation.

Template:

```markdown
# FAIL-CLOSED ESCAPE

When evidence is missing, contradictory, inaccessible, or outside assigned authority, do not invent a resolution.

Use one of:

- `BLOCKED_SOURCE_UNRESOLVED`
- `BLOCKED_SOURCE_CONFLICT`
- `BLOCKED_AUTHORITY_UNCLEAR`
- `BLOCKED_DEPENDENCY`
- `BLOCKED_VALIDATION_NOT_RUN`
- `BLOCKED_ENVIRONMENT`
- `OUT_OF_SCOPE_FINDING`
- `NOT_APPLICABLE`

A partial correct result with a precise blocker is preferred over a complete-looking result based on assumptions.
```

## 6.1 No silent defaults

For high-consequence tasks add:

```text
No silent engineering/business/legal/product defaults.
Only explicitly authorized defaults may be used, with provenance and reason.
```

---

# 7. Execution Order

Do not merely list tasks. Define dependency order.

Generic form:

```markdown
# REQUIRED EXECUTION ORDER

Do not reorder these phases unless the issue explicitly permits it.

PHASE 0  live state / source audit
PHASE 1  contradiction + blocker ledger
PHASE 2  contract / specification / scaffold
PHASE 3  failing tests proving the missing protection
PHASE 4  minimum implementation
PHASE 5  repair projections / integration
PHASE 6  focused validation
PHASE 7  full release / qualification gate
PHASE 8  recovery report / handoff
```

## 7.1 Critical anti-drift rule

When fixing drift:

> **First make a deterministic test fail on the existing contradiction; only then repair the contradiction.**

This proves the repository has gained a permanent drift detector instead of only receiving a one-time cleanup.

## 7.2 Phase entry gates

Where useful, add explicit entry conditions:

```text
PHASE 4 may not start until PHASE 3 contains a failing regression.
PHASE 7 may not start until focused validation passes.
Authority promotion may not start inside this issue.
```

---

# 8. Machine Acceptance Tests

Acceptance criteria should describe **properties the system must enforce**, not only features delivered.

Use IDs:

```text
AC-001
AC-002
...
```

Template:

```markdown
# MACHINE ACCEPTANCE TESTS

AC-001 — [single invariant]
Expected: [machine-observable result]
Failure: [what must fail if invariant is violated]

AC-002 — [single invariant]
Expected: ...
Failure: ...
```

Examples:

```text
AC-001 adapter authority equals machine manifest
AC-002 UI authority is projected, not independently hard-coded
AC-003 designAuthority cannot become true without an authorized transition
AC-004 missing source causes BLOCKED, not fallback
AC-005 changing one authority representation alone makes CI fail
AC-006 benchmark expected values cannot be generated by production implementation
AC-007 stale results cannot be exported as current
AC-008 Product Freeze cannot be inferred from method qualification
```

## 8.1 Property-first acceptance

Prefer:

```text
If someone later changes X incorrectly, test Y fails.
```

instead of:

```text
Add a test for X.
```

The first defines the protected property. The second merely requests test code.

## 8.2 Acceptance criterion to file mapping

For each PR/change set, maintain:

| Criterion | Required artifact/test | Files changed | Status |
|---|---|---|---|
| AC-001 | authority consistency validator | ... | PASS/FAIL/NOT_RUN |
| AC-002 | projection regression | ... | ... |

This makes unauthorized file changes easier to detect.

---

# 9. State Separation — required for governed systems

When a task contains lifecycle, authority, validation, release, qualification, publication, or approval concepts, enumerate them separately.

Template:

```markdown
# STATE SEPARATION

Do not infer one state from another.

Track independently where applicable:

- CODE_PRESENT
- IMPLEMENTATION_STATE
- DATA_QUALIFICATION
- METHOD_QUALIFICATION
- CAPABILITY_LIFECYCLE
- SCREENING / OPERATIONAL AUTHORITY
- DESIGN / APPROVAL AUTHORITY
- RELEASE / PRODUCT_FREEZE
- VALIDATION_EXECUTION_STATE
- MERGE / PUBLICATION AUTHORITY
```

Typical invariant:

```text
FUNCTION_EXISTS
!= IMPLEMENTED
!= QUALIFIED
!= ACTIVE
!= RELEASED
!= DESIGN_APPROVED
```

If the task uses a lifecycle such as:

```text
RESERVED -> QUALIFIED -> ACTIVE -> DEPRECATED
```

state explicitly what that lifecycle governs and what it does **not** govern.

---

# 10. Authority Boundary — required for high-consequence work

Template:

```markdown
# AUTHORITY BOUNDARY

Current authorized state:

[explicit values]

This issue may change:

[bounded list]

This issue may not change:

- governing method
- acceptance criterion
- benchmark oracle
- authority level
- lifecycle state
- release state
- design approval

unless a separately identified acceptance criterion and explicit approval authorize the transition.
```

Promotion should preferably be executed by a controlled command/gate rather than by manually editing a status field.

---

# 11. Benchmark / Oracle Contract

Use this whenever numerical, analytical, scientific, compliance, conversion, or classification correctness matters.

Template:

```markdown
# BENCHMARK / ORACLE CONTRACT

Each critical implementation branch requires an oracle independent of the production implementation.

Expected values must never be:

- generated by production output
- corrected from production output
- tuned to production output
- loosened solely to obtain PASS

Classify evidence:

B1 controlled published/adopted example
B2 independent engineering/analytical/reference vector
B3 boundary/unit/regression evidence
B4 API/UI/product parity evidence
```

The issue must define which classes count for qualification and which are additional regression evidence only.

---

# 12. Validation Truth

Every issue must define allowed validation statuses.

Recommended:

```text
PASS
FAIL
NOT_RUN
NOT_APPLICABLE
BLOCKED
```

Never convert:

```text
source inspection -> PASS
file exists -> PASS
workflow created -> PASS
job with zero executed steps -> PASS/FAIL of product
browser diagnostic -> official release gate PASS
```

Template:

```markdown
# VALIDATION TRUTH RULE

For every gate record:

- COMMAND / PROCEDURE
- ORACLE
- OBSERVATION
- STATUS
- ARTIFACT / RECEIPT

If the gate did not execute, status is `NOT_RUN` or `BLOCKED`, never PASS.
```

---

# 13. Stop Conditions

The issue must explicitly tell the agent when to stop extending implementation.

Template:

```markdown
# STOP CONDITIONS

Stop implementation and report the boundary if completion would require:

- changing an unassigned governing method
- changing a benchmark oracle
- inventing a missing source rule
- resolving an authority conflict without approval
- widening applicability
- changing lifecycle/production authority
- modifying a protected or overlapping active workstream
- claiming an unexecuted validation gate
```

This is not failure. It is correct fail-closed execution.

---

# 14. Live-State Grounding

Any issue likely to outlive a single session must instruct the next agent to re-ground current state.

Template:

```markdown
# LIVE-STATE GROUNDING

All SHAs, PR states, test counts, file lists and statuses in this issue are snapshots, not permanent truth.

Before mutation, re-resolve:

- current base SHA
- current branch / PR head
- open overlapping PRs
- exact changed-file set
- current implementation state
- current authority state
- current validation state

If live truth differs from this issue, record `STALE_ISSUE_FINDING` and use the controlled source precedence rules.
```

This prevents a historically correct issue from becoming an incorrect execution authority months later.

---

# 15. Recovery / Handoff Contract

Long-running tasks need a durable handoff artifact.

Template:

```markdown
# RECOVERY / HANDOFF

Maintain a living recovery report containing:

- task/issue ID
- base SHA
- current head SHA
- exact changed files
- current state/authority
- controlled source identities
- acceptance-criterion status
- validation commands and truth
- blockers
- residual risks
- out-of-scope findings
- EXACT_NEXT_ACTION
```

The next agent should be able to recover without reconstructing chat history.

---

# 16. Definition of Done

The definition of done should describe verifiable repository/system behavior.

Template:

```markdown
# DEFINITION OF DONE

This issue is complete only when:

- all mandatory expertise-gate facts are grounded;
- every change maps to an acceptance criterion;
- all required machine acceptance tests exist;
- known drift scenarios cause deterministic failure;
- implementation satisfies the bounded mission;
- all required validation gates are truthfully classified;
- no unauthorized state/authority promotion occurred;
- recovery/handoff record is current;
- remaining blockers/out-of-scope findings are explicit.
```

Avoid definitions of done such as:

```text
code looks good
UI improved
tests added
ready for production
```

unless those terms have machine-verifiable definitions.

---

# 17. Full reusable GitHub issue template

Copy this block when creating a new high-control issue.

```markdown
# [TITLE]

## TASK CLASSIFICATION — [EXPERT/SPECIALIST] ASSIGNMENT

This is not a generic [task type] assignment.

Required disciplines:

- [expertise A]
- [expertise B]
- [expertise C]

Consequence class: [LOW/MODERATE/HIGH/SAFETY-CRITICAL]

Working posture:

SOURCE CONTROLLED
FAIL CLOSED
TRACEABILITY REQUIRED
NO UNAUTHORIZED SCOPE EXPANSION

---

## EXPERTISE GATE — NO MUTATION YET

Before changing any file, establish from current live evidence:

1. [critical fact]
2. [critical authority/state]
3. [implementation seam]
4. [source/benchmark]
5. [known blocker/exclusion]
6. [validation/release command]
7. [known or possible contradiction]

For each answer provide:

VALUE
SOURCE
CURRENT REVISION / COMMIT / BLOB
STATUS

If a required fact cannot be proven:

BLOCKED_SOURCE_UNRESOLVED

Do not infer it.

---

## SINGLE MISSION

Your assignment has exactly one objective:

> [single independently verifiable outcome]

You are not assigned to:

- [out-of-scope A]
- [out-of-scope B]
- [authority/promotion boundary]
- [unrelated cleanup]

Record discovered items as `OUT_OF_SCOPE_FINDING`.

---

## CURRENT SNAPSHOT

Snapshot date: [date]
Base SHA: [sha]
Known current state: [state]
Known authority: [authority]
Known blockers: [blockers]

This section is informational. Re-ground live state before mutation.

---

## SOURCE PRECEDENCE

1. [highest authority]
2. [next]
3. [next]
...

Contradictions must be recorded as `DRIFT_FINDING` before modification.

---

## SCOPE LOCK

Every changed file must map to an acceptance criterion.

Allowed paths:

- [path]

Forbidden paths:

- [path]

No while-I-am-here changes.
No broad refactor.
No dependency upgrade.
No speculative abstraction.

---

## AUTHORITY / STATE BOUNDARY

Track separately:

- implementation state = [...]
- method/data qualification = [...]
- capability lifecycle = [...]
- operational/screening authority = [...]
- design/approval authority = [...]
- release/product-freeze state = [...]
- merge/publication authority = [...]

This issue may change:

- [...]

This issue may not change:

- [...]

---

## FAIL-CLOSED ESCAPE

Allowed blocker classifications:

BLOCKED_SOURCE_UNRESOLVED
BLOCKED_SOURCE_CONFLICT
BLOCKED_AUTHORITY_UNCLEAR
BLOCKED_DEPENDENCY
BLOCKED_VALIDATION_NOT_RUN
BLOCKED_ENVIRONMENT
OUT_OF_SCOPE_FINDING
NOT_APPLICABLE

Do not guess to obtain completion.

---

## REQUIRED EXECUTION ORDER

PHASE 0  live repository/system audit
PHASE 1  drift/blocker ledger
PHASE 2  contract/scaffold/specification
PHASE 3  failing regression for missing protection
PHASE 4  minimum implementation
PHASE 5  integration/projection repair
PHASE 6  focused validation
PHASE 7  full gate
PHASE 8  recovery report

Do not repair an existing drift before a deterministic test can detect it, where such a test is feasible.

---

## MACHINE ACCEPTANCE TESTS

AC-001 — [invariant]
Expected: [...]
Failure: [...]

AC-002 — [invariant]
Expected: [...]
Failure: [...]

AC-003 — [invariant]
Expected: [...]
Failure: [...]

Each changed file must identify the AC that requires it.

---

## BENCHMARK / ORACLE CONTRACT

[Delete this section only when genuinely not applicable.]

B1 = [...]
B2 = [...]
B3 = [...]
B4 = [...]

Production output must never create/correct/tune expected benchmark values.

---

## VALIDATION

Required commands/procedures:

1. [...]
2. [...]

Record each as:

COMMAND / PROCEDURE
ORACLE
OBSERVATION
STATUS = PASS | FAIL | NOT_RUN | NOT_APPLICABLE | BLOCKED
ARTIFACT / RECEIPT

Never claim unexecuted validation.

---

## STOP CONDITIONS

Stop and report if completion requires:

- [unassigned method change]
- [authority change]
- [benchmark change]
- [scope expansion]
- [protected workstream modification]

---

## RECOVERY / HANDOFF

Maintain:

- base SHA
- head SHA
- exact changed-file list
- source identities
- current authority/state
- acceptance criteria status
- validation truth
- blockers
- residual risk
- OUT_OF_SCOPE_FINDINGS
- EXACT_NEXT_ACTION

---

## DEFINITION OF DONE

Complete only when:

- [machine-verifiable criterion]
- [machine-verifiable criterion]
- [validation criterion]
- [authority/non-promotion criterion]
- [handoff criterion]

Do not merge/publish/promote unless explicitly authorized.
```

---

# 18. Compact schema for ordinary issues

Not every issue requires the full high-consequence template.

For normal bounded software work, retain at minimum:

```text
1. TASK CLASSIFICATION
2. SINGLE MISSION
3. LIVE CURRENT STATE
4. SOURCE PRECEDENCE / existing contract
5. SCOPE LOCK
6. EXECUTION ORDER
7. MACHINE ACCEPTANCE TESTS
8. VALIDATION
9. DEFINITION OF DONE
```

Use the full schema when any of the following are present:

- safety or engineering authority;
- regulated/compliance behavior;
- numerical/scientific correctness;
- irreversible data mutation;
- lifecycle or publication promotion;
- security-sensitive behavior;
- multiple active PRs/workstreams;
- source conflicts;
- previous agent drift;
- a long-running multi-agent task.

---

# 19. Anti-patterns this schema is designed to prevent

## 19.1 The encyclopedia issue

```text
50 pages of useful context
but no single mission or acceptance contract
```

Result: agent selects its own mission.

## 19.2 The questionnaire-only issue

```text
agent answers 20 questions correctly
then ignores those answers during implementation
```

Fix: questionnaire is only the expertise gate; machine acceptance tests enforce execution.

## 19.3 The placeholder-only issue

```text
TODO comments and empty functions describe future work
```

Result: agent can bypass or reinterpret them.

Fix: pair placeholders with executable blockers and tests.

## 19.4 The GitHub-issue-as-authority problem

```text
issue was correct when written
repository evolved
agent follows stale issue literally
```

Fix: live-state grounding + source precedence.

## 19.5 Green-by-any-means

```text
test is difficult
agent removes case / loosens tolerance / changes oracle
```

Fix: benchmark/oracle contract and scope lock.

## 19.6 Helpful drift

```text
agent notices nearby cleanup opportunity
performs broad refactor
creates overlap and new risk
```

Fix: every file change maps to an acceptance criterion.

## 19.7 Authority conflation

```text
code exists -> implemented -> qualified -> active -> safe/design approved
```

Fix: explicit state separation.

## 19.8 Validation inflation

```text
source review or a zero-step CI job described as PASS
```

Fix: validation truth taxonomy and retained evidence.

---

# 20. Issue-author preflight checklist

Before publishing an issue, the issue author should answer:

- [ ] Is the required expertise explicit enough to route this away from generic implementation work?
- [ ] Does the expertise gate require live evidence rather than textbook answers?
- [ ] Is there exactly one mission sentence?
- [ ] Are out-of-scope items explicit?
- [ ] Is source precedence defined?
- [ ] Can uncertainty end in BLOCKED rather than invention?
- [ ] Does every likely file change map to an acceptance criterion?
- [ ] Is execution order dependency-aware?
- [ ] Are at least the critical acceptance criteria machine-verifiable?
- [ ] Does the issue separate implementation, qualification, authority and release states where applicable?
- [ ] Are benchmark oracles protected from production self-reference?
- [ ] Are validation statuses defined truthfully?
- [ ] Are stop conditions explicit?
- [ ] Can a new agent recover from repository evidence without chat history?
- [ ] Would a future incorrect change cause a deterministic failure rather than merely violate prose?

If the last answer is **no**, the issue is not yet drift-resistant.

---

# 21. Governing mantra

Use this when deciding whether to add more prose or more enforcement:

```text
DO NOT TEACH THE AGENT EVERY CORRECT MOVE.
REMOVE UNNECESSARY DECISIONS.
MAKE WRONG MOVES FAIL.
MAKE UNCERTAINTY BLOCK.
MAKE AUTHORITY EXPLICIT.
MAKE SUCCESS MACHINE-VERIFIABLE.
```

And for all multi-agent work:

> **One machine truth, many projections, fail on drift.**
