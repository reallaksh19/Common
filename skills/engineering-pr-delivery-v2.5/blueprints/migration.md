# Migration blueprint

## WHEN TO APPLY
Apply when changing persisted data/schema, wire/API contracts, configuration formats, state machines, storage layout, protocol versions, feature rollout state, or when moving from a legacy relay/control model.

## REQUIRED INPUTS
Source and target representations, compatibility window, population/state inventory, rollback/forward strategy, irreversible steps, version detection, Owner decisions, and acceptance/evidence requirements.

## PROCEDURE
1. Inventory actual source states; do not infer uniformity from the happy path.
2. Define target invariant and explicit mapping for every source category, including unknown/invalid states.
3. Define ordering, compatibility, idempotency, retry, and crash recovery.
4. Dry-run or simulate transformation where possible and quantify affected records/artifacts.
5. Execute only within authority and verify target state after each irreversible boundary.
6. Preserve evidence for deferred/unmigrated cases rather than silently coercing them.

## BEST-PRACTICE CHECKLIST
- No fabricated history/evidence.
- Re-running is safe or explicitly prevented.
- Partial completion is discoverable and recoverable.
- Rollback limitations stated before execution.
- Old and new readers/writers compatibility intentionally handled.

## ANTI-PATTERNS
Blind bulk rewrite, implicit defaults for unknown legacy states, deleting source evidence before verification, assuming success from command exit alone, and mixing Owner-intent reinterpretation into mechanical migration.

## REQUIRED ARTIFACTS
Inventory, mapping/reconciliation plan, dry-run evidence, migration receipt/result, unresolved-state list, and QRV findings.

## VERIFICATION
Compare pre/post counts/invariants, sample transformed objects, validate readers/writers, and prove crash/retry behavior for material migrations.

## QUALITY FINDING CLASSIFICATION
Use MIGRATION, DELIVERY_RISK, AUTHORITY, or DESIGN. Unresolved legacy ambiguity may require Owner review without automatically stopping unrelated safe work.

## TRUE HARD-STOP CONDITIONS
Authority ambiguity that would rewrite intent, irreversible unsafe transformation, repository-state conflict, or protected-invariant loss maps to existing hard stops. Cosmetic cleanup does not.

## OWNER REPORT
Explain what moved, what did not, reversibility, compatibility, residual ambiguity, and any decision needed before the next irreversible step.

## SUCCESSOR HANDOVER
Transfer inventory basis, completed range, unresolved cases, retry/rollback rules, and the exact next migration verification step.
