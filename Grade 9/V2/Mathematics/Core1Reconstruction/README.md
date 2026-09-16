# Mathematics V2 — Core1Reconstruction (M-UPGRADE-2 item 6)

The strongest cross-topic finding of the seven-topic stress test was an **asymmetry**:
Core2 became more mature than Core1. A question book exposed a six-state reasoning chain
while the study guide that supposedly prepared the learner contained a theorem statement, a
short explanation and one exercise.

So a full-teaching lesson must *realize* the chain, not declare that the labels exist:

```text
ANCHOR -> REPRESENT -> EXPLAIN -> RECONSTRUCT -> WORKED -> GUIDED
       -> FADED -> INDEPENDENT -> VERIFY -> TRANSFER
```

## What "realized" means, stage by stage

`policies/math-core1-reconstruction-policy.json` sets the evidence obligation per stage:

| stage | evidence kind | obligation |
| --- | --- | --- |
| `ANCHOR` / `REPRESENT` / `EXPLAIN` / `VERIFY` | `PROSE` or `DERIVATION` | a real minimum of learner-facing text |
| `RECONSTRUCT` | `DERIVATION` **only** | at least 3 steps, at least 2 of them substantive |
| `WORKED` / `GUIDED` / `FADED` / `INDEPENDENT` / `TRANSFER` | `REALIZATION` **only** | a materialized learner instance that itself passes the item 2 gate |

The chain order is significant, and the requirement is treatment-sensitive: the full chain
is demanded of `ACTIVE_STUDY` / `REPAIR_BEFORE` / `REPAIR_IN_UNIT` lessons, while a
`VERIFY_ONLY` lesson may legitimately be shorter — and still must carry a real derivation
wherever it claims to reconstruct something.

## Built from item 2's objects, not a parallel vocabulary

This is the dependency the issue called out. A `RECONSTRUCT` derivation is a list of the
same `math-route-state.schema.json` objects item 2 defined, and each practice stage
references a `math-learner-realization.schema.json` instance by `item_ref`. Those instances
are re-validated through `validate_realization()` here, so a chain cannot smuggle in a
worked example that names an operation without demonstrating it.

The contract resolver store consequently spans three phases
(`Core1Reconstruction` → `LearnerRealization` → `MathTypesetting`), which is the intended
shape rather than an accident.

## Teaching evidence is derived, never declared

`realized_teaching_evidence` is computed from what the chain actually contains — one token
`<lesson_ref>#<ROLE>` per substantive, non-trivial reasoning role realized anywhere in the
chain, including inside the realizations its practice stages reference. A chain that
declares evidence it does not realize fails `CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE`.

A trivial `CLASSIFY` step that restates the givens is deliberately *not* teaching evidence
for a Core2 `TRANSFORM` state.

## Theorem direction is first-class

Core2 proof routes depend on which direction was taught. A lesson that teaches only
"p(a) = 0 ⟹ (x − a) is a factor" has not prepared a learner for a Core2 item that needs the
reverse. `math-theorem-direction.schema.json` therefore states the forward implication and
its converse separately, declares whether the converse is true, and requires a
counterexample when it is not:

```text
forward   p(a) = 0                      ->  (x − a) is a factor of p(x)
converse  (x − a) is a factor of p(x)   ->  p(a) = 0            is_true: true
```

```text
forward   a and b are rational          ->  ab is rational
converse  ab is rational                ->  a and b are rational  is_true: false
          counterexample: √2 × √2 = 2 is rational while neither factor is
```

A converse that merely re-types the forward statement fails
`CONVERSE_RESTATES_FORWARD_STATEMENT`, and a Core2 state flagged `uses_converse` against a
lesson whose `direction_taught` is `FORWARD` fails `CONVERSE_USED_WITHOUT_BEING_TAUGHT`.

## The cross-core bridge

`math-cross-core-bridge-manifest.schema.json` makes the release invariant machine-falsifiable:

```text
Core2 required reasoning evidence − Core1 realized teaching evidence = {}
```

Each row carries what the consolidated review asked for:

```text
core2_question_ref   atomic_ask_ref      concept_refs[]        prerequisite_refs[]
reasoning_states[]   representation_requirements[]             verification_witness
core1_evidence_refs[]                    first_recovery_evidence_ref
```

Linkage is at the level of the **individual reasoning state**, not the lesson: a row that
points a `SETUP` state at `MATH-C1L-FACTOR-THEOREM` rather than
`MATH-C1L-FACTOR-THEOREM#SETUP` fails, because a lesson whose title happens to match is not
evidence that the move was taught.

## Fixture

`fixtures/build_math_reconstruction_chains.py` builds two chains of deliberately different
treatment:

- `MATH-C1L-FACTOR-THEOREM` (`ACTIVE_STUDY`) realizes the full chain. Its `RECONSTRUCT`
  stage derives the factor theorem from the division identity
  `p(x) = (x − a)q(x) + R` rather than asserting it; its `WORKED` stage reuses `PY-W1` from
  the LearnerRealization reference corpus, and `GUIDED`/`FADED`/`INDEPENDENT`/`TRANSFER`
  are fresh instances of the same family generated from distinct root triples
  (1,2,3 · −1,2,4 · 1,−2,5 · 3,−1,−2 — the last with a missing `x²` term, so the transfer
  is genuinely disguised).
- `MATH-C1L-IRRATIONAL-PRODUCT` (`VERIFY_ONLY`) realizes the shorter chain, but its
  `RECONSTRUCT` stage still carries the universal-claim → search-edge-case → counterexample
  → infer route the owner asked Number Systems to teach.

## Falsifiers

```text
CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE
CORE1_RECONSTRUCTION_WITHOUT_DERIVATION
CORE1_WORKED_INSTANCE_NOT_MATERIALIZED
CORE1_TRANSFER_INSTANCE_MISSING
CORE1_CHAIN_ORDER_DRIFT
CORE1_STAGE_UNDERREALIZED
THEOREM_DIRECTION_NOT_DECLARED
CONVERSE_RESTATES_FORWARD_STATEMENT
CONVERSE_USED_WITHOUT_BEING_TAUGHT
CORE1_CORE2_REASONING_COVERAGE_GAP
CORE1_RECONSTRUCTION_GATE_FAILED
```

## Release meaning

`PUBLICATION_ENGINEERING` only. A realized reconstruction chain is evidence that the
teaching surface exists and is grounded. It is not a pedagogy or expert-review PASS — both
remain `PENDING` — and it promotes no PCK beyond `PROVISIONAL_PROMOTED`.
