# Question-Driven Self-Sufficient Study Guide Skill v2

## Status and role

This document is the generalized production contract that supplements `../SKILL.md`.

It captures the workflow required to turn a supplied Olympiad-style corpus into a self-sufficient Grade 9 study guide:

> source custody -> question-to-method matrix -> prerequisite regrouping -> Draft 1 -> orphan-method audit -> visual-pedagogy audit -> worked-bridge repair -> progressive local hints -> self-sufficiency audit -> optional simple exam navigator -> inspected PDF.

Use this contract for Algebra, Number Theory, Geometry, Combinatorics, or another Grade 9 IOQM domain.

A polished PDF is not evidence that the guide is pedagogically complete.

The durable guide and the short-horizon exam layer have different jobs:

> **Navigator = where to go. Core = how to do it.**

The Navigator must not become a second textbook.

---

## 1. Learner model

Assume a learner with roughly 30–50% prior knowledge.

The learner may remember school formulas and solve routine exercises, but may not reliably:

- recognize an Olympiad structure from wording;
- distinguish nearby methods;
- choose a strategic substitution, representation, or construction;
- remember legality conditions;
- detect irreversible operations;
- write the first useful line;
- execute a non-routine method from a one-line name.

The guide must teach enough to move through:

**problem wording -> recognition -> legal method choice -> first useful line -> execution -> checking.**

---

## 2. Source roles and custody

Classify every input before authoring.

### Authority source

Official or repository-validated contest papers, correction overlays, stable source maps, frozen historical IDs, and explicitly authoritative material.

Use these for exact wording where available, answer custody, source claims, and correction decisions.

### Comparison / practice source

User notes, coaching sheets, videos, reconstructed questions, unofficial worksheets, external lists, and similar material.

Use these for method discovery, teaching-gap discovery, recognition cues, and practice breadth.

Do not silently upgrade them to official authority.

### Internal quality benchmark

Inspect the strongest repository benchmark available for the learner level.

Benchmark:

- explanation completeness;
- missing-link repair;
- recognition before formula use;
- first useful line;
- method contrasts;
- full execution;
- question-by-question self-sufficiency;
- source discipline;
- visual pedagogy;
- cover/index usability;
- final PDF quality.

A benchmark is a quality comparator, not a layout/content template. Do not copy its wording, exercises, typography, or diagrams.

---

## 3. Non-negotiable production pipeline

Execute in this order:

```text
INGEST SOURCES
-> CLASSIFY SOURCE AUTHORITY
-> INVENTORY EVERY SUPPLIED QUESTION
-> BUILD QUESTION-TO-METHOD MATRIX
-> AUDIT SYLLABUS / REPOSITORY SCOPE
-> DEFINE STABLE SKILL / BRIDGE IDS
-> DESIGN PREREQUISITE ORDER
-> WRITE DRAFT 1
-> DISTRUST DRAFT 1
-> RUN ORPHAN-METHOD AUDIT
-> RUN VISUAL-PEDAGOGY AUDIT
-> ADD / REPAIR WORKED BRIDGES
-> REGROUP / REWRITE
-> RUN BROADER-SYLLABUS AUDIT
-> BUILD APPENDIX A WITH ADAPTIVE LOCAL HINTS
-> BUILD APPENDIX B
-> BUILD APPENDIX C / QUICK REFERENCE
-> DESIGN COVER + CONTENTS/STUDY ROUTE + VISUAL BRIDGES
-> RUN CITATION / PROVENANCE AUDIT
-> RUN QUESTION-BY-QUESTION SELF-SUFFICIENCY AUDIT
-> REQUIRE PASS_n_OF_n
-> IF SHORT-HORIZON MODE IS NEEDED, BUILD SIMPLE PART 0 NAVIGATOR
-> GENERATE PDF
-> PREFLIGHT
-> RENDER EVERY PAGE AT 200 DPI
-> VISUALLY INSPECT EVERY PAGE
-> RECORD PAGE COUNT + SHA-256
```

PDF generation is downstream of content qualification.

The optional Navigator is downstream of the qualified core. It routes into the core and must not reteach it.

---

## 4. Mandatory question-to-method matrix

Before learner prose, create one row for every supplied question.

Required columns:

- stable local question ID;
- exact mathematical surface;
- main subtopic;
- secondary prerequisite;
- recognition cue;
- first useful mathematical line;
- complete execution method;
- domain / reversibility / admissibility conditions;
- likely half-knowledge misconception;
- planned teaching location;
- required visual, if any;
- hint depth: `NONE`, `H1`, `H1-H2`, or `H1-H3`;
- distinct mechanism family;
- global study-priority inputs when short-horizon mode is requested;
- current support status: `PASS`, `PARTIAL`, or `FAIL`.

### Teaching-obligation rule

Every supplied question creates a teaching obligation.

If a required method does not appear in the guide, the guide is incomplete.

If it appears only as a formula or one-line cue, the guide is still incomplete.

---

## 5. Stable skill and bridge IDs

Every reusable method should receive a stable ID.

Recommended pattern:

```text
<DOMAIN>-<FAMILY>-<NN>
```

Examples:

```text
ALG-SYM2-01
GEO-CYCLIC-02
COMB-GAPS-01
NT-VALUATION-02
```

Advanced worked bridges may use domain-qualified IDs such as:

```text
ALG-A17
GEO-A08
```

Student-facing references should normally display a readable name first or alongside the ID:

> **Centroid 2:1** · `GEO-CENTROID-01`

Stable IDs support durable cross-references, audits, future reordering, Appendix A H2 retrieval, and internal routing.

Do not let opaque IDs dominate a stressed learner's interface.

---

## 6. Syllabus and scope audit

For each declared syllabus item mark one of:

- `FULLY_TAUGHT`;
- `BRIDGE_LEVEL`;
- `TAUGHT_UNDER_ANOTHER_HEADING`;
- `INTENTIONALLY_SCOPE_LIMITED`;
- `MISSING_AND_REQUIRES_REPAIR`.

Compare the supplied corpus with the syllabus, existing domain packages, relevant cross-domain interfaces, and verified historical mechanism maps.

Do not fake completeness. A topic appearing only on a memory sheet is not automatically fully taught.

---

## 7. Dependency-based learner order

Do not copy source-question order unless it is pedagogically strong.

A robust default order is:

1. notation and foundations;
2. direct school-to-Olympiad bridges;
3. legal transformations and checking;
4. core structural methods;
5. restricted variants;
6. representation changes;
7. advanced methods;
8. mixed method selection.

Regroup after the orphan-method audit if prerequisites still appear after use.

---

## 8. Draft 1 teaching contract

For every substantial subtopic include, where applicable:

### What you probably remember
Minimal school-level refresh.

### The missing Olympiad link
What ordinary school treatment usually leaves unstated.

### Why this works
Mechanism, not only a formula.

### Non-identical worked example
A complete example revealing the method without copying Appendix A.

### What should I notice?
Recognition cues from wording, diagram, or structure.

### Try this first
An executable first mathematical line or construction.

### Close contrast
A nearby case where the method is wrong, illegal, or inefficient.

### Common mistake
Target the likely half-knowledge error.

### Legality / domain / equality check
State conditions before theorem use or irreversible steps.

### Practice pointer
Point to answer-free practice and the relevant stable skill ID.

Use student/teacher language, not internal production jargon.

---

## 9. Orphan-method audit

For every supplied question ask:

> Could a learner with roughly 30–50% prior knowledge actually execute this method from the guide, or did the guide merely name the trick?

Examples of orphaning:

- “use Vieta” without rebuilding the target expression;
- “apply AM-GM” without positivity and equality conditions;
- “draw an auxiliary line” without explaining the relation it should create;
- “use Burnside” without fixed-set counting;
- “square both sides” without extraneous-root handling;
- “use a recurrence” without defining state or proving recurrence;
- “use coordinates” without explaining coordinate placement.

Repair every orphan with stronger chapter teaching or a dedicated Advanced Worked Bridge.

No required question may remain `PARTIAL` or `FAIL` before final PDF generation.

---

## 10. Visual-pedagogy audit

Figures are teaching tools, not decoration.

For every chapter and supplied question ask:

> Would a figure, graph, number line, table, construction, state diagram, or schematic materially reduce cognitive load or reveal structure that prose alone hides?

If yes, include it.

### Geometry — visuals strongly expected

Use construction-quality figures for diagram-dependent reasoning such as collinearity, concurrency, cyclicity, angle relations, similarity/homothety, equal lengths, loci, transformations, auxiliary constructions, coordinate placement, area decomposition, moving points, and extremal geometry.

For Geometry Appendix A, H1 may tell the learner what to mark on the figure.

### Algebra — visuals only when they reveal structure

Useful cases include root/tangency graphs, sign/domain number lines, function-composition maps, finite-difference tables, recurrence/state evolution, and smoothing/extremum schematics.

### Combinatorics

Useful cases include blocks/gaps, graph models, state diagrams, circular arrangements, matchings, symmetry/orbits, and small game-state pictures.

### Number Theory

Useful cases include residue cycles, exponent grids, valuation tables, and lattice/Diophantine-region sketches.

### Figure quality rules

Prefer author-created mathematical figures.

Every figure should:

- have readable labels at final size;
- use notation consistent with nearby text;
- have a short caption or nearby explanation;
- avoid solution leakage in answer-free practice;
- preserve mathematical geometry unless marked `not to scale`;
- avoid clutter;
- be cited if externally sourced;
- survive final 200-dpi inspection.

If a problem requires a figure to preserve mathematical conditions, Appendix A/B must include it.

---

## 11. Visual Bridge pages

Use thematic **Visual Bridge** pages when several related methods become clearer through a common representation.

A strong Visual Bridge normally contains 2–4 compact panels, each with:

- a visual model;
- one recognition phrase;
- one first move;
- one boundary/contrast if useful.

Examples:

- Geometry: cyclicity / tangent / similarity / homothety;
- Algebra: roots/tangency, symmetry/compression, polynomial structure, recurrence/finite differences;
- Combinatorics: blocks/gaps, circles/symmetry, graphs/coloring, states/recurrences;
- Number Theory: residues, valuations, divisor exponent grids.

Visual Bridges should be interleaved near the relevant core chapters rather than collected as decorative plates at the end.

---

## 12. Advanced Worked Bridges

After orphan-method and visual audits, create bridges for remaining non-routine methods.

A bridge should include:

1. recognition cue;
2. why the method fits;
3. first line / construction;
4. full execution;
5. legality / equality check;
6. nearby wrong approach;
7. one small transfer prompt;
8. stable bridge ID.

Use non-identical examples.

A bridge must be imitation-ready: enough intermediate work should be visible that a half-prepared learner can reproduce the mechanism on a nearby problem.

---

## 13. Appendix A — supplied corpus with adaptive local hints

Appendix A preserves source custody.

Rules:

- every supplied question appears exactly once;
- preserve all mathematical conditions and required figures;
- no worked solution in the problem body;
- no source commentary in the problem body;
- answer key only after the final question;
- provenance remains in a separate source ledger;
- do not invent continuation numbering when the source ends.

### Preferred static-PDF layout

```text
Qn. Problem statement
[small relevant figure if useful]

H1 👀 Notice     recognition clue
H2 ↩ Recall     readable skill name + stable ID
H3 ✏ Start      first executable move
```

Hints should be thin, visually quiet strips directly under the question or figure. The question remains dominant.

### Adaptive hint depth

- routine transfer: `NONE` or `H1`;
- easy: `H1`;
- medium: `H1-H2`;
- hard: `H1-H3`.

Aim for 2–3 questions/page where legibility permits.

### Hint length

- H1: usually one sentence;
- H2: usually one sentence;
- H3: at most two short sentences/equations.

If a hint needs a paragraph, move that teaching into the core or a Worked Bridge.

### H1 — Notice

Recognition only.

### H2 — Recall

Retrieve previously taught learning. Prefer readable name + stable ID.

### H3 — Start

Give the first executable move, not the solution.

### Progressive-use instruction

At the start of Appendix A:

> Try the problem first. Read H1 only if you cannot identify the structure. Read H2 only if you cannot retrieve the earlier skill. Use H3 only if you still cannot write the first mathematical move.

For static PDFs, use visual hierarchy: H1 strongest, H2 quieter, H3 quietest.

Use a consolidated Hint Bank only when local hints would overcrowd a large figure or reveal too much by proximity.

---

## 14. Appendix B — mixed transfer set

Appendix B should test the revised guide beyond the supplied corpus.

Default size: approximately 20 questions unless the domain warrants another count.

Rules:

- source historical items accurately;
- label author-created items clearly;
- sample methods actually taught;
- include underrepresented canonical mechanisms where useful;
- hide topic labels where transfer is being tested;
- use lighter scaffolding than Appendix A;
- no solution beside the question;
- answer key after the final problem;
- independently recompute every answer.

Create an Appendix B method-coverage table for reviewer QA.

---

## 15. Appendix C — decision-first quick reference

Appendix C should be a compact memory helper, usually 1–3 pages.

The first page should be **decision-first**, not formula-first:

> **What do I see? -> What should I draw/write first?**

Then place formulas/tools after method choice.

Include only high-value recall material:

- method triggers;
- core formulas;
- theorem legality conditions;
- equality conditions;
- common transforms;
- final pre-submit checks;
- stable IDs in secondary type where useful.

Do not put full worked solutions in Appendix C.

A topic appearing only in Appendix C does not count as fully taught.

---

## 16. Cover, contents, operating rule, and book navigation

A strong study guide should be understandable before the learner enters Chapter 1.

### Cover

The cover should communicate, at a glance:

1. Grade / exam context;
2. subject;
3. edition / guide identity;
4. concise value proposition;
5. learner profile;
6. short process strip.

Example structure:

```text
IOQM GRADE 9
<SUBJECT>
Complete Study Guide

3-Day Navigator + durable reference + guided practice + mixed transfer + visual quick reference

Built for a learner who:
- knows roughly 30–50% but misses the hidden method;
- needs to recognize, choose, execute, and check;
- cannot read a textbook front-to-back before the exam.

LEARN -> VISUALIZE -> PRACTISE -> RETRIEVE
```

Do not overload the cover with QA metadata.

### Contents and Study Route

Prefer **Contents and Study Route** over a plain table of contents.

For every major destination show:

- section name;
- one-line purpose;
- page number.

Make `START HERE` visually clear.

Typical destinations:

- Part 0 / simple short-horizon Navigator;
- Core Reference Book;
- interleaved Visual Bridges;
- Advanced Worked Bridges;
- Appendix A Guided Practice;
- Appendix B Mixed Transfer;
- Appendix C Decision-First Quick Reference;
- Sources and Provenance.

### One-page operating rule

A durable guide may include one simple operating-rule page before the core.

Use no more than 3–5 domain-specific questions such as:

- What structure is visible?
- Which representation makes it cheaper?
- Is the first move legal?
- What is my first useful line?

Do not expose internal audit jargon on this page.

### Sources and provenance

Keep provenance separate from clean learner practice. Use a source ledger / end section rather than cluttering Appendix A.

---

## 17. Optional Part 0 — Simple 72-Hour Exam Navigator

### 17.1 Governing principle

When a learner has only a few days before an exam, the production system may use sophisticated routing internally, but the **student-facing interface must remain simple**.

> **Complexity belongs in the engine, not in the learner interface.**

The core reference book remains unchanged in purpose.

The student should be able to understand Part 0 without learning a diagnostic vocabulary.

Target student-facing length: **4 pages maximum** unless a domain genuinely requires more.

### 17.2 Student-facing four-page architecture

#### Page 1 — Start Here

One message:

> You do not need to read this book from beginning to end in three days.

Show one simple flow:

```text
QUICK CHECK -> FIND WEAK TOPICS -> FIX HIGH-VALUE GAPS -> PRACTISE -> MIXED TEST
```

Show the three-day purpose only:

- Day 1 — recognize the main patterns;
- Day 2 — practise important weak areas;
- Day 3 — mixed questions + quick revision.

Do not show formulas, readiness percentages, or internal metrics here.

#### Page 2 — Quick Check

Default: **8–10 short items**; domain profile may set the exact count.

Use `T1`, `T2`, … labels for diagnostic items so they cannot be confused with source/practice `Q1`, `Q2`, … numbering.

Instruction:

> Spend about 1–2 minutes on each. Do not fully solve. Mark: `[OK] knew the move` `[?] unsure` `[X] no idea`.

Each item should ask a recognition/first-move question, not demand full execution.

**No H1 or method router before the learner marks the item.**

The unaided response is the useful signal. H1 may be revealed afterward for learning.

#### Page 3 — What should I study?

Map each `T` item to a readable skill/topic and the relevant core section.

Use a simple priority interface:

- **DO FIRST**;
- **DO NEXT**;
- **ONLY IF TIME**.

Readable names should dominate. Stable IDs may appear in smaller secondary type.

Fold the method router into this page **after** the Quick Check rather than showing it before the diagnostic.

A simple default rule:

- `[X]` on a high-value family -> DO FIRST;
- `[?]` -> DO NEXT;
- `[OK]` -> one quick mixed retest, then move on.

#### Page 4 — When you get stuck

Use plain language rather than exposing internal codes:

```text
I don't know what method applies
-> read H1 Notice

I know the topic but forgot the method
-> read H2 Recall

I know the method but cannot begin
-> read H3 Start

I started correctly but got stuck halfway
-> open the linked Worked Bridge / worked example

I reached an answer but it is wrong
-> run the legality / branch / equality / final-target checklist
```

Also include:

- the Day 1 / Day 2 / Day 3 reminder;
- the rule to try a nearby problem with less help;
- a short night-before check;
- **no major new core skill on Day 3**;
- stop studying at a sensible time and protect normal sleep.

### 17.3 Internal routing model — not normally student-facing

The authoring/teacher layer may retain richer diagnostics:

- recognition before cue versus recognition after H1;
- recognition weakness versus execution weakness;
- `R/M/S/E/C` error localization;
- global `MUST/SHOULD/IF_TIME` curriculum priority;
- workload caps;
- hint-dependency tracking;
- transfer success;
- suggested readiness thresholds.

These are routing tools, not learner-facing terminology and not psychometrically validated scales.

Do not print them in the simple Navigator unless a teacher-facing edition explicitly requests them.

### 17.4 Recognition-before-cue rule

For internal measurement distinguish, if useful:

- `R0` — recognized unaided;
- `R1` — recognized after H1/Notice;
- `R2` — still not recognized after H1.

The student still sees only `[OK]`, `[?]`, `[X]`.

After an unsuccessful attempt, provide corrective feedback rather than repeated blind guessing.

### 17.5 Global educational priority

Hint depth and priority are orthogonal.

Use an internal authoring rubric when useful:

```text
PriorityScore = 3T + 2F + 2D + R
```

with `T,F,D,R` scored `0–2` for:

- transfer value;
- distinct-mechanism frequency plus canonical relevance;
- dependency value;
- repair value for common partial-knowledge misconceptions.

This is an **authoring rubric**, not a validated scientific metric.

Any numeric thresholds are calibration defaults only. Curriculum review confirms final priority.

Deduplicate repeated questions before using frequency.

Apply foundational and niche overrides where needed.

### 17.6 Global priority versus personal route

Distinguish:

- **Global priority:** educational/curriculum value;
- **Personal route:** what this learner needs now.

A learner does not need to complete every global MUST question.

Internal routing can use:

| Global value | Learner state | Action |
|---|---|---|
| high | weak | do now |
| high | uncertain | do next |
| high | secure | quick retest only |
| medium | weak | after high-value gaps |
| low / niche | weak | usually skip in 72-hour mode |

Student-facing labels remain `DO FIRST / DO NEXT / ONLY IF TIME`.

### 17.7 Workload guardrails

The Navigator must prioritize deficits, not enumerate them as homework.

Useful calibration defaults:

```text
MAX_ACTIVE_WEAK_CORE_FAMILIES_PER_DAY = 4
MAX_NEW_CORE_SKILLS_DAY3 = 0
MAX_GLOBAL_CORE_PRACTICE_ROUTE ≈ 24 ITEMS
```

These are workload guardrails, not empirically validated IOQM constants.

### 17.8 Hint fading and spacing

Do not call mastery after repeating the identical problem immediately.

Use:

```text
LEARN
worked bridge; H1 + H2 + H3 as needed

-> later / nearby non-identical problem

RETRIEVE
maximum H2

-> later / different nearby problem

TRANSFER
maximum H1

-> mixed unlabeled problem

EXAM
no hints
```

Space important families across the three days rather than completing all repetitions in one block.

### 17.9 Source-stability rule

Preserve unresolved or reconstructed items in the durable corpus when source custody requires them, but do not spend scarce short-horizon time on unstable wording or unresolved answer conflicts.

Mark internally:

```text
SOURCE_STATUS = UNRESOLVED
72_HOUR_CORE = NO
```

Likewise, duplicates should not consume a separate priority slot unless deliberate spaced retrieval is intended.

### 17.10 Student-facing acceptance gates

When simple Part 0 is requested, require:

```text
SIMPLE_NAVIGATOR_PRESENT = PASS
SIMPLE_NAVIGATOR_PAGES <= 4
QUICK_CHECK_LABELS_USE_T_PREFIX = PASS
QUICK_CHECK_Q_NUMBER_COLLISION = 0
QUICK_CHECK_ITEMS = 8_TO_10_OR_DOMAIN_OVERRIDE
QUICK_CHECK_UNAIDED_BEFORE_HINT = PASS
READABLE_SKILL_ROUTE = PASS
DO_FIRST_NEXT_IF_TIME_ROUTE = PASS
PLAIN_LANGUAGE_STUCK_REPAIR = PASS
DAY3_NEW_MAJOR_CORE_SKILLS = 0
NIGHT_BEFORE_NEW_ADVANCED_THEORY = 0
NAVIGATOR_INTERNAL_JARGON_EXPOSED = 0
NAVIGATOR_THEORY_DUPLICATION = 0
```

The final two conditions are hard rules.

---

## 18. Citation and provenance audit

Keep provenance separate from clean question presentation.

Preferred locations:

- `Sources_and_Citations.md`;
- reviewer manifest;
- stable historical ID tables;
- final provenance section;
- chapter endnotes only where useful.

Preserve uncertainty.

Never convert:

- identified practice problem -> confirmed official lecture question;
- reconstructed wording -> official wording;
- answer-key agreement -> proof of source identity.

---

## 19. Final self-sufficiency audit

Create one row for every Appendix A question.

A question passes only when all required support exists:

1. prerequisite refresh;
2. recognition cue;
3. first useful line;
4. execution bridge;
5. legality/error check where relevant;
6. answer-free practice presentation;
7. required visual support where relevant;
8. assigned local hint depth is present and non-solution-like;
9. H2 references previously taught learning where applicable.

Record:

```text
QUESTION_INVENTORY = PASS_n_OF_n
QUESTION_TO_METHOD_MATRIX = PASS_n_OF_n
ORPHAN_METHOD_AUDIT = PASS_n_OF_n
VISUAL_PEDAGOGY_AUDIT = PASS_n_OF_n
APPENDIX_A_CUSTODY = PASS_n_OF_n
APPENDIX_A_HINT_AUDIT = PASS_n_OF_n
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n
```

Use `PASS_n_OF_n` only when every row genuinely passes.

This is a static document-level claim, not classroom evidence.

Keep separate unless actually measured:

- learner solve rate;
- timing;
- retention;
- recognition accuracy;
- first-line accuracy;
- hint dependency;
- transfer success;
- psychometric calibration;
- qualification probability.

---

## 20. Hard PDF gate

PDF generation is allowed only when:

```text
QUESTION_MATRIX = COMPLETE_n_OF_n
ORPHAN_METHODS = 0
VISUAL_PEDAGOGY_GAPS = 0
ADVANCED_BRIDGES_REQUIRED = ADVANCED_BRIDGES_PRESENT
APPENDIX_A_CUSTODY = PASS_n_OF_n
APPENDIX_A_HINT_AUDIT = PASS_n_OF_n
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n
```

If short-horizon mode is requested, also require the simple Navigator acceptance gates.

If any required question remains `PARTIAL` or `FAIL`:

```text
PDF_GENERATION_ALLOWED = FALSE
STATUS = CONTENT_REWRITE_REQUIRED
```

Do not override this gate because the draft looks polished.

---

## 21. PDF production and QA

Before PDF work, read the environment's required PDF-production skill.

Mandatory final QA:

- preflight the exact binary;
- confirm page size and page count;
- confirm text extraction where expected;
- render every page at 200 dpi;
- visually inspect every page;
- inspect every mathematical figure at final size;
- inspect cover hierarchy and Contents/Study Route readability;
- inspect Visual Bridge panels;
- verify H1/H2/H3 strips remain readable but quiet;
- inspect simple Navigator pages and T-label consistency if present;
- check clipping, overlap, broken glyphs, malformed math, missing figures, tiny labels, illegible captions, and page-break damage;
- record SHA-256 of the exact delivered PDF.

If an essential figure is missing/broken, treat it as a content failure, not a cosmetic defect.

---

## 22. Recommended output package

```text
README.md
<Subject>_Study_Guide_vN.md
Question_to_Method_Matrix.md
Advanced_Worked_Bridges.md
Appendix_A_<supplied-corpus>.md
Appendix_B_<mixed-transfer-set>.md
Quick_Reference.md
Self_Sufficiency_Audit.md
Sources_and_Citations.md
QA.md
PDFs/<Subject>_IOQM_Grade9_Study_Guide_vN.pdf
```

Part 0 normally remains integrated in the primary guide source rather than becoming a separate theory document.

Domain profiles may add figure manifests, diagram sources, specialized method maps, or domain-specific short-horizon routing tables.

---

## 23. Acceptance principle

A guide is not self-sufficient because it lists every formula, mentions every syllabus heading, contains many solved examples, has a large Appendix A, or looks professional.

It is self-sufficient only when a half-prepared learner can move from:

**problem wording -> recognized structure -> legal first step -> executable method -> correct check**

without relying on an unnamed trick that exists only in the teacher's head.

For short-horizon use:

> **Coverage per hour matters more than coverage per page.**

The durable core remains complete. The simple Navigator only tells this learner where to go next.