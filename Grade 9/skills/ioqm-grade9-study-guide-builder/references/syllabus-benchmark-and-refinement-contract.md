# IOQM Grade 9 Study-Guide Syllabus, Benchmark and Refinement Contract

## Purpose

This reference is the shared contract for the `ioqm-grade9-study-guide-builder` prompts.

The intended learner is a Grade 9 student with roughly 50% prior knowledge: routine school facts may be familiar, but method recognition, theorem legality, and Olympiad execution cannot be assumed.

The syllabus below is a user-supplied scope reference. It is not asserted here to be an official Grade-9-only IOQM syllabus. Repository official/validated source maps remain the authority for historical IOQM claims.

## Syllabus reference

### Algebra

Inequalities, Progressions (A.P, G.P, H.P), Theory of indices, System of linear equations, Theory of equations, Binomial theorem and properties of binomial coefficients, Complex Numbers, Polynomials in one and two variables, Functional equations, Sequences.

### Plane Geometry

Triangles, quadrilaterals, circles and their properties; standard Euclidean constructions; concurrency and collinearity (Theorems of Ceva and Menelaus); basic trigonometric identities, compound angles, multiple and submultiple angles, general solutions, sine rule, cosine rule, properties of triangles and polygons, Coordinate Geometry (straight line, circle, conics, 3-D geometry), vectors.

### Combinatorics

Basic enumeration, pigeonhole principle and its applications, recursion, elementary graph theory.

### Number Theory

Divisibility theory in the Integers (The Division Algorithm, the Greatest Common Divisor, The Euclidean Algorithm, The Diophantine Equation ax + by = c), Fundamental Theorem of Arithmetic, Basic properties of congruence, Linear congruences, Chinese Remainder Theorem, Fermat's Little Theorem, Wilson's Theorem, Euler's Phi function and Euler's generalisation of Fermat's Theorem, Pythagorean triples (definition and properties), Diophantine equations.

## Benchmark hierarchy

Use these as internal quality comparators, not ground truth and not copy templates.

1. `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`
2. `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/Quadratics_Assimilation_Benchmark_v2.pdf`
3. `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/README.md`
4. `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Combinatorics_Study_Guide_v2.md`
5. `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Self_Sufficiency_Audit.md`
6. `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Advanced_Worked_Bridges.md`
7. `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Quick_Reference_2pp.md`
8. `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Appendix_B_20_IOQM_Style_Mock.md`
9. `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Sources_and_Citations.md`
10. `Grade 9/skills/ioqm-grade9-study-guide-builder/SKILL.md`

The Quadratics benchmark establishes the quality bar for learner assimilation and production. The Combinatorics v2 package is the concrete benchmark for the later rethink: question-by-question self-sufficiency auditing, orphan-method repair, a separate source ledger, Appendix B, a compact memory sheet, and a second audit that is allowed to fail the first draft.

## Mandatory work process

### Stage 0 - Read authority and classify inputs

Read the relevant `ALG-*`, `NT-*`, or `GEO-*` repository topic packages, the IOQM architecture/source-provenance files, the benchmark files above, and every supplied attachment.

Classify each input as:
- official/validated authority;
- repository canonical teaching material;
- comparison/practice material;
- internal quality benchmark.

Never silently promote comparison material into official authority.

### Stage 1 - Build the syllabus/subtopic map before prose

Map the supplied syllabus scope and repository topic ownership into a learner dependency order.

For every syllabus item mark:
- explicitly taught;
- taught under a different name;
- prerequisite/bridge only;
- out of Grade-9 guide scope for this edition;
- missing and needing a new bridge.

Do not merely copy the order of a coaching handout or question compilation.

### Stage 2 - Inventory every supplied question

For each supplied question record:
- question number;
- mathematical surface;
- primary subtopic;
- secondary prerequisite;
- recognition cue;
- first useful mathematical line;
- complete method required;
- theorem/formula legality conditions;
- likely misconception;
- whether the current draft teaches enough to execute the method.

This matrix is mandatory even if there are 50+ questions.

### Stage 3 - Draft the teacher-style guide

Write for a student who knows about half the background.

For every substantial subtopic include:
- what you likely remember;
- the missing Olympiad link;
- why the method/theorem works;
- one non-identical worked example;
- "What should I notice?";
- "Try this first";
- a near-miss or competing method;
- common mistakes;
- legality/domain/hypothesis checks;
- practice references.

Avoid internal production jargon in the learner document.

### Stage 4 - First self-sufficiency audit: orphan-method test

Distrust the first draft.

For every supplied question ask:
"Could a half-prepared student execute this from the guide, or did I merely name the trick?"

Fail and repair any question that needs an unstated theorem, formula, transformation, construction, counting device, representation, special case, or hidden algebraic/geometric step.

Create worked bridges for methods that are still too compressed.

### Stage 5 - Second audit: grouping and learner flow

Revisit the chapter grouping itself.

Ask:
- Are prerequisites introduced before use?
- Are two visually similar methods explicitly contrasted?
- Are advanced methods introduced only after simpler ones?
- Does the guide tell the student when *not* to use a method?
- Does the sequence suit a student with about 50% prior knowledge?
- Are any source-driven headings pedagogically artificial?

Regroup and rewrite if needed. Do not preserve the first taxonomy merely because it already exists.

### Stage 6 - Broader-syllabus audit

The supplied question set may underrepresent canonical skills.

Compare the guide against:
- the user-supplied syllabus above;
- repository `03_Main_Topics`;
- validated historical IOQM mechanism/source maps.

Add missing foundational bridges where appropriate. If a syllabus item is intentionally not developed, state the scope boundary instead of pretending coverage.

### Stage 7 - Appendix A

Reproduce the supplied questions as a clean question bank:
- every question exactly once;
- questions only;
- no worked solutions;
- no tips;
- no source commentary;
- preserve all conditions/figures needed to solve;
- answers only after the final Appendix A question.

Keep provenance in `Sources_and_Citations.md`.

### Stage 8 - Appendix B

Create 20 fresh questions based on verified previous-year IOQM mechanisms and/or clearly labelled IOQM-style author-created mocks.

Rules:
- do not fabricate historical provenance;
- cover the important syllabus/subtopics, including material underrepresented in Appendix A;
- no method labels or hints in the question text unless specifically requested;
- answers only after B20;
- independently solve every question before promotion;
- record the mathematical audit.

### Stage 9 - Quick reference

Create a 1-2 page memory sheet containing only material worth rapid recall:
- formulas;
- theorem hypotheses;
- standard identities;
- compact decision cues;
- common special values;
- "do not forget" checks.

It is a memory aid, not a miniature textbook.

### Stage 10 - Citation and source audit

Create `Sources_and_Citations.md`.

Cite:
- official historical paper/key IDs where used;
- repository source maps/stable IDs;
- external comparison material where useful;
- benchmark files.

Preserve uncertainty. Never attach an official label to a reconstructed or coaching-source problem.

### Stage 11 - Final static self-sufficiency audit

Create `Self_Sufficiency_Audit.md` with a row for every supplied question.

A question passes only if the guide provides:
1. prerequisite refresh;
2. recognition cue;
3. first useful step;
4. execution bridge;
5. legality/error check;
6. answer-free practice isolation.

Use:
`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n`

only for document-level coverage. It is not a classroom solve-rate claim.

### Stage 12 - PDF production

The final student deliverable is PDF.

Before creating or editing the final PDF, read:
`/home/oai/skills/pdfs/SKILL.md`

Follow its render-first/create/re-render/preflight workflow. For a long text-heavy guide, prefer the text-document authoring route recommended by the PDF skill, then convert to PDF.

Final repository location:
`Grade 9/Mathematics/IOQM/04_Study_Guides/<DOMAIN>_v1/PDFs/`

Required final student PDF:
`<DOMAIN>_IOQM_Grade9_Study_Guide_v1.pdf`

The PDF should include the study guide, quick reference, Appendix A, Appendix B, and student-appropriate source notes. Keep detailed reviewer QA/source ledgers as repository companion files if they would clutter the student edition.

PDF gates:
- opens successfully;
- not encrypted;
- text extractable unless a source figure requires otherwise;
- no clipped text, overlaps, black squares, broken glyphs or malformed math;
- every page rendered at 200 dpi and visually inspected;
- page count recorded;
- SHA-256 recorded;
- exact final binary committed;
- no workflow is required.

### Stage 13 - Final comparison and refinement

Compare the finished guide against both benchmark families:
- Quadratics Assimilation v2;
- Combinatorics Study Guide v2.

Explicitly answer:
- What did the first draft miss?
- What was added after the question-by-question audit?
- What was regrouped for the 50%-knowledge learner?
- Which syllabus items required new bridges?
- Which items remain scope-limited?
- Is Appendix A completely supported by the guide?
- Does Appendix B test breadth without leaking answers?
- Is the quick-reference sheet genuinely memorization-oriented?
- Are citations/provenance adequate?
- Has the final PDF passed page-by-page visual QA?

Do not call the work complete until this revisit is documented.