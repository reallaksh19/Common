# Radicals, Exponents & Logarithmic Transformations — First-Step Reference v2

`ISSUE_AUTHORITY: #45`

`WAVE: 3 — FIRST_STEP_COMPRESSION`

`STATUS: FIRST_STEP_REFERENCE_COMPLETE_INTERNAL`

This is a **compression layer after the Wave-2 Assimilation Book**. It is not the teaching book and must not replace it.

Use it when you already understand the ideas and need to answer quickly:

> **What did I notice? What is the first useful move? What condition must I carry? What tempting move should I reject?**

Routine:

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

---

# 1. The 10-second decision tree

```text
START
 |
 |-- Several radicals / nth roots?
 |      |
 |      |-- same irreducible residue? -> COMMON BASIS
 |      |-- A ± B√d / nested radical / fractional surd power? -> HIDDEN POWER
 |      |-- equation with even roots? -> DOMAIN -> ISOLATE -> SQUARE ONLY IF NEEDED
 |
 |-- Powers / exponential expression?
 |      |
 |      |-- negative/fractional exponent meaning unstable? -> RECIPROCAL / RADICAL LANGUAGE
 |      |-- related bases? -> NORMALIZE BASES
 |      |-- a^(2x), a^x, constant? -> t = a^x, record t>0
 |      |-- homogeneous two-base pattern? -> divide by positive power -> ratio variable
 |
 |-- x and 1/x appear symmetrically?
 |      |
 |      |-- symmetric target? -> RECIPROCAL INVARIANT / RECURRENCE
 |      |-- asymmetric target? -> may need more information / explicit x
 |
 |-- Logarithms?
 |      |
 |      |-- meaning/law uncertain? -> LOG <-> EXPONENT
 |      |-- log object repeats? -> substitute the WHOLE repeated object
 |      |-- equal logs / related bases? -> DOMAIN -> COMMON BASE / POWER RELATION
 |      |-- exponent and log share a base? -> EXACT INVERSE BEFORE DECIMALS
 |
 |-- Any risky transformation?
        |
        |-- squaring? -> candidate risk / sign ledger
        |-- divide by g(x)? -> check g(x)=0 first
        |-- substitution with restricted range? -> carry the range
        |-- source/key disagreement? -> recompute, then preserve source disposition
```

---

# 2. Recognition atlas

| Code | What you see | What it usually means | First move |
|---|---|---|---|
| `CB` | several related square/cube/nth roots | one common radical basis is hidden | extract perfect powers; rewrite all terms in the same basis |
| `HS` | `A±B√d`, nested radical, surd to `1/2` or `3/2` power | expression may already be a binomial square/cube | reverse an identity before expanding |
| `PR` | `√(g(x)^2)` | principal square root controls the sign | write `|g(x)|` unless sign is known |
| `EM` | negative/fractional exponent | reciprocal or radical meaning is the real structure | rewrite explicitly as reciprocal/radical before manipulating |
| `EN` | bases like `2,4,8` or `3,9,27` | same-base normalization may remove the exponential difficulty | rewrite all bases first |
| `EV` | `a^(2x), a^x, 1` | low-degree algebra in one positive exponential variable | set `t=a^x`, write `t>0` |
| `ER` | homogeneous mixtures such as `9^x,6^x,4^x` | ratio variable is cheaper than separate powers | divide by a positive common power; set a ratio variable |
| `RQ` | square-root equation | even-power transformation may lose sign information | write domain/sign conditions; isolate before squaring |
| `ZR` | temptation to divide by `g(x)` | zero case may be lost | test/split `g(x)=0` before division |
| `RI` | `x^n+x^-n` or symmetry under `x↔1/x` | target may depend only on `x+1/x` | define reciprocal invariant; use recurrence |
| `LD` | simple log statement / forgotten law | logarithm is exponent language | convert `log_b y=z` to `b^z=y` |
| `LV` | repeated `log_b x` | one algebraic variable is hidden | set `t=log_b x`; preserve `x>0` |
| `LS` | repeated `√(log_b x)` | the whole outer object is the efficient variable | set `u=√(log_b x)`, write `u≥0` |
| `LA` | equal logs / different related log bases | a simple power relation may be hidden | check domain, then convert to common base / exponent form |
| `LI` | `b^(log_b y)` or compatible power/log bases | exact inverse cancellation is intended | rewrite exactly before approximating |
| `DR` | transformed roots/candidates | transformed algebra may not equal original problem | restore all domain/sign/range conditions and check original |
| `QC` | printed key disagrees with verified mathematics | possible source conflict, not permission to change the problem | recompute independently; classify source disposition |

---

# 3. Phrase / structure decoder

| Phrase or visual structure | Translate it mentally into |
|---|---|
| “simplify several radicals” | “Do they share one irreducible radical basis?” |
| `A±B√d` | “Can I run `(√m±√n)^2` backwards?” |
| “rationalize” | “Will conjugation expose useful structure, or is another representation shorter?” |
| `√(x^2)` | “principal root = `|x|`” |
| negative exponent | “reciprocal, not negative value” |
| fractional exponent | “radical language” |
| related exponential bases | “normalize before logs” |
| repeated exponential power | “name the repeated positive object” |
| `x + 1/x` known | “build symmetric powers; do not solve x unless needed” |
| “square both sides” | “Is this equivalence or only candidate generation?” |
| divide by expression | “Could this expression be zero?” |
| `log_b x` | “the exponent that turns b into x” |
| repeated `√(log_b x)` | “substitute the whole repeated object; carry non-negativity” |
| equal logs | “first check arguments/base, then use injectivity” |
| exponent with matching log | “exact inverse structure before decimals” |
| answer key seems impossible | “mathematics first, provenance second; never force the key” |

---

# 4. First-Step cards

## Card 1 — Common radical basis `CB`

**SEE:** `√72`, `√8`, `√2` in the same expression.

**WRITE:** extract perfect powers until all terms use the same irreducible radical.

**CHOOSE:** combine only after normalization.

**CHECK:** no false distribution over addition.

**Reject:** `√(a+b)=√a+√b`.

---

## Card 2 — Hidden surd `HS`

**SEE:** `A±B√d`, nested radical, or a surd base raised to `3/2`.

**WRITE:** test `A±B√d=(√m±√n)^2`.

**CHOOSE:** reconstruct before applying the outer power.

**CHECK:** square the proposed reconstruction and check the sign of the principal root.

**Reject:** blind expansion / early decimals.

---

## Card 3 — Principal root `PR`

**SEE:** `√(g(x)^2)`.

**WRITE:** `|g(x)|`.

**CHOOSE:** remove the absolute value only after proving the sign.

**CHECK:** radical notation gives one non-negative value; solving a square equation may give two signs.

---

## Card 4 — Exponent meaning `EM`

**SEE:** negative or fractional exponent.

**WRITE:** `a^(-n)=1/a^n` for `a≠0`; translate fractional powers into root language when useful.

**CHOOSE:** stabilize the meaning before applying exponent laws.

**Reject:** treating a negative exponent as a negative value or confusing `a^-n` with `(-a)^n`.

---

## Card 5 — Exponent normalization `EN`

**SEE:** related bases.

**WRITE:** rewrite every base as a power of the same base.

**CHOOSE:** equate exponents only after base normalization with a valid positive base not equal to 1.

**Reject:** taking logarithms when normalization already makes the structure algebraic.

---

## Card 6 — Exponential variable `EV`

**SEE:** `a^(2x), a^x, constant`.

**WRITE:** `t=a^x`, `t>0`.

**CHOOSE:** solve the low-degree algebra in `t`, filter by `t>0`, map back.

**Reject:** accepting a negative polynomial root as an exponential value.

---

## Card 7 — Exponential ratio `ER`

**SEE:** homogeneous powers of two bases, e.g. `9^x,6^x,4^x`.

**WRITE:** divide by a known positive power, then set a ratio such as `t=(3/2)^x`.

**CHECK:** `t>0`.

---

## Card 8 — Radical equation / reversibility `RQ`

**SEE:** even roots in an equation.

**WRITE:** domain + side-sign restrictions first.

**CHOOSE:** isolate before squaring.

**ARROW:** use `<=>` only if both directions are secured on the carried domain; otherwise use `=>` and verify candidates.

**CHECK:** substitute candidates into the original equation.

---

## Card 9 — Zero-case protection `ZR`

**SEE:** temptation to divide by `g(x)`.

**WRITE:** `g(x)=0?`

**CHOOSE:** preserve the zero case before dividing.

**Reject:** cancelling a variable factor as though it were a known non-zero constant.

---

## Card 10 — Reciprocal invariant `RI`

**SEE:** symmetry under `x↔1/x`.

**WRITE:** `S1=x+1/x`, with `x≠0`; for `S_n=x^n+x^-n`, use `S0=2`, `S_n=S1*S_(n-1)-S_(n-2)`.

**CHOOSE:** compute the invariant directly.

**Reject:** solving the quadratic for `x` unless the target is asymmetric.

---

## Card 11 — Log definition `LD`

**SEE:** a log law or log meaning is uncertain.

**WRITE:** `log_b y=z <=> b^z=y`, with `b>0`, `b≠1`, `y>0`.

**CHOOSE:** derive the law from exponent structure if needed.

**Reject:** a fabricated sum/difference law.

---

## Card 12 — Log variable `LV / LS`

**SEE:** one log object repeats.

**WRITE:** choose the **whole repeated object**.

- repeated `log_b x` -> `t=log_b x`;
- repeated `√(log_b x)` -> `u=√(log_b x)`, `u≥0`.

**CHECK:** restore `x>0` and any stronger original argument restrictions.

---

## Card 13 — Log to algebra `LA`

**SEE:** equal logs or related bases connecting variables.

**WRITE:** domain first, then common-base / exponent form.

**CHOOSE:** convert to a simple algebraic power relation and solve there.

**CHECK:** every returned value must keep all original log arguments positive.

---

## Card 14 — Exact inverse `LI`

**SEE:** exponent and logarithm with compatible bases.

**WRITE:** expose `b^(log_b y)` or equivalent.

**CHOOSE:** simplify exactly.

**Reject:** calculator approximation before structural cancellation.

---

## Card 15 — Domain/reversibility audit `DR`

Before accepting a transformed answer ask:

1. original radical/log domain satisfied?
2. principal-root side sign satisfied?
3. substitution range satisfied (`t>0`, `u≥0`, etc.)?
4. zero case preserved?
5. transformation was `<=>` or only `=>`?
6. candidate checked in the original if needed?

---

## Card 16 — Source integrity `QC`

**SEE:** source/key conflicts with valid recomputation.

**WRITE:** keep three separate records: `PRINTED SOURCE | DERIVED MATHEMATICS | KEY / DISPOSITION`.

**CHOOSE:** preserve the conflict.

**Reject:** changing a sign, root convention, option or interpretation merely to make the key work.

---

# 5. The six boundary questions

1. **Basis or hidden power?** Are radicals meant to combine after normalization, or is one structured surd meant to be reconstructed?
2. **Exponent meaning, normalization, or logarithm?** Is the issue reciprocal/root meaning, related bases, or genuinely unrelated bases?
3. **Equivalent or candidate-generating?** Does the transformation preserve both directions?
4. **Invariant or explicit variable?** Is the requested target symmetric under `x↔1/x`?
5. **Which repeated object?** Is it `log_b x`, `√(log_b x)`, or another larger repeated structure?
6. **Algebraic candidate or original solution?** Did all original sign/domain/range conditions survive?

---

# 6. Quick arrow guide — `<=>` or `=>`?

| Transformation | Default status | What can change it? |
|---|---|---|
| add/subtract same expression | `<=>` where defined | domain of expressions still matters |
| multiply/divide by known non-zero constant | `<=>` | none |
| divide by `g(x)` | conditional | separately handle/prove `g(x)≠0` |
| square both sides | usually `=>` | becomes `<=>` if both sides are known non-negative (or both known non-positive with care) |
| cube both sides over reals | `<=>` | real-domain assumption |
| `log_b y=z` to `b^z=y` | `<=>` | valid base and positive argument |
| equal valid same-base logs -> equal arguments | `<=>` | both logs must exist |
| `t=a^x` | representation change with `t>0` | mapping back must respect valid base |
| `u=√(log_b x)` | representation change with `u≥0` | also preserve original log domain |

---

# 7. Common traps — one-line repair statements

| Trap | Repair statement |
|---|---|
| `√(a+b)=√a+√b` | radical multiplication behavior does not distribute over sums |
| `√(x^2)=x` | write `|x|`; remove bars only after a sign argument |
| radical symbol interpreted as `±` | `√A` is the principal non-negative root; `u^2=A` is different |
| `a^-n` treated as negative | negative exponent means reciprocal |
| exponent law used across addition | exponent addition law belongs to multiplication of same bases |
| logs used immediately | normalize related bases first |
| negative root accepted for `t=a^x` | exponential substitution carries `t>0` |
| square-root equation squared immediately | write domain/sign; isolate first |
| every same-operation step called equivalent | test injectivity / zero cases |
| divide by variable factor | preserve its zero case |
| solve `x` for reciprocal symmetric target | compute the invariant directly |
| `log(a+b)` split | no logarithm sum law |
| log restriction forgotten after logs disappear | original domain remains authoritative |
| `u=√(log_b x)` allowed negative | definition forces `u≥0` |
| exact log/exponent expression approximated | expose inverse structure first |
| source altered to match key | preserve source conflict after independent recomputation |

---

# 8. Source-to-mechanism map

Historical IDs ground mechanisms only; full third-party statements are not reproduced.

| Mechanism | Clean scored evidence | Other disposition |
|---|---|---|
| common radical basis | `NMTC-BH-P-2018-Q01`, `NMTC-BH-P-2023-Q26`, `NMTC-BH-P-2025-Q03` | — |
| hidden/nested surd reconstruction | `NMTC-BH-P-2023-Q21`, `NMTC-BH-P-2024-Q26`, `NMTC-BH-P-2025-Q04` | `NMTC-BH-P-2023-Q04` source-sensitive bridge |
| radical equation / checking | `NMTC-BH-P-2018-Q26` | `NMTC-BH-P-2025-Q18` source-conflict QC only |
| reciprocal invariant | `NMTC-BH-P-2018-Q21`, `NMTC-BH-P-2025-Q09` | — |
| exponent normalization/substitution | `NMTC-BH-P-2023-Q07`, `NMTC-BH-P-2024-Q04`, `NMTC-BH-P-2024-Q09` | `NMTC-BH-P-2023-Q20` source-sensitive bridge |
| log variable / sqrt-log variable | `NMTC-BH-P-2024-Q12`, `NMTC-BH-P-2025-Q12` | — |
| exact log/exponent structure | `NMTC-BH-P-2024-Q28` | — |
| log system -> algebra | `NMTC-BH-P-2025-Q27` | — |

`BONUS_EVIDENCE: none identified in the current topic source map.`

---

# 9. Recognition-only drill — DO NOT SOLVE

For each prompt, write only the best first-step code from:

`CB HS PR EM EN EV ER RQ ZR RI LD LV LS LA LI DR QC`

1. `(√50+√8)/√2`.
2. `√(19-6√10)`.
3. `√((2x-7)^2)`.
4. `27^x=9^(x+2)`.
5. `4^x-9·2^x+8=0`.
6. `25^x-6·10^x+4·4^x=0`.
7. `√(x+7)=x-1`.
8. `(x-3)(x+5)=0`, and someone proposes dividing by `x-3`.
9. `t+1/t=5`; target `t^6+t^-6`.
10. `log_3 81=4` is to be interpreted, not calculated.
11. `(log_2 x)^2-6log_2 x+5=0`.
12. `log_2 x-5√(log_2 x)+4=0`.
13. positive `x,y`: `log_4 x=log_2 y`.
14. `25^(log_5 3)`.
15. squaring produced roots 2 and 9; original radical equation has not been rechecked.
16. a solution uses `log_2(x+1)=log_2 x` at `x=-2`.
17. `√20+√45-√5`.
18. `(11+6√2)^(3/2)`.
19. `16^x=8^(x+1)` and a solver reaches for logarithms first.
20. a printed key accepts a root that makes the original logarithm undefined.
21. `x+1/x` is known but the target is `x^3-1/x^3`.
22. `a^-3` is being interpreted as `-a^3`.
23. a derivation uses `log(M+N)=log M+log N`.
24. `u=√(log_3 x)` has been introduced with no range written.

## Recognition key

1 `CB`  
2 `HS`  
3 `PR`  
4 `EN`  
5 `EV`  
6 `ER`  
7 `RQ`  
8 `ZR`  
9 `RI`  
10 `LD`  
11 `LV`  
12 `LS`  
13 `LA`  
14 `LI`  
15 `DR`  
16 `DR`  
17 `CB`  
18 `HS`  
19 `EN`  
20 `QC` + `DR`  
21 `RI` **recognition, then boundary check**: the target is asymmetric, so `x+1/x` alone may not determine its sign/value uniquely  
22 `EM`  
23 `LD`  
24 `LS` + `DR` (`u≥0`)

### Recognition standard

- `21–24`: first-step compression is stable;
- `17–20`: review only missed cards/boundaries;
- `<17`: return to the corresponding Wave-2 teaching section rather than memorizing this sheet harder.

These bands are internal study diagnostics, not psychometric or official NMTC thresholds.

---

# 10. One-line ADOPT rules

- **When radicals look different, first ask whether they share a basis.**
- **When a surd looks engineered, run an identity backwards before expanding.**
- **When a square root contains a square, principal-root sign comes first.**
- **When a negative/fractional exponent is unstable, rewrite its reciprocal/root meaning first.**
- **When exponential bases are related, normalize before taking logs.**
- **When one exponential object repeats, name it and keep its positivity.**
- **When reciprocal powers are symmetric, compute the invariant before solving the hidden variable.**
- **When a transformation may lose sign or a zero case, mark it as conditional/candidate-generating.**
- **When logarithms appear, remember they are exponent statements with domain restrictions.**
- **When a compound log object repeats, substitute the whole repeated object and carry its range.**
- **When logs disappear into algebra, their original domain does not disappear.**
- **When exponent and log are inverse structures, simplify exactly before approximating.**
- **When source/key disagrees with valid mathematics, preserve the conflict; do not repair history silently.**

---

# 11. Five-second final check

Before boxing an answer:

```text
REPRESENTATION chosen deliberately?      yes / no
DOMAIN / SIGN / ZERO condition carried?  yes / no
TRANSFORMATION reversible?               <=> / =>
SUBSTITUTION range respected?            yes / no
ORIGINAL problem checked if required?    yes / no
SOURCE disposition preserved?            yes / no
```

`WAVE3_FIRST_STEP_REFERENCE_COMPLETE`

`NEXT_ALLOWED_STATE: WAVE4_MIXED_MASTERY_AND_TRANSFER`
