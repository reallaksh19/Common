# Counting, P&C, Pigeonhole & Inclusion–Exclusion — Assimilation Book
## Issue #50 · Wave 2 · NMTC Bhaskara Preliminary / Grade IX–X

### Core belief
A counting answer is not trustworthy until you can say:
1. what one outcome is;
2. when two descriptions are the same outcome;
3. why every valid outcome appears;
4. why no valid outcome appears twice.

Use:
`RECONNECT → DISCOVER → MAKE SENSE → TRY → DIAGNOSE → FADE → ADOPT → TRANSFER`

Performance:
`DEFINE OBJECT → ORDER? → REPETITION? → RESTRICTIONS → BUILD SAMPLE SPACE → DIRECT/COMPLEMENT → OVERLAP? → EXACT COUNT/GUARANTEE → REPRESENTATION → COUNT → CHECK`

---

# 0. RECONNECT — “What exactly is being counted?”

Do not calculate first. Write the **object type**.

1. Select 3 students from 9 for one committee.
2. Select president, secretary and treasurer from 9.
3. Form a 4-digit PIN from digits 0–9.
4. Form a 4-digit positive integer.
5. Count integers from 1 to 100 divisible by 2 or 5.
6. Prove that among 9 integers two have the same remainder modulo 8.
7. Find a coefficient in a product of finite power sums.
8. Count exact-length walks on a line graph.

Expected object types:
unordered subset; ordered role assignment; ordered string; ordered numeral subject to leading-digit legality; union of sets; objects assigned to residue boxes; bounded exponent tuple; state/path.

A wrong object type is an earlier error than wrong arithmetic.

---

# 1. DISCOVER — same people, different sample spaces

From five students:
- choose a 2-person team;
- choose captain and vice-captain.

For the team `{A,B}={B,A}`.
For roles `(A,B)≠(B,A)`.

## Contrast 1 — ordered vs unordered
The question is not “does it say choose or arrange?”
The question is:

> If I swap selected objects, did the outcome change?

### TRY — H0
From 6 students:
A. choose 2 for a team;
B. choose captain and vice-captain.

Write only the two first counting structures.

After attempt:
- H1: use the swap test.
- H2: A is an unordered subset; B is an ordered pair.
- H3: A `C(6,2)`; B `6·5`.

---

# 2. Why permutation and combination formulas have their shape

Choose 3 distinct roles from 8:
`8·7·6`.

This falling product is what `8P3` compresses.

Now choose one 3-person team from 8.
If we count ordered triples first, each team appears `3!` times.
Therefore divide the description-level overcount:
`8C3 = (8·7·6)/3!`.

## Reconstruction rule
Do not memorize “permutation has no r! denominator” as the reason.
The reason is **outcome identity**.

### TRY
Explain why a 4-person committee from 10 is not `10P4`.

---

# 3. Sequential stages vs alternative cases

A full outfit needs:
- one of 3 shirts;
- one of 4 trousers.

Each complete outcome requires both choices:
`3·4=12`.

If a code is either one of 7 red codes or one of 5 blue codes and the classes do not overlap:
`7+5=12`.

## Contrast 2 — multiply vs add
- complete outcome uses **all stages** → multiply;
- complete outcome belongs to **one disjoint case** → add.

### WHY NOT?
“3 mains and 5 drinks gives 8 meals” fails because a meal needs one of each.

---

# 4. Casework is a partition, not a list

Good casework must be:
- disjoint;
- exhaustive.

For every case table ask:
1. Can one object appear in two rows?
2. Is every legal object in some row?

## Contrast 3 — disjoint add vs overlapping add
If cases overlap, plain addition double-counts.

### TRY
Count 3-digit even numbers from `0,1,2,3,4` without repetition.

Efficient partition:
- units digit 0;
- units digit 2 or 4.

Case 0: `4·3=12`.
Case 2/4: `2·3·3=18`.
Total `30`.

Cases are disjoint because the final digit differs.

---

# 5. Restriction first — especially leading zero

A 4-digit PIN and a 4-digit integer are different sample spaces.

- PIN `0123` may be legal.
- integer `0123` is actually 123 and is not 4-digit.

## Contrast 4 — code vs integer
Do not carry a no-leading-zero restriction into a code unless stated.
Do not allow leading zero in a fixed-length integer.

### TRY
How many 3-digit numbers can be formed from `0,1,2,3` without repetition?

First digit: 3 choices.
Second: 3.
Third: 2.
Total `18`.

Independent check: list/brute force gives 18.

---

# 6. Direct count or complement?

“At least one” often has many direct cases.

Example: 4-digit PINs containing at least one `7`.

All PINs: `10^4`.
No `7`: `9^4`.
Desired:
`10^4-9^4=3439`.

## Contrast 5 — direct vs complement
Complement is not automatically better. Use it when the opposite event is structurally simpler.

### TRY — first move only
Count 6-letter strings over `{A,B,C}` containing at least one `A`.

Write only the complement setup.

---

# 7. Repeated objects — overcount can come from descriptions

Arrange the letters in `LEVEL`.

There are 5 positions, but the two `L`s are indistinguishable and the two `E`s are indistinguishable.

If all five copies were labeled, `5!` descriptions arise.
Swapping the two L labels changes no word: divide by `2!`.
Same for E:
`5!/(2!2!)=30`.

## Contrast 6 — allowed repetition vs indistinguishable copies
“Repetition allowed” in a string-building problem is not the same concept as repeated identical objects already present.

---

# 8. Inclusion–exclusion — exact union count

Count integers `1..100` divisible by 2 or 5.

Let:
- `A`: divisible by 2 → 50;
- `B`: divisible by 5 → 20;
- `A∩B`: divisible by 10 → 10.

Plain addition counts the intersection twice:
`50+20-10=60`.

For three sets:
`+ singles - pair intersections + triple intersection`.

## Contrast 7 — disjoint addition vs IE
If overlap can occur, the intersection must be audited.

### TRY
How many integers `1..60` are divisible by 2 or 3?

Result after work:
`30+20-10=40`.

---

# 9. Pigeonhole — a guarantee, not an exact count

Among 9 integers, prove two have the same remainder modulo 8.

Pigeons: the 9 integers.
Boxes: residue classes `0,1,...,7`.

Eight boxes, nine pigeons → a collision is forced.

## Strong form
25 students enter 6 groups.
If every group had at most 4 students, there would be at most 24.
Therefore some group has at least 5.

## Contrast 8 — exact count vs guarantee
“How many are divisible by 2 or 3?” → exact counting.
“Prove two share a residue” → occupancy guarantee.

### WHY NOT?
Saying “by pigeonhole” without naming valid boxes is incomplete reasoning.

---

# 10. Inclusion–exclusion and pigeonhole can use the same residues differently

Residues modulo 5 can be:
- sets whose union/intersections are counted;
- boxes used to force a repeated residue.

The representation depends on the target, not the vocabulary.

---

# 11. Subset products hidden in a product

Expand:
`(1+a)(1+b)(1+c)`.

From each factor choose:
- `1`: exclude the element;
- the variable: include the element.

So expanded terms correspond to subsets.

For values `a1,...,an`,
`∏(1+a_i)` is the sum of all subset products, including the empty subset product `1`.

Therefore non-empty subset-product sum is:
`∏(1+a_i)-1`.

Clean mechanism anchor: `NMTC-BH-P-2019-Q07`.

### TRY
Sum non-empty subset products of `{1,2,3}`:
`(2)(3)(4)-1=23`.

Second method: direct enumeration also gives 23.

---

# 12. Coefficient as a bounded count

Coefficient of `x^8` in:
`(1+x+...+x^4)(1+x+...+x^7)`.

Choose `x^i` from first factor and `x^j` from second.
Need:
`i+j=8`,
`0≤i≤4`, `0≤j≤7`.

Legal pairs:
`(1,7),(2,6),(3,5),(4,4)`.

Coefficient = 4.

## Contrast 9 — algebra expansion vs exponent-tuple count
The bounds matter. Unrestricted `i+j=8` would overcount illegal exponent choices.

Clean mechanism anchor: `NMTC-BH-P-2019-Q30`.

---

# 13. State counting — compress histories

Positions `0,1,2,3`.
A move changes position by ±1 but may not leave the range.
How many 4-move walks start at 0 and end at 2?

Define:
`C_t(p) = number of legal ways to be at position p after t moves`.

Start:
`C_0(0)=1`.

Update from allowed neighbors.

Table:
- t0: `[1,0,0,0]`
- t1: `[0,1,0,0]`
- t2: `[1,0,1,0]`
- t3: `[0,2,0,1]`
- t4: `[2,0,3,0]`

Answer: 3.

## Contrast 10 — raw path strings vs states
`2^4` counts illegal boundary moves and ignores state restrictions.

Historical state/path signal `NMTC-BH-P-2019-Q23` remains figure-gated; this is an author-created text-complete model.

---

# 14. High-ceiling representation — uniqueness before counting

Suppose integers are represented as:
`a0·1 + a1·3 + a2·9`
with `a_i∈{-1,0,1}`.

Before saying there are `3^3=27` represented integers, ask whether two different digit triples could produce the same value.

For balanced ternary powers `1,3,9`, uniqueness follows because the largest differing place cannot be cancelled by all smaller places:
`9 > 2(1+3)`.

Only after this check is `3^3=27` a one-to-one representation count.

## Contrast 11 — digit choices vs object count
Counting encodings is valid only if encoding → object is one-to-one, or duplicate encodings are corrected.

`NMTC-BH-P-2019-Q28` supports this as high-ceiling evidence, not entry-level work.

---

# 15. Overcount / double-count laboratory

For each proposed count, identify the first defect.

1. 3-person team from 8: `8·7·6`.
2. captain and vice-captain from 8: `C(8,2)`.
3. `A or B` where overlap exists: `|A|+|B|`.
4. 4-digit integers: `10^4`.
5. 3-digit even numbers without repetition: `9·9·5`.
6. coefficient target: count all nonnegative solutions and ignore factor exponent caps.
7. pigeonhole: “there are lots of integers, so repetition happens.”
8. two overlapping casework rows counted separately.
9. subset-product sum over non-empty subsets but retain the empty product `1`.
10. state walk: use `2^m` despite illegal boundary transitions.

Repair each before doing more arithmetic.

---

# 16. Source-integrity laboratory

Current source statuses:

- `2019-Q07` subset product — clean scored anchor.
- `2019-Q09` configuration classification — clean mechanism anchor.
- `2019-Q12` configuration count — figure-gated.
- `2019-Q23` path/state — figure-gated.
- `2019-Q28` balanced representation — high-ceiling bridge.
- `2019-Q30` coefficient-as-count — clean scored anchor.
- `2025-Q21` digit restriction/divisibility — clean scored anchor.
- `2023-Q25` odd-digit count — source conflict.

## Conflict falsifier
Printed 2023-Q25 wording permits five odd digits and different ordered digits:
`5·4=20`.

A supplied solution/key uses 12 after an unexplained restriction.
Correct action:
`SOURCE_CONFLICT_EVIDENCE`,
not alteration of the printed sample space.

---

# 17. FADE — same idea, less support

## Ordered/unordered family
H3: Team of 2 from 5: `C(5,2)`.
H2: Ask whether swapping creates a new outcome.
H1: Identify whether roles exist.
H0: “From 7 students choose one captain and two other committee members.” Write a correct counting expression.

H0 answer:
`7·C(6,2)=105`.

## Complement family
H3: `4-digit PIN with at least one 7 = 10^4-9^4`.
H2: Count all minus none.
H1: What is the opposite of “at least one A”?
H0: Number of 5-letter strings over `{A,B,C,D}` containing at least one `A`.

H0 answer:
`4^5-3^5=781`.

## Pigeonhole family
H3: 13 students, 12 months → at least two share month.
H2: compare objects to boxes.
H1: invent residue boxes.
H0: among 11 integers prove two have same last digit.

H0 first proof line:
10 last-digit boxes for 11 integers.

---

# 18. ADOPT — mixed first-move-only

Write only the counted object and first useful structure.

1. Choose 4 from 10, no roles.
2. Award gold, silver, bronze among 10.
3. 5-digit even integer with distinct digits from a given set.
4. At least one repeated category in a code.
5. Count objects satisfying A or B with possible overlap.
6. Prove a collision among 8 residues modulo 7.
7. Sum of non-empty subset products.
8. Coefficient of `x^k` in three finite power sums.
9. Exact-length walk on a line with forbidden boundary moves.
10. Arrange a multiset with repeated identical letters.
11. One captain plus an unordered 3-person committee.
12. Historical path question with missing essential diagram.
13. Source wording gives 20 while key gives 12 without justified restriction.
14. A signed-power representation problem.

Teacher key is separate.

---

# 19. TRANSFER — unlabelled mixed problems

T1. From 8 students choose a president and a 3-person advisory committee not including the president.

T2. How many 4-digit even integers can be formed from digits `0,1,2,3,4,5` without repetition?

T3. How many 5-letter strings over `{A,B,C}` contain at least one `A`?

T4. Count integers `1..120` divisible by 2 or 3.

T5. Count integers `1..120` divisible by 2, 3 or 5.

T6. Among any 13 integers, prove two have the same remainder modulo 12.

T7. If 41 objects are put into 8 boxes, what occupancy is guaranteed in some box?

T8. Sum all non-empty subset products of `{2,3,4}`.

T9. Find coefficient of `x^7` in `(1+x+x^2+x^3)(1+x+...+x^6)`.

T10. Find coefficient of `x^6` in `(1+x+x^2)(1+x+x^2+x^3)(1+x+x^2+x^3+x^4)`.

T11. How many distinct arrangements of `BANANA`?

T12. From 9 students select a captain, then a 2-person team from the remaining students.

T13. How many 4-digit integers can be formed from `0,1,2,3,4` without repetition?

T14. How many 4-digit PINs over 0–9 contain no 0?

T15. How many 4-digit PINs contain at least one 0?

T16. On positions `0,1,2,3`, how many 6-move walks start at 0 and end at 2, using ±1 legal moves only?

T17. Using digits `a0,a1∈{-1,0,1}`, how many distinct values can `a0+3a1` represent? Justify uniqueness.

T18. Count 3-element subsets of `{1,2,...,10}`.

T19. Count ordered triples of distinct elements from `{1,2,...,10}`.

T20. A historical problem's essential grid is missing, but a prose solution says there are 18 paths. State the correct publication action.

---

# 20. Adoption standard

You have adopted this topic when you can:
- define the object before formulas;
- distinguish ordered from unordered;
- separate repetition from description-level overcount;
- choose add/multiply/casework;
- make cases disjoint and exhaustive;
- handle leading zero and controlling digit restrictions;
- choose complement when structurally cheaper;
- correct overlap with IE;
- distinguish exact count from pigeonhole guarantee;
- reinterpret subset products and coefficients;
- compress paths into states;
- establish uniqueness before high-ceiling representation counting;
- preserve figure/source conflicts without repair.
