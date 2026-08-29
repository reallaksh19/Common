# NMTC Bhaskara Preliminary — Topic Package Production Manifests v1

## Purpose

Freeze the **allowed publication projection** for each of the ten internally complete topic packages.

This closes the semantic student/teacher split at source level. It does **not** close rendered leakage QA until actual student/teacher artifacts are produced and inspected.

## Projection vocabulary

### `STUDENT_CORE`

Concept teaching intended for the learner.

### `STUDENT_PRACTICE`

Question-first projection of practice/transfer/mastery material. Solutions, answer keys, package labels and diagnostic tags are excluded from the live-question flow unless a deliberate answer section is placed after the attempt section.

### `TEACHER_FULL`

Full source material including solutions, first moves, misconceptions, QA, provenance/source conflicts and diagnostic routing.

### `AUTHOR_ONLY`

Authority/QC material not intended for ordinary classroom distribution.

---

# P0-1 — Polynomial & Root Structure

Source home:

`03_Concept_Books/Algebra/Polynomial_Root_Structure/`

### Student projection

- `Polynomial_Root_Structure_Student_Draft_v0.1.md` -> `STUDENT_CORE` after production copyedit;
- First-Step cards -> `STUDENT_CORE` or revision card form;
- practice ladder -> `STUDENT_PRACTICE`;
- transfer bank -> question-first `STUDENT_PRACTICE`;
- mastery test -> question-only assessment, answers after attempt if included.

### Teacher/author projection

- concept spec;
- source coverage map;
- full transfer/mastery solutions;
- package QA;
- source-conflict notes.

---

# P0-2 — Radicals / Exponents / Logarithmic Transformations

Source home:

`03_Concept_Books/Algebra/Radical_Exponent_Log_Transformations/`

Student: student draft + first-step/revision cards + question-first ladder/transfer/mastery projections.

Teacher/author: concept spec, source map, full solution banks, QA, domain/source notes.

---

# P0-3 — Inequalities / Bounds / Equality Conditions

Source home:

`03_Concept_Books/Algebra/Inequalities_Bounds_Equality/`

Student: student draft + boundedness/equality First-Step cards + question-first ladder/transfer/mastery projections.

Teacher/author: solution/equality-condition notes, source-conflict examples, concept spec/source map, QA.

Do not expose a teacher label such as `UNBOUNDEDNESS_FALSIFIER` as a hint beside an active assessment item.

---

# P0-4 — Modular / Divisibility / Digit Structures

Source home:

`03_Concept_Books/Number_Theory/Modular_Divisibility_Digit_Structure/`

Student: student draft + First-Step cards + question-first ladder/transfer/mastery projections.

Teacher/author: source map, concept spec, full solutions, exact LCM-vs-GCD contrast notes, QA/provenance.

---

# P0-5 — Circle / Tangent Recognition

Source home:

`03_Concept_Books/Geometry/Circle_Tangent_Recognition/`

Student: student draft + author-created/text-complete examples + First-Step recognition cards + question-first ladder/transfer/mastery projections.

Teacher/author: source coverage map, figure-custody statuses, full solutions, concept spec, QA.

### Historical figure rule

Any historical item marked `FIGURE_GATED` remains **excluded from canonical student PYQ publication** until exact figure custody is recovered. An author-created analogue may be published only under author-created provenance.

---

# P1-1 — Sequence & Series Preliminary Overlay

Source home:

`03_Concept_Books/Algebra/Sequence_Series_Preliminary/`

Deep concept authority remains `../Sequence and Series/`.

Student: Preliminary student route/overlay + First-Step cards + question-first ladder/transfer/mastery projections; link/defer deep concept exposition to the existing Sequence & Series chapter rather than duplicating it.

Teacher/author: source map, overlay spec, full solutions, 2025 Q30 conflict custody, QA.

---

# P1-2 — Counting / Permutations / Combinations / Pigeonhole / Inclusion–Exclusion

Source home:

`03_Concept_Books/Combinatorics/Counting_Permutations_Pigeonhole_IE/`

Student: student draft + structural counting First-Step cards + question-first ladder/transfer/mastery projections.

Teacher/author: source map, concept spec, figure/source-gated PYQ notes, full solutions, QA.

Student material must not imply that recurrence percentages are official combinatorics weightage.

---

# P1-3 — Triangle Metric / Apollonius / Stewart

Source home:

`03_Concept_Books/Geometry/Triangle_Metric_Apollonius_Stewart/`

Student: student draft + theorem-reconstruction examples + First-Step cards + question-first ladder/transfer/mastery projections.

Teacher/author: concept spec, source map, 2023 Q02 source-conflict custody, full solutions, QA.

Stewart author-created core material must not receive invented NMTC year/question attribution.

---

# P2-1 — Mathematical Induction

Source home:

`03_Concept_Books/Algebra/Mathematical_Induction/`

Student: student draft + proof-logic First-Step cards + question-first ladder/transfer/mastery projections.

Teacher/author: source coverage map explicitly recording weak current PYQ recurrence, concept spec, broken-proof diagnostics, full solutions, QA.

Student publication may state that Induction is syllabus-required; it must not invent PYQ recurrence.

---

# P2-2 — Greatest / Least Integer Functions

Source home:

`03_Concept_Books/Algebra/Greatest_Least_Integer_Functions/`

Student: student draft + interval-translation First-Step cards + question-first ladder/transfer/mastery projections.

Teacher/author: source map, concept spec, incidental-floor vs primary-mechanism classification, full solutions, QA.

2024 Q27 remains bridge evidence only, not a direct floor/ceiling PYQ anchor.

---

# Shared support-directory projection

## `04_First_Step_Reference/`

Default role: student revision + teacher teaching aid.

Before assessment export, remove/withhold cards that would reveal the intended first move for live unlabelled items.

## `05_Practice_Ladders/`

Default role: student practice.

Teacher solutions/hints, if embedded, must be projected to a separate answer section or teacher artifact.

## `06_Speed_Labs/`

Recognition and first-line labs may be student-facing as training artifacts. Answer/routing material belongs after the attempt or in teacher output.

## `07_Mastery_Banks/`

Question-first student projection + teacher full solution projection.

## `08_Mixed_Preliminary_Tests/`

Package mastery tests follow the same question-first rule. Mock A/B/C already have physically separate student and teacher files.

## `09_QA/`

Default role: `AUTHOR_ONLY` / teacher-authority. Do not include in ordinary student publication.

---

# Production leakage rules

A student artifact fails the source split if it unintentionally exposes any of the following before the learner attempts the relevant question:

- answer;
- first useful move;
- package/concept label in an intentionally mixed/unlabelled assessment;
- diagnostic code;
- teacher misconception note;
- source conflict resolution;
- internal QA status;
- hidden invariant stated as the answer to a recognition task.

# Current state

```text
PACKAGE_MANIFESTS_DEFINED = 10/10
MOCK_FILE_LEVEL_SPLIT = PASS_STATIC
TOPIC_SOURCE_LEVEL_SPLIT = PASS_STATIC
RENDERED_STUDENT_TEACHER_LEAKAGE_AUDIT = NOT_RUN
FINAL_STUDENT_TEACHER_SEPARATION = PARTIAL
```

The remaining work for this gate is artifact generation + rendered leakage inspection, not deciding where content belongs.
