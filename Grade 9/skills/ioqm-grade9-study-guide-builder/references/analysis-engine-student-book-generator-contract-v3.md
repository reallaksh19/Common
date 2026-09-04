# Question-Driven Study Guide Builder v3.2

## Grade 9 Platform + IOQM Analysis Engine + Student Book Generator Contract

**Status:** generalized production contract informed by Algebra, Combinatorics and Number Theory rebuilds.

This contract is an IOQM specialization of the existing Grade 9 learning platform. It does not replace Grade 9 source grounding, concept IDs, difficulty vectors, canonical master data, question-bank calibration, enrichment, or publishing. It adds the contest-corpus decomposition and self-sufficiency needed to guarantee that target questions are actually teachable from the book.

Core principle:

```text
reliable Grade 9 infrastructure
+
rich IOQM analysis underneath
->
simple concept-assimilation learner interface
```

---

## 1. Platform inheritance

Reuse these Grade 9 contracts:

- source fidelity/QC/provenance from `grade9-source-grounding`;
- stable concept IDs/prerequisites/primary concept mapping from `grade9-concept-architect`;
- subject reasoning and Mathematics difficulty vector from the relevant subject skill;
- calibrated original practice/challenges from `grade9-question-bank`;
- misconception/diagnostic repair objects from `grade9-learning-enrichment`;
- `grade9-master.schema.json` as the canonical base master-data schema;
- master-data-first layout/link/render QA from `grade9-textbook-publisher`.

The IOQM layer adds:

```text
recognition cue
representation/compression
first executable move
execution route
legality/check
variant requirement
transfer gap
visual obligation
hint route
question support status
```

These are additive extensions to the canonical Grade 9 master, not a competing data model.

Every scored question still has exactly one `primary_concept_id` and may have secondary concept IDs.

Important:

> A primary concept assignment tells us where a question belongs. It does not prove the learner has been taught enough to solve it.

---

## 2. Two-layer IOQM architecture

```text
LAYER A - ANALYSIS ENGINE

freeze syllabus / scope
-> source-ground research material
-> freeze target corpus
-> decompose every question
-> build canonical concept graph
-> extend with opening signatures
-> build prerequisite DAG
-> audit difficulty / priority / mastery separately
-> audit orphan methods
-> audit variants and transfer gaps
-> audit visual obligations
-> qualify analysis package

================ HARD GATE ================

LAYER B - STUDENT BOOK GENERATOR

collect learner self-report
-> run unaided recognition / first-move diagnostic
-> build Part 0 route when needed
-> prototype concept/practice/navigation surfaces
-> derive learner teaching units from concept graph
-> generate teacher-like concept assimilation
-> integrate structural visuals
-> generate practice/hints/transfer
-> build Appendices
-> publish from canonical master data
-> render / link-check / inspect final pages
```

`STUDENT_BOOK_GENERATION_ALLOWED = FALSE` until the Analysis Engine passes qualification gates.

---

## 3. Syllabus and corpus custody

Do not let the target questions alone define the curriculum.

Freeze the intended syllabus/scope first, then anchor every target question back to it.

Use Grade 9 source statuses exactly:

```text
VERIFIED_TRANSCRIPTION
RECONSTRUCTED
QC_ALERT
SOURCE_UNRESOLVED
```

Preserve original source statement, verified correction if any, provenance class, figure custody and answer status.

Do not silently convert unresolved source material into a clean scored question.

---

## 4. Question Decomposition Contract

For every target question record at minimum:

- stable local question ID;
- exact/custody-preserved stem;
- source/QC/provenance status;
- syllabus topic/subtopic;
- primary concept ID;
- secondary concept IDs;
- decisive recognition cue;
- representation/compression move;
- first executable move;
- execution requirements;
- legality/reversibility/admissibility requirements;
- prerequisites;
- likely partial-knowledge misconception;
- difficulty vector;
- simple displayed difficulty badge;
- educational priority;
- learner mastery/risk when evidence exists;
- visual requirement;
- hint route/depth when allowed;
- variant requirement;
- transfer-gap status;
- final support status.

Canonical chain:

```text
QUESTION
-> SYLLABUS ANCHOR
-> PRIMARY/SECONDARY CONCEPTS
-> RECOGNITION
-> REPRESENTATION
-> FIRST MOVE
-> EXECUTION
-> LEGALITY/CHECK
-> VARIANT/TRANSFER if needed
```

---

## 5. Concept graph and Opening Signature

Build a concept/prerequisite graph using stable Grade 9 concept IDs.

For contest support, define an **Opening Signature**:

```text
(recognition cue, representation, first executable move, legality/check)
```

Split internal support nodes when question families materially differ in any component.

Hard split triggers:

```text
SPLIT if recognition differs materially
OR representation differs materially
OR first move differs materially
OR legality/check differs materially.
```

### But do not make analysis granularity a book-design rule

Never require:

```text
one internal skill = one student page
one concept ID = one chapter
validated N skills = exactly N learner-facing teaching units
```

Student teaching units may merge, split, nest or expand internal concepts to create a coherent learning journey.

The design principle is:

```text
CONCEPT ASSIMILATION determines student structure.
QUESTION COVERAGE audits that structure.
```

No target count of concepts, skills, chapters or pages is a success metric.

---

## 6. Prerequisite DAG Contract

Teaching order comes from dependency, not source order or question numbering.

Requirements:

- every stable concept/support node declares real prerequisites;
- unjustified prerequisite cycles are rejected;
- learner personalization may skip secure nodes but may not corrupt durable dependency logic;
- concept links useful for assimilation should be surfaced in readable language.

Examples of useful learner-visible chains:

```text
GCD -> Bezout -> modular inverse -> CRT
```

```text
prime factorisation -> exponent vectors -> divisor count -> perfect powers -> valuations
```

---

## 7. Orphan-Method Contract

A question is orphaned if support still requires an unnamed trick.

Required route:

```text
recognition
-> retrieve taught concept/representation
-> first executable move
-> enough continuation to finish
-> legality/check
-> extra variant/transfer when required
```

Not acceptable:

> Use CRT.

Acceptable:

```text
check compatibility
-> substitute one congruence
-> solve reduced congruence
-> state merged modulus
-> verify original conditions
```

Gate:

`ORPHAN_METHODS = 0`

---

## 8. Variant and Transfer-Gap Contract

Worked Bridges/Transfer Labs are not generic enrichment. They close a real unsupported edge:

```text
taught concept journey
-> normal worked example
-> TRANSFER GAP
-> target family
```

Classify:

```text
NONE
MODERATE
HARD
```

Rules:

- every HARD gap requires a learner-usable Variant / Transfer Lab / Worked Bridge;
- repeated MODERATE gaps may justify one;
- bridge count is evidence-driven, never a quota;
- bridge must be non-identical to the target problem;
- it must show recognition, why representation fits, first move, intermediate execution, closure, legality/wrong route and transfer prompt.

A compact reference may omit target stems only if the companion practice corpus remains in the package and all question support/transfer routes survive.

---

## 9. Difficulty model and badges

Use the Grade 9 subject difficulty vector as the analytical model. For Mathematics:

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

A D1-D5 badge is a learner-facing summary, not the underlying model.

Never collapse:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != SOURCE_STATUS
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

Concepts should normally show ranges when transfer demand is higher than core use:

```text
Chinese Remainder Theorem
[CORE D3] [TRANSFER D5] [HIGH-YIELD]
```

Questions may show:

```text
Q17 [D4 ADVANCED] [TRANSFER] [OFFICIAL PYQ]
```

After learner diagnosis, separate badges may show:

```text
[YOUR STATUS: DEVELOPING] [DO FIRST]
```

Do not encode learner weakness into authored difficulty.

---

## 10. Visual Obligation Contract

For every concept/question choose:

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
- show state/process/case structure;
- make symmetry or geometry visible;
- preserve a source-essential figure.

Decorative imagery is not coverage.

Required visuals remain subject to the visual-production lifecycle and final-size render QA.

---

## 11. Learner diagnosis and Part 0

Self-reported knowledge such as `30%` or `60%` is useful context but is not enough by itself.

Use:

```text
self-report
+
short unaided recognition / representation / first-move diagnostic
```

Do not expose method-revealing routing before the diagnostic is scored.

Part 0 uses:

```text
syllabus importance
+ prerequisite value
+ learner weakness
+ transfer value
+ time available
```

Visible routing should remain simple:

```text
DO FIRST
DO NEXT
QUICK RETEST
ONLY IF TIME
```

Keep authored difficulty, learner mastery and personalized priority as separate badges.

---

## 12. Student-Surface Concept Assimilation Contract

The student surface is **teacher-like exposition**, not a compulsory stack of cards.

Available teaching roles include:

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

These are roles, not mandatory equal-weight boxes.

For an unfamiliar/strategic concept, establish the object and mechanism before compressing to a first move.

A direct/familiar concept may be compact. A transfer-heavy concept may occupy several pages.

### Concept-assimilation questions

Borrow the Grade 9 Mathematics six-question test:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation requires a different method?
5. Can you write the first useful lines without help?
6. Can you solve a disguised version?

If the book only enables reproduction of a worked example, the concept is not yet assimilated.

---

## 13. Concrete retrieval objects

### FIRST MOVE

Must be visually findable and concrete when practical.

Bad:

> Compute the gcd first.

Better:

```text
84x + 126y = 30

gcd(84,126)=42
42 does not divide 30
STOP: no integer solutions.
```

### WATCH OUT

For subtle/risky methods, show an actual mathematical counterexample or failure mode.

### CHECK

Execute the verification with numbers/symbols when practical instead of merely saying `check the answer`.

---

## 14. Progressive Help and misconception repair

Normal IOQM learner-facing support:

```text
NOTICE - recognition clue only
RECALL - readable concept / representation
START - first executable setup only
```

Use unaided/H0 attempt first in diagnostic/testing contexts.

Fade support across later practice.

Borrow Grade 9 enrichment's causal diagnosis:

```text
wrong response
-> likely misconception
-> diagnostic probe
-> targeted repair
-> retry / transfer
```

Store specific wrong models, not generic `be careful` warnings.

---

## 15. Question-bank integration

The frozen target corpus remains source-grounded and should not be rewritten to satisfy a desired difficulty distribution.

Use `grade9-question-bank` when additional practice is needed:

- same-level calibrated originals;
- structural analogues;
- concept reinforcement;
- advanced transfer;
- mixed mastery;
- Appendix B author-created material.

Preserve the relevant Grade 9 difficulty-vector acceptance policy, while also checking IOQM recognition mechanism, Opening Signature and transfer lineage.

---

## 16. Canonical master-data contract

Use `grade9-master.schema.json` as the base source of truth.

Add IOQM analysis as extension fields rather than a competing schema, for example:

```text
question.ioqm.recognition_cue
question.ioqm.representation
question.ioqm.first_move
question.ioqm.execution_route
question.ioqm.legality_check
question.ioqm.variant_ids
question.ioqm.transfer_lab_ids
question.ioqm.visual_obligation
question.ioqm.hint_route
question.ioqm.support_status

concept.ioqm.opening_signatures
concept.ioqm.transfer_range
concept.ioqm.visual_assets
concept.ioqm.teaching_unit_ids
```

PDF page numbers and page layouts are render outputs, not canonical linkage authority.

---

## 17. Prototype gate before bulk generation

Before a long book, render and inspect at least:

- one substantial concept-assimilation journey;
- one Appendix A practice page with badges and hints;
- one Part 0/navigation page;
- one required-visual page when applicable.

Reject:

- low-contrast/broken heading colors;
- raw-ID dominance;
- tiny badges/navigation;
- card-reader teaching flow;
- missing variants or mechanism;
- vague FIRST MOVE/WATCH OUT/CHECK;
- off-page tables/figures.

Do not scale until prototypes pass.

---

## 18. Student package roles

Typical full package:

```text
PART 0
learner-specific Navigator when needed

CORE
concept-assimilation teaching journeys

APPENDIX A
frozen deliberate-practice corpus
badges + progressive local support when allowed
answers only after final question

APPENDIX B
independent mixed transfer / challenge

APPENDIX C
decision-first rapid reference

APPENDIX D
when used/requested: answers + concise learner-readable provenance/source notes
```

Challenge Ladders train progression; Appendix B tests independent mixed transfer. Do not merge their roles.

Reviewer/build dossier remains separate from the normal student reading path.

---

## 19. Publishing Contract

Use `grade9-textbook-publisher` as publishing authority.

Publish from canonical master data and preserve linked architecture:

```text
Concept
<-> Core practice
<-> Challenge / transfer
<-> Helper / hint
<-> Solution / answer
<-> Misconception diagnosis
<-> Mixed-test diagnosis
```

IOQM adds question-to-variant/transfer links and visual-obligation QA.

Render every final PDF, inspect critical pages at final reading size, validate internal links and verify IDs/answers against master data.

---

## 20. Integrated gates

### Analysis gates

```text
SYLLABUS_SCOPE_FROZEN = PASS
SOURCE_GROUNDING = PASS_n_OF_n
CORPUS_FROZEN = PASS_n_OF_n
QUESTION_DECOMPOSITION = PASS_n_OF_n
PRIMARY_CONCEPT_ID = PASS_n_OF_n
IOQM_EXECUTABLE_ROUTE = PASS_n_OF_n
PREREQUISITE_GRAPH = PASS
UNJUSTIFIED_PREREQUISITE_CYCLES = 0
ORPHAN_METHODS = 0
UNTAUGHT_REQUIRED_VARIANTS = 0
HARD_TRANSFER_GAPS_WITHOUT_SUPPORT = 0
VISUAL_OBLIGATIONS = PASS_n_OF_n
GRADE9_DIFFICULTY_VECTOR = PASS_n_OF_n_WHERE_SCORED
```

### Student-book gates

```text
CONCEPT_ASSIMILATION = PASS_ALL_REQUIRED_TEACHING_UNITS
FIRST_MOVE_CONCRETE = PASS
WATCH_OUT_CONCRETE_FOR_RISKY_METHODS = PASS
CHECK_EXECUTED_FOR_RISKY_METHODS = PASS
GUIDED_PRACTICE_FOR_TRANSFER_HEAVY_UNITS = PASS
CONCEPT_LINKS_VISIBLE = PASS
LOCAL_HINT_AUDIT = PASS_n_OF_n
CONCEPT_DIFFICULTY_BADGES = PASS_n_OF_n_WHERE_DISPLAYED
QUESTION_DIFFICULTY_BADGES = PASS_n_OF_n_WHERE_DISPLAYED
DIFFICULTY_PRIORITY_MASTERY_CONFLATION = 0
ANALYSIS_JARGON_LEAKAGE = 0
```

### Platform/publication gates

```text
GRADE9_SOURCE_STATUSES_REUSED = PASS
GRADE9_MASTER_SCHEMA_IS_CANONICAL = PASS
MASTER_LINKS = PASS
ANSWER_QA = PASS
LOW_CONTRAST_HEADINGS = 0
BROKEN_HEADING_COLORS = 0
TINY_NAVIGATION_OR_BADGES = 0
RAW_INTERNAL_ID_DOMINANCE = 0
CARD_READER_PAGE_FAILURES = 0
FINAL_RENDER_QA = PASS
```

Then apply all triggered source, visual, provenance, answer and appendix gates from the specialized references.

---

## 21. Evidence boundary

Static production gates demonstrate document/package completeness only.

Do not convert them into claims about retention, learner solve rate, contest score, classroom timing, psychometric calibration or guaranteed performance without observed learner evidence.

---

## Final rule

The book should look simpler than the machinery that produced it.

The learner should be able to answer:

```text
What is this idea?
How is it connected to what I already know?
What clue should make me notice it?
What representation should I use?
What do I write/draw first?
Which subtle variant changes the route?
What can make the move illegal or wrong?
How do I finish and check?
Where do I practise it again with less help?
```
