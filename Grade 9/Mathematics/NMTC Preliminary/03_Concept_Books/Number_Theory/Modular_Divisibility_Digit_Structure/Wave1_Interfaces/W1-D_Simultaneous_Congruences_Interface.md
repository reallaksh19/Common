# W1-D — Simultaneous Congruences Interface

`ISSUE_AUTHORITY: #47`

`WAVE: 1D`

`STATUS: INTERFACE_COMPLETE`

## 1. CONCEPTS

- each congruence as an arithmetic progression;
- intersection of residue progressions;
- parameterize one condition and impose the next;
- compatible versus incompatible non-coprime moduli;
- smallest positive solution;
- full solution family repeating modulo an LCM;
- CRT-style constructive reasoning without requiring theorem-first formalism;
- distinguish true simultaneous remainder conditions from successive quotient/remainder division.

## 2. PREREQUISITES

- W1-A congruence meaning and legal operations;
- linear congruence solving at a basic level;
- gcd/lcm;
- arithmetic progressions.

## 3. LIKELY_HALF_KNOWLEDGE

- can list numbers in one residue class but does not see each congruence as an arithmetic progression;
- assumes any two remainder conditions have a common solution;
- thinks non-coprime moduli automatically make a system unsolvable, or alternatively ignores compatibility entirely;
- finds one candidate and forgets the full repeating solution class;
- flattens remainders of successive quotients into congruences for the original number.

## 4. RECOGNITION_CUES

- one fixed unknown number with two or more remainder conditions applied directly to that same number;
- “smallest positive integer satisfying …”;
- several congruences displayed simultaneously;
- non-coprime moduli such as 4 and 6;
- wording involving a quotient being divided again, which signals a different representation.

## 5. FIRST_MOVES

1. Confirm that every remainder condition applies to the **same original unknown**, not to successive quotients.
2. Before constructing, check compatibility when moduli share a gcd.
3. Parameterize one condition: `N=a+mk`.
4. Substitute into the next congruence and solve for `k`.
5. Continue progressively.
6. Verify the final candidate in every original condition.

## 6. INVARIANTS

- `N≡a (modm)` is the progression `a+mk`;
- two congruences `N≡a (modm)`, `N≡b (modn)` are compatible iff `a≡b (mod gcd(m,n))`;
- when compatible, all common solutions repeat modulo `lcm(m,n)`;
- pairwise-coprime moduli are a convenient special case, not the only solvable case.

## 7. REPRESENTATION_SWITCHES

- congruence -> arithmetic progression;
- progression intersection -> congruence in parameter `k`;
- compatibility -> difference `a-b` divisible by `gcd(m,n)`;
- one found solution `N0` -> full family `N≡N0 (mod lcm(...))`;
- successive quotient/remainder chain -> nested division algorithm, not a simultaneous congruence system.

## 8. LEGALITY / ADMISSIBILITY CONDITIONS

- do not assume every set of remainder conditions is compatible;
- if residues are not written canonically, reduce them before compatibility checks;
- after solving a coefficient congruence for `k`, apply W1-A cancellation rules;
- “least positive solution” means choose the positive representative after the full class is established;
- do not flatten a remainder of a quotient into a congruence for the original number.

## 9. DECISION_BOUNDARIES

**DB-D1 coprime vs non-coprime compatible**  
`N≡2 (mod5)`, `N≡1 (mod3)` is automatically compatible.  
`N≡1 (mod4)`, `N≡3 (mod6)` is compatible because both residues agree modulo `gcd=2`.

**DB-D2 compatible vs impossible**  
`N≡1 (mod4)`, `N≡2 (mod6)` is impossible because the residues disagree modulo 2.

**DB-D3 one solution vs solution class**  
Finding 7 for `N≡2 (mod5)`, `N≡1 (mod3)` is not the full statement: `N≡7 (mod15)`.

**DB-D4 simultaneous vs successive division**  
Direct remainder conditions on the same `N` form a simultaneous-congruence system. A remainder condition on a quotient after a prior division belongs to a nested division-algorithm chain.

## 10. MISCONCEPTION_TRAPS

- brute-force listing without seeing progression intersection;
- assuming “CRT” means moduli must always be coprime;
- skipping compatibility for shared factors;
- stopping after one solution when a family is requested;
- failing to check all original congruences after progressive substitution;
- reading quotient remainders as if all remainders belonged to the original number.

## 11. CONTRAST_PAIRS

1. `x≡1 (mod4), x≡3 (mod6)` -> compatible.
2. `x≡1 (mod4), x≡2 (mod6)` -> incompatible.
3. `x=7` as least positive solution vs `x≡7 (mod15)` as complete class.
4. Direct remainders on one number vs remainders of successive quotients.

## 12. TRANSFER_MECHANISMS

- three congruences where the easiest starting modulus is not the first listed;
- non-coprime compatible system;
- deliberately inconsistent system requiring rejection before search;
- word problem that hides simultaneous congruences;
- near-miss wording where quotient remainders require nested reconstruction instead.

## 13. SOURCE_IDS_AND_DISPOSITIONS

There is currently **no exact clean historical anchor frozen for generic simultaneous-congruence/CRT reconstruction**.

`NMTC-BH-P-2024-Q20` is now classified for Issue #47 as:

`SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`.

Reason: the reproduced stem is ambiguous; the published solution interprets successive quotient division and then assumes an unstated range/top-quotient condition to obtain the keyed `43*`. The older repository summary that described Q20 as three simultaneous congruences is also mathematically incompatible with 43.

Therefore this stream uses:
- `AUTHOR_CREATED_FOUNDATION` for compatibility, constructive intersection and complete solution classes;
- `AUTHOR_CREATED_TRANSFER` for disguised CRT-style systems;
- Q20 only as a source-QC/representation-boundary case, never as a clean worked anchor.

## 14. CANDIDATE_MASTERY_ITEMS

`D-M1` Solve `N≡2 (mod5)`, `N≡1 (mod3)`; give least positive and complete class.

`D-M2` Decide without search whether `N≡1 (mod4)`, `N≡2 (mod6)` has a solution.

`D-M3` Solve `N≡1 (mod4)`, `N≡3 (mod6)`.

`D-M4` Find the least positive `N` satisfying `N≡2 (mod3)`, `N≡3 (mod5)`, `N≡2 (mod7)`.

`D-M5` In a clearly stated successive-division chain, `N=5q1+3`, `q1=6q2+2`, `q2=7t+2`. Express `N` in terms of `t` and decide whether these data alone determine a unique remainder modulo 120.

Independent check:
- D-M1: `N≡7 (mod15)`;
- D-M2: no solution; parity conflict;
- D-M3: `N≡9 (mod12)`;
- D-M4: least positive solution 23; complete class `N≡23 (mod105)`;
- D-M5: `N=210t+73`; modulo 120 this is `90t+73`, so the remainder depends on `t`; the data alone do **not** determine one remainder modulo 120.

## 15. DIAGNOSTIC_TAGS

- `CRT_AS_BRUTE_FORCE`
- `NONCOPRIME_COMPATIBILITY_MISSING`
- `INCOMPATIBLE_SYSTEM_NOT_REJECTED`
- `ONE_SOLUTION_NOT_CLASS`
- `FINAL_CONGRUENCE_NOT_RECHECKED`
- `SUCCESSIVE_QUOTIENT_FLATTENED_TO_CONGRUENCES`
- `SOURCE_PARAPHRASE_INCOMPLETE`

## 16. H3_TO_H0_FADE_PLAN

- `D-F1 H3`: supply `N=a+mk` and the next substitution line.
- `D-F2 H2`: cue “view each congruence as a progression; check shared gcd.”
- `D-F3 H1`: ask only “same original number, and compatible?” before arithmetic.
- `D-F4 H0`: mixed system requiring independent compatibility check, parameter choice, reconstruction and class statement, plus a near-miss successive-division prompt that must be rejected as a CRT item.

`W1-D_GATE: PASS_WITH_SOURCE_CUSTODY_CORRECTION`