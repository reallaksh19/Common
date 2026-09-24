# Parent / Programme Engineering Issue Template

Use for `ISSUE_TOPOLOGY: PROGRAM_ISSUE_SET`.

The parent issue is the durable **Programme Specification + Coordination Record**. It preserves programme meaning; it is not a live execution lock.

```markdown
ISSUE_ROLE: PROGRAM_ROOT
PROGRAM_ID: PGM-<repo>-<short-task>
PROGRAMME_BASIS_REVISION: PB-0001
RELAY_PROTOCOL: V3.1_ONLY
RELAY_HANDOVER_ISSUE: PENDING

# Owner outcome
<Human/programme result that must ultimately become true.>

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

# Canonical input/source registry
| ID | Ref/source | Meaning | Authority | Kind | Invalidation |
|---|---|---|---|---|---|
| INPUT-001 | ... | ... | ... | PRODUCTION / AUTHORED / GENERATED / FIXTURE / EXTERNAL / OWNER_SUPPLIED | ... |

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
| ID | Requirement | Responsible workstreams | Evidence sources | Status |
|---|---|---|---|---|
| EXIT-001 | ... | A,B | PR/test/artifact | OPEN |

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
