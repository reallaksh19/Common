# Review lease

A review lease is the machine-readable statement of exactly what an independent review outcome covers.

## When it is sealed

Reviewer and Coordinator/Super Reviewer may repair product material during their stage. Therefore the lease is sealed against the **final candidate actually verified after those repairs**, not blindly against the stage input.

The lease names:

- repository and PR;
- task/stage record;
- certifier role and principal;
- candidate SHA and candidate-tree digest;
- target ref and target-base SHA;
- merge-base SHA;
- integration-tree digest;
- stacked dependency heads;
- Common protocol ref/digest;
- project protocol ref/digest;
- task and parent specification digests;
- PRE_VERDICT context reference and context digests;
- PR-description digest;
- Owner-control digest;
- required-check policy digest;
- environment ref/digest;
- acceptance-surface digest and transitive acceptance-surface manifest digest;
- explicit harness, baseline, oracle and fixture digests.

## Content-addressed identity

`lease_id` is not a free-form label. It is `sha256:<canonical-lease-content>`, computed from the complete visible lease record excluding the `lease_id` field itself.

Changing any bound lease field therefore changes the lease ID. Stages, evidence records, waivers and delivery results that reference the old lease do not silently follow the edit; they become stale until a newly sealed lease is referenced explicitly.

The validator recomputes this identity and rejects a lease whose claimed ID does not match its canonical content.

## Expiry

A lease is stale when any bound assumption changes materially. Examples include candidate head, target head, merge base, stacked predecessor head, Common/project protocol, specification, context frontier, Owner control, environment, required-check policy, protected harness/baseline/oracle/fixture set or integration tree.

An agent may not preserve approval with prose such as “the old review should still apply.”

## Stacked PRs

Each downstream lease carries the exact predecessor/dependency head set. A changed predecessor invalidates the downstream lease even if the downstream branch name and task text are unchanged.

## Target refs

Common does not assume every PR targets `main`. TASK pins `target_ref`; source attestation, lease, observed state, provider merge observation and canonical post-merge evidence must agree with that target.

## Waivers

Waivers bind to the final lease and candidate. They are non-transitive and expire independently. They never alter the evidence result. A required `NOT_RUN` may advance only under the protocol's explicit approved-with-waiver path; `FAIL` and `INCONCLUSIVE` remain non-advancing.

