# Issue #45 — Wave 1E Interface
## Logarithms as exponents

`STATUS: W1_INTERFACE_COMPLETE`

`ROLE: INTERNAL_SUBTOPIC_INTERFACE`

This stream must prevent formula-list learning. The learner should be able to reconstruct logarithmic rules from exponent structure and choose log/exponent language deliberately.

## 1. CONCEPTS

- logarithm as inverse exponent statement;
- valid real base and argument conditions;
- product/quotient/power laws derived from exponent laws;
- exact inverse cancellation;
- change of base as a representation tool;
- injectivity of valid logarithm/exponential functions;
- exact structure before decimal approximation.

## 2. PREREQUISITES

- exponent laws;
- positive-base exponent behavior;
- simple equation solving;
- multiplication/division of powers.

## 3. RECOGNITION_CUES

| Visible cue | Structural recognition |
|---|---|
| `log_b x=y` | read as `b^y=x` |
| uncertain log law | derive it from exponent form |
| log and exponent use the same base | test exact inverse cancellation |
| related log bases | convert only if a common base reduces structure |
| `log(M+N)` | no sum law exists; do not imitate the product law |
| calculator temptation | preserve exact inverse/common-base form first |

## 4. FIRST_MOVES

1. Write the definition `log_b x=y <=> b^y=x` with `b>0`, `b!=1`, `x>0`.
2. If a law is uncertain, introduce exponent names and rebuild it instead of guessing.
3. If base-matched log/exponent inverse structure appears, simplify it before numerical work.
4. Use change of base only when it exposes a simpler relation.

## 5. INVARIANTS

For valid real logarithms:

- `log_b x` is exactly the exponent producing `x` from base `b`;
- product of positive arguments corresponds to addition of exponents;
- quotient corresponds to subtraction;
- powers correspond to scalar multiplication of the exponent;
- exponentiation and logarithm with the same valid base are inverse operations;
- argument positivity is never discarded by a representation switch.

## 6. REPRESENTATION_SWITCHES

- `b^y=x <-> log_b x=y`;
- `M=b^p`, `N=b^q` -> `MN=b^(p+q)` -> product law;
- `b^(log_b x) <-> x` for `x>0`;
- `log_b(b^y) <-> y` for valid base and real `y`;
- related log bases -> one common base when useful.

## 7. REVERSIBILITY_OR_DOMAIN_CONDITIONS

For ordinary real logarithms:

- base `b>0`, `b!=1`;
- every argument is positive;
- equality `log_b A=log_b B <=> A=B` is valid only after both arguments are known positive and the base is valid;
- `b^(log_b x)=x` requires `x>0`;
- derived log laws inherit positivity of all participating arguments.

## 8. DECISION_BOUNDARIES

`E-DB1 PRODUCT_LAW_vs_FALSE_SUM_LAW`  
`log_b(MN)` splits because exponents add under multiplication; no analogous rule exists for `M+N`.

`E-DB2 EXACT_INVERSE_vs_DECIMAL`  
Preserve a base-matched inverse pair before approximating.

`E-DB3 EXPONENT_NORMALIZATION_vs_TAKING_LOGS`  
If an exponential equation already normalizes to one base, logs are usually inferior.

`E-DB4 CHANGE_BASE_USEFUL_vs_CHANGE_BASE_REFLEX`  
Change base only if it shortens the relation or reveals a common exponent language.

`E-DB5 VALID_LOG_vs_SURFACE_ALGEBRA`  
A formally neat manipulation is invalid if its log argument/base is invalid.

## 9. MISCONCEPTION_TRAPS

- `log(a+b)=log a+log b`;
- treating a logarithm as an unexplained calculator button;
- forgetting `x>0` for an argument;
- allowing base 1 or a non-positive real base in ordinary real logarithms;
- approximating before exact cancellation;
- using change of base by reflex;
- taking logs when common-base exponent normalization already solves the problem.

## 10. CONTRAST_PAIRS

### CP-E1 — exponent statement vs log statement
`3^4=81` and `log_3 81=4` are the same fact in two languages.

### CP-E2 — product vs sum
- `log_b(MN)=log_b M+log_b N` under valid domains.
- `log_b(M+N)` does not split.

### CP-E3 — exact vs decimal
- `9^(log_3 5)` -> exact structure gives `25`.
- converting `log_3 5` to a decimal first is valid numerically but structurally inferior.

### CP-E4 — common base vs unnecessary logs
- `8^x=4^(x+1)` -> powers of 2.
- a genuinely non-normalizable exponential relation may need logarithms later.

## 11. TRANSFER_MECHANISMS

- rebuild log laws from exponent laws with no formula sheet;
- diagnose a false sum/difference log law;
- exact simplification of mixed log/exponent expressions;
- choose between common-base exponent normalization and logarithmic conversion;
- domain-invalid near-miss with otherwise identical algebra.

## 12. SOURCE_IDS_AND_DISPOSITIONS

### CLEAN_SCORED_ANCHOR / BRIDGE
- `NMTC-BH-P-2024-Q28` — exact log-exponent simplification;
- `NMTC-BH-P-2024-Q12` — transformed logarithmic quantity;
- `NMTC-BH-P-2025-Q12` — transformed `sqrt(log)` quantity;
- `NMTC-BH-P-2025-Q27` — log relation converted to algebra.

These PYQs assume foundational log meaning/laws; they do not replace author-created derivation teaching.

### AUTHOR_CREATED_FOUNDATION required
- definition-first log meaning;
- base/argument restrictions;
- derivation of product/quotient/power laws;
- false sum-law contrast;
- inverse cancellation and injectivity.

## 13. CANDIDATE_MASTERY_ITEMS

All are `AUTHOR_CREATED_TRANSFER` candidates.

### E-M1 — meaning
Convert `log_5 125=3` into exponent form and explain what the 3 means.

Expected: `5^3=125`; 3 is the exponent needed on base 5.

### E-M2 — domain + equation
Solve `log_3(x-2)=2`.

Expected: `x=11`.

Check: domain `x>2`; exponent form gives `x-2=9`.

### E-M3 — exact inverse structure
Evaluate exactly `9^(log_3 5)`.

Expected: `25`.

Check: `(3^2)^(log_3 5)=3^(2log_3 5)=5^2`.

### E-M4 — WHY NOT sum law
A student claims `log_2(1+3)=log_2 1+log_2 3`.

Expected diagnosis: false. Left side is `2`; right side is `log_2 3`. Product/quotient/power laws come from exponent structure; addition has no corresponding law.

### E-M5 — method-choice contrast
Solve `8^x=4^(x+1)` using the shortest structural route.

Expected: `x=2` by common-base normalization; taking logs is possible but inferior.

## 14. DIAGNOSTIC_TAGS

- `LOG_MEANING_NOT_CONNECTED_TO_EXPONENT`
- `FALSE_LOG_SUM_LAW`
- `LOG_DOMAIN_IGNORED`
- `INVALID_LOG_BASE`
- `EXACT_INVERSE_STRUCTURE_MISSED`
- `CHANGE_OF_BASE_BY_REFLEX`
- `UNNECESSARY_LOG_USE`
- `CALCULATION`

## 15. H3_TO_H0_FADE_PLAN

Every task starts H0. Rescue fades:

- **H3 execution**: “Write `log_b x=y <=> b^y=x` and substitute the given values.”
- **H2 structure**: “Translate the logarithm into exponent language.”
- **H1 recognition**: “A logarithm names an exponent.”
- **H0 independent**: learner chooses the representation.

For laws:

- H3: set `M=b^p`, `N=b^q` and multiply;
- H2: “derive from exponent multiplication”;
- H1: “which operation on arguments matches addition of exponents?”;
- H0: reconstruct unaided.

`W1-E_GATE: PASS_INTERFACE_READY_FOR_WAVE2`
