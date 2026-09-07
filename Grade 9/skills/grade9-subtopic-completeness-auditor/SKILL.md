---
name: grade9-subtopic-completeness-auditor
description: Audit one Grade 9 learning subtopic before publication for source coverage, instructional completeness, real-life/context bridges, concept helpers, misconception repair, practice/scaffold coverage, external/PYQ transfer coverage, and rendered typography/layout quality. Use after a subtopic draft exists and before declaring its Study Guide or transfer book complete.
---

# Grade 9 Subtopic Completeness Auditor

Audit the **whole learning experience**, not only whether content exists somewhere.

This skill wraps the source, pedagogy, transfer, and publication gates for a single subtopic. It should normally run together with `grade9-transfer-coverage-auditor` whenever an external question corpus such as ExamSIDE is part of the brief.

## Core principle

A subtopic is complete only when all four directions agree:

```text
SOURCE -> STUDY GUIDE
STUDY GUIDE -> LEARNER REASONING
ELIGIBLE TRANSFER QUESTIONS -> STUDY SUPPORT
RENDERED PDF -> INTENDED LEARNING EXPERIENCE
```

A page containing the right facts can still fail if the explanation order, misconception repair, helper, practice, formula typography, or layout is poor.

---

## 1. Required subtopic contract

Before publication, every subtopic must have a record like:

```json
{
  "subtopic_id": "RX-ST01",
  "title": "Oxidation Number",
  "source_obligation_ids": [],
  "concept_ids": [],
  "instructional_weight": "CORE",
  "real_life_context_ids": [],
  "concept_helper_ids": [],
  "misconception_ids": [],
  "worked_example_ids": [],
  "guided_practice_ids": [],
  "independent_check_ids": [],
  "required_external_question_ids": [],
  "render_artifact_ids": [],
  "status": "PASS"
}
```

Do not use page numbers as authoritative IDs. Page numbers are render outputs.

---

## 2. Instructional grammar audit

Use the user's textbook-reference grammar as the default structure:

```text
ORIENT / REAL-LIFE OR FAMILIAR CONTEXT
-> EXPLAIN THE IDEA IN ORDINARY LANGUAGE
-> SHOW WHAT THE IDEA MEANS SYMBOLICALLY / VISUALLY
-> THINGS TO KNOW / KEY RULE
-> WORKED EXAMPLE WITH REASONING STORY
-> CONCEPT HELPER / REPRESENTATION
-> MISCONCEPTION CLINIC / CLOSE CONTRAST
-> TRY WITH ME
-> FADED PRACTICE
-> CHECK YOUR KNOWLEDGE
-> TRANSFER LINK
```

Not every page must contain every module, but the **subtopic as a whole** must contain the required learning functions.

### Narrative-before-procedure rule

Do not open a subtopic with a long algorithm unless the learner already understands the idea the algorithm operates on.

Required order for a new concept:

```text
meaning -> interpretation -> example -> rule/procedure
```

Use procedure-first only for a later consolidation page.

---

## 3. Real-life / familiar-context bridge

For each CORE subtopic, include at least one context bridge when a truthful, age-appropriate example is available without introducing new chemistry.

Allowed bridge status:

```text
PEDAGOGICAL_BRIDGE
```

The bridge may make the formula or idea familiar, but it may not create a new factual dependency outside the source boundary.

Examples of acceptable patterns:

- a familiar product formula used only to notice an oxidation-number exception;
- a corrosion/burning visual used only to motivate oxidation-state tracking when those reaction facts are already source-supported;
- an everyday label/formula used as a recognition hook without teaching a new application chapter.

Checklist:

- [ ] Context is accurate.
- [ ] Context is understandable at target level.
- [ ] Context clarifies the source concept.
- [ ] Context introduces no untaught chemistry dependency.
- [ ] Context is labelled/treated as a bridge, not source authority.

If no safe context exists, record `REAL_LIFE_CONTEXT_NOT_APPLICABLE` with a reason rather than inventing one.

---

## 4. Concept-helper audit

A concept helper answers one of:

```text
What should I notice?
What should I draw / mark?
What should I think about first?
What representation makes this easier?
```

For every high-recognition-load concept require at least one helper.

Typical helper types:

- rule-priority ladder;
- charge-balance visual;
- before -> after oxidation-state lane;
- SELF vs OTHER agent frame;
- decision strip;
- split/converge topology;
- average-vs-actual site diagram.

Checklist:

- [ ] Helper reveals the representation, not the final answer.
- [ ] Helper uses the same language as worked examples and hints.
- [ ] Helper is reusable across several questions.
- [ ] Helper does not become decorative clutter.

---

## 5. Misconception audit

High-risk concepts require explicit misconception repair.

Each misconception record should include:

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

- [ ] Specific wrong mental model is named.
- [ ] A close contrast or micro-example exposes it.
- [ ] Repair explains why the wrong model fails.
- [ ] A retry/transfer item checks the repair.

Do not use generic warnings such as `be careful` as a misconception treatment.

---

## 6. Worked-example quality

A worked example must tell a reasoning story, not only show algebra.

Required stages where applicable:

```text
READ THE GIVEN
-> IDENTIFY WHAT IS ALREADY KNOWN
-> CHOOSE / BUILD THE REPRESENTATION
-> EXECUTE THE RULE
-> STATE THE RESULT
-> CHECK / INTERPRET
```

For chemistry formulas, explicitly read subscripts and overall charge before solving when those are common failure points.

---

## 7. Practice and scaffold audit

For each CORE concept require:

- at least one worked example;
- at least one guided `TRY WITH ME` item;
- at least one faded/independent item;
- at least one `CHECK YOUR KNOWLEDGE` item.

Where transfer difficulty is high, use:

```text
FULL SCAFFOLD -> FADED SCAFFOLD -> TRANSFER
```

Do not let the final check merely repeat the exact worked example surface form.

---

## 8. External/PYQ transfer audit

When an external corpus is part of the project, invoke `grade9-transfer-coverage-auditor`.

The subtopic is blocked unless:

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

The Study Guide must teach the recognition cue, first move, and representation needed by every required question; a topic-label match alone is insufficient.

---

## 9. Chemistry typography audit

For chemistry publication, formulas and ions must be visually correct.

Required checks:

- [ ] Numeric formula indices are rendered as subscripts, e.g. `H₂O₂`, `K₂Cr₂O₇`.
- [ ] Ionic charges are rendered as superscripts, e.g. `Fe³⁺`, `Cr₂O₇²⁻`.
- [ ] Oxidation numbers placed above atoms are visually distinct from stoichiometric subscripts and ionic charge.
- [ ] No plain-text ambiguity such as `VO2+` when the intended form is `VO²⁺` or `VO₂⁺`.
- [ ] Equation arrows, plus/minus signs, fractions and parentheses render without missing glyphs.
- [ ] Formula typography remains legible at 100% PDF zoom.

Use a font with complete chemistry-relevant Unicode coverage or a tested superscript/subscript rendering method. Never accept black squares, fallback glyphs, or visually ambiguous charge placement.

---

## 10. Layout audit

Compare the rendered pages against the intended textbook rhythm.

Blocking failures:

- clipped title or subtitle;
- title/subtitle collision;
- text outside boxes;
- overlapping cards;
- unreadably small body text;
- formulas too small to parse;
- accidental half-page voids;
- an explanation broken across pages before its worked example without a pedagogical reason;
- excessive card fragmentation that destroys narrative flow.

Recommended checks:

```text
HEADER_TITLE_FITS = PASS
HEADER_SUBTITLE_FITS = PASS
BODY_MIN_SIZE = PASS
FORMULA_MIN_SIZE = PASS
NO_OVERLAP = PASS
NO_CLIPPING = PASS
PAGE_RHYTHM = PASS
MEANINGFUL_OCCUPANCY = PASS
```

For two-column textbook-style spreads, reserve separate title and subtitle regions rather than drawing both into the same unrestricted line.

---

## 11. Required subtopic self-checklist

Before a subtopic can be marked complete, emit a checklist with all applicable items:

### Source and concept

- [ ] All source obligations assigned to this subtopic are taught.
- [ ] No source obligation is hidden by a merged learner concept.
- [ ] Source-QC corrections are explicit.
- [ ] No outside-scope chemistry has leaked into Core.

### Explanation quality

- [ ] Concept meaning is explained before the procedure.
- [ ] At least one familiar/real-life bridge exists or is explicitly `NOT_APPLICABLE`.
- [ ] At least one reusable concept helper exists for high-recognition-load concepts.
- [ ] High-risk misconceptions have explicit repair objects.
- [ ] Worked examples include reasoning, not only answers.
- [ ] Guided, faded, and independent practice are present.
- [ ] Check Your Knowledge tests understanding after explanation.

### Transfer

- [ ] Required external/PYQ set is frozen for the subtopic.
- [ ] Every required question has one primary subtopic and primary concept.
- [ ] Every required question is placed or validly deferred during incremental build.
- [ ] Difficulty-appropriate H1-H3 support exists.
- [ ] Appendix solution exists.
- [ ] Source link exists and is valid.

### Publication

- [ ] Formula subscripts/superscripts render correctly.
- [ ] Title and subtitle fit without collision.
- [ ] No text clipping/overflow/overlap.
- [ ] Body and formula sizes are readable at 100% zoom.
- [ ] Rendered page rhythm resembles a learning spread, not a dashboard of disconnected cards.

---

## 12. Deterministic counters

Emit at least:

```text
SOURCE_OBLIGATIONS_REQUIRED = n
SOURCE_OBLIGATIONS_TAUGHT = n
SOURCE_OBLIGATIONS_MISSING = 0
REAL_LIFE_BRIDGE_REQUIRED = 0|1
REAL_LIFE_BRIDGE_PRESENT = 0|1
CONCEPT_HELPERS_REQUIRED = n
CONCEPT_HELPERS_PRESENT = n
MISCONCEPTION_REPAIRS_REQUIRED = n
MISCONCEPTION_REPAIRS_PRESENT = n
GUIDED_PRACTICE_REQUIRED = n
GUIDED_PRACTICE_PRESENT = n
INDEPENDENT_CHECK_REQUIRED = n
INDEPENDENT_CHECK_PRESENT = n
EXTERNAL_REQUIRED = n
EXTERNAL_PLACED_OR_VALIDLY_DEFERRED = n
EXTERNAL_MISSING = 0
TYPOGRAPHY_FAILURES = 0
LAYOUT_FAILURES = 0
SUBTOPIC_COMPLETENESS_STATUS = PASS
```

Any non-zero blocking failure produces `FAIL` and an exact repair list.

---

## 13. Gap-analysis output

When a draft already exists, report gaps by function rather than by page aesthetics alone:

```text
GAP ID
expected learning function
current evidence
failure type
learner consequence
smallest repair
blocking? YES/NO
```

Recommended failure classes:

- `SOURCE_GAP`
- `EXPLANATION_ORDER_GAP`
- `REAL_LIFE_BRIDGE_GAP`
- `CONCEPT_HELPER_GAP`
- `MISCONCEPTION_GAP`
- `PRACTICE_GAP`
- `TRANSFER_GAP`
- `TYPOGRAPHY_GAP`
- `LAYOUT_GAP`

---

## 14. Workflow

1. Read source-grounding ledger.
2. Read learner concept/subtopic architecture.
3. Inspect the draft Study Guide and transfer book as rendered pages.
4. Run source/concept completeness.
5. Run instructional-grammar audit.
6. Run real-life/context, helper and misconception audits.
7. Run worked-example and scaffold audit.
8. Invoke transfer-coverage auditor when an external corpus is present.
9. Run chemistry typography checks.
10. Render every page and run layout checks.
11. Emit gap table, deterministic counters and exact repairs.
12. Rebuild.
13. Re-render and rerun the full checklist before `PASS`.

## Completion rule

Do not declare a subtopic finished because the PDF was generated successfully.

Declare it complete only when:

```text
SOURCE = PASS
PEDAGOGY = PASS
TRANSFER = PASS (when applicable)
TYPOGRAPHY = PASS
LAYOUT = PASS
```
