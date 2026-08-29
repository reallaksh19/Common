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

## A. Pedagogy authorities

1. `Grade 9/skills/grade9-math-assimilation/SKILL.md`
2. `Grade 9/skills/grade9-math/SKILL.md`
3. `Grade 9/skills/grade9-math/references/partial-knowledge-assimilation-concept-map.md`
4. `Grade 9/skills/grade9-math/references/concept-book-see-realize-understand-adopt.md`

Binding consequences:

- learner is roughly 50%-prepared, not blank-slate;
- formula recall is not mastery;
- concept map must precede prose;
- every major concept needs `PRIOR -> BRIDGE -> INVARIANT -> FIRST MOVE -> TRANSFER`;
- every major method needs a close competing method/non-example;
- learner attempts before hints;
- hints fade `H3 -> H2 -> H1 -> H0` across practice;
- First-Step material is a post-teaching compression layer;
- independent mathematics audit is mandatory before promotion.

## B. NMTC authority

1. `Grade 9/Mathematics/NMTC Preliminary/README.md`
2. `Grade 9/Mathematics/NMTC Preliminary/00_Authority/NMTC_Preliminary_Scope_and_Source_Policy.md`
3. `Grade 9/Mathematics/NMTC Preliminary/00_Authority/NMTC_Preliminary_Concept_Dependency_Map.md`

Binding consequences:

- Preliminary / Screening only for curriculum weighting and difficulty calibration;
- historical frequency informs emphasis, never syllabus inclusion;
- stable IDs use `NMTC-BH-P-YYYY-QNN`;
- source provenance and scoring disposition are separate facts;
- source defects cannot be silently repaired;
- bonus evidence cannot inflate ordinary scored recurrence;
- the global Algebra bottleneck is representation switching -> first useful move;
- this topic sits at A6 and depends on the A1 structural-representation network plus quadratic/algebra fluency.

## C. Topic authorities / legacy package

1. `Radical_Exponent_Log_Transformations/README.md`
2. `Radical_Exponent_Log_Concept_Book_Spec.md`
3. `Radical_Exponent_Log_Source_Coverage_Map.md`
4. `Radical_Exponent_Log_Student_Draft_v0.1.md`
5. `09_QA/P0_Algebra_Radical_Exponent_Log_QA.md`

Binding consequences:

- existing package already recognizes common basis, hidden surds, reciprocal invariants, exponent normalization, log variables, log-to-algebra conversion and domain/source QC;
- existing source map is the custody authority for topic PYQ use;
- existing QA is valid evidence about the legacy package, but its PASS labels are not automatically inherited by the new Issue #45 rebuild;
- publication/render/classroom gates remain separate.

## D. Benchmark authority

- merged PR #44;
- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`;
- benchmark PDF is a quality comparator, not a wording/layout template.

Wave-0 benchmark takeaways:

- concept-map completeness must be explicit;
- missing-link repair must be visible;
- decision boundaries are mandatory;
- first-move independence matters more than worked-example volume;
- source custody and answer verification must be auditable;
- classroom timing and longitudinal mastery remain evidence-dependent, not inferable from static artifacts.

---

# 3. Research synthesis beyond the repository

External research is used here only to sharpen misconception and pedagogy design. It does **not** alter NMTC source recurrence, evidence class, syllabus custody or PYQ provenance.

## R-01 Exponent knowledge is often procedural and sign/inverse errors persist

A 2026 study of 150 middle-school students reported misconceptions involving zero exponents, negative exponents, sign/grouping distinctions and confusion among exponent forms. This is directly relevant to W1-B because a learner who “knows exponent laws” may still lack a stable inverse/grouping model.

Reference:

- Sevgi, S. & Akdemir Kabalcı, S. (2026), *Students’ Misconceptions About Exponents*, SAGE Open, DOI `10.1177/21582440261449038`.

A Journal of Mathematical Behavior study also found persistent exponential-expression errors tied to negative signs and underdeveloped inverse conceptions, even among students in progressively advanced courses.

Reference:

- Cangelosi et al. (2013), *The negative sign and exponential expressions: Unveiling students’ persistent errors and misconceptions*, Journal of Mathematical Behavior 32(1), DOI `10.1016/j.jmathb.2012.10.002`.

### Design implication

Do not test negative/fractional exponents only by routine simplification. Use close contrasts such as:

- `a^-2` vs `(-a)^2` vs `-a^2`;
- multiplication of same-base powers vs addition of same-base powers;
- explicit reciprocal rewrite before compact notation.

The diagnostic target is conceptual grouping/inverse meaning, not arithmetic speed.

---

## R-02 Students can compute exponents but still lack process-level understanding of exponentials/logarithms

Work on exponential/logarithmic understanding has emphasized that students may successfully compute simple exponent cases while failing to reason about exponentiation as a process. Instruction that constructs exponent/log relationships and meaning can outperform rule-only instruction on conceptual and explanatory measures.

References:

- Weber, K. (2002), *Developing Students’ Understanding of Exponents and Logarithms*, ERIC `ED471763`.
- Weber, K. (2002), *Students’ Understanding of Exponential and Logarithmic Functions*, ERIC `ED477690`.
- Recent APOS-based work: *High school student understanding of exponential and logarithmic functions*, Journal of Mathematical Behavior 66 (2022), article 100953, DOI `10.1016/j.jmathb.2022.100953`.

### Design implication

W1-E must begin with exponent meaning and inverse translation, then derive log laws. It must not open with a list of `log` identities.

W1-F should make the learner move deliberately among:

```text
exponent statement <-> logarithmic statement <-> algebraic relation
```

while preserving domain conditions.

---

## R-03 Principal square-root meaning is a genuine conceptual fault line

Research on pre-university students shows that `sqrt(x^2)` can evoke inconsistent answers such as `x` or `±x`, while `|x|` is often not retrieved reliably. Studies of radicals likewise report persistent conceptual and operational misconceptions.

References:

- Kontorovich, I. (2021), *Pre-university students square-root from squared things: A commognitive account of apparent conflicts within learners’ mathematical discourses*, Journal of Mathematical Behavior 64, 100910, DOI `10.1016/j.jmathb.2021.100910`.
- *Misconceptions in radicals in high school mathematics* (2011), Procedia - Social and Behavioral Sciences 15, 120–127, DOI `10.1016/j.sbspro.2011.03.060`.
- *Misconceptions and Learning Difficulties in Radical Numbers* (2012), Procedia - Social and Behavioral Sciences 46, 462–467, DOI `10.1016/j.sbspro.2012.05.142`.

### Design implication

W1-A must separate three ideas that are commonly blended:

1. the radical symbol `sqrt(a)` denotes the non-negative principal square root for `a>=0`;
2. simplifying `sqrt(x^2)` gives `|x|` over the reals;
3. solving `u^2=a` can produce two values when `a>0`.

This boundary should be taught through a contrast pair, not a warning box alone.

---

## R-04 Extraneous solutions are fundamentally about equivalence and reversibility

Mathematics-education and instructional sources emphasize that squaring can preserve every original solution while enlarging the solution set because squaring is not one-to-one on the reals. Related risks occur when multiplying or dividing by variable expressions that can vanish.

References:

- Grosser-Clarkson, D. L. (2015), *The Root of the Problem*, Mathematics Teacher 109(2), ERIC `EJ1074852`.
- Emory/Oxford College Mathematics Center, *Equivalent Equations* — explains invertible transformations and why non-invertible squaring can create extraneous candidates.
- Illustrative Mathematics, `HSA-REI.A.2 Radical Equations` task — explicitly contrasts squaring and cubing and asks students to explain extraneous solutions.

### Design implication

W1-C must not reduce the rule to “square, then check.” It should teach an equation-transform grammar:

```text
<=>  both directions justified on the current domain
=>   every old solution survives, but new candidates may appear
```

Learners must also ask whether a multiplier/divisor can be zero before transforming an equation.

---

## R-05 Expression-structure and equality interpretation errors are cross-cutting

A recent secondary-school error analysis of exponential/logarithmic functions classified errors not only as arithmetic, but also as failures to see algebraic-expression structure and as procedural interpretations of equality. That supports Issue #45’s decision to foreground representation choice and reversible transformations rather than merely add more practice of laws.

Reference:

- Ramadhanti, F. T. (2025/2026 issue cycle), *Students’ Errors in Exponential and Logarithmic Functions: An Error Analysis Using AVAEM Categories*, Absis: Mathematics Education Journal, DOI `10.32585/absis.v7i2.7357`.

### Design implication

Diagnostics should distinguish:

- rule recall failure;
- representation failure;
- structural-expression failure;
- equality/equivalence failure;
- domain/condition failure;
- execution/calculation failure.

These should not all receive the same “review the formula” remediation.

---

# 4. Wave-0 architecture decisions

## D-01 The organizing lens is `TRANSFORM`, not formula family

Every stream must repeatedly ask:

> Which equivalent representation makes the structure smaller?

This unifies radicals, exponents and logarithms.

## D-02 `REVERSIBILITY` is a cross-stream spine

It is not confined to radical equations.

It applies to:

- squaring / taking even powers;
- odd-power transforms;
- multiplying/dividing by expressions that may vanish;
- exponential/log inverse conversion;
- equality of logarithms;
- substitution with restricted range.

## D-03 Every substitution carries a domain/range payload

Examples:

- `t=a^x` -> `t>0` for valid real exponential base;
- `u=sqrt(log_b x)` -> `u>=0`, `x>0`, valid base;
- `S=x+1/x` -> `x!=0`.

The payload must be written with the substitution, not recovered at the end.

## D-04 Method-choice contrasts must change one structural condition at a time

Examples:

- same-base exponential equation vs unrelated-base equation;
- `sqrt(ab)` vs `sqrt(a+b)`;
- square vs cube;
- `t=log_b x` vs `u=sqrt(log_b x)`;
- symmetric reciprocal target vs asymmetric target;
- clean source anchor vs conflicted key/source case.

## D-05 First-Step Reference remains downstream

The current legacy package contains First-Step cards, but the Issue #45 rebuild must produce its new First-Step Reference only after the Assimilation Book is integrated. Legacy cards are evidence/input, not a substitute for Wave-2 teaching.

## D-06 Legacy QA does not auto-promote new artifacts

The old package’s `PASS_INTERNAL` findings demonstrate that useful content exists. New Wave-1/2/3/4 outputs must still independently pass the new Issue #45 gates and answer audit.

---

# 5. Qualified evidence inventory

The inventory below preserves the current topic Source Coverage Map. No evidence class is upgraded here.

| PYQ ID | Mechanism | Existing source disposition | Wave-0 weighting disposition | Wave-1 home |
|---|---|---|---|---|
| `NMTC-BH-P-2018-Q01` | common square-root basis | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-A |
| `NMTC-BH-P-2018-Q21` | reciprocal cube-root invariant | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-D |
| `NMTC-BH-P-2018-Q26` | radical-ratio equation | `CLEAN_SCORED_ANCHOR` | primary reversibility/radical anchor | W1-C / W1-A |
| `NMTC-BH-P-2023-Q04` | cube-root identity reconstruction | `SOURCE_SENSITIVE_EVIDENCE` | bridge/supplement only; not canonical | W1-A |
| `NMTC-BH-P-2023-Q07` | exponential ratio normalization | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-B |
| `NMTC-BH-P-2023-Q20` | exponent/radical system linearization | `SOURCE_SENSITIVE_EVIDENCE` | bridge/supplement only; notation-sensitive | W1-B / W1-F |
| `NMTC-BH-P-2023-Q21` | nested-radical reconstruction | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-A |
| `NMTC-BH-P-2023-Q26` | common cube-root basis | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-A |
| `NMTC-BH-P-2024-Q04` | same-base exponential normalization | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-B |
| `NMTC-BH-P-2024-Q09` | exponential-to-algebra substitution | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-B |
| `NMTC-BH-P-2024-Q12` | logarithmic variable substitution | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-E / W1-F |
| `NMTC-BH-P-2024-Q26` | radical identity normalization | `CLEAN_SCORED_ANCHOR` | primary mechanism anchor | W1-A |
| `NMTC-BH-P-2024-Q28` | exact log-exponent simplification | `CLEAN_SCORED_ANCHOR` | primary inverse-language anchor | W1-E / W1-F |
| `NMTC-BH-P-2025-Q03` | common nth-root factor | `CLEAN_SCORED_ANCHOR` | primary extension anchor | W1-A |
| `NMTC-BH-P-2025-Q04` | conjugate surd square/cube | `CLEAN_SCORED_ANCHOR` | primary reconstruction anchor | W1-A |
| `NMTC-BH-P-2025-Q09` | symmetric radical ratio | `CLEAN_SCORED_ANCHOR` | primary reciprocal-invariant anchor | W1-D |
| `NMTC-BH-P-2025-Q12` | sqrt-log substitution | `CLEAN_SCORED_ANCHOR` | primary repeated-object anchor | W1-E / W1-F |
| `NMTC-BH-P-2025-Q18` | cube-root equation / root convention | `SOURCE_CONFLICT_EVIDENCE` | QC-only; never canonicalized | W1-C / W1-F source-integrity lab |
| `NMTC-BH-P-2025-Q27` | log-system algebraic conversion | `CLEAN_SCORED_ANCHOR` | primary log-to-algebra anchor | W1-F |

## Evidence class counts for this topic map

- `CLEAN_SCORED_ANCHOR`: 16 IDs.
- `SOURCE_SENSITIVE_EVIDENCE`: 2 IDs.
- `SOURCE_CONFLICT_EVIDENCE`: 1 ID.
- `BONUS_EVIDENCE`: **0 identified in the current topic Source Coverage Map**.

Do not infer that “zero bonus items” means the topic has no high-ceiling mechanisms. It means only that this topic’s current qualified evidence set contains no items dispositioned as bonus evidence.

---

# 6. Clean / bonus / bridge / conflict weighting policy for Issue #45

Issue #45 asks for clean/bonus/bridge/conflicted inventory before examples are weighted. The current repository vocabulary includes `SOURCE_SENSITIVE_EVIDENCE`, so Wave 0 maps it without renaming the source record:

| Working weight bucket | Repository disposition | Use |
|---|---|---|
| CLEAN | `CLEAN_SCORED_ANCHOR` | mechanism grounding and candidate canonical historical anchors |
| BONUS | `BONUS_EVIDENCE` | enrichment only; excluded from ordinary scored recurrence |
| BRIDGE | `BRIDGE_EVIDENCE` or source-sensitive evidence used only as a bridge | mechanism support, not primary recurrence/canonical anchor |
| CONFLICT | `SOURCE_CONFLICT_EVIDENCE` | source-integrity/QC only; never silently repaired |

Current topic result:

```text
CLEAN:    substantial coverage across all six streams
BONUS:    none identified
BRIDGE:   2023 Q04, 2023 Q20 are source-sensitive and limited to bridge/support use
CONFLICT: 2025 Q18
```

No recurrence statistic is recomputed in Wave 0, and no source-sensitive item is promoted to clean.

---

# 7. Author-created foundation inventory

The source map explicitly leaves several fundamentals to author-created teaching. Wave 1 must create these without fake NMTC attribution.

## W1-A gaps

- principal square-root semantics;
- `sqrt(x^2)=|x|`;
- legal/illegal radical distribution;
- rationalization as a method-choice tool rather than ritual;
- real-domain interpretation of even/odd roots and fractional exponents.

## W1-B gaps

- negative exponent as reciprocal;
- fractional exponent as radical/power bridge;
- sign/grouping contrasts;
- false exponent-distribution rules;
- positivity/range after `t=a^x` substitution.

## W1-C gaps

- `<=>` versus `=>` transformation language;
- squaring as non-injective over reals;
- cubing as injective over reals;
- multiply/divide-by-variable zero-case logic;
- isolate-before-square contrast.

## W1-D gaps

- recurrence derivation for `S_n=x^n+x^-n`;
- explicit “do I need x?” decision test;
- symmetric versus asymmetric target contrasts.

## W1-E gaps

- logarithm definition from exponent meaning;
- derivation of product/quotient/power laws;
- invalid sum-law contrast;
- base and argument domain;
- exact inverse cancellation.

## W1-F gaps

- substitution-range ledger;
- choosing the repeated whole log object;
- injectivity + domain before equating log arguments;
- transformed algebraic candidate filtering;
- source conflict versus learner error diagnosis.

---

# 8. Legacy-package gap analysis against Issue #45

The current package is valuable but should not simply be reformatted.

## What is already strong

- broad mechanism coverage;
- clean source mapping;
- principal-root and false-log-law warnings;
- reciprocal invariant presence;
- domain checking;
- existing recognition/first-line/transfer assets;
- legacy second-pass math review.

## What Issue #45 makes more explicit / stricter

### Gap G-01 — one integrated partial-knowledge concept map

The legacy package has a concept-book specification but not the new mandatory partial-knowledge map with explicit prior knowledge, half-knowledge, missing bridge, invariant, representation, decision boundary, misconception, first move, transfer and source nodes across all six streams.

**Wave-0 action:** closed by `Radical_Exponent_Log_Assimilation_Concept_Map_v2.md`.

### Gap G-02 — transformation reversibility as a named cross-stream spine

The legacy draft teaches extraneous roots mainly in radical equations. Issue #45 explicitly requires reversible/non-reversible transformations including variable multiplication/division.

**Wave-0 action:** promoted reversibility/domain ledger to a central invariant and dedicated W1-C stream.

### Gap G-03 — explicit decision-boundary density

Legacy material contains contrasts, but Issue #45 requires close method-choice boundaries systematically across all streams.

**Wave-0 action:** 15 mandatory cross-topic boundaries defined before prose.

### Gap G-04 — H3->H0 fading embedded in each stream

Legacy practice assets exist, but the new rebuild must show a deliberate hint fade after H0 attempt for each major concept.

**Wave-0 action:** added `H3_TO_H0_FADE_PLAN` to every Wave-1 interface contract; execution remains Wave 1/2.

### Gap G-05 — First-Step compression must be regenerated after teaching

Legacy First-Step cards cannot be treated as the Issue #45 final First-Step Reference.

**Wave-0 action:** lock legacy cards as research input only until Wave 3.

### Gap G-06 — new mastery quotas

Issue #45 requires at least:

- 20 recognition-only prompts;
- 12 first-line prompts;
- 18 solve/transfer items;
- 6 WHY-NOT contrasts;
- 4 domain/extraneous checks.

The legacy package happens to contain similarly sized components, but the Issue #45 bank must be rebuilt/audited against the new integrated architecture rather than assumed equivalent.

---

# 9. Wave-1 execution interfaces now frozen

Wave 1 may proceed in parallel only if each stream returns:

```text
CONCEPTS
PREREQUISITES
RECOGNITION_CUES
FIRST_MOVES
INVARIANTS
REPRESENTATION_SWITCHES
REVERSIBILITY_OR_DOMAIN_CONDITIONS
DECISION_BOUNDARIES
MISCONCEPTION_TRAPS
CONTRAST_PAIRS
TRANSFER_MECHANISMS
SOURCE_IDS_AND_DISPOSITIONS
CANDIDATE_MASTERY_ITEMS
DIAGNOSTIC_TAGS
H3_TO_H0_FADE_PLAN
```

Cross-stream vocabulary to keep stable:

- `REPRESENTATION_GAP`
- `INVARIANT_GAP`
- `REVERSIBILITY_GAP`
- `DOMAIN_GAP`
- `ZERO_CASE_GAP`
- `PRINCIPAL_ROOT_GAP`
- `EXPONENT_INVERSE_GAP`
- `LOG_INVERSE_GAP`
- `REPEATED_OBJECT_GAP`
- `METHOD_CHOICE_GAP`
- `SOURCE_INTEGRITY_GAP`
- `EXECUTION_ERROR`

These are provisional diagnostic tags for authoring consistency; Wave 2 may refine labels but should not collapse distinct conceptual failures into “careless mistake.”

---

# 10. Wave-0 QA gates

| Gate | Status | Evidence |
|---|---|---|
| Issue #45 read | PASS | objective, inputs, Waves 0–5 and acceptance criteria reviewed |
| assimilation skill read | PASS | `grade9-math-assimilation/SKILL.md` |
| Grade 9 Math authority read | PASS | `grade9-math/SKILL.md` |
| partial-knowledge map read | PASS | required learner/bridge node contract adopted |
| concept-book protocol read | PASS | SEE/REALIZE/UNDERSTAND/ADOPT + operational loop retained |
| NMTC scope/source policy read | PASS | Preliminary-only, provenance, defect and bonus rules retained |
| dependency map read | PASS | A6 prerequisites and representation bottleneck incorporated |
| topic folder/spec/source map read | PASS | legacy package treated as evidence input |
| legacy QA reviewed | PASS | prior PASS states not automatically inherited |
| benchmark PR #44 / manifest reviewed | PASS | comparator architecture used; no wording/layout copied |
| external misconception research | PASS | exponent, radical, log/inverse and equivalence literature synthesized |
| concept map created before prose | PASS | concept-map commit precedes this note |
| prior/half-knowledge explicit | PASS | concept map Section 2 plus per-stream maps |
| missing bridges explicit | PASS | concept map Sections 2 and 5–10 |
| decision boundaries explicit | PASS | concept map Section 12 |
| source custody explicit | PASS | concept map Section 16 + this note Section 5 |
| clean/bonus/bridge/conflict inventoried | PASS | this note Sections 5–6 |
| source-sensitive items not inflated | PASS | 2023 Q04/Q20 remain bridge/support only |
| 2025 Q18 conflict preserved | PASS | QC-only; no silent repair |
| author-created foundation needs isolated | PASS | this note Section 7 |
| Wave-1 interfaces frozen | PASS | this note Section 9 |
| Wave-1 teaching prose | NOT_RUN | intentionally outside Wave 0 |
| First-Step Reference | NOT_RUN | Wave 3 only |
| mastery-bank rebuild | NOT_RUN | Wave 4 only |
| PDF rendering/page inspection | NOT_RUN | Wave 5 only |
| benchmark PDF visual comparison | NOT_RUN | Wave 5 production comparison |
| classroom timing/readability | NOT_RUN | requires learner observation |
| longitudinal retention/transfer | NOT_RUN | requires longitudinal evidence |

## Wave-0 verdict

`PASS — WAVE0_GROUNDING_COMPLETE`

This is not a claim that Issue #45 is complete. It authorizes the six Wave-1 streams to begin from a common concept/evidence architecture.

`NEXT: W1-A ... W1-F PARALLEL SUBTOPIC INTERFACES`
