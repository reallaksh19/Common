# Physics learner-product maturity handoff — P-UPGRADE-2 (2026-09-13)

This directory is the durable handoff for the work on issue
[#353](https://github.com/reallaksh19/Common/issues/353), branch
`v2-physics-learner-product-maturity`, stacked on `v2-physics-core1a-publication` (PR #350).

It exists so that a fresh agent can continue without reconstructing the investigation:
what was built, what the machine can now prove, what it still cannot, the exact hashes of
the current-best artifacts, and the order the remaining work should be taken in.

**Release claim: `PUBLICATION_ENGINEERING` only.** `SUBJECT_CORRECTNESS`,
`PEDAGOGICAL_DESIGN`, `ASSESSMENT_DESIGN` and `VISUAL_USABILITY` are `PENDING`,
`REFERENCE_COMPARABILITY` is `NOT_RUN`, `MATURE_DESIGN_QUALITY` is `PENDING`. No human has
read these artifacts. Nothing in this directory is evidence of learning.

## Start here

1. `physics-learner-product-maturity-status.json` — the machine-readable status: every
   authority digest, every stage digest for both runs, artifact hashes, counts, the
   attempt-invariance table and the P-L release states.
2. `artifacts/` — the current-best learner PDFs and the reports they are bound to.
3. This README, sections *What changed* and *Known limitations*, before reusing anything.
4. To reproduce from scratch, nothing here is needed:

```bash
python "Grade 9/V2/Physics/ColdStart/engine/physics_cold_start_runner.py" --out-dir /tmp/phy
python "Grade 9/V2/Physics/ExactProduct/engine/audit_physics_exact_candidate.py" \
  --run-dir /tmp/phy/with-attempts --out /tmp/phy/ai_pre_review.json
python "Grade 9/V2/Physics/ExactProduct/engine/evaluate_physics_exact_product.py" \
  --run-dir /tmp/phy/with-attempts --ai-pre-review /tmp/phy/ai_pre_review.json
```

The cold start reads only `GENERATION_AUTHORITY_MANIFEST.json` and the repository
artifacts it names. There is no chat or issue history in the runtime input contract.

## Current-best artifacts

From the `with-attempts` run at head `e46ac563`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `artifacts/physics-core-study-guide.pdf` | 415299 | `9ecd078a2881ce8e43d3157192b869be927eeff6d212180e7b0418efb405fea5` |
| `artifacts/physics-transfer-solution-book.pdf` | 43495 | `ce829bb27f97f4ba077d2ca0676cad1278931cc0eba5385b613bda9f8525e1cf` |
| `artifacts/run_report.json` | 11807 | `e46f72e3b34ee0d6b7436b5d0fde593929cd0c647eb5eab00df1343cbb8d362f` |
| `artifacts/core1a_quality_report.json` | 17721 | `f1aa2d251b2e70b3279325556cbe3ee53dd911834cae6446610ef7b440f29b6e` |
| `artifacts/comparison.json` | 996 | `cefcef8543be9a83311265da880c139e6d93dbba17fdcdcd6424be98bfff6c1e` |
| `artifacts/exact_candidate.json` | 1564 | `ec2bba171cc7ed0b69bd43f16101caf5cfb157130dd2bdab1965c187933fdf4f` |
| `artifacts/exact_release.json` | 1499 | `b0683eab7479a3a145a70ea4bb79c0616504a89a644d3c5bd387a6754597232f` |
| `artifacts/ai_pre_review.json` (ADVISORY ONLY) | 2794 | `2071ed49b37ff832931be0611451822c54c7c7e01ceeceef952674bb086eba9f` |

Two products, never three: Appendix C is a section of the Core study guide.

| Product | Pages | Figures | Draw-time vector ops |
|---|---:|---:|---:|
| `CORE_STUDY_GUIDE` | 142 | 128 | 2302 |
| `TRANSFER_SOLUTION_BOOK` | 16 | 21 | 426 |

The `no-attempt` run produces 146 pages / 132 figures for the Core guide and a
byte-identical transfer book; the assessment-derived scope digest is identical across both
runs, which is the P-K invariant.

## Authority digests

| Authority | Digest |
|---|---|
| `GENERATION_AUTHORITY_MANIFEST.json` | `d848f8346106df3858b6d8c63e99171961ec455320dc1e311b81dcdab060c0ca` |
| P-A0 source question ledger | `0eccb4a5efbce35ae1aa7c2cc7c813b260e6269f3c15107931417cc11c060c89` |
| P-G authored-instance registry | `a065a36379a7c21b721964636c168bcd6eebb096012b1a5844093f9ed4038baa` |
| P-H teaching-primitive registry | `9361cfa8242d4241bedbff6e83cf6bcb92553596cbbc0251859c00f18bfe192d` |
| Core (1A) learner-language registry | `PHY-CORE1A-LEARNER-LANGUAGE-v2` |

Stage digests for both runs are in the status JSON.

## What changed

### 1. Core (1A) is the published Core study guide (P-K wiring)

P-K no longer calls `render_core_study_guide` directly. It compiles the P-G plan through
the P-GA Core (1A) publication compiler and renders that — #350's own stated next step.
The artifact name, product id, required sections and the two-product topology are
unchanged, and Core (1A) took on the custody obligations the old renderer carried:
`render_core1a` returns a real `PhysicalPageMap` built from draw-time evidence, and every
representation the P-H bundle declares for a capability is physically placed (128/128)
rather than only the two that fit the designed spread.

### 2. P-A0 source question reconciliation ledger (new phase)

The independent denominator. Completeness used to be proved relative to whatever P-A
extraction produced, so a dropped source item was invisible — the NLM defect where three
direct Unit-9 items had no home while concept coverage read as complete. The ledger is
frozen from the source documents before authoring, declares
`derived_from_question_set: false`, and P-J cannot reach `CLOSED` without a `RECONCILED`
report against it. The P-J test proves the blind spot directly: drop an item from the
question set and the question-set denominator still shows zero uncovered while the ledger
names the missing item.

### 3. A worked example resolves to an actual number

`CoreAuthoring/registry/physics-authored-instances.json` (14 families, data) plus
`engine/physics_instance_resolver.py` (the engine, no Physics in it). Every learner-facing
question carries a resolved instance: situation, declared frame, typed givens, one unknown,
a typed `reasoning_route`, a computed answer. The resolver evaluates each `EXECUTE` state
with a restricted `ast` evaluator and **recomputes** the answer rather than trusting it;
proves the route transforms state; expands declared per-given value lists into deterministic
variants so worked/guided/faded/independent/retry/Appendix A are different numbers on the
same physics; and runs the declared independent verification as real arithmetic on a
genuinely different expression.

This is what makes `CORE1A_TEMPLATE_ONLY_CONTENT` stop firing **for real**: the Core (1A)
quality report is findings-free and `instructional_content_maturity` is
`READY_FOR_HUMAN_REVIEW` — meaning ready for a human to read it, not reviewed.

### 4. The hint ladder projects the shared reasoning route

H1/H2/H3 are projections of the same route-state object P-G authors
(`physics-instance-route-state.schema.json`, one schema, two phases): H1 ← `REPRESENT` as
`ATTENTION_CUE`, H2 ← `MODEL` as `MODEL_REPRESENTATION`, H3 ← `FRAME` as
`FIRST_MOVE_OVERLAY`. The solution's sections project the same states. For a spatial family
the ladder is diagram-first — 7 of 8 transfer pages and 24 hint-figure projections, of which
21 are physically placed and 4 are grounded in the source item's own preserved
`figure_semantic`.

### 5. The bbox is a hard boundary

The allocation is installed as a clip path around every `render_primitive` call. The ink
box became a real bound (path and Bezier control points, arc extents, measured text width
with font ascent/descent) instead of an anchor sample. Every primitive declares measured
size floors and `supports_compact_variant`, and a smaller allocation is refused. Two
genuine bounds defects the new measurement exposed were fixed in the primitives
themselves. Zero placements escape their allocated box at zero tolerance across all 128
Core-guide figures.

### 6. Answer custody

Answer, quick check and independent verification are three separate objects everywhere,
and may not collapse. Appendix A and the Core (2) question pages are protected attempt
surfaces: `answer_ref` only. Core (2) resolves to the **source's own** answer key with
`authored_by_core2: false`.

### 7. Kid-appropriate learner copy

Extends #350's `physics-core1a-learner-language.json` rather than duplicating it — see
*How this reconciled with #350* below. `INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE` scans
rendered PDF text for clinical role labels in prose, which the identifier-shape scan cannot
see. It immediately caught four real leaks from teaching primitives' own default titles;
both learner renderers now supply the governed figure heading instead.

## How this reconciled with #350

The base branch moved 25 commits while this work was in flight, growing from 7 files to 23
and adding `CORE1A_UI_SPEC.md`, a Core (1A)↔Core (2) linkage registry, a Motion-in-a-Plane
chapter build, and `registry/physics-core1a-learner-language.json`.

- The branch was rebased onto the new tip (`e4c7f5db`) with no conflicts.
- Item 7 had been building a parallel copy registry. That file is **deleted**; its 45
  additional roles (route states, hint levels, Core (2) solution sections, support stages,
  readiness/probe roles) are folded into #350's registry, which is now the single governed
  vocabulary at `PHY-CORE1A-LEARNER-LANGUAGE-v2` with 59 module labels, 43 banned terms and
  19 figure titles.
- Where #350 already defined a label, that label is kept verbatim, and a test pins the five
  it shipped. This extends the incumbent vocabulary; it does not restyle it.
- The ban list is the union of #350's banned words and the clinical curriculum-design
  phrases item 7 names. Ordinary school vocabulary the governed labels themselves use
  ("worked example", "guided practice") is deliberately **not** banned: the target is
  curriculum-design jargon, not normal textbook English.
- #350's `learner_ui`, `difficulty` and `raw_math_strings_forbidden` policy and its
  `test_core1a_ui_policy.py` are untouched and still pass.

## Known limitations

- **No human has read any of this.** Every subject, pedagogy, assessment and visual state
  is `PENDING`. The P-L gate exits 2 (BLOCKED) by design and the AI pre-review is
  `ADVISORY_ONLY` and structurally incapable of setting a quality state.
- **The source ledger is a synthetic-fixture ledger.** The repository's Motion source is a
  synthetic fixture with no separate source PDF in-tree, so the ledger declares
  `ledger_class: SYNTHETIC_FIXTURE_LEDGER` and `production_claim: false`, and the validator
  rejects it if it ever claims otherwise. For a real source it must be transcribed from the
  source document before P-A extraction. The mechanism is identical either way.
- **Most figures are still schematic.** The AI pre-review raises
  `MOSTLY_SCHEMATIC_FIGURES`: only a minority of Core-guide figures carry quantities
  extracted from the source. The authored instances now carry real numbers, but those
  numbers are not yet threaded into the P-H representation bundle's `render_params`, so the
  worked example's diagram is structurally right and quantitatively generic. **This is the
  highest-value next step.**
- **Core (2) routes carry no numbers.** The source body is preserved exactly and Core (2)
  may not invent quantities, so its route states have `equation: null` and declared-state
  outputs. The hint ladder is a real projection of a real route, but it is not a resolved
  numeric route like P-G's.
- **`PHY-PF-PROJECTILE-COMPONENTS` is authored but unreached.** It resolves and is tested
  (it is the cross-topic genericity proof, using trigonometry through the same schema), but
  no capability in the Motion fixture binds to it, so it never appears in a rendered
  product. Motion-in-a-Plane content on #350 is where it becomes live.
- **Occupancy remains an advisory signal.** 23 of 142 Core-guide pages are below the 70%
  target (the lesson opening spreads, the cover and the appendix tails). The policy
  tolerates up to 25%; this is not a proof of good page rhythm.
- **Item 7 is enforced on text, not on rendered pixels.** The scan reads `pdftotext`
  output. Overlapping labels, clipped badges and broken glyphs are not caught by it —
  `CORE1A_UI_SPEC.md` §5 is right that a release candidate needs rendering to page images
  and human inspection.

## Next steps, in order

1. **Thread the authored instances' real quantities into the P-H representation bundle.**
   `build_physics_representations` should read the resolved instance for a lesson and set
   `render_params` from its givens, with `quantitative_grounding: SOURCE_QUANTITIES` where
   the numbers come from a source item. This removes `MOSTLY_SCHEMATIC_FIGURES` and makes
   the worked example's diagram show the worked example's own numbers. Everything needed is
   already in the plan.
2. **Render to page images and inspect.** Per `CORE1A_UI_SPEC.md` §5: text bounds, badge
   clipping, label overlap, blank pages. Add the collision checks as falsifiers; the
   TracingCanvas ink boxes now make intra-figure occupancy measurable.
3. **Wire the Core (1A)↔Core (2) linkage registry into the rendered products** so the
   `CHECK → APPLY → TRANSFER` gateway and the exact repair target appear on the page, and
   `CORE1A_NO_CORE2_MASTERY_LINK` / `CORE1A_CORE2_REPAIR_TARGET_MISMATCH` become live rather
   than declared.
4. **Author instances for the Motion-in-a-Plane families** #350 added. The schema and
   resolver are subject-wide generic and the projectile-components instance is the worked
   proof; this is data authoring, not engineering.
5. **Raise body type to the 10.5–11 pt spec target.** The renderer is at 10.2 pt, above the
   10.0 pt floor but below `body_font_target_pt`. It is a layout retune, not a new
   mechanism.
6. **Then, and only then, seek authorized human review.** The machine gates cannot move the
   four human states, and no amount of further engineering will.

## Falsifiers added by this work

| Code | Phase | Catches |
|---|---|---|
| `SOURCE_ITEM_MISSING_FROM_QUESTION_SET` | P-A0 | extraction dropped a source item review did not exclude |
| `QUESTION_SET_ITEM_NOT_IN_SOURCE_LEDGER` | P-A0 | an item not from the declared source, or a stale ledger |
| `DIRECT_SOURCE_ITEM_WITHOUT_COVERAGE_HOME` | P-A0 | a direct item with no lesson, practice item or exclusion |
| `COVERAGE_PROVEN_ONLY_AGAINST_ITSELF` | P-A0/P-J | closure claimed with no independent denominator |
| `SOURCE_LEDGER_DERIVED_FROM_QUESTION_SET` | P-A0 | a ledger generated from the artifact it audits |
| `SOURCE_LEDGER_NOT_FROZEN_BEFORE_AUTHORING` | P-A0 | a ledger written after the fact |
| `SOURCE_LEDGER_DIGEST_MISMATCH` | P-A0 | the frozen listing was edited |
| `SOURCE_LEDGER_IS_SYNTHETIC_CLAIMED_AS_PRODUCTION` | P-A0 | a fixture ledger presented as real |
| `WORKED_EXAMPLE_UNINSTANTIATED` | P-G | a worked example that is still an authoring plan |
| `WORKED_EXAMPLE_FINAL_ANSWER_MISSING` | P-G | no resolved result, or one the route never produces |
| `WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE` | P-G | a route that restates its givens |
| `VERIFICATION_ROUTE_NOT_INDEPENDENT` | P-G | a "check" that repeats the solving relation, or disagrees |
| `INSTANCE_VARIANT_VIOLATES_DECLARED_CONSTRAINT` | P-G | a variant that breaks the instance's own physics |
| `LEARNER_QUESTION_WITHOUT_ANSWER` | P-G/P-I | a question resolving only to a hint or a check |
| `SELF_CHECK_SUBSTITUTED_FOR_ANSWER` | P-G/P-I | answer, quick check and verification collapsed |
| `ANSWER_LEAKS_INTO_PROTECTED_ATTEMPT_PAGE` | P-G/P-GA/P-I | an answer beside its own question |
| `HINT_NOT_PROJECTED_FROM_ROUTE_STATE` | P-I | a hint authored independently of the route |
| `SPATIAL_FAMILY_HINT_WITHOUT_REPRESENTATION` | P-I | prose about a diagram the learner never sees |
| `CORE2_INVENTS_FIGURE_QUANTITY` | P-I | a hint diagram carrying a number the source never stated |
| `PRIMITIVE_INK_ESCAPES_ALLOCATED_BBOX` | P-H | a primitive drawing outside its allocation |
| `TRACING_BBOX_INCOMPLETE_FOR_PATH_OP` | P-H | an unmeasured path op, so the ink box is not a bound |
| `PRIMITIVE_MIN_SIZE_VIOLATION` | P-H | a figure squeezed below the size it needs to teach |
| `INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE` | P-GA/P-L | curriculum-design jargon on a Grade-9 page |

## What this handoff is not

It is not a release, not a canonical package, and not a substitute for the repository's
P-A0→P-L authority chain. The PDFs are worked design evidence and regression fixtures,
bound to the exact hashes above. If any authority digest in the status JSON no longer
matches the repository, the artifacts here are stale: re-run the cold start and replace
them deliberately.
