# Domain Prompt Examples for `ioqm-grade9-study-guide-builder`

These prompts are templates. Replace the bracketed paths/sources with the actual repository topic package and user-supplied material.

---

# Example 1 — Algebra study guide

You are preparing a Grade 9 IOQM Algebra study guide for a student with about 50% prior knowledge.

## Inputs

1. Read the Grade 9 IOQM architecture and algebra topic packages in:
   - `Grade 9/Mathematics/IOQM/03_Main_Topics/ALG-*`
2. Read the benchmark:
   - `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`
3. Read the supplied algebra question/tip attachment completely.
4. Treat the attachment as comparison/practice material unless it is independently established as official source authority.

## Required analysis before writing

Create a full question-to-method matrix.

For every supplied question identify:

- exact question number;
- primary algebra subtopic;
- prerequisite;
- first useful line;
- the method needed to finish;
- likely misconception for a half-prepared Grade 9 learner;
- whether the proposed guide explicitly teaches that method.

Fail the draft if any question requires an unnamed trick.

Suggested algebra grouping:

1. identities and factorization;
2. equations and admissibility checks;
3. inequalities, bounds and equality cases;
4. polynomials, roots and Vieta;
5. sequences/recurrences;
6. functional equations;
7. exponents, radicals and logarithms;
8. floor/ceiling and discrete functions;
9. cross-topic integer restrictions.

Do not use these headings mechanically if the source set suggests a better dependency order.

## Student guide

Write in ordinary teacher language.

Each subtopic must contain:

- what the student probably already knows;
- the missing Olympiad link;
- why the method works;
- a non-identical worked example;
- “What should I notice?”;
- “Try this first”;
- common mistakes;
- when a nearby method is not appropriate.

Do not expose internal terms such as microstream, wave, H-level, transfer gate or interface owner.

## Appendices

Appendix A:
- all supplied questions;
- questions only;
- no worked solutions, tips or source commentary;
- answers only after the final question.

Appendix B:
- 20 author-created IOQM-style algebra mock questions;
- balance them against verified 2023–2025 IOQM mechanism patterns;
- include underrepresented canonical algebra skills;
- answers only after B20;
- independently recompute every answer.

## Quick reference

Create a 1–2 page Algebra Quick Reference containing only high-value recall items, for example:

- standard identities;
- discriminant/Vieta;
- inequality legality/equality conditions;
- radical domain checks;
- exponent/log laws with restrictions;
- floor/ceiling definitions;
- “candidate answer must satisfy the original equation.”

## QA

Produce:
- `Self_Sufficiency_Audit.md`;
- `Sources_and_Citations.md`.

Record document-level sufficiency separately from classroom evidence.

---

# Example 2 — Number Theory / Number System study guide

You are preparing a Grade 9 IOQM Number Theory study guide for a student with about 50% prior knowledge.

## Inputs

1. Read:
   - `Grade 9/Mathematics/IOQM/03_Main_Topics/NT-*`
2. Read the Grade 9 Quadratics benchmark as a quality comparator only.
3. Read the complete supplied number-theory question/tip source.
4. Preserve the source role:
   - official/validated material = authority;
   - coaching/video/notes = comparison/practice.

## Pre-authoring audit

Map every question to one or more of:

1. divisibility, gcd/lcm, Euclidean algorithm;
2. Euclid's Lemma and Bézout/extended Euclid;
3. congruences and residues;
4. power cycles, Euler/Fermat legality;
5. prime factorization and valuations;
6. divisor count and perfect powers;
7. Diophantine equations;
8. digit/place-value/base structure;
9. consecutive sums and odd-divisor structure;
10. pigeonhole/extremal number-theory applications.

For each problem, write the first mathematical move the learner should be able to produce after studying the guide.

Examples:
- “gcd expression” → run Euclidean reduction before factoring huge numbers;
- “last digits” → choose a modulus and inspect a short power cycle;
- “integer solutions” → check gcd divisibility before parameterizing;
- “number of divisors” → write the prime-exponent vector;
- “digit sum/divisibility” → use place value or residues before enumeration.

If a problem needs a theorem not explicitly taught, repair the guide before calling it complete.

## Student guide requirements

Teach each major theorem with:

- statement;
- why it is true at Grade 9 level;
- hypothesis checks;
- a simple worked example;
- a near-miss where the theorem cannot be used.

Do not merely say “apply Euler” or “use CRT” without explaining legality and a practical decision rule.

## Appendices

Appendix A:
- complete supplied questions only;
- answer key only at the end.

Appendix B:
- 20 fresh IOQM-style number-theory mock questions;
- use verified historical mechanisms as style references;
- include at least:
  - gcd/Euclid;
  - residues;
  - valuations;
  - divisor structure;
  - Diophantine solvability;
  - digits/place value;
  - one pigeonhole/extremal item.

## Quick reference

Prepare a 1–2 page sheet with:

- gcd/lcm identities;
- Euclidean algorithm;
- Euclid's Lemma;
- Bézout solvability criterion;
- modular arithmetic rules;
- Euler/Fermat hypotheses;
- valuation/divisor formulas;
- standard divisibility tests;
- common residue cycles.

## QA

Run the full 50%-knowledge self-sufficiency audit and create the source ledger.

---

# Example 3 — Geometry study guide

You are preparing a Grade 9 IOQM Geometry study guide for a student with about 50% prior knowledge.

## Inputs

1. Read:
   - `Grade 9/Mathematics/IOQM/03_Main_Topics/GEO-*`
2. Read the Grade 9 benchmark only for quality comparison.
3. Read the complete supplied geometry question/tip source.
4. Preserve exact historical figures/stems only from validated authority. A coaching reconstruction is not figure authority.

## Pre-authoring audit

Map every supplied problem by the *first geometric structure to recognize*, not by superficial diagram appearance.

Suggested grouping:

1. angle chasing, parallel lines and polygon angle structure;
2. triangle feasibility and right/acute/obtuse tests;
3. similarity and ratio;
4. area ratios and centroid structure;
5. medians, Apollonius and Stewart;
6. angle bisectors and special cevians;
7. cyclic quadrilaterals and power of a point;
8. tangency and radius relations;
9. coordinate geometry as an alternate representation;
10. integer/metric geometry filters.

For every question identify:

- exact givens;
- target;
- first theorem whose hypotheses are already established;
- any missing bridge theorem;
- whether the problem can be solved more simply by ratio/area than by coordinates;
- whether a diagram is source-controlled or merely illustrative.

Fail the guide if it expects the student to know a theorem that is only named.

## Student guide

Write like a teacher at the board:

- draw or describe the structure;
- state what is known before invoking a theorem;
- derive the theorem when appropriate;
- show a near-miss where a tempting theorem is illegal;
- use one non-identical worked example;
- provide “What should I notice?” and “First line to try”.

Examples of legality checks:
- similarity needs a valid criterion;
- a quadrilateral is not cyclic just because it looks cyclic;
- a tangent-radius right angle applies at the point of tangency;
- Stewart applies to a cevian with correctly named segments;
- Pythagoras is not an acute/obtuse test unless side ordering is clear.

## Appendices

Appendix A:
- every supplied question;
- preserve all needed figure information;
- questions only;
- answers after the final question.

If the original question depends on an official printed figure, do not silently redraw or alter it without source custody.

Appendix B:
- 20 fresh IOQM-style geometry mock questions;
- include a balanced mix of angle, triangle metric, similarity/area, circles/tangency and coordinate representation;
- independently recompute every answer.

## Quick reference

Prepare a 1–2 page sheet with:

- triangle inequality;
- Pythagorean/acute/obtuse side-square tests;
- similarity criteria and area-scale rule;
- median/Apollonius formula;
- Stewart theorem;
- angle-bisector theorem;
- cyclic angle facts;
- tangent-radius and power-of-a-point facts;
- centroid ratios;
- coordinate distance/slope/midpoint formulas only where canonically in scope.

## QA

Run the full self-sufficiency audit.

The final claim should be:

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS`

only if every supplied question has a taught and executable method.

Do not convert static document completeness into a claim about classroom solve rate.
