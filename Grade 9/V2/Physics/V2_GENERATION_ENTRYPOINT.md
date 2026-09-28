# Physics V2 — generation entrypoint (cold start)

Read this file and `GENERATION_AUTHORITY_MANIFEST.json`. Between them they are sufficient:
**no chat history, no issue history and no manually pre-computed intermediate is required or
permitted.** If you find yourself needing one, that is a defect in this document, not a
reason to proceed.

## One command

```bash
python "Grade 9/V2/Physics/ColdStart/engine/physics_cold_start_runner.py" \
  --out-dir /tmp/physics-v2-cold-start
```

That drives the whole chain twice over the *same* assessment — once with no `AttemptSet`
and once with one — and writes, per run:

```text
<out>/no-attempt/      physics-core-study-guide.pdf
                       physics-transfer-solution-book.pdf
                       run_report.json  + every intermediate artifact
<out>/with-attempts/   the same, with learner attempt evidence applied
<out>/comparison.json  the two-run invariant comparison
```

Independently validate a run:

```bash
python "Grade 9/V2/Physics/ColdStart/engine/physics_cold_start_validator.py" \
  --report /tmp/physics-v2-cold-start/with-attempts/run_report.json
```

## The chain

| phase | directory | produces |
|---|---|---|
| P-A | `AssessmentIntake` | QuestionSet, DeclaredTopicScope, AttemptSet (optional) |
| P-B | `AssessmentReview` | item validity and diagnostic-use review |
| P-C | `AssessmentScope` | scope authority, question/capability bindings |
| P-D | `ProblemSemantics` | problem families, reasoning routes, verification routes |
| P-E | `LearnerEvidence` | LearnerStateSnapshot (identical shape with or without attempts) |
| P-F | `StudySynthesis` | LearnerStudyScope + LearnerStudyModel + longitudinal init |
| P-G | `CoreAuthoring` | promoted-pilot PCK + Core1 study plan + Appendices A/B/C |
| P-H | `Representation` | teaching-primitive registry, representation bundle, PhysicalPageMap |
| P-I | `Core2Transfer` | transfer pages, H1/H2/H3 hint ladder, First-Step Reference |
| P-J | `CoverageClosure` | coverage matrices, longitudinal update, publication closure |
| P-K | `ColdStart` | this runner, the authority manifest, the two learner PDFs |
| P-L | `ExactProduct` | exact-product quality gates and the mature-candidate state model |

## What must be identical across the two runs

The assessment decides **what must be teachable**; learner evidence decides only
**order, depth, bridge, treatment and support**. So these are byte-identical in both runs
and the comparison fails if any differs:

```text
question set digest          declared topic scope digest      scope authority digest
external corpus digest       problem semantics digest         study scope digest
required capability set      required item set                problem family truth
physical model truth         law truth                        external eligibility
two-product topology
```

These are *expected* to differ, because that is what learner evidence is for:

```text
study model digest    core1 plan digest    lesson mode counts
```

## Two products, never three

```text
CORE_STUDY_GUIDE          main teaching + Appendix A practice + Appendix B solutions
                          + Appendix C printable handout
TRANSFER_SOLUTION_BOOK    transfer questions + hint ladders + full solutions
```

Appendix C is a **section of the Core study guide**, not a third PDF. Emitting it
separately fails `THIRD_PRODUCT_PDF_CREATED`.

## Boundaries you must not cross

- **PR #156 is not a producer input.** It is a merged Physics pilot outside this V2 chain
  and is admissible only at P-L, as a final design comparator, after every required review
  gate has been resolved. Any producer read of it fails
  `PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON`.
- **`Grade 9/V2/Physics/Publication/` and `Grade 9/V2/Physics/LearningDesign/` are legacy.**
  They belong to the pre-assessment-gate chain (#221–#233) and must not be wired into any
  phase above. See their `README_LEGACY_QUARANTINE.md`.
- **Human review states cannot be set by this repository.** `SUBJECT_EXPERT_PASS`,
  `PEDAGOGY_EXPERT_PASS`, `ASSESSMENT_EXPERT_PASS` and `VISUAL_USABILITY_EXPERT_PASS`
  require an authorized human reviewer and an attestation bound to exact artifact bytes.
  They are all `PENDING`. Marking one `PASS` fails `FAKE_HUMAN_REVIEW_STATE`.

## Current honest state

The chain runs end to end and produces two real PDFs in both modes, with every figure drawn
as actual vector graphics and reconciled to physical-page custody. It has had **no human
subject, pedagogy, assessment or visual review of any kind**. It is not a mature product and
P-L will report `BLOCKED_PENDING_AUTHORIZED_REVIEW_OR_EXACT_ARTIFACT` until that changes.
