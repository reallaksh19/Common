# Parent / Programme Engineering Issue Template

Use for `ISSUE_TOPOLOGY: PROGRAM_ISSUE_SET`.

The parent issue is the durable **Programme Specification + Coordination Record**. It preserves programme meaning; it is not a live execution lock.

```markdown
ISSUE_ROLE: PROGRAM_ROOT
AUTHORING_PROFILE: PROGRAMME
PROGRAM_ID: PGM-<repo>-<short-task>
PROGRAMME_BASIS_REVISION: PB-0001
RELAY_PROTOCOL: V3.1_ONLY
ORIGINAL_INTENT_ISSUE: PENDING
RELAY_HANDOVER_ISSUE: PENDING

# Owner outcome
<Human/programme result that must ultimately become true.>

# Original Intent source

Create/link one `[Original Intent] <programme title>` child when the programme originates from direct Owner instruction and the raw source is available.

```text
ORIGINAL_INTENT_ISSUE: github:<owner>/<repo>#<issue>
ORIGINAL_INTENT_DIGEST: sha256:<digest>
```

The Original Intent issue preserves historical Owner wording/inputs/ideas/expected outputs. It is not an EP and later Owner amendments do not rewrite it.

# Owner requirement ledger

| ID | Original/effective requirement | Source ref | Current interpretation | Status |
|---|---|---|---|---|
| TASK-001 | ... | Original Intent / Owner amendment | ... | ACTIVE / SUPERSEDED / SATISFIED |

# Why now / governing witnesses
<Concrete need/failure/evidence.>

Observed main: `<40-hex>`

# Non-goals
- ...

# Effective amendment index
CURRENT_BASIS_REVISION: PB-0001

| Amendment | Kind | Durable ref | Summary | Supersedes |
|---|---|---|---|---|
| ... | OWNER_DECISION / OWNER_AMENDMENT / RESPONSIBILITY_TRANSFER / PROGRAMME_DISCOVERY / EVIDENCE_RECORD | ... | ... | ... |

Ordinary discussion does not change the programme contract. Explicit amendments do.

# Governing Roadmap / authority registry
| ID | Ref/revision | Meaning | Authority | Mutation rule |
|---|---|---|---|---|
| RM-001 | ... | ... | OWNER / PROGRAMME | OWNER_ONLY / ... |

# Canonical input/source registry
| ID | Ref/source | Meaning | Authority | Kind | Invalidation |
|---|---|---|---|---|---|
| INPUT-001 | ... | ... | ... | PRODUCTION / AUTHORED / GENERATED / FIXTURE / EXTERNAL / OWNER_SUPPLIED | ... |

# Common benchmark / oracle registry
| ID | Type | Source/ref | Meaning | Independence | Status |
|---|---|---|---|---|---|
| BM-001 | FROZEN_ANALYTICAL / AUTHORITATIVE_REFERENCE / PRODUCT_REGRESSION / ... | ... | ... | YES / NO | READY / NOT_RUN |

# Common validation registry
| ID | Requirement | Evidence expectation | PASS/FAIL/NOT_RUN semantics |
|---|---|---|---|
| VAL-001 | ... | ... | ... |

# Programme invariants / preserve
- ...

# Workstream registry
| Workstream | Child issue | Outcome | Owns | Excludes | Consumers | Plan ref/revision |
|---|---|---|---|---|---|---|
| A | PENDING | ... | ... | ... | B | MISSING |

# Producer / consumer contracts
## OUT-001 — <production output>
Producer: A
Consumers: B
Meaning:
- ...
Consumers must not infer:
- ...

# Dependency contracts
## DEP-001 — <required production output>
Producer: A
Consumer: B
Why required: ...
Satisfaction evidence:
- ...
Work that may continue independently:
- ...

A dependency is missing production truth, not permission.

# Programme success / exit criteria
Use stable `EXIT-*` IDs. These are the denominator for programme-contribution reporting.

| ID | Requirement | Responsible workstreams | Evidence sources | Weight | Status |
|---|---|---|---|---:|---|
| EXIT-001 | ... | A,B | PR/test/artifact | — | OPEN |

Use declared weights only when the programme genuinely needs weighted acceptance. Otherwise V3.1 reports unweighted criterion coverage explicitly.

# Reconstruction topology

A successor should be able to traverse without replaying all chat:

```text
Original Intent
→ current Roadmap/Owner amendments
→ EP / child responsibility
→ primary-agent conversation + typed task publications
→ Local Agent/OFFLOAD provider issue(s)
→ RLL execution/state/results when used
→ PR/test/runtime material truth
→ Task Snapshot / Relay Handover
```

Index refs; do not duplicate transcript bodies.

# Decision surface
Engineer: implementation choices inside owned responsibility.
Coordinator: cross-agent consequences, useful parallelism, re-observation, helper/local-coordinator recommendation and routing.
Owner: genuine human/product/programme choices only.

# Dedicated [Relay Handover] operational ledger
Create one child issue:
`[Relay Handover] <programme title>`

It indexes workstreams, plans, PRs, exact heads, dependencies, pending items, known issues, negative knowledge, handoffs and next observations.

A stale/missing ledger reduces observability only; it never invalidates production engineering.

# Relay V3.1
Use Engineering Relay V3.1 only for recorder/reconstruction/reporting semantics when useful.
Do not use V3 or V2.5 for live coordination, status, recovery, gating, handover or Owner-command semantics.
```
