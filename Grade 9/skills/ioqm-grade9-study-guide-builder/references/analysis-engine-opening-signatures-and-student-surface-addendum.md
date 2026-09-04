# Analysis Engine, Opening Signatures, Transfer Gaps, and Student Surface

This addendum is a **domain-neutral organizing contract** for large or heterogeneous competitive-exam study-guide builds.

It exists because a question-to-method matrix alone does not answer the hardest authoring question:

> How do many heterogeneous questions become the correct set of teachable skills, in the correct order, without exposing the analysis machinery to the learner?

This addendum takes precedence over older linear-pipeline wording for:

- corpus decomposition;
- concept/skill granularity;
- prerequisite graphing;
- transfer-gap and bridge creation;
- student-facing semantic page grammar;
- FIRST MOVE prominence.

It does **not** weaken source custody, difficulty, learner-profile, visual-production, appendix, self-sufficiency, or PDF-QA contracts.

---

## 1. Two-layer architecture

Treat production as two literal layers separated by a hard gate.

```text
LAYER A — ANALYSIS ENGINE

Frozen corpus
    ↓
Question decomposition
    ↓
Topic / subtopic / concept / method graph
    ↓
Concept-splitting audit
    ↓
Stable skills
    ↓
Prerequisite DAG
    ↓
Orphan-method audit
    ↓
Difficulty + visual obligations
    ↓
Transfer-gap audit
    ↓
Required bridges
    ↓
QUALIFIED ANALYSIS PACKAGE

================ HARD GATE ================

LAYER B — STUDENT BOOK GENERATOR

Qualified skills + graph
    ↓
Learner order / chapter order
    ↓
Student-facing teaching pages
    ↓
Appendix A / B / C + Challenge Ladders
    ↓
Integrated audit
    ↓
PDF / rendered QA
```

The analysis may be complex. The learner interface must remain simple.

```text
complex analysis underneath
        ↓
simple learner interface above
```

`STUDENT_BOOK_GENERATION_ALLOWED = FALSE` until the Analysis Engine is qualified.

This avoids the common failure mode of writing attractive chapters first and later discovering that one chapter heading concealed several different methods.

---

## 2. Corpus Decomposition Contract

Before chapter writing, decompose **every target question**.

Minimum path:

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

Recommended question-decomposition fields:

```text
question_id
source_status
source_ledger_id
stem_hash_or_custody_reference
surface_topic
subtopic
concept_id
candidate_skill_id
recognition_cue
representation
first_move
execution_steps_or_bridge_need
legality_signature
prerequisite_skill_ids
authored_difficulty
priority
visual_level
visual_job
learner_risk_if_profile_exists
notes
```

Never infer teaching granularity from source order or textbook headings alone.

---

## 3. Opening Signature

A stable skill is defined by its **Opening Signature**, not merely by a textbook label.

```text
Opening Signature =
(
  recognition,
  representation,
  first executable move,
  legality / check logic
)
```

A concept should be split when two question families have materially different Opening Signatures.

### Hard split test

```text
SPLIT if recognition cue differs materially
OR representation differs materially
OR first executable move differs materially
OR legality/check logic differs materially.
```

Examples of why broad labels can fail:

```text
Factorisation
→ powers / difference-sum structures
→ manufactured fixed-product forms
→ polynomial-to-consecutive-factor reductions

Digit sum
→ congruence / bounded digit-sum structure
→ exact carry accounting

Recurrence
→ recurrence-state / modular reduction
→ overlapping-window subtraction

Counting
→ direct multiplicity choices
→ pigeonhole / residue obstruction
→ square-gap extremal reasoning
→ graph modelling
```

A skill does not need one literal identical first line in every problem. It must have one coherent **opening family** that a learner can recognize and start reliably.

### Stable-skill qualification question

Ask:

> Can a Grade 9 learner be taught one recognizable situation, one useful representation, one first move family, and the relevant legality check in this unit?

If not, split it.

---

## 4. Concept / Method Graph

For large or heterogeneous corpora, create a build artifact that makes the decomposition explicit.

Recommended hierarchy:

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
                └── visual asset IDs
```

Recommended file:

```text
Concept_Method_Graph.csv
```

or a YAML equivalent.

Recommended fields:

```text
topic_id
subtopic_id
concept_id
skill_id
parent_skill_ids
recognition_signature
representation
first_move
legality_signature
difficulty_core
difficulty_transfer_range
question_ids
bridge_ids
visual_asset_ids
```

The graph becomes mandatory when the build is clearly large/heterogeneous — normally 30+ target questions, 12+ candidate skills, or whenever broad headings hide materially different openings.

For smaller guides, the same information may live inside the main question matrix if it remains auditable.

---

## 5. Prerequisite DAG

After the split audit, build a prerequisite graph before deciding chapter order.

Teaching order must follow dependencies, not source sequence.

Requirements:

- each stable skill lists prerequisite skill IDs;
- cycles must be either eliminated or explicitly justified as co-taught clusters;
- school-level refreshers should sit immediately before the Olympiad upgrade they enable;
- later chapters may depend on earlier ones, but should not silently require an untaught method.

The chapter sequence should be **derived from the DAG** plus learner usability, not handwritten first and rationalized later.

---

## 6. Orphan-Method Audit

Every target question must map to a complete support route:

```text
recognize
→ choose representation
→ write first useful move
→ execute
→ check legality / boundary
```

A question fails if the guide merely names a trick.

Examples of failures:

- “use Vieta” without teaching reconstruction of the requested expression;
- “apply CRT” without compatibility/substitution/merge logic;
- “use conservation of energy” without defining the system and terms in a Physics profile;
- “use limiting reagent” without a mole-ratio setup in a Chemistry profile.

Required gate:

```text
ORPHAN_METHODS = 0
```

before the Analysis Engine may qualify.

---

## 7. Transfer-Gap / Bridge Contract

Worked Bridges are not generic enrichment.

A bridge exists because the graph contains an unsupported transfer edge.

```text
taught skill
    ↓
normal worked example
    ↓
UNSUPPORTED TRANSFER JUMP
    ↓
target question
```

Classify each important edge:

```text
TRANSFER_GAP = NONE
TRANSFER_GAP = MODERATE
TRANSFER_GAP = HARD
```

Rules:

- `NONE` → ordinary practice is enough;
- `MODERATE` → use reduced support, contrast, or a short bridge when repeated;
- `HARD` → a non-identical Worked Bridge is required;
- new bridges should close documented gaps, not inflate page count;
- a bridge must itself expose recognition, representation, first move, execution, and check;
- bridge difficulty may be below the target question if it isolates the missing transfer step.

Required gates:

```text
TRANSFER_GAP_AUDIT = PASS_n_OF_n
HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
```

---

## 8. Difficulty stays hierarchical and separate

Keep independent:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

Questions receive an authored `D1...D5` badge.

Concepts/subtopics/topics normally use a band or core-to-transfer range, for example:

```text
CRT
Core difficulty: D3
Transfer range: D3-D5
```

Learner knowledge changes routing and ladder entry, not the authored task difficulty.

---

## 9. Analysis package qualification

Before student-book generation, the Analysis Engine should contain or explicitly derive:

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

For large builds, these should be persistent repository artifacts rather than only notes in an authoring session.

Minimum hard gates:

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

## 10. Student-Surface Contract

The Student Book Generator consumes the rich analysis but does **not** print the analysis model as page furniture.

Default student semantic grammar:

```text
REMEMBER
SEE THE IDEA
TRY IT
FIRST MOVE
WATCH OUT
PRACTISE
```

These are semantic roles, not mandatory identical page layouts.

### Mapping

| Internal authoring role | Student surface |
|---|---|
| prerequisite refresh | **REMEMBER** |
| missing competitive-exam link + mechanism | **SEE THE IDEA** |
| worked example + execution | **TRY IT** |
| executable opening | **FIRST MOVE** |
| close contrast + misconception + legality | **WATCH OUT** |
| stable skill/question pointers | **PRACTISE** |

Do not expose separate machine-like headings for every internal field.

For example, do not make a page visually depend on a long sequence such as:

```text
What you probably remember
The missing Olympiad link
Why this works
Try this first
Close contrast
Common mistake
Legality
Practice targets
```

Those internal ideas may remain in the content model, but should collapse into the six student roles above.

---

## 11. FIRST MOVE is a high-priority retrieval object

`FIRST MOVE` is not ordinary explanatory text.

It is one of the most important retrieval objects in the guide.

Examples:

```text
FIRST MOVE
Set p = xyz.
```

```text
FIRST MOVE
Draw the free-body diagram and mark the chosen system.
```

```text
FIRST MOVE
Convert every given quantity to moles before comparing reactants.
```

Rendering requirements:

```text
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_READING_PARAGRAPH = PASS_n_OF_n
```

A student flipping to a skill should be able to find the first move immediately.

The heading must therefore have strong contrast, adequate size, and whitespace. It must not be a barely visible footer strip.

---

## 12. Heading and visual hierarchy

Recommended relative hierarchy for ordinary reference pages:

```text
Chapter / major topic         strongest
Concept / stable skill        strong
REMEMBER / SEE THE IDEA       clear section headings
TRY IT / WATCH OUT            clear section headings
FIRST MOVE                    strongest callout inside the skill page
PRACTISE                      quiet pointer
Difficulty/source badges      compact secondary metadata
```

Exact typography is implementation-specific, but the semantic hierarchy is mandatory.

The following fail student-surface QA:

- section labels readable only after close inspection;
- FIRST MOVE styled like a footnote;
- low-contrast heading-on-fill combinations;
- excessive colored strips competing equally for attention;
- badges visually stronger than the mathematics;
- internal codes/stable IDs more prominent than readable names.

---

## 13. Domain portability

This architecture must survive outside Mathematics.

### Mathematics

```text
recognize structure
→ choose representation
→ first mathematical line / construction
→ execute
→ check domain/equality/cases
```

### Physics

```text
recognize physical situation
→ choose system + representation
→ first law/equation/diagram
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

Domain profiles define concrete Opening Signatures, legality rules, visuals, and difficulty anchors.

The orchestrator remains generic.

---

## 14. Student-facing complexity boundary

The learner should normally see:

- readable topic/concept names;
- a compact difficulty badge;
- source badge where useful;
- strong teaching explanation;
- a clearly visible FIRST MOVE;
- worked examples;
- practice pointers;
- local Notice / Recall / Start hints only where appropriate.

The learner should normally **not** see:

- concept-graph IDs;
- transfer-gap labels;
- prerequisite-edge IDs;
- opening-signature tuples;
- K/R/M/E/I/B/T difficulty vectors;
- internal audit status;
- raw routing formulas;
- build-dossier language.

Principle:

```text
COMPLEXITY_BELONGS_IN_THE_ENGINE = PASS
ANALYSIS_JARGON_LEAKAGE = 0
```

---

## 15. Appendix / Challenge-Ladder role boundary

Retain the existing distinct jobs:

```text
Appendix A = supplied corpus with allowed support
Appendix B = independent mixed transfer / exam audit
Appendix C = decision-first rapid recall
Challenge Ladders = concept-specific progression through existing resources
```

Do not create another large mixed hard-problem appendix merely because transfer practice is valuable.

Challenge Ladders should use the Concept/Method Graph and difficulty metadata to answer:

> What should I try next for this concept?

---

## 16. Independent cross-check

Before final PDF generation, verify both layers.

### Analysis Engine

```text
QUESTION_DECOMPOSITION = PASS_n_OF_n
OPENING_SIGNATURES = PASS_n_OF_n
CONCEPT_SPLIT_AUDIT = PASS
PREREQUISITE_DAG = PASS
ORPHAN_METHODS = 0
HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
```

### Student Surface

```text
STUDENT_SURFACE_SEMANTIC_GRAMMAR = PASS
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_READING_PARAGRAPH = PASS_n_OF_n
ANALYSIS_JARGON_LEAKAGE = 0
LOW_CONTRAST_CRITICAL_HEADINGS = 0
BADGES_DOMINATING_MATHEMATICS = 0
```

Then apply the existing question-level self-sufficiency, hint, visual-production, provenance, PDF preflight, 200-dpi render, and page inspection gates.

---

## Final rule

A scalable study-guide methodology is not:

```text
many questions → many chapters
```

It is:

```text
many questions
→ decompose
→ discover opening signatures
→ split concepts correctly
→ build dependency graph
→ find unsupported transfer edges
→ create only required bridges
→ qualify the analysis
→ render a simple student book
```

The richer the analysis becomes, the more disciplined the learner-facing simplification must become.