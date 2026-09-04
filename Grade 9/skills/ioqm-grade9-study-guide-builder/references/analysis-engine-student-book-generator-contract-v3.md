# Question-Driven Study Guide Builder v3

## Analysis Engine + Student Book Generator Contract

**Status:** generalized production contract informed by the Algebra and Number Theory rebuilds.

This contract changes the organizing architecture of the study-guide builder. It does not discard the existing v2 custody, hint, visual, difficulty, provenance, or PDF-QA rules. It places them inside a stronger two-layer production system.

The core principle is:

```text
complex analysis underneath
        ->
simple learner interface above
```

A large problem corpus must not be converted directly into chapters. First determine the actual teachable skills required by the questions. Only then generate the student book.

---

## 1. Two-layer architecture

```text
LAYER A - ANALYSIS ENGINE

freeze corpus
-> decompose every question
-> build concept/method graph
-> split broad concepts by opening signature
-> assign stable skills
-> build prerequisite DAG
-> audit orphan methods
-> audit difficulty / priority / learner mastery separately
-> audit visual obligations
-> audit transfer gaps
-> create only the bridges that close real gaps
-> qualify analysis package

================ HARD GATE ================

LAYER B - STUDENT BOOK GENERATOR

derive teaching order from dependency graph
-> generate simple student pages
-> integrate required visuals
-> generate adaptive practice/hints
-> generate mixed transfer
-> generate decision-first quick reference
-> run integrated question-level audit
-> render PDF
-> inspect final-size pages
```

The Student Book Generator must not invent skill granularity independently of the Analysis Engine.

`STUDENT_BOOK_GENERATION_ALLOWED = FALSE` until the Analysis Engine passes its qualification gates.

---

## 2. Corpus Decomposition Contract

Freeze the supplied corpus before teaching design.

For every supplied question record at minimum:

- stable local question ID;
- exact or custody-preserved mathematical stem;
- provenance/source class;
- topic;
- subtopic;
- concept;
- candidate stable skill/method family;
- decisive recognition cue;
- representation or compression move;
- first executable move;
- execution requirements;
- legality/reversibility/admissibility requirements;
- prerequisites;
- likely half-knowledge misconception;
- authored difficulty;
- educational priority;
- learner mastery/risk when learner evidence exists;
- visual requirement;
- planned teaching location;
- hint depth when hints are allowed;
- transfer-gap status;
- support status.

The canonical chain is:

```text
QUESTION
-> TOPIC
-> SUBTOPIC
-> CONCEPT
-> STABLE SKILL / METHOD
-> RECOGNITION
-> REPRESENTATION
-> FIRST MOVE
-> EXECUTION
-> CHECK
```

Do not let source order determine teaching order.

---

## 3. Concept / Method Graph Contract

For a large domain, create a graph before drafting chapters:

```text
DOMAIN
`-- TOPIC
    `-- SUBTOPIC
        `-- CONCEPT
            `-- STABLE SKILL / METHOD
                |-- recognition cues
                |-- representation
                |-- first move
                |-- legality/check
                |-- question IDs
                |-- bridge IDs
                `-- difficulty range
```

Recommended machine-readable fields:

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
difficulty_range
question_ids
bridge_ids
visual_asset_ids
```

A separate graph artifact is normally required for large corpora. A small guide may keep the graph inside the question matrix if all relationships remain explicit and auditable.

---

## 4. Concept-Splitting Contract

Broad textbook labels are not automatically stable skills.

Define the **Opening Signature** of a question family as:

```text
(recognition cue, representation, first executable move, legality/check)
```

Split a concept whenever two question families require materially different opening signatures.

Hard split triggers:

```text
SPLIT if recognition cue differs materially
OR representation differs materially
OR first executable move differs materially
OR legality/check logic differs materially.
```

A candidate stable skill should pass this learner test:

> Can a Grade 9 learner recognize one coherent situation and produce a predictable legal opening from this skill?

If not, split it.

Do not use an umbrella label such as `factorisation`, `counting`, `recurrence`, `energy`, or `stoichiometry` as the final skill when the actual first moves differ substantially.

Umbrella concepts may remain for navigation, but question support must point to the executable stable skill.

---

## 5. Stable Skill Contract

Each stable skill requires:

- stable ID;
- readable learner name;
- prerequisite links;
- recognition signature;
- representation/compression move;
- first executable move;
- normal execution closure;
- legality/check signature;
- close contrast / anti-trigger;
- at least one non-identical worked example for non-routine methods;
- associated question IDs;
- associated bridges when needed;
- visual obligation when representation is inherently visual.

Stable IDs are internal retrieval anchors. They may appear in secondary type or in Recall hints, but the student should primarily see readable names.

---

## 6. Prerequisite DAG Contract

Teaching order comes from dependency, not question numbering.

Build a directed prerequisite graph and derive chapter/unit order from it.

Requirements:

- every stable skill declares its real prerequisite skills;
- cycles are rejected unless they are explicitly justified as a co-taught cluster;
- advanced methods may not appear before the minimum legal prerequisites;
- mixed method-selection comes after enough individual engines are secure;
- short-horizon routing may skip secure skills for one learner but must not corrupt the durable dependency order.

Recommended gate:

```text
PREREQUISITE_GRAPH = PASS
UNJUSTIFIED_PREREQUISITE_CYCLES = 0
```

---

## 7. Orphan-Method Contract

A question is orphaned if its support route still requires an unnamed trick.

Question-level support must contain:

```text
recognition
-> retrieval to taught stable skill
-> first executable move
-> enough execution to finish
-> legality/check
```

Not acceptable:

> Use CRT.

Acceptable support teaches a usable route such as:

```text
check compatibility
-> write one congruence as a substitution
-> solve the reduced congruence
-> state the merged modulus
-> verify original congruences
```

Required gate:

```text
ORPHAN_METHODS = 0
```

---

## 8. Transfer-Gap / Worked-Bridge Contract

Worked Bridges are not generic enrichment.

Create a bridge only when the graph contains a meaningful transfer jump:

```text
taught stable skill
        ↓
normal worked example
        ↓
TRANSFER GAP
        ↓
target question family
```

Classify the edge:

```text
TRANSFER_GAP = NONE
TRANSFER_GAP = MODERATE
TRANSFER_GAP = HARD
```

Rules:

- every HARD transfer gap requires a Worked Bridge;
- repeated MODERATE gaps may justify a bridge;
- do not add bridges merely to make the book look advanced;
- every bridge must be non-identical to the target problem;
- every bridge must expose enough intermediate reasoning to imitate;
- bridge legality and nearby wrong route must be explicit;
- bridge count is evidence-driven, not a fixed target.

Bridge quality checklist:

1. recognition cue;
2. why the representation fits;
3. first executable move;
4. intermediate execution;
5. normal closure;
6. legality/equality condition;
7. nearby wrong route;
8. transfer prompt.

---

## 9. Difficulty, Priority and Mastery Separation

Never collapse these dimensions:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

Question difficulty may use D1-D5 as defined in the difficulty addendum.

Broader structures should usually show ranges:

```text
concept: D2 core | D4 transfer
subtopic: D2 -> D5
```

Learner routing may combine authored difficulty with learner mastery and time pressure, but the visible labels remain separate.

---

## 10. Visual Obligation Contract

Visuals are decided in the Analysis Engine.

For every question/skill, explicitly choose:

```text
VISUAL_NONE
VISUAL_OPTIONAL
VISUAL_REQUIRED
VISUAL_SOURCE_REQUIRED
```

A required visual must have a teaching job such as:

- reveal a hidden representation;
- externalize working-memory load;
- distinguish nearby methods;
- show a state transition;
- make a geometric/algebraic structure visible;
- preserve a source-essential figure.

Decorative imagery is not coverage.

All required visuals remain subject to the existing visual-production addendum and final-size render QA.

---

## 11. Student-Surface Contract

The analysis may be complex. The student surface must be simple.

The default stable-skill page grammar is:

```text
REMEMBER
What you already know.

SEE THE IDEA
The Olympiad upgrade and why the representation works.

TRY IT
One non-identical worked example.

FIRST MOVE
The legal opening to write/draw now.

WATCH OUT
Close contrast, common mistake, legality/check.

PRACTISE
Quiet references to relevant questions/ladder rungs.
```

The exact layout may vary by domain, but the semantic roles must remain easy to scan.

### FIRST MOVE prominence

`FIRST MOVE` is a high-value retrieval object, not ordinary prose.

It must be visually findable without reading the entire paragraph.

Recommended gates:

```text
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_FINDABLE_WITHOUT_PARAGRAPH_SCAN = PASS_n_OF_n
```

### Internal vocabulary must not leak

Internal QA may use H0/H1/H2/H3, RMSEC, transfer-gap states, graph IDs and production gates.

The student should see plain language:

```text
Notice
Recall
Start
Check
```

Opaque production codes must not be the main learner-facing language.

`ANALYSIS_JARGON_LEAKAGE = 0`

---

## 12. Progressive Help Contract

When local hints are allowed:

```text
NOTICE - recognition only
RECALL - readable prior skill + optional stable ID
START - first executable setup only
```

A recommended fading sequence is:

```text
first similar problem: Notice + Recall + Start if needed
next: maximum Recall
then: Notice only
mixed transfer: no hints
```

Hints must not reveal the answer or complete the decisive execution unless the user explicitly requests solutions.

Strict user-requested questions-only mode overrides local hints.

---

## 13. Short-Horizon Student Route

A short-horizon Navigator is a routing layer, not the book's knowledge architecture.

For a learner with only a few days:

```text
Quick Check
-> identify weak/high-value skills
-> route to stable skill
-> practise with fading help
-> mixed no-topic-label retest
```

Keep the interface plain:

```text
DO FIRST
DO NEXT
QUICK RETEST
ONLY IF TIME
```

Do not route by `hardest first`.

Do not expose a method-revealing router before the learner has attempted the diagnostic.

---

## 14. Student Edition vs Reviewer / Build Dossier

A learner edition and a reviewer dossier have different jobs.

Preferred publication split:

```text
STUDENT EDITION
- Navigator if needed
- dependency-ordered teaching core
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
- bridge-gap audit
- visual manifest/audit
- provenance/custody ledger
- static self-sufficiency evidence
- final QA record
```

The dossier may be delivered separately or as a clearly separated second artifact when the user needs build evidence. Do not force reviewer tables into the normal learner reading path.

---

## 15. Integrated Production Gates

### Analysis Engine gates

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

### Student Book gates

```text
STUDENT_SURFACE_SEMANTIC_GRAMMAR = PASS
FIRST_MOVE_PROMINENCE = PASS_n_OF_n
ANALYSIS_JARGON_LEAKAGE = 0
LOCAL_HINT_AUDIT = PASS_n_OF_n
QUESTION_CUSTODY = PASS_n_OF_n
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n
DIFFICULTY_PRIORITY_MASTERY_CONFLATION = 0
```

Then apply the existing visual, provenance, answer, and final PDF render-QA gates.

---

## 16. Cross-domain portability

This architecture is deliberately not a Mathematics-only trick.

Physics example:

```text
Mechanics
-> Forces
-> free-body modelling
-> equilibrium / Newton II
-> constraint representation
-> first equation
-> sign/constraint check
```

Chemistry example:

```text
Stoichiometry
-> mole relation
-> equation balancing
-> limiting-reagent representation
-> first mole table/equation
-> yield / conservation check
```

The reusable abstraction is:

```text
recognition
-> representation
-> first executable move
-> execution
-> check
```

Domain profiles supply the concrete representations, legality rules, visuals, and difficulty anchors.

---

## 17. Evidence boundary

Repository build counts such as number of stable skills, bridges, or question-level PASS rows demonstrate static production coverage only.

Do not convert document-level evidence into claims about:

- learner solve rate;
- retention;
- contest score;
- classroom timing;
- psychometric difficulty;
- guaranteed performance.

Those require observed learner data.

---

## Final rule

The book should look simpler than the machinery that produced it.

A successful build has a rich internal graph and a learner who can quickly answer:

```text
What am I seeing?
What should I write or draw first?
How do I continue?
What can make this illegal or wrong?
Where do I practise it again?
```
