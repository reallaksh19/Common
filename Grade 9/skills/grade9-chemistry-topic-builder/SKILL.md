---
name: grade9-chemistry-topic-builder
description: Build any source-grounded Grade 9 Chemistry topic as exactly two learner-facing PDFs: a Core Study Guide with mandatory Appendix A Core Practice, Appendix B Core Solutions and Appendix C Printable Handout, plus an ExamSIDE Solution & Transfer book with concept-segregation labels, badges, progressive hints, transfer metadata, source links and complete solutions. Use for Chemistry topic production before chapter aggregation or publication review.
---

# Grade 9 Chemistry Topic Builder

Use this skill whenever one Chemistry topic/subtopic is taken up for learner-facing production. This is the subject-wide authoring contract; Redox is only one instance.

Read `Grade 9/Chemistry/CHEMISTRY_PUBLICATION_SCHEMA.md` and conform to `Grade 9/Chemistry/schema/chemistry-topic-delivery.schema.json`.

## 1. Exactly two learner-facing files per topic

Every topic build produces exactly:

```text
1. <topic>_Core_Study_Guide.pdf
2. <topic>_ExamSIDE_Solution_Transfer.pdf
```

Do not create a third handout PDF. Chapter/master compilations may be created later, but they do not replace the two per-topic deliverables.

## 2. Core Study Guide contract

The Core Study Guide contains the connected teaching narrative first, using source-grounded Chemistry pedagogy:

```text
ORIENT / FAMILIAR CONTEXT
-> EXPLAIN IN ORDINARY LANGUAGE
-> MACRO / PARTICLE / SYMBOLIC REPRESENTATION AS NEEDED
-> KEY RULE / THINGS TO KNOW
-> WORKED REASONING
-> CONCEPT HELPER
-> MISCONCEPTION REPAIR
-> TRY WITH ME
-> FADED PRACTICE
-> INDEPENDENT CHECK
-> TRANSFER LINK
```

After the teaching section, the same PDF must contain all three appendices:

### Appendix A — Core Practice

- independent and faded topic practice;
- stable concept IDs/labels;
- sufficient variety to test recognition, representation and reasoning rather than surface copying;
- no leakage from Appendix B.

### Appendix B — Core Solutions

- complete solution for every Appendix A item;
- reasoning before final answer;
- chemistry-safe notation, conservation/charge/unit checks where relevant;
- misconception repair when the item targets a known wrong model.

### Appendix C — Printable Handout

Appendix C is mandatory and blocking.

It is a detachable revision handout inside the Core PDF, normally one or a few printable pages. It must be usable standalone and should contain only the minimum high-value topic reference:

- concept map / first-move workflow;
- key rules, conditions and exceptions;
- essential diagram/particle/symbolic representations;
- formula/notation or reaction pattern where relevant;
- common traps / misconception warnings;
- short self-check or retrieval prompts.

It must not become a dense answer key, must not require the main book to decode it, and must not introduce chemistry outside the source/topic boundary.

Emit:

```text
APPENDIX_A_PRESENT = 1
APPENDIX_B_PRESENT = 1
APPENDIX_C_HANDOUT_PRESENT = 1
HANDOUT_STANDALONE_USABLE = 1
HANDOUT_SCOPE_LEAKS = 0
```

Any missing/failed value blocks the Core Study Guide.

## 3. ExamSIDE Solution & Transfer contract

The second PDF is attempt-first external-question practice plus support and full solutions.

Every placed eligible question must visibly carry:

```text
QUESTION ID
SOURCE / YEAR / SHIFT BADGE
SOURCE LINK
PRIMARY CONCEPT LABEL
CONCEPT SEGREGATION LABEL
SECONDARY / PREREQUISITE CONCEPT LABELS when needed
DIFFICULTY BADGE
TRANSFER BADGE
SCOPE / PLACEMENT BADGE when useful
CORE STUDY GUIDE CROSS-LINK
H0 INDEPENDENT ATTEMPT
H1 / H2 / H3 progressive hints as required
QUESTION-SPECIFIC CONCEPT HELPER when needed
MISCONCEPTION WATCH when needed
COMPLETE SOLUTION
```

### Concept segregation label

The learner must be able to see what the question is primarily testing versus what is merely prerequisite/supporting knowledge. Use a clear pattern such as:

```text
PRIMARY: <concept>
SUPPORTS: <concept>, <concept>
```

Every scored/external question has exactly one primary concept ID.

### Badge contract

At minimum expose:

- source/date/shift badge;
- difficulty badge;
- transfer badge;
- primary concept badge/label.

Transfer badge vocabulary is topic-configured, but examples include:

```text
DIRECT
REPRESENTATION_SHIFT
MULTI_CONCEPT
FAR_TRANSFER
CUMULATIVE
```

Do not use a badge as a substitute for explanation.

### Hint ladder

```text
H0 = independent attempt, no hint shown
H1 = direction / first observation
H2 = representation / method cue
H3 = strong scaffold without giving the final answer
FULL SOLUTION = after attempt/hints, in the same PDF
```

Difficulty determines how many optional hints are required. Hints must be question-specific and progressively revealing.

## 4. Source and external-corpus grounding

- Treat supplied topic sources as the chemistry scope authority.
- Freeze source obligations before drafting.
- If ExamSIDE/another corpus is in the brief, enumerate and classify candidates before final publication.
- Keep source-derived teaching and external-question evidence distinguishable.
- Never widen the topic merely to make an external question fit.

## 5. Chemistry representations

Choose representations by concept need, not decoration:

- macroscopic observations;
- particle/structure views;
- symbolic formulas/equations;
- conservation ledgers;
- decision trees / before-after lanes;
- apparatus/process diagrams where experimentally relevant.

All chemistry typography must be unambiguous at 100% zoom.

## 6. Completion gate

A topic is not complete until both PDFs pass:

```text
SOURCE = PASS
CORE_PEDAGOGY = PASS
APPENDIX_A = PASS
APPENDIX_B = PASS
APPENDIX_C_HANDOUT = PASS
EXAMSIDE_SUPPORT = PASS
CONCEPT_SEGREGATION = PASS
TRANSFER_METADATA = PASS
TYPOGRAPHY = PASS
LAYOUT = PASS
LINKS = PASS
```

Run the relevant source/completeness/transfer auditors and then `$grade9-chemistry-publication-review` when packaging for repository review.
