# GitHub delivery blueprint

## WHEN TO APPLY
Apply when the slice publishes or reconciles GitHub PR/issue/check/run/relationship state, changes delivery workflow, or depends on external coordination projection. Pure local implementation without GitHub mutation may be not applicable.

## REQUIRED INPUTS
Repository authority objects, current GHGEN/GHOP when applicable, target repository/ref, PR/issue identifiers, exact material ref, CI requirements, projection capability limits, and closure/supersession rules.

## PROCEDURE
1. Confirm repository truth before preparing external mutation.
2. Use stable operation identity and persist attempt state before writes when the projection protocol requires it.
3. Perform the smallest external mutation; never infer success from request intent.
4. Read back and verify the actual external state/relationship/marker.
5. Reconcile repository projection state only after verified observation.
6. Preserve uncertain outcomes for retry-safe recovery rather than duplicating operations.

## BEST-PRACTICE CHECKLIST
- Draft/merge state changes require explicit authority.
- Exact-head CI evidence names the actual head/run.
- Native relationships are claimed only when created and read back natively.
- Connector limitations remain visible.
- Superseded operations lose retry authority.

## ANTI-PATTERNS
Treating GitHub as roadmap authority, blind retry after timeout, body links masquerading as native relationships, stale-head CI claims, auto-merge without authorization, and overwriting unresolved projection history.

## REQUIRED ARTIFACTS
GHGEN/GHOP/observation records when issue projection is required, `DOBS-*` delivery observation when a PR delivery vehicle is current, CI run IDs/head refs, issue/PR changes, and QRV delivery findings. Merge authorization, when granted, is an applied Owner ODR bound to the exact PR/head and is not a provider observation.

## VERIFICATION
Read back issue/PR state and relationships, confirm exact head/checks, and validate projection convergence/generation history.

## QUALITY FINDING CLASSIFICATION
Use DELIVERY_RISK, MIGRATION, AUTHORITY, or OTHER. Projection lag is coordination state; it does not rewrite engineering truth.

## TRUE HARD-STOP CONDITIONS
Unauthorized write/merge, repository-state conflict, write collision, or another existing authority/safety stop. A stale external projection can withhold HANDOVER_READY without becoming an engineering hard stop.

## OWNER REPORT
Report what changed externally, what remains unconfirmed, PR lifecycle/head/base, exact-head CI state, mergeability, review/change-request state, ready-for-review, technical-ready-to-merge, merge authorization, and any explicit Owner action required. Keep these dimensions independent.

## SUCCESSOR HANDOVER
Transfer operation/generation IDs, uncertain outcomes, exact refs/run IDs, remaining reconciliation, and what must never be retried blindly.


## PR DESCRIPTION CORRELATION

When PR delivery is applicable, the PR body must contain the V2.5 correlation marker and a meaningful Issue↔EP mapping.

Required shape:

```text
Issue number / ISSUE_GRAPH node
↔ execution package id / path
↔ roadmap work package
↔ relationship
↔ plain-language meaning
```

The provider-read body is normalized into `DELIVERY_OBSERVATION.description_contract`. The repository validator proves that the issue and EP converge on the same roadmap work package; string presence alone is insufficient.

Run `validate_pr_correlation.py` at task close. A current active EP or latest checkpoint EP that is absent from all tracked relevant PR correlations is a delivery-contract failure.

All tracked non-terminal PRs are recurring Owner-summary obligations until MERGED/CLOSED. Unknown lifecycle is carried forward conservatively until readback resolves it.

