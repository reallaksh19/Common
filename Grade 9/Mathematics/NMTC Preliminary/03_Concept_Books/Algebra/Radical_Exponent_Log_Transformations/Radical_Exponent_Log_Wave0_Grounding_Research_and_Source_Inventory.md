# Issue #45 Wave 0 — Grounding Research and Source Inventory

`TOPIC: Radicals / Exponents / Logarithmic Transformations`

`WAVE: 0`

`STATUS: WAVE0_GROUNDING_COMPLETE`

This note was authored only after `Radical_Exponent_Log_Assimilation_Concept_Map_v2.md` existed, preserving the Issue #45 concept-map-before-prose rule.

---

# 1. Wave-0 conclusion

The rebuild should not be organized as three adjacent formula chapters called **Radicals**, **Exponents**, and **Logarithms**.

The stronger architecture is a single transformation network:

```text
NOTICE REPRESENTATION
   -> CHOOSE A COMMON / INVARIANT LANGUAGE
   -> REDUCE TO SMALLER ALGEBRA
   -> LABEL THE TRANSFORMATION AS REVERSIBLE OR CANDIDATE-GENERATING
   -> PRESERVE DOMAIN / SIGN / ZERO CONDITIONS
   -> MAP BACK
   -> CHECK
```

The existing repository package already contains strong mathematical content and source grounding. Issue #45 raises the standard by requiring the content to be rebuilt around partial-knowledge assimilation, explicit decision boundaries, attempt-before-hint, H3->H0 fading, and a First-Step compression layer only after teaching.

Wave 0 therefore does **not** discard the existing package. It reclassifies it as research/evidence input and defines a stricter integration architecture for Waves 1–5.

---

# 2. Authority stack read

The following were read before authoring the Wave-0 concept map and grounding note:

1. `Grade 9/skills/grade9-math-assimilation/SKILL.md`;
2. `Grade 9/skills/grade9-math/SKILL.md`;
3. `Grade 9/skills/grade9-math/references/partial-knowledge-assimilation-concept-map.md`;
4. `Grade 9/skills/grade9-math/references/concept-book-see-realize-understand-adopt.md`;
5. `Grade 9/Mathematics/NMTC Preliminary/README.md`;
6. `00_Authority/NMTC_Preliminary_Scope_and_Source_Policy.md`;
7. `00_Authority/NMTC_Preliminary_Concept_Dependency_Map.md`;
8. topic `README.md`;
9. `Radical_Exponent_Log_Concept_Book_Spec.md`;
10. `Radical_Exponent_Log_Source_Coverage_Map.md`;
11. legacy `Radical_Exponent_Log_Student_Draft_v0.1.md`;
12. legacy First-Step cards, practice ladders, recognition lab, first-line lab, transfer bank, mastery test and QA;
13. Quadratics Assimilation v2 benchmark manifest and merged benchmark PR #44.

Authority relationship:

- syllabus/source policy controls source claims;
- source coverage map controls PYQ disposition;
- assimilation skill controls authoring sequence;
- Wave-0 concept map controls the new Issue #45 teaching architecture;
- legacy student/performance files are evidence and candidate material, not automatic publication authority.

---

# 3. Research synthesis for the rebuild

External mathematics-education research was used only to test and strengthen the pedagogical architecture; it does not replace repository/NMTC source custody.

Research signals relevant to this topic include:

- exponent misconceptions often come from weak process meaning for negative signs, reciprocals and exponent notation rather than arithmetic alone;
- logarithm/exponent success can remain procedural unless the learner sees them as inverse processes and representations of the same relation;
- square-root misconceptions persist when learners conflate the principal radical value with the two solutions of a square equation;
- structural reading of expressions and reversible/non-reversible equation moves is essential to avoiding extraneous solutions and invalid cancellations.

Wave-0 design consequence:

> representation choice, equivalence/reversibility, and domain custody must be taught as first-move structures, not appended as warnings after calculation.

---

# 4. Qualified source inventory

## 4.1 CLEAN_SCORED_ANCHOR — 16 unique IDs

- `NMTC-BH-P-2018-Q01` — common square-root basis;
- `NMTC-BH-P-2018-Q21` — reciprocal cube-root invariant;
- `NMTC-BH-P-2018-Q26` — radical-ratio equation;
- `NMTC-BH-P-2023-Q07` — exponential ratio normalization;
- `NMTC-BH-P-2023-Q21` — nested-radical reconstruction;
- `NMTC-BH-P-2023-Q26` — common cube-root basis;
- `NMTC-BH-P-2024-Q04` — same-base exponential normalization;
- `NMTC-BH-P-2024-Q09` — exponential-to-algebra substitution;
- `NMTC-BH-P-2024-Q12` — logarithmic variable substitution;
- `NMTC-BH-P-2024-Q26` — structured radical normalization;
- `NMTC-BH-P-2024-Q28` — exact log-exponent simplification;
- `NMTC-BH-P-2025-Q03` — common nth-root factor;
- `NMTC-BH-P-2025-Q04` — conjugate surd square/cube;
- `NMTC-BH-P-2025-Q09` — symmetric radical ratio;
- `NMTC-BH-P-2025-Q12` — `sqrt(log)` substitution;
- `NMTC-BH-P-2025-Q27` — log-system algebraic conversion.

These may ground mechanisms without reproducing full third-party statements.

## 4.2 SOURCE_SENSITIVE_EVIDENCE — 2

- `NMTC-BH-P-2023-Q04` — useful cube-root identity mechanism, but secondary notation/options are inconsistent;
- `NMTC-BH-P-2023-Q20` — useful exponent/radical linearization mechanism, but exact recovered notation is delicate.

Disposition:

- bridge/support only;
- not primary clean canonical anchors;
- no silent normalization of uncertain notation.

## 4.3 SOURCE_CONFLICT_EVIDENCE — 1

- `NMTC-BH-P-2025-Q18` — printed real cube-root equation versus provisional-key distinct-root/multiplicity convention.

Disposition:

- source/convention QC only;
- preserve printed mathematics and key disagreement separately;
- do not repair it into a clean exercise;
- do not use it to inflate clean scored recurrence.

## 4.4 BONUS_EVIDENCE

No topic-specific `BONUS_EVIDENCE` is identified in the current source coverage map.

Disposition:

- record **none identified**;
- do not invent a bonus bucket;
- do not infer bonus recurrence.

---

# 5. Coverage gaps that require author-created foundation

The qualified corpus supports transformation mechanisms strongly, but several prerequisites are assumed rather than taught. Issue #45 must therefore author original foundation material for:

1. negative exponent meaning as reciprocal;
2. fractional exponent meaning and real-domain interpretation;
3. principal square-root meaning and `sqrt(a^2)=|a|`;
4. legal versus illegal radical distribution;
5. rationalization as a method choice rather than compulsory endpoint;
6. explicit `<=>` versus `=>` transformation logic;
7. multiplication/division by an expression that may vanish;
8. logarithm definition and base/argument domain;
9. derivation of product/quotient/power log laws from exponent laws;
10. injectivity/inverse structure of valid exponentials/logarithms;
11. extraneous-candidate checking after non-injective transformations;
12. substitution range such as `u>=0` for `u=sqrt(log_b x)`.

These are `AUTHOR_CREATED_FOUNDATION`, not PYQs.

---

# 6. Delta from the legacy package

The legacy package already has substantial strengths:

- common-basis, hidden-surd, reciprocal, exponent-normalization and logarithm mechanisms;
- clean source grounding;
- recognition/first-line drills;
- transfer bank and mixed mastery test;
- source-conflict visibility;
- internal math review.

Issue #45 still requires a rebuild because the old architecture does not yet prove all of the new assimilation obligations in one coherent package.

Required delta:

1. one mandatory partial-knowledge concept map before prose;
2. explicit likely-half-knowledge and missing-bridge model;
3. reversibility/equivalence as a cross-stream spine;
4. explicit decision boundaries at method-selection points;
5. H0 attempt before any hint and deliberate H3->H0 fading;
6. one integrated student journey rather than practice-family adjacency;
7. First-Step material created/re-issued only after teaching;
8. larger unlabelled Wave-4 mastery counts from Issue #45;
9. new answer/domain/equivalence audit for the rebuilt artifacts;
10. rendered PDF QA in Wave 5.

Therefore prior `PASS_INTERNAL` statuses are historical evidence, not inherited PASS for the rebuild.

---

# 7. Benchmark comparison — architecture only

The Quadratics Assimilation benchmark is used only as a minimum-quality comparator.

Wave-0 requirements carried over:

- explicit prior knowledge and missing bridge;
- concept map before prose;
- near-miss decision boundaries;
- attempt-before-hint;
- H3->H0 fading;
- independent first move;
- non-identical transfer;
- source custody;
- First-Step as post-teaching compression;
- independent mathematical audit.

Not copied:

- wording;
- exercise text;
- page layout;
- typography/colors;
- visual composition.

---

# 8. Wave-0 gate table

| Gate | Status | Evidence |
|---|---|---|
| required authorities read | PASS | Section 2 |
| topic/source map read | PASS | Sections 2 and 4 |
| concept map authored before prose | PASS | concept-map commit precedes this note |
| prior / half-knowledge / missing bridges explicit | PASS | concept map |
| invariants and representation network explicit | PASS | concept map |
| decision boundaries explicit | PASS | 15 frozen boundaries in concept map |
| misconception traps explicit | PASS | concept map diagnostic table |
| first moves explicit | PASS | concept map first-move atlas |
| transfer endpoints explicit | PASS | concept map transfer map |
| source custody explicit | PASS | Section 4 + concept map |
| clean/sensitive/conflict separated | PASS | Section 4 |
| bonus evidence isolated | PASS | none identified; not invented |
| author-created foundation gaps explicit | PASS | Section 5 |
| benchmark architecture compared | PASS | Section 7 |
| Wave-1 interfaces | NOT_RUN at Wave-0 close | successor wave |
| Assimilation Book | NOT_RUN | Wave 2 |
| First-Step rebuild | NOT_RUN | Wave 3 |
| final mastery rebuild | NOT_RUN | Wave 4 |
| PDF/render QA | NOT_RUN | Wave 5 |
| classroom timing/readability | NOT_RUN | evidence-dependent |
| longitudinal retention/transfer | NOT_RUN | evidence-dependent |

`WAVE0_GROUNDING_COMPLETE: PASS`

---

# 9. Successor status

Wave 1 has subsequently been completed on the same Issue #45 branch.

See `Wave1_Interfaces/Wave1_Integration_Readiness_Matrix.md`.

Current successor state:

- six Wave-1 stream interfaces: PASS;
- 15/15 required interface fields: PASS across 6/6 streams;
- candidate mastery pool: 28;
- independent candidate answer recheck: 28/28 PASS;
- source dispositions unchanged;
- next allowed wave: `WAVE2_INTEGRATED_ASSIMILATION_BOOK`.

This successor note does not retroactively alter the Wave-0 gate history above.
