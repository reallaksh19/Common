# W1-F — Factor-Pair & Divisor Structure Interface

`ISSUE_AUTHORITY: #47`

`WAVE: 1F`

`STATUS: INTERFACE_COMPLETE`

## 1. CONCEPTS

- turn integrality into divisibility by a fixed constant;
- algebraic division / substitution before enumeration;
- factor-pair reconstruction;
- difference of squares;
- same-parity filter for `u-v, u+v`;
- sign/order/bound filters;
- coprimality as prime-factor separation;
- coprime product perfect-power principle.

## 2. PREREQUISITES

- factorization;
- divisors and prime factorization;
- gcd/coprimality;
- parity;
- rational expressions and denominator restrictions.

## 3. LIKELY_HALF_KNOWLEDGE

- can factor `a²-b²` but accepts every factor pair;
- tries many integer values in rational-integrality questions;
- checks only positive divisors even when all integers are allowed;
- forgets denominator-zero exclusions;
- knows `gcd(a,b)=1` but does not exploit disjoint prime supports;
- assumes a product being a square makes each factor a square even without coprimality.

## 4. RECOGNITION_CUES

- “expression is an integer”;
- denominator depends on integer `n`;
- difference of two squares plus divisibility or bounds;
- coprime factors with product a square/perfect power;
- finite divisor/factor-pair target hidden behind an infinite search.

## 5. FIRST_MOVES

1. Rewrite rational expressions as `integer part + C/g(n)` or substitute to isolate the denominator.
2. Convert integrality to `g(n)|C`.
3. For `u²-v²`, factor immediately.
4. Before solving from factor pairs, write parity/sign/order/bound conditions.
5. For coprime perfect-power products, move to prime-exponent allocation rather than numerical trial.

## 6. INVARIANTS

- integrality of `A(n)+C/g(n)` forces `g(n)|C`;
- `u-v` and `u+v` have the same parity;
- if positive `a,b` are coprime and `ab` is a perfect `k`th power, then each prime exponent stays wholly within one factor and must be divisible by `k`;
- factorization changes the representation, not the integer constraints.

## 7. REPRESENTATION_SWITCHES

- rational expression -> quotient + remainder form;
- hidden linear denominator -> substitution such as `t=2n-1`;
- square difference -> product of two factors;
- factor pair `(r,s)` -> `u=(r+s)/2`, `v=(s-r)/2`;
- coprime product -> prime exponent vectors.

## 8. LEGALITY / ADMISSIBILITY CONDITIONS

- denominator cannot be zero;
- divisor sign set depends on whether integers, positive integers or naturals are allowed;
- factor-pair reconstruction requires parity compatibility;
- positivity/order/bounds must be checked after algebraic factorization;
- coprime-product-to-individual-perfect-power inference requires coprimality and appropriate positivity/nonzero assumptions.

## 9. DECISION_BOUNDARIES

**DB-F1 divisor reduction vs trial**  
`(n+5)/(n+1)` integer -> `1+4/(n+1)`; finite divisor list beats trial.

**DB-F2 factorization vs expansion**  
`k²-n²=96` -> factor pairs, not square-table guessing.

**DB-F3 factor pair vs admissible factor pair**  
For difference of squares, opposite-parity factor pairs cannot reconstruct integer `k,n`.

**DB-F4 coprime product vs arbitrary product**  
`2·8=16` is a square but 2 and 8 are not squares; gcd is 2. Coprimality is the missing condition.

## 10. MISCONCEPTION_TRAPS

- brute-force testing `n`;
- forgetting negative divisors;
- accepting denominator zero;
- using every factor pair without parity filtering;
- assuming gcd=1 is decorative;
- promoting `ab` square -> each factor square without coprimality.

## 11. CONTRAST_PAIRS

1. `(n+5)/(n+1)` -> fixed remainder 4; `(n²+1)/(n+1)` may require polynomial division first.
2. Factor pair `(2,48)` for product 96 has same parity and can reconstruct integers; `(3,32)` has opposite parity and cannot.
3. Coprime 9 and 25 multiply to a square and are individually squares; non-coprime 2 and 8 show why the condition matters.

## 12. TRANSFER_MECHANISMS

- substitution that turns a quadratic-looking integrality condition into `t|C`;
- difference-of-squares under a range bound;
- recover all integer pairs rather than only positive pairs;
- product is a cube/perfect fourth power rather than square;
- combine coprimality with consecutive integers.

## 13. SOURCE_IDS_AND_DISPOSITIONS

Clean scored anchors:
- `NMTC-BH-P-2018-Q10` — coprimality -> divisor restrictions;
- `NMTC-BH-P-2018-Q18` — difference of squares + same-parity factor pairs;
- `NMTC-BH-P-2018-Q19` — algebraic reduction + integrality/perfect-square filtering;
- `NMTC-BH-P-2019-Q27` — difference of squares + divisibility + bounds;
- `NMTC-BH-P-2023-Q18` — coprime consecutive product square;
- `NMTC-BH-P-2025-Q26` — `t=2n-1` -> `t|25`.

## 14. CANDIDATE_MASTERY_ITEMS

`F-M1` Find positive integers `n` for which `(n+5)/(n+1)` is an integer.

`F-M2` Find positive integer pairs `k>n` satisfying `k²-n²=96`.

`F-M3` Explain why factor pair `(3,32)` cannot arise as `(k-n,k+n)` for integers.

`F-M4` If positive coprime integers `a,b` have `ab` a perfect square, prove each is a square; then give a counterexample when coprimality is removed.

`F-M5` Let odd positive `t=2n-1` and suppose an expression reduces to integrality condition `t|25`. List possible positive `n`.

Independent check:
- F-M1: `n+1|4`, positive `n`: `n+1=2,4`, so `n=1,3`;
- F-M2: same-parity positive factor pairs of 96: `(2,48),(4,24),(6,16),(8,12)` -> `(k,n)=(25,23),(14,10),(11,5),(10,2)`, four pairs;
- F-M3: factors have opposite parity, so half-sum/half-difference are not both integers;
- F-M4: prime-exponent proof; counterexample `2·8=16`;
- F-M5: positive odd divisors `1,5,25` -> `n=(t+1)/2=1,3,13`.

## 15. DIAGNOSTIC_TAGS

- `INTEGRALITY_BRUTE_FORCE`
- `DENOMINATOR_ZERO_IGNORED`
- `NEGATIVE_DIVISORS_OMITTED`
- `FACTOR_PAIR_PARITY_MISSED`
- `BOUND_FILTER_MISSING`
- `COPRIMALITY_UNUSED`
- `PERFECT_POWER_INFERENCE_OVERGENERALIZED`

## 16. H3_TO_H0_FADE_PLAN

- `F-F1 H3`: perform the algebraic division/substitution and ask learner to enumerate divisors.
- `F-F2 H2`: cue “make the denominator divide a constant” or “factor into two same-parity factors.”
- `F-F3 H1`: point only to “integer-valued” / “difference of squares” / “coprime product.”
- `F-F4 H0`: mixed unlabelled item requiring independent selection of divisor reduction, factor-pair filters or prime-exponent reasoning.

`W1-F_GATE: PASS`