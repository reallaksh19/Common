# COPY-PASTE PROMPT — IOQM Grade 9 Algebra Study Guide

You are the lead teacher-author for a Grade 9 IOQM Algebra study guide. Build a self-sufficient student guide for a learner with roughly 50% prior knowledge: they may remember routine school formulas and solve standard textbook exercises, but they cannot be assumed to recognize Olympiad structures or know advanced tricks without teaching.

Your task is not to produce a formula list or a set of solved questions. Your task is to create a teacher-quality study guide that allows such a learner to move from:

**problem wording -> recognize the algebraic structure -> choose a legal method -> write the first useful line -> execute the method -> check the result.**

## Repository and skill authority

Repository: `reallaksh19/Common`

Read first:

1. `Grade 9/skills/ioqm-grade9-study-guide-builder/SKILL.md`
2. `Grade 9/skills/ioqm-grade9-study-guide-builder/references/syllabus-benchmark-and-refinement-contract.md`
3. `Grade 9/Mathematics/IOQM/README.md`
4. all relevant algebra packages under:
   - `Grade 9/Mathematics/IOQM/03_Main_Topics/ALG-*`
5. relevant number-theory interfaces when an algebra problem has integer restrictions:
   - `Grade 9/Mathematics/IOQM/03_Main_Topics/NT-*`

Read every supplied Algebra attachment/question/tip file completely before writing.

Treat supplied coaching notes, compilations, videos, routines, worksheets, or reconstructed questions as **comparison/practice material unless independently established as official authority**. Do not let them override validated repository sources.

## Syllabus scope to cover and audit

Use the following supplied Algebra syllabus as a scope reference:

- Inequalities
- Progressions: A.P., G.P., H.P.
- Theory of indices
- System of linear equations
- Theory of equations
- Binomial theorem and properties of binomial coefficients
- Complex Numbers
- Polynomials in one and two variables
- Functional equations
- Sequences

Also compare against the existing repository Algebra topics so that important IOQM Grade 9 bridges already built in the repo are not lost, including identities/factorization, roots and Vieta, radicals, logarithms where relevant, floor/ceiling/discrete functions where relevant, and integer admissibility checks.

Do **not** pretend every advanced syllabus word must receive equal depth. For each item mark it as:
- fully taught in this guide;
- prerequisite/bridge coverage;
- taught under another heading;
- intentionally scope-limited for Grade 9;
- missing and requiring repair.

In particular, do not silently claim full complex-number, two-variable polynomial, or advanced progression coverage if the source evidence and Grade-9 architecture do not support it. State the boundary and teach the amount needed for the supplied questions and verified IOQM-style mechanisms.

## Benchmarks — use as quality comparators, not ground truth

Inspect:

- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`
- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/Quadratics_Assimilation_Benchmark_v2.pdf`

Also inspect the later self-sufficiency benchmark created in this work:

- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/README.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Combinatorics_Study_Guide_v2.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Self_Sufficiency_Audit.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Advanced_Worked_Bridges.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Quick_Reference_2pp.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Appendix_B_20_IOQM_Style_Mock.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Sources_and_Citations.md`

Do not copy their wording, exercises, typography, or layout. Copy only the rigor of the process: missing-link repair, method contrasts, question-by-question audit, willingness to fail the first draft, citations/provenance, and page-by-page PDF QA.

## Work process — execute in full

### 1. Source and syllabus inventory

Before prose, create a syllabus coverage table.

At minimum include:
- syllabus item;
- repository owner/topic;
- current student prerequisite;
- required Grade-9 bridge;
- source evidence;
- intended depth in this guide.

Then list all supplied questions.

### 2. Question-to-method matrix

For **every supplied question**, record:

- exact question number;
- surface wording;
- primary algebra subtopic;
- prerequisite;
- recognition cue;
- first useful mathematical line;
- full method required;
- domain/reversibility/admissibility conditions;
- likely half-knowledge mistake;
- whether the current guide teaches enough to finish.

Examples of distinctions the matrix must catch:

- identity vs equation;
- factorization vs expanding;
- implication vs equivalence after squaring or clearing denominators;
- equality condition in an inequality;
- Vieta vs direct root solving;
- recurrence vs closed-form sequence manipulation;
- functional-equation substitution choice;
- exponent normalization vs taking logs;
- radical domain and extraneous roots;
- polynomial remainder/factor theorem vs coefficient comparison;
- system of equations vs symmetric substitution;
- AP/GP structure vs an arbitrary sequence;
- binomial coefficient identity vs numerical expansion.

### 3. Design the student chapter order

Do not copy the attachment order.

Start from a dependency order suitable for 50% prior knowledge. A strong default is:

1. algebraic language, identities and factorization;
2. equations, equivalence and candidate checking;
3. linear systems and symmetric substitutions;
4. inequalities, bounds and equality conditions;
5. polynomials, roots, Vieta and remainder/factor ideas;
6. progressions and sequences;
7. binomial theorem and binomial coefficients;
8. exponents/indices, radicals and logarithmic bridges where needed;
9. functional equations;
10. discrete/floor-ceiling or integer filters where required;
11. introductory complex-number or two-variable-polynomial bridges only if genuinely needed by the syllabus/question set;
12. mixed method selection.

Regroup if your question audit shows a better pedagogical sequence.

### 4. Write the first draft like a teacher

For every substantial subtopic include:

- **What you probably remember**
- **The missing Olympiad link**
- **Why this works**
- a non-identical worked example
- **What should I notice?**
- **Try this first**
- a close contrast: when a similar-looking method is wrong
- common mistakes
- legality/domain/equality checks
- a short practice pointer

Use ordinary teacher language. Do not use learner-facing internal terms such as wave, microstream, H0/H1/H2/H3, transfer gate, interface owner, or control plane.

### 5. Fail the first draft if necessary — orphan-method audit

For every supplied question ask:

> Could a half-prepared Grade 9 student execute the needed method from the guide, or did I merely name the method?

Examples of Algebra orphan failures:

- “use Vieta” without teaching how a target expression is rebuilt from sum/product of roots;
- “apply AM-GM” without positivity and equality conditions;
- “square both sides” without explaining the implication/extraneous-root issue;
- “use the binomial theorem” without showing coefficient indexing;
- “try x=0,1” in a functional equation without explaining why those substitutions are strategic;
- “let t=x+1/x” without explaining when and why the substitution closes;
- “use logarithms” without domain/base restrictions;
- “compare coefficients” without establishing a polynomial identity;
- “use AP/GP” without defining the parameterization that reduces the variables.

Repair every orphan with an executable worked bridge.

### 6. Revisit the grouping itself

After repairing methods, challenge your own chapter structure.

Check:
- prerequisite before use;
- simple representation before advanced representation;
- equations before transformations that can create extraneous roots;
- polynomial/root structure before advanced functional substitution when needed;
- AP/GP basics before mixed progression identities;
- theorem statements before theorem use;
- explicit distinction between school manipulation and Olympiad method selection.

If the first grouping is not right for a 50%-prepared learner, regroup and rewrite. Document what changed.

### 7. Broader syllabus audit

Compare the revised guide with the supplied Algebra syllabus and all `ALG-*` repository material.

Identify:
- areas fully covered;
- areas represented by a short bridge;
- areas absent from the supplied questions but important enough to add;
- advanced areas intentionally scope-limited.

Do not create fake completeness. If complex numbers or two-variable polynomial theory is only introductory, say so.

### 8. Appendix A — supplied questions

Create a clean Appendix A:

- reproduce **all supplied Algebra questions**;
- each appears exactly once;
- questions only;
- no worked solutions;
- no tips;
- no source commentary;
- preserve necessary diagrams/conditions;
- answers only after the final Appendix A question.

Do not insert method labels beside the questions.

Create a separate `Sources_and_Citations.md` for provenance.

### 9. Appendix B — 20-question audit mock

Create **20 fresh Algebra questions** modeled on verified previous-year IOQM mechanisms and clearly labelled author-created IOQM-style items when not historical.

The mock should sample the revised guide, for example:
- identities/factorization;
- systems;
- inequalities/equality cases;
- polynomial/Vieta;
- AP/GP/sequences;
- binomial coefficients;
- exponents/radicals;
- functional equations;
- one discrete/integer-filter problem;
- any syllabus bridge actually taught.

No hints/method labels in question text.

Answers only after B20.

Independently solve all 20 and record the audit.

### 10. Quick-reference handout

Create a **1-2 page Algebra Quick Reference**.

Include only high-value memory material, such as:
- standard identities and factor patterns;
- discriminant/root facts;
- Vieta;
- AP/GP core formulas;
- binomial theorem/coefficient facts;
- exponent/index laws with legality;
- inequality conditions and equality cases;
- radical/log domain rules where taught;
- polynomial factor/remainder facts;
- candidate-check rule;
- functional-equation substitution cues.

Do not include full worked solutions.

### 11. Citations and provenance

Create `Sources_and_Citations.md`.

Cite wherever possible:
- official/validated historical IOQM IDs and keys;
- repository source maps;
- comparison attachments;
- benchmark files.

Preserve uncertainty. Never label a reconstructed coaching problem as an official IOQM item unless independently established.

### 12. Self-sufficiency audit

Create a row for every Appendix A question.

A question passes only if the guide gives:

1. prerequisite refresh;
2. recognition cue;
3. first useful line;
4. execution bridge;
5. legality/error check;
6. answer-free question practice.

Use:
`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n`

only if all pass.

This is not evidence of classroom solve rate, timing, retention, or qualification probability.

### 13. PDF is the final output

Before PDF work, read:
`/home/oai/skills/pdfs/SKILL.md`

The final student deliverable must be:

`Grade 9/Mathematics/IOQM/04_Study_Guides/Algebra_v1/PDFs/Algebra_IOQM_Grade9_Study_Guide_v1.pdf`

Because this is a long text-heavy guide, follow the PDF skill's recommended authoring route (typically document authoring followed by PDF conversion) rather than forcing fragile manual PDF layout.

The final PDF should integrate:
- student study guide;
- quick-reference handout;
- Appendix A;
- Appendix B;
- student-appropriate citations/source notes.

Keep detailed reviewer QA/source ledgers as companion repository files if needed.

Mandatory PDF QA:
- preflight;
- render every page at 200 dpi;
- visually inspect every page;
- no clipping/overlap/broken glyphs/black squares/malformed mathematics;
- record page count;
- record SHA-256;
- commit the exact final PDF binary;
- no GitHub Actions workflow is required.

## Required repository package

Create under:

`Grade 9/Mathematics/IOQM/04_Study_Guides/Algebra_v1/`

At minimum:

- `README.md`
- `Algebra_Study_Guide_v1.md`
- `Quick_Reference_2pp.md`
- `Appendix_A_<source-set>.md`
- `Appendix_B_20_IOQM_Style_Mock.md`
- `Self_Sufficiency_Audit.md`
- `Sources_and_Citations.md`
- `QA.md`
- `PDFs/Algebra_IOQM_Grade9_Study_Guide_v1.pdf`

## Final revisit/refinement report

Before completion, explicitly document:

1. what the first draft missed;
2. which supplied questions exposed those gaps;
3. what methods were initially orphaned;
4. what was added to make them executable;
5. what subtopics were regrouped for a 50%-knowledge learner;
6. which syllabus items required new bridges;
7. which syllabus items remain intentionally scope-limited;
8. whether Appendix A is now fully supported by the guide;
9. whether Appendix B tests the whole guide fairly;
10. whether the quick reference contains only memorization-worthy material;
11. whether citations/provenance are adequate;
12. whether the final PDF passed structural and page-by-page visual QA.

Do not mark the work complete merely because all files exist. Complete it only after the revision loop and exact-PDF QA are closed.