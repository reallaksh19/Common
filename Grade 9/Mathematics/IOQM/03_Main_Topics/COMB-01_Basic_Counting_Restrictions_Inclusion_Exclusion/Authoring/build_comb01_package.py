from pathlib import Path
import csv, io, textwrap

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / 'Authoring'
PDFS = ROOT / 'PDFs'
AUTH.mkdir(parents=True, exist_ok=True)
PDFS.mkdir(parents=True, exist_ok=True)

files = {}

files['00_Concept_and_Dependency_Map.md'] = r'''# COMB-01 - Concept and Dependency Map

Status: `STATIC_SOURCE_AUTHORING`
Canonical owner: `IOQM-G9-COMB-01`

## Governing belief

`DEFINE THE OBJECT -> ORDERED OR UNORDERED? -> RESTRICTIONS -> DISJOINT CASES OR STAGES -> DIRECT / COMPLEMENT / IE -> COUNT -> DOUBLE-COUNT CHECK`

Counting is not formula matching. A count is valid only after the counted object and its identity are fixed.

## Canonical scope

Owned here:
- addition principle with explicit disjointness;
- multiplication principle with explicit sequential-stage semantics;
- permutation and combination derived from ordered/unordered structure;
- repeated-object identity and multiset arrangements;
- restrictions and position constraints;
- complement counting;
- inclusion-exclusion for overlapping properties;
- digit-string counting when the task is to count admissible strings/numbers.

Retrieved / not duplicated:
- arithmetic digit properties, divisibility and place-value algebra belong to `IOQM-G9-NT-05` when arithmetic structure is the learning target;
- recurrence/state evolution belongs to `IOQM-G9-COMB-03`; this topic exports counting/model language to it;
- graph coloring and forbidden-subgraph canon belong to `IOQM-G9-COMB-02`;
- advanced group-action/Burnside formalism is not introduced; the 2023 dice anchor is handled by fixing a rotational frame and counting representatives.

## Dependency graph

Prerequisites: integer arithmetic, factorial notation, elementary set language.
Downstream consumers: `IOQM-G9-COMB-02`, `IOQM-G9-COMB-03`, selected NT/GEO applications.
Stable provider interface: `Authoring/COMB01_Stable_Counting_Model_Interface_v1.md`.

## Seven production microstreams

1. addition and multiplication principles;
2. permutation/combination derivation;
3. repeated objects and identity;
4. restrictions and position constraints;
5. complement and inclusion-exclusion;
6. digit-string counting and NT-05 boundary;
7. source/PYQ/misconception audit.
'''

files['01_Source_Coverage_Map.md'] = r'''# COMB-01 - Source Coverage Map

All historical items below retain the frozen corpus ID, paper/key custody and independently verified answer. They are source anchors, not a claim of official topic frequency.

| Stable ID | Verified answer | Canonical mechanism here | Independent reconstruction |
|---|---:|---|---|
| `IOQM-2025-Q05` | 45 | restricted digit counting | for hundreds digit `a=1,...,9`, allowed tens digits number `10-a`; sum `9+...+1=45` |
| `IOQM-2025-Q15` | 40 | restricted injection / inclusion-exclusion | three coupon-pairs have allowed envelope sets of size 4 and distinct envelope choices; direct restricted-injection or IE count gives 40 |
| `IOQM-2025-Q18` | 40 | multiset permutations + complement/relative order | choose positions of two 2s in `C(9,2)=36`; among the remaining 3 threes and 4 fours, required final symbol is 3 in `C(6,2)=15` ways; `N=540`, remainder 40 mod 100 |
| `IOQM-2024-Q02` | 12 | position restriction + permutation | units digit is 1 or 3, then arrange remaining three digits: `2*3!=12` |
| `IOQM-2023-Q07` | 48 | symmetry-normalized arrangements | fix opposite faces 1,2; six cyclic orders of 3,4,5,6 around the axis and `2^3` opposite-pair colour choices give 48 |
| `IOQM-2023-Q17` | 66 | unordered subsets + order-statistic symmetry | for a uniform 5-subset of `1,...,99`, the expected fourth order statistic is `4*100/6=200/3`; requested floor is 66 |
| `IOQM-2023-Q20` | 43 | finite-set cardinality/max constraints + binomial counts | factor the two cardinality/maximum equations; count feasible subsets containing prescribed maxima; repository verification gives `N=439`, requested `4+39=43` |

## Source custody

### 2025 Q05/Q15/Q18
Paper: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/en.M1.pdf`
Key: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/final-key-7th-September.pdf`
Authority: `HBCSE_OFFICIAL`; key status: `FINAL_OFFICIAL`.

### 2024 Q02
Paper: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf`
Key: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf`
Authority: `HBCSE_OFFICIAL`; key status: `OFFICIAL_HBCSE_KEY`.

### 2023 Q07/Q17/Q20
Paper/key: `https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf`
Authority: `HBCSE_LINKED_MTAI`; key status: `HBCSE_LINKED_MTAI_EMBEDDED_KEY`.

Independent verification authority: `01_Corpus/Verification/IOQM_Independent_Answer_Verification_Batch_A_Q01_Q10_v1.md` and `...Batch_B_Q11_Q20_v1.md`.
'''

files['02_Assimilation_Book.md'] = r'''# Basic Counting, Restrictions & Inclusion-Exclusion
## Integrated Assimilation Book

> **Count objects, not formulas. First decide what makes two outcomes the same.**

## 1. RECONNECT - what is the counted object?

Suppose you own 3 shirts and 4 caps. An outfit is an ordered pair `(shirt, cap)`. There are `3*4=12` outfits because every shirt choice can be followed by every cap choice.

Now suppose you may travel by one of 5 buses or one of 3 trains. These are disjoint types of journey, so there are `5+3=8` choices.

The symbols `+` and `*` are not automatic. They encode different structures:
- **add** counts from disjoint alternatives;
- **multiply** counts sequential stages when every first-stage choice can be combined with the counted second-stage choices.

### The exact-one rule

Before adding case counts, ask:

`Does every valid object enter exactly one case?`

If some object enters two cases, naive addition double-counts. If some object enters no case, the split is incomplete.

## 2. DISCOVER - ordered or unordered?

Choosing a captain and vice-captain from 8 people is ordered: `(A,B)` and `(B,A)` are different roles. Count `8*7=56`.

Choosing two representatives from 8 is unordered: `{A,B}` and `{B,A}` are the same pair. The ordered count `8*7` counts each pair twice, so divide by `2!`:

`C(8,2)=8*7/2=28`.

This is the meaning behind permutation and combination notation:
- order matters -> ordered arrangements;
- order does not matter -> remove the overcount caused by rearranging the chosen objects.

## 3. MAKE SENSE - derive, do not memorize

For `r` ordered selections from `n` distinct objects without replacement:

`n*(n-1)*...*(n-r+1)`.

For an unordered `r`-subset, each chosen set appears in `r!` orders, so

`C(n,r) = n*(n-1)*...*(n-r+1) / r!`.

The formula is the last line of the reasoning, not the first question to ask.

## 4. Repeated objects change identity

How many distinct arrangements of `AABC` are there?

If the two A's were temporarily named `A1,A2`, there would be `4!` arrangements. Swapping `A1,A2` changes no visible word, so every visible arrangement was counted `2!` times.

Therefore the count is `4!/2!=12`.

For multiplicities `m1,m2,...` summing to `n`, the same identity argument gives

`n!/(m1!m2!... )`.

Use this only when objects within each repeated class are genuinely indistinguishable for the problem.

## 5. Restrictions should enter before the factorial

To form a 4-digit odd number using `1,2,3,4` exactly once, the units digit must be `1` or `3`. Choose the restricted position first:

`2 * 3! = 12`.

This is often cheaper than counting all `4!` permutations and then testing parity.

### Position-first cue

When one condition strongly controls a position (last digit, first digit, fixed role, forbidden envelope), handle that position or restriction before expanding the rest of the count.

## 6. Complement - count the easier opposite event

To count length-7 binary strings with at least one `1`, direct cases by first `1` are possible but unnecessary.

All binary strings: `2^7`.
The only forbidden string with no `1`: one string.

Required count: `2^7-1=127`.

Complement is especially useful for phrases such as:
- at least one;
- not all;
- at least one violation;
- a difficult relative-order event whose opposite has rigid structure.

## 7. Inclusion-exclusion - overlap must be repaired explicitly

Among the integers `1,...,100`, how many are divisible by 2 or 5?

Multiples of 2: 50.
Multiples of 5: 20.
Multiples of both, i.e. 10: 10.

If we add `50+20`, the multiples of 10 were counted twice. Subtract the overlap once:

`50+20-10=60`.

For three properties, the same principle continues:

`single counts - pair overlaps + triple overlap`.

Do not use inclusion-exclusion when the original cases are already disjoint.

## 8. Digit strings: counting structure versus arithmetic structure

A digit problem can belong to two different worlds.

**Counting question:** How many 4-digit odd numbers use `1,2,3,4` exactly once? The arithmetic condition only restricts the last position; the main work is counting admissible arrangements.

**Arithmetic digit question:** Which numbers are divisible by 11, or how does a decimal block reduce modulo a divisor? That arithmetic mechanism belongs to the later digit-structure topic. Here we may retrieve such a restriction, but we do not reteach its number-theory derivation.

Boundary rule:

`If the property is already known and the task is to count strings satisfying it -> count here.`

`If the task is to derive or exploit the arithmetic digit property itself -> route to number theory.`

## 9. Historical anchors as decision models

### Restricted digit relation
The 2025 three-digit anchor is not a permutation problem. The relation `c=a+b` converts the number into bounded integer-pair choices. Counting admissible `(a,b)` pairs gives 45.

### Grouped restricted assignment
The 2025 coupon anchor treats `(1,2)`, `(3,4)`, `(5,6)` as three grouped objects assigned injectively to six envelopes, each with two forbidden envelopes. The restriction belongs in the assignment model before any factorial shortcut. The verified count is 40.

### Multiset + complement
For permutations of `223334444`, repeated digits require multiset counting. The relative-order condition becomes simpler when phrased through the last symbol among the 3/4 subsequence; the verified count is 540, giving remainder 40 modulo 100.

### Position restriction
The 2024 odd-number anchor chooses the units digit first, then permutes the remaining symbols: 12.

### Rotational equivalence
The 2023 dice anchor first fixes the opposite `1,2` axis. The remaining four labels have six cyclic orders around that axis; the three opposite face-pairs each choose one of two colours. The repository's independent verification gives 48. No formal group-action machinery is needed for this Grade-9 interface.

### Unordered selection symmetry
The 2023 order-statistic anchor treats increasing 5-tuples as 5-subsets. Reflection/order-statistic symmetry avoids enumerating every subset and leads to 66.

### Finite-set constraints
The 2023 finite-set anchor first solves constraints on set size and maximum, then uses binomial counts for lower elements. It is a model-first count, not raw subset enumeration; the verified requested value is 43.

## 10. TRY - support fades toward independence

### Full support
How many 5-bit strings contain exactly two `1`s?
Identify the two positions of the `1`s: `C(5,2)`.

### Medium support
How many 4-person committees from 10 contain at least one of two specified people?
Cue: the complement excludes both specified people.

### Light support
How many arrangements of `AABBCC` have the two A's nonadjacent?
Cue: total minus an `AA` block.

### Independent
How many 6-letter strings over `{A,B,C,D}` use every symbol at least once?
Choose and justify direct/complement/inclusion-exclusion without a method label.

## 11. DIAGNOSE - common counting failures

- **Object drift:** switching halfway from ordered sequences to unordered sets.
- **Case overlap:** adding counts when one object satisfies two cases.
- **Case gap:** a split does not cover every valid object.
- **Factorial reflex:** writing `n!` before restrictions are modeled.
- **Repeated-object overcount:** treating identical copies as labelled.
- **Complement mismatch:** subtracting from the wrong universe.
- **Arithmetic/counting collision:** deriving a divisibility rule inside a problem whose actual task is only to count already-characterized strings.

## 12. ADOPT - the counting checklist

1. What exactly is one object/outcome?
2. When are two outcomes considered the same?
3. Is order structural?
4. What restrictions must every object satisfy?
5. If splitting into cases, are the cases disjoint and exhaustive?
6. If making stages, does each stage count the choices available after previous choices?
7. Would the complement be simpler?
8. If properties overlap, where is inclusion-exclusion needed?
9. Are repeated symbols genuinely indistinguishable?
10. Does a digit condition belong to counting or to arithmetic structure?
11. Check small cases or an alternate count when practical.

## 13. TRANSFER

This language is designed to be retrieved downstream.

For recurrence/state problems, the consumer may say: define the counted state, split every valid object into exactly one first-step branch, multiply within stages, and add only disjoint branches. It should not re-teach combinations, repeated-object formulas or inclusion-exclusion.

For graph/coloring problems, the same counted-object, restriction and complement vocabulary applies, while graph-specific canon remains with its owner.
'''

files['03_First_Step_Reference.md'] = r'''# Basic Counting - First-Step Reference

## One-question router

> **What is one counted object, and when are two objects the same?**

Then ask:

`ORDER? -> RESTRICTIONS? -> DISJOINT CASES OR STAGES? -> DIRECT / COMPLEMENT / IE -> CHECK`

## Recognition atlas

| Visible clue | First move |
|---|---|
| one choice followed by another | define stages; multiply stage counts |
| one of several nonoverlapping types | prove disjointness; add case counts |
| roles/sequence/positions | treat as ordered unless the problem identifies orders |
| committee/subset/group | treat as unordered unless roles are later assigned |
| repeated symbols | divide labelled count by permutations of identical copies |
| last/first digit restriction | handle the restricted position first |
| at least one / not all | test whether complement is shorter |
| two properties joined by “or” | check overlap before adding |
| multiple overlapping restrictions | consider inclusion-exclusion |
| digit condition | decide whether arithmetic property is given or must be derived |

## Exact-one case test

Before adding branches:
1. Every valid object belongs to at least one branch.
2. No valid object belongs to two branches.

If either fails, repair the split before counting.

## Identity test

Before dividing by a factorial, state exactly which labelled arrangements become the same visible object.
'''

files['04_Recognition_and_First_Line_Lab.md'] = r'''# Basic Counting - Recognition and First-Line Lab

Write only the first useful model/counting line unless asked for a value.

1. Choose a captain and vice-captain from 9 students: ordered or unordered?
2. Choose a 3-person committee from 9: ordered or unordered?
3. A meal chooses one starter from 4 and one main from 6: add or multiply?
4. A route is either one of 5 bus routes or one of 2 train routes: what condition makes addition valid?
5. Arrange `AABC`: what overcount must be removed?
6. Form a 4-digit even number using `1,2,3,4` once: which position should be chosen first?
7. Count 8-bit strings with at least one `1`: name the easier complementary event.
8. Count integers divisible by 3 or 5: what overlap must be corrected?
9. Split a count by “starts with A” and “contains A”: why is naive addition unsafe?
10. A recurrence splits tilings by first tile: what exact-one question must be checked before adding branches?
11. Assign three distinct tasks to five people, at most one task per person: identify the sequential stages.
12. Select 4 people from 10 with at least one of two specified people: write the complement universe.
13. A word contains repeated L's and O's: what must be decided before using a multiset formula?
14. A number must be divisible by 4 and the divisibility characterization is already supplied: is the remaining task arithmetic derivation or counting?
15. Two restrictions overlap: state when inclusion-exclusion becomes necessary.
16. A set problem specifies the maximum element: what must every counted subset contain?
'''

files['05_Practice_and_Transfer_Bank.md'] = r'''# Basic Counting - Practice and Transfer Bank

## Foundation
1. An outfit uses one of 3 shirts and one of 4 caps. How many outfits?
2. A trip uses exactly one of 5 bus routes or 3 train routes. How many route choices?
3. How many 2-person committees can be chosen from 6 people?
4. How many linear arrangements of 4 distinct books are possible?
5. How many distinct arrangements of the letters `AABC` are possible?

## Direct
6. How many 4-digit even numbers can be formed using `1,2,3,4` exactly once?
7. How many 3-person committees can be chosen from 8 people?
8. How many distinct arrangements of `BANANA` are possible?
9. How many length-3 strings can be formed from `1,2,3,4,5` without repetition?
10. How many binary strings of length 5 contain exactly two `1`s?

## Standard
11. How many 4-digit numbers can be formed from `0,1,2,3,4,5` without repetition?
12. In how many permutations of `1,2,3,4,5,6` does `1` occur before `2`?
13. How many subsets of `{1,2,3,4,5,6,7,8}` contain exactly one of `1,2`?
14. Three distinct tasks are assigned to three different people chosen from five. How many assignments?
15. How many length-3 strings over `{0,1,2,3,4}` contain at least one `0`?

## Disguised
16. How many distinct arrangements of `BALLOON` are possible?
17. How many 5-digit even numbers can be formed from `0,1,2,3,4,5,6` without repetition?
18. How many 4-person committees from 10 contain at least one of two specified people?
19. How many permutations of `1,2,3,4,5,6,7` have `1` and `2` nonadjacent?
20. Five people stand in a line. In how many orders is A left of B and C left of D?
21. Four letters are placed into four addressed envelopes, one per envelope. How many placements put no letter in its matching envelope?
22. How many integers from 1 through 100 are divisible by 2 or 5?

## Preliminary-style
23. How many length-6 strings over `{A,B,C,D}` use every symbol at least once?
24. How many distinct arrangements of the multiset `112233` end in `3`?
25. How many distinct length-7 strings with three `1`s, two `2`s and two `3`s do not begin with `1`?
26. A committee of 5 is chosen from 12 people, including 4 designated seniors. How many committees contain at least 2 seniors?
27. In a class of 30, 18 study mathematics, 16 study physics and 9 study both. How many study at least one of the two subjects, and how many study neither?
28. How many length-5 digit strings (leading zero allowed) use distinct digits from `0,1,2,3,4,5` and contain exactly two even digits?
29. How many distinct arrangements of `AABBCC` have the two A's nonadjacent?
30. How many length-6 strings over `{0,1,2}` use all three symbols at least once?
'''

files['06_H0_Mastery_Test.md'] = r'''# Basic Counting - Independent Mixed Mastery Check

No default hints or method labels.

1. Choose a captain and vice-captain from 8 students. How many choices?
2. Choose two representatives from 8 students. How many choices?
3. How many 4-digit odd numbers use `1,2,3,4` exactly once?
4. How many distinct arrangements of `LEVEL` are possible?
5. How many length-7 binary strings contain at least one `1`?
6. How many integers from 1 through 120 are divisible by 3 or 4?
7. How many 4-person committees from 9 do not contain both A and B?
8. How many 5-digit numbers can be formed from `0,1,2,3,4,5` without repetition?
9. Four letters are placed into four addressed envelopes, one per envelope. How many placements have no correct address?
10. How many distinct arrangements of `112233` end in `2`?
11. A committee of 4 is chosen from 10 people. How many contain at least one of three specified people?
12. How many permutations of `A,B,C,D,E,F` satisfy A before B, C before D and E before F?
13. How many length-5 strings over `{A,B,C}` use all three symbols?
14. How many distinct arrangements of `BANANA` are possible?
15. How many length-5 digit strings (leading zero allowed) use distinct digits from `0,1,2,3,4,5` and contain exactly two even digits?
16. How many 3-person committees from 8 contain at least one of two specified people?
'''

files['Teacher_Diagnostic_Key.md'] = r'''# COMB-01 - Teacher Diagnostic Key

Teacher/control artifact. Internal topic and support-control language is allowed here; it is not included in the student PDF.

## Governing diagnostic

A wrong numerical count should be classified before correcting arithmetic:
1. counted-object/identity error;
2. ordered-vs-unordered error;
3. non-disjoint or non-exhaustive case split;
4. stage/product error;
5. repeated-object overcount;
6. restriction applied too late;
7. complement universe mismatch;
8. inclusion-exclusion overlap error;
9. counting/arithmetic ownership collision.

## Historical anchors

- `IOQM-2025-Q05 = 45`: sum admissible pair counts `9+8+...+1`.
- `IOQM-2025-Q15 = 40`: restricted injection of three coupon-pairs into distinct envelopes; allowed sets `{3,4,5,6}`, `{1,2,5,6}`, `{1,2,3,4}`. IE check: `120-120+48-8=40`.
- `IOQM-2025-Q18 = 40`: `C(9,2)*C(6,2)=540`, requested remainder mod 100 is 40.
- `IOQM-2024-Q02 = 12`: `2*3!`.
- `IOQM-2023-Q07 = 48`: fix the 1/2 axis, six cyclic orders, `2^3` opposite-pair colour choices.
- `IOQM-2023-Q17 = 66`: fourth order statistic expectation `200/3`, requested floor 66.
- `IOQM-2023-Q20 = 43`: factor cardinality/max constraints, then binomial counts; independent verification gives `N=439`, requested `4+39`.

## Practice answers

1. 12 — product of 3 shirt and 4 cap choices.
2. 8 — disjoint alternatives `5+3`.
3. 15 — `C(6,2)`.
4. 24 — `4!`.
5. 12 — `4!/2!`.
6. 12 — choose units digit 2 or 4, then `3!`.
7. 56 — `C(8,3)`.
8. 60 — `6!/(3!2!)`.
9. 60 — `5*4*3`.
10. 10 — choose positions of two ones: `C(5,2)`.
11. 300 — first digit 5 choices, then `5*4*3`.
12. 360 — symmetry: half of `6!` have 1 before 2.
13. 128 — choose which of 1,2 is present, then any subset of remaining six: `2*2^6`.
14. 60 — ordered injection `5*4*3`.
15. 61 — `5^3-4^3`.
16. 1260 — `7!/(2!2!)`.
17. 1260 — last digit 0 contributes `6*5*4*3=360`; last digit 2/4/6 contributes `3*(5*5*4*3)=900`.
18. 140 — `C(10,4)-C(8,4)=210-70`.
19. 3600 — `7!-2*6!`.
20. 30 — the two pairwise order constraints divide `5!` by 4.
21. 9 — derangements of four; IE gives `24-24+12-4+1=9`.
22. 60 — `50+20-10`.
23. 1560 — `4^6-4*3^6+6*2^6-4`.
24. 30 — fix one 3 last, arrange `11223`: `5!/(2!2!)`.
25. 120 — total `7!/(3!2!2!)=210`; bad first-1 arrangements `6!/(2!2!2!)=90`.
26. 456 — `C(4,2)C(8,3)+C(4,3)C(8,2)+C(4,4)C(8,1)`.
27. 25 at least one; 5 neither — `18+16-9=25`.
28. 360 — choose 2 of the 3 even and all 3 odd digits, then arrange: `C(3,2)*5!`.
29. 60 — total `6!/(2!2!2!)=90`; bad AA-block `5!/(2!2!)=30`.
30. 540 — `3^6-3*2^6+3`.

## Independent mastery answers

1. 56 — ordered roles `8*7`.
2. 28 — unordered `C(8,2)`.
3. 12 — last digit 1 or 3, then `3!`.
4. 30 — `5!/(2!2!)`.
5. 127 — `2^7-1`.
6. 60 — `40+30-10`.
7. 105 — `C(9,4)-C(7,2)=126-21`.
8. 600 — first digit 5 choices, then `5*4*3*2`.
9. 9 — derangements of four.
10. 30 — fix one 2 last, arrange `11223`.
11. 175 — `C(10,4)-C(7,4)=210-35`.
12. 90 — each of three independent pair-order constraints halves `6!`: `720/8`.
13. 150 — `3^5-3*2^5+3`.
14. 60 — `6!/(3!2!)`.
15. 360 — `C(3,2)*C(3,3)*5!`.
16. 36 — `C(8,3)-C(6,3)=56-20`.

## H-control fading map

H3: counted object, representation and first computation line supplied.
H2: counted object/representation supplied; computation withheld.
H1: only the distinguishing clue is supplied.
H0: no route label or default hint.

These H-levels are teacher controls and must not appear in the learner export.
'''

files['Authoring/Independent_Mathematics_Audit.md'] = r'''# COMB-01 - Independent Mathematics Audit

Status: `PASS_STATIC_SOURCE_MATH`

## Historical anchors

All seven required anchors agree with the frozen repository verification authority.

- `IOQM-2025-Q05=45`: direct bounded-pair sum.
- `IOQM-2025-Q15=40`: direct restricted injection; independent inclusion-exclusion check `120-120+48-8=40`.
- `IOQM-2025-Q18`: exact count 540, requested remainder mod 100 is 40.
- `IOQM-2024-Q02=12`: two valid units digits, then `3!`.
- `IOQM-2023-Q07=48`: six cyclic label orders after fixing the 1/2 axis, times eight opposite-pair colourings.
- `IOQM-2023-Q17=66`: verified order-statistic symmetry route.
- `IOQM-2023-Q20=43`: verified finite-set cardinality/max route with binomial subset counts.

## Authored bank

Practice 1-30 and mastery 1-16 were recomputed independently using direct enumeration identities, complement, inclusion-exclusion or symmetry as appropriate. Promoted numerical answers in `Teacher_Diagnostic_Key.md` were checked against a second calculation where practical.

## Ownership audit

- no recurrence/state-evolution canon is authored here;
- no graph-coloring canon is authored here;
- no divisibility/place-value rule is derived here;
- repeated-object formulas are derived from identity/overcount, not presented as unexplained tables;
- addition is explicitly gated on disjointness and multiplication on stage semantics.
'''

files['Authoring/COMB01_Stable_Counting_Model_Interface_v1.md'] = r'''# COMB-01 Stable Counting / Model Interface v1

Status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`
Provider: `IOQM-G9-COMB-01`
Primary consumers: `IOQM-G9-COMB-02`, `IOQM-G9-COMB-03`

This interface exports concise counting/model semantics. Consumers retrieve these statements; they do not rebuild the underlying counting chapter.

## Minimum provider payload

### C01-1 — Counted-object definition
**Canonical wording:** Before counting, define one valid object/outcome and state when two objects are considered the same.
Retrieval example: “A state represents one partial tiling with the same remembered boundary data; two construction histories leading to the same defined state are not automatically two states.”

### C01-2 — Addition principle semantics
**Canonical wording:** Add case counts only when the cases are disjoint. If cases overlap, naive addition is invalid.

### C01-3 — Multiplication principle semantics
**Canonical wording:** Multiply stage counts when an object is built through sequential choices and the stated count at each stage is the number of choices available after the earlier stage choices.

### C01-4 — Exhaustiveness discipline
**Canonical wording:** A case split is valid only if every valid object enters at least one case. A disjoint-and-exhaustive split makes every valid object enter exactly one branch.
Checklist question: `Does every valid object enter exactly one branch?`

### C01-5 — Ordered vs unordered decision
**Canonical wording:** Order is structural when exchanging positions/roles/stages changes the object. If exchanging selected elements does not change the object, count unordered selections and remove the permutation overcount.
Retrieval cue: “Would swapping the two selected elements create a different valid object?”

### C01-6 — Direct vs complement decision
**Canonical wording:** When the desired event is difficult but its negation has a simpler description, count `universe - complement`. The universe and complement must use the same object definition.

### C01-7 — Restriction vocabulary
Use these stable terms:
- **allowed choice:** satisfies all restrictions active at that stage;
- **forbidden choice:** violates at least one active restriction;
- **state memory / remembered condition:** information needed so future allowed choices can be determined;
- **local restriction:** depends only on the current position/stage/state;
- **global restriction:** depends on the completed object or on information that must be carried in state;
- **admissible object:** satisfies every original restriction.

### C01-8 — Inclusion-exclusion boundary
**Canonical wording:** If properties/cases overlap, do not add their counts as if disjoint. Either redesign a disjoint split or use inclusion-exclusion from the counting owner. A recurrence consumer must fail closed rather than inventing its own generic IE chapter.

### C01-9 — Repeated-object distinction
**Canonical wording:** Two copies are indistinguishable only if swapping them does not create a new counted object. When labelled arrangements differ only by permutations inside identical classes, divide by those internal permutation counts exactly once.

### C01-10 — Digit-string counting boundary
**Canonical wording:** Counting admissible digit strings belongs here once the arithmetic property/restriction is known. Deriving divisibility, decimal-block, digit-sum/product or place-value arithmetic rules belongs to the number-theory digit owner.

## Compatibility tests

### T1 — Retrieval, not reteaching: PASS
A consumer may write “these first-step cases are disjoint, so add their counts” using C01-2 without deriving the addition principle.

### T2 — Exact-one-branch test: PASS
C01-4 provides the exact canonical question: `Does every valid object enter exactly one branch?`

### T3 — Ordered/unordered stability: PASS
C01-5 defines identity structurally and does not depend on `nPr`/`nCr` notation.

### T4 — Overlap fail-closed: PASS
C01-2 and C01-8 explicitly prohibit naive addition of overlapping branches.

### T5 — Restriction handoff: PASS
C01-7 provides `state memory / remembered condition` plus local/global restriction language sufficient to name previous tile type, carry, boundary occupancy or any other information needed to determine future legal moves.

### T6 — Boundary ownership: PASS
Consumers do not own generic permutation/combination derivation, repeated-object formula derivation, generic complement/IE teaching, or arithmetic digit properties. Those remain with this provider or the digit-arithmetic owner as stated above.

## Retrieval map for COMB-03

| Consumer move | Retrieve here | Consumer adds |
|---|---|---|
| define counted state | C01-1, C01-7 | minimal sufficient state |
| split by first/last move | C01-2, C01-4 | recurrence from smaller states |
| count transition stages | C01-3 | transition-specific choices |
| avoid double count | C01-5, C01-8 | recurrence branch validation |
| compare direct/complement/recursive routes | C01-6 | recursion usefulness test |

No student-facing control codes are exported from this authoring interface into learner materials.
'''

# Seven schema-compliant microstream interfaces.
streams = [
('W1-A','addition-multiplication','Addition and multiplication principles','disjoint alternatives and sequential stages','addition requires disjoint cases; multiplication requires valid stage counts after previous choices','IOQM-2024-Q02'),
('W1-B','permutation-combination','Permutation and combination derivation','ordered roles/sequences versus unordered selections','combination counts arise by removing the r! order overcount from ordered selections','IOQM-2023-Q17'),
('W1-C','repeated-objects','Repeated objects and identity','multiset arrangements and indistinguishable copies','divide only by permutations inside classes whose swaps do not change the counted object','IOQM-2025-Q18'),
('W1-D','restrictions','Restrictions and position constraints','forbidden/required positions, grouped assignments and restricted injections','apply the strongest restriction before unrestricted factorial counting when it reduces the state space','IOQM-2025-Q15; IOQM-2024-Q02'),
('W1-E','complement-inclusion-exclusion','Complement and inclusion-exclusion','universe/complement modeling and overlap correction','complement uses the same universe; IE repairs repeated membership in overlapping properties','IOQM-2025-Q18; IOQM-2025-Q15'),
('W1-F','digit-string-counting','Digit-string counting and arithmetic boundary','counting admissible strings once arithmetic restrictions are known','counting owns arrangement of admissible digits; arithmetic digit-rule derivation remains with NT-05','IOQM-2025-Q05; IOQM-2024-Q02'),
('W1-G','source-pyq-audit','Source, symmetry and misconception audit','source custody, independent verification, symmetry normalization and ownership drift','historical mechanisms are preserved without expanding this topic into recurrence, graph or digit-arithmetic canon','all seven required anchors'),
]
index=['# COMB-01 - Microstream Interface Index','','Status: `INDEX_ONLY__NOT_INTERFACE_AUTHORITY`','','Mandatory interface authority:']
for mid,slug,title,scope,invariant,anchors in streams:
    fn=f'IOQM-G9-COMB-01__{mid}__{slug}__interface.md'
    index.append(f'- `{fn}`')
    files['Authoring/'+fn]=f'''---
main_topic_id: IOQM-G9-COMB-01
microstream_id: {mid}
microstream_title: {title}
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-01
prerequisite_interfaces: []
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: {scope}. Excluded: generic recurrence/state evolution, graph-coloring canon and arithmetic digit-rule derivation.
## B. Learner-state model
PRIOR_KNOWLEDGE: basic factorial notation and informal counting. LIKELY_HALF_KNOWLEDGE: can apply formulas but may not define identity/cases. MISSING_BRIDGES: object definition, exact-one cases, restriction-first modeling. OWNERSHIP_TARGET: structure before formula.
## C. Mathematical invariant / governing structure
{invariant}. The topic router is `DEFINE OBJECT -> IDENTITY/ORDER -> RESTRICTIONS -> CASES/STAGES -> DIRECT/COMPLEMENT/IE -> COUNT -> CHECK`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| object + identity rule | what is distinct | state equivalence | before counting | formula-first |
| case split | alternatives | test disjoint/exhaustive | exact-one branches | naive addition |
| stages | sequential choices | count choices per stage | later counts respect earlier choices | independent multiplication |
| complement/property sets | forbidden/overlap structure | define universe | same object universe | subtract unrelated counts |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| ordered vs unordered | arrangements/roles | subsets | does swapping selected elements change the object? | same chosen elements |
| direct vs complement | count desired | universe minus forbidden | which description is simpler? | direct wording feels mandatory |
| disjoint cases vs IE | add | repair overlap | can one object enter two cases? | both use addition signs |
| digit counting vs arithmetic | count known-valid strings | NT-05 | is the digit property being derived? | same decimal surface |
## F. Misconception/diagnosis catalogue
ERROR_CODE: COMB01-{mid}-01
WRONG_MOVE: write a factorial/binomial expression before defining the counted object and restrictions.
WHY_TEMPTING: familiar surface keywords.
MISSING_LINK_CLASS: MODEL_SELECTION
REPAIR_INVARIANT: define identity, then verify stages/cases before calculating.
FALSIFIER_OR_CONTRAST: two solutions with the same formula surface can differ because one is ordered and the other unordered.
## G. First-move cues
Name one object, decide identity/order, list active restrictions, then choose disjoint cases or sequential stages.
## H. H3 -> H0 fading plan
H3: object and case/stage model supplied. H2: object supplied, split withheld. H1: only the decisive identity/restriction cue. H0: changed surface with no method label.
## I. Validated IOQM source anchors
{anchors}. Exact source/key custody and independent routes are recorded in the source map and audit.
## J. Source-independent mathematical trace
Promoted counts are recomputed with a second route or small-case check where practical; IE signs and repeated-object multiplicities are explicitly audited.
## K. Contrast-pair candidates
ordered/unordered; disjoint/overlapping; direct/complement; distinct/repeated; counting/arithmetic digit structure.
## L. Transfer candidates
restricted assignments; subset statistics; finite-set counts; recurrence branch validation; graph/coloring restrictions.
## M. Candidate mastery items
recognition; first-line model; full count; WHY-NOT formula; overlap repair; changed-surface transfer.
## N. Dependency declarations
REQUIRES: elementary arithmetic/set language. BRIDGE_REQUIRES: arithmetic digit rules only when a problem requires deriving them. EXPORTS: stable counting/model semantics to COMB-02/03.
## O. Lead integration notes
Keep formulas subordinate to object identity, restrictions and exact-one reasoning. Retrieve the stable provider interface downstream rather than duplicating this chapter.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact current-source PDF render QA pending
'''
files['Authoring/Microstream_Interfaces.md']='\n'.join(index)+'\n\nThis file is navigation only and does not establish schema conformance.\n'

# Frozen 31-column metadata.
cols=['item_id','source_year','source_question_number','source_paper_url','source_key_url','source_authority','key_status','question_mark_value','official_answer','primary_domain','main_topic_id','secondary_domains','mechanisms','visible_clues','hidden_invariant','first_move','prerequisites','decision_boundaries','figure_required','source_integrity_status','provenance','student_use_disposition','teacher_use_disposition','recognition_difficulty','representation_difficulty','execution_difficulty','transfer_difficulty','answer_verified_independently','classification_review_status','classification_confidence','notes']
rows=[]
def hist(item,year,q,paper,key,authority,status,marks,answer,secondary,mechanisms,clues,invariant,first,boundary):
    rows.append(dict(item_id=item,source_year=year,source_question_number=q,source_paper_url=paper,source_key_url=key,source_authority=authority,key_status=status,question_mark_value=marks,official_answer=answer,primary_domain='COMB',main_topic_id='IOQM-G9-COMB-01',secondary_domains=secondary,mechanisms=mechanisms,visible_clues=clues,hidden_invariant=invariant,first_move=first,prerequisites='elementary counting',decision_boundaries=boundary,figure_required='false',source_integrity_status='CLEAN_VALIDATED',provenance='HISTORICAL_VALIDATED_PYQ',student_use_disposition='CANONICAL_SOURCE_LINKED_PYQ',teacher_use_disposition='SOURCE_LEDGER_AND_MECHANISM_ANALYSIS',recognition_difficulty='',representation_difficulty='',execution_difficulty='',transfer_difficulty='',answer_verified_independently='true',classification_review_status='SECOND_PASS_STEM_REVIEWED',classification_confidence='HIGH',notes=''))
p25='https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/en.M1.pdf'; k25='https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/final-key-7th-September.pdf'
p24='https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf'; k24='https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf'
p23='https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf'
hist('IOQM-2025-Q05','2025','5',p25,k25,'HBCSE_OFFICIAL','FINAL_OFFICIAL','2','45','NT','restricted digit counting','3-digit abc; c=a+b','digit relation becomes bounded pair count','count admissible (a,b)','counting strings vs deriving digit arithmetic')
hist('IOQM-2025-Q15','2025','15',p25,k25,'HBCSE_OFFICIAL','FINAL_OFFICIAL','3','40','','restricted injection; inclusion-exclusion','three coupon-pairs; distinct envelopes; forbidden matches','grouped objects with forbidden envelope sets','model three pair-groups then count injectively','independent placement vs grouped restriction')
hist('IOQM-2025-Q18','2025','18',p25,k25,'HBCSE_OFFICIAL','FINAL_OFFICIAL','3','40','','multiset permutations; complement; relative order','223334444; condition right of rightmost 4','relative 3/4 subsequence controls event','separate 2 positions from 3/4 relative order','direct position cases vs complement')
hist('IOQM-2024-Q02','2024','2',p24,k24,'HBCSE_OFFICIAL','OFFICIAL_HBCSE_KEY','2','12','','permutations; parity restriction','4-digit odd; digits 1,2,3,4 once','units position restriction first','choose odd units digit then permute rest','permutation vs arithmetic parity rule')
hist('IOQM-2023-Q07','2023','7',p23,p23,'HBCSE_LINKED_MTAI','HBCSE_LINKED_MTAI_EMBEDDED_KEY','2','48','','symmetry-normalized arrangements; cube rotations','1,2 opposite; opposite faces same colour','fix rotational frame before counting visible designs','fix 1/2 axis; cyclic labels; colour opposite pairs','raw face permutations vs rotational equivalence')
hist('IOQM-2023-Q17','2023','17',p23,p23,'HBCSE_LINKED_MTAI','HBCSE_LINKED_MTAI_EMBEDDED_KEY','3','66','ALG','order statistics; subset symmetry','increasing 5-tuples from 1..99; average fourth element','increasing tuples are unordered subsets with symmetric order statistics','use reflection/order-statistic symmetry','enumerating tuples vs subset symmetry')
hist('IOQM-2023-Q20','2023','20',p23,p23,'HBCSE_LINKED_MTAI','HBCSE_LINKED_MTAI_EMBEDDED_KEY','3','43','','finite sets; cardinality/max; binomial counts','max(A)|B|=12; |A|max(B)=11','factor constraints determine size/max before subset count','solve size/max factors then choose lower elements','set enumeration vs parameter factorization')

practice_answers=['12','8','15','24','12','12','56','60','60','10','300','360','128','60','61','1260','1260','140','3600','30','9','60','1560','30','120','456','25;5','360','60','540']
practice_mech=['multiplication principle','addition principle','combination','permutation','repeated objects','position restriction; permutation','combination','repeated objects','ordered selection','combination positions','leading-zero restriction; permutation','symmetry; permutation','subset restriction','restricted injection','complement','repeated objects','position restriction; permutation','complement; combination','block complement','order symmetry','inclusion-exclusion; derangement','inclusion-exclusion','inclusion-exclusion','repeated objects; fixed last symbol','repeated objects; complement','case split; combinations','inclusion-exclusion','digit strings; parity classification','block complement; repeated objects','inclusion-exclusion']
for i,(ans,mech) in enumerate(zip(practice_answers,practice_mech),1):
    rows.append({c:'' for c in cols}); r=rows[-1]
    r.update(item_id=f'COMB01-P{i:02d}',official_answer=ans,primary_domain='COMB',main_topic_id='IOQM-G9-COMB-01',mechanisms=mech,visible_clues='authored practice item',hidden_invariant='counted-object identity and restriction model',first_move='define object; choose ordered/unordered/cases/stages',prerequisites='elementary arithmetic',decision_boundaries='direct vs complement; disjoint vs overlap; ordered vs unordered',figure_required='false',source_integrity_status='AUTHOR_CREATED',provenance='AUTHOR_CREATED',student_use_disposition='STUDENT_PRACTICE',teacher_use_disposition='TEACHER_KEYED',recognition_difficulty='F'+str(min((i-1)//5,4)),representation_difficulty='',execution_difficulty='',transfer_difficulty='',answer_verified_independently='true',classification_review_status='AUTHORED_QA',classification_confidence='HIGH',notes='')
mastery_answers=['56','28','12','30','127','60','105','600','9','30','175','90','150','60','360','36']
for i,ans in enumerate(mastery_answers,1):
    rows.append({c:'' for c in cols}); r=rows[-1]
    r.update(item_id=f'COMB01-M{i:02d}',official_answer=ans,primary_domain='COMB',main_topic_id='IOQM-G9-COMB-01',mechanisms='mixed counting decision',visible_clues='independent mastery item',hidden_invariant='model before formula',first_move='define object and identity',prerequisites='COMB-01 integrated learner path',decision_boundaries='ordered/unordered; direct/complement; overlap; repeated identity',figure_required='false',source_integrity_status='AUTHOR_CREATED',provenance='AUTHOR_CREATED',student_use_disposition='STUDENT_MASTERY_UNLABELLED',teacher_use_disposition='TEACHER_H0_CONTROL',recognition_difficulty='MIXED',representation_difficulty='',execution_difficulty='',transfer_difficulty='',answer_verified_independently='true',classification_review_status='AUTHORED_QA',classification_confidence='HIGH',notes='learner surface is unlabelled')
out=io.StringIO(); w=csv.DictWriter(out,fieldnames=cols,lineterminator='\n'); w.writeheader(); w.writerows(rows)
files['Item_Metadata.csv']=out.getvalue()

files['QA.md'] = r'''# COMB-01 - QA

Status: `STATIC_SOURCE_READY__RENDER_REVALIDATION_REQUIRED`

Static source, mathematical reconstruction, ownership, frozen metadata schema, stable downstream provider interface and seven per-microstream interfaces are authored. Current-source exact PDF custody/visual QA must pass before promotion.

Evidence-dependent classroom timing/readability, longitudinal retention, psychometrics, qualification probability and percentile/pass-mark calibration remain `NOT_RUN`.
'''

files['PDFs/README.md'] = r'''# COMB-01 PDF custody

Current-source PDF render and exact custody are pending the deterministic render gate. See `../QA.md`.
'''

files['Authoring/render_comb01_pdfs.py'] = r'''from pathlib import Path
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
PDFS=ROOT/'PDFs'; PDFS.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if Path(font).exists():
    pdfmetrics.registerFont(TTFont('DV',font)); pdfmetrics.registerFont(TTFont('DVB',bold)); BODY='DV'; BOLD='DVB'
else: BODY='Helvetica'; BOLD='Helvetica-Bold'
styles=getSampleStyleSheet()
base=ParagraphStyle('Body',parent=styles['BodyText'],fontName=BODY,fontSize=8.4,leading=10.6,spaceAfter=3)
h1=ParagraphStyle('H1',parent=base,fontName=BOLD,fontSize=15,leading=18,spaceBefore=5,spaceAfter=8)
h2=ParagraphStyle('H2',parent=base,fontName=BOLD,fontSize=11.4,leading=14,spaceBefore=7,spaceAfter=4)
h3=ParagraphStyle('H3',parent=base,fontName=BOLD,fontSize=9.5,leading=12,spaceBefore=5,spaceAfter=3)
small=ParagraphStyle('Small',parent=base,fontSize=7.5,leading=9.2)
cover=ParagraphStyle('Cover',parent=h1,fontSize=22,leading=26,alignment=TA_CENTER,spaceAfter=14)
subtitle=ParagraphStyle('Sub',parent=base,fontSize=11,leading=14,alignment=TA_CENTER)

def esc(s):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    s=s.replace('**','').replace('`','')
    return s

def flow(paths,title):
    story=[Spacer(1,55*mm),Paragraph(esc(title),cover),Paragraph('Integrated Grade-9 learner pack',subtitle),PageBreak()]
    for fi,name in enumerate(paths):
        if fi: story.append(PageBreak())
        lines=(ROOT/name).read_text().splitlines(); i=0
        while i<len(lines):
            raw=lines[i].rstrip(); s=raw.strip()
            if not s: story.append(Spacer(1,2.4*mm)); i+=1; continue
            if s.startswith('```'):
                i+=1; block=[]
                while i<len(lines) and not lines[i].strip().startswith('```'):
                    block.append(lines[i]); i+=1
                story.append(Paragraph(esc(' / '.join(x.strip() for x in block if x.strip())),small)); i+=1; continue
            if s.startswith('|'):
                block=[]
                while i<len(lines) and lines[i].strip().startswith('|'):
                    row=lines[i].strip()
                    if not re.fullmatch(r'[| :\-]+',row): block.append(' | '.join(x.strip() for x in row.strip('|').split('|')))
                    i+=1
                for row in block: story.append(Paragraph(esc(row),small))
                continue
            if s.startswith('# '): story.append(Paragraph(esc(s[2:]),h1))
            elif s.startswith('## '): story.append(Paragraph(esc(s[3:]),h2))
            elif s.startswith('### '): story.append(Paragraph(esc(s[4:]),h3))
            elif s.startswith('> '): story.append(Paragraph(esc(s[2:]),ParagraphStyle('Quote',parent=base,leftIndent=6*mm,rightIndent=6*mm,fontName=BOLD)))
            elif re.match(r'^\d+\.\s',s): story.append(Paragraph(esc(s),base))
            elif s.startswith('- '): story.append(Paragraph(esc('• '+s[2:]),base))
            else: story.append(Paragraph(esc(s),base))
            i+=1
    return story

def footer(canvas,doc,label):
    canvas.saveState(); canvas.setFont(BODY,6.4); canvas.drawString(16*mm,8*mm,label); canvas.drawRightString(A4[0]-16*mm,8*mm,f'Page {doc.page}'); canvas.restoreState()

def build(out,paths,title,label):
    doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=15*mm,bottomMargin=14*mm,title=title,author='OpenAI-assisted curriculum production',pageCompression=1,invariant=1)
    story=flow(paths,title)
    doc.build(story,onFirstPage=lambda c,d:footer(c,d,label),onLaterPages=lambda c,d:footer(c,d,label))

build(PDFS/'COMB01_Student_Pack_v1.pdf',['02_Assimilation_Book.md','03_First_Step_Reference.md','04_Recognition_and_First_Line_Lab.md','05_Practice_and_Transfer_Bank.md','06_H0_Mastery_Test.md'],'Basic Counting, Restrictions & Inclusion-Exclusion','IOQM Grade 9 | Basic Counting')
build(PDFS/'COMB01_Teacher_Key_v1.pdf',['Teacher_Diagnostic_Key.md'],'Basic Counting - Teacher Diagnostic Key','IOQM Grade 9 | Teacher Diagnostic Key')
'''

for rel,content in files.items():
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content)

print('wrote',len(files),'package files')
