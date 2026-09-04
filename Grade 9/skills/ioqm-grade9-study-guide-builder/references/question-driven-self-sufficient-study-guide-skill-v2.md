# Question-Driven Self-Sufficient Study Guide Skill v2

## Status and role

This document is a generalized production contract that supplements `../SKILL.md`.

It captures the workflow required to turn a supplied Olympiad-style problem corpus into a self-sufficient Grade 9 study guide:

> corpus custody -> question-to-method matrix -> prerequisite regrouping -> Draft 1 -> orphan-method audit -> visual-pedagogy audit -> worked-bridge repair -> progressive local hints -> self-sufficiency audit -> appendices -> inspected PDF.

Use this contract for Algebra, Number Theory, Geometry, Combinatorics, or another Grade 9 IOQM domain.

A polished PDF is not evidence that the guide is pedagogically complete.

---

## 1. Learner model

Assume a learner with roughly 50% prior knowledge.

The learner may remember school formulas and solve routine exercises, but may not reliably:

- recognize an Olympiad structure from wording;
- distinguish nearby methods;
- choose a strategic substitution or construction;
- remember legality conditions;
- detect irreversible operations;
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
- willingness to reject Draft 1;
- question-by-question self-sufficiency;
- source discipline;
- visual pedagogy;
- final PDF quality.

Do not copy wording, exercises, typography, or diagrams.

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
- current support status: `PASS`, `PARTIAL`, or `FAIL`.

### Teaching-obligation rule

Every supplied question creates a teaching obligation.

If a required method does not appear in the guide, the guide is incomplete.

If it appears only as a formula or one-line cue, the guide is still incomplete.

---

## 5. Stable skill and bridge IDs

Every reusable method taught in the guide should receive a stable ID.

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

Hints should normally display both a stable ID and a readable skill name, for example:

> `GEO-CENTROID-01 · Centroid 2:1`

This is better than an unstable chapter/page number alone.

Stable IDs allow:

- Appendix A hints to retrieve prior learning;
- audit rows to verify real coverage;
- quick-reference links back to teaching;
- future chapter reordering without breaking references;
- difficult questions to receive help without printing a disguised solution.

---

## 6. Syllabus and scope audit

Compare the supplied corpus with the declared syllabus, existing domain packages, relevant cross-domain interfaces, and verified historical mechanism maps.

For each syllabus item mark one of:

- `FULLY_TAUGHT`;
- `BRIDGE_LEVEL`;
- `TAUGHT_UNDER_ANOTHER_HEADING`;
- `INTENTIONALLY_SCOPE_LIMITED`;
- `MISSING_AND_REQUIRES_REPAIR`.

Do not fake completeness.

A topic appearing only on a memory sheet is not automatically fully taught.

---

## 7. Dependency-based learner order

Do not copy the source question order unless it is pedagogically strong.

A robust default dependency order is:

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

Use teacher/student language, not internal production jargon.

---

## 9. Orphan-method audit

For every supplied question ask:

> Could a learner with roughly 50% prior knowledge actually execute this method from the guide, or did the guide merely name the trick?

A method is orphaned if the learner must already know an unstated move.

Examples:

- “use Vieta” without rebuilding the target expression;
- “apply AM-GM” without positivity and equality conditions;
- “draw an auxiliary line” without explaining what relation it should create;
- “use Burnside” without fixed-set counting;
- “square both sides” without extraneous-root handling;
- “use a recurrence” without defining state or proving recurrence;
- “use coordinates” without explaining the coordinate placement.

Repair every orphan with stronger chapter teaching or a dedicated Advanced Worked Bridge.

No `PARTIAL` or `FAIL` question may remain before final PDF generation.

---

## 10. Visual-pedagogy audit

Figures are teaching tools, not decoration.

For every chapter and supplied question ask:

> Would a figure, graph, number line, table, construction, state diagram, or schematic materially reduce cognitive load or reveal structure that prose alone hides?

If yes, include it.

### Geometry — visuals are strongly expected

Use construction-quality figures whenever reasoning depends on:

- collinearity or concurrency;
- cyclicity;
- angle relations;
- similarity or homothety;
- equal lengths;
- loci;
- reflections or rotations;
- auxiliary constructions;
- coordinate placement;
- area decomposition;
- moving-point or extremal geometry.

A diagram-dependent theorem or worked example should not force the learner to construct the entire picture mentally.

For Geometry Appendix A, local hints should often interact directly with the figure, for example:

> **H1 · Notice** Mark the equal base angles created by the two equal-length conditions.

### Algebra — visuals only when they clarify structure

Useful visuals include:

- root-count and tangent-root graphs;
- sign/domain number lines;
- function-composition maps;
- finite-difference tables;
- recurrence/state evolution;
- feasible-region or smoothing schematics.

Do not add decorative graphs when symbols are clearer.

### Combinatorics

Useful visuals include graph models, block/gap schematics, state diagrams, circular arrangements, matching diagrams, and small symmetry models.

### Number theory

Useful visuals may include residue cycles, exponent grids, valuation tables, and lattice/Diophantine-region sketches when they materially help.

### Figure quality rules

Prefer author-created mathematical figures over stock imagery.

Every figure should:

- have readable labels at final PDF size;
- use notation consistent with the text;
- have a short caption or nearby explanation;
- avoid leaking a hidden construction or answer in answer-free practice;
- preserve mathematical geometry unless marked `not to scale`;
- avoid clutter;
- be cited if externally sourced;
- be inspected in the final 200-dpi render.

If a problem requires a figure to preserve mathematical conditions, Appendix A/B must include it.

---

## 11. Advanced Worked Bridges

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

The purpose is transfer, not rehearsal of the exact Appendix A problem.

---

## 12. Appendix A — supplied corpus with adaptive local hints

Appendix A preserves source custody.

Rules:

- every supplied question appears exactly once;
- preserve all mathematical conditions and required figures;
- no worked solution in the problem body;
- no source commentary in the problem body;
- answer key only after the final question set / hint area according to the chosen layout;
- provenance remains in a separate source ledger;
- do not invent continuation numbering when the source ends.

### Default student-facing layout

Keep the compact problem-set rhythm.

The preferred static-PDF layout is:

```text
Qn. Problem title / statement
[small relevant figure if useful]

H1 👀 Notice     recognition clue
H2 ↩ Recall     prior skill ID + readable skill name
H3 ✏ Start      first mathematical move / decisive setup
```

The hints should appear as thin, visually quiet horizontal strips directly under the question or figure.

The question and figure remain visually dominant.

### Adaptive hint depth

Not every problem needs three hints.

Use approximately:

- routine transfer: `NONE` or `H1`;
- easy: `H1`;
- medium: `H1-H2`;
- hard: `H1-H3`.

A strong default page rhythm is 2–3 questions per page where legibility permits.

Do not force one hard question onto one page merely because it has three hints.

### Hint length limits

Keep hints compact:

- **H1 · Notice:** usually one sentence;
- **H2 · Recall:** usually one sentence;
- **H3 · Start:** at most two short sentences/equations.

If a hint requires a paragraph, the material belongs in the main teaching or an Advanced Worked Bridge.

### H1 — recognition only

Purpose: identify the relevant structure without solving it.

Example:

> **H1 · Notice** Both `x+y` and `xy` appear. This is a symmetric two-variable structure.

H1 should answer:

- What should I notice?
- Which family is relevant?

### H2 — retrieve prior learning

Purpose: make the student reopen a previously learned skill instead of depending on a more explicit hint.

Preferred form:

> **H2 ↩ Recall `ALG-SYM2-01 · Sum-product substitution`** Use the same compression idea as in the earlier worked example.

For Geometry:

> **H2 ↩ Recall `GEO-CENTROID-01 · Centroid 2:1`** Mark the ratio before opening H3.

H2 is especially valuable on hard questions because it trains retrieval.

### H3 — first mathematical move

Purpose: unblock execution without becoming a solution.

Example:

> **H3 ✏ Start** Set `s=x+y`, `p=xy`; translate the two conditions into equations in `s,p`.

For Geometry:

> **H3 ✏ Start** Let `∠A=α`, `∠B=β`; use the right-angle relation before chasing the marked equal angles.

H3 should not reveal the final answer.

### Progressive-use instruction

At the start of Appendix A include a short learner instruction such as:

> Try each problem first. Open H1 only if you cannot identify the structure. Use H2 if you know the topic but cannot retrieve the earlier skill. Use H3 only if you still cannot write the first mathematical move.

A static PDF cannot truly hide H2/H3, so use visual hierarchy: H1 most noticeable, H2 quieter, H3 quietest.

### Stable reference rule

H2 should normally reference both:

- a stable skill/bridge ID; and
- a readable skill name.

Avoid bare page numbers as the only reference.

### Geometry-specific default

For diagram-driven Geometry, local hints under the problem/figure are the preferred default because the student often needs to act on the diagram immediately.

H1 may ask the learner to mark equal angles, equal lengths, cyclic points, a midpoint, a tangent relation, or a target auxiliary construction.

### Fallback: consolidated Hint Bank

Use a separate Hint Bank only when local hints would:

- overcrowd the page;
- make a large diagram unreadable;
- reveal too much by proximity;
- disrupt a heavily visual layout.

The consolidated bank is a fallback, not the default.

---

## 13. Appendix B — approximately 20 audit problems

Appendix B should test the revised guide beyond the supplied corpus.

Rules:

- source historical items accurately;
- label author-created items clearly;
- sample methods actually taught;
- include underrepresented canonical methods where useful;
- no solution beside the question;
- use the same adaptive local H1-H3 system on difficult items when beneficial;
- answer key only after the final problem;
- independently recompute every answer.

Create an Appendix B method-coverage table for reviewer QA.

---

## 14. Appendix C / Quick Reference

Create a 1–2 page memory helper when useful.

Include only high-value recall material:

- core formulas;
- compact method triggers;
- theorem legality conditions;
- equality conditions;
- common transforms;
- frequently used small patterns;
- final pre-submit checks;
- stable skill IDs for deeper review where space permits.

Do not put full worked solutions in the helper.

A topic appearing only in Appendix C does not count as fully taught.

---

## 15. Citation and provenance audit

Keep provenance separate from clean question presentation.

Preferred locations:

- `Sources_and_Citations.md`;
- reviewer manifest;
- stable historical ID tables;
- chapter endnotes where useful.

Preserve uncertainty.

Never convert:

- identified practice problem -> confirmed official lecture question;
- reconstructed wording -> official wording;
- answer-key agreement -> proof of source identity.

---

## 16. Final self-sufficiency audit

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
9. H2 references a previously taught skill/bridge where applicable.

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

Do not override this gate because the current draft looks polished.

---

## 18. PDF production and QA

Before PDF work, read the environment's required PDF-production skill.

Mandatory final QA:

- preflight the exact binary;
- confirm page size and page count;
- confirm text extraction where expected;
- render every page at 200 dpi;
- visually inspect every page;
- inspect every mathematical figure at final size;
- verify H1/H2/H3 strips remain readable but visually quiet;
- check clipping, overlap, broken glyphs, malformed math, missing figures, tiny labels, illegible captions, and page-break damage;
- record SHA-256 of the exact delivered PDF.

If a figure is essential to a proof or question, a missing/broken figure is a content failure, not a cosmetic defect.

---

## 19. Recommended output package

```text
README.md
<Subject>_Study_Guide_vN.md
Question_to_Method_Matrix.md
Advanced_Worked_Bridges.md
Appendix_A_<supplied-corpus>.md
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

A guide is not self-sufficient because it lists every formula, mentions every syllabus heading, contains many solved examples, has a large Appendix A, or looks professional as a PDF.

It is self-sufficient only when a half-prepared learner can move from:

**problem wording -> recognized structure -> legal first step -> executable method -> correct check**

without relying on an unnamed trick that exists only in the teacher's head.
