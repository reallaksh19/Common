---
name: ioqm-grade9-study-guide-builder
description: Build or revise a Grade 9 competitive-exam study guide from large or small question corpora using a qualified analysis engine, opening-signature skill decomposition, prerequisite and transfer-gap graphs, configurable learner knowledge, portable domain profiles, difficulty/source badges, challenge ladders, student-friendly teaching pages, and traceable visual/PDF QA.
---

# IOQM Grade 9 Study Guide Builder

## Purpose

Use this skill to turn a supplied competitive-exam corpus into a **teacher-style, student-friendly study guide**.

The core problem is not merely solving questions. It is discovering the correct teachable structure hidden inside them:

```text
questions
→ decomposition
→ concepts / methods
→ stable skills
→ prerequisite order
→ transfer gaps
→ teaching pages
→ guided + independent practice
```

The analysis may be technically rich. The learner interface must remain simple.

This builder is an orchestrator. Domain-specific reasoning belongs in domain profiles so the same architecture can later support Mathematics, Physics, and Chemistry.

---

## Mandatory references

Before production, read:

1. `references/question-driven-self-sufficient-study-guide-skill-v2.md`
   - detailed self-sufficiency, hints, Appendix A/B/C, bridge, audit, and PDF contract.

2. `references/analysis-engine-opening-signatures-and-student-surface-addendum.md`
   - **organizing architecture for corpus decomposition, concept splitting, concept/method graphs, prerequisite DAGs, transfer gaps, and the student surface.**
   - this addendum takes precedence over older linear-pipeline wording for those fields.

3. `references/difficulty-badges-portability-and-challenge-ladders-addendum.md`
   - portable difficulty model, learner-facing `D1-D5` badges, topic/concept bands, source mini-badges, and Challenge Ladders.

When learner knowledge or short-horizon routing is involved, also read:

4. `references/learner-knowledge-profile-and-readiness-addendum.md`
   - optional subject/topic/subtopic/skill knowledge;
   - specificity precedence;
   - flexible `T1 ... Tx` Quick Check selection.

If any pedagogical visual is `OPTIONAL`, `REQUIRED`, or `SOURCE_REQUIRED`, also read:

5. `references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md`

When a domain profile exists, read it **after** the generalized contracts. Domain profiles specialize the generic system; they do not weaken its gates.

Current example:

`references/algebra-question-driven-profile-v2.md`

---

# ORGANIZING BACKBONE

Production has two literal layers.

```text
LAYER A — ANALYSIS ENGINE

1. Freeze corpus
2. Decompose every question
3. Build Topic → Subtopic → Concept → Method graph
4. Run Opening-Signature / concept-splitting audit
5. Assign stable skills
6. Build prerequisite DAG
7. Run orphan-method audit
8. Assign difficulty + source + visual metadata
9. Audit transfer gaps
10. Create only required Worked Bridges
11. Qualify analysis package

================ HARD GATE ================

LAYER B — STUDENT BOOK GENERATOR

12. Derive learner/chapter order
13. Render student-facing teaching units
14. Integrate required visuals
15. Build Appendix A
16. Build Appendix B
17. Build Appendix C
18. Build / integrate Challenge Ladders
19. Add optional short-horizon Navigator
20. Run integrated question-level audits
21. Generate PDF
22. Preflight, render at 200 dpi, inspect, close QA
```

Do not begin final student-book production from attractive chapter headings alone.

```text
STUDENT_BOOK_GENERATION_ALLOWED = FALSE
```

until the Analysis Engine is qualified.

---

# LAYER A — ANALYSIS ENGINE

## 1. Freeze and classify the corpus

Inventory every target question/source before authoring.

Preserve:

- stable question ID;
- mathematical/scientific stem;
- source status;
- source/provenance ledger entry;
- source-required figures;
- corrections/uncertainty;
- duplicate relationships;
- stem hash/custody reference where repository workflow uses hashes.

Do not silently upgrade a weak/practice source to official authority.

### Source roles

**Authority source** — official/validated contest papers, repository source maps, correction overlays.

**Comparison/practice source** — notes, coaching material, videos, DPPs, external problem lists.

**Internal quality benchmark** — a comparator for pedagogy/layout/QA, never a template to copy.

---

## 2. Decompose every target question

Minimum decomposition:

```text
question
→ topic
→ subtopic
→ concept
→ stable method / skill
→ recognition cue
→ representation
→ first executable move
→ execution path
→ legality / check
→ prerequisites
→ difficulty
→ provenance
→ visual requirement
```

The question matrix must record enough information to answer:

> What must the learner notice, represent, write first, execute, and check?

Recommended fields include:

- question ID;
- surface/topic/subtopic/concept;
- candidate stable skill;
- recognition cue;
- representation;
- first move;
- execution bridge requirement;
- legality/boundary check;
- prerequisite skill IDs;
- authored difficulty `D1-D5`;
- learner-relative risk when a profile exists;
- educational priority as a separate field;
- source ledger ID/status;
- visual level/job/asset ID;
- planned teaching/bridge location.

---

## 3. Opening Signature and concept splitting

Define each stable skill by an **Opening Signature**:

```text
Opening Signature =
(recognition, representation, first executable move, legality/check)
```

Split a broad concept when question families differ materially in any of those components.

```text
SPLIT if recognition cue differs materially
OR representation differs materially
OR first executable move differs materially
OR legality/check logic differs materially.
```

Do not assume one textbook heading equals one teachable skill.

Examples of broad labels that may need splitting:

```text
Factorisation
Digit sum
Recurrence
Counting
Root problems
Forces
Stoichiometry
```

The test is operational:

> Can a Grade 9 learner be taught one recognizable situation, one useful representation, one first-move family, and the relevant legality check in this unit?

If not, split it.

---

## 4. Build the Concept / Method Graph

For large or heterogeneous builds, create a persistent graph artifact.

```text
DOMAIN
└── TOPIC
    └── SUBTOPIC
        └── CONCEPT
            └── STABLE SKILL / METHOD FAMILY
                ├── recognition signature
                ├── representation
                ├── first move
                ├── legality
                ├── prerequisites
                ├── difficulty range
                ├── question IDs
                ├── bridge IDs
                └── visual IDs
```

Preferred artifact:

```text
Concept_Method_Graph.csv
```

or YAML equivalent.

Normally require it when:

- target corpus is roughly 30+ questions; or
- there are roughly 12+ candidate skills; or
- textbook/source headings conceal materially different openings.

These are operational defaults, not scientific thresholds.

For smaller guides, the main question matrix may carry the same information if it remains auditable.

---

## 5. Build the prerequisite DAG

Teaching order is derived from dependencies, not source order.

For every stable skill:

- list prerequisite skill IDs;
- eliminate unjustified cycles;
- explicitly justify co-taught clusters if a cycle is unavoidable;
- place school-level refreshers immediately before the competitive-exam upgrade they enable.

Then derive chapter/section sequence from the DAG plus learner usability.

---

## 6. Orphan-method audit

A method is orphaned if the guide merely names the trick and assumes the learner already knows how to perform it.

Every question needs a route:

```text
recognize
→ choose representation
→ write first useful move
→ execute
→ check
```

Examples of failures:

- “use Vieta” without reconstructing the requested expression;
- “apply CRT” without compatibility/substitution/merge logic;
- “use conservation of energy” without defining system and terms;
- “use limiting reagent” without teaching the mole-ratio setup.

Hard gate:

```text
ORPHAN_METHODS = 0
```

---

## 7. Transfer-gap audit and Worked Bridges

Worked Bridges exist to close unsupported transfer edges, not to add generic enrichment.

```text
taught skill
    ↓
normal worked example
    ↓
TRANSFER GAP
    ↓
target question
```

Classify important edges:

```text
TRANSFER_GAP = NONE
TRANSFER_GAP = MODERATE
TRANSFER_GAP = HARD
```

Rules:

- `NONE` → ordinary practice is enough;
- `MODERATE` → use contrast/reduced support; repeated moderate gaps may justify a bridge;
- `HARD` → non-identical Worked Bridge required;
- bridge content must expose recognition, representation, first move, execution, and check;
- create bridges because the matrix/graph shows a gap, not because an “advanced” section looks desirable.

Gates:

```text
TRANSFER_GAP_AUDIT = PASS_n_OF_n
HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
```

---

## 8. Difficulty, priority, learner mastery, and provenance

Keep distinct:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

Use the difficulty addendum for full calibration.

Student-facing question badge:

```text
[D3 STRATEGIC]
```

Broad topics use a range/band, not one misleading number.

Source mini-badge example:

```text
[SRC 12]
```

The full source ledger remains authoritative.

---

## 9. Visual obligations

Use visuals only when they materially expose structure or reduce cognitive load.

If a visual is triggered, apply the visual-production addendum.

A required visual must be traceable:

```text
question/skill
→ visual obligation
→ asset brief
→ asset
→ placement
→ rendered page
→ final-size QA
```

Do not count decorative imagery as pedagogy.

---

## 10. Qualify the Analysis Engine

For large builds, the package should contain or explicitly derive:

```text
Frozen_Corpus_Registry
Source_Provenance_Ledger
Question_Decomposition_Matrix
Concept_Method_Graph
Stable_Skill_Registry
Prerequisite_DAG
Orphan_Method_Audit
Difficulty_Map
Visual_Obligation_Register
Transfer_Gap_Map
Worked_Bridge_Obligations
```

Minimum gates:

```text
CORPUS_FROZEN = PASS_n_OF_n
QUESTION_DECOMPOSITION = PASS_n_OF_n
QUESTION_TO_CONCEPT_BINDING = PASS_n_OF_n
CONCEPT_SPLIT_AUDIT = PASS
STABLE_SKILL_OPENING_SIGNATURE = PASS_n_OF_n
PREREQUISITE_GRAPH = PASS
PREREQUISITE_CYCLES_UNJUSTIFIED = 0
ORPHAN_METHODS = 0
TRANSFER_GAP_AUDIT = PASS_n_OF_n
HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
VISUAL_OBLIGATIONS_ANALYZED = PASS_n_OF_n
DIFFICULTY_ANALYZED = PASS_n_OF_n
```

Only then:

```text
ANALYSIS_ENGINE_QUALIFIED = PASS
STUDENT_BOOK_GENERATION_ALLOWED = TRUE
```

---

# LAYER B — STUDENT BOOK GENERATOR

## 11. Student-facing complexity boundary

The analysis model is not the student page design.

The learner normally sees:

- readable topic/concept names;
- compact difficulty/source badges;
- clear explanations;
- a very visible FIRST MOVE;
- worked examples;
- practice pointers;
- Notice / Recall / Start hints where appropriate.

The learner normally does **not** see:

- concept-graph IDs;
- Opening-Signature tuples;
- transfer-gap classifications;
- prerequisite-edge IDs;
- K/R/M/E/I/B/T vectors;
- internal pass/fail statuses;
- raw routing equations;
- build-dossier terminology.

Hard principle:

```text
COMPLEXITY_BELONGS_IN_THE_ENGINE = PASS
ANALYSIS_JARGON_LEAKAGE = 0
```

---

## 12. Student semantic grammar

Default reference-page roles:

```text
REMEMBER
SEE THE IDEA
TRY IT
FIRST MOVE
WATCH OUT
PRACTISE
```

These are semantic roles, not mandatory identical layouts.

Map internal richness to a simpler surface:

| Internal authoring role | Student surface |
|---|---|
| prerequisite refresh | **REMEMBER** |
| missing competitive-exam link + mechanism | **SEE THE IDEA** |
| worked example + execution | **TRY IT** |
| executable opening | **FIRST MOVE** |
| close contrast + misconception + legality | **WATCH OUT** |
| stable skill/question pointers | **PRACTISE** |

Do not expose a long stack of machine-like headings such as separate “missing link”, “why this works”, “close contrast”, and “legality” strips when those can be combined into a clearer student section.

---

## 13. FIRST MOVE must be visually dominant

The first move is a retrieval object, not a footnote.

Examples:

```text
FIRST MOVE
Set p = xyz.
```

```text
FIRST MOVE
Draw the free-body diagram and choose the system.
```

```text
FIRST MOVE
Convert all given quantities to moles.
```

Required gates:

```text
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_READING_PARAGRAPH = PASS_n_OF_n
LOW_CONTRAST_CRITICAL_HEADINGS = 0
```

A student should be able to flip to the skill and find the first move immediately.

Difficulty/source badges remain secondary and must never dominate the mathematics.

---

## 14. Learner knowledge

If no learner-specific profile exists, use the partial-knowledge baseline from the detailed contract.

If the user supplies subject/topic/subtopic/skill knowledge, do not flatten it into one global percentage.

Use the learner-profile addendum precedence:

```text
diagnostic evidence
> stable skill / method
> subtopic
> topic
> subject
> default partial baseline
```

Personalization changes:

- Navigator routing;
- Quick Check selection;
- practice priority;
- Challenge Ladder entry;
- starting hint/support level.

It does not silently delete the durable core unless the user explicitly asks for a pruned personal edition.

---

## 15. Appendix roles

Keep roles distinct.

### Appendix A — supplied corpus

- preserve every target question exactly subject to documented source corrections;
- use Notice / Recall / Start support when allowed;
- answer key after the final question;
- source-required figures preserved;
- difficulty/source badges compact and non-spoiling.

If the user requests strict questions-only, remove local hints/commentary and preserve only problem-essential figures.

### Appendix B — independent mixed transfer / exam audit

- mixed/unlabelled where transfer is being tested;
- answers only after the final item;
- independently recompute answers;
- no redundant second “hard mixed problem” appendix.

### Appendix C — decision-first rapid recall

Usually 1–3 pages:

```text
What do I see?
→ What should I draw/write first?
→ What must I check?
```

Use compact formulas/tools only after method choice.

### Challenge Ladders — train progression

Challenge Ladders answer:

> What should I try next for this concept?

They should mostly reuse Worked Bridges, Appendix A, Appendix B, and verified practice by difficulty rung.

```text
APPENDIX_B = TEST_TRANSFER
CHALLENGE_LADDER = TRAIN_PROGRESSION
```

---

## 16. Optional short-horizon Navigator

When the learner has only a few days, keep Part 0 simple.

Default student interface:

1. Start Here;
2. Quick Check `T1 ... Tx`;
3. What should I study?;
4. When stuck.

Rules:

- initial Quick Check is unaided;
- use `T` labels, never collide with corpus `Q` labels;
- `x` is derived from learner knowledge, scope, important weak/unknown/partial families, time/page fit, and explicit requested count;
- route with plain `DO FIRST / DO NEXT / QUICK RETEST / ONLY IF TIME` language;
- Notice / Recall / Start support appears only after the initial diagnostic attempt;
- internal metrics/priority equations stay hidden;
- difficulty badge is supporting metadata, not a “hardest first” router;
- no major new core skill on Day 3;
- protect normal sleep.

Architecture:

```text
Navigator = where to go.
Core = how to do it.
```

---

## 17. Domain portability

The orchestration stays generic.

### Mathematics

```text
recognize structure
→ choose representation
→ first mathematical line/construction
→ execute
→ check domain/equality/cases
```

### Physics

```text
recognize physical situation
→ choose system + representation
→ first diagram/law/equation
→ model + calculate
→ units/sign/assumption check
```

### Chemistry

```text
recognize process
→ choose chemical representation
→ first balancing/mole/structure step
→ calculate/reason
→ conservation/units/conditions check
```

Domain profiles own concrete Opening Signatures, legality rules, visuals, and difficulty anchors.

---

# INTEGRATED QA

## 18. Question-level self-sufficiency

A target question passes only when the durable guide supplies:

1. prerequisite refresh;
2. recognition cue;
3. usable representation where needed;
4. first useful move;
5. execution bridge;
6. legality/common-error check;
7. required visual support;
8. difficulty metadata;
9. provenance metadata;
10. non-spoiling practice presentation.

Record only when all target rows pass:

```text
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n
```

This is a document-coverage claim, not evidence of learner solve rate or psychometric calibration.

---

## 19. Student-surface QA

Required:

```text
STUDENT_SURFACE_SEMANTIC_GRAMMAR = PASS
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_READING_PARAGRAPH = PASS_n_OF_n
ANALYSIS_JARGON_LEAKAGE = 0
LOW_CONTRAST_CRITICAL_HEADINGS = 0
BADGES_DOMINATING_MATHEMATICS = 0
```

Headings such as FIRST MOVE and WATCH OUT must remain legible at final reading size and in grayscale.

---

## 20. Final PDF / visual QA

Apply the detailed and visual-production contracts.

Minimum final workflow:

```text
content gates pass
→ build PDF
→ preflight
→ render every page at 200 dpi
→ inspect every page
→ repair
→ rerender changed pages / full final as needed
→ record page count + SHA-256
```

A required visual that is missing, mathematically wrong, clipped, unreadable, or too solution-revealing blocks final visual completion.

Do not call representative-page inspection a full final QA pass.

---

# Required reusable artifacts

For a substantial build, create or maintain as appropriate:

```text
README.md
Frozen_Corpus_Registry.md/.csv
Source_Provenance_Ledger.md
Question_Decomposition_Matrix.md/.csv
Concept_Method_Graph.csv/.yaml
Stable_Skill_Registry.md
Prerequisite_DAG.md/.csv
Transfer_Gap_Map.md/.csv
Worked_Bridge_Obligations.md
Difficulty_Map.md/.csv
Visual_Obligation_Register.md/.csv
<Subject>_Study_Guide_vN.md
Appendix_A_*.md
Appendix_B_*.md
Appendix_C_*.md
Challenge_Ladders.md or integrated route table
Self_Sufficiency_Audit.md
QA.md
```

For small builds, artifacts may be consolidated if all required fields remain traceable.

---

# Final rule

A scalable study guide is not created by mapping many questions directly into many chapters.

It is created by:

```text
many questions
→ decompose
→ discover Opening Signatures
→ split concepts correctly
→ build prerequisite graph
→ find unsupported transfer edges
→ create only required bridges
→ qualify the analysis
→ render a simple student book
→ audit every target question
→ inspect the final PDF
```

The richer the engine becomes, the simpler and more readable the learner surface must become.