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
- CRT-style constructive reasoning without requiring theorem-first formalism.

## 2. PREREQUISITES

- W1-A congruence meaning and legal operations;
- linear congruence solving at a basic level;
- gcd/lcm;
- arithmetic progressions.

## 3. RECOGNITION_CUES

- one unknown number with two or more remainder conditions;
- “smallest positive integer satisfying …”;
- several congruences displayed simultaneously;
- non-coprime moduli such as 4 and 6.

## 4. FIRST_MOVES

1. Before constructing, check obvious compatibility when moduli share a gcd.
2. Parameterize one condition: `N=a+mk`.
3. Substitute into the next congruence and solve for `k`.
4. Continue progressively.
5. Verify the final candidate in every original condition.

## 5. INVARIANTS

- `N≡a (modm)` is the progression `a+mk`;
- two congruences `N≡a (modm)`, `N≡b (modn)` are compatible iff `a≡b (mod gcd(m,n))`;
- when compatible, all common solutions repeat modulo `lcm(m,n)`;
- pairwise-coprime moduli are a convenient special case, not the only solvable case.

## 6. REPRESENTATION_SWITCHES

- congruence -> arithmetic progression;
- progression intersection -> congruence in parameter `k`;
- compatibility -> difference `a-b` divisible by `gcd(m,n)`;
- one found solution `N0` -> full family `N≡N0 (mod lcm(...))`.

## 7. LEGALITY / CONDITIONS

- do not assume every set of remainder conditions is compatible;
- if residues are not written canonically, reduce them before compatibility checks;
- after solving a coefficient congruence for `k`, apply W1-A cancellation rules;
- “least positive solution” means choose the positive representative after the full class is established.

## 8. DECISION_BOUNDARIES

**DB-D1 coprime vs non-coprime compatible**  
`N≡2 (mod5)`, `N≡1 (mod3)` is automatically compatible.  
`N≡1 (mod4)`, `N≡3 (mod6)` is compatible because both residues are odd modulo `gcd=2`.

**DB-D2 compatible vs impossible**  
`N≡1 (mod4)`, `N≡2 (mod6)` is impossible because residues disagree modulo 2.

**DB-D3 one solution vs solution class**  
Finding 7 for `N≡2 (mod5)`, `N≡1 (mod3)` is not the full statement: `N≡7 (mod15)`.

## 9. MISCONCEPTION_TRAPS

- brute-force listing without seeing progression intersection;
- assuming “CRT” means moduli must always be coprime;
- skipping compatibility for shared factors;
- stopping after one solution when a family is requested;
- failing to check all original congruences after progressive substitution.

## 10. CONTRAST_PAIRS

1. `x≡1 (mod4), x≡3 (mod6)` -> compatible.
2. `x≡1 (mod4), x≡2 (mod6)` -> incompatible.
3. `x=7` as least positive solution vs `x≡7 (mod15)` as complete class.

## 11. TRANSFER_MECHANISMS

- three congruences where the easiest starting modulus is not the first listed;
- non-coprime compatible system;
- deliberately inconsistent system requiring rejection before search;
- word problem that hides simultaneous congruences in repeated remainder language.

## 12. SOURCE_IDS_AND_DISPOSITIONS

Clean scored anchor:
- `NMTC-BH-P-2024-Q20` — constructive reconstruction from several congruences.

Author-created foundation required for:
- compatibility criterion with non-coprime moduli;
- incompatible contrast pair;
- full-solution-period interpretation.

## 13. CANDIDATE_MASTERY_ITEMS

`D-M1` Solve `N≡2 (mod5)`, `N≡1 (mod3)`; give least positive and complete class.

`D-M2` Decide without search whether `N≡1 (mod4)`, `N≡2 (mod6)` has a solution.

`D-M3` Solve `N≡1 (mod4)`, `N≡3 (mod6)`.

`D-M4` Find the least positive `N` satisfying `N≡3 (mod5)`, `N≡2 (mod6)`, `N≡2 (mod7)`.

`D-M5` Explain why common solutions to compatible conditions modulo 8 and 12 repeat modulo 24 rather than 96.

Independent check:
- D-M1: `N≡7 (mod15)`;
- D-M2: no solution; parity conflict;
- D-M3: `N≡9 (mod12)`;
- D-M4: 23? Check: 23 mod5=3, mod6=5 not 2, so not. Construct: numbers 2 mod6 and 2 mod7 are `2 mod42`; impose mod5: `2+42k≡3`, `2k≡1 mod5`, `k≡3`, least `128`; hence `N≡128 (mod210)`;
- D-M5: common period is lcm(8,12)=24.

## 14. DIAGNOSTIC_TAGS

- `CRT_AS_BRUTE_FORCE`
- `NONCOPRIME_COMPATIBILITY_MISSING`
- `INCOMPATIBLE_SYSTEM_NOT_REJECTED`
- `ONE_SOLUTION_NOT_CLASS`
- `FINAL_CONGRUENCE_NOT_RECHECKED`

## 15. H3_TO_H0_FADE_PLAN

- `D-F1 H3`: supply `N=a+mk` and the next substitution line.
- `D-F2 H2`: cue “view each congruence as a progression; check shared gcd.”
- `D-F3 H1`: ask only “compatible?” before any arithmetic.
- `D-F4 H0`: mixed system requiring independent compatibility check, parameter choice, reconstruction, and class statement.

`W1-D_GATE: PASS`