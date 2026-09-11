# V2-01 PR plan

## Objective

Freeze the clean V2 Core1 canonical authority before subject-specific V2 producers
begin.

## Stack

While PR #179 is open:

```text
main
  └─ V2-00A / PR #179
       └─ V2-01
```

After PR #179 merges, retarget V2-01 to `main`.

This is a clean V2 stack, not the historical PR #160→#173 stack.

## Implementation sequence

1. Freeze canonical asset/registry/knowledge-set/gap contracts.
2. Add deterministic semantic-digest and resolver implementation.
3. Add synthetic dependency-composition fixture.
4. Add missing/unpromoted gap fixtures.
5. Add cycle, digest-drift, learner-contamination and benchmark-contamination falsifiers.
6. Add path-scoped CI.
7. Review adoption-ledger mapping without changing `PLANNED` → `ADOPTED` until
   the clean implementation and revalidation are accepted.

## Review gates

```text
CORE1_CONTRACTS_PRESENT = PASS
CANONICAL_SEMANTIC_DIGEST = PASS
DEPENDENCY_CLOSURE = PASS
SHARED_DEPENDENCY_DEDUPLICATION = PASS
CANONICAL_GAP_CANDIDATE = PASS
UNPROMOTED_ASSET_BLOCK = PASS
DEPENDENCY_CYCLE_REJECTION = PASS
DIGEST_DRIFT_REJECTION = PASS
LEARNER_CONTAMINATION_REJECTION = PASS
BENCHMARK_CONTAMINATION_REJECTION = PASS
DETERMINISTIC_KNOWLEDGE_SET = PASS
OLD_BRANCH_RUNTIME_DEPENDENCIES = 0
REAL_SUBJECT_MIGRATION = 0
```

## Follow-on

After this boundary is accepted:

- V2-02 may bind learner-state snapshots to canonical registry versions without mutating
  canonical truth.
- V2-03 may compose real cross-subject canonical dependencies.
- PHY-V2-01 / CHEM-V2-01 / Math V2 may add subject-specific canonical assets under
  separate subject-owned PRs.
