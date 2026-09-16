# Mathematics V2 — SourceLedger (M-UPGRADE-2 item 3)

Top-level question count is not a completeness measure. The seven-topic stress test produced
three *independent* completeness failures, so this phase gates three layers separately.

```text
SOURCE CORPUS COMPLETENESS      every top-level source row is present
        +
ATOMIC ASK COMPLETENESS         every subpart / proof obligation / option / condition
        +
RENDERED ASSESSMENT COMPLETENESS  every one of those is visible after layout
```

## Why each layer exists

| Topic | What happened | Why the previous layer could not see it |
| --- | --- | --- |
| Number Systems | an upstream omission went undetected | completeness was measured against the *supplied* `question_set`, which is self-relative |
| Polynomials | `72/72` questions did **not** mean `151/151` asks | a compound question loses a subpart while its top-level count stays unchanged |
| Linear Equations | options C and D were covered by the next panel | the pre-render JSON compared equal; the learner still could not read them |

## The frozen manifest

`math-source-corpus-manifest.schema.json` is established `BEFORE_AUTHORING` and freezes
both dimensions. `freeze_manifest()` **derives** `required_question_refs[]` and
`required_atomic_ask_refs[]` from the corpus rows rather than trusting them as input, so a
manifest cannot claim completeness it does not describe — and `SOURCE_CORPUS_MANIFEST_DIGEST_DRIFT`
catches a later quiet edit.

Atomic-ask kinds are subject-wide generic (`registry/math-atomic-ask-kind-registry.json`).
A topic never adds a kind; it only supplies instances. Each kind records *how it loses
silently*, which is the reason it is tracked at all:

```text
SUBPART               a compound question rendered with only its first part
OPTION                an option set truncated, or covered by a later panel
PROOF_OBLIGATION      "prove ... and hence deduce ..." keeping only the first deduction
PARAMETER_CONDITION   "for which values of k" dropped, turning underdetermined into unique
UNIT_REQUIREMENT      "give your answer in cubic centimetres" dropped
JUSTIFICATION         "give a reason" dropped, and the item becomes recall
CONSTRUCTION_STEP     the figure kept, a required step lost
COUNTEREXAMPLE_REQUEST  a universal claim losing its "or give a counterexample" branch
```

## The rendered witness

`math-rendered-object-map.schema.json` records what the renderer actually placed — page,
box, paint order, opacity, text, typography role and font size. The witness then:

1. requires a placed object for every learner-visible atomic ask;
2. fails `ASSESSMENT_OBJECT_CLIPPED` if a box leaves the printable area;
3. fails `ASSESSMENT_OBJECT_OCCLUSION` if a later-painted **opaque** object covers more
   than 5% of an assessment object (deliberately low: a partly covered option is unusable);
4. fails `RENDERED_SOURCE_OPTION_COVERAGE_GAP` if the atomic ask's text is not extractable
   from the rendered page at all — text a learner cannot read is text that is missing.

`engine/render_attempt_probe.py` is a deterministic attempt-page probe renderer so the
witness is exercised against a real PDF rather than a hand-written map. It has three
deliberate defect modes, and each reproduces a stress-test failure:

```text
occlude_after_option="(B)"   paints the following panel over options C and D
drop_atomic_ask="Q1#OPT-D"   omits one required atomic ask entirely
clip_atomic_ask="Q3#COND"    places one object outside the printable area
```

The occlusion test asserts something worth stating explicitly: after the mutation the
option text `(4, 0)` and `(1, 2)` is *still present in the extracted page text*, and the gate
still fails. That is the difference between "the data is complete" and "the learner can read
it".

## The reconciliation block

`reconcile()` never raises; it reports. `audit_source_completeness()` is the fail-closed
wrapper. The ledger carries the block the consolidated review asked for:

```text
required source rows      included source rows
required atomic asks      included atomic asks
concept-linked            core1-evidence-linked
solution-complete         verification-complete
render-visible            unresolved[]
```

`status` is `PASS` only when `unresolved` is empty.

## Falsifiers

```text
CORE2_SOURCE_CORPUS_COVERAGE_GAP
CORE2_ATOMIC_ASK_COVERAGE_GAP
CORE2_SUBPART_SHAPE_DRIFT
SOURCE_CORPUS_NOT_FROZEN_BEFORE_AUTHORING
SOURCE_CORPUS_MANIFEST_DIGEST_DRIFT
RENDERED_SOURCE_OPTION_COVERAGE_GAP
ASSESSMENT_OBJECT_OCCLUSION
ASSESSMENT_OBJECT_CLIPPED
SOURCE_LEDGER_GATE_FAILED
```

## A note on the fixture

`fixtures/math-source-corpus.fixture.json` is a **source-shape probe**, not a vendored NCERT
extract. It reproduces the four shapes that lost content during the stress test (a
four-option MCQ, a two-obligation proof item, a multipart item with a parameter condition,
a modelling item with a unit requirement) so the dimensions are exercised without restating
source content. The official units remain the authority named in the #345 handoff, and the
manifest records `vendored: false` explicitly.

## Release meaning

`PUBLICATION_ENGINEERING` only. A reconciled ledger is evidence that nothing was silently
dropped. It is not a subject, pedagogy, assessment or expert-review PASS, all of which
remain `PENDING`.
