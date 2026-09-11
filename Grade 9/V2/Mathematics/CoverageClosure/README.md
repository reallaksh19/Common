# Mathematics M-J — coverage closure, transfer evidence and longitudinal update

M-J closes the semantic loop from the original assessment through study design and Core2 transfer back into learner evidence and future learning obligations.

The separation invariant remains:

```text
what happened on a transfer attempt
!= what evidence class that creates
!= what we infer about current learner state
!= which future obligations remain open
```

## Closure chain

```text
Assessment Question / Subpart
↔ declared topic + canonical concept/capability + prerequisites
↔ M-D problem family / reasoning / verification
↔ Core1 teaching obligation
↔ M-I Core2 transfer page + H1/H2/H3
↔ MathTransferEvidenceEvent
↔ MathLearnerStateUpdate
↔ MathLongitudinalUpdate
```

A planned Core1 link is enough to prove semantic traceability but **not** enough to claim publication readiness. While M-G is waiting for real human PCK promotion, the publication closure is explicitly `BLOCKED_UPSTREAM_PCK_PROMOTION`.

## Evidence semantics

Support use is preserved as evidence provenance:

- `INDEPENDENT_SUCCESS` is independent current evidence.
- `H1_SUCCESS`, `H2_SUCCESS`, and `H3_SUCCESS` are assisted evidence of increasing support depth; none is rewritten as independent success.
- `SOLUTION_EXPOSED` is non-mastery evidence.
- `CORRECT_ANSWER_INVALID_REASONING` is not full capability success.
- `INCORRECT_AFTER_SUPPORT` can create negative evidence only when the assessment-safety policy permits negative inference.
- `NO_ATTEMPT` creates no readiness claim.
- verification is tracked separately as `VERIFICATION_SUCCESS`, `VERIFICATION_FAILURE`, `VERIFICATION_NOT_ATTEMPTED`, or `VERIFICATION_NOT_APPLICABLE`.

For Q9, M-B's underdetermined-item policy survives end-to-end: an incorrect response cannot create ordinary negative learner evidence. For Q12, both valid branches remain accepted by the transfer page and closure layer.

## Longitudinal invariant

A current success can update acquisition and, when independent, independent reconstruction. It cannot silently close:

```text
delayed_retention
near_transfer
far_transfer
mixed_discrimination
fluency
timed_performance
```

Every future obligation carries an explicit owner capability and remains machine-visible until separately evidenced.

## Fail-closed gaps

M-J rejects missing Core1 semantic coverage, missing Core2 transfer, missing treatment decisions, source-custody drift, reasoning routes without family authority, evidence events without source pages, learner-state updates without evidence semantics, and longitudinal obligations without owners.
