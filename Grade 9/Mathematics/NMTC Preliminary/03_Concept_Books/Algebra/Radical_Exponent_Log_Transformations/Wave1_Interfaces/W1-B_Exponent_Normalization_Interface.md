# Issue #45 — Wave 1B Interface
## Exponent normalization

`STATUS: W1_INTERFACE_COMPLETE`

`ROLE: INTERNAL_SUBTOPIC_INTERFACE`

This interface defines what Wave 2 must teach and what the learner must eventually recognize independently.

## 1. CONCEPTS

- exponent laws as structural consequences, not symbol rules;
- negative exponents as reciprocals;
- fractional exponents as radical/power representation switches;
- common-base normalization;
- repeated exponential object substitution;
- homogeneous two-base ratio substitution;
- positivity inherited by `t=a^x` for valid positive base.

## 2. PREREQUISITES

- repeated multiplication and basic factorization;
- integer powers;
- fractions/reciprocals;
- simple radicals;
- linear/quadratic solving once the substitution is known.

## 3. RECOGNITION_CUES

| Visible cue | Structural recognition |
|---|---|
| bases such as `2,4,8` or `3,9,27` | rewrite to a common base |
| `a^(2x), a^x, 1` | low-degree algebra in `t=a^x` |
| homogeneous powers of two bases | divide by one positive exponential and use a ratio variable |
| negative exponent | reciprocal, not a negative number |
| fractional exponent | power/root representation link |
| temptation to take logs immediately | first ask whether normalization is cheaper |

## 4. FIRST_MOVES

1. Rewrite related bases before applying any new operation.
2. If the same exponential object repeats, set `t=a^x` and record `t>0`.
3. If two base families occur homogeneously, divide by one nonzero positive exponential factor and set a ratio such as `t=(a/b)^x`.
4. If a negative/fractional exponent is causing sign confusion, rewrite it explicitly as a reciprocal or radical.

## 5. INVARIANTS

- multiplication of same-base powers adds exponents;
- quotient of same-base powers subtracts exponents;
- power of a power multiplies exponents;
- negative exponent means multiplicative inverse;
- valid positive-base exponential values remain positive;
- common-base rewriting changes notation, not value.

## 6. REPRESENTATION_SWITCHES

- `8^x <-> 2^(3x)`;
- `a^-n <-> 1/a^n` for `a!=0`;
- `a^(m/n) <-> nthroot(a^m)` under the intended real-domain interpretation;
- `a^(2x),a^x,1 -> t^2,t,1` with `t=a^x>0`;
- homogeneous `a^x,b^x` combinations -> powers of `(a/b)^x`.

## 7. REVERSIBILITY_OR_DOMAIN_CONDITIONS

- negative exponents require nonzero base;
- real fractional powers need domain interpretation; do not import complex conventions silently;
- `t=a^x` with `a>0`, `a!=1` gives `t>0`, so non-positive algebraic roots of the transformed polynomial are invalid;
- dividing by `b^x` for `b>0` is safe because `b^x>0`;
- equality of powers with the same valid base is reversible because the exponential is one-to-one.

## 8. DECISION_BOUNDARIES

`B-DB1 COMMON_BASE_vs_LOGS`  
Use common-base normalization first when bases are related; logs are not automatically the “advanced” method.

`B-DB2 NEGATIVE_EXPONENT_vs_NEGATIVE_BASE`  
`a^-n` is reciprocal structure; `(-a)^n` is base grouping/sign structure.

`B-DB3 PRODUCT_POWER_LAW_vs_FALSE_SUM_LAW`  
`a^m a^n=a^(m+n)` is valid; `a^m+a^n=a^(m+n)` is generally false.

`B-DB4 REPEATED_POWER_SUBSTITUTION_vs_SOLVE_EXPONENT_NOW`  
Name the repeated object before trying to isolate `x`.

`B-DB5 SINGLE_BASE_vs_RATIO_VARIABLE`  
If no single obvious common base exists but the equation is homogeneous in two positive base families, divide and use a ratio variable.

## 9. MISCONCEPTION_TRAPS

- `a^-2=-a^2`;
- `(-a)^2=-a^2`;
- exponent laws distributed over addition;
- cancelling exponents across sums;
- forgetting `t>0` after substitution;
- taking logarithms before checking common-base structure;
- using a fractional-exponent identity outside the intended real domain.

## 10. CONTRAST_PAIRS

### CP-B1 — normalization vs logs
- `16^x=8^(x+1)` -> rewrite both as powers of 2.
- genuinely unrelated bases with no algebraic normalization -> logarithms may later be appropriate.

### CP-B2 — multiplication vs addition
- `2^m * 2^n=2^(m+n)`.
- `2^m+2^n` does not combine that way; e.g. `m=1,n=2` gives `6`, not `8`.

### CP-B3 — reciprocal vs sign
- `2^-3=1/8`.
- `(-2)^3=-8`.

### CP-B4 — algebraic transformed root vs admissible exponential value
- transformed polynomial root `t=-2` may be algebraically valid;
- it cannot equal `a^x` for positive real base `a`.

## 11. TRANSFER_MECHANISMS

- mixed bases that collapse to one prime-base language;
- polynomial in `a^x` with a positivity filter;
- homogeneous equation in `a^x,b^x` solved by a ratio variable;
- radical/fractional-exponent expression where representation choice is the main difficulty;
- near-miss where logs are possible but structurally inferior.

## 12. SOURCE_IDS_AND_DISPOSITIONS

### CLEAN_SCORED_ANCHOR
- `NMTC-BH-P-2023-Q07` — exponential ratio normalization;
- `NMTC-BH-P-2024-Q04` — same-base normalization;
- `NMTC-BH-P-2024-Q09` — exponential-to-algebra substitution.

### SOURCE_SENSITIVE_EVIDENCE
- `NMTC-BH-P-2023-Q20` — exponent/radical linearization; exact notation remains delicate.

### AUTHOR_CREATED_FOUNDATION required
- negative exponent meaning;
- fractional exponent meaning;
- false distribution/addition contrasts;
- positivity filtering after `t=a^x`.

## 13. CANDIDATE_MASTERY_ITEMS

All are `AUTHOR_CREATED_TRANSFER` candidates.

### B-M1 — fractional exponent representation
Evaluate exactly `27^(2/3)`.

Expected: `9`.

Check: `27=3^3`, so `(3^3)^(2/3)=3^2`.

### B-M2 — common-base normalization
Solve `16^x=8^(x+1)`.

Expected: `x=3`.

Check: `2^(4x)=2^(3x+3)`.

### B-M3 — repeated power + positivity
Solve `9^x-7*3^x+12=0`.

Expected: `x=1` or `x=log_3 4`.

Check: `t=3^x>0`; `(t-3)(t-4)=0`.

### B-M4 — ratio normalization
Solve `9^x-5*6^x+4*4^x=0`.

Expected: `x=0` or `x=log_(3/2) 4`.

Check: divide by `4^x>0`; `t=(3/2)^x>0`; `(t-1)(t-4)=0`.

### B-M5 — WHY NOT
A student writes `2^1+2^2=2^(1+2)`. Diagnose the rule error.

Expected: false; exponent addition law belongs to multiplication of same-base powers. `2+4=6`, while `2^3=8`.

## 14. DIAGNOSTIC_TAGS

- `NEGATIVE_EXPONENT_RECIPROCAL_MISSED`
- `NEGATIVE_BASE_GROUPING_ERROR`
- `FALSE_EXPONENT_ADDITION_LAW`
- `EXPONENTIAL_BASES_NOT_NORMALIZED`
- `REPEATED_POWER_NOT_NAMED`
- `RATIO_VARIABLE_MISSED`
- `EXPONENTIAL_SUBSTITUTION_POSITIVITY_IGNORED`
- `UNNECESSARY_LOG_USE`
- `CALCULATION`

## 15. H3_TO_H0_FADE_PLAN

Every problem starts with H0. If rescue is needed, maximum available support fades:

- **H3 execution**: “Rewrite `16^x=2^(4x)` and `8^(x+1)=2^(3x+3)`.”
- **H2 structure**: “Put every base into one base.”
- **H1 recognition**: “The bases are related powers.”
- **H0 independent**: no cue.

For repeated-power items:

- H3: give `t=3^x>0` and the transformed polynomial;
- H2: “name the repeated exponential object”;
- H1: “this is ordinary algebra wearing exponential notation”;
- H0: learner chooses the substitution and positivity condition.

`W1-B_GATE: PASS_INTERFACE_READY_FOR_WAVE2`
