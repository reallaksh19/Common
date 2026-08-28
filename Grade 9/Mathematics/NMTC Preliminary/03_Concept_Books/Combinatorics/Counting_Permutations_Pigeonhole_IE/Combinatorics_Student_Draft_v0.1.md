# Counting, Permutations, Pigeonhole & Inclusion–Exclusion
## NMTC Bhaskara Preliminary — Student Draft v0.1

> **Main question:** What exactly am I counting?

Use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

and while solving:

`RECOGNIZE -> DEFINE OBJECT -> COUNT -> CORRECT OVERLAP -> CHECK -> TRANSFER`

---

# 0. Diagnostic

Try without notes.

1. How many two-letter strings can be made from A, B, C if repetition is allowed?
2. How many if repetition is not allowed?
3. How many 2-person teams can be chosen from 5 people?
4. How many ways can a captain and vice-captain be selected from 5 people?
5. How many 3-digit numbers can be formed from 1,2,3,4 with no repeated digit?
6. Why is `012` not a three-digit number?
7. If 13 students are placed into 12 birth-month boxes, what is forced?
8. If 20 students play cricket, 14 play football and 8 play both, how many play at least one?

### Answers

1. `3*3=9`.
2. `3*2=6`.
3. `C(5,2)=10`.
4. `5*4=20`.
5. `4*3*2=24`.
6. Leading zero shortens the numeral.
7. At least two share a birth month.
8. `20+14-8=26`.

---

# 1. Define one outcome before counting

## SEE

From five students A, B, C, D, E:

- choose two for a quiz team;
- choose a captain and vice-captain.

The same five people appear, but the outcomes are different.

## REALIZE

For a team, `{A,B}` and `{B,A}` are the same outcome.

For captain/vice-captain, `(A,B)` and `(B,A)` are different.

## UNDERSTAND

Before every counting question, complete this sentence:

> One outcome is a ________.

Examples:

- unordered subset;
- ordered pair;
- digit string;
- integer satisfying restrictions;
- path;
- geometric configuration;
- choice of one term from each factor.

## ADOPT

Classify only; do not count.

A. Select 3 books from 10.

B. Award gold, silver, bronze among 10 students.

C. Form a four-digit PIN.

D. Choose an exponent from each of two generating factors whose sum is 20.

### Check

A unordered subset; B ordered assignment; C ordered string; D ordered exponent pair.

---

# 2. Multiplication and addition principles

## SEE — multiplication

Three shirts and four trousers.

For every shirt, four trousers are possible.

Total outfits:

`3*4=12`.

## REALIZE

Sequential choices multiply when each complete outcome requires one choice from each stage.

## SEE — addition

Suppose a code is either:

- one of 7 red codes, or
- one of 5 blue codes.

If the two classes cannot overlap, total = `7+5=12`.

## REALIZE

Disjoint alternatives add.

## Wrong-method contrast

“Choose a main course and a drink” -> multiply.

“Choose either a main course or a dessert” -> add, if the categories are disjoint.

---

# 3. Permutations — why the falling product appears

Choose 3 winners from 8 students: first, second, third.

First place: 8 choices.

Second place: 7 choices.

Third place: 6 choices.

Total:

`8*7*6`.

This is:

`8P3 = 8!/(8-3)!`.

The formula is only compressed multiplication.

## First-move question

Does swapping two selected people create a different outcome?

If yes, order matters.

---

# 4. Combinations — why divide by `r!`

Choose 3 students from 8 for one team.

If we first count ordered selections, every team appears:

`3! = 6`

times—once under every internal ordering.

So:

`8C3 = 8P3/3!`.

Thus:

`nCr = n!/[r!(n-r)!]`.

## Contrast

Select 3 students for a team -> combination.

Select president, secretary, treasurer -> permutation.

---

# 5. Restricted digit counting

## SEE

How many 3-digit even numbers can be formed from digits `0,1,2,3,4` without repetition?

Do not begin with `5P3`.

The last digit controls evenness.

## REALIZE

A restriction attached to one position should often be handled first.

## UNDERSTAND

Case 1: last digit 0.

Hundreds: 4 choices (`1,2,3,4`).

Tens: 3 remaining choices.

Count = 12.

Case 2: last digit 2 or 4.

Choose last digit: 2 ways.

Hundreds cannot be 0 and cannot equal last digit: 3 choices.

Tens: 3 remaining choices.

Count = `2*3*3=18`.

Total = `30`.

## CHECK

Cases are disjoint because the last digit differs.

Together they cover all even last digits.

## PYQ CONNECTION

`NMTC-BH-P-2025-Q21` uses digit positions plus divisibility by 9. The important lesson is to encode the digit condition before counting, including the fact that two different digits can share the same residue modulo 9.

---

# 6. Casework must be disjoint and exhaustive

Good casework answers two questions:

1. Can one outcome appear in two cases?
2. Is every valid outcome included somewhere?

### Example

Count positive integer solutions to `x+y=10` with `x,y` odd.

Instead of listing randomly, write:

`x=1,3,5,7,9`.

Then `y=9,7,5,3,1`.

Five ordered solutions.

### Geometry connection

`NMTC-BH-P-2019-Q09` classifies vertex triples by geometric type before counting. The lesson is not the particular box figure; it is **classification first, counting second**.

---

# 7. Subsets hidden inside a product

## SEE

Expand:

`(1+a)(1+b)(1+c)`.

To create one term, we choose from each factor either:

- `1`, meaning “do not include this element”, or
- the letter, meaning “include this element”.

So each expanded term corresponds to a subset of `{a,b,c}`.

Expansion:

`1+a+b+c+ab+ac+bc+abc`.

## REALIZE

Product expansion is a subset generator.

## UNDERSTAND

For numbers `a1,...,an`:

`product(1+a_i)`

contains the product belonging to every subset.

The empty subset contributes `1`.

Therefore sum of products over all **non-empty** subsets is:

`product(1+a_i)-1`.

## PYQ CONNECTION

`NMTC-BH-P-2019-Q07` is a clean Preliminary anchor for this mechanism.

## ADOPT

Find the sum of all non-empty subset products of `{1,2,3}`.

### Check

`(1+1)(1+2)(1+3)-1=2*3*4-1=23`.

Directly: `1+2+3+2+3+6+6=23`.

---

# 8. Coefficient as count

## SEE

Consider:

`(1+x+x^2+...+x^5)(1+x+x^2+...+x^7)`.

What is the coefficient of `x^6`?

## REALIZE

Choose `x^i` from the first factor and `x^j` from the second.

Their product is `x^(i+j)`.

So the coefficient of `x^6` counts pairs:

`i+j=6`, with `0<=i<=5`, `0<=j<=7`.

Possible `i=0,1,2,3,4,5`: six pairs.

Coefficient = 6.

## PYQ CONNECTION

`NMTC-BH-P-2019-Q30` uses exactly this representation at a higher target exponent.

## ADOPT

Coefficient of `x^8` in

`(1+x+...+x^4)(1+x+...+x^7)`?

### Check

`i+j=8`, `0<=i<=4`, `0<=j<=7`.

`i=1,2,3,4`: four pairs.

Answer 4.

---

# 9. Path/state counting

Suppose a token is at positions `0,1,2,3` on a line. Each move changes position by `+1` or `-1`, but the token cannot leave `0..3`.

How many 4-move paths start at 0 and end at 2?

Do not list every L/R word blindly.

Define:

`C_t(p) = number of ways to be at position p after t moves`.

Start:

`C_0(0)=1` and others 0.

Update using allowed predecessor states.

This is counting by state compression.

## Historical boundary

`NMTC-BH-P-2019-Q23` is a real exact-move path-count signal, but the original grid is figure-gated. We teach the mechanism with text-complete author-created states instead of inventing that historical grid.

---

# 10. Pigeonhole principle

## SEE

13 students, 12 months.

## REALIZE

If every month had at most one student, there could be at most 12 students.

But there are 13.

Therefore some month has at least two.

## UNDERSTAND

If `N` objects are placed into `k` boxes, some box contains at least:

`ceil(N/k)`

objects.

## The real skill: choose the boxes

Examples:

- same remainder mod 5 -> five residue boxes;
- same last digit -> ten boxes;
- same birth month -> twelve boxes;
- numbers in intervals -> interval boxes.

## Example

Choose 6 integers. Show two have the same remainder modulo 5.

Pigeons: 6 integers.

Boxes: residues `0,1,2,3,4`.

Five boxes, six pigeons -> two share a box.

## ADOPT

Among 11 integers, prove two have the same last digit.

Answer: 10 last-digit boxes.

---

# 11. Stronger pigeonhole

If 25 students enter 6 groups, some group has at least:

`ceil(25/6)=5`

students.

Why? If every group had at most 4, total would be at most 24.

This “maximum if no box reaches target” argument is often the cleanest proof.

---

# 12. Inclusion–exclusion

## SEE

30 students play chess.

25 play badminton.

12 play both.

If we calculate `30+25`, the 12 who play both are counted twice.

## REALIZE

Subtract one copy of the overlap.

## UNDERSTAND

`|A union B| = |A|+|B|-|A intersection B|`.

### Three sets

`|A union B union C|`

`= singles`

`- pairwise overlaps`

`+ triple overlap`.

The triple intersection was added three times, subtracted three times, so it must be added once.

## Number-theory example

How many integers from 1 to 100 are divisible by 2 or 5?

Divisible by 2: 50.

Divisible by 5: 20.

Divisible by both -> divisible by 10: 10.

Total:

`50+20-10=60`.

---

# 13. Complement counting

“How many contain at least one zero?” can be easier as:

`all - none`.

### Example

How many 4-digit PINs from 0000 to 9999 contain at least one 7?

All: `10^4`.

No 7: `9^4`.

Answer:

`10000-6561=3439`.

## REALIZE

“At least one” is a strong signal to test the complement.

---

# 14. A source-integrity lesson

The reproduced 2023 Q25 says two-digit numbers with different odd digits. Under the printed wording there are five odd digits, and ordered different-digit choices give:

`5*4=20`.

The supplied key/solution gives 12 after restricting to four odd digits without justification.

Correct curriculum behavior:

`SOURCE_CONFLICT`

not “change the mathematics until the key works.”

---

# 15. First-move laboratory

Write only the first move.

1. Choose 4 from 10, order irrelevant.
2. Arrange 5 different books on a shelf.
3. Count 5-digit numbers divisible by 5 from a specified digit set.
4. Count objects satisfying property A or B.
5. Prove two of 8 integers have same remainder mod 7.
6. Coefficient of `x^20` in a product of finite sums.
7. Sum of all non-empty subset products.
8. Count exact-length paths on a small graph.

### Check

1 combination; 2 permutation; 3 split by last digit; 4 inclusion–exclusion if overlap; 5 pigeonhole on residues; 6 exponent tuples; 7 product expansion; 8 define states/recurrence.

---

# 16. Self-test

1. How many 4-letter strings from A,B,C,D,E with no repetition?
2. How many 3-person committees from 9 students?
3. How many ways to choose president and secretary from 9?
4. How many integers from 1 to 60 are divisible by 2 or 3?
5. Show among any 9 integers, two have same remainder mod 8.
6. Coefficient of `x^7` in `(1+x+...+x^3)(1+x+...+x^6)`.
7. Sum of all subset products of `{2,3,4}`, including empty subset.
8. How many 3-digit even numbers can be formed from 0,1,2,3 without repetition?

### Answers

1. `5*4*3*2=120`.
2. `9C3=84`.
3. `9P2=72`.
4. `30+20-10=40`.
5. eight residue boxes.
6. pairs `i+j=7`, `0<=i<=3`, `0<=j<=6`: `i=1,2,3`, so 3.
7. `(1+2)(1+3)(1+4)=60`.
8. last digit 0: `3*2=6`; last digit 2: hundreds `2` choices (`1,3`), tens `2` choices -> 4; total 10.

---

# Mastery checklist

I can:

- define one outcome;
- say whether order matters;
- choose addition vs multiplication principle;
- use `nPr/nCr` only after defining structure;
- handle leading zero/repetition/parity/divisibility restrictions;
- make disjoint exhaustive cases;
- use complement counting;
- interpret product expansion as subset choices;
- interpret coefficients as counts;
- define states for paths;
- identify pigeons and boxes;
- correct overlap by inclusion–exclusion;
- reject a conflicting source/key rather than force agreement.
