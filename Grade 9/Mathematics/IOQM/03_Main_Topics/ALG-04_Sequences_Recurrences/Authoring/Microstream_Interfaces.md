# ALG-04 — Wave-1 Research Interfaces

Authoring-only evidence. These interfaces are inputs to the single integrated student book; they are not standalone student chapters.

## W1-A — AP/GP recognition

**Invariant**
- AP: constant first difference.
- GP: constant nonzero ratio.

**Misconception**
Formula matching from appearance.

**Decision boundary**
Check difference before declaring AP; check nonzero ratio before declaring GP; allow “neither”.

**Lead integration**
Teach once in RECONNECT/DISCOVER, then retrieve only.

## W1-B — term vs partial sum

**Invariant**
`a_n=S_n-S_{n-1}` for `n>=2`, with `a_1=S_1`.

**Representation**
accumulation -> local contribution.

**Misconception**
`S_n` and `a_n` share the same index, so the learner treats them as the same quantity.

**Lead integration**
Use as the first canonical example of local cancellation.

## W1-C — recurrence reading

**Semantics**
A recurrence is a dependency rule on an index range and needs sufficient initialization.

**Verification**
Initial values + identity under the recurrence for all allowed indices.

**Misconception**
Checking several generated terms is treated as proof.

**Lead integration**
Export this exact language downstream to COMB-03.

## W1-D — window subtraction

**Invariant**
For `W_i=a_i+...+a_{i+k-1}`:
`W_{i+1}-W_i=a_{i+k}-a_i`.

**Anchor**
`IOQM-2025-Q26`, answer `10`, independently verified.

**Decision boundary**
moving average surface vs termwise index-shift relation.

**Lead integration**
Primary discovery anchor for “subtract nearby relations”.

## W1-E — telescoping

**Invariant**
Represent `u_k=F(k)-F(k+1)` so internal terms cancel.

**Decision boundary**
consecutive-factor denominator is a clue, not proof.

**Lead integration**
Teach as the summation-scale version of the same local-cancellation idea.

## W1-F — neighboring-term invariants

For
`a_{n+2}=p a_{n+1}+q a_n`,
define
`D_n=a_n^2-a_{n-1}a_{n+1}`.

Then:
`D_{n+1}=-qD_n`.

**Anchor**
`IOQM-2023-Q10`, answer `51`, independently verified.

**Decision boundary**
huge raw terms vs small invariant.

**Lead integration**
Derive once; use an author-created recurrence for independent mastery so historical wording is not reconstructed from classifier metadata.

## W1-G — source custody

- ALG-04 primary historical IDs: exactly `IOQM-2025-Q26`, `IOQM-2023-Q10`.
- Both source statuses clean.
- Both official/key values agree with independent verification.
- No metadata-correction overlay event applies to these IDs.
- COMB-03 anchors are not promoted as ALG-04 primary recurrence evidence.

## Cross-stream contrast candidates

1. term `a_n` vs partial sum `S_n`;
2. AP vs GP;
3. explicit formula vs recurrence;
4. recurrence iteration vs difference transform;
5. moving averages vs window subtraction;
6. rational sum vs true telescope;
7. high-index raw terms vs invariant;
8. algebraic recurrence vs counting-state recurrence;
9. deterministic state evolution vs adversarial game;
10. matching early terms vs recurrence verification.

## H3 -> H0 fading

- H3: first algebraic relation supplied.
- H2: structure/representation supplied.
- H1: visible clue supplied.
- H0: independent changed-surface item.
- Every item is first attempted H0 before optional hints are accessed.

## Independent QA status

```text
DERIVATIONS_CHECKED: PASS_STATIC_SECOND_ROUTE
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS_STATIC
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: CLASSROOM_TIMING/PSYCHOMETRICS NOT_RUN
```

## Lead integration rule

Do not organize the student book as separate AP, GP, recurrence and telescoping mini-books with repeated onboarding. Reuse one question:

> What neighboring representation cancels the most before I calculate?
