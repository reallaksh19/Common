---
name: grade9-math-assimilation
description: Reproduce the Grade 9 Mathematics partial-knowledge assimilation workflow for difficult topics. Use when an agent must turn source-grounded Grade IX/X mathematics into a concept map, Assimilation Book, First-Step Reference, transfer/mastery layer, rendered PDFs, and QA for a learner who already knows about half the topic.
---

# Grade 9 Mathematics Assimilation

## Purpose

This skill is the execution/reproduction layer for the pedagogy developed in the Quadratics v2 benchmark.

Target learner:

> The student has about 50% of the concept already: definitions/formulas may be familiar, but the connections, decision boundaries, first moves, and transfer are unstable.

The goal is not to reteach from zero and not to compress immediately into a reference sheet. The goal is to repair missing mental links until the learner can recognize, explain, choose, execute, and transfer independently.

## Required upstream authorities

Read these before authoring:

1. `../grade9-math/SKILL.md`
2. `../grade9-math/references/concept-book-see-realize-understand-adopt.md`
3. `../grade9-math/references/partial-knowledge-assimilation-concept-map.md`
4. topic-specific source/coverage maps and concept dependencies;
5. the relevant benchmark artifact under `Grade 9/Mathematics/benchmarks/` when one exists.

For NMTC work also read the relevant `NMTC Preliminary/00_Authority` and topic Source Coverage Map before using PYQ IDs.

## Cognitive contract

Macro mathematics loop:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Operational assimilation loop:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Performance loop:

`RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER`

Do not collapse these into one list. The first is conceptual ownership, the second is teaching choreography, and the third is execution under problem-solving conditions.

## Mandatory pre-authoring concept map

Before prose, create a topic/subtopic map containing at least:

- `PRIOR_KNOWLEDGE`
- `LIKELY_HALF_KNOWLEDGE`
- `MISSING_BRIDGE`
- `INVARIANT_OR_STRUCTURE`
- `REPRESENTATIONS`
- `DECISION_BOUNDARIES`
- `MISCONCEPTION_TRAPS`
- `FIRST_MOVE_CUES`
- `TRANSFER_ENDPOINTS`
- `SOURCE_CUSTODY`

For each major node answer:

1. What does the student probably already know?
2. What connection is likely missing?
3. What familiar case can reconnect it?
4. What invariant/structure makes the idea make sense?
5. Which representation makes it visible?
6. What near-miss problem requires a different method?
7. What wrong move is tempting and why?
8. What first move should eventually become automatic?
9. What disguised transfer proves ownership?
10. What is the source/provenance status?

No difficult-concept prose should be written before this map exists.

## Execution sequence

### Step 0 - Ground scope and evidence

- identify topic and exact subtopic boundary;
- read source coverage/provenance files;
- classify clean anchors, bonus evidence, bridge evidence, source conflicts, and author-created needs;
- do not infer recurrence/weightage from sparse evidence;
- do not silently repair source defects.

### Step 1 - Reconnect

Start from knowledge the partial learner likely owns.

Use a short diagnostic that distinguishes:

- missing prerequisite;
- remembered formula without meaning;
- correct concept but weak representation choice;
- recognition failure;
- execution/calculation failure.

Do not use the diagnostic as a pass/fail label. Use it to choose the bridge to teach.

### Step 2 - Discover

Show a concrete pattern, example, diagram, representation, or contrast before the general compact statement.

Avoid naked formulas.

### Step 3 - Make sense

Explain why the idea works. As applicable:

- derive/reconstruct;
- explain signs/factors/exponents/index shifts;
- translate among representations;
- show invariant/structure;
- test edge cases;
- contrast with a plausible wrong model.

### Step 4 - Try before explanation is complete

The student must attempt a nearby question before seeing the full worked route.

Prefer first-move-only attempts before full solving.

### Step 5 - Diagnose

For each major concept, write the likely wrong move and classify the missing link:

- recognition;
- representation;
- invariant;
- condition/domain;
- execution;
- source-integrity/checking.

Explain why the wrong move looks reasonable and why it is inferior or invalid.

### Step 6 - Fade support

Use the four-level hint ladder:

- `H3 EXECUTION`: explicit next relation/equation;
- `H2 STRUCTURE`: invariant/representation cue;
- `H1 RECOGNITION`: clue/feature only;
- `H0 INDEPENDENT`: no hint.

Required progression:

`H3 -> H2 -> H1 -> H0`

Do not keep repeating H3-level worked scaffolding.

### Step 7 - Adopt

Require the learner to:

- recognize the concept without a chapter label;
- write the first useful line;
- reject a tempting wrong method;
- rebuild the result if the formula is removed.

### Step 8 - Transfer

Change surface wording/representation while preserving the invariant.

Transfer must be non-identical. Merely changing numbers is not sufficient.

### Step 9 - Build the First-Step Reference

Only after concept teaching is complete.

The reference is a compression/revision product, not the teaching product.

It should contain:

- recognition atlas;
- phrase/structure decoder;
- decision tree;
- First-Step cards;
- contrast pairs;
- recognition-only laboratory;
- quick source-to-first-step map;
- concise traps/checks.

### Step 10 - Build mastery/diagnostic layer

Use the six-question assimilation test for every major idea:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation needs a different method?
5. Can you write the first two useful lines without help?
6. Can you solve a disguised version?

For a capstone/mastery paper, remove method labels and default hints.

### Step 11 - Independent mathematics audit

Before promotion:

- recompute every numerical answer;
- check algebra independently from the written solution path;
- test condition endpoints/signs/domains;
- verify transformed variables/root relations;
- verify source-conflict disposition;
- correct stale answer headers, not merely annotate them as known defects.

### Step 12 - PDF production and render QA

For PDF output:

- use production mathematical typesetting;
- render the complete PDF to page images;
- inspect every page for clipping, overlap, broken glyphs, box/table breaks, equation spacing, and student/teacher leakage;
- run PDF preflight;
- record page count and SHA-256 for benchmark artifacts;
- do not call a source publication-ready only because static render QA passes.

Evidence-dependent classroom timing/readability remains `NOT_RUN` until observed.

### Step 13 - Benchmark comparison

Benchmark against the canonical PDF for:

- pedagogy;
- completeness;
- readability;
- concept-map coverage;
- contrast/decision boundaries;
- hint fading;
- independent first-move demand;
- transfer depth;
- source custody;
- production quality.

Do **not** copy wording, question text, layout, or visual composition. The benchmark is a minimum-quality comparator, not a template.

## Required output set

For a difficult topic/subtopic produce, as applicable:

1. concept map;
2. Assimilation Book/module;
3. First-Step Reference;
4. recognition/first-line practice;
5. transfer/mastery layer;
6. teacher diagnostic/answer key;
7. QA snapshot;
8. rendered PDF(s);
9. benchmark comparison note.

## Source integrity contract

Use the repository provenance vocabulary. For NMTC work preserve distinctions such as:

- `CLEAN_SCORED_ANCHOR`
- `BONUS_EVIDENCE`
- `BRIDGE_EVIDENCE`
- `SOURCE_CONFLICT_EVIDENCE`
- `AUTHOR_CREATED_FOUNDATION`
- `AUTHOR_CREATED_TRANSFER`

Historical IDs may ground mechanisms without reproducing full third-party statements.

Never convert a source conflict into a clean exercise by silently changing a sign, option, figure, or key.

## Gates

Required static gates:

- concept map exists;
- partial-knowledge diagnostic exists;
- missing bridge is explicit;
- no naked major formula;
- at least one contrast/decision boundary per major concept;
- attempt before hint;
- H3->H0 fading present;
- First-Step Reference comes after concept teaching;
- transfer is non-identical;
- independent math audit complete;
- source custody explicit;
- final notation/render QA complete.

Evidence-dependent gates:

- classroom timing/readability calibration: `NOT_RUN` until observed;
- longitudinal mastery evidence: `NOT_RUN` until observed;
- publication approval: separate decision.

## Completion states

Use one of:

- `DRAFT_CONCEPT_MAP`
- `INTERNAL_ASSIMILATION_COMPLETE`
- `STATIC_RENDER_QA_PASS`
- `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`
- `PUBLICATION_READY` only when all required human/evidence gates are actually closed.

## Quadratics benchmark and issue program

Canonical reproduction program:

- #36 Foundations / representations
- #37 Discriminant / repeated roots
- #38 Vieta / root invariants
- #39 Transformed & integer roots / structural reduction
- #40 Mixed mastery / transfer
- #41 coordination index

Read `references/quadratics-v2-retrace-runbook.md` for the exact sequence used to create the benchmark.
