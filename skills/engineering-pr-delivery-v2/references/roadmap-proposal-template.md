# Roadmap Proposal and Owner Decision Templates

## 1. Agent roadmap proposal

Path:

```text
agents/chains/<CHAIN_ID>/roadmap-proposals/<PROPOSAL_ID>.md
```

Template:

```text
# <PROPOSAL_ID> — <short title>

CHAIN_ID:
PROPOSAL_ID: RP-0001
PROPOSAL_STATUS: PROPOSED
PROPOSAL_TYPE: CONCEPT_CHANGE | SCOPE_ADDITION | SCOPE_REDUCTION |
  BENCHMARK_ADDITION | BENCHMARK_REPLACEMENT | PHASE_REORDER |
  AUTHORITY_BOUNDARY_CHANGE | DEPENDENCY_CHANGE | STATUS_REFRESH |
  DEPRECATION | MIGRATION

ROADMAP_ID:
ROADMAP_PATH:
ROADMAP_BASIS_BLOB:
ROADMAP_WRITE_AUTHORITY: NONE

CREATED_AT:
CREATED_BY:

### Observation

What live repository/source/benchmark evidence triggered this proposal?

### Proposed roadmap change

Describe the strategic change. Do not edit the roadmap here.

### Why this belongs in the roadmap

Explain why this is strategic rather than an ordinary implementation detail.

### Evidence

List exact repository paths/commits/tests/benchmarks/sources.

### Engineering / architecture impact

### Benchmark / validation impact

### Dependency / sequencing impact

### Alternatives considered

### Risks

### Current coding impact

State one:

CONTINUE_WITHIN_CURRENT_ROADMAP
OWNER_DECISION_REQUIRED_BEFORE_CODING
BLOCKED_PENDING_OWNER_DECISION

### Suggested owner decision boundary

Define the smallest roadmap section/change that would need authorization.
```

The proposal is immutable after durable creation. Correct/supersede it with another proposal rather than rewriting the original evidence.

## 2. Owner decision receipt

Path:

```text
agents/chains/<CHAIN_ID>/roadmap-decisions/<DECISION_ID>.md
```

Create this only after an explicit Owner decision.

Template:

```text
# <DECISION_ID> — Owner roadmap decision

CHAIN_ID:
DECISION_ID: RD-0001
ROADMAP_ID:
ROADMAP_PATH:
ROADMAP_BASIS_BLOB:
PROPOSAL_REF: <path | NONE>

OWNER_DECISION: APPROVED | REJECTED | MODIFIED
AUTHORIZED_ROADMAP_MUTATION: YES | NO
AUTHORIZED_CHANGE_BOUNDARY:
REGISTRY_CHANGE_AUTHORIZED: YES | NO
COMBINED_WITH_PRODUCTION_CHANGE_AUTHORIZED: YES | NO

AUTHORIZATION_SOURCE: <owner instruction / GitHub comment / other durable locator>
RECORDED_AT:
RECORDED_BY:

### Decision summary

### Exact authorized mutation

### Explicitly not authorized

### Re-ground requirements before write

### Validation / review required after roadmap update
```

A receipt records the Owner's instruction; it does not create technical evidence by itself.

Do not infer approval from:

```text
AUTO MODE
merge approval for another PR
permission to continue implementation
issue assignment
silence / no objection
a prior roadmap authorization
```
