# W1-E — Place Value & Digit Divisibility Interface

`ISSUE_AUTHORITY: #47`

`WAVE: 1E`

`STATUS: INTERFACE_COMPLETE`

## 1. CONCEPTS

- base-10 place-value algebra;
- two-/three-digit numbers and reversals;
- repeated blocks;
- derive divisibility by 9 and 11 from powers of 10;
- digit-sum constraints;
- ordered versus unordered digit choices;
- leading-zero restrictions;
- distinct digits can occupy the same residue class modulo a divisor.

## 2. PREREQUISITES

- decimal place value;
- elementary algebra;
- W1-A modular reduction;
- basic counting principle.

## 3. LIKELY_HALF_KNOWLEDGE

- knows divisibility-by-9/11 rules but cannot reconstruct them;
- can write `10a+b` after prompting but guesses digits before encoding;
- treats a pair of digits as unordered even when they form a numeral;
- forgets that a leading digit cannot be zero;
- identifies residue 0 mod9 with digit 0 only, overlooking digit 9.

## 4. RECOGNITION_CUES

- tens/units/hundreds digits;
- reversed number;
- digit sum or alternating sum;
- repeated block such as `ABCABC`;
- count numbers satisfying a digit-divisibility condition.

## 5. FIRST_MOVES

1. Encode the numeral before guessing: `10a+b`, `100a+10b+c`, etc.
2. Write digit domains explicitly (`a∈{1,...,9}` for a leading decimal digit; other digits may include 0).
3. If divisibility is involved, reduce powers of 10 modulo the divisor.
4. State whether ordered digit positions or unordered digit selections are being counted.

## 6. INVARIANTS

- a decimal numeral is a polynomial in 10 with digit coefficients;
- modulo 9, every power of 10 is congruent to 1;
- modulo 11, powers of 10 alternate `1,-1`;
- reversing a two-digit number changes it by `9(b-a)`;
- repeated block `ABCABC = 1001·ABC = 7·11·13·ABC`.

## 7. REPRESENTATION_SWITCHES

- digit words -> place-value polynomial;
- reversal -> swapped coefficients;
- divisibility by 9 -> digit sum mod9;
- divisibility by 11 -> alternating digit sum;
- repeated block -> factorization by `10^k+1`;
- digit count -> finite residue-state/counting table.

## 8. LEGALITY / ADMISSIBILITY CONDITIONS

- leading digit cannot be zero;
- digit variables are integers in `0..9`;
- “different digits” imposes inequality constraints;
- ordered numeral positions usually make `(a,b)` different from `(b,a)`;
- reducing a digit modulo 9 does not identify the digit itself (`0` and `9` share residue 0);
- divisibility rules must match the actual place positions/sign pattern.

## 9. DECISION_BOUNDARIES

**DB-E1 place-value algebra vs guessing**  
If a two-digit number and reversal are related, encode first; trial listing is inferior.

**DB-E2 rule vs proof**  
Digit-sum divisibility by 9 is not magic: derive from `10≡1 (mod9)`.

**DB-E3 ordered vs unordered**  
Digits 2 and 5 can make 25 and 52; counting a numeral is positional.

**DB-E4 digit identity vs residue identity**  
0 and 9 are different digits but both are residue 0 modulo 9.

**DB-E5 repeated block vs ordinary digit test**  
`ABCABC` should be factored by place value before applying ad-hoc divisibility tests.

## 10. MISCONCEPTION_TRAPS

- using `a+b` for the value of a two-digit number;
- allowing a leading zero;
- counting a digit pair only once when order matters;
- treating residue 0 as digit 0 only;
- memorizing alternating-sum signs incorrectly;
- testing `ABCABC` digit by digit instead of factoring 1001.

## 11. CONTRAST_PAIRS

1. “digits are 2 and 5” as an unordered set vs “two-digit number uses digits 2 and 5” as ordered numerals 25/52.
2. `N=100a+10b+c` divisible by 9 -> `a+b+c`; divisible by 11 -> `a-b+c` up to sign convention.
3. `ABCABC` -> structural factorization; arbitrary six-digit number -> ordinary place-value/residue analysis.

## 12. TRANSFER_MECHANISMS

- reversal relation where the unknown is a digit difference rather than the number itself;
- count three-digit multiples of 9 with a fixed digit and a leading-zero trap;
- repeated two-/three-digit block divisibility;
- derive a divisibility test for another modulus from powers of 10 rather than memorizing a rule.

## 13. SOURCE_IDS_AND_DISPOSITIONS

Clean scored anchors:
- `NMTC-BH-P-2018-Q28` — two-digit number and reversal;
- `NMTC-BH-P-2019-Q01` — repeated block factorization;
- `NMTC-BH-P-2019-Q16` — quotient/remainder/digit encoding;
- `NMTC-BH-P-2019-Q17` — digit sum plus algebraic relation;
- `NMTC-BH-P-2025-Q14` — direct two-digit place-value equations;
- `NMTC-BH-P-2025-Q21` — digit counting via modulo 9, including residue-class subtlety.

## 14. CANDIDATE_MASTERY_ITEMS

`E-M1` A two-digit number has digit sum 11 and exceeds its reversal by 27. Find the number(s).

`E-M2` Prove from place value why divisibility by 9 is determined by digit sum.

`E-M3` For a four-digit number `abcd`, derive the mod-11 alternating-sum relation.

`E-M4` How many two-digit numbers have digit sum divisible by 9? Count positionally and enforce a nonzero tens digit.

`E-M5` Show that every six-digit repeated block `ABCABC` is divisible by 7, 11 and 13.

Independent check:
- E-M1: `(10a+b)-(10b+a)=9(a-b)=27`, so `a-b=3`; `a+b=11`; `(a,b)=(7,4)`, number 74;
- E-M2: `10^k≡1 (mod9)`;
- E-M3: `1000a+100b+10c+d≡-a+b-c+d (mod11)`;
- E-M4: sums 9 or 18; sum 9 gives 9 choices for tens 1..9 with units 8..0; sum18 only (9,9), total 10;
- E-M5: `ABCABC=1001·ABC`, `1001=7·11·13`.

## 15. DIAGNOSTIC_TAGS

- `DIGIT_GUESSING_BEFORE_ENCODING`
- `LEADING_ZERO_ADMITTED`
- `ORDERED_UNORDERED_CONFUSION`
- `RESIDUE_CLASS_AS_DIGIT_IDENTITY`
- `DIVISIBILITY_RULE_WITHOUT_PLACE_VALUE`
- `REPEATED_BLOCK_STRUCTURE_MISSED`

## 16. H3_TO_H0_FADE_PLAN

- `E-F1 H3`: provide the place-value expression and ask learner to finish the relation.
- `E-F2 H2`: cue “write the numeral as powers of 10; state digit domains.”
- `E-F3 H1`: point only to “digits/reversal/repeated block.”
- `E-F4 H0`: unlabelled digit-count/reversal problem where learner must encode, choose modulus, decide order, and enforce leading-zero restrictions independently.

`W1-E_GATE: PASS`