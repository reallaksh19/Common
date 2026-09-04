# Analysis Engine, Opening Signatures, Transfer Gaps, and Student Surface

This addendum is the **domain-neutral organizing contract** for large or heterogeneous competitive-exam study-guide builds.

Its governing principle is:

```text
rich analysis underneath
        ->
simple learner interface above
```

It defines how a large corpus becomes the correct set of teachable skills, how those skills are qualified before book production, and how the resulting learner pages stay readable rather than exposing the internal analysis machinery.

It takes precedence over older linear-pipeline wording for corpus decomposition, skill granularity, prerequisite graphing, transfer-gap/bridge creation, student-facing page grammar, navigation, packaging mode, and FIRST MOVE prominence. It does not weaken source custody, learner-profile, difficulty, visual-production, appendix, self-sufficiency, or PDF-QA contracts.

---

## 1. Two-layer architecture

Production has two literal layers separated by a hard gate.

```text
LAYER A - ANALYSIS ENGINE

Freeze corpus
-> decompose every question
-> build Topic / Subtopic / Concept / Method graph
-> run Opening-Signature split audit
-> assign stable skills
-> build prerequisite DAG
-> run orphan-method audit
-> assign difficulty / source / visual metadata
-> audit transfer gaps
-> create only required Worked Bridges
-> QUALIFY ANALYSIS PACKAGE

================ HARD GATE ================

LAYER B - STUDENT BOOK GENERATOR

derive learner / chapter order
-> prototype student surface
-> render teaching pages
-> build practice navigation
-> build Appendices / Challenge Ladders
-> integrated question-level audit
-> PDF generation
-> preflight + 200-dpi render + page inspection
```

Do not begin final student-book production from attractive chapter headings alone.

```text
STUDENT_BOOK_GENERATION_ALLOWED = FALSE
```

until the Analysis Engine is qualified.

---

## 2. Corpus Decomposition Contract

Before chapter writing, decompose **every target question**.

Minimum path:

```text
question
-> topic
-> subtopic
-> concept
-> stable method / skill
-> recognition cue
-> representation
-> first executable move
-> execution path
-> legality / check
-> prerequisites
-> authored difficulty
-> provenance
-> visual requirement
```

Recommended fields:

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

## 3. Opening Signature and concept splitting

A stable skill is defined by its **Opening Signature**, not merely by a broad textbook label.

```text
Opening Signature =
(
  recognition,
  representation,
  first executable move,
  legality / check logic
)
```

Split a candidate concept when any of those components differs materially.

```text
SPLIT if recognition cue differs materially
OR representation differs materially
OR first executable move differs materially
OR legality/check logic differs materially
```

Examples:

```text
Factorisation
-> powers / difference-sum structures
-> manufactured fixed-product forms
-> polynomial-to-consecutive-factor reductions

Digit sum
-> congruence / bounded digit-sum reasoning
-> exact carry accounting

Recurrence
-> modular/state recurrence
-> overlapping-window cancellation

Counting
-> fixed-multiplicity choices
-> pigeonhole / residue obstruction
-> extremal square-gap reasoning
-> graph modelling
```

Qualification question:

> Can a Grade 9 learner be taught one recognizable situation, one useful representation, one coherent first-move family, and the relevant legality check in this unit?

If not, split it.

A skill does not need one literally identical first line in every problem. It needs one coherent opening family that can be recognized and started reliably.

---

## 4. Concept / Method Graph

For large or heterogeneous corpora, persist the decomposition as a build artifact.

```text
DOMAIN
└-- TOPIC
    └-- SUBTOPIC
        └-- CONCEPT
            └-- STABLE SKILL / METHOD FAMILY
                |-- recognition signature
                |-- representation
                |-- first move
                |-- legality
                |-- prerequisites
                |-- difficulty range
                |-- question IDs
                |-- bridge IDs
                `-- visual asset IDs
```

Recommended artifact: `Concept_Method_Graph.csv` or YAML equivalent.

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

The graph is normally required for clearly large/heterogeneous builds - operational default about 30+ target questions, 12+ candidate skills, or whenever broad headings hide materially different openings. These are authoring defaults, not scientific thresholds.

For smaller guides, equivalent information may remain inside the main matrix if it is auditable.

---

## 5. Prerequisite DAG

Build the prerequisite graph **after** the split audit and **before** deciding chapter order.

Requirements:

- every stable skill lists prerequisite skill IDs;
- cycles are eliminated or explicitly justified as co-taught clusters;
- school-level refreshers sit close to the competitive-exam upgrade they enable;
- later chapters do not silently require untaught methods.

Teaching order is derived from the DAG plus learner usability, not source sequence.

---

## 6. Orphan-method audit

Every target question needs a complete support route:

```text
recognize
-> choose representation
-> write first useful move
-> execute
-> check legality / boundary
```

A question fails when the guide merely names a trick.

Examples of failure:

- "use Vieta" without teaching reconstruction of the requested expression;
- "apply CRT" without compatibility/substitution/merge logic;
- "use conservation of energy" without defining the system/terms in a Physics profile;
- "use limiting reagent" without a mole-ratio setup in a Chemistry profile.

Required gate:

```text
ORPHAN_METHODS = 0
```

---

## 7. Transfer-gap / Worked-Bridge contract

Worked Bridges are not generic enrichment. A bridge exists because the graph contains an unsupported transfer edge.

```text
taught skill
   -> normal example
   -> unsupported transfer jump
   -> target question
```

Classify important edges:

```text
TRANSFER_GAP = NONE
TRANSFER_GAP = MODERATE
TRANSFER_GAP = HARD
```

Rules:

- `NONE`: ordinary practice is enough;
- `MODERATE`: reduced support, contrast, or a short bridge when repeated;
- `HARD`: a non-identical Worked Bridge is required;
- bridges close documented gaps rather than inflate page count;
- a bridge exposes recognition, representation, first move, execution, and check;
- bridge difficulty may sit below the target if it isolates the missing transfer step.

Gates:

```text
TRANSFER_GAP_AUDIT = PASS_n_OF_n
HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
```

---

## 8. Difficulty remains separate

Keep independent:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

Questions receive authored `D1...D5` badges. Topics/concepts normally use a band or core-to-transfer range.

Example:

```text
CRT                 [D3 core | D5 transfer]
```

Learner knowledge changes routing and ladder entry, not the authored task difficulty.

---

## 9. Analysis package qualification

Before student-book generation, the engine should contain or explicitly derive:

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

For large builds, persist these as repository artifacts rather than session-only notes.

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

# LAYER B - STUDENT BOOK GENERATOR

## 10. Student-surface semantic roles

The learner book consumes the rich analysis but does **not** print the analysis model as page furniture.

Available semantic roles:

```text
REMEMBER
SEE THE IDEA
TRY IT
FIRST MOVE
WATCH OUT
PRACTISE
```

These are **roles, not a mandatory six-box template**.

Mapping:

| Internal authoring role | Student surface |
|---|---|
| prerequisite refresh | REMEMBER |
| missing competitive-exam link + mechanism | SEE THE IDEA |
| worked example / execution | TRY IT |
| executable opening | FIRST MOVE |
| contrast + misconception + legality | WATCH OUT |
| practice pointers | PRACTISE |

Do not force every role onto every skill page. Use only what earns space.

In particular:

- `FIRST MOVE` is normally the strongest recurring callout;
- `REMEMBER` may disappear when the prerequisite is obvious;
- `SEE THE IDEA` and `TRY IT` may merge when a tiny worked example teaches the mechanism directly;
- close contrast, common mistake, legality, boundary and admissibility normally collapse into one `WATCH OUT` block;
- `PRACTISE` is a quiet pointer, not another large card;
- repeated equal-weight colored strips fail the student-surface goal even when every strip is technically correct.

Avoid exposing a machine-like sequence such as:

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

The content model may retain those fields internally; the page should not.

---

## 11. FIRST MOVE is the main retrieval object

A learner flipping to a concept should be able to find the opening immediately.

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

Gates:

```text
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_READING_PARAGRAPH = PASS_n_OF_n
```

FIRST MOVE must have strong contrast, adequate size, whitespace, and mathematical content. It must not look like a footnote or thin footer strip.

---

## 12. Readable name first; stable ID second

Stable IDs are essential to the engine and repository. They are not the learner's primary navigation language.

Default learner-facing order:

```text
Readable Skill Name                 [D2 core | D4 transfer]
small secondary text: NT-ORDER-01
```

Rules:

- concept pages lead with readable names;
- Contents, study routes, Quick Checks, Practice Maps, and Challenge Ladders lead with readable names;
- stable IDs may appear in small secondary type, cross-reference notes, or the teacher/build dossier;
- a page or table that requires the learner to decode many raw IDs before understanding where to go fails.

Gate:

```text
RAW_STABLE_IDS_AS_PRIMARY_NAVIGATION = 0
```

---

## 13. Student navigation tables are UI, not audit tables

Do not dump a question matrix, graph export, or reviewer manifest into the learner book and call it navigation.

Student-facing route tables should:

- group skills into readable families;
- lead with readable concept names;
- use question IDs only as destinations;
- use adequate font size and row spacing;
- prefer ragged-right text over compressed columns;
- avoid excessive hyphenation and code-heavy cells;
- fit final reading size without zoom-dependent interpretation.

The reviewer may have a 20-column matrix. The student should not.

Gate:

```text
NAV_TABLE_FINAL_SIZE_LEGIBILITY = PASS
```

---

## 14. Practice Map has a distinct job

For a large frozen corpus, a **Practice Map** is a learner index from readable skills to practice question IDs.

```text
Readable Skill / Family -> Q IDs
```

It is not:

- the Question Decomposition Matrix;
- Appendix B;
- a Challenge Ladder;
- a substitute for the actual corpus.

Use it when the reference book and question book are separate, or when a large embedded Appendix A needs a compact index.

A Practice Map answers:

> I just learned this skill. Which source questions should I attempt?

---

## 15. Challenge Ladders use readable progression

A Challenge Ladder answers:

> What should I try next for this concept?

It should normally reuse Worked Bridges, Appendix A/source questions, Appendix B/transfer questions, and verified practice rather than create a duplicate hard-problem bank.

Student-facing ladder example:

```text
Repeated roots
D2  worked bridge
 -> D3 guided source problem
 -> D4 mixed transfer problem
 -> D5 optional challenge
```

Readable names lead. Raw IDs are secondary or omitted unless needed for lookup.

Keep roles distinct:

```text
PRACTICE_MAP = WHERE_TO_PRACTISE_THIS_SKILL
CHALLENGE_LADDER = WHAT_TO_TRY_NEXT_FOR_THIS_SKILL
APPENDIX_B = INDEPENDENT_MIXED_TRANSFER_AUDIT
```

---

## 16. Packaging mode must be explicit

A study-guide package may be produced in one of two modes.

### A. SELF_CONTAINED_EDITION

The final deliverable itself contains every target question required for self-sufficient use, including the frozen Appendix A corpus when that is part of scope.

```text
PACKAGING_MODE = SELF_CONTAINED_EDITION
APPENDIX_A_CORPUS_EMBEDDED = PASS_n_OF_n
```

A Practice Map never substitutes for the embedded corpus when the user requests one self-contained PDF.

### B. REFERENCE_PLUS_PRACTICE_BOOK

The reference/teaching PDF may omit repeated large question stems **only** when the frozen practice book/corpus is an explicit companion in the same package and every practice pointer resolves to it.

```text
PACKAGING_MODE = REFERENCE_PLUS_PRACTICE_BOOK
COMPANION_PRACTICE_BOOK_PRESENT = PASS
PRACTICE_POINTERS_RESOLVE = PASS_n_OF_n
```

The student-facing book must say clearly that it is a reference edition and that the companion question book should be kept beside it.

Do not claim one-PDF self-sufficiency for this mode.

This distinction emerged clearly in the Number Theory pilot: condensing a 90-question corpus into a compact skill reference is useful, but the reference is not the same artifact as the frozen practice corpus.

---

## 17. Student-surface prototype gate

Before rendering an entire long book, build a representative mini-prototype in the actual final template.

It must include at least:

1. one ordinary core/skill page;
2. one navigation/route or Practice Map page;
3. one practice/problem page with badges/source treatment.

Render those pages at final size and inspect:

- FIRST MOVE prominence;
- heading contrast;
- readable-name-first navigation;
- stable-ID leakage;
- badge balance;
- table density;
- problem-page whitespace;
- font size/hyphenation;
- whether repeated card/strip styling feels mechanical.

Gates:

```text
STUDENT_SURFACE_PROTOTYPE = PASS
CORE_PAGE_PROTOTYPE_FINAL_SIZE = PASS
NAVIGATION_PAGE_PROTOTYPE_FINAL_SIZE = PASS
PRACTICE_PAGE_PROTOTYPE_FINAL_SIZE = PASS
RAW_STABLE_IDS_AS_PRIMARY_NAVIGATION = 0
NAV_TABLE_FINAL_SIZE_LEGIBILITY = PASS
LOW_CONTRAST_CRITICAL_HEADINGS = 0
```

Do not wait until a 50-100 page book exists to discover that the learner interface is too dense or machine-like.

---

## 18. Heading and visual hierarchy

Recommended relative hierarchy:

```text
Chapter / major topic          strongest
Readable concept / skill       strong
FIRST MOVE                     strongest callout inside skill block
SEE THE IDEA / TRY IT          clear supporting roles
WATCH OUT                      clear but secondary
PRACTISE                       quiet destination pointer
Difficulty/source badges       compact metadata
Stable ID                      secondary metadata
```

Student-surface QA fails when:

- a critical heading is barely visible;
- FIRST MOVE is styled like a footnote;
- badges dominate the mathematics;
- many colored strips compete equally;
- raw IDs dominate readable names;
- navigation tables require zooming or decoding;
- dense analysis prose survives into the learner book merely because it exists in the matrix.

---

## 19. Student-facing complexity boundary

The learner should normally see:

- readable topic/concept names;
- compact difficulty/source badges where useful;
- a concise explanation of the idea;
- a highly visible FIRST MOVE;
- a worked example when it adds value;
- one WATCH OUT when a nearby mistake is important;
- practice destinations;
- Notice / Recall / Start hints only where appropriate.

The learner should normally **not** see:

- concept-graph IDs as primary navigation;
- transfer-gap labels;
- prerequisite-edge IDs;
- opening-signature tuples;
- K/R/M/E/I/B/T difficulty vectors;
- internal audit statuses;
- raw routing formulas;
- build-dossier terminology.

```text
COMPLEXITY_BELONGS_IN_THE_ENGINE = PASS
ANALYSIS_JARGON_LEAKAGE = 0
```

---

## 20. Appendix / practice role boundary

Retain distinct jobs:

```text
Appendix A = supplied/frozen corpus with allowed support
Appendix B = independent mixed transfer / exam audit
Appendix C = decision-first rapid recall
Practice Map = readable skill -> corpus destinations
Challenge Ladders = concept-specific progression through existing resources
```

Do not create another large mixed hard-problem appendix merely because transfer practice is valuable.

In a clean exam simulation, Appendix B should normally hide topic/method labels and pre-attempt rescue hints. Difficulty/source badges may remain if the edition is not intended as a facsimile; otherwise hide them for simulation integrity.

---

## 21. Domain portability

The architecture must survive outside Mathematics.

### Mathematics

```text
recognize structure
-> choose representation
-> first mathematical line / construction
-> execute
-> check domain/equality/cases
```

### Physics

```text
recognize physical situation
-> choose system + representation
-> first law/equation/diagram
-> model + calculate
-> units/sign/assumption check
```

### Chemistry

```text
recognize process
-> choose chemical representation
-> first balancing/mole/structure step
-> calculate/reason
-> conservation/units/conditions check
```

Domain profiles define concrete Opening Signatures, legality rules, visuals, and difficulty anchors. The orchestrator remains generic.

---

## 22. Independent cross-check

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
PACKAGING_MODE = DECLARED
STUDENT_SURFACE_SEMANTIC_GRAMMAR = PASS
STUDENT_SURFACE_PROTOTYPE = PASS
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_READING_PARAGRAPH = PASS_n_OF_n
RAW_STABLE_IDS_AS_PRIMARY_NAVIGATION = 0
NAV_TABLE_FINAL_SIZE_LEGIBILITY = PASS
ANALYSIS_JARGON_LEAKAGE = 0
LOW_CONTRAST_CRITICAL_HEADINGS = 0
BADGES_DOMINATING_CONTENT = 0
PRACTICE_ROLE_COLLISIONS = 0
```

Then apply the existing question-level self-sufficiency, hint, visual-production, provenance, PDF preflight, 200-dpi render, and page-inspection gates.

---

## Number Theory pilot lesson

A verified large-corpus pilot successfully demonstrated the architectural distinction between the engine and the learner surface:

```text
90 target questions
-> opening-signature decomposition
-> 36 learnable skills
-> readable skill reference
-> Practice Map back to the frozen corpus
-> independent mixed challenge set
```

The methodological lesson is not the literal numbers `90` or `36`. It is that the engine may need dozens of stable IDs, source routes, bridge obligations, and audit fields while the student can still receive a compact book organized around readable concept names and first moves.

This is repository-scale production evidence, not measured learner efficacy or psychometric validation.

---

## Final rule

A scalable study-guide methodology is not:

```text
many questions -> many chapters
```

It is:

```text
many questions
-> decompose
-> discover Opening Signatures
-> split concepts correctly
-> build dependency graph
-> find unsupported transfer edges
-> create only required bridges
-> qualify the analysis
-> prototype the learner surface
-> declare packaging mode
-> render a simple student book
```

The richer the engine becomes, the more disciplined the learner-facing simplification must become.