---
name: grade4-math
description: Create and analyze Grade 4 Mathematics learning content using concept graphs, prerequisite dependencies, representation progressions, Learning Cells, controlled question archetypes, diagnostics, mastery evidence, transfer, and textbook-quality publishing.
---

# Grade 4 Mathematics Skill

## Mandatory references

Always load and follow:

- `../../Grade4MathSchema.md`

When a chapter-specific schema exists, load it in addition to the core schema.

Naming convention:

```text
Grade4Math<TopicPascalCase>Schema.md
```

Known chapter schema:

- Division -> `../../Grade4MathDivisionSchema.md`

For PDF/book production also load:

- `../../Grade4PublishingSchema.md`
- chapter-specific publishing contract when available, e.g. `../../Grade4MathDivisionPublishingContract.md`

## Core principle

Do not treat a mathematics chapter as a collection of questions.

Use the hierarchy:

```text
CHAPTER
  -> MACROCONCEPT
  -> MICROCONCEPT / LEARNING CELL
  -> QUESTION INSTANCE
```

The Learning Cell is the primary instructional object. Questions are evidence/practice instances beneath it.

## Supported modes

```text
ANALYZE_SOURCE
BUILD_CHAPTER
BUILD_CONCEPT_MAP
BUILD_LEARNING_CELL
BUILD_QUESTION_BANK
BUILD_PRACTICE
BUILD_DIAGNOSTIC
BUILD_ASSESSMENT
BUILD_REVISION
BUILD_OLYMPIAD
BUILD_TEXTBOOK
BUILD_WORKBOOK
BUILD_TEACHER_EDITION
BUILD_PDF
```

## Workflow

### Stage 1 — Resolve scope

Determine:

- grade = 4;
- chapter/topic;
- curriculum/source basis;
- school/HOTS/Olympiad target;
- requested output;
- whether source fidelity is strict;
- whether extension material is allowed.

Do not silently extend beyond the source/curriculum.

### Stage 2 — Load schemas

1. Load `Grade4MathSchema.md`.
2. Resolve chapter-specific schema by naming convention.
3. If found, treat it as the authoritative chapter blueprint.
4. If absent, derive a temporary chapter blueprint from the core schema + supplied source. Do not invent a permanent repository schema unless the user asks to create one.

### Stage 3 — Reverse-engineer source

When source material is supplied, inspect:

- lesson titles and objectives;
- concept introduction sequence;
- vocabulary;
- concrete/pictorial/structural models;
- symbolic representations;
- worked examples;
- strategy progression;
- guided vs independent practice;
- problem-solving/reasoning sections;
- review/spiral sections;
- challenge/extension sections;
- assessment structure.

Preserve source terminology and progression unless explicitly asked to redesign.

### Stage 4 — Build concept architecture

Create or validate:

- chapter big ideas;
- macroconcepts;
- microconcepts;
- concept invariants;
- prerequisite graph with `CRITICAL`, `STRONG`, `SUPPORTING` dependencies;
- vocabulary;
- connections to prior/future learning.

### Stage 5 — Build representation architecture

Use the Grade 4 progression where appropriate:

```text
R0 CONCRETE
R1 PICTORIAL
R2 STRUCTURAL MODEL
R3 SYMBOLIC
R4 STRATEGIC
R5 PROCEDURAL
R6 ABSTRACT REASONING
```

Record input representation, expected working representation, and answer representation separately.

Representation translation is itself a learning target.

### Stage 6 — Build Learning Cells

Each important microconcept should define:

- ID and status (`CORE`, `REVIEW`, `EXTENSION`, `OLYMPIAD_BRIDGE`);
- objective and success criteria;
- big idea;
- child-friendly meaning;
- concept invariant;
- prerequisites and connections;
- vocabulary;
- launch context;
- representation sequence;
- `what_to_notice`;
- recognition cues;
- concept trigger;
- strategies;
- expected reasoning path;
- worked examples;
- guided practice;
- controlled variation practice;
- independent practice;
- mixed/spiral practice;
- misconceptions;
- diagnostic probes;
- repair paths;
- mastery evidence;
- transfer tasks.

### Stage 7 — Question design

Do not generate large banks by changing numbers only.

Select questions from controlled archetypes such as:

```text
DIRECT_CALCULATION
MODEL
MODEL_TO_EQUATION
EQUATION_TO_MODEL
MISSING_VALUE
REVERSE
ESTIMATE
COMPARE
WORD_PROBLEM
CHOOSE_OPERATION
CHOOSE_STRATEGY
EXPLAIN
JUSTIFY
ERROR_ANALYSIS
MULTI_STEP
OPEN_RESPONSE
CONSTRAINT
PATTERN
OLYMPIAD_TRANSFER
```

Each question should carry the fields required by the core/chapter schema, including:

- classification;
- provenance;
- learning fingerprint;
- number structure;
- representation;
- reasoning moves;
- difficulty vector;
- prerequisites;
- what to notice;
- recognition cues;
- concept trigger;
- helper;
- progressive hints;
- solution and verification;
- misconceptions/error signatures;
- diagnostic/repair links;
- mastery evidence tags;
- transfer/analogue links.

### Stage 8 — Difficulty

Use a cognitive profile, not just `easy/medium/hard`.

Consider:

- concept demand;
- fact fluency;
- place value;
- recognition;
- representation;
- strategy selection;
- procedure;
- calculation;
- language;
- working memory;
- reasoning steps;
- context/remainder interpretation where relevant;
- transfer distance.

### Stage 9 — Helpers and hints

Helpers are teacher-like questions, not mini-solutions.

Default hint roles:

```text
H1 NOTICE
H2 REMEMBER
H3 REPRESENT
H4 PLAN
H5 DO
```

Hints must attach to distinct reasoning states. Avoid five paraphrases of the same clue.

### Stage 10 — Diagnostics

Use causal diagnosis:

```text
OBSERVED RESPONSE
  -> ERROR SIGNATURE
  -> POSSIBLE CAUSES
  -> DIAGNOSTIC PROBE
  -> EVIDENCE
  -> REPAIR CONCEPT/ACTIVITY
  -> ISOMORPHIC RETRY
  -> ORIGINAL RETRY when appropriate
```

Do not label a learner simply `weak in <topic>`.

### Stage 11 — Practice sequencing

Prefer deliberate progression:

```text
P0 prerequisite check
P1 worked model
P2 guided completion
P3 direct independent
P4 controlled number variation
P5 representation variation
P6 unknown-position variation
P7 application/word problem
P8 explanation/justification
P9 error analysis
P10 mixed spiral
P11 transfer
```

Interleave after initial acquisition so the operation/strategy is not obvious merely from page context.

### Stage 12 — Mastery

Do not infer mastery from repeated routine correctness alone.

Require evidence across relevant dimensions:

- conceptual understanding;
- representation;
- fluency;
- place value/procedure;
- recognition/application;
- strategy;
- contextual interpretation;
- reasoning;
- transfer.

Mastery thresholds belong to learner-state logic, not immutable question content.

### Stage 13 — Transfer

Use a controlled ladder:

```text
T0 PREREQUISITE_REPAIR
T1 NEAR_TWIN
T2 NUMBER_VARIATION
T3 REPRESENTATION_TRANSFER
T4 UNKNOWN_POSITION_TRANSFER
T5 CONTEXT_TRANSFER
T6 STRATEGY_TRANSFER
T7 MULTI_STEP_TRANSFER
T8 CONSTRAINT_REASONING
T9 OLYMPIAD_TRANSFER
```

Olympiad difficulty should come from structure, constraints, reverse reasoning, pattern, and transfer—not oversized arithmetic.

## Source fidelity and provenance

For source-grounded work:

- never silently repair source items;
- preserve source assets/models when mathematically meaningful;
- keep `VERIFIED_TRANSCRIPTION`, `RECONSTRUCTED`, `QC_ALERT`, or `SOURCE_UNRESOLVED` status;
- keep source-derived and newly authored questions separate;
- clearly mark extension/Olympiad content.

## Math quality gates

A mathematics deliverable is incomplete until applicable checks pass:

- `M-QG1 CONCEPT_COVERAGE`
- `M-QG2 PREREQUISITE_INTEGRITY`
- `M-QG3 REPRESENTATION_PROGRESSION`
- `M-QG4 QUESTION_ARCHETYPE_COVERAGE`
- `M-QG5 NUMBER_STRUCTURE_VARIATION`
- `M-QG6 REASONING_COVERAGE`
- `M-QG7 DIAGNOSTIC_CAUSALITY`
- `M-QG8 MASTERY_EVIDENCE`
- `M-QG9 TRANSFER_COVERAGE`
- `M-QG10 SOURCE_FIDELITY`
- `M-QG11 MATHEMATICAL_CORRECTNESS`
- `M-QG12 GRADE4_LANGUAGE_AND_SCOPE`

## Publishing handoff

If the user requests a PDF/book/workbook/teacher edition:

1. finish and validate subject content first;
2. load `../grade4-publishing/SKILL.md`;
3. load `Grade4PublishingSchema.md` and any chapter publishing contract;
4. pass validated Learning Cells, questions, models, answers, diagnostics, and provenance to the publishing workflow;
5. never modify mathematical meaning merely to make a page fit.
