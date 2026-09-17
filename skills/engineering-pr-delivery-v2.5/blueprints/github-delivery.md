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
GHGEN/GHOP/observation records when projection is required, CI run IDs/head refs, issue/PR changes, and QRV delivery findings.

## VERIFICATION
Read back issue/PR state and relationships, confirm exact head/checks, and validate projection convergence/generation history.

## QUALITY FINDING CLASSIFICATION
Use DELIVERY_RISK, MIGRATION, AUTHORITY, or OTHER. Projection lag is coordination state; it does not rewrite engineering truth.

## TRUE HARD-STOP CONDITIONS
Unauthorized write/merge, repository-state conflict, write collision, or another existing authority/safety stop. A stale external projection can withhold HANDOVER_READY without becoming an engineering hard stop.

## OWNER REPORT
Report what changed externally, what remains unconfirmed, CI state, merge/review state, and any explicit Owner action required.

## SUCCESSOR HANDOVER
Transfer operation/generation IDs, uncertain outcomes, exact refs/run IDs, remaining reconciliation, and what must never be retried blindly.
