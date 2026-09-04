---
name: ioqm-grade9-study-guide-builder
description: Build or revise Grade 9 IOQM/competitive study guides as a specialization of the Grade 9 learning platform, using source-grounded canonical master data plus corpus decomposition, opening signatures, concept assimilation, learner routing, transfer-gap analysis, visual obligations, progressive hints, badges, and rendered PDF QA.
---

# IOQM Grade 9 Study Guide Builder

## Purpose

Use this skill when a Grade 9 learner must turn a syllabus plus a supplied contest corpus into a concept-assimilation study guide that is both source-grounded and executable.

This skill is **not a parallel replacement** for the generic Grade 9 system. It specializes the existing Grade 9 source, concept, difficulty, question-bank, enrichment, master-data, and publishing contracts for IOQM-style contest preparation.

Core principle:

```text
Grade 9 platform infrastructure
+
IOQM contest-corpus assimilation engine
->
student can recognize, start, execute, transfer and check
```

The student should see a simple teaching journey. The build system may remain complex underneath.

---

# 0. Mandatory inherited Grade 9 contracts

Before a production build, reuse these existing Grade 9 skills/contracts:

1. `Grade 9/skills/grade9-source-grounding/SKILL.md`
   - source fidelity, QC statuses, provenance classes.

2. `Grade 9/skills/grade9-concept-architect/SKILL.md`
   - stable concept IDs, prerequisite graph, one primary concept ID per scored question.

3. `Grade 9/skills/grade9-math/SKILL.md` for Mathematics
   - partial-knowledge assimilation, representation switching, competing-method contrasts, difficulty vector, attempt-before-hint, hint fading and transfer.

4. `Grade 9/skills/grade9-question-bank/SKILL.md` when creating calibrated original practice, Challenge Ladders, Appendix B originals, or mixed mastery sets.

5. `Grade 9/skills/grade9-learning-enrichment/SKILL.md`
   - causal misconception/repair objects, diagnostics, progressive support and transfer checks.

6. `Grade 9/skills/grade9-textbook-publisher/SKILL.md`
   - canonical-master-first publishing, linked products, render/link QA.

7. `Grade 9/skills/grade9/references/grade9-master.schema.json`
   - canonical reusable master-data base schema.

8. `Grade 9/skills/grade9/references/grade9-workflow.md`
   - generic Grade 9 multi-stage workflow.

Then read IOQM-specific references:

9. `references/grade9-platform-integration-addendum-v1.md`
10. `references/analysis-engine-student-book-generator-contract-v3.md`
11. `references/compression-loss-preservation-and-concept-assimilation-addendum-v1.md`
12. `references/question-driven-self-sufficient-study-guide-skill-v2.md`
13. `references/difficulty-badges-portability-and-challenge-ladders-addendum.md`
14. `references/learner-knowledge-profile-and-readiness-addendum.md` when learner-specific routing is required.
15. `references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md` whenever any visual obligation is not NONE.
16. Relevant domain profile, e.g. Algebra or Number Theory.

### Precedence

- Grade 9 source-grounding controls source status/provenance vocabulary and no-silent-repair policy.
- Grade 9 master schema is the canonical base structured-data contract.
- Grade 9 subject skill controls subject-specific reasoning/difficulty foundations.
- IOQM v3 controls contest-corpus decomposition, opening signatures, transfer gaps and self-sufficiency.
- Compression/assimilation addendum controls learner-facing teaching depth, variants, readable maps and prototype gates.
- v2 remains authoritative for detailed Appendix A/B/C behavior, custody, hints and integrated support requirements not replaced above.
- Grade 9 publisher controls master-data-first artifact generation and publication QA.
- Explicit user requirements override defaults.

---

# 1. Canonical workflow

Use this sequence for a full build.

## Step 1 - Identify and freeze syllabus/scope

Establish the syllabus boundary before allowing the question corpus to define the curriculum.

Create:

```text
DOMAIN
-> TOPIC
-> SUBTOPIC
-> preliminary concepts
```

Mark material as appropriate to the project, for example:

```text
CORE
EXTENSION
OUTSIDE_SCOPE
```

Do not silently widen scope because an interesting source exists.

## Step 2 - Research and source-ground the domain

When web/repository research is requested or needed, prefer the source hierarchy from `grade9-source-grounding`.

Collect reusable material such as:

- definitions/theorems;
- conceptual explanations;
- worked-example candidates;
- variants and close contrasts;
- common misconceptions;
- legality/boundary conditions;
- visual-helper ideas;
- official/verified contest questions and provenance.

Store research as reusable `.md` source notes in the appropriate domain folder. Keep raw research separate from final student prose.

## Step 3 - Freeze Appendix A corpus and custody

The corpus may contain 20, 50, 90, 200, or any other number of items. The count is not a design target.

For every item preserve:

- exact/custody-preserved stem;
- stable local question ID;
- source page/question identifier;
- source-required figure;
- answer when supplied;
- source QC status;
- provenance class;
- correction/reconstruction record if needed.

Reuse Grade 9 statuses:

```text
VERIFIED_TRANSCRIPTION
RECONSTRUCTED
QC_ALERT
SOURCE_UNRESOLVED
```

A `SOURCE_UNRESOLVED` item must not silently become a scored clean item.

## Step 4 - Decompose every question

This happens **before final teaching-unit design**.

Every target question needs at minimum:

```text
question ID
syllabus topic/subtopic
primary concept ID
secondary concept IDs
recognition cue
representation/compression
first executable move
execution route
legality/check
prerequisites
likely misconception
variant requirement
transfer-gap status
visual obligation
difficulty vector
simple difficulty badge
source/provenance
hint route
support status
```

Canonical executable route:

```text
surface wording
-> recognition
-> representation
-> first move
-> execution
-> legality/check
-> variant/transfer when needed
```

A primary concept ID is necessary for navigation and analytics but does **not** by itself prove support sufficiency.

## Step 5 - Build concept graph and teaching-unit architecture

Use stable concepts/prerequisites from the Grade 9 concept architect.

For contest support, additionally use the IOQM **Opening Signature**:

```text
recognition
+ representation
+ first move
+ legality/check
```

Split internal support nodes when materially different openings are required.

But do **not** impose:

```text
one internal skill = one student page
one concept ID = one teaching unit
one analysis count = one chapter count
```

Student teaching units may merge, split, nest, or expand internal concepts whenever concept assimilation demands it.

### Design rule

```text
CONCEPT_ASSIMILATION determines book structure.
QUESTION COVERAGE audits the structure.
```

No predetermined number of concepts, skills, chapters, or pages is a success criterion.

## Step 6 - Build prerequisite and transfer graph

Teaching order comes from conceptual dependency, not corpus numbering.

Run:

- prerequisite-cycle audit;
- orphan-method audit;
- variant audit;
- transfer-gap audit;
- visual-obligation audit.

Every HARD transfer gap requires a learner-usable Variant / Transfer Lab / Worked Bridge.

`ORPHAN_METHODS = 0`

## Step 7 - Assign difficulty and learner-facing badges

Use the Grade 9 Mathematics difficulty vector underneath:

```text
conceptual
recognition
reasoning_steps
algebra
hidden_structure
constraints_cases
calculation_burden
trap_density
```

Simple student badges summarize rather than replace this model.

Keep separate:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != SOURCE_STATUS
DIFFICULTY != FREQUENCY
```

### Concept badge example

```text
Chinese Remainder Theorem
[CORE D3] [TRANSFER D5] [HIGH-YIELD]
```

### Question badge example

```text
Q17 [D4 ADVANCED] [TRANSFER] [OFFICIAL PYQ]
```

After learner diagnosis, separate personalization badges may appear:

```text
[YOUR STATUS: DEVELOPING] [DO FIRST]
```

## Step 8 - Ask learner knowledge, then verify with an unaided diagnostic

A learner may report `30%`, `60%`, etc. Treat this as context, not as the full model.

Use:

```text
self-report
+
short unaided recognition/first-move diagnostic
```

The diagnostic should usually ask:

- What do you notice?
- Which representation/method family fits?
- What is the first useful line/drawing?

Do not reveal method-revealing routing before scoring the unaided attempt.

## Step 9 - Create Part 0 / T1...Tx learner route

Part 0 is learner-specific orchestration, not the durable knowledge architecture.

Route using:

```text
syllabus value
+ prerequisite value
+ learner weakness
+ transfer value
+ time available
```

Visible route labels should remain simple:

```text
DO FIRST
DO NEXT
QUICK RETEST
ONLY IF TIME
```

A concept may show authored difficulty, learner status and priority as separate badges.

## Step 10 - Prototype the student surface before bulk generation

Before creating the full book, render and inspect at least:

- one substantial concept-assimilation journey;
- one Appendix A question/practice page with badges and hints;
- one Part 0/navigation page;
- one required-visual page when applicable.

Do not scale until the prototype is approved.

Reject prototypes with:

- card-reader teaching flow;
- low-contrast/broken heading colors;
- raw-ID dominance;
- tiny badges/navigation;
- insufficient mechanism explanation;
- vague FIRST MOVE/WATCH OUT/CHECK;
- missing variants where nearby methods are easily confused.

## Step 11 - Expand all required teaching units

Expand based on assimilation and corpus support, not target page count.

A teaching unit may use roles such as:

```text
WHAT IS THIS?
TINY CONCRETE EXAMPLE
CONNECTS TO...
WHY / MECHANISM
COMPLETE WORKED EXAMPLE
FIRST MOVE
VARIANT
SUBTLE VARIANT / CLOSE CONTRAST
WATCH OUT
CHECK
VISUAL HELPER
GUIDED PRACTICE
NOTICE / RECALL / START
INDEPENDENT PRACTICE
```

These are teaching roles, not compulsory equal-weight boxes.

For unfamiliar/strategic concepts, establish the idea before presenting the shortcut.

## Step 12 - Generate extra practice only when needed

The frozen Appendix A corpus remains source-grounded.

When additional same-level/challenge questions are needed, use `grade9-question-bank` and preserve its difficulty-vector and relationship checks.

Use calibrated originals for:

- same-level reinforcement;
- structural analogues;
- advanced transfer;
- Appendix B author-created mixed transfer;
- mastery retests.

## Step 13 - Build progressive help

For normal IOQM learner-facing support:

```text
NOTICE - recognition clue only
RECALL - readable concept / representation
START - first executable setup only
```

Use H0/unaided attempt before support in diagnostic/testing contexts.

Fade support across later problems.

Use causal misconception repair from the Grade 9 enrichment skill:

```text
wrong response
-> likely misconception
-> diagnostic probe
-> targeted repair
-> retry / transfer
```

## Step 14 - Generate student package

Typical full student package:

```text
PART 0
learner-specific Navigator / T1...Tx

CORE
concept-assimilation teaching journeys

APPENDIX A
frozen deliberate-practice corpus
question difficulty/source/role badges
progressive local hints when allowed
answers only after the final question

APPENDIX B
independent mixed transfer / challenge set

APPENDIX C
decision-first rapid reference
What do I see? -> What do I write/draw first? -> What do I check?

APPENDIX D
when requested/used: answers + concise student-readable provenance/source notes
```

Reviewer/build dossier stays separate and may include:

- corpus registry;
- master-data export;
- concept/method graph;
- question decomposition matrix;
- orphan/transfer audits;
- visual manifest;
- custody/provenance ledger;
- static gates;
- final QA evidence.

## Step 15 - Publish from canonical master data

Use `grade9-master.schema.json` as the base source of truth and extend it with IOQM-specific fields; do not create a competing canonical schema.

Every scored question keeps exactly one `primary_concept_id` and may have secondary concepts.

Store IOQM extensions such as:

```text
recognition_cue
representation
first_move
execution_route
legality_check
variant_ids
transfer_lab_ids
visual_obligation
hint_route
support_status
```

PDF pages are render outputs, not source-of-truth objects.

Use the Grade 9 publisher's linked architecture:

```text
Concept
<-> Core practice
<-> Challenge / transfer
<-> Helper / hint
<-> Solution / answer
<-> Misconception diagnosis
<-> Mixed-test diagnosis
```

## Step 16 - Final integrated QA

Minimum gates:

```text
SYLLABUS_SCOPE_FROZEN = PASS
SOURCE_GROUNDING = PASS_n_OF_n
CORPUS_CUSTODY = PASS_n_OF_n
QUESTION_DECOMPOSITION = PASS_n_OF_n
PRIMARY_CONCEPT_ID = PASS_n_OF_n
QUESTION_EXECUTABLE_ROUTE = PASS_n_OF_n
PREREQUISITE_GRAPH = PASS
ORPHAN_METHODS = 0
UNTAUGHT_REQUIRED_VARIANTS = 0
HARD_TRANSFER_GAPS_WITHOUT_SUPPORT = 0
REQUIRED_VISUALS_MISSING = 0
HINT_LEAKAGE = 0

GRADE9_DIFFICULTY_VECTOR = PASS_n_OF_n_WHERE_SCORED
CONCEPT_DIFFICULTY_BADGES = PASS_n_OF_n_WHERE_DISPLAYED
QUESTION_DIFFICULTY_BADGES = PASS_n_OF_n_WHERE_DISPLAYED
DIFFICULTY_PRIORITY_MASTERY_CONFLATION = 0

FIRST_MOVE_CONCRETE = PASS
WATCH_OUT_CONCRETE_FOR_RISKY_METHODS = PASS
CHECK_EXECUTED_FOR_RISKY_METHODS = PASS
GUIDED_PRACTICE_FOR_TRANSFER_HEAVY_UNITS = PASS
CONCEPT_LINKS_VISIBLE = PASS

STUDENT_SURFACE_PROTOTYPE = PASS
LOW_CONTRAST_HEADINGS = 0
BROKEN_HEADING_COLORS = 0
TINY_NAVIGATION_OR_BADGES = 0
RAW_INTERNAL_ID_DOMINANCE = 0
CARD_READER_PAGE_FAILURES = 0

GRADE9_MASTER_SCHEMA_IS_CANONICAL = PASS
MASTER_LINKS = PASS
ANSWER_QA = PASS
FINAL_RENDER_QA = PASS
```

Apply all additional triggered gates from the referenced IOQM and Grade 9 contracts.

---

# Student-surface principles

## Teacher-like flow, not a card stack

A concept page should teach the idea before compressing it into retrieval aids.

For a difficult unfamiliar concept, a strong sequence is often:

```text
plain definition
-> tiny numerical/visual example
-> why this matters in IOQM
-> mechanism
-> complete worked example
-> concrete FIRST MOVE
-> variants and subtle contrast
-> concrete WATCH OUT
-> executed CHECK
-> guided practice
-> fading hints
-> independent transfer
```

Not every concept needs every stage.

## FIRST MOVE

Make it prominent and concrete.

Bad:

> Compute the gcd first.

Better:

```text
84x + 126y = 30

gcd(84,126)=42
42 does not divide 30
STOP: no integer solutions.
```

## WATCH OUT

Show actual mathematics/counterexample when possible, not generic warnings.

## CHECK

Execute the check with numbers/symbols when possible.

## Visual helper

Use a visual when it externalizes structure the learner would otherwise need to hold mentally.

A visual requirement is an analysis obligation and must reach final-size rendered QA.

## Concept links

Show readable concept relationships when they help assimilation, for example:

```text
GCD -> Bezout -> modular inverse -> CRT
```

or:

```text
prime factorisation -> exponent vectors -> divisor count -> perfect powers -> valuations
```

Internal IDs remain secondary.

---

# Evidence boundary

Static build gates prove document/package coverage only.

Do not claim measured retention, contest score, solve rate, psychometric calibration, classroom timing or guaranteed performance without learner evidence.

---

# Final rule

The internal machinery may contain syllabus graphs, stable IDs, source states, difficulty vectors, transfer edges, visual obligations and QA ledgers.

The learner should experience a coherent book that helps answer:

```text
What is this idea?
How is it connected to what I already know?
What clue should make me notice it?
What representation should I use?
What do I write or draw first?
Which nearby variant changes the method?
What can make the move illegal or wrong?
How do I check it?
Where do I practise it with less help next time?
```
