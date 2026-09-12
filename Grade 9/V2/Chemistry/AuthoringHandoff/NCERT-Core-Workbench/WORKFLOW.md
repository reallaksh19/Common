# Rebuild workflow for a novice agent

This file turns the lessons from the stress test into an explicit execution sequence.

## Phase 0 — choose the base correctly

This handoff is stacked on PR #322. Work from the branch containing this folder or rebase the folder after #322 lands. Do not copy only the PDFs; use the HTML + ledger + this workflow.

## Phase 1 — freeze the source denominator

### Input

A chapter/topic name plus an explicit list of source PDF URLs.

### Procedure

1. Open or parse every supplied PDF that could plausibly contain the requested topic.
2. Inventory question instances using a stable source identifier, for example `U3 Q26` or `SP1 Q34B`.
3. For each instance record:
   - `source_id`
   - `question_id`
   - `short_title`
   - `retained` boolean
   - `primary_topic`
   - `question_family`
   - `reason_if_excluded`
4. Freeze the denominator **before** authoring.
5. Reject any later build whose placed count differs from the retained denominator unless the ledger itself is intentionally revised.

### Required counters

```text
TOTAL_SCANNED
ELIGIBLE_IN_TOPIC
PLACED_UNIQUE
EXCLUDED_WITH_REASON
MISSING
DUPLICATE_PRIMARY
```

Required closure:

```text
ELIGIBLE_IN_TOPIC == PLACED_UNIQUE
MISSING == 0
DUPLICATE_PRIMARY == 0
```

## Phase 2 — derive capabilities and question families

Do not use one vague chapter label as the authoring schema. Group questions by the operation the learner actually has to perform.

Examples:

- classify matter by composition;
- convert units by dimensional factors;
- distinguish coefficient / subscript / charge;
- build an ionic formula by charge neutrality;
- convert mass → moles → particles;
- count ions per formula unit;
- calculate concentration with the correct denominator;
- track oxidation-number changes;
- distinguish redox from chemical-but-non-redox change.

Each retained question gets exactly one primary family, even when it touches multiple concepts. Secondary dependencies may be recorded but must not create duplicate primary placement.

## Phase 3 — assign visual obligations before prose

For each family choose the representation that reduces reasoning load.

Example mapping:

```text
CLASSIFY_MATTER                 -> MATTER_CLASSIFICATION_TREE / THREE_BUCKET_SORT
CONVERT_UNITS                   -> DIMENSIONAL_ANALYSIS_LADDER
READ_FORMULA                    -> FORMULA_ANATOMY_VIEW
BUILD_IONIC_FORMULA             -> CHARGE_BALANCE_BUILDER
COUNT_ATOMICITY                 -> ATOM_COUNT_MODEL
MASS_TO_MOLES                   -> MASS_MOLE_BRIDGE
MOLES_TO_PARTICLES              -> MOLE_PARTICLE_BRIDGE
COUNT_IONS                      -> ENTITY_MULTIPLIER_MODEL
CALCULATE_CONCENTRATION         -> PART_WHOLE_CONCENTRATION_MODEL
USE_STOICHIOMETRIC_RATIO        -> GIVEN_MOLES_RATIO_TARGET_FLOW
TRACK_REDOX                     -> OXIDATION_STATE_LANE / BEFORE_AFTER_MAP
VERIFY_CONSERVATION             -> ATOM_LEDGER
```

A representation is required when it helps the learner determine the next meaningful operation. Do not add decorative diagrams with no reasoning role.

## Phase 4 — author Core (1)

Core (1) is the study guide. For a full-learning topic family, the recommended teaching sequence is:

```text
Familiar context / anchor
→ See the idea (visual model)
→ Ordinary-language explanation
→ Rule / model / condition
→ Why / derivation / reconstruction
→ Worked example
→ Need a nudge? / first move
→ Watch for this (misconception repair)
→ Guided attempt
→ Faded attempt
→ Independent attempt
→ Verification / sense-check
→ Transfer / competitive reasoning
```

Do not force every heading onto every page. Preserve the learning functions, not a rigid cosmetic template.

### Core (1) question-check rule

Every learner-facing practice question must have a checking path. Prefer:

1. practice page;
2. nearby quick-answer page / strip;
3. later full worked solution.

Open-ended prompts require an expected-response rubric.

## Phase 5 — author Core (2)

Each retained source item gets one canonical question page.

Recommended page contract:

```text
Try the question
See the idea
Write this first
First nudge
Set it up on paper
Watch for this
Before you answer
Answer check — cover until finished
```

Then provide a separate full worked solution later.

### Helper language rule

A hint must be actionable. It should cause a visible learner action.

Bad:

> Use mole conversion.

Good:

> Write `n = m/M`. Put the given mass on top. Calculate the molar mass below it. Check that `g` cancels and `mol` remains.

Bad:

> Use the definition.

Good:

> First decide whether the sample is one pure substance or a mixture. If pure, ask whether it contains one kind of atom only (element) or different elements chemically combined in a fixed ratio (compound).

## Phase 6 — immediate answer checks

Required invariant for objectively checkable retained items:

```text
QUESTIONS_TOTAL == ANSWER_CHECKS_TOTAL == FULL_SOLUTIONS_TOTAL
```

The immediate answer should be concise enough not to become a second solution.

Examples:

- MCQ: `Correct option: (c)`
- Numerical: `311 K`
- Formula: `Ca3(PO4)2`
- Classification: list expected categories
- Short explanation: 2–4 required marking points

The full solution should expose the method line by line.

## Phase 7 — visual / notation QA

Check the rendered PDF, not only source text.

Fail the build or revise it if any of these occur:

- overlapping shapes or arrows;
- clipped cards / text;
- equations too small to read;
- ambiguous charge vs subscript;
- text-only helper where the family requires a diagram;
- diagram species not grounded in the source-authorized context;
- a visual that contradicts the prose;
- color is the only carrier of meaning;
- a question has no visible answer path.

## Phase 8 — typography target

Use PR #322's minimum font rule only as a hard lower bound. Aim for:

```text
body text               >= 10 pt
question stem           >= 12 pt
primary equation        >= 12 pt
visual annotation       >= 9 pt
footer / metadata       may be smaller if non-instructional
```

If density forces smaller learner text, split the page instead.

## Phase 9 — render and inspect

Run:

```bash
python tools/rebuild_pdf.py final/<topic>/core1.html final/<topic>/core1.pdf
python tools/rebuild_pdf.py final/<topic>/core2.html final/<topic>/core2.pdf
python tools/validate_handoff.py --root .
```

Then rasterize representative pages and inspect at least:

- cover / route page;
- one concept page from every Core (1) family;
- one Core (1) practice page;
- one Core (1) answer page;
- one Core (2) question page from every family;
- one Core (2) numerical solution page;
- one qualitative / classification solution page;
- last page / appendix closure.

## Phase 10 — report completion honestly

Report:

- retained denominator;
- placed count;
- immediate-answer count;
- full-solution count;
- exclusions / chapter-boundary decisions;
- page counts;
- known limitations;
- whether human gates have or have not been run.

Do not infer `MATURE_DESIGN_QUALITY` from machine closure alone.
