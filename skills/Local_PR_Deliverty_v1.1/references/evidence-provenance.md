# Evidence provenance

A PASS-shaped sentence is not evidence. v1.1 records evidence as typed provenance tied to an exact candidate and trust basis.

## Evidence classes

- `AUTHOR`: Coder/implementation evidence.
- `REVIEWER_INDEPENDENT`: evidence produced by the Reviewer production stage.
- `SUPER_REVIEW_INDEPENDENT`: evidence produced by Coordinator/Super Reviewer against the project acceptance contract.
- `CI_PROVIDER`: provider-observed CI evidence.
- `EXTERNAL_ORACLE`: evidence from a project-declared external oracle.
- `MANUAL_OBSERVATION`: structured manual observation.

A project criterion marked `super_review_required` cannot be satisfied solely by AUTHOR evidence.

## Evidence record binding

Evidence records include:

- producer role/principal;
- Common and project protocol basis;
- candidate SHA;
- review-lease ref where independent;
- acceptance-surface digest;
- harness/baseline/fixture digests;
- environment digest;
- collection timestamp;
- procedure kind;
- command argv/exit code when command-backed;
- result;
- artifact digest.

Independent evidence must resolve to the same lease and protected acceptance surface as the stage outcome.

## Result truth

Evidence and acceptance results use truthful values:

`PASS | FAIL | NOT_RUN | INCONCLUSIVE | NOT_APPLICABLE`

Owner risk acceptance never rewrites a result to PASS. Where policy permits, a required NOT_RUN may yield `APPROVED_WITH_WAIVER`, with the NOT_RUN result and exact waiver retained.

## CI evidence

Trusted required checks bind the check name, policy source, provider, workflow path/digest, expected app identity, run/job identity, candidate SHA, mandatory-step execution and artifact digests.

A green wrapper with skipped mandatory validation is NOT_RUN, not PASS.

## Limitation

The v1.1 checker validates supplied/provider-observed record consistency. Without stronger external credentials/signatures it cannot cryptographically prove that a human or provider statement is authentic. That stronger trust boundary belongs to later credential/attestation hardening, not fabricated certainty in v1.1.

