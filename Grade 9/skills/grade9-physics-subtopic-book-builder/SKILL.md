---
name: grade9-physics-subtopic-book-builder
description: Build one Grade 9 Physics subtopic at a time as a paired Study Guide and external-transfer question book, using source-grounded concept assimilation, real-life physical anchors, functional visuals, causal misconception repair, H1-H3 scaffold fading, per-subtopic ExamSIDE coverage audits, Appendix solutions, and strict typography/layout/render QA. Use for Motion subtopic Study Guide + PYQ/ExamSIDE pairs and similar Physics learning packages.
---

# Grade 9 Physics Subtopic Book Builder

Build **one subtopic completely before moving to the next**.

This skill is a production specialist. It works with, and does not replace:

- `../grade9-source-grounding/SKILL.md` for source authority;
- `../grade9-physics/SKILL.md` for Physics correctness, model validity and difficulty;
- `../grade9-learning-enrichment/SKILL.md` for hints and misconception diagnostics;
- `../grade9-subtopic-completeness-auditor/SKILL.md` for whole-subtopic completeness;
- `../grade9-transfer-coverage-auditor/SKILL.md` for external/PYQ completeness;
- `../grade9-textbook-publisher/SKILL.md` for PDF/link/render QA.

## Core product contract

For each subtopic produce a pair:

```text
(1) STUDY GUIDE
    concept assimilation + application + guided fading

(2) TRANSFER QUESTION BOOK
    every eligible external/PYQ item assigned to the subtopic
    + stable concept links
    + learner difficulty
    + H1-H3 support according to difficulty
    + visual/model helpers where required
    + Appendix A full solutions
```

Do not hand-pick a convenient external-question sample and call the subtopic transfer-complete. The required-question set must come from the transfer-coverage audit.

---

## 1. Subtopic-first rule

A chapter heading is not automatically a learner subtopic. Split until each unit has one clear cognitive job.

For Motion, a large block such as constant acceleration may naturally split into:

```text
what constant acceleration looks like
-> acceleration as signed velocity change
-> why v = u + at
-> sign/direction: speeding vs slowing
-> stopping-time application
-> displacement as v-t area
-> why s = ut + 1/2 at^2
-> average velocity under constant acceleration
-> why v^2 = u^2 + 2as
-> equation-selection routine / model gate
```

Do not set a page-count target. Let concept assimilation determine length.

Block progression to the next subtopic until the current Study Guide + transfer pair passes content, transfer, typography, layout and render gates.

---

## 2. Information-architecture benchmark

Use the supplied school-reference-book snapshots as an **information-structure reference**, not a decorative-font reference.

Borrow:

- one clear cognitive job per page/spread;
- spatial explanation instead of dense stacked prose;
- meaningful left/right relationships;
- large visual memory anchors;
- `FOR EXAMPLE`, `THINGS TO KNOW`, `WHY THIS MATTERS`, `COMPARE`, `DON'T MIX THIS UP`, `CHECK YOUR KNOWLEDGE` roles;
- numbered reusable procedures when the learner needs an algorithm;
- generous whitespace;
- explanation and retrieval separated when useful.

Do not create a dashboard of equal-weight cards. The learner should see one dominant idea, its supporting explanation, and a clear next move.

---

## 3. Required Study Guide learning grammar

Across a substantial subtopic, cover these roles as applicable:

```text
BIG QUESTION / REAL-LIFE SITUATION
-> SEE IT physically
-> SAY IT IN ORDINARY LANGUAGE
-> CONCEPT / INVARIANT
-> VISUAL MEMORY ANCHOR
-> CONCEPT HELPER / THINGS TO KNOW
-> BUILD / RECONSTRUCT THE RELATION
-> WORKED EXAMPLE
-> WHY THIS WORKS
-> APPLICATION FAMILY
-> VARIANT / CLOSE CONTRAST
-> DON'T MIX THIS UP
-> CAUSAL MISCONCEPTION REPAIR
-> WHAT THIS IS NOT / WHEN NOT TO USE
-> GUIDED 1
-> GUIDED 2 WITH FADED SUPPORT
-> INDEPENDENT TRANSFER
-> CHECK YOUR UNDERSTANDING
-> LEARNER SELF-CHECK / NEXT SUBTOPIC
```

These are pedagogical roles, not mandatory equal-size boxes.

### Real-life anchor

Begin an abstract Physics idea with a familiar physical situation when it helps expose the structure.

Examples:

- scooter/car for changing velocity;
- bicycle/car for braking;
- stopwatch/timeline for nth-second intervals;
- trains/escalators for relative motion;
- balloon/helicopter for moving release;
- falling/throwing object for gravity;
- motion story before a graph.

The example must reveal the Physics, not merely supply numbers for substitution.

---

## 4. Functional concept helpers / memory anchors

Use recurring representations so the learner develops recognition habits.

```text
PATH vs ENDPOINT ARROW           distance/displacement
TIME STRIP vs DISTANCE STRIP     average-speed weighting
VELOCITY + ACCELERATION ARROWS   speeding/slowing sign logic
u-v-a-t-s STRIP                  constant-acceleration relation choice
AREA UNDER v-t                   displacement under constant acceleration
TIMELINE SLICE                   nth-second / last-N-second
TWO-LANE CLOCK                   delayed start / two-body
VERTICAL SIGN STRIP              gravity / highest point / moving release
SLOPE-AREA DECODER               motion graphs
```

A helper counts only if it reduces cognitive load or exposes hidden structure.

Use representation status:

- `REASONING_VISUAL_REQUIRED`
- `REASONING_VISUAL_OPTIONAL`
- `NO_VISUAL_NEEDED`

Treat translation as a first-class objective:

```text
words <-> physical picture <-> line/timeline/table <-> graph <-> equation
```

---

## 5. Physics first-step pipeline

Use one reasoning grammar in worked examples, hints, diagnostics and solutions:

```text
P1 SEE       what is physically happening?
P2 FRAME     reference frame / positive direction
P3 REPRESENT draw the useful picture/timeline/graph
P4 EXTRACT   knowns, hidden facts, target
P5 MODEL     choose the physical model and validity conditions
P6 CHOOSE    choose a relation avoiding unnecessary unknowns
P7 SOLVE
P8 CHECK     units, sign, magnitude, graph/model consistency
```

For constant acceleration, use `u,v,a,t,s` only after the model gate passes.

---

## 6. Equations are compressed Physics

Never introduce a naked equation when a physical/graphical reconstruction is available.

For each important relation explain:

1. what physical story it compresses;
2. what each term means;
3. why unusual mathematical features appear;
4. assumptions/model validity;
5. unit/dimensional check where useful;
6. limiting/special cases where useful;
7. how to rebuild from an earlier principle or representation.

Examples:

- `v = u + at`: `at` is accumulated velocity change;
- `s = ut + 1/2 at^2`: rectangle + triangle under a v-t graph; explain `1/2` and `t^2`;
- `s = (u+v)t/2`: average velocity is the midpoint of a linear velocity ramp;
- `v^2 = u^2 + 2as`: squared velocities arise when time is eliminated through sum x difference;
- nth-second relation: interval subtraction from cumulative displacement.

---

## 7. Misconception repair

Do not stop at a warning box. For high-risk misconceptions use:

```text
WRONG IDEA
-> WHY IT LOOKS PLAUSIBLE
-> COUNTEREXAMPLE / VISUAL CONTRAST
-> CORRECT PHYSICAL MODEL
-> RETRY ON A CLOSE VARIANT
```

High-priority Motion examples:

- negative acceleration = slowing down;
- `v = 0 -> a = 0`;
- dropped -> `u = 0` from any frame;
- distance = displacement;
- arithmetic mean for equal-distance speeds;
- nth second = first n seconds;
- final velocity x time = displacement under acceleration;
- one SUVAT equation across a multistage journey;
- SUVAT used when acceleration is not constant;
- graph height confused with slope/area;
- signed v-t area confused with total distance;
- inconsistent clocks/signs for two bodies.

When diagnosing a wrong response, tag the likely failed pipeline stage P1-P8.

---

## 8. Guided practice and true visual fading

Use at least these support states for important applications.

### Worked example

- complete physical representation;
- hidden facts identified;
- model named;
- first relation justified;
- solution + physical check.

### Guided 1

- substantial visual scaffold;
- incomplete learner fields;
- H1-H3 available progressively.

### Guided 2

- skeleton visual / blank table;
- learner supplies more of the model;
- H1-H3 available but not automatically exposed.

### Independent transfer

- no supplied representation initially;
- learner chooses/draws it.

Visual fading:

```text
SHOW -> COMPLETE -> PARTIAL -> SKELETON -> DRAW/CHOOSE YOURSELF
```

Physics hint semantics:

```text
H1 NOTICE  decisive clue/event
H2 MODEL   representation/model
H3 START   first executable relation/line, not the final solution
```

In static PDF, spatially isolate the hint region so H3 is not read accidentally.

---

## 9. Typography and layout contract

For A4 landscape Physics Study Guides, use the following **default floor**, unless a tested alternative is demonstrably more readable:

```text
instructional body          11.5 pt / about 15.2 pt leading
helper/callout body         10.5-11 pt / about 14 pt leading
visual labels               >= 9.5 pt where possible
section heading             about 15 pt
header title                17-19 pt
header subtitle             about 9.5-10.5 pt
display equation            19-22+ pt
compact equation            >= 16.5 pt
footer/provenance only      about 7.5-8 pt
```

Prefer a clean, readable sans-serif for instructional prose and a tested math-capable font for equations.

Hard rule:

> **Do not shrink instructional text to preserve a page. Reflow, reduce empty box height, or add/split a page.**

Layout rules:

- one dominant cognitive job per page/spread;
- meaningful left/right relationship only;
- primary visual large enough to remember;
- no instructional body copy at footer-size typography;
- no heading/equation crossing the center gutter;
- no tiny diagram labels attached to large empty boxes;
- avoid long single-line headings/equations when wrapping or a second line improves readability;
- do not let labels collide with arrows/graphs;
- if a misconception clinic becomes dense, split it into diagnosis and repair pages rather than shrinking.

### Math/font QA

Before PASS verify:

- equations are vector/searchable where practical;
- superscripts/subscripts are legible;
- Greek letters, arrows, minus signs, roots and operators render correctly;
- no fallback boxes/black squares;
- no clipping at column/gutter boundaries;
- no label collision with equations/diagrams;
- math is not made smaller than comfortable body size to force fit.

Render every page at **200 dpi**, inspect the complete contact sheet, then inspect high-risk pages at full size.

---

## 10. Study Guide self-audit

Run `grade9-subtopic-completeness-auditor` and emit at least:

```text
SOURCE_OBLIGATIONS = n/n
REAL_LIFE_ANCHOR = PASS | NOT_REQUIRED
CONCEPT_EXPLANATION = PASS
MEMORY_HELPER = PASS | NOT_REQUIRED
REPRESENTATION = PASS | NOT_REQUIRED
RELATION_RECONSTRUCTION = PASS | NOT_REQUIRED
WORKED_EXAMPLE = PASS
VARIANT_OR_CONTRAST = PASS
MISCONCEPTION_REPAIR = PASS | NOT_REQUIRED
WHEN_NOT_TO_USE = PASS | NOT_REQUIRED
GUIDED_1 = PASS
GUIDED_2_FADED = PASS
INDEPENDENT_TRANSFER = PASS
RETRIEVAL_CHECK = PASS
FONT_QA = PASS
LAYOUT_QA = PASS
RENDER_QA = PASS
SUBTOPIC_STUDY_GUIDE_STATUS = PASS
```

A formula appearing somewhere is not enough for `CONCEPT_EXPLANATION = PASS`.

---

## 11. External / ExamSIDE transfer audit

When external PYQs are in scope, use `../grade9-transfer-coverage-auditor/SKILL.md`.

Required workflow:

```text
freeze corpus snapshot
-> classify candidates by minimum solution path
-> assign every eligible item exactly one primary subtopic
-> derive CURRENT_SUBTOPIC_REQUIRED set
-> build transfer book from that required set
-> reverse-audit every question back to concept/support/solution/source
```

Do not curate a convenient sample and call it complete.

During incremental builds:

- `PLACED` = present now;
- `DEFERRED_VALID` = eligible but assigned to a named future subtopic;
- `MISSING` = should be here but absent -> blocking;
- `EXCLUDED_VALID` = valid partial/out-of-scope exclusion;
- `UNRESOLVED` = source cannot yet be verified.

At final chapter completion, eligible deferred count must be zero.

Every eligible external item needs:

```text
external_question_id
snapshot_id
source_url
scope_status
scope_reason
primary_subtopic_id
secondary_subtopic_ids
primary_concept_id
secondary_concept_ids
question_family
novelty
learner_difficulty
coverage_status
study_guide_concept_link
transfer_book_question_id
hint_depth_required
h1_present
h2_present
h3_present
visual_helper_required
visual_helper_present
appendix_solution_id
source_link_present
source_link_valid
support_status
```

Stable concept/question IDs are authoritative; PDF page numbers are convenience metadata.

---

## 12. Transfer-book difficulty support

Default learner-facing policy:

```text
D1 -> H1 optional/minimal recognition aid
D2 -> H1-H2
D3 -> H1-H3; visual/model helper when representation causes difficulty
D4-D5 -> H1-H3 + explicit concept/model helper + stronger validation/contrast
```

Hints target the actual reasoning bottleneck, not merely add more words.

For each current subtopic:

- include all required eligible external items assigned to it;
- group by reasoning/application family;
- show D1-D5 difficulty;
- show stable Study Guide concept link;
- preserve source/provenance link;
- provide H1-H3 according to difficulty;
- provide a visual/concept helper when required;
- Appendix A contains a full solution for every included question;
- solution begins from the same representation/first move taught in the Study Guide;
- exclude out-of-scope items from the canonical learner book;
- do not bulk reproduce a third-party question bank verbatim; use permitted adapted/paraphrased wording with source metadata/link.

---

## 13. Required per-subtopic transfer self-check

Always emit both views.

### View A - subtopic -> questions

```text
M-ST04A
  EX-M-001 PLACED -> C3 -> D1 -> solution present
  EX-M-002 PLACED -> C4 -> D2 -> H1-H2 -> visual present

required n / placed n / missing 0
```

### View B - question -> support route

```text
EX-M-002
-> scope ELIGIBLE_IN_SCOPE
-> primary subtopic M-ST04A
-> concept taught YES
-> representation taught YES
-> first move taught YES
-> required hints present YES
-> visual helper QA PASS
-> Appendix A solution present
-> source link valid
-> COMPLETE
```

Blocking counters:

```text
SUBTOPIC_REQUIRED = n
SUBTOPIC_PLACED = n
SUBTOPIC_DEFERRED_VALID = n
SUBTOPIC_MISSING = 0
SUBTOPIC_DUPLICATE_PRIMARY = 0
SUBTOPIC_CONCEPT_LINK_FAILURES = 0
SUBTOPIC_HINT_FAILURES = 0
SUBTOPIC_VISUAL_FAILURES = 0
SUBTOPIC_SOLUTION_FAILURES = 0
SUBTOPIC_BROKEN_SOURCE_LINKS = 0
SUBTOPIC_SCOPE_LEAKS = 0
SUBTOPIC_TRANSFER_STATUS = PASS
```

Final chapter acceptance requires:

```text
CHAPTER_ELIGIBLE_TOTAL = n
CHAPTER_PLACED_UNIQUE = n
CHAPTER_DEFERRED = 0
CHAPTER_MISSING = 0
CHAPTER_DUPLICATE_PRIMARY = 0
CHAPTER_UNTAUGHT_DEPENDENCY = 0
CHAPTER_TRANSFER_STATUS = PASS
```

---

## 14. Build sequence

For one subtopic:

```text
A SOURCE FREEZE
  -> source obligations and question anchors

B LEARNER ARCHITECTURE
  -> concept split
  -> application families
  -> prerequisite / misconception map

C STUDY GUIDE
  -> real-life anchor
  -> visual/helper
  -> explanation/reconstruction
  -> worked example
  -> variant/contrast
  -> causal misconception repair
  -> model gate
  -> Guided 1
  -> Guided 2 faded
  -> transfer
  -> retrieval/self-check

D STUDY GUIDE AUDIT
  -> source + pedagogy + typography + render

E EXTERNAL REQUIRED SET
  -> frozen snapshot
  -> minimum solution path
  -> primary-subtopic assignment

F TRANSFER BOOK
  -> all required questions
  -> concept links
  -> D1-D5
  -> H1-H3
  -> visual/model helpers
  -> Appendix A solutions

G REVERSE AUDIT
  -> question -> concept -> helper -> hint -> solution -> source

H FINAL PDF QA
  -> render all pages at 200 dpi
  -> inspect contact sheet
  -> inspect equation-, graph-, misconception-, and hint-heavy pages full size
  -> validate links
  -> PASS before next subtopic
```

## Completion rule

A subtopic is complete only when:

```text
SOURCE = PASS
PEDAGOGY = PASS
TRANSFER = PASS (when applicable)
TYPOGRAPHY = PASS
LAYOUT = PASS
RENDER = PASS
```

Static QA proves package/content coverage, not measured learner mastery.