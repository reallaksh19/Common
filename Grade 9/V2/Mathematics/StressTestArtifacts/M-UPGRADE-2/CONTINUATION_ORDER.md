# Continuation order after M-UPGRADE-2

Read `README.md` and `STATUS.json` in this directory first, and #345's `PR323/README.md`
and `PR323/STATUS.json` before either. This file is the exact next-step order, highest value
first. Each step names what "done" looks like so a later agent does not have to re-derive it.

---

## 1. Wire the gates into `LearnerProduct`'s `STAGE_RUNNERS` (highest value)

`LearnerProduct/engine/run_learner_product.py` holds the ordered LP-00..LP-17 contract and
an intentionally empty `STAGE_RUNNERS`. Every phase built by #358 is a callable library with
a fail-closed entry point, so the wiring is mechanical:

| LP stage | gate to install |
| --- | --- |
| `LP-02 BUILD_CORE1A_REPRESENTATIONS` | `validate_math_spatial_semantics.audit_spatial` |
| `LP-03 REALIZE_CORE1A` | `validate_core1_reconstruction.audit_reconstruction` |
| `LP-04 MAP_CORE2_TO_CORE1A` | the cross-core bridge from the same module |
| `LP-05 PRESERVE_CORE2_SOURCE` | `build_math_source_ledger.audit_source_completeness` |
| `LP-11..LP-13 AUTHOR_*` | `learner_realization.audit_realizations` |
| `LP-15 RENDER_LEARNER_PRODUCTS` | `math_expression.audit_expressions` |
| `LP-16 VISUAL_PREFLIGHT` | `validate_layout_safety.assert_layout_safe` + the rendered coverage witness |
| `LP-17 FINAL_AUDIT` | all of the above, emitted as the artifact manifest |

**Done looks like:** a run manifest executes end to end and `LP-17` emits one audit bundle
containing every phase's status, with no stage bypassing its gate.

---

## 2. Make `LP-15` emit a `math-rendered-object-map`

Both post-render gates (source-ledger coverage and layout safety) audit an object map, and
today only the two committed probes emit one. The real renderer must emit it as it places
objects: `object_id`, `kind`, `question_ref`, `atomic_ask_ref`, `page`, `paint_order`,
`opaque`, `box`, `text`, `typography_role`, `font_size_pt`, `container_id`,
`content_height_pt`, `response_mode`.

`SourceLedger/engine/render_attempt_probe.py` is the reference for how to accumulate it
while drawing. Note the `container_id` discipline: without it every child overlapping its
own panel reads as a collision.

**Done looks like:** the production renderer's map validates against
`math-rendered-object-map.schema.json` and passes both post-render audits.

---

## 3. Route Core1A's mathematics through `MathTypesetting`

`Core1A/engine/build_math_core1a_textbook.py` still renders learner mathematics through its
own `safe_text()`, and `Publication/engine/realize_math_core_products.py` still defines and
uses `ascii_safe()`. Neither was removed by #358, because removing the flattening function
without a replacement renderer would change #323's rendered product.

The replacement path already exists: build the expression as a `MathExpression` AST and draw
it with `Typesetter.measure(...).draw(...)`.

**Done looks like:** `ascii_safe()` has no callers, `detect_flattening()` returns `[]` for
every page of the real Core1A PDF, and the geometric script check (a reduced-size span at
the declared ratio) passes on it.

---

## 4. Extend the reference realizations to the remaining three topics

Euclid's Geometry, Lines & Angles and Surface Areas & Volumes currently appear only as
*shapes* in the source-ledger probe. They are the three that exercise the parts of the
contract the existing four do not:

- **Euclid** — `answer_kind: PROOF`, so `model_proof_steps` with `licensed_by` per step is
  exercised for real (proof grammar: `GIVEN → licensed fact → derived statement →
  conclusion`);
- **Lines & Angles** — the `ANGLE_FIGURE` spatial primitive and a theorem whose converse is
  genuinely needed by Core2, so `CONVERSE_USED_WITHOUT_BEING_TAUGHT` is exercised against
  real content;
- **Surface Areas & Volumes** — `UNIT_REQUIREMENT` atomic asks, `DIMENSIONAL_UNIT_CHECK` and
  `CONSERVATION_CHECK` verification kinds, and the missing `SOLID` spatial primitive.

**Done looks like:** seven topics in the realization corpus, and the audit bundle reporting
seven under `topics`.

---

## 5. Add the `SOLID` spatial primitive

`SOLID_SURFACE_SELECTION_MISMATCH` is named in the consolidated review and is the one
figure-semantics gate #358 did not implement. It needs exposed / contact / removed surface
roles, dimensions attached to the correct geometric entity, and composite-solid
decomposition validity — plus the same `learner_must_supply` separation the other
primitives have.

---

## 6. Reconcile the seven-topic frozen corpora

The source ledger runs against a 4-row / 12-ask probe. The real frozen corpora for the seven
topics are described in #345's `PR323/STATUS.json` and `ARTIFACT_SHA256.txt`. Import them,
freeze each with `freeze_manifest()`, and reconcile the authored plans against them.

**Done looks like:** a per-topic ledger with `status: PASS` and an empty `unresolved` list,
committed beside the handoff.

---

## 7. Strengthen the equivalence witness from asserted to computed

Today the engine checks that a witness exists, carries a precondition, actually changes the
relation, and declares reversibility honestly. It does **not** verify symbolically that the
solution set is preserved. For the Grade 9 families in scope (linear equations, surds,
polynomial factorisation) a small checker is tractable and would turn
`EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS` from a structural gate into a
mathematical one.

---

## What NOT to do

- **Do not** build a second learner-language ban-list.
  `LearnerProduct/policies/math-learner-language-policy.json` is the authority; extend it in
  place and keep `policy_id` stable so `run_learner_product.py`'s binding check resolves.
- **Do not** add a topic-specific schema shape. Every topic in this work is a data instance
  of one subject-wide contract, and that is load-bearing: the cross-item transplant check
  and the cross-core bridge both depend on it.
- **Do not** copy the mathematics out of the golden `theory-of-equations` fixture or out of
  this work's reference corpus into a new topic. Copy the *sequence*; synthesize the content
  from governed Core1 capability/PCK/problem-family authority.
- **Do not** mark any PCK beyond `PROVISIONAL_PROMOTED` or record any expert review. No gate
  in this lineage can assert one, and none should learn how.
- **Do not** restart from the compact Core1 pattern. That was one of the central stress-test
  failures and `CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE` now refuses it.
