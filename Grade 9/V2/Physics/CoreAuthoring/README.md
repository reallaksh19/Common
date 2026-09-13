# Physics V2 — P-G Promoted Physics PCK and Core1 instructional authoring

P-G implements issue #255 under the #320 catch-up. It turns a P-F
`PhysicsLearnerStudyModel` into a treatment-relative Core1 semantic study plan using
**promoted-pilot** Physics PCK, newly authored Core1 problem instances, and mandatory
Appendices A/B/C.

## Authority boundary

```text
P-F LearnerStudyScope + LearnerStudyModel   decides required scope and treatment
+ P-D problem-family / reasoning-route / verification semantics (carried through P-F)
+ P-G promoted-pilot Physics PCK             supplies teaching affordances
+ P-G authoring profiles                     constrain authored instances
→ PhysicsCore1StudyPlan
```

PCK does **not** choose learner treatment and does **not** redefine canonical Physics.
Treatment comes from P-F; a plan that rewrites it fails `PCK_DECIDES_TREATMENT`.

## SEE → REALIZE → UNDERSTAND

Every promoted asset carries the three phases explicitly, and a `FULL_LEARNING` lesson
lays them out in order:

```text
SEE       phenomenon anchor + system/frame/sign setup
REALIZE   representation path + reconstruction steps
UNDERSTAND relation, model validity condition, and what makes it stop holding
→ worked reasoning sequence
→ misconception minimal contrast + repair + retry
→ guided → faded → independent
→ physical verification
→ transfer bridge
```

`READY_VERIFY_ONLY` stays concise (activation, independent attempt, physical check) and
`PROBE_FIRST` stays a probe: both are falsifier-guarded against silently becoming reteaching.

## Honest PCK promotion — the central mechanism

The promotion state of a PCK asset is **derived from its review ledger**, never declared:

```text
CANDIDATE
  → EVIDENCE_REVIEWED   evidence-stage review passed
  → PROMOTED_PILOT      + pedagogical AI review PASS + machine scope check PASS
  → PROMOTED_RELEASE    + real SUBJECT_EXPERT_PASS and PEDAGOGY_EXPERT_PASS
```

`AI_ASSISTED_REFERENCE_REVIEW` is advisory and structurally cannot become a human expert
pass:

| rule | falsifier |
|---|---|
| a declared promotion state that disagrees with the derived one | `FABRICATED_PROMOTION_STATE` |
| a human-only review class marked `PASS` with no attestation reference | `FAKE_HUMAN_REVIEW_STATE` |
| an AI/machine review row carrying an attestation reference | `AI_REVIEW_COUNTED_AS_EXPERT_PASS` |
| a review class whose reviewer authority class does not match it | `FABRICATED_EXPERT_REVIEWER_IDENTITY` |
| release flags inconsistent with the derived state | `AI_REVIEW_COUNTED_AS_EXPERT_PASS` |

**Current state: every asset is `PROMOTED_PILOT`.** `SUBJECT_EXPERT_PASS` and
`PEDAGOGY_EXPERT_PASS` are `PENDING` for all 13 assets, and
`final_product_release_blocked` is `true`. No authorized human reviewer has seen this
material. `PROMOTED_RELEASE` is unreachable from this repository.

## Subject-wide generic, not topic-specific

The primary PCK family for a capability is selected by **structural rules over the P-F
record's own obligations** — graph/signed-area representation, multiphase structure,
model-validity requirement, vector representation, frame/sign requirement, relation
representation — declared as data in `physics-instructional-authoring-profile.json`.

No capability id, topic id or problem-family id appears in the selection code. A new
Physics topic (dynamics, work-energy, waves) enters as P-C/P-D data and authors correctly
without a schema change or a new code branch. The falsifier
`TOPIC_SPECIFIC_SCHEMA_INSTEAD_OF_GENERIC_PHYSICS_REASONING_ROUTE` asserts that renaming a
capability does not change its selected family, while changing its structure does.

## PCK families (13, all generic)

```text
PHENOMENON_ANCHOR                 SYSTEM_FRAME_SIGN_SETUP
STATE_REPRESENTATION_TRANSLATION  MODEL_SELECTION_AND_VALIDITY
PHASE_CONTINUITY_REASONING        RELATION_RECONSTRUCTION
GRAPH_SLOPE_AREA_DECODING         VECTOR_COMPONENT_DECOMPOSITION
WORKED_REASONING_SEQUENCE         MISCONCEPTION_MINIMAL_CONTRAST
FIRST_MOVE_DECISION_SUPPORT       PHYSICAL_VERIFICATION
TRANSFER_VARIATION
```

## New Core1 problems, not transfer leakage

Worked examples and Appendix A items are `NEW_AUTHORED_CORE1` instances bound to an
upstream P-D problem family, with `external_candidate_refs` empty. Original external
transfer items stay reserved for P-I Core2.

## Authored instances: a worked example resolves to a number (P-UPGRADE-2 item 3)

A Core (1) problem used to be an authoring *plan* — "select the model, choose the relation,
solve" — with no situation, no quantities and no result. A learner cannot watch that being
solved. Now every place a learner is asked to do something carries a **resolved instance**.

```text
registry/physics-authored-instances.json     data, keyed by problem family
engine/physics_instance_resolver.py          the engine that makes the data load-bearing
contracts/physics-authored-instance.schema.json
contracts/physics-instance-route-state.schema.json   shared with P-I
```

An instance declares a `situation`, a `frame`, typed `givens`, one `unknown`, a typed
`reasoning_route` of route states (`role`, `input_state_refs`, `representation_ref`,
`equation`, `why_valid`, `output_state`) and its checks. The resolver then:

- **computes** every `EXECUTE` state and the final answer with a restricted `ast`
  evaluator — no `eval`, arithmetic and a fixed function set only — so a declared answer
  that does not follow from the declared route is a failure, not a claim;
- proves the route **transforms state**: every input must already be known and the set of
  known symbols must grow, or `WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE`;
- expands declared per-given value lists into deterministic variants, so worked, guided,
  faded, independent, retry and Appendix A are different numbers on the same physics, each
  with its own computed answer;
- checks each variant against the instance's declared `constraints`, so a variant that
  breaks the physics fails rather than rendering;
- runs the declared `independent_verification` as real arithmetic on a genuinely different
  expression, and rejects a "verification" that repeats a solving-route relation.

14 families are authored, spanning Motion 1D, motion under gravity, graphs, multiphase,
relative motion and projectile components. The engine holds arithmetic, route structure and
answer custody — and no Physics topic at all, so a new topic is a new data row.

Falsifiers: `WORKED_EXAMPLE_UNINSTANTIATED`, `WORKED_EXAMPLE_FINAL_ANSWER_MISSING`,
`WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE`, `VERIFICATION_ROUTE_NOT_INDEPENDENT`,
`INSTANCE_VARIANT_VIOLATES_DECLARED_CONSTRAINT`.

## Answer custody (P-UPGRADE-2 item 6)

Every learner-facing question resolves to three separate objects that may never collapse:

- `final_answer` — the resolved result, recomputed from the route;
- `quick_check` — one defining property, sign or unit;
- `independent_verification` — a genuinely distinct route to the same number.

Appendix A is a **protected attempt surface**: its items carry `answer_ref` only, and the
answers live in Appendix B. A `final_answer` beside an Appendix A question is
`ANSWER_LEAKS_INTO_PROTECTED_ATTEMPT_PAGE`.

Falsifiers: `LEARNER_QUESTION_WITHOUT_ANSWER`, `SELF_CHECK_SUBSTITUTED_FOR_ANSWER`,
`ANSWER_LEAKS_INTO_PROTECTED_ATTEMPT_PAGE`.

## Mandatory appendices

```text
Appendix A — Core Practice        guided/faded/independent per treatment
Appendix B — Core Solutions       one-to-one with A, reasoning + independent verification route
Appendix C — Printable Handout    answer-free, scope-bounded, grayscale/print-safe
```

## Running

```bash
python "Grade 9/V2/Physics/CoreAuthoring/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/CoreAuthoring/tests/test_physics_core1.py"
```

`tests/upstream.py` drives the real merged P-A → P-F chain in process, so P-G is proved
against genuine assessment-derived input rather than a stub.

## Non-claims

P-G authors semantic instructional material. It does **not** claim renderer quality, page
composition, authorized expert review, learning effectiveness, Core2 hint quality, or
publication readiness. PR #156 is not a producer input at this stage and contaminating the
profiles with it fails `PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON`.
