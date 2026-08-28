# Inequalities, Bounds & Equality Conditions — PYQ Source Coverage Map

## Scope

This map links the A7 package to solution-qualified Bhaskara Preliminary evidence. It records mechanisms, not full third-party question text.

## Clean / usable anchors

| Stable ID | Year | Qualified mechanism | First-move signal | Package home |
|---|---:|---|---|---|
| `NMTC-BH-P-2018-Q12` | 2018 | reciprocal constraint; minimum via Cauchy/Engel or equivalent | combine target sum with reciprocal constraint before guessing values | Cauchy/Engel + equality |
| `NMTC-BH-P-2018-Q13` | 2018 | quadratic expression minimum | complete squares / solve equality conditions | completing-square bounds |
| `NMTC-BH-P-2019-Q05` | 2019 | fixed sum-of-squares geometry bound | translate geometry to a quadratic bound before optimization | bound translation |
| `NMTC-BH-P-2023-Q17` | 2023 | requested maximum is unbounded | test boundedness before applying any inequality | boundedness falsifier |
| `NMTC-BH-P-2024-Q17` | 2024 | four positive roots; AM-GM equality collapse | compare fixed product and sum; equality forces all roots equal | equality condition |
| `NMTC-BH-P-2024-Q30` | 2024 | odd-function symmetry plus `|2 cos x|<=2` | identify hard bound separately from algebraic value | direct bound + symmetry |
| `NMTC-BH-P-2025-Q10` | 2025 | absolute rational inequality; integer count | convert absolute inequality to distance interval, exclude denominator zero | interval + integer count |
| `NMTC-BH-P-2025-Q16` | 2025 | sum of squares equals zero | complete square and use real non-negativity to force equality | zero-sum equality collapse |

## Supporting cross-topic evidence

The following are not primary A7 anchors but reinforce the same habits:

- `NMTC-BH-P-2018-Q19` — impose integer/perfect-square restrictions after domain reduction;
- `NMTC-BH-P-2019-Q11` — positivity, bounds and divisibility restrict a symmetric integer system;
- `NMTC-BH-P-2023-Q13` — discriminant-square/nonnegative condition restricts integer solutions;
- `NMTC-BH-P-2023-Q28` — intersect inequalities before retaining natural numbers;
- `NMTC-BH-P-2024-Q19` — trigonometric/triangle relation with admissibility conditions;
- `NMTC-BH-P-2025-Q24` — determine signs before removing absolute values.

## Deliberate contrast evidence

### 2023 Q17 — unbounded maximum

This is a required contrast anchor because it falsifies the common student habit:

`sees positive variables + product constraint -> writes AM-GM -> reports equality value as requested extremum`.

The correct sequence is:

`ASK WHETHER A MAXIMUM EXISTS -> construct an escaping family -> only then discuss lower bounds if useful`.

## Source-integrity rule

This package must not manufacture optimization questions from source-conflicted items. If a PYQ statement, key or scoring disposition changes the existence/value of an extremum, keep it blocked until source custody is resolved.

## Coverage matrix

| Competency | PYQ evidence | Required student products |
|---|---|---|
| boundedness before optimization | 2023 Q17 | Concept Book + First-Step card + recognition/first-line drill + mastery falsifier |
| AM-GM equality | 2024 Q17 | derivation + equality-condition drills + transfer |
| reciprocal/Cauchy bound | 2018 Q12 | derivation + direct and disguised transfer |
| completing squares | 2018 Q13; 2025 Q16 | visual/algebraic derivation + zero/equality contrasts |
| direct bounded expression | 2024 Q30 | bound recognition card + short solve |
| absolute/rational interval | 2025 Q10 | number-line workflow + denominator exclusion + integer-count transfer |
| discriminant as feasibility/bound tool | 2023 Q13 supporting | First-Step contrast + transfer |

## Publication condition

A7 cannot be called PYQ-grounded unless all seven competency rows above have:

1. a concept explanation;
2. a first-move rule;
3. at least one reviewed author-created transfer;
4. one unlabelled assessment item;
5. explicit domain/equality/boundedness checking.
