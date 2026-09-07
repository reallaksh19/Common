---
name: grade9-subtopic-completeness-auditor
description: Audit one Grade 9 learning subtopic before publication for source coverage, instructional completeness, textbook-reference learning rhythm, context bridges, concept helpers, misconception repair, scaffolded practice, external/PYQ transfer coverage, chemistry typography, and rendered layout quality. Use after a subtopic draft exists and before declaring its Study Guide or transfer book complete.
---

# Grade 9 Subtopic Completeness Auditor

Audit the **whole learning experience**, not only whether the right facts appear somewhere.

Run this skill together with `grade9-transfer-coverage-auditor` whenever an external corpus such as ExamSIDE is part of the brief.

## Core completion rule

A subtopic is complete only when all five directions agree:

```text
SOURCE -> STUDY GUIDE
STUDY GUIDE -> LEARNER REASONING
LEARNER REASONING -> PRACTICE / TRANSFER
ELIGIBLE TRANSFER QUESTIONS -> STUDY SUPPORT
RENDERED PDF -> INTENDED LEARNING EXPERIENCE
```

A generated PDF is not evidence of completion.

Final gate:

```text
SOURCE = PASS
PEDAGOGY = PASS
TRANSFER = PASS       # when applicable
TYPOGRAPHY = PASS
LAYOUT = PASS
```

---

## 1. Required subtopic record

```json
{
  "subtopic_id": "RX-ST01",
  "title": "Oxidation Number",
  "source_obligation_ids": [],
  "concept_ids": [],
  "instructional_weight": "CORE",
  "familiar_context_ids": [],
  "concept_helper_ids": [],
  "misconception_ids": [],
  "worked_example_ids": [],
  "guided_practice_ids": [],
  "faded_practice_ids": [],
  "independent_check_ids": [],
  "required_external_question_ids": [],
  "render_artifact_ids": [],
  "status": "PASS"
}
```

Stable IDs are authoritative. Rendered page numbers are derived metadata only.

---

## 2. Reference-book instructional grammar

When the user provides textbook/reference snapshots, imitate the **learning grammar**, not decorative boxes or fonts.

Default sequence:

```text
ORIENT / FAMILIAR CONTEXT
-> EXPLAIN THE IDEA IN ORDINARY LANGUAGE
-> SHOW WHAT IT MEANS VISUALLY / SYMBOLICALLY
-> THINGS TO KNOW / KEY RULE
-> WORKED EXAMPLE WITH REASONING STORY
-> CONCEPT HELPER / REPRESENTATION
-> MISCONCEPTION CLINIC / CLOSE CONTRAST
-> TRY WITH ME
-> FADED PRACTICE
-> CHECK YOUR KNOWLEDGE
-> TRANSFER LINK
```

Not every page needs every module. The **subtopic as a whole** must provide the required learning functions.

### Narrative-before-procedure

For a genuinely new concept:

```text
meaning -> interpretation -> example -> rule/procedure
```

Do not lead with a long algorithm before the learner knows what the algorithm is doing.

### Connected-spread rule

A learning spread should read as one teacher explanation, not a dashboard of independent cards.

Use boxes only when they perform a teaching job such as:

- definition;
- key rule;
- contrast;
- helper;
- misconception repair;
- worked example;
- knowledge check.

If several boxes can be removed without changing the reasoning sequence, the page is likely over-fragmented.

---

## 3. Familiar / real-life bridge

For each `CORE` subtopic, include at least one truthful familiar-context bridge when one is available without introducing new chemistry.

Status:

```text
PEDAGOGICAL_BRIDGE
```

Examples:

- an everyday formula label used only to make a formula familiar;
- an ordinary material/reaction already supported by source scope used to motivate a symbolic idea;
- a visible macroscopic situation used only as a recognition hook.

Checklist:

- [ ] Accurate.
- [ ] Understandable at target level.
- [ ] Clarifies the source concept.
- [ ] Introduces no new chapter dependency.
- [ ] Treated as a bridge, not as source authority.

If no safe bridge exists, record `FAMILIAR_CONTEXT_NOT_APPLICABLE` with a reason. Never invent an application merely to satisfy the checklist.

---

## 4. Concept-helper audit

A helper answers one of:

```text
What should I notice?
What should I mark?
What should I draw?
What should I think about first?
What representation makes this easier?
```

High-recognition-load concepts require at least one reusable helper.

Useful helper types include:

- formula anatomy;
- rule-priority ladder;
- charge-balance visual;
- before -> after oxidation-state lane;
- SELF vs OTHER agent frame;
- Redox Decision Strip;
- split/converge topology;
- average-vs-actual site diagram;
- per-atom electron-change lane.

Checklist:

- [ ] Reveals the representation, not the final answer.
- [ ] Uses the same reasoning language as examples/hints.
- [ ] Reusable across several questions.
- [ ] Visually distinguishable from decoration.
- [ ] Placed near the point where the learner needs it.

---

## 5. Misconception audit

High-risk concepts require explicit misconception repair.

Each misconception should contain:

```json
{
  "misconception_id": "RX-M01",
  "wrong_model": "oxygen is always -2",
  "observable_error": "assigns -2 in peroxide/superoxide/O-F cases",
  "diagnostic_question": "...",
  "repair_explanation": "...",
  "micro_contrast": "...",
  "retry_check": "..."
}
```

Checklist:

- [ ] Names a specific wrong mental model.
- [ ] Uses a close contrast or micro-example.
- [ ] Explains why the wrong model fails.
- [ ] Includes a retry/transfer check where appropriate.

Generic `be careful` warnings do not count.

---

## 6. Worked-example quality

A worked example must tell a reasoning story:

```text
READ THE GIVEN
-> IDENTIFY WHAT IS ALREADY KNOWN
-> BUILD / CHOOSE THE REPRESENTATION
-> EXECUTE THE RULE
-> STATE THE RESULT
-> CHECK / INTERPRET
```

For chemistry formulas, explicitly distinguish:

- subscripts = atom counts;
- superscripts = ionic charge;
- oxidation numbers = separate assigned values.

A worked example that only presents algebra and an answer is incomplete.

---

## 7. Practice and scaffold audit

For each CORE concept require, where applicable:

- one worked example;
- one `TRY WITH ME` item;
- one faded-scaffold item;
- one independent item;
- one `CHECK YOUR KNOWLEDGE` item.

Preferred progression:

```text
FULL SCAFFOLD -> FADED SCAFFOLD -> TRANSFER
```

The independent check must not merely repeat the exact surface form of the worked example.

---

## 8. External/PYQ transfer audit

When an external corpus is part of the project, invoke `grade9-transfer-coverage-auditor`.

Block the subtopic unless:

```text
SUBTOPIC_REQUIRED = n
SUBTOPIC_PLACED + SUBTOPIC_DEFERRED_VALID = n
SUBTOPIC_MISSING = 0
SUBTOPIC_WRONG_PLACEMENT = 0
SUBTOPIC_CONCEPT_LINK_FAILURES = 0
SUBTOPIC_HINT_FAILURES = 0
SUBTOPIC_SOLUTION_FAILURES = 0
SUBTOPIC_BROKEN_SOURCE_LINKS = 0
SUBTOPIC_SCOPE_LEAKS = 0
```

At final chapter acceptance, `DEFERRED_VALID = 0`.

A Study Guide supports a transfer question only when it teaches the question's:

- recognition cue;
- first move;
- representation;
- misconception repair when high-risk;
- prerequisite concepts.

A topic-label match is not sufficient.

---

## 9. Chemistry typography audit

Chemistry notation is a blocking publication requirement.

Required checks:

- [ ] Formula indices are true/clear subscripts, e.g. `H₂O₂`, `K₂Cr₂O₇`.
- [ ] Ionic charges are true/clear superscripts, e.g. `Fe³⁺`, `Cr₂O₇²⁻`.
- [ ] Oxidation numbers above atoms are visually distinct from formula subscripts and ionic charge.
- [ ] No ambiguous plain text such as `VO2+` when `VO²⁺` or `VO₂⁺` is intended.
- [ ] Equation arrows, plus/minus signs, fractions and parentheses render cleanly.
- [ ] Formula typography is readable at 100% PDF zoom.
- [ ] Body font supports all chemistry glyphs used; no fallback squares or missing characters.

### Font rule learned from approved redox build

For programmatic chemistry PDFs, prefer a tested Unicode-complete text font such as **Noto Sans** over default Helvetica when formulas rely on Unicode subscripts/superscripts.

Do not ship font files; embed/use them only in the generated artifact.

---

## 10. Header and layout audit

### Separate title/subtitle zones

Never draw a long title and subtitle into one unrestricted line. Reserve independent bounding regions.

Required header checks:

```text
HEADER_TITLE_FITS = PASS
HEADER_SUBTITLE_FITS = PASS
HEADER_COLLISION = 0
```

If a title can exceed its zone, wrap or shrink it deterministically.

### Page layout blocking failures

- clipped title/subtitle;
- title/subtitle collision;
- body text outside a box;
- overlapping cards;
- helper/hint collision;
- unreadably small body text;
- formulas too small to parse;
- accidental half-page voids;
- a reasoning sequence broken across pages for no pedagogical reason;
- excessive card fragmentation;
- answer strips clipped at page bottom.

Recommended render checks:

```text
BODY_MIN_SIZE = PASS
FORMULA_MIN_SIZE = PASS
NO_OVERLAP = PASS
NO_CLIPPING = PASS
PAGE_RHYTHM = PASS
MEANINGFUL_OCCUPANCY = PASS
```

### Hint-layout rule

For H1-H3 transfer pages, use deterministic non-overlapping slots. Do not calculate hint positions only from approximate text length and then place a helper underneath without checking remaining vertical space.

Hard questions should normally use:

```text
H1 slot
H2 slot
H3 slot
```

with concept helper / misconception content in a separate column or reserved region.

---

## 11. Render-first QA loop

A PDF cannot pass from source code inspection alone.

Required loop:

```text
GENERATE
-> RENDER EVERY PAGE TO PNG
-> INSPECT TITLES / FORMULAS / BOX BOUNDS / PAGE RHYTHM
-> REPAIR
-> RE-RENDER
-> PASS
```

For PDF work follow the repository/environment PDF workflow and verify in at least one renderer.

Visual inspection must explicitly sample:

- the longest title page;
- the densest worked-example page;
- the page with the most chemistry notation;
- the page with the deepest H1-H3 ladder;
- the final audit/check page.

---

## 12. Required subtopic self-checklist

### Source and concept

- [ ] All assigned source obligations are taught.
- [ ] No source obligation disappears through concept merging.
- [ ] Source-QC corrections are explicit.
- [ ] No outside-scope chemistry leaks into Core.

### Pedagogy

- [ ] Meaning precedes procedure for new concepts.
- [ ] Familiar/real-life bridge exists or is explicitly not applicable.
- [ ] Reusable concept helpers exist for high-recognition-load concepts.
- [ ] High-risk misconceptions have explicit repair objects.
- [ ] Worked examples show reasoning, not just answers.
- [ ] Guided, faded and independent practice are present.
- [ ] Check Your Knowledge follows explanation.
- [ ] Page reads as a connected teaching sequence rather than a dashboard.

### Transfer

- [ ] Required external/PYQ set is frozen.
- [ ] Every required question has one primary subtopic and primary concept.
- [ ] Every required question is placed or validly deferred during incremental build.
- [ ] Difficulty-appropriate H1-H3 support exists.
- [ ] Required helper/misconception support exists.
- [ ] Appendix solution exists.
- [ ] Source link exists and resolves correctly.

### Publication

- [ ] Formula subscripts/superscripts render correctly.
- [ ] Title and subtitle fit without collision.
- [ ] No clipping/overflow/overlap.
- [ ] Body/formula sizes are readable at 100% zoom.
- [ ] Densest pages have been rendered and inspected.
- [ ] Final page rhythm resembles a textbook learning spread.

---

## 13. Deterministic counters

Emit at least:

```text
SOURCE_OBLIGATIONS_REQUIRED = n
SOURCE_OBLIGATIONS_TAUGHT = n
SOURCE_OBLIGATIONS_MISSING = 0
FAMILIAR_CONTEXT_REQUIRED = 0|1
FAMILIAR_CONTEXT_PRESENT = 0|1
CONCEPT_HELPERS_REQUIRED = n
CONCEPT_HELPERS_PRESENT = n
MISCONCEPTION_REPAIRS_REQUIRED = n
MISCONCEPTION_REPAIRS_PRESENT = n
GUIDED_PRACTICE_REQUIRED = n
GUIDED_PRACTICE_PRESENT = n
FADED_PRACTICE_REQUIRED = n
FADED_PRACTICE_PRESENT = n
INDEPENDENT_CHECK_REQUIRED = n
INDEPENDENT_CHECK_PRESENT = n
EXTERNAL_REQUIRED = n
EXTERNAL_PLACED_OR_VALIDLY_DEFERRED = n
EXTERNAL_MISSING = 0
TYPOGRAPHY_FAILURES = 0
HEADER_FAILURES = 0
LAYOUT_FAILURES = 0
SUBTOPIC_COMPLETENESS_STATUS = PASS
```

Any blocking non-zero failure produces `FAIL` with an exact repair list.

---

## 14. Gap-analysis output

When a draft exists, report gaps by learning function rather than page aesthetics alone:

```text
GAP ID
expected learning function
current evidence
failure type
learner consequence
smallest repair
blocking? YES/NO
```

Failure classes:

- `SOURCE_GAP`
- `EXPLANATION_ORDER_GAP`
- `FAMILIAR_CONTEXT_GAP`
- `CONCEPT_HELPER_GAP`
- `MISCONCEPTION_GAP`
- `PRACTICE_GAP`
- `TRANSFER_GAP`
- `TYPOGRAPHY_GAP`
- `HEADER_GAP`
- `LAYOUT_GAP`

---

## 15. Workflow

1. Read source-grounding ledger.
2. Read subtopic/concept architecture.
3. Inspect reference-book snapshots when provided and extract their instructional grammar.
4. Inspect the draft Study Guide and transfer book as rendered pages.
5. Run source/concept completeness.
6. Run instructional-grammar and connected-spread audit.
7. Run familiar-context, concept-helper and misconception audits.
8. Run worked-example and scaffold audit.
9. Invoke transfer-coverage auditor when an external corpus exists.
10. Run chemistry typography checks.
11. Render every page and run header/layout checks.
12. Emit gap table, counters and exact repairs.
13. Rebuild.
14. Re-render and rerun the full checklist.
15. Mark `PASS` only when all five top-level gates pass.

## Approved-pattern note from Redox Subtopic 01 v4

The user-approved Redox oxidation-number build established these reusable patterns:

- Noto Sans for chemistry-heavy programmatic PDFs;
- separate title/subtitle header zones;
- familiar formula context before rules;
- formula-anatomy helper for subscript vs charge;
- rule-priority ladder before algebra;
- charge-balance visual for sum rule;
- explicit wrong-model -> repair misconception boxes;
- worked -> guided -> faded -> independent progression;
- transfer-book concept links + H1-H3 + misconception/helper + Appendix A;
- end-of-subtopic completeness audit and separate transfer-coverage audit.

Treat these as a reusable baseline for later Redox subtopics unless the concept requires a different representation.