# Project-specific acceptance contract

Common v1.1 deliberately does not know project semantics.

A project protocol is an exact, versioned engineering-acceptance contract. It declares criteria, verification method IDs, Super Reviewer harnesses, fixtures/oracles and external gates. TASK pins it by exact repository/commit/path and digest.

Super Reviewer executes that contract against the exact candidate. Product fixes are allowed; changing the protected acceptance surface during the same certification attempt is not.

Common may define a shared verification vocabulary without making every class mandatory: POSITIVE, NEGATIVE, BOUNDARY, INVARIANT, ROUND_TRIP, METAMORPHIC, PROPERTY, DIFFERENTIAL, FAULT_INJECTION, ROLLBACK, IDEMPOTENCY, REPLAY, CONCURRENCY, PRODUCER_CONSUMER, FUZZ, PERFORMANCE, EXTERNAL_ORACLE, MANUAL_VISUAL, SECURITY.

The project declares a normalized `verification_methods` table. Each method declares its verification class, applicable production roles, permitted evidence classes, optional harness/external-gate binding, material inputs and rerun policy. Criteria reference method IDs; harnesses list the methods they actually execute. Common derives criterion/gate truth from method-bound evidence rather than trusting duplicated result labels.


## Canonical protocol identity

The bundled project-protocol record is not trusted merely because it contains a `digest` string. Common recomputes the canonical SHA-256 of the visible project-protocol content (excluding the `digest` field) and requires that value to match the pinned TASK digest.

This prevents an agent from editing criteria, harness coverage, protected fixtures/oracles, external-gate policy or regression inventory while preserving an old claimed protocol digest.

The same canonical-digest rule applies to the visible protected acceptance surface and environment records. Product fixes may change product identity; they may not silently rewrite these trust records under the same identity.

## External gates

Each project external gate declares:

- whether it is required;
- whether Owner risk waiver is permitted;
- which task kinds it applies to;
- `allowed_evidence_classes`.

A gate reported as `PASS` must cite evidence and every cited evidence class must be allowed by the pinned project protocol. AUTHOR evidence cannot satisfy an external gate unless the Common schema explicitly permits that class; v1.1's external-gate contract intentionally limits gates to independent/provider/manual-observation classes.

Required external-gate `FAIL` or `INCONCLUSIVE` cannot be waived. A required `NOT_RUN` may advance only as `STAGE_COMPLETE_WITH_WAIVER` when that exact gate is marked waivable and an active Owner waiver is bound to the exact final review lease/candidate. The recorded gate result remains `NOT_RUN`.

External-gate IDs are unique within a project protocol.


## Transitive protected-surface manifest

The protected surface is a manifest, not only a top-level harness hash. It records content identities for harness entrypoints and transitive imported helpers plus protected fixtures, baselines, oracle configuration, tolerances, generators, lockfiles/toolchain configuration, CI workflow/policy material and other project-declared acceptance dependencies.

The canonical `manifest_digest` is bound into each acceptance surface, final independent evidence and review lease. Changing an imported helper while preserving a top-level harness label therefore expires the acceptance basis.

## Discovery and repair epoch

Reviewer/Super Reviewer first executes the role-required discovery methods against the input candidate. The finding set and discovery evidence are frozen before the first repair. Findings are classified as bounded product fix, material scope change, acceptance-surface defect or external dependency.

Only bounded product fixes remain inside the same acceptance epoch. After repair, affected project methods are rerun on the resulting final candidate. A material scope or acceptance-surface change requires an explicit new basis rather than self-certification.
