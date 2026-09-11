# COPY-PASTE PROMPT — IOQM Grade 9 Number Theory / Number System Study Guide

You are the lead teacher-author for a Grade 9 IOQM Number Theory / Number System study guide. Build a self-sufficient guide for a student with roughly 50% prior knowledge: they may remember school divisibility tests and basic prime factorization, but cannot be assumed to recognize Olympiad number-theory structures or theorem legality without teaching.

The guide must help the learner move from:

**problem wording -> identify the arithmetic structure -> choose the right representation/theorem -> write the first useful line -> execute -> verify integrality/congruence conditions.**

## Repository and skill authority

Repository: `reallaksh19/Common`

Read first:

1. `Grade 9/skills/ioqm-grade9-study-guide-builder/SKILL.md`
2. `Grade 9/skills/ioqm-grade9-study-guide-builder/references/syllabus-benchmark-and-refinement-contract.md`
3. `Grade 9/Mathematics/IOQM/README.md`
4. all relevant number-theory packages under:
   - `Grade 9/Mathematics/IOQM/03_Main_Topics/NT-*`
5. relevant algebra/combinatorics packages where they provide legitimate bridges rather than duplicate ownership.

Read every supplied Number Theory / Number System question, note, tip, coaching source, or worksheet completely.

Treat non-official material as comparison/practice material unless independently verified as official authority.

## Syllabus scope to cover and audit

Use this supplied Number Theory syllabus as the scope reference:

- Divisibility theory in the Integers
- The Division Algorithm
- Greatest Common Divisor
- Euclidean Algorithm
- the Diophantine equation `ax + by = c`
- Fundamental Theorem of Arithmetic
- basic properties of congruence
- linear congruences
- Chinese Remainder Theorem
- Fermat's Little Theorem
- Wilson's Theorem
- Euler's Phi function
- Euler's generalisation of Fermat's Theorem
- Pythagorean triples: definition and properties
- Diophantine equations

Also retain the repository's Grade-9 IOQM number-theory bridges already built, including:
- Euclid's Lemma;
- Bézout/extended Euclid;
- prime valuations/divisor structure;
- digit/place-value/base methods;
- consecutive sums/odd-divisor characterization;
- integer restrictions and factorization;
- residue-cycle decision making.

For each syllabus item mark:
- fully taught;
- bridge-level taught;
- taught under another heading;
- intentionally scope-limited;
- missing and requiring repair.

Do not silently claim advanced CRT, Wilson, or general Diophantine mastery if the actual guide only gives a first-use Grade-9 bridge. State the depth honestly.

## Benchmarks — quality comparators only

Inspect:

- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`
- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/Quadratics_Assimilation_Benchmark_v2.pdf`

Also inspect:

- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/README.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Combinatorics_Study_Guide_v2.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Self_Sufficiency_Audit.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Advanced_Worked_Bridges.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Quick_Reference_2pp.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Appendix_B_20_IOQM_Style_Mock.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Sources_and_Citations.md`

Use these to match the rigor of explanation, self-sufficiency audit and production QA, not their content or layout.

## Work process — execute in full

### 1. Syllabus/repository map

Create a table connecting each supplied syllabus item to:
- repository owner topic;
- prerequisite;
- exact Grade-9 theorem/bridge needed;
- evidence/source;
- intended guide depth.

### 2. Inventory every supplied question

For every question record:
- number;
- surface;
- primary subtopic;
- prerequisite;
- recognition cue;
- first useful mathematical line;
- full method;
- theorem hypotheses;
- integrality/positivity/coprimality/parity restrictions;
- likely half-knowledge mistake;
- current-guide sufficiency.

Important distinctions include:

- divisibility vs congruence;
- gcd reduction vs prime factorization;
- existence of `ax+by=c` vs finding all solutions;
- Euclid's Lemma vs Euclidean algorithm;
- Fermat/Euler vs a shorter residue cycle;
- Euler's theorem requiring coprimality;
- CRT requiring compatible congruences/moduli treatment;
- Wilson only for prime-modulus characterization/use;
- valuation counting vs divisor enumeration;
- digit/place-value structure vs brute force;
- Pythagorean triple generation vs merely checking `a^2+b^2=c^2`;
- general Diophantine equation vs a factorization trick.

### 3. Design a 50%-knowledge chapter order

A strong default:

1. divisibility language and Division Algorithm;
2. gcd/lcm and Euclidean Algorithm;
3. Euclid's Lemma and Fundamental Theorem of Arithmetic;
4. Bézout and linear Diophantine equation `ax+by=c`;
5. congruences and residue arithmetic;
6. linear congruences and modular inverses;
7. CRT as a controlled bridge;
8. powers modulo `n`: cycles, Fermat, Euler, phi;
9. Wilson's theorem as a prime-modulus tool/bridge;
10. prime factorization, valuations, divisor functions and perfect powers;
11. Pythagorean triples;
12. broader Diophantine equations and integer factorization restrictions;
13. digits, place value, bases and digit divisibility;
14. consecutive sums and odd-divisor structure;
15. mixed method selection.

Regroup if the supplied question matrix demands a better dependency order.

### 4. Write the first draft like a teacher

Each major theorem/subtopic should include:

- what you probably remember;
- exact statement;
- why it is true at an accessible Grade-9 level;
- hypotheses;
- non-identical worked example;
- near-miss where the theorem is illegal or inefficient;
- **What should I notice?**
- **Try this first**
- common mistakes;
- practice references.

Do not write “apply Euler”, “use CRT”, “by Wilson”, “use valuations”, or “solve the Diophantine equation” without teaching the actual execution path.

### 5. Orphan-method audit — distrust the first draft

For every supplied problem ask whether a student can finish using only the guide.

Typical Number Theory orphan failures:

- “run Euclid” without showing backward substitution for Bézout;
- “Euler's theorem” without defining `phi(n)` or checking `gcd(a,n)=1`;
- “use CRT” without solving the pair of congruences;
- “Wilson” without identifying the prime-modulus condition;
- “valuation” without explaining `v_p` and how min/floor conditions work;
- “Pythagorean triples” without the primitive parameterization or parity/coprime conditions when needed;
- “factor the Diophantine equation” without showing why the factors are integers and how signs/divisors are enumerated;
- “digit sum” without writing place value or congruence.

Repair every orphan with a worked bridge.

### 6. Revisit grouping and method choice

Challenge the first chapter organization.

For a half-prepared learner, ensure:
- Euclid before Bézout;
- basic congruence before inverses/CRT;
- power cycles before presenting Euler as a hammer;
- prime factorization before valuations/divisor functions;
- Pythagorean checking before parameterization;
- existence criteria before full Diophantine families;
- digit/place-value tools after modular foundations.

Explicitly teach **when a simpler method beats a stronger theorem**.

### 7. Broader syllabus audit

Compare the revised guide with:
- the supplied Number Theory syllabus;
- all `NT-*` topics;
- validated 2023-2025 IOQM source/mechanism maps.

If Wilson, CRT, Pythagorean triples or another syllabus item is not present in the supplied question set but is important to the declared scope, add a suitable bridge and at least one independent practice example. If depth must be limited, label the boundary.

### 8. Appendix A

Create questions-only Appendix A:
- all supplied questions exactly once;
- no tips;
- no solutions;
- no method names;
- no source commentary;
- preserve all conditions;
- answers only after the final question.

Put provenance in `Sources_and_Citations.md`.

### 9. Appendix B — 20 fresh audit questions

Create 20 independently solved IOQM-style questions spanning the guide, including at least:

- Division Algorithm/gcd/Euclid;
- Bézout or `ax+by=c`;
- congruence;
- linear congruence/inverse;
- CRT;
- Fermat/Euler or power cycle;
- Wilson bridge;
- phi/divisor/valuation structure;
- Pythagorean triple;
- general Diophantine/factorization;
- digit/place value/base;
- one extremal/pigeonhole number-theory application if canonically appropriate.

If an item is author-created, label it as such in the source ledger, not in the student question wording unless needed.

Answers only after B20.

Independently recompute all answers.

### 10. Quick-reference handout

Create a 1-2 page Number Theory Quick Reference with only high-value recall:

- Division Algorithm;
- gcd/lcm;
- Euclidean algorithm;
- Euclid's Lemma;
- Bézout and solvability of `ax+by=c`;
- congruence arithmetic;
- modular inverse condition;
- CRT workflow;
- Fermat/Euler hypotheses;
- `phi` basics;
- Wilson statement;
- valuation/divisor formulas;
- primitive Pythagorean triple pattern and conditions;
- common divisibility/digit rules;
- short residue-cycle cues.

No full solutions.

### 11. Citations and provenance

Create `Sources_and_Citations.md`.

Cite:
- official paper/key and stable IOQM IDs;
- repository source maps/interfaces;
- external comparison material;
- benchmark files.

Preserve source uncertainty.

### 12. Self-sufficiency audit

Every Appendix A question must pass:

1. prerequisite refresh;
2. recognition cue;
3. first useful line;
4. execution bridge;
5. legality/error check;
6. answer-free practice isolation.

Use:
`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n`

only when all pass.

Do not claim classroom solve rate or retention.

### 13. PDF is the final output

Before any final PDF creation, read:

`/home/oai/skills/pdfs/SKILL.md`

Final student PDF:

`Grade 9/Mathematics/IOQM/04_Study_Guides/Number_Theory_v1/PDFs/Number_Theory_IOQM_Grade9_Study_Guide_v1.pdf`

Use the PDF skill's recommended long-document workflow. The PDF should integrate:
- guide;
- quick reference;
- Appendix A;
- Appendix B;
- student-appropriate source notes.

Keep full source ledger and QA companions in the repository.

PDF QA:
- preflight;
- 200 dpi render of every page;
- visual page-by-page inspection;
- no clipping/overlap/broken glyphs/black squares/bad math;
- record page count;
- record SHA-256;
- commit exact final PDF;
- no workflow required.

## Required repository package

Under:

`Grade 9/Mathematics/IOQM/04_Study_Guides/Number_Theory_v1/`

create:

- `README.md`
- `Number_Theory_Study_Guide_v1.md`
- `Quick_Reference_2pp.md`
- `Appendix_A_<source-set>.md`
- `Appendix_B_20_IOQM_Style_Mock.md`
- `Self_Sufficiency_Audit.md`
- `Sources_and_Citations.md`
- `QA.md`
- `PDFs/Number_Theory_IOQM_Grade9_Study_Guide_v1.pdf`

## Final revisit/refinement report

Document in detail:

1. deficiencies of the first draft;
2. questions that exposed each deficiency;
3. orphan theorems/methods;
4. worked bridges added;
5. chapter regrouping made for a 50%-knowledge learner;
6. new syllabus bridges such as CRT/Wilson/Pythagorean triples where required;
7. scope limits;
8. Appendix A support status;
9. Appendix B breadth and independent-answer audit;
10. quick-reference quality;
11. citation/provenance status;
12. final PDF visual/preflight status.

Do not stop at “coverage exists.” Finish only after the guide is executable and the final PDF is verified.