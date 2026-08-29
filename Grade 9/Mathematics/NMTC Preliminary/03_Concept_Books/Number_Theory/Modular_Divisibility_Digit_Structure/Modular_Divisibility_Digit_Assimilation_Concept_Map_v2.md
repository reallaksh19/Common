# Modular, Divisibility & Digit Structures — Assimilation Concept Map v2

`ISSUE_AUTHORITY: #47`

`WAVE: 0 — CONCEPT_MAP_FIRST`

`STATUS: DRAFT_CONCEPT_MAP`

Target learner: Grade IX/X student with partial prior knowledge. The learner can usually perform routine division, recall some divisibility rules, use HCF/LCM in familiar word problems, and find simple remainders. The unstable part is **representation and method choice**: turning words into congruences, knowing which information a remainder preserves, detecting cycles, distinguishing two different “same remainder” structures, encoding digits algebraically, and carrying admissibility conditions through divisor/state arguments.

The map is the pre-prose authority for Issue #47. It is not a student chapter and must exist before Wave-2 teaching prose.

---

# 1. Governing belief

> **A large integer problem often becomes small when we keep only the remainder, factor, digit-position, or state information that the target can actually see.**

The unit is therefore not a bag of divisibility tricks. It is a network of **integer compression representations**.

```text
VISIBLE INTEGER / WORD STATEMENT
        |
        v
WHAT INFORMATION MATTERS?
        |
        +--> remainder under one modulus
        +--> divisibility of a difference
        +--> residue cycle of a power
        +--> common multiple after subtracting a remainder
        +--> common divisor of pairwise differences
        +--> place-value expression in powers of 10
        +--> factor/divisor condition
        +--> prefix/state remainder
        |
        v
CHOOSE A COMPRESSION
        |
        +--> N = mq+r
        +--> N ≡ r (mod m)
        +--> residue table / cycle
        +--> N-r is a common multiple
        +--> d | (A-B)
        +--> 10a+b / 100a+10b+c / block factorization
        +--> integer part + constant/divisor
        +--> prefix residues S_i mod m
        |
        v
CHECK WHETHER THE OPERATION IS LEGAL
        |
        +--> addition/subtraction/multiplication: safe
        +--> cancellation/division: condition required
        +--> digit/state domain: preserve leading-zero/order restrictions
        +--> simultaneous congruences: verify compatibility
        |
        v
SOLVE / COUNT / RECONSTRUCT
        |
        v
CHECK ORIGINAL CONDITIONS
```

Cognitive contract:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Operational contract:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Performance contract:

`RECOGNIZE -> COMPRESS -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER`

---

# 2. Learner-state map

## 2.1 PRIOR_KNOWLEDGE — likely already owned

`PK-01` Division algorithm in concrete arithmetic: quotient and remainder.

`PK-02` HCF/GCD and LCM of small integers.

`PK-03` Familiar divisibility rules for 2, 3, 5, 9 and possibly 11.

`PK-04` Prime factorization and parity.

`PK-05` Basic place value: a two-digit number can be written from its digits.

`PK-06` Difference of squares and elementary factorization.

`PK-07` Simple power patterns/last digits by listing a few cases.

`PK-08` Solving linear equations after the representation has already been supplied.

These should be used as reconnect material, not retaught as a blank-slate chapter.

## 2.2 LIKELY_HALF_KNOWLEDGE — remembered but unstable

`HK-01` Can find a remainder but treats congruence notation as a new equality symbol rather than compressed divisibility information.

`HK-02` Knows that residues can be added/multiplied but may cancel a common factor without checking whether cancellation is valid modulo the stated modulus.

`HK-03` Can spot a last-digit cycle after prompting but makes off-by-one errors when the exponent is a multiple of the cycle length.

`HK-04` Sees the phrase “same remainder” and reaches for LCM automatically.

`HK-05` Can list simultaneous-congruence candidates by trial but does not see the intersection of arithmetic progressions or compatibility condition.

`HK-06` Uses divisibility-by-9/11 as memorized rules but cannot derive them from powers of 10.

`HK-07` Guesses digits verbally instead of writing place-value algebra.

`HK-08` Counts digit choices without separating ordered from unordered choices or without enforcing a nonzero leading digit.

`HK-09` Tests many integer values in an integrality problem instead of converting the condition into a finite divisor list.

`HK-10` Factors a difference of squares but forgets that `(u-v)` and `(u+v)` must have the same parity when recovering integers.

`HK-11` Knows `gcd(a,b)=1` as vocabulary but does not use prime-exponent separation in perfect-power products.

`HK-12` Has never connected consecutive-block sums with differences of prefix sums/remainder states.

`HK-13` May know the phrase “multiplicative order” from Olympiad material but uses it before ordinary residue cycles are secure.

`HK-14` Trusts a printed/source key even when the searchable statement is damaged.

## 2.3 MISSING_BRIDGES — the real repair targets

`B-01 DIVISION_TO_CONGRUENCE`  
Connect `N=mq+r` to `N≡r (mod m)` and then to `m | (N-r)`.

`B-02 CONGRUENCE_TO_DIFFERENCE_DIVISIBILITY`  
Understand `a≡b (mod m)` as exactly `m|(a-b)`. This bridge explains equal remainders, modular operations, and source of many GCD arguments.

`B-03 SAFE_OPERATION_VS_CANCELLATION`  
Addition/subtraction/multiplication preserve congruence directly. Division/cancellation is not automatic. If `ca≡cb (mod m)`, cancelling `c` modulo the same `m` requires an invertibility condition such as `gcd(c,m)=1`; otherwise the modulus/solution class may change.

`B-04 CYCLE_AS_FINITE_STATE`  
A power modulo `m` is not “huge arithmetic”; it moves through finitely many residue states. The cycle index, not the exponent magnitude, controls the answer.

`B-05 TWO_SAME_REMAINDER_GRAMMARS`  
One number leaving remainder `r` under several divisors means `N-r` is a common multiple. One divisor producing the same remainder on several numbers means that divisor divides their differences.

`B-06 SIMULTANEOUS_CONGRUENCE_AS_PROGRESSIONS`  
Each congruence is an arithmetic progression. A common solution is an intersection. For non-coprime moduli, compatibility must be checked rather than assuming a solution exists.

`B-07 PLACE_VALUE_AS_ALGEBRA`  
Digit language becomes `10a+b`, `100a+10b+c`, repeated blocks, or powers-of-10 expressions before guessing/counting.

`B-08 DIVISIBILITY_RULE_FROM_POWERS_OF_10`  
Digit-sum and alternating-sum rules are consequences of `10≡1 (mod 9)` and `10≡-1 (mod 11)`, not magic tests.

`B-09 DIGIT_DOMAIN_AND_ORDER`  
Digit variables have finite domains; leading digits cannot be zero; ordered numbers are different objects even when they use the same digits; different digits can share the same residue class.

`B-10 INTEGRALITY_TO_DIVISOR_CONDITION`  
Rewrite a rational expression as an integer part plus `C/g(n)` or substitute so the denominator must divide a fixed constant. Infinite search becomes finite factor structure.

`B-11 FACTOR_PAIR_FILTERS`  
After factorization, parity, sign, order, bounds, coprimality and perfect-power conditions decide which factor pairs are actually admissible.

`B-12 PREFIX_REMAINDER_STATE`  
A consecutive block sum is `S_j-S_i`; it is divisible by `m` exactly when two prefix sums have the same residue modulo `m`.

`B-13 CYCLE_TO_MULTIPLICATIVE_ORDER`  
Only after ordinary cycles are secure: the least exponent returning to residue 1 can constrain possible prime divisors. This is a ceiling bridge, not entry-level notation.

`B-14 SOURCE_CUSTODY`  
A recovered solution can support a mechanism without authorizing reconstruction of a corrupted exact question.

---

# 3. Core invariants / structures

`I-01 DIVISION_ALGORITHM`  
For positive `m`, every integer has a unique representation `N=mq+r`, `0≤r<m`.

`I-02 CONGRUENCE_DIFFERENCE`  
`a≡b (mod m) <=> m|(a-b)`.

`I-03 RESIDUE_OPERATION`  
Replacing an integer by an equivalent residue preserves sums, differences, products and integer powers modulo the same modulus.

`I-04 CANCELLATION_CONDITION`  
A common factor is cancellable modulo `m` without loss only when its residue is invertible modulo `m` (e.g. coprime to `m`). Otherwise the correct conclusion may use a smaller modulus or require case analysis.

`I-05 FINITE_RESIDUE_STATE`  
Repeated powers modulo `m` eventually repeat; once a state repeats, subsequent residues are periodic.

`I-06 SAME_REMAINDER_LCM`  
If the same `N` leaves remainder `r` under divisors `d_1,d_2,...`, then `N-r` is a common multiple.

`I-07 SAME_REMAINDER_GCD`  
If divisor `d` leaves the same remainder on `A,B,C,...`, then `d` divides all pairwise differences.

`I-08 SIMULTANEOUS_SOLUTION_PERIOD`  
When compatible, common solutions repeat modulo `lcm(m,n,...)`; coprimality is a special case, not a permission to ignore compatibility generally.

`I-09 PLACE_VALUE`  
A base-10 numeral is a polynomial in 10 with digit coefficients.

`I-10 MOD_9_AND_MOD_11_PLACE_VALUE`  
`10^k≡1 (mod9)`; `10^k≡(-1)^k (mod11)`.

`I-11 DIVISOR_REDUCTION`  
If an integer expression is `A(n)+C/g(n)`, integrality forces `g(n)|C`, subject to domain restrictions.

`I-12 FACTOR_PAIR_PARITY`  
For integers `u,v`, the factors `u-v` and `u+v` have the same parity.

`I-13 COPRIME_PERFECT_POWER`  
If positive coprime integers multiply to a perfect `k`th power, prime exponents cannot be shared across the factors; each factor must itself carry exponents divisible by `k`.

`I-14 PREFIX_DIFFERENCE`  
`a_{i+1}+...+a_j=S_j-S_i`; divisibility by `m` is equality of prefix residues.

`I-15 SOURCE_DISPOSITION`  
Source status does not improve merely because a plausible solution exists: clean stays clean; a transcription-suspect item stays blocked until independently resolved.

---

# 4. Representation network

```text
WORD: “remainder r on division by m”
        |
        +--> N = mq+r
        |
        +--> N ≡ r (mod m)
        |
        +--> m | (N-r)
```

```text
HUGE POWER a^N mod m
        |
        v
reduce a mod m
        |
        v
residue table / cycle
        |
        v
N mod cycle length
        |
        v
correct cycle position
```

```text
“SAME REMAINDER”
      |
      +--> same N, many divisors
      |       N-r = common multiple -> LCM
      |
      +--> same divisor, many numbers
              divisor | pairwise differences -> GCD
```

```text
DIGIT WORDING
      |
      v
PLACE VALUE
10a+b / 100a+10b+c / repeated blocks
      |
      +--> ordinary algebra
      +--> modulo 9/11/other justified modulus
      +--> ordered digit-domain counting
```

```text
RATIONAL INTEGRALITY
      |
      v
algebraic division / substitution
      |
      v
integer part + C / divisor-expression
      |
      v
finite divisor list
      |
      v
sign/domain/bound filter
```

```text
CONSECUTIVE BLOCKS
      |
      v
prefix sums S0,S1,...
      |
      v
prefix residues modulo m
      |
      v
same residue <=> divisible block
```

---

# 5. Seven Issue-47 stream paths

| Stream | PRIOR -> BRIDGE | Invariant / representation | First move that should become automatic | Transfer endpoint |
|---|---|---|---|---|
| W1-A Congruence meaning/operations | ordinary remainder -> divisibility of difference -> congruence | `a≡b (modm) <=> m|(a-b)`; invertibility for cancellation | translate words to `N=mq+r` or congruence; ask whether any proposed division is legal | diagnose/correct an illegal modular cancellation |
| W1-B Power cycles/order | last-digit patterns -> finite residue state -> period/order | residue table; cycle length; later multiplicative order | reduce base and list residues before touching the large exponent | a disguised last-two-digit or prime-divisor problem |
| W1-C Same remainder | HCF/LCM routine -> identify which quantity is common | common multiple vs common divisor of differences | ask “same number under many divisors, or same divisor on many numbers?” | a near-identical pair where only one word changes the method |
| W1-D Simultaneous congruences | trial lists -> arithmetic-progression intersection | `N=r+mk`; compatibility; period `lcm` | parameterize one congruence and impose the next | compatible vs incompatible non-coprime moduli |
| W1-E Place value/digits | known digit rules -> powers-of-10 algebra | `10a+b`; `10≡1 mod9`; `10≡-1 mod11` | encode the numeral before guessing digits | ordered/reversal/count problem with leading-zero and residue-class traps |
| W1-F Factor/divisor | factorization + divisibility -> finite divisor/filter structure | `g(n)|C`; parity; coprimality; perfect-power exponents | divide/factor until only finitely many divisors/factor pairs remain | integrality or difference-square problem requiring sign/parity filtering |
| W1-G Prefix/state | cumulative sums -> difference of states | `S_j-S_i`; equal prefix residues | include `S0`; record prefix residues instead of enumerating all blocks | existence/count of divisible blocks; representation/state ceiling bridge |

---

# 6. Decision boundaries / close contrast pairs

## DB-01 Congruence versus equality

- `17≡2 (mod5)` is true.
- `17=2` is false.

**Boundary:** congruence preserves one remainder class, not the integer itself.

## DB-02 Safe reduction versus unsafe cancellation

- Reducing `14·19` to `2·1 (mod6)` is safe.
- From `2x≡2 (mod6)`, concluding `x≡1 (mod6)` is false; the valid reduction is `x≡1 (mod3)`.

**Boundary:** multiplication respects congruence automatically; division requires invertibility/coprimality or a modified modulus.

## DB-03 Base reduction versus exponent reduction

- Reduce the **base** modulo `m` directly.
- Reduce the **exponent** only through a proved residue cycle/order, not by taking the exponent modulo `m` by reflex.

## DB-04 Cycle remainder zero

If a cycle has length 4 and `N≡0 (mod4)`, use the fourth cycle position, not the zeroth/first entry.

## DB-05 Same remainder: LCM versus GCD

- one `N`, several divisors -> subtract remainder -> LCM;
- one divisor, several numbers -> differences -> GCD.

This is the mandatory flagship contrast.

## DB-06 Compatible versus incompatible simultaneous congruences

`N≡1 (mod4)` and `N≡3 (mod6)` are compatible because the residues agree modulo `gcd(4,6)=2`.

`N≡1 (mod4)` and `N≡2 (mod6)` are incompatible because they disagree modulo 2.

**Boundary:** constructive CRT-style work begins after compatibility is respected.

## DB-07 Place-value algebra versus digit guessing

“two-digit number with digits `a,b`” -> `10a+b` first. Guessing candidate numbers is a fallback, not the representation.

## DB-08 Ordered versus unordered digit choices

Digits `{2,5}` produce different two-digit numbers `25` and `52`. A digit pair used in a numeral is usually ordered unless the problem explicitly asks for an unordered set.

## DB-09 Residue class versus actual digit

Modulo 9, decimal digits 0 and 9 have the same residue but remain different digit choices.

## DB-10 Divisibility rule versus proof from place value

Using digit sum is efficient after understanding; if the rule is forgotten or the base/modulus changes, reconstruct from powers of 10.

## DB-11 Brute-force integrality versus divisor reduction

Testing many `n` values is inferior when algebra can force a denominator to divide a fixed constant.

## DB-12 Factor pair versus admissible factor pair

`(u-v)(u+v)=K` does not authorize every factor pair of `K`; same parity, sign, order and bounds must be checked.

## DB-13 Prefix states versus block enumeration

Many consecutive-block sums -> compare prefix residues. Directly adding every possible block is usually quadratic work and hides the invariant.

## DB-14 Ordinary cycle versus multiplicative-order ceiling

Cycle listing is core. Multiplicative order is used only after the base is nonzero/invertible modulo the candidate prime and ordinary cycle meaning is secure.

## DB-15 Source mechanism versus canonical PYQ

A corrupted stem with a recoverable modulo-4 solution can support a **mechanism note** but cannot be printed as a clean historical question.

---

# 7. Misconception nodes and repair statements

`M-01 “≡ means =.”`  
Repair: congruence means equal remainder / divisible difference.

`M-02 “Cancel anything appearing on both sides.”`  
Repair: modular cancellation needs an invertible factor or a carefully changed modulus.

`M-03 “Reduce the exponent modulo the modulus.”`  
Repair: exponent reduction comes from a cycle/order, not from the modulus number itself.

`M-04 “Same remainder means LCM.”`  
Repair: identify whether the repeated object is the number or the divisor.

`M-05 “CRT always gives a solution.”`  
Repair: with non-coprime moduli, first check residue compatibility modulo their GCD.

`M-06 “Divisibility by 9/11 is a magic digit trick.”`  
Repair: derive the rule from powers of 10.

`M-07 “Digits are just labels; order does not matter.”`  
Repair: place value makes positions part of the number.

`M-08 “Residue 0 mod9 means the digit is 0.”`  
Repair: residue class and digit identity are different; 9 is also 0 mod9.

`M-09 “Try integers until the fraction becomes integral.”`  
Repair: transform to a divisor of a fixed constant.

`M-10 “Every factor pair of K gives integer u,v.”`  
Repair: enforce same parity when recovering sum/difference variables.

`M-11 “Coprime is only a GCD calculation.”`  
Repair: coprimality separates prime-exponent ownership across factors.

`M-12 “Prefix sums start at S1.”`  
Repair: include `S0=0`; blocks starting at the first term depend on it.

`M-13 “A solution/key repairs a damaged source.”`  
Repair: mechanism evidence and exact-source custody are separate facts.

---

# 8. First-move atlas

| Visible clue | First move to test |
|---|---|
| remainder `r` on division by `m` | write `N=mq+r` or `N≡r (modm)` |
| two numbers claimed congruent | inspect/divide their difference by the modulus |
| proposed cancellation/division modulo `m` | check `gcd(factor,m)` / invertibility before cancelling |
| huge power or last digit | reduce base; build the residue cycle |
| same `N` leaves `r` under several divisors | `N-r` is a common multiple -> LCM structure |
| greatest divisor leaves same remainder on several numbers | take pairwise differences -> GCD structure |
| several remainder equations | parameterize one progression and impose the next; check compatibility |
| two-/three-digit or reversal wording | write place-value algebra immediately |
| divisibility by 9 or 11 | reduce powers of 10 modulo 9/11 |
| rational expression required to be integer | algebraically divide/substitute until denominator must divide a constant |
| `u²-v²`, product with parity/bounds | factor first, then filter factor pairs |
| coprime factors multiply to a perfect power | distribute prime exponents factor-by-factor |
| many consecutive block sums | write prefix sums including `S0`, then residues |
| prime divides `a^k±1` | only after core cycle check: consider order and candidate-prime restrictions |
| source notation damaged | preserve mechanism evidence; block exact canonical anchor |

---

# 9. Transfer endpoints — ownership under disguise

`T-01` A congruence equation where naive cancellation loses valid residue classes.

`T-02` A last-two-digit or non-decimal remainder problem whose cycle is not supplied.

`T-03` Two “same remainder” prompts differing only in whether the repeated object is the number or divisor.

`T-04` A pair of non-coprime simultaneous congruences: one compatible, one impossible.

`T-05` A reversed-digit problem combining place value, divisibility and digit-domain constraints.

`T-06` A digit-count problem where 0 and 9 share a residue but are different choices, with an ordered/unordered contrast.

`T-07` A rational integrality expression requiring negative-divisor or denominator-zero filtering.

`T-08` A difference-of-squares factorization where half the factor pairs fail the parity condition.

`T-09` A coprime perfect-cube/square product in a surface form different from the historical consecutive-integer anchor.

`T-10` A consecutive-block existence/count problem solved by prefix states rather than direct sums.

`T-11` A score/attainability problem where a residue obstruction eliminates a target before enumeration.

`T-12` A prime-divisor power problem requiring multiplicative-order reasoning after checking the base is nonzero modulo the prime.

`T-13` A corrupted-source case where the mathematically plausible mechanism is retained but exact wording remains blocked.

---

# 10. Source custody frozen for Wave 0

## CLEAN_SCORED_ANCHOR — core/ordinary

- `NMTC-BH-P-2018-Q10`
- `NMTC-BH-P-2018-Q18`
- `NMTC-BH-P-2018-Q19`
- `NMTC-BH-P-2018-Q28`
- `NMTC-BH-P-2018-Q29`
- `NMTC-BH-P-2019-Q01`
- `NMTC-BH-P-2019-Q16`
- `NMTC-BH-P-2019-Q17`
- `NMTC-BH-P-2019-Q27`
- `NMTC-BH-P-2023-Q18`
- `NMTC-BH-P-2024-Q20`
- `NMTC-BH-P-2024-Q21`
- `NMTC-BH-P-2025-Q01`
- `NMTC-BH-P-2025-Q13`
- `NMTC-BH-P-2025-Q14`
- `NMTC-BH-P-2025-Q21`
- `NMTC-BH-P-2025-Q26`

## CLEAN_SCORED_ANCHOR — ceiling / bridge role

These are real scored Preliminary evidence, but pedagogy must not make them entry prerequisites:

- `NMTC-BH-P-2019-Q06` — prefix residues;
- `NMTC-BH-P-2019-Q14` — attainability/congruence restrictions;
- `NMTC-BH-P-2019-Q26` — multiplicative-order prime filtering;
- `NMTC-BH-P-2019-Q28` — balanced ternary / canonical representation bridge.

They remain clean scored evidence; “ceiling” is a teaching-role label, not a scoring demotion.

## SOURCE_SENSITIVE_EVIDENCE — blocked exact anchor

- `NMTC-BH-P-2023-Q12` — searchable statement is corrupted; recovered solution indicates modulo-4 parity/residue reasoning. Retain as research/mechanism evidence only until original wording is recovered.

## BONUS_EVIDENCE

No topic-specific bonus item is currently needed to ground this package. Do not infer bonus recurrence.

## AUTHOR_CREATED_FOUNDATION required because historical evidence does not directly teach the bridge

- legal vs illegal modular cancellation;
- compatible vs incompatible simultaneous congruences with non-coprime moduli;
- cycle-index zero-position diagnosis;
- derivation of mod-9/mod-11 rules before compression;
- ordered vs unordered digit choices / leading-zero restrictions;
- denominator-zero and negative-divisor filtering;
- core-cycle versus multiplicative-order decision boundary.

## Source-map correction made in Wave 0

The previous topic coverage map omitted `NMTC-BH-P-2018-Q18` from the factor/divisor section even though the qualified 2018 ledger explicitly identifies Q18 as a scored difference-of-squares/same-parity factor-pair problem. Wave 0 restores that anchor. Q19 remains a separate integrality/perfect-square anchor.

---

# 11. Benchmark requirements carried forward

The Quadratics benchmark is a minimum-quality comparator, not a layout template. Issue #47 must therefore ensure that later waves:

1. teach missing links rather than merely repeat divisibility rules;
2. put the student attempt before any H1/H2/H3 scaffold;
3. physically separate hints/keys from attempt surfaces;
4. use genuine H3 -> H2 -> H1 -> H0 fading across fresh problems;
5. make every major method compete with a close near-miss;
6. require an unlabelled first move;
7. use non-identical transfer, not number swaps;
8. preserve ceiling and source-sensitive dispositions;
9. independently recompute every residue, cycle, divisor count and digit admissibility claim before promotion;
10. treat classroom timing/readability as `NOT_RUN` until observed.

---

# 12. End-state learner belief

> **Congruence, divisibility, HCF/LCM, digit rules and residue cycles are not separate tricks. They are different ways of compressing integer information. I first ask what information the target can see, choose the matching representation, check that every modular operation is legal, and only then calculate.**

`NEXT_ALLOWED_STATE: WAVE1_SEVEN_STREAM_INTERFACES`