# W1-C — Same-Remainder Structure Interface

`ISSUE_AUTHORITY: #47`

`WAVE: 1C`

`STATUS: INTERFACE_COMPLETE`

## 1. CONCEPTS

- same number under several divisors;
- same divisor on several numbers;
- subtract-the-remainder construction;
- pairwise-difference divisibility;
- LCM as common-multiple structure;
- GCD as greatest common-divisor-of-differences structure;
- bounds and smallest/largest admissible reconstruction.

## 2. PREREQUISITES

- division algorithm;
- W1-A congruence meaning;
- HCF/GCD and LCM;
- arithmetic progressions and simple bounds.

## 3. LIKELY_HALF_KNOWLEDGE

- sees “same remainder” and chooses LCM before identifying what is fixed;
- knows the subtract-remainder trick but cannot explain it from divisibility;
- takes GCD of the original numbers instead of pairwise differences;
- finds the arithmetic progression family but forgets the final bound;
- accepts a claimed remainder that is not smaller than the divisor.

## 4. RECOGNITION_CUES

- “N leaves remainder r when divided by 12, 18, 30 …”;
- “greatest divisor leaving the same remainder when dividing A, B, C …”;
- “same remainder” plus either many divisors or many numbers.

## 5. FIRST_MOVES

Ask one grammatical question before calculating:

> Is the **number fixed and the divisors changing**, or is the **divisor fixed and the numbers changing**?

Then:
- fixed `N`, many divisors -> write `N-r`; use an LCM;
- fixed divisor `d`, many numbers -> subtract numbers; use a GCD of differences.

## 6. INVARIANTS

- if `N≡r (mod d_i)` for every `i`, then every `d_i | (N-r)`;
- if `A≡B≡C (mod d)`, then `d` divides every pairwise difference;
- for same-number structure, solutions repeat by the LCM;
- for greatest-divisor structure, the greatest possible `d` is the GCD of the relevant differences, subject to any remainder-size condition.

## 7. REPRESENTATION_SWITCHES

- verbal same-remainder statement -> congruences;
- congruences -> common multiple after subtracting `r`;
- equal residue classes -> divisibility of differences;
- bound on `N` -> choose a multiple of the LCM within the interval.

## 8. LEGALITY / ADMISSIBILITY CONDITIONS

- a remainder `r` on division by `d` requires `0≤r<d`;
- if the same divisor leaves remainder `r`, candidate `d` must exceed `r` if `r` is explicitly known;
- using only one pairwise difference can be insufficient when several numbers are involved; the divisor must divide all relevant differences;
- “greatest divisor” is not automatically the largest pairwise difference; take their GCD.

## 9. DECISION_BOUNDARIES

**DB-C1 flagship LCM vs GCD**  
`N` leaves remainder 4 under 16,24,36 -> `N-4` common multiple -> LCM.  
A divisor leaves equal remainders on 30,53,99 -> divisor divides differences -> GCD.

**DB-C2 remainder known vs merely equal**  
If remainder is specified, enforce `r<d`. If only “same remainder” is stated, the common remainder can be recovered afterward.

**DB-C3 least vs greatest value**  
Once `N=r+kL`, selecting least/greatest under a bound is a separate interval step, not a different number-theory mechanism.

## 10. MISCONCEPTION_TRAPS

- seeing “same remainder” and always using LCM;
- taking the GCD of the original numbers rather than their differences;
- forgetting to subtract the common remainder before LCM;
- forgetting an upper/lower bound after obtaining the family;
- accepting a divisor `d≤r` when the remainder `r` is prescribed.

## 11. CONTRAST_PAIRS

1. Same `N`, divisors 8 and 12, remainder 3 -> `N=24k+3`.
2. Same divisor on 53 and 29 -> divisor divides 24.
3. Same divisor on 53,29,17 -> use `gcd(24,12,36)=12`, not just 24.

## 12. TRANSFER_MECHANISMS

- one-word change from “divided by” to “divisor of several numbers” switches LCM to GCD;
- combine same-remainder family with a strict bound;
- recover the common remainder after finding the greatest divisor;
- determine whether a stated same-remainder condition is impossible because the claimed remainder is not smaller than the divisor.

## 13. SOURCE_IDS_AND_DISPOSITIONS

Clean scored flagship anchors:
- `NMTC-BH-P-2025-Q01` — same number, several divisors -> subtract remainder + LCM;
- `NMTC-BH-P-2024-Q21` — same divisor, several numbers -> pairwise differences + GCD.

These two must remain a paired teaching contrast.

## 14. CANDIDATE_MASTERY_ITEMS

`C-M1` Find the least positive integer greater than 100 that leaves remainder 5 on division by 12 and 18.

`C-M2` Find the greatest divisor that leaves the same remainder on 84,129,174.

`C-M3` Largest `N<5000` leaving remainder 7 when divided by 12,18,30.

`C-M4` A divisor `d` leaves remainder 8 on each of 50 and 92. Find all possible positive `d`.

`C-M5` Explain why `gcd(84,129,174)` is not the correct first quantity for an equal-remainder divisor problem.

Independent check:
- C-M1: `lcm(12,18)=36`; `N=36k+5`; least >100 is 113;
- C-M2: differences 45,45,90 -> gcd 45;
- C-M3: `lcm=180`; `N=180k+7`; largest <5000 is 4867;
- C-M4: `d | 42` and `d>8`; possibilities 14,21,42;
- C-M5: equal remainders imply divisibility of differences, not divisibility of the original numbers.

## 15. DIAGNOSTIC_TAGS

- `SAME_REMAINDER_LCM_REFLEX`
- `GCD_ORIGINAL_NUMBERS`
- `REMAINDER_NOT_SUBTRACTED`
- `BOUND_FILTER_MISSING`
- `REMAINDER_GE_DIVISOR`

## 16. H3_TO_H0_FADE_PLAN

- `C-F1 H3`: explicitly ask “which quantity becomes divisible after subtracting the remainder?”
- `C-F2 H2`: cue only “fixed number or fixed divisor?”
- `C-F3 H1`: underline the changing objects in the sentence.
- `C-F4 H0`: two near-identical unlabelled prompts, one LCM and one GCD, requiring independent method discrimination.

`W1-C_GATE: PASS`