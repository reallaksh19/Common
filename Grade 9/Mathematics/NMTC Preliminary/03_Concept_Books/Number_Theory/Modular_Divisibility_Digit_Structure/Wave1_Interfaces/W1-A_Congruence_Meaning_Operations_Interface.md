# W1-A — Congruence Meaning & Operations Interface

`ISSUE_AUTHORITY: #47`

`WAVE: 1A`

`STATUS: INTERFACE_COMPLETE`

## 1. CONCEPTS

- division algorithm as the concrete source of remainder language;
- `a ≡ b (mod m)` as `m | (a-b)`;
- canonical residue reduction;
- addition, subtraction, multiplication and integer-power preservation;
- equality versus congruence;
- modular cancellation/division only under valid invertibility conditions;
- solution-set change when a non-invertible factor is cancelled.

## 2. PREREQUISITES

- quotient/remainder arithmetic;
- divisibility notation;
- gcd/coprimality;
- elementary algebraic rearrangement.

## 3. LIKELY_HALF_KNOWLEDGE

- can compute a remainder but treats congruence notation as a new equality symbol;
- reduces large numbers modulo `m` correctly but may divide/cancel residues as in ordinary equations;
- remembers a rule such as “same remainder means subtract” without knowing it comes from divisibility of a difference;
- expects a linear congruence to have one residue-class solution even when the coefficient is not invertible.

## 4. RECOGNITION_CUES

- “remainder when divided by …”;
- “same remainder”;
- “modulo / mod”;
- large numbers where only a remainder is requested;
- a proposed simplification that divides both sides of a congruence.

## 5. FIRST_MOVES

1. Translate `N leaves remainder r on division by m` to `N = mq+r`, hence `N ≡ r (mod m)`.
2. Translate `a ≡ b (mod m)` back to `m | (a-b)` whenever legality is unclear.
3. Reduce operands before adding/multiplying.
4. Before cancellation ask: `gcd(c,m)=1?` If not, do not cancel modulo the same modulus by reflex.

## 6. INVARIANTS

- integers in one congruence class differ by a multiple of the modulus;
- sums/differences/products of congruent representatives stay congruent;
- a factor has a multiplicative inverse modulo `m` iff it is coprime to `m`;
- non-invertible cancellation can enlarge or otherwise change the residue-class description.

## 7. REPRESENTATION_SWITCHES

- words ↔ `N=mq+r` ↔ `N≡r (modm)` ↔ `m|(N-r)`;
- `a≡b (modm)` ↔ `a-b=km`;
- modular equation ↔ ordinary divisibility equation when cancellation is questionable.

## 8. LEGALITY / ADMISSIBILITY CONDITIONS

Safe without extra conditions:
- add/subtract congruences with the same modulus;
- multiply congruences;
- raise both sides to a positive integer power.

Condition-sensitive:
- cancelling `c` from `ca≡cb (modm)` modulo the same `m` requires `gcd(c,m)=1`;
- if `d=gcd(c,m)>1`, one may often reduce to `a≡b (mod m/d)` after dividing the divisibility relation by `d`, not retain modulus `m`.

## 9. DECISION_BOUNDARIES

**DB-A1 congruence vs equality**  
`17≡2 (mod5)` is true; `17=2` is false.

**DB-A2 reduction vs cancellation**  
`14·19≡2·1 (mod6)` is safe.  
From `2x≡2 (mod6)`, `x≡1 (mod6)` is false; correct reduction is `x≡1 (mod3)`.

**DB-A3 divide by a unit vs non-unit**  
`5x≡10 (mod12)` -> multiply by inverse of 5, valid.  
`4x≡8 (mod12)` -> 4 is not invertible modulo 12; solutions must be handled through divisibility/reduced modulus.

## 10. MISCONCEPTION_TRAPS

- treating `≡` as weak equality rather than an equivalence relation on residue classes;
- reducing the exponent modulo the modulus because the base was reduced modulo the modulus;
- cancelling any visible common factor;
- forgetting that moduli should be positive in the standard school convention;
- assuming a modular equation has one residue-class solution when a non-unit coefficient can create several.

## 11. CONTRAST_PAIRS

1. `23≡3 (mod5)` vs `23=3`.
2. `7x≡7 (mod10)` permits cancellation by 7; `2x≡2 (mod6)` does not permit cancellation modulo 6.
3. `x≡2 (mod5)` and `x≡7 (mod5)` are the same class; `x=2` and `x=7` are different integers.

## 12. TRANSFER_MECHANISMS

- diagnose a worked solution whose only error is illegal cancellation;
- solve a congruence with non-coprime coefficient by reverting to divisibility;
- translate a verbal remainder condition into an algebraic family and back;
- compare two different congruence descriptions and determine whether they define the same class.

## 13. SOURCE_IDS_AND_DISPOSITIONS

Clean scored mechanism anchor:
- `NMTC-BH-P-2025-Q13` — direct residue squaring modulo 11.

Nearby clean anchors from other streams use congruence meaning, especially `NMTC-BH-P-2024-Q21` and `NMTC-BH-P-2025-Q01`, but their primary mechanisms remain same-remainder structure.

Author-created foundation is mandatory for:
- explicit congruence meaning;
- illegal cancellation;
- modular inverse/coprimality boundary;
- multiple-solution behavior of non-unit coefficients.

`NMTC-BH-P-2024-Q20` is **not** promoted here; Issue #47 now classifies it as source-conflict/QC evidence.

## 14. CANDIDATE_MASTERY_ITEMS

`A-M1` Translate: “N leaves remainder 7 when divided by 12.” Write three equivalent forms.

`A-M2` Decide whether `38≡8 (mod10)` is true and justify from divisibility of a difference.

`A-M3` Reduce `47·58+19 (mod9)` without multiplying large numbers.

`A-M4` Solve `2x≡2 (mod6)` as residue classes modulo 6; explain why cancelling 2 modulo 6 loses information.

`A-M5` Solve `5x≡10 (mod12)` and explain why cancellation/inversion is legal.

Independent check:
- A-M1: `N=12q+7`, `N≡7 (mod12)`, `12|(N-7)`;
- A-M2 true since 30 is divisible by 10;
- A-M3 `2·4+1=9≡0`;
- A-M4 `x≡1,4 (mod6)`; equivalently `x≡1 (mod3)`;
- A-M5 `x≡2 (mod12)`.

## 15. DIAGNOSTIC_TAGS

- `CONGRUENCE_AS_EQUALITY`
- `DIVISION_ALGORITHM_BRIDGE_MISSING`
- `ILLEGAL_MODULAR_CANCELLATION`
- `NONUNIT_COEFFICIENT_UNSEEN`
- `REPRESENTATIVE_CLASS_CONFUSION`

## 16. H3_TO_H0_FADE_PLAN

- `A-F1 H3`: give `a≡b (modm) <=> m|(a-b)` and ask learner to verify one congruence.
- `A-F2 H2`: state “return to divisibility before cancelling” for a non-unit coefficient equation.
- `A-F3 H1`: point only to `gcd(coefficient, modulus)`.
- `A-F4 H0`: mixed unlabelled congruence requiring the learner to decide independently whether reduction, cancellation, or divisibility is the correct first move.

`W1-A_GATE: PASS`