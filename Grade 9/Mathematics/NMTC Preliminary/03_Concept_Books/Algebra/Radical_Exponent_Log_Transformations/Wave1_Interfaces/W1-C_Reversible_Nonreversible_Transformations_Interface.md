# Issue #45 — Wave 1C Interface
## Reversible vs non-reversible transformations

`STATUS: W1_INTERFACE_COMPLETE`

`ROLE: INTERNAL_SUBTOPIC_INTERFACE`

This stream is the logical spine that Wave 2 must weave through radicals, exponents and logarithms. It must not be isolated as a one-page warning box.

## 1. CONCEPTS

- equivalent equations versus candidate-generating equations;
- injective versus non-injective transformations on the relevant real domain;
- squaring versus cubing;
- principal-root side-sign conditions;
- multiplication/division by a variable expression that may vanish;
- domain ledger before transformation;
- original-equation verification;
- distinct original solutions versus multiplicity in a transformed polynomial.

## 2. PREREQUISITES

- solve linear/quadratic equations;
- understand zero product;
- basic function idea: two inputs may or may not map to the same output;
- routine substitution check.

## 3. RECOGNITION_CUES

| Planned move | Question to ask first |
|---|---|
| square both sides | is the step reversible on the current sign/domain? |
| cube both sides over reals | cubing is one-to-one, so equivalence is available |
| divide by `g(x)` | can `g(x)=0`? |
| multiply by `g(x)` | can a zero value erase information and create candidates? |
| remove a square root | what sign/domain restrictions are already implied? |
| solve transformed polynomial | are these roots solutions or only candidates? |

## 4. FIRST_MOVES

1. Write the original real-domain and side-sign restrictions.
2. Mark each risky transformation as `<=>` only when both directions are justified; otherwise use `=>`.
3. Before dividing by a variable expression, split/check the zero case.
4. After a candidate-generating step, verify every candidate in the original equation.

## 5. INVARIANTS

- the original problem defines the authoritative solution set;
- reversible transformations preserve that set exactly;
- non-injective transformations may enlarge the candidate set;
- division by a zero-capable factor can shrink the solution set if the zero case is discarded;
- domain/sign restrictions remain active even after the original radicals/logs disappear.

## 6. REPRESENTATION_SWITCHES

Use arrows explicitly:

- `A <=> B` — both directions valid on the stated domain;
- `A => B` — every solution of `A` satisfies `B`, but `B` may contain extra candidates.

Maintain a compact ledger:

```text
D0 ORIGINAL DOMAIN: ...
D1 NON-ZERO / SIGN CONDITIONS: ...
TRANSFORM: <=> or =>
ALGEBRAIC CANDIDATES: ...
ORIGINAL CHECK: ...
VALID SOLUTIONS: ...
```

## 7. REVERSIBILITY_OR_DOMAIN_CONDITIONS

- squaring: `a=b => a^2=b^2`; converse fails without additional sign information;
- cubing over reals: `a=b <=> a^3=b^3`;
- `sqrt(F(x))=G(x)` requires `F(x)>=0` and `G(x)>=0` before squaring can become equivalent;
- division by `g(x)` is equivalent only after ensuring `g(x)!=0` or separately preserving the zero case;
- logarithmic transformations inherit positive-argument and valid-base conditions even after conversion to algebra.

## 8. DECISION_BOUNDARIES

`C-DB1 SQUARE_vs_CUBE`  
Square is many-to-one over reals; cube is one-to-one.

`C-DB2 CONSTANT_FACTOR_vs_VARIABLE_FACTOR`  
A known nonzero constant can be divided safely; a variable expression requires a zero-case check.

`C-DB3 CANDIDATE_vs_SOLUTION`  
A transformed root is not automatically an original root.

`C-DB4 PRINCIPAL_ROOT_vs_PLUS_MINUS`  
The radical symbol gives a principal value; `±` belongs to solving an equation such as `u^2=a`.

`C-DB5 ISOLATE_THEN_SQUARE_vs_SQUARE_EARLY`  
Both can be legal, but isolation reduces cross terms and makes sign/domain logic visible.

## 9. MISCONCEPTION_TRAPS

- “doing the same thing to both sides” treated as automatic equivalence;
- accepting all roots after squaring;
- dividing by `x-a` and silently losing `x=a`;
- treating cubing as if it had the same sign ambiguity as squaring;
- accepting multiplicity in a transformed polynomial as multiple distinct original solutions;
- reconstructing domain only at the end instead of carrying it throughout.

## 10. CONTRAST_PAIRS

### CP-C1 — squaring vs cubing
- `x=-2` implies `x^2=4`, but `x^2=4` does not imply `x=-2`.
- `x^3=8 <=> x=2` over the reals.

### CP-C2 — divide safely vs lose a zero case
- `5(x+1)=10` -> divide by 5 safely.
- `(x-2)(x+5)=3(x-2)` -> dividing by `x-2` loses the possible case `x=2`.

### CP-C3 — candidate vs verified solution
- after squaring `sqrt(x+6)=x`, algebra gives `x=3,-2`;
- original domain/equation leaves only `x=3`.

### CP-C4 — principal root vs equation roots
- `sqrt(9)=3`;
- `u^2=9` gives `u=±3`.

## 11. TRANSFER_MECHANISMS

- radical equation that generates exactly one extraneous candidate;
- factor equation where naive division loses a valid solution;
- mixed transformation chain requiring the learner to label each arrow `<=>` or `=>`;
- log-to-algebra problem where an algebraic branch violates the original log domain;
- source-integrity case where key/multiplicity language conflicts with the original real equation.

## 12. SOURCE_IDS_AND_DISPOSITIONS

### CLEAN_SCORED_ANCHOR
- `NMTC-BH-P-2018-Q26` — radical-ratio transformation with checking.

### SOURCE_CONFLICT_EVIDENCE
- `NMTC-BH-P-2025-Q18` — printed real cube-root equation versus provisional-key root/multiplicity convention. Use only for source/convention QC; do not repair or convert to a clean canonical exercise.

### AUTHOR_CREATED_FOUNDATION required
- explicit `<=>` versus `=>` exercises;
- divide-by-zero-capable-factor examples;
- square-versus-cube contrasts;
- domain-ledger drills.

## 13. CANDIDATE_MASTERY_ITEMS

All are `AUTHOR_CREATED_TRANSFER` candidates.

### C-M1 — extraneous candidate
Solve `sqrt(x+6)=x` over the reals.

Expected: `x=3` only.

Independent check: original requires `x>=0`; squaring gives `x^2-x-6=0`, candidates `3,-2`; `-2` is invalid.

### C-M2 — zero case lost by division
Solve `(x-2)(x+5)=3(x-2)`.

Expected: `x=2,-2`.

Check: move terms and factor `(x-2)(x+2)=0`. Dividing by `x-2` would lose `x=2`.

### C-M3 — arrow classification
Classify each as `<=>` or `=>` over the reals:

1. `x=-2` to `x^2=4`;
2. `x^3=8` to `x=2`;
3. `sqrt(x+1)=x-1` to `x+1=(x-1)^2` without first imposing `x>=1`.

Expected: `=>`, `<=>`, `=>` respectively.

### C-M4 — equivalence after securing sign
For `sqrt(x+1)=x-1`, first impose `x>=1`. Then explain why squaring becomes equivalent on this restricted domain.

Expected reasoning: both sides are nonnegative; for nonnegative real `A,B`, `A=B <=> A^2=B^2`.

### C-M5 — source/convention discipline
A transformed polynomial has a repeated root, while the printed original real equation has one distinct solution. What must be counted if the source asks for distinct original solutions?

Expected: count the distinct solutions of the original equation; transformed multiplicity is not silently substituted. If the source/key disagrees, preserve a `SOURCE_CONFLICT_EVIDENCE` record.

## 14. DIAGNOSTIC_TAGS

- `EQUIVALENCE_ASSUMED_WITHOUT_PROOF`
- `EXTRANEOUS_ROOT_NOT_CHECKED`
- `ZERO_CASE_LOST_BY_DIVISION`
- `PRINCIPAL_ROOT_PLUS_MINUS_CONFUSION`
- `DOMAIN_LEDGER_DROPPED`
- `TRANSFORMED_MULTIPLICITY_CONFUSED_WITH_ORIGINAL_SOLUTIONS`
- `SQUARED_TOO_EARLY`
- `SOURCE_CONFLICT_NOT_FLAGGED`

## 15. H3_TO_H0_FADE_PLAN

All tasks begin H0. Rescue support fades:

- **H3 execution**: “Write `x>=0`, then square and factor.”
- **H2 structure**: “This transformation can create candidates; keep an original-domain ledger.”
- **H1 recognition**: “Is the next operation one-to-one?”
- **H0 independent**: learner labels arrows and filters candidates without cues.

For zero-factor items:

- H3: explicitly split `x-2=0` and `x-2!=0`;
- H2: “check the factor before dividing”;
- H1: “can your divisor be zero?”;
- H0: no prompt.

`W1-C_GATE: PASS_INTERFACE_READY_FOR_WAVE2`
