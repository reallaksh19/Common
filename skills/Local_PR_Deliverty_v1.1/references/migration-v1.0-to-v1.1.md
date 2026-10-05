# Migration from Local_PR_Deliverty_v1.0 to v1.1

V1.0 records remain historical evidence and are not rewritten.

V1.1 changes the responsibility model while retaining the Coder -> Reviewer -> Coordinator/Super Reviewer order.

## Semantic changes

1. Reviewer and Coordinator/Super Reviewer are production stages. They fix internal product defects discovered in their own stage instead of routing ordinary repair backward.
2. `repeat_stages` is retained only for structural compatibility and must be empty.
3. Independence is enforced by protecting the pinned project acceptance surface rather than by prohibiting downstream product writes.
4. TASK pins a project-specific acceptance protocol and declares verification methods / Super Review applicability.
5. STAGE_RECORD publishes structured `acceptance_results`, `evidence_manifest`, `acceptance_surface`, and `production_output`.
6. Required project acceptance uses PASS / FAIL / NOT_RUN / INCONCLUSIVE / NOT_APPLICABLE semantics.
7. Super Review criteria require independent project-harness or external-oracle evidence; author tests alone are insufficient.
8. Review leases, environment records, context snapshots, waivers and observed-state records are content-addressed supporting contracts for later freshness/provider hardening.

## Operational migration

Do not convert an in-flight v1.0 attempt in place. Finish or checkpoint it under its recorded v1.0 basis, then start the next material attempt under an exact v1.1 protocol reference and project-protocol reference.

Do not reinterpret an old v1.0 `repeat_stages` record as v1.1 behavior. It remains evidence of the old protocol.

Project teams adopting v1.1 must first publish a project acceptance protocol. Common v1.1 does not synthesize domain acceptance criteria from implementation code.

## Acceptance-surface changes

A change to project protocol, independent harness, protected fixture/baseline, oracle, tolerance, benchmark budget, or required acceptance CI is a new acceptance basis. Product fixes and acceptance-surface changes must not mutually certify one another.
