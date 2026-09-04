---
name: ioqm-grade9-study-guide-builder
description: Build or revise a Grade 9 competitive-exam study guide from supplied questions and repository material using a two-layer Analysis Engine -> Student Book Generator architecture, stable skills, dependency graphs, transfer-gap bridges, progressive hints, difficulty/source metadata, visual obligations, and rendered PDF QA.
---

# IOQM Grade 9 Study Guide Builder

## Purpose

Use this skill when the goal is to turn a supplied competitive-exam question corpus into a **self-sufficient, student-friendly study guide** for a Grade 9 learner with partial prior knowledge.

The builder must solve two different problems:

1. **Analysis Engine** - determine what the corpus actually requires the learner to recognize and execute.
2. **Student Book Generator** - present that internal model through a simple, readable learner interface.

The student should not see most of the production machinery.

Core principle:

```text
powerful internal analysis
        ->
simple student surface
```

---

## Mandatory references and precedence

Before a production build, read in this order:

### 1. v3 organizing contract - always

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/analysis-engine-student-book-generator-contract-v3.md`

This is the organizing contract for:

- corpus decomposition;
- concept/method graph;
- opening-signature skill splitting;
- prerequisite DAG;
- transfer-gap analysis;
- evidence-driven Worked Bridges;
- Analysis Engine -> Student Book Generator hard gate;
- simplified student-surface grammar;
- student edition vs reviewer/build dossier separation.

### 2. v2 detailed self-sufficiency contract - always

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2.md`

Use it for detailed question-to-method support, stable IDs, orphan-method repair, Appendix A/B/C behavior, progressive local hints, self-sufficiency audit, short-horizon routing, and inspected PDF delivery.

Where the v3 contract and v2 contract organize the same workflow differently, **v3 controls pipeline order, concept splitting, bridge triggering, and student-surface presentation**. The v2 contract remains authoritative for detailed custody/support/QA requirements not replaced by v3.

### 3. difficulty / provenance / progression - always

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/difficulty-badges-portability-and-challenge-ladders-addendum.md`

Keep separate:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

### 4. learner-specific routing - when applicable

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/learner-knowledge-profile-and-readiness-addendum.md`

Use the most specific evidence available. Do not flatten topic/subtopic/skill knowledge into one global percentage.

### 5. visual-production contract - whenever any visual is not NONE

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md`

A required visual is a teaching obligation, not optional polish.

### 6. domain profile - when available

Read the domain profile after the generalized contracts.

Current profiles include:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/algebra-question-driven-profile-v2.md`

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/number-theory-question-driven-profile-v1.md`

A domain profile specializes representations, legality, visuals, skill families, difficulty anchors and method-selection boundaries. It may not weaken generalized custody, self-sufficiency or QA gates.

### User overrides

Explicit user requirements remain binding. For example, a request for **strict questions-only** overrides the default local-hint display in the appendix.

---

# Layer A - Analysis Engine

Do not draft chapters first.

## A1. Freeze the corpus

Inventory every supplied question/source before teaching design.

Preserve:

- stems;
- source/provenance status;
- corrections/repairs;
- stable local IDs;
- source-required figures;
- answer custody when available.

Source order does not determine teaching order.

## A2. Decompose every question

For every question record:

- topic;
- subtopic;
- concept;
- candidate method/stable skill;
- decisive recognition cue;
- representation/compression move;
- first executable move;
- execution requirements;
- legality/reversibility/admissibility;
- prerequisites;
- misconception risk;
- difficulty;
- priority;
- learner mastery/risk when known;
- visual requirement;
- hint depth when allowed;
- provenance;
- transfer-gap status;
- final support status.

Canonical route:

```text
question
-> concept
-> stable skill
-> recognition
-> representation
-> first move
-> execution
-> check
```

## A3. Build the concept/method graph

For large corpora, explicitly construct:

```text
DOMAIN
`-- TOPIC
    `-- SUBTOPIC
        `-- CONCEPT
            `-- STABLE SKILL / METHOD
                |-- recognition
                |-- representation
                |-- first move
                |-- legality
                |-- question IDs
                `-- bridge IDs
```

The graph may be CSV/YAML/Markdown, but it must be auditable.

## A4. Split broad concepts by Opening Signature

Define:

```text
Opening Signature
= recognition cue
+ representation
+ first executable move
+ legality/check
```

Split whenever question families materially differ in any of those components.

Hard rule:

```text
SPLIT if recognition differs materially
OR representation differs materially
OR first move differs materially
OR legality differs materially.
```

Umbrella labels may remain for navigation but may not hide distinct executable engines.

## A5. Assign stable skills

Each stable skill needs:

- stable ID;
- readable name;
- prerequisites;
- recognition signature;
- representation;
- first move;
- normal execution closure;
- legality/check;
- close contrast;
- worked example when non-routine;
- question links;
- bridge links;
- visual obligation when required.

## A6. Build the prerequisite DAG

Teaching order comes from dependencies, not question numbering.

Reject unjustified cycles.

Short-horizon personalization may skip secure skills for one learner, but the durable core keeps the real dependency order.

## A7. Run orphan-method analysis

A question is orphaned if the guide still expects an unnamed trick.

Required route:

```text
recognition
-> retrieval
-> first executable move
-> executable continuation
-> legality/check
```

Required gate:

`ORPHAN_METHODS = 0`

## A8. Audit transfer gaps

A Worked Bridge exists to close a real graph jump:

```text
taught skill
-> normal example
-> transfer gap
-> target family
```

Classify:

```text
NONE / MODERATE / HARD
```

Every HARD gap requires a bridge.

Bridge count is evidence-driven, not a fixed quota.

## A9. Audit visuals

Choose explicitly:

```text
VISUAL_NONE
VISUAL_OPTIONAL
VISUAL_REQUIRED
VISUAL_SOURCE_REQUIRED
```

A required visual must have a stated teaching job and must flow through the visual-production addendum to final-size rendered QA.

## A10. Qualify the Analysis Engine

Minimum hard gates:

```text
CORPUS_FROZEN = PASS_n_OF_n
QUESTION_DECOMPOSITION = PASS_n_OF_n
QUESTION_TO_CONCEPT_BINDING = PASS_n_OF_n
CONCEPT_SPLIT_AUDIT = PASS
STABLE_SKILL_OPENING_SIGNATURE = PASS_n_OF_n
PREREQUISITE_GRAPH = PASS
UNJUSTIFIED_PREREQUISITE_CYCLES = 0
ORPHAN_METHODS = 0
TRANSFER_GAP_AUDIT = PASS_n_OF_n
HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
VISUAL_OBLIGATIONS = PASS_n_OF_n
```

Until these pass:

`STUDENT_BOOK_GENERATION_ALLOWED = FALSE`

---

# Layer B - Student Book Generator

The book must be easier to navigate than the analysis that produced it.

## B1. Derive teaching order from the graph

Do not recreate source order.

A strong generic progression is:

```text
foundations
-> direct methods
-> conditional/legal variants
-> representation changes
-> advanced transfer
-> mixed method selection
```

Domain profiles provide the concrete order.

## B2. Stable-skill page grammar

Default student surface:

```text
REMEMBER
What you already know.

SEE THE IDEA
The upgrade and mechanism.

TRY IT
A non-identical worked example.

FIRST MOVE
The legal opening to write/draw now.

WATCH OUT
Close contrast + common mistake + legality/check.

PRACTISE
Quiet pointers to relevant questions/ladder rungs.
```

Exact page layout may vary by domain, but these semantic anchors must remain easy to scan.

### FIRST MOVE is special

The learner should be able to locate it without reading the surrounding paragraph.

Required gates:

```text
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_PARAGRAPH_SCAN = PASS_n_OF_n
```

## B3. Learner-facing language

Write like a strong teacher, not a production system.

Prefer:

- Notice;
- Recall;
- Start;
- Check;
- Why this works;
- Try it;
- Watch out;
- First move.

Internal QA may use H0/H1/H2/H3, RMSEC, transfer-gap states, graph IDs or gates.

Do not make opaque production codes the main student language.

`ANALYSIS_JARGON_LEAKAGE = 0`

## B4. Progressive help

When local hints are allowed:

```text
NOTICE - recognition only
RECALL - readable prior skill; stable ID may appear secondarily
START - first executable setup only
```

Fade help across attempts:

```text
first similar problem: Notice / Recall / Start if needed
next: maximum Recall
then: Notice only
mixed transfer: no hints
```

Do not reveal an answer or complete the decisive execution unless the user asks for solutions.

## B5. Worked Bridges

A bridge must expose enough intermediate reasoning to imitate and must remain non-identical to the target problem.

Minimum bridge anatomy:

1. recognition cue;
2. why the representation fits;
3. first move;
4. intermediate execution;
5. closure;
6. legality/equality;
7. nearby wrong route;
8. transfer prompt.

## B6. Short-horizon Navigator

When only a few days are available:

```text
Quick Check
-> identify weak/high-value skills
-> route to stable skill
-> practise with fading help
-> mixed retest without topic labels
```

Keep the visible routing simple:

```text
DO FIRST
DO NEXT
QUICK RETEST
ONLY IF TIME
```

Do not expose a method-revealing router before the unaided diagnostic.

Difficulty badges support orientation; they do not create a hardest-first route.

## B7. Difficulty / source badges

Use the difficulty addendum.

Typical learner-facing practice header:

```text
Q17                         [D4 ADVANCED] [SRC 7]
```

Broad topics should normally show ranges rather than one misleading difficulty number.

Source badges are shortcuts to provenance, not substitutes for the full ledger.

## B8. Appendix A - deliberate practice

If the user requests strict questions-only, obey that request.

Otherwise, for a partial-knowledge learner, local support may use Notice / Recall / Start at the assigned depth.

Every question must still map to a taught stable skill/bridge.

Answer key only after the final Appendix A question.

## B9. Appendix B - mixed independent transfer

Appendix B tests transfer; it is not another teaching chapter.

Rules include:

- verified source identity or clear author-created status;
- mixed method balance;
- topic labels hidden when transfer is being tested;
- adaptive rescue support only when specified;
- answers after the final item;
- every answer independently recomputed;
- problem-essential visuals preserved.

Keep role separation:

```text
APPENDIX_B = TEST_TRANSFER
CHALLENGE_LADDER = TRAIN_PROGRESSION
```

## B10. Appendix C - decision-first memory helper

Start with:

```text
What do I see?
-> What should I write/draw first?
-> What must I check?
```

Include triggers, first moves, high-value formulas, legality conditions and a final check list.

Prefer micro-models over extra prose when a visual representation carries the method.

## B11. Student edition vs reviewer/build dossier

Preferred publication split:

```text
STUDENT EDITION
- Navigator when needed
- teaching core
- Worked Bridges
- support map
- Appendix A
- Appendix B
- Appendix C

REVIEWER / BUILD DOSSIER
- corpus registry
- concept/method graph
- question-to-method matrix
- orphan-method audit
- transfer-gap audit
- visual manifest/audit
- provenance/custody ledger
- static self-sufficiency gates
- final QA record
```

Do not put PR numbers, production-state labels, or gate tables in the normal student page header.

## B12. Final integrated gates

At minimum:

```text
STUDENT_SURFACE_SEMANTIC_GRAMMAR = PASS
FIRST_MOVE_PROMINENCE = PASS_n_OF_n
ANALYSIS_JARGON_LEAKAGE = 0
LOCAL_HINT_AUDIT = PASS_n_OF_n
QUESTION_CUSTODY = PASS_n_OF_n
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n
DIFFICULTY_PRIORITY_MASTERY_CONFLATION = 0
```

Then apply all triggered visual, provenance, answer and final-PDF gates from the existing references.

---

## PDF rule

For a final PDF:

- render the complete artifact;
- inspect representative and critical pages at final reading size;
- inspect every required visual at final size;
- reject clipping, overlaps, broken glyphs, black squares, off-page tables, unreadable badges, and solution-leaking visuals;
- keep reviewer evidence separate from the student reading path unless the user explicitly requests one combined artifact.

---

## Evidence boundary

Static production gates demonstrate document coverage only.

Do not claim learner success, retention, contest score, classroom timing or psychometric calibration without observed learner evidence.

---

## Final rule

A guide is successful when the target learner can answer:

```text
What am I seeing?
What representation should I use?
What is the first legal move?
How do I continue?
What can make this route wrong or illegal?
Where should I practise it again?
```

without relying on an unnamed trick that exists only in the teacher's head.
