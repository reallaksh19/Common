# Issue #45 — Wave 1A Interface
## Common radical basis & surd structure

`STATUS: W1_INTERFACE_COMPLETE`

`ROLE: INTERNAL_SUBTOPIC_INTERFACE`

This is not student prose. It is the compact contract that Wave 2 must teach through `RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`.

## 1. CONCEPTS

- extracting perfect square/cube/nth-power factors;
- common irreducible radical basis;
- radical <-> fractional-exponent representation;
- reverse recognition of hidden binomial squares/cubes;
- conjugate structure;
- principal square-root meaning;
- rationalization as an optional structural move, not a ritual.

## 2. PREREQUISITES

Learner should already be able to:

- factor integers and simple monomials;
- use `(a+b)^2`, `(a-b)^2`, `(a+b)(a-b)`;
- simplify one routine radical;
- understand absolute value on the real line.

If these fail, route to foundation repair rather than treating the failure as an NMTC transformation failure.

## 3. RECOGNITION_CUES

| Visible cue | What the learner should notice |
|---|---|
| several radicals with related radicands | they may share one small radical generator |
| `A ± Bsqrt(d)` or a nested radical | the expression may already be a square/cube |
| conjugate pair | sum/product/difference may collapse before expansion |
| `sqrt(g(x)^2)` | principal-root sign is active |
| denominator with a conjugate | rationalization may help, but only if it exposes structure |
| fractional power of a surd | reconstruct the base before raising the power |

## 4. FIRST_MOVES

1. Extract perfect powers and write all terms in a common radical basis.
2. For `A ± Bsqrt(d)`, test a reverse square/cube identity before expanding or approximating.
3. For `sqrt(g(x)^2)`, write `|g(x)|` unless a sign condition removes the absolute value.
4. For conjugates, inspect product/sum symmetry before rationalizing term-by-term.

## 5. INVARIANTS

- correctly rewritten radicals represent the same real quantity;
- the non-perfect radical core is the useful basis element;
- a hidden binomial square preserves its exact value when reconstructed;
- principal square root is always non-negative;
- conjugate multiplication removes the irrational cross term.

## 6. REPRESENTATION_SWITCHES

- `sqrt(k m^2) <-> |m|sqrt(k)` for real variable `m`;
- `nthroot(a^r) <-> a^(r/n)` only under the intended real-domain interpretation;
- `A ± Bsqrt(d) <-> (sqrt(m) ± sqrt(n))^2` when coefficient matching works;
- `u+v, u-v` <-> conjugate pair;
- denominator-with-surd <-> conjugate product when rationalization is useful.

## 7. REVERSIBILITY_OR_DOMAIN_CONDITIONS

- `sqrt(x^2)=|x|`, not `x` and not `±x`;
- product splitting for square roots requires real-domain care; a sum never acquires a corresponding distribution law;
- even roots require non-negative radicands in ordinary real work;
- odd roots preserve sign over the reals;
- when reconstructing `sqrt(H^2)`, the answer is `|H|`; only a known sign lets us remove the absolute value.

## 8. DECISION_BOUNDARIES

`A-DB1 COMMON_BASIS_vs_HIDDEN_POWER`  
Many related radicals -> reduce basis. A deliberately structured `A ± Bsqrt(d)` -> test reverse square/cube first.

`A-DB2 PRODUCT_vs_SUM_RADICAL`  
A product can sometimes split under valid conditions; a sum generally cannot.

`A-DB3 PRINCIPAL_ROOT_vs_EQUATION_ROOTS`  
`sqrt(x^2)` is one non-negative quantity; solving `u^2=x^2` asks for possible values of `u`.

`A-DB4 RATIONALIZE_vs_STRUCTURE_FIRST`  
Rationalization is useful only if it simplifies or exposes the target structure.

`A-DB5 EVEN_ROOT_vs_ODD_ROOT`  
Even roots impose non-negativity; odd roots are one-to-one on the reals.

## 9. MISCONCEPTION_TRAPS

- `sqrt(a+b)=sqrt(a)+sqrt(b)`;
- `sqrt(x^2)=x` for all real `x`;
- radical symbol interpreted as `±`;
- direct expansion of a high/fractional power when the base is a hidden square;
- automatic rationalization that makes the expression longer;
- ignoring sign after reconstructing a square.

## 10. CONTRAST_PAIRS

### CP-A1 — common basis vs false distribution
- `sqrt(12)+sqrt(27)` -> reduce both to multiples of `sqrt(3)`.
- `sqrt(12+27)` -> do **not** distribute the root over the sum.

### CP-A2 — principal root vs solving a square equation
- simplify `sqrt((x-4)^2)` -> `|x-4|`.
- solve `y^2=(x-4)^2` -> `y=±(x-4)`.

### CP-A3 — reconstruct vs expand
- `sqrt(19-6sqrt(10))` -> recognize `(sqrt(10)-3)^2`.
- an unstructured surd sum -> common-basis/factor route instead.

### CP-A4 — rationalization useful vs inferior
- denominator obstructs simplification -> conjugate may help.
- conjugate pair already appears symmetrically in a sum/product -> combine first.

## 11. TRANSFER_MECHANISMS

- mixed square/cube/nth-root expression where the shared radical core is hidden;
- fractional-exponent surd where reverse reconstruction turns a long expansion into a short cube;
- variable expression where principal-root sign creates a piecewise/absolute-value result;
- conjugate expression where rationalizing each fraction separately is valid but structurally inferior.

## 12. SOURCE_IDS_AND_DISPOSITIONS

### CLEAN_SCORED_ANCHOR
- `NMTC-BH-P-2018-Q01` — common square-root basis;
- `NMTC-BH-P-2023-Q21` — nested-radical reconstruction;
- `NMTC-BH-P-2023-Q26` — common cube-root basis;
- `NMTC-BH-P-2024-Q26` — structured radical normalization;
- `NMTC-BH-P-2025-Q03` — common nth-root factor;
- `NMTC-BH-P-2025-Q04` — conjugate surd square/cube.

### SOURCE_SENSITIVE_EVIDENCE
- `NMTC-BH-P-2023-Q04` — cube-root identity mechanism only; notation/options remain sensitive.

### AUTHOR_CREATED_FOUNDATION required
- principal-root sign;
- legal/illegal radical distribution;
- rationalization method choice;
- variable-domain examples.

No full third-party statement should be reproduced merely because an ID is listed here.

## 13. CANDIDATE_MASTERY_ITEMS

All are `AUTHOR_CREATED_TRANSFER` candidates.

### A-M1 — common basis
Simplify `(sqrt(108)-sqrt(12))/sqrt(3)`.

Expected: `4`.

Independent check: `sqrt108=6sqrt3`, `sqrt12=2sqrt3`.

### A-M2 — hidden square + sign
Simplify `sqrt(19-6sqrt(10))`.

Expected: `sqrt(10)-3`.

Check: `(sqrt10-3)^2=19-6sqrt10` and `sqrt10-3>0`.

### A-M3 — principal-root boundary
Simplify `sqrt((2x-5)^2)` and state when it equals `2x-5`.

Expected: `|2x-5|`; it equals `2x-5` iff `x>=5/2`.

### A-M4 — rationalization is not the goal
Evaluate `1/(sqrt7+sqrt5)+1/(sqrt7-sqrt5)` by the shortest exact route.

Expected: `sqrt7`.

Check: combine over `(sqrt7)^2-(sqrt5)^2=2`; numerator is `2sqrt7`.

## 14. DIAGNOSTIC_TAGS

- `RADICAL_COMMON_BASIS_MISSED`
- `FALSE_RADICAL_DISTRIBUTION`
- `HIDDEN_SURD_NOT_RECONSTRUCTED`
- `PRINCIPAL_ROOT_SIGN_ERROR`
- `RATIONALIZATION_BY_REFLEX`
- `EVEN_ODD_ROOT_BOUNDARY_MISSED`
- `CALCULATION`

## 15. H3_TO_H0_FADE_PLAN

Every item begins with an H0 attempt. If support is needed, the **maximum available rescue** fades across adjacent practice:

- **H3 execution**: “Rewrite `sqrt(108)=6sqrt3` and `sqrt(12)=2sqrt3`.”
- **H2 structure**: “Find the common irreducible radical basis.”
- **H1 recognition**: “These radicals share a hidden basis.”
- **H0 independent**: no cue; learner chooses the representation.

For hidden surds:

- H3: give `m+n=A`, `2sqrt(mn)=Bsqrt(d)`;
- H2: say “reverse a binomial square”;
- H1: say “the inside looks engineered”;
- H0: no label.

`W1-A_GATE: PASS_INTERFACE_READY_FOR_WAVE2`
