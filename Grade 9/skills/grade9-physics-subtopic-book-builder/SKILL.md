---
name: grade9-physics-subtopic-book-builder
description: Build one Grade 9 Physics subtopic at a time as a paired Study Guide and external-transfer question book, using source-grounded concept assimilation, real-life physical anchors, functional visuals, causal misconception repair, H1-H3 scaffold fading, per-subtopic ExamSIDE coverage audits, Appendix solutions, and strict typography/layout/render QA. Use when creating Motion subtopic books or similar Physics study-guide + PYQ transfer pairs.
---

# Grade 9 Physics Subtopic Book Builder

Build **one subtopic completely before moving to the next**.

This skill is a production specialist. It does not replace:

- `../grade9-source-grounding/SKILL.md` for source authority;
- `../grade9-physics/SKILL.md` for Physics correctness, model validity, difficulty and representation reasoning;
- `../grade9-learning-enrichment/SKILL.md` for hints and misconception diagnostics;
- `../grade9-subtopic-completeness-auditor/SKILL.md` for whole-subtopic completeness;
- `../grade9-transfer-coverage-auditor/SKILL.md` for external/PYQ completeness;
- `../grade9-textbook-publisher/SKILL.md` for publication/link/render QA.

## Core product contract

For each subtopic produce a pair:

```text
(1) STUDY GUIDE
    concept assimilation + application + guided fading

(2) TRANSFER QUESTION BOOK
    every eligible external/PYQ item assigned to this subtopic
    + concept links
    + difficulty-appropriate H1-H3
    + visual/model helpers where required
    + Appendix A full solutions
```

Do not build the transfer book from a hand-picked sample and call it complete. The required-question set must come from the transfer-coverage auditor.

---

# 1. Subtopic-first rule

A chapter heading is not automatically a learner subtopic.

Split until each unit has one clear cognitive job.

Example:

```text
Constant acceleration
  -> what the pattern looks like
  -> acceleration as signed velocity change
  -> why v = u + at
  -> sign/direction: speeding vs slowing
  -> stopping-time application
  -> model gate / first-step routine
```

Do not force a page-count target. Let concept assimilation determine length.

Block progression to the next subtopic until the current pair passes content, transfer, typography, layout and render gates.

---

# 2. Information-architecture benchmark

Use the supplied school-reference-book snapshots as an **information-structure reference**, not a font/style copy.

Borrow:

- one clear idea per spread/page;
- spatial explanation instead of stacked prose;
- meaningful left/right comparisons;
- strong visual memory anchors;
- `FOR EXAMPLE`, `THINGS TO KNOW`, `WHY THIS MATTERS`, `COMPARE`, `DON'T MIX THIS UP`, `CHECK YOUR KNOWLEDGE` roles;
- numbered reusable procedures when the learner needs an algorithm;
- generous whitespace;
- explanation and retrieval separated when useful.

Do **not** imitate decorative/handwritten fonts.

A page must not feel like a dense dashboard of equal-weight cards. The learner should see a dominant idea, supporting explanation and a clear next move.

---

# 3. Required Study Guide learning grammar

For a substantial Physics concept/application, cover these roles as applicable:

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

These are pedagogical roles, not mandatory equal-sized boxes.

## Real-life anchor

Start abstract Physics with a familiar physical situation whenever useful.

Examples:

- scooter/car for changing velocity;
- bicycle/car for braking;
- stopwatch/timeline for nth-second intervals;
- trains/escalators for relative motion;
- balloon/helicopter for moving release;
- falling/throwing object for gravity;
- a motion story before a graph.

The physical situation must expose the reasoning structure, not merely provide numbers for substitution.

---

# 4. Physics concept helpers / memory anchors

Use recurring functional visuals so the learner develops recognition habits.

Candidate memory objects:

```text
PATH vs ENDPOINT ARROW          distance/displacement
TIME STRIP vs DISTANCE STRIP    average-speed weighting
VELOCITY + ACCELERATION ARROWS  speeding/slowing sign logic
u-v-a-t-s STRIP                 constant-acceleration relation choice
TIMELINE SLICE                  nth-second / last-N-second
TWO-LANE CLOCK                  delayed start / two-body
VERTICAL SIGN STRIP             gravity / highest point / moving release
SLOPE-AREA DECODER              motion graphs
```

A helper counts only when it reduces cognitive load or externalizes hidden structure.

Use representation status:

- `REASONING_VISUAL_REQUIRED`
- `REASONING_VISUAL_OPTIONAL`
- `NO_VISUAL_NEEDED`

Treat translation as a learning objective:

```text
words <-> physical picture <-> line/timeline/table <-> graph <-> equation
```

---

# 5. Physics reasoning pipeline

Use the canonical first-step pipeline:

```text
P1 SEE       what is physically happening?
P2 FRAME     reference frame / positive direction
P3 REPRESENT draw the useful motion line/timeline/graph
P4 EXTRACT   knowns, hidden facts, target
P5 MODEL     choose the physical model and validity conditions
P6 CHOOSE    choose a relation avoiding unnecessary unknowns
P7 SOLVE
P8 CHECK     units, sign, magnitude, graph/model consistency
```

Worked examples, hints, diagnostics and solutions should use the same grammar.

For constant acceleration, use the `u,v,a,t,s` strip only **after** the model gate passes.

---

# 6. Explain equations as compressed Physics

Never introduce a naked formula when a physical or graphical reconstruction is available.

For each important relation explain:

1. what physical story it compresses;
2. what each term means;
3. why unusual mathematical features appear;
4. assumptions/model validity;
5. a unit/dimensional check where useful;
6. a limiting/special-case check where useful;
7. how to rebuild it from an earlier principle or representation.

Examples:

- `v = u + at`: `at` is accumulated velocity change;
- `s = ut + 1/2 at^2`: rectangle + triangle under a v-t graph; explain `1/2` and `t^2`;
- `v^2 = u^2 + 2as`: squared velocities arise when time is eliminated through sum x difference;
- nth-second relation: interval subtraction from cumulative displacement.

---

# 7. Misconception repair

Do not stop at a warning box.

For high-risk misconceptions use:

```text
WRONG IDEA
-> WHY IT LOOKS PLAUSIBLE
-> COUNTEREXAMPLE / VISUAL CONTRAST
-> CORRECT PHYSICAL MODEL
-> RETRY ON A CLOSE VARIANT
```

Examples:

- negative acceleration = slowing down;
- v = 0 -> a = 0;
- dropped -> u = 0 from any frame;
- nth second = first n seconds;
- signed v-t area = distance;
- SUVAT valid whenever the object is slowing;
- one SUVAT equation across a multistage journey.

When diagnosing a wrong answer, tag the likely failed pipeline stage P1-P8.

---

# 8. Guided practice + visual fading

Use at least these support states for important applications.

## Worked example

- complete physical representation;
- hidden facts identified;
- model named;
- first relation justified;
- solution and physical check.

## Guided 1

- substantial visual scaffold;
- incomplete learner fields;
- H1-H3 available progressively.

## Guided 2

- skeleton visual / blank table;
- learner supplies more of the model;
- H1-H3 available but not automatically exposed.

## Independent transfer

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

In static PDF, spatially isolate the hint region so H3 is not read accidentally while attempting the question.

---

# 9. Study Guide layout rules

Prefer landscape/two-page-spread architecture when it materially improves Physics diagrams and comparisons.

Use left/right columns only when the relationship is meaningful, for example:

- story vs mathematical compression;
- case A vs case B;
- physical picture vs graph;
- worked example vs reusable method;
- correct model vs tempting wrong model.

Layout rules:

- one dominant cognitive job per page/spread;
- primary visual should be large enough to remember;
- ordinary body text should remain comfortably readable at A4 normal zoom;
- keep margins and whitespace generous;
- do not let headings or equations cross the center gutter;
- avoid very long single-line equations/headings;
- if content does not fit, reflow or add a page rather than shrink aggressively;
- use consistent box roles and hierarchy;
- labels attached to arrows/graphs must not overlap the object they explain.

---

# 10. Font / mathematics QA

Use a math-capable font with complete glyph coverage.

Before declaring PASS verify:

- equations are vector/searchable where practical;
- superscripts/subscripts are legible;
- Greek letters, arrows, minus signs, square roots and operators render correctly;
- no fallback boxes / black squares;
- no clipping at column/gutter boundaries;
- no label collision with equations or diagrams;
- math is not smaller than normal readable body text merely to force fit;
- extracted text is not the authority for visual correctness, but obvious extraction corruption should trigger a font/encoding review.

Render every page at 200 dpi and visually inspect the complete contact sheet plus high-risk pages at full size.

---

# 11. Study Guide self-audit record

Run `grade9-subtopic-completeness-auditor` and emit at least:

```json
{
  "subtopic_id": "M-ST04A",
  "title": "Constant acceleration and v = u + at",
  "source_obligation_ids": ["MS-S08", "MS-S09", "MS-S10", "MS-S11"],
  "real_life_anchor": "PASS",
  "concept_explanation": "PASS",
  "memory_helper": "PASS",
  "representation_status": "REASONING_VISUAL_REQUIRED",
  "representation_qa": "PASS",
  "relation_reconstruction": "PASS",
  "worked_example": "PASS",
  "variant_or_contrast": "PASS",
  "misconception_repair": "PASS",
  "when_not_to_use": "PASS",
  "guided_1": "PASS",
  "guided_2_faded": "PASS",
  "independent_transfer": "PASS",
  "retrieval_check": "PASS",
  "font_qa": "PASS",
  "layout_qa": "PASS",
  "render_qa": "PASS",
  "status": "PASS"
}
```

A formula appearing somewhere is not sufficient for `concept_explanation = PASS`.

---

# 12. External / ExamSIDE question audit

When external PYQs are in scope, read and apply:

`../grade9-transfer-coverage-auditor/SKILL.md`

Required workflow:

```text
freeze corpus snapshot
-> classify every candidate by minimum solution path
-> assign every eligible item exactly one primary subtopic
-> derive CURRENT_SUBTOPIC_REQUIRED set
-> build transfer book from that required set
-> reverse-audit every question back to concept/support/solution/source
```

Do not curate a convenient sample and call the subtopic transfer-complete.

During incremental builds:

- `PLACED` = present now;
- `DEFERRED_VALID` = eligible but assigned to a named future subtopic;
- `MISSING` = should be here but absent -> blocking;
- `EXCLUDED_VALID` = only for valid partial/out-of-scope exclusions;
- `UNRESOLVED` = source cannot yet be verified.

At final chapter completion, eligible deferred count must be zero.

---

# 13. Transfer question record

Every eligible external item needs:

```text
external_question_id
snapshot_id
source_url
source_status
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

Stable concept/question IDs are authoritative. Rendered page numbers are convenience metadata only.

---

# 14. Transfer-book difficulty support

Use Physics difficulty reasoning underneath, but student-facing D1-D5 may be shown.

Default hint policy when the user has not overridden it:

```text
D1 -> H1 optional / minimal recognition aid
D2 -> H1-H2
D3 -> H1-H3; visual/model helper when representation causes difficulty
D4-D5 -> H1-H3 + explicit concept/model helper + stronger validation/contrast
```

Do not make hard-question hints merely more verbose. Hint depth should target the actual reasoning bottleneck.

---

# 15. Transfer book output contract

For the current subtopic:

- include all required eligible external questions assigned to it;
- group by reasoning/application family, not chronology alone;
- show D1-D5 difficulty;
- show stable Study Guide concept link;
- include source/provenance link;
- include visual/concept helper when required;
- include H1-H3 according to difficulty;
- Appendix A must contain a full solution for every included question;
- Appendix solution begins from the same physical representation/first move taught in the Study Guide;
- exclude out-of-scope items from the canonical learner book;
- do not bulk reproduce third-party copyrighted question banks verbatim; use permitted adapted/paraphrased learner-facing wording with retained metadata/source link.

---

# 16. Required per-subtopic transfer self-check

Always emit both views.

## View A - subtopic -> questions

```text
M-ST04A Constant acceleration
  EX-M-001 PLACED -> C3 -> D1 -> solution present
  EX-M-002 PLACED -> C4 -> D2 -> H1-H2 -> visual present
  EX-M-003 DEFERRED_VALID -> target M-ST04D

required n / placed n / deferred n / missing 0
```

## View B - question -> support route

```text
EX-M-002
-> scope ELIGIBLE_IN_SCOPE
-> primary subtopic M-ST04A
-> concept C4 taught YES
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

# 17. Build sequence

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
  -> grade9-subtopic-completeness-auditor
  -> source/content/visual/font/layout/render PASS

E EXTERNAL AUDIT INPUT
  -> frozen corpus
  -> required current-subtopic question set

F TRANSFER BOOK
  -> all required questions
  -> concept links
  -> difficulty/hints/helpers
  -> Appendix A solutions
  -> source links

G REVERSE AUDIT
  -> grade9-transfer-coverage-auditor
  -> question -> concept -> representation -> hint -> solution -> source

H PUBLICATION QA
  -> links
  -> font/math
  -> layout
  -> render

I PASS BEFORE NEXT SUBTOPIC
```

---

# 18. Failure policy

If a page is crowded, do not solve it by shrinking fonts.

If a subtopic is conceptually overloaded, split it.

If an eligible external question does not fit the current subtopic, assign it to the correct named future subtopic and mark `DEFERRED_VALID`; do not silently omit it.

If a question requires untaught/out-of-scope Physics, classify/exclude it; do not expand the Study Guide to make the question fit.

If a visual does not improve reasoning, remove it.

If a hint reveals the final route too early, redesign the hint placement or fade.

Static audits prove coverage and production quality; they do not claim measured learner mastery.
