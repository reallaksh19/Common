# P1 Combinatorics — Reviewed Transfer Bank v1

All items are `AUTHOR_CREATED_TRANSFER`. They are not historical NMTC questions.

## T01 — Order or selection
From 8 students, choose a 3-person team and then choose one of those 3 as spokesperson. How many outcomes?

**First move:** choose team, then spokesperson.

**Solution:** `C(8,3)*3 = 56*3 = 168`.

---

## T02 — Restricted roles
From 7 students, choose president, secretary and a 2-person committee from the remaining students. Committee members have equal roles.

**Solution:** president/secretary `7*6`; committee `C(5,2)=10`; total `420`.

---

## T03 — Leading zero + parity
How many 4-digit even numbers can be formed from `0,1,2,3,4,5` without repetition?

**Solution:**
- units 0: thousands 5, hundreds 4, tens 3 -> 60;
- units 2 or 4: 2 choices; thousands 4 nonzero choices; then 4,3 -> `2*4*4*3=96`.
Total `156`.

---

## T04 — Digit-sum congruence
How many ordered pairs of digits `(a,b)` with `a in {1,...,9}` and `b in {0,...,9}` satisfy `a+b+4` divisible by 9?

**Solution:** need `a+b≡5 mod9`. For each `a=1..9`, count digit `b` in 0..9 matching residue `5-a`. Residue 0 has digits 0 and 9; all other residues one digit. Residue 0 occurs when `a=5`, so total `9+1=10`.

---

## T05 — Complement
How many 5-digit PINs using digits `0..9` contain at least one digit 3?

**Solution:** `10^5-9^5=100000-59049=40951`.

---

## T06 — Inclusion–exclusion
How many integers from 1 to 200 are divisible by 4 or 6?

**Solution:** `floor(200/4)+floor(200/6)-floor(200/12)=50+33-16=67`.

---

## T07 — Three-set inclusion–exclusion
How many integers from 1 to 120 are divisible by 2, 3 or 5?

**Solution:** singles `60+40+24=124`; subtract pairwise `20+12+8=40`; add triple `4`; total `88`.

---

## T08 — Pigeonhole residue
Show that among any 9 integers, two have the same remainder when divided by 8.

**Solution:** 8 residue classes, 9 integers.

---

## T09 — Strong pigeonhole
Thirty-one students are assigned to 6 project groups. Prove some group has at least 6 students.

**Solution:** if every group had at most 5, total at most 30. Contradiction.

---

## T10 — Pigeonhole interval design
Choose 11 distinct integers from `{1,2,...,20}`. Prove two chosen integers are consecutive.

**Solution:** boxes `{1,2},{3,4},...,{19,20}`. Ten boxes, 11 chosen integers; two lie in same pair and hence are consecutive.

---

## T11 — Subset product
Find the sum of products of all non-empty subsets of `{1/2,1/3,1/4}`.

**Solution:** `(1+1/2)(1+1/3)(1+1/4)-1=(3/2)(4/3)(5/4)-1=5/2-1=3/2`.

---

## T12 — Coefficient as pair count
Find the coefficient of `x^12` in `(1+x+...+x^7)(1+x+...+x^9)`.

**Solution:** count `i+j=12`, `0<=i<=7`, `0<=j<=9`. Then `3<=i<=7`, giving 5 pairs.

---

## T13 — Coefficient as triple count
Find coefficient of `x^5` in `(1+x+x^2)^3`.

**Solution:** count ordered triples `(a,b,c)` in `{0,1,2}` with sum 5. Only permutations of `(2,2,1)`: 3. Coefficient `3`.

---

## T14 — Disjoint case classification
How many 3-element subsets of `{1,2,3,4,5,6}` have even sum?

**First move:** classify by number of odd elements.

**Solution:** odds=3, evens=3. Even sum occurs with 0 odds or 2 odds. Counts: `C(3,3)=1` all evens, plus `C(3,2)C(3,1)=9`; total `10`.

---

## T15 — State recurrence
A token moves on positions 0,1,2,3. Each move changes position by ±1 and cannot leave the interval. Starting at 0, how many 4-move walks end at 2?

**Solution table:**
`t0: [1,0,0,0]`
`t1: [0,1,0,0]`
`t2: [1,0,1,0]`
`t3: [0,2,0,1]`
`t4: [2,0,3,0]`.
Answer `3`.

---

## T16 — Adjacency via complement/collapse
How many arrangements of A,B,C,D,E have A and B adjacent?

**Solution:** treat AB/BA as one block: `4!*2=48`.

---

## T17 — Restricted selection
A committee of 4 is chosen from 6 boys and 5 girls. How many committees contain at least 2 girls?

**Solution:** girls 2,3,4:
`C(5,2)C(6,2)+C(5,3)C(6,1)+C(5,4)=150+60+5=215`.

---

## T18 — Source-integrity contrast
A printed problem asks: “How many two-digit numbers have two different odd digits?” A supplied key says 12.

**Independent count:** odd digits `{1,3,5,7,9}`. Tens 5 choices, units 4 different choices -> `20`.

**Disposition:** `SOURCE_KEY_CONFLICT`; do not change the digit set merely to force 12.

---

# Review checklist

Second-pass checks performed:

- ordered/unordered distinctions;
- leading-zero cases;
- inclusion–exclusion LCM intersections;
- pigeonhole box coverage;
- coefficient bounds;
- state recurrence boundary handling;
- complement/case disjointness;
- source-conflict behavior.
