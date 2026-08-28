# Radicals, Exponents & Logarithmic Transformations — PYQ Source Coverage Map v1

## Purpose

Trace the P0 teaching mechanisms to solution-qualified Bhaskara Preliminary evidence without reproducing full third-party paper statements.

## Evidence vocabulary

- `CLEAN_SCORED_ANCHOR` — scored, mathematically qualified, source clean enough for mechanism use.
- `SOURCE_SENSITIVE_EVIDENCE` — mathematics is useful, but exact notation/statement needs retained source caution.
- `SOURCE_CONFLICT_EVIDENCE` — source/key/convention conflict blocks canonical student use.
- `BRIDGE_EVIDENCE` — nearby transform supports the learning progression.

---

## Coverage table

| Mechanism | PYQ ID | Evidence role | First move / invariant |
|---|---|---|---|
| common square-root basis | `NMTC-BH-P-2018-Q01` | `CLEAN_SCORED_ANCHOR` | rewrite numerator/denominator using the same simple radicals before dividing |
| reciprocal cube-root invariant | `NMTC-BH-P-2018-Q21` | `CLEAN_SCORED_ANCHOR` | set a simple cube-root variable and use `(t+1/t)^3` rather than expand nested radicals |
| radical-ratio equation | `NMTC-BH-P-2018-Q26` | `CLEAN_SCORED_ANCHOR` | isolate the two radicals, cross-multiply, square once, then domain-check |
| exponential ratio normalization | `NMTC-BH-P-2023-Q07` | `CLEAN_SCORED_ANCHOR` | set a ratio such as `(2/3)^x` after normalizing bases |
| cube-root identity reconstruction | `NMTC-BH-P-2023-Q04` | `SOURCE_SENSITIVE_EVIDENCE` | set `p=∛7,q=∛6` and reconstruct a factor identity; secondary notation/options are inconsistent |
| exponent/radical system linearization | `NMTC-BH-P-2023-Q20` | `SOURCE_SENSITIVE_EVIDENCE` | convert radical/exponential statements to linear relations in exponents; exact notation delicate |
| nested-radical reconstruction | `NMTC-BH-P-2023-Q21` | `CLEAN_SCORED_ANCHOR` | match an inner radical to `(√a±√b)^2` stepwise |
| common cube-root basis | `NMTC-BH-P-2023-Q26` | `CLEAN_SCORED_ANCHOR` | set `t=∛2`; convert every cube root to a power of `t` and use `t^3=2` |
| same-base exponential normalization | `NMTC-BH-P-2024-Q04` | `CLEAN_SCORED_ANCHOR` | rewrite all bases using powers of 2 and 3 before solving |
| exponential-to-algebra substitution | `NMTC-BH-P-2024-Q09` | `CLEAN_SCORED_ANCHOR` | introduce one common-power variable, solve a quadratic relation |
| logarithmic variable substitution | `NMTC-BH-P-2024-Q12` | `CLEAN_SCORED_ANCHOR` | treat the logarithmic quantity as an algebra variable, then use symmetric-root information |
| radical identity normalization | `NMTC-BH-P-2024-Q26` | `CLEAN_SCORED_ANCHOR` | simplify the structured bracket first; the long normalized radical collapses to 1 |
| log-exponent exact simplification | `NMTC-BH-P-2024-Q28` | `CLEAN_SCORED_ANCHOR` | convert logarithmic exponent to a power of 10 before numerical simplification |
| common nth-root factor | `NMTC-BH-P-2025-Q03` | `CLEAN_SCORED_ANCHOR` | factor the shared seventh-root quantity before manipulating fractional exponents |
| conjugate surd square/cube | `NMTC-BH-P-2025-Q04` | `CLEAN_SCORED_ANCHOR` | recognize `A±B√d=(√m±√n)^2`, then convert `3/2` powers to cubes |
| symmetric radical ratio | `NMTC-BH-P-2025-Q09` | `CLEAN_SCORED_ANCHOR` | seek `x+1/x`; avoid solving the hidden parameters individually |
| sqrt-log substitution | `NMTC-BH-P-2025-Q12` | `CLEAN_SCORED_ANCHOR` | set `t=√(log_2 x)` and solve a quadratic in `t` |
| log-system algebraic conversion | `NMTC-BH-P-2025-Q27` | `CLEAN_SCORED_ANCHOR` | convert `log_4 x=log_2 y` to `x=y^2`, then solve with the second equation and log-domain checks |
| cube-root equation / root convention | `NMTC-BH-P-2025-Q18` | `SOURCE_CONFLICT_EVIDENCE` | cubing is reversible over reals, but the provisional key appears to count algebraic multiplicity after transformation; not a canonical exercise |

---

# Teaching families promoted

## R1 — Common radical basis

Clean scored support:

- 2018 Q01;
- 2023 Q26;
- 2025 Q03 as nth-root extension.

Required learning sequence:

`identify base radicals -> express every term in that basis -> factor -> simplify`.

## R2 — Reconstruct before expanding

Clean anchors:

- 2023 Q21;
- 2025 Q04;
- 2024 Q26.

Recognition triggers:

- paired conjugate surds;
- nested radicals;
- suspiciously structured `A±B√d`;
- fractional powers of a surd expression.

## R3 — Radical equations and reversibility

Clean anchor:

- 2018 Q26.

Teaching obligations:

- radicand/domain restrictions;
- isolate before squaring;
- squaring can introduce extraneous roots;
- real cubing is one-to-one, so cubing a real equation does not create sign ambiguity, but algebraic multiplicity after transformation is not the same as distinct equation solutions.

Use 2025 Q18 only as a source/convention QC contrast.

## E1 — Normalize exponential bases

Clean anchors:

- 2023 Q07;
- 2024 Q04;
- 2024 Q09.

Teach:

`rewrite bases -> choose one power/ratio variable -> solve algebra -> map back`.

Do not begin with logarithms if the bases already normalize cleanly.

## L1 — Logarithm as exponent

Foundation teaching is author-created because PYQs assume log laws and meaning.

Required progression:

`b^y=x <-> log_b x=y -> product/quotient/power laws -> equations -> transformed variables`.

Mandatory domain:

`b>0, b!=1, x>0`.

## L2 — Log-variable substitution

Clean anchors:

- 2024 Q12;
- 2025 Q12.

Choose a variable that matches the expression actually repeated. If `sqrt(log_b x)` repeats, set that entire object to `t`, not merely `log_b x`.

## L3 — Convert log systems back to algebra

Clean anchors:

- 2024 Q28;
- 2025 Q27.

Student must preserve:

- argument positivity;
- base conditions;
- positivity implied by exponentiation;
- rejection of algebraic roots that violate the original logarithms.

---

# Source-sensitive exclusions

## 2023 Q04

Useful cube-root identity mechanism, but secondary statement/options have notation inconsistencies. Use as `SOURCE_SENSITIVE_EVIDENCE`, not the primary canonical anchor.

## 2023 Q20

Useful exponent-linearization mechanism, but exact recovered notation is delicate. Preserve as source-sensitive bridge.

## 2025 Q18

Printed real equation has one distinct solution while the AMTI provisional key appears to sum multiplicity after cubing. Keep as `SOURCE_CONFLICT_EVIDENCE` for convention/source-integrity training only.

---

# Coverage gaps requiring author-created teaching

Even with strong PYQ recurrence, the following fundamentals must be explicitly taught with original examples:

- index laws including fractional/negative exponents;
- rationalizing simple denominators where useful;
- principal square-root meaning;
- conditions for `sqrt(a^2)=|a|`;
- log definition and base/argument domains;
- derivation of product/quotient/power log laws;
- one-to-one behavior of exponentials for valid bases;
- extraneous-root checking after even-power operations.

These are `AUTHOR_CREATED_FOUNDATION`, not PYQs.

## Publication state

`SOURCE_GROUNDING: READY_FOR_AUTHORING`

`STUDENT_PUBLICATION: NOT_READY`
