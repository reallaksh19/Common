# Question-Driven Self-Sufficient Study Guide Skill v2

## Status and role

This document is a **generalized production contract** that supplements `../SKILL.md`.

It captures the production method proven necessary by the Grade 9 IOQM Combinatorics v2 benchmark and the later Algebra v2 rebuild:

> corpus custody -> question-to-method matrix -> prerequisite regrouping -> Draft 1 -> orphan-method audit -> visual-pedagogy audit -> worked-bridge repair -> self-sufficiency audit -> appendices -> inspected PDF.

Use this contract for Algebra, Number Theory, Geometry, Combinatorics, or another Grade 9 IOQM domain whenever a study guide must support a supplied problem corpus.

A polished PDF is **not** evidence that the guide is pedagogically complete.

---

## 1. Learner model

Assume a learner with roughly **50% prior knowledge**.

The learner may:

- remember familiar school formulas;
- solve routine textbook exercises;
- recognize standard notation;
- reproduce a recently demonstrated method.

Do not assume the learner can:

- recognize an Olympiad structure from wording;
- distinguish two nearby methods;
- choose a strategic substitution;
- recall theorem legality conditions automatically;
- detect when an operation is irreversible;
- finish a non-routine method from a one-line hint.

The guide must therefore teach enough to move through:

**problem wording -> recognition -> legal method choice -> first useful line -> execution -> checking.**

---

## 2. Source roles and custody

Classify every input before authoring.

### Authority source

Official or repository-validated contest papers, source maps, correction overlays, stable interfaces, frozen historical IDs, and other explicitly authoritative material.

Use these for:

- exact historical claims;
- official wording where available;
- answer custody;
- correction decisions;
- syllabus/source assertions.

### Comparison / practice source

User notes, coaching handouts, videos, reconstructed questions, unofficial worksheets, DPPs, preparation routines, external problem lists, and similar material.

Use these for:

- method discovery;
- teaching-gap discovery;
- recognition cues;
- practice breadth.

Do not silently upgrade them to official authority.

### Internal quality benchmark

Inspect the strongest repository benchmark available for the same learner level.

Benchmark:

- explanation completeness;
- missing-link repair;
- recognition before formula use;
- first useful line;
- method contrasts;
- complete execution;
- willingness to reject Draft 1;
- question-by-question self-sufficiency;
- source discipline;
- visual pedagogy;
- final PDF quality.

Do not copy wording, exercises, diagrams, visual style, typography, or page design.

---

## 3. Non-negotiable production pipeline

Execute this sequence in order:

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
-> BUILD APPENDIX A + HINT LADDERS
-> BUILD APPENDIX B
-> BUILD APPENDIX C / QUICK REFERENCE
-> RUN CITATION / PROVENANCE AUDIT
-> RUN QUESTION-BY-QUESTION SELF-SUFFICIENCY AUDIT
-> REQUIRE PASS_n_OF_n
-> GENERATE PDF
-> PREFLIGHT
-> RENDER EVERY PAGE AT 200 DPI
-> VISUALLY INSPECT EVERY PAGE
-> RECORD PAGE COUNT + SHA-256
```

PDF generation is downstream of content qualification.

---

## 4. Stage 1 — mandatory question-to-method matrix

Before learner prose, create a row for **every supplied question**.

Required columns:

- stable local question ID;
- exact mathematical surface;
- main subtopic;
- secondary prerequisite;
- recognition cue;
- first useful mathematical line;
- complete execution method;
- domain / reversibility / admissibility conditions;
- likely misconception of a half-prepared learner;
- planned teaching location;
- required visual, if any;
- hint depth required: `NONE`, `H1`, `H1-H2`, or `H1-H3`;
- current support status: `PASS`, `PARTIAL`, or `FAIL`.

### Teaching-obligation rule

Every supplied question creates a teaching obligation.

If a problem needs a method that does not appear in the planned guide, the guide is incomplete.

If the method appears only as a formula or one-line cue, the guide is still incomplete.

---

## 5. Stable skill and bridge IDs

Every reusable method taught in the guide should receive a stable local ID.

Recommended pattern:

```text
<DOMAIN>-<FAMILY>-<NN>
```

Examples:

```text
ALG-SYM2-01
ALG-VIETA-03
GEO-CYCLIC-02
COMB-GAPS-01
NT-VALUATION-02
```

Advanced worked bridges may use:

```text
A01, A02, A03, ...
```

or a domain-qualified form such as:

```text
ALG-A17
GEO-A08
```

### Why IDs matter

The IDs allow:

- Appendix A hints to refer back to earlier teaching;
- the self-sufficiency audit to verify actual coverage;
- the quick reference to point to the correct chapter;
- future revisions to preserve learner navigation;
- hard questions to receive progressive support without printing a disguised solution.

---

## 6. Stage 2 — syllabus and scope audit

Compare the supplied corpus with:

- declared syllabus;
- existing domain topic packages;
- relevant cross-domain interfaces;
- verified historical mechanism maps.

For each syllabus item mark one of:

- `FULLY_TAUGHT`;
- `BRIDGE_LEVEL`;
- `TAUGHT_UNDER_ANOTHER_HEADING`;
- `INTENTIONALLY_SCOPE_LIMITED`;
- `MISSING_AND_REQUIRES_REPAIR`.

Do not fake completeness.

A topic appearing only on a memory sheet is not automatically `FULLY_TAUGHT`.

A named topic without an executable example is not automatically `BRIDGE_LEVEL`.

---

## 7. Stage 3 — dependency-based learner order

Do not copy source-document order unless it is pedagogically strong.

A robust default dependency order is:

1. language / notation / foundations;
2. direct school-to-Olympiad bridges;
3. legal transformations and candidate checking;
4. core structural methods;
5. restricted / conditional variants;
6. representation changes;
7. advanced methods;
8. mixed method choice.

Regroup after the orphan-method audit if the first organization still creates prerequisite jumps.

Record what changed and why.

---

## 8. Stage 4 — write Draft 1 like a teacher

For every substantial subtopic include, where applicable:

### What you probably remember

Minimal school-level refresh.

### The missing Olympiad link

What standard school treatment usually does not teach.

### Why this works

Mechanism, not merely formula.

### Non-identical worked example

A complete example revealing the method without copying Appendix A.

### What should I notice?

Recognition cues from wording or structure.

### Try this first

An executable first mathematical line.

### Close contrast

A similar-looking case where this method is wrong, illegal, or inefficient.

### Common mistake

Target the likely half-knowledge error.

### Legality / domain / equality check

State conditions before theorem use or irreversible operations.

### Practice pointer

Point to answer-free practice and its relevant skill ID.

Use teacher/student language. Keep internal production jargon out of learner-facing prose.

---

## 9. Stage 5 — distrust Draft 1: orphan-method audit

For every supplied question ask:

> Could a learner with roughly 50% prior knowledge actually execute this method from the guide, or did the guide merely name the trick?

A method is **orphaned** if the learner must already know an unstated move.

Cross-domain examples:

- “use Vieta” without rebuilding the target expression;
- “apply AM-GM” without positivity and equality conditions;
- “use Burnside” without fixed-set counting;
- “draw an auxiliary line” without explaining what relation it is meant to create;
- “use generating functions” without coefficient extraction;
- “square both sides” without extraneous-root handling;
- “use a recurrence” without defining state or proving recurrence;
- “use coordinates” without explaining the coordinate placement.

Repair every orphan with either:

- stronger main-chapter teaching; or
- a dedicated **Advanced Worked Bridge**.

Do not mark the guide self-sufficient while any supplied question remains `PARTIAL` or `FAIL`.

---

## 10. Stage 6 — visual-pedagogy audit

Figures are a **teaching tool**, not decoration.

For every chapter and supplied question ask:

> Would a figure, graph, state diagram, number line, table, construction, or schematic materially reduce cognitive load or reveal structure that prose alone hides?

If yes, include it.

### Geometry — visuals strongly expected

Use construction-quality figures whenever reasoning depends on:

- collinearity / concurrency;
- cyclicity;
- angle relations;
- similarity / homothety;
- equal lengths;
- loci;
- reflections / rotations;
- auxiliary constructions;
- coordinate placement;
- area decomposition;
- moving-point or extremal geometry.

A diagram-dependent theorem or worked example should not force the learner to construct the whole picture mentally.

### Algebra — visuals when they explain structure

Useful visuals include:

- graph shape and root count;
- repeated / tangent roots;
- function transformations;
- sign intervals on a number line;
- mapping / composition diagrams;
- sequence evolution;
- recurrence state transitions;
- inequality feasible regions;
- floor / ceiling / piecewise behavior.

Do not add a graph when the symbolic structure is clearer.

### Combinatorics

Useful visuals include:

- graph models;
- state diagrams;
- block/gap schematics;
- circular arrangements;
- matching diagrams;
- small symmetry examples;
- recurrence-state transitions.

### Number theory

Useful visuals may include:

- exponent grids;
- residue cycles;
- valuation tables;
- lattice / Diophantine-region sketches;
- factor trees only when pedagogically justified.

### Figure quality rules

Prefer author-created mathematical figures over decorative or stock imagery.

Every useful figure should:

- have readable labels at final PDF size;
- use notation consistent with the text;
- have a short caption or nearby explanation;
- avoid leaking a hidden construction or answer in answer-free practice;
- preserve mathematical geometry unless marked `not to scale`;
- avoid visual clutter;
- be cited if externally sourced;
- be checked in the final 200-dpi render.

### Appendix figure rule

If an Appendix A or B question requires a figure to preserve mathematical conditions, include the figure.

Do not replace a necessary figure with prose just to keep the appendix text-only.

---

## 11. Stage 7 — Advanced Worked Bridges

After orphan-method and visual audits, create bridges for remaining non-routine methods.

A bridge should include:

1. recognition cue;
2. why the method is appropriate;
3. first line;
4. full execution;
5. legality / equality check;
6. nearby wrong approach;
7. one small transfer prompt;
8. stable bridge ID.

Use a non-identical example.

The purpose is transfer, not rehearsal of the exact Appendix A problem.

---

## 12. Appendix A — supplied corpus with progressive hints

Appendix A is the supplied corpus and must preserve custody.

Rules:

- every supplied question appears exactly once;
- preserve all mathematical conditions and required figures;
- no worked solution in the question body;
- no source commentary in the question body;
- answer key only after the final question;
- provenance kept in a separate source ledger;
- do not invent continuation numbering when the source ends.

### Progressive hint ladder

Especially for difficult questions, Appendix A should include a **progressive H1-H3 hint ladder** that points back to skills already taught in the guide.

Hints should be usable one at a time.

#### H1 — recognition hint

Purpose: help the learner recognize the structure without giving the opening algebra.

Typical form:

> **H1 — Recognition:** This is a symmetric two-variable problem. Revisit `ALG-SYM2-01`.

H1 should answer:

- What should I notice?
- Which earlier skill family is relevant?

H1 should **not** reveal the result or full substitution unless that substitution itself is the recognition objective.

#### H2 — first-step hint

Purpose: provide the first useful mathematical move.

Typical form:

> **H2 — First step:** Use the sum-product variables from `ALG-SYM2-01`: set `s=x+y`, `p=xy`.

H2 should answer:

- What do I write first?
- Which earlier worked bridge should I reopen?

It may reference a chapter or bridge ID.

#### H3 — execution-direction hint

Purpose: break the main bottleneck while still withholding the final numerical answer.

Typical form:

> **H3 — Execution:** After finding `s,p`, rebuild the target using the power-sum identity from `ALG-SYM2-02` rather than solving for `x,y` separately.

H3 may expose:

- the decisive identity;
- the correct branch test;
- the auxiliary construction goal;
- the required state definition;
- the exact earlier bridge to imitate.

H3 should normally **not** print the final answer.

### Hint-depth policy

Not every question needs three hints.

Use:

- `NONE` for routine transfer problems;
- `H1` when recognition is the main challenge;
- `H1-H2` when the opening move is likely to block a half-prepared learner;
- `H1-H3` for genuinely tough questions with a non-obvious execution bottleneck.

The question-to-method matrix should record the required depth.

### Previous-skill reference rule

Hints should preferably refer to **previously taught skill IDs or bridge IDs**.

A hint should reinforce navigation through the guide rather than introduce a new method for the first time.

If H3 requires a method not already taught, the guide has an orphan method and must be repaired before Appendix A is finalized.

### Layout options

For a static PDF, choose one of:

1. hints immediately below each question, visually separated and progressively indented;
2. a dedicated `Appendix A Hint Bank` after all questions but before the answer key;
3. question-level hint references plus a consolidated hint bank.

Prefer the consolidated hint-bank approach when immediate hints would make the problem page too revealing.

Regardless of layout, preserve the progression H1 -> H2 -> H3.

---

## 13. Appendix B — approximately 20 reliable-source or clearly labeled author-created problems

Use Appendix B to audit the revised guide beyond the supplied corpus.

Rules:

- source every historical item accurately;
- label author-created items clearly;
- sample the methods actually taught;
- include underrepresented but canonical methods where useful;
- no solution beside the question;
- optional H1-H3 hint ladders may be supplied for the hardest items, following the same policy as Appendix A;
- answer key only after the final problem;
- independently recompute every answer.

Create an Appendix B method-coverage table for reviewer QA.

---

## 14. Appendix C / Quick Reference

Create a 1-2 page memory helper when useful.

Include only high-value recall material:

- core formulas;
- compact method triggers;
- theorem legality conditions;
- equality conditions;
- common transforms;
- frequently used small constants / patterns;
- final pre-submit checks;
- skill IDs for deeper explanation where space permits.

Do not put full worked solutions in the helper.

A topic appearing only in Appendix C does **not** count as fully taught.

---

## 15. Citation and provenance audit

Keep provenance separate from clean question presentation.

Preferred locations:

- `Sources_and_Citations.md`;
- reviewer manifest;
- stable historical ID tables;
- chapter endnotes where pedagogically useful.

Preserve uncertainty.

Never convert:

- “identified practice problem” into “confirmed official lecture question”;
- reconstructed wording into official wording;
- answer-key agreement into proof of source identity.

---

## 16. Final self-sufficiency audit

Create one row for every Appendix A question.

A question passes only when all required support exists:

1. prerequisite refresh;
2. recognition cue;
3. first useful line;
4. execution bridge;
5. legality / error check where relevant;
6. answer-free practice presentation;
7. required visual support where relevant;
8. H1-H3 hint ladder at the difficulty level assigned in the matrix.

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

This is a **static document-level claim**, not classroom evidence.

Keep these separate unless measured:

- classroom timing;
- learner solve rate;
- retention;
- psychometric calibration;
- qualification probability.

---

## 17. Hard PDF gate

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

If even one question remains `PARTIAL` or `FAIL`:

```text
PDF_GENERATION_ALLOWED = FALSE
STATUS = CONTENT_REWRITE_REQUIRED
```

Do not override this gate because the current draft is visually polished.

---

## 18. PDF production and QA

Before PDF work, read the repository/system PDF-production skill required by the environment.

Mandatory final QA:

- preflight the exact binary;
- confirm page size and page count;
- confirm text extraction where expected;
- render **every page at 200 dpi**;
- visually inspect every page;
- inspect every mathematical figure at final size;
- check clipping, overlap, broken glyphs, malformed math, missing figures, tiny labels, illegible captions, and page-break damage;
- record SHA-256 of the exact delivered PDF.

If a figure is essential to a proof or question, a missing/broken figure is a **content failure**, not a cosmetic defect.

---

## 19. Recommended output package

A robust study-guide package should contain:

```text
README.md
<Subject>_Study_Guide_vN.md
Question_to_Method_Matrix.md
Advanced_Worked_Bridges.md
Appendix_A_<supplied-corpus>.md
Appendix_A_Hints.md              # optional if hints are not inline
Appendix_B_<mixed-audit-set>.md
Quick_Reference_1or2pp.md
Self_Sufficiency_Audit.md
Sources_and_Citations.md
QA.md
PDFs/<Subject>_IOQM_Grade9_Study_Guide_vN.pdf
```

Domain-specific profiles may add figure manifests, diagram sources, or specialized method maps.

---

## 20. Acceptance principle

A guide is not self-sufficient because it:

- lists every formula;
- mentions every syllabus heading;
- contains many solved examples;
- has a long Appendix A;
- looks professional as a PDF.

It is self-sufficient only when a half-prepared learner can move from:

**problem wording -> recognized structure -> legal first step -> executable method -> correct check**

without relying on an unnamed trick that exists only in the teacher's head.
