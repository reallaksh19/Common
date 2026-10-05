# Evidence provenance

A PASS-shaped sentence is not evidence. v1.1 records evidence as typed provenance tied to an exact candidate, executable verification method and trust basis.

## Evidence classes and origin

Evidence classes are `AUTHOR`, `REVIEWER_INDEPENDENT`, `SUPER_REVIEW_INDEPENDENT`, `CI_PROVIDER`, `EXTERNAL_ORACLE` and `MANUAL_OBSERVATION`.

Origin is separate from collection/attestation. Each EVIDENCE_RECORD records `origin_kind/origin_principal` and `collected_by_role/collected_by_principal`. A Super Reviewer may collect and consume a GitHub Actions result without pretending the Super Reviewer produced that CI evidence. Likewise an external oracle remains externally originated.

Independence is also explicit: `oracle_independence` is orthogonal to `principal_relationship_to_candidate`. A role label does not make mutable author expectations independent.

## Executable-method binding

Every evidence record names:

- `verification_method_id`;
- `harness_id` or `external_gate_id` where applicable;
- `evidence_phase` — `DISCOVERY | FINAL_ACCEPTANCE | EXTERNAL_GATE`;
- exact candidate SHA;
- Common/project protocol basis;
- final review lease where final independent evidence applies;
- protected acceptance-surface and transitive-manifest digests;
- harness/baseline/fixture digests;
- environment digest;
- collection timestamp and procedure;
- result and artifact identity.

The project protocol is authoritative for which evidence classes may satisfy each verification method. A required method is not proved merely because its ID appears in an acceptance row.

## Result derivation

Evidence and criterion/gate results use:

`PASS | FAIL | NOT_RUN | INCONCLUSIVE | NOT_APPLICABLE`

Common derives a method result from the cited evidence and then derives the criterion/gate result. A claimed criterion `PASS` with cited `FAIL`, `INCONCLUSIVE` or unresolved `NOT_RUN` evidence is rejected.

Owner risk acceptance never rewrites a result to PASS. Where policy permits, a required NOT_RUN may yield stage lifecycle `STAGE_COMPLETE_WITH_WAIVER`; the evidence and criterion/gate result remain `NOT_RUN`.

## Discovery versus final evidence

Reviewer/Super Reviewer discovery evidence is bound to the input candidate and frozen before the first product repair. Final acceptance evidence is recollected against the resulting validated candidate. Pre-repair evidence cannot certify post-repair output.

## CI identity

Trusted required checks distinguish:

- triggering PR head SHA;
- provider run head SHA;
- tested/checked-out commit SHA;
- tested tree digest;
- checkout mode (`PR_HEAD | SYNTHETIC_MERGE | MERGE_QUEUE`);
- base and merge-base SHAs;
- integration-tree digest;
- provider/app, workflow path/digest, run/job identity;
- mandatory-step execution and artifacts.

A GitHub PR workflow may run against a synthetic merge commit. That is valid only when trusted policy says the check certifies an integration candidate and the tested integration-tree identity matches the reviewed candidate/base integration tree. A green wrapper with skipped mandatory validation is NOT_RUN, not PASS.

## Repository policy and merge authority

Repository policy is part of evidence freshness, not an assumption. PRE_MERGE observed state records the trusted policy source reference, policy digest and visibility. Only `CONFIRMED` policy visibility can become merge-ready; `UNKNOWN` or `UNAVAILABLE` is `WAITING_EXTERNAL`.

Merge authority is a separate authenticated observation. Engineering approval never implies merge authority.

## Limitation

The checker validates supplied/provider-observed record consistency. Without stronger external credentials/signatures it cannot cryptographically prove that a human or provider statement is authentic. Missing evidence remains missing; it is never converted into certainty by prose.
