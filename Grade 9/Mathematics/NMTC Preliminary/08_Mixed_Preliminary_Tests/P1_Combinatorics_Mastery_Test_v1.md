# P1 Combinatorics — Unlabelled Mixed Mastery Test v1

All questions are author-created. No method labels are shown in the question section.

Recommended internal timing: 35 minutes before classroom calibration.

## Questions

### Q1
From 9 students, form a 4-person team and choose one team member as leader. How many outcomes?

### Q2
How many 4-digit odd numbers can be formed from digits `0,1,2,3,4,5` without repetition?

### Q3
How many integers from 1 to 300 are divisible by 4 or 9?

### Q4
Among any 13 integers, prove that two have the same remainder upon division by 12.

### Q5
Twenty-nine objects are placed into 7 boxes. Prove that some box contains at least 5 objects.

### Q6
Find the sum of products of all non-empty subsets of `{1/2,1/4,1/6}`.

### Q7
Find the coefficient of `x^10` in

`(1+x+x^2+x^3+x^4)(1+x+x^2+...+x^8)`.

### Q8
How many 4-element subsets of `{1,2,3,4,5,6,7,8}` have an even sum?

### Q9
How many arrangements of the letters A,B,C,D,E,F have A and B not adjacent?

### Q10
A token moves on positions 0,1,2,3,4. Each move changes the position by `+1` or `-1` without leaving the range. Starting at 0, how many 6-move walks end at 2?

### Q11
How many integers from 1 to 200 are divisible by at least one of 2, 3, 5?

### Q12
A reproduced problem says: “How many two-digit numbers have two different odd digits?” An answer key says 12. What is the mathematically defensible response?

---

# Solutions

## Q1
Choose team then leader:

`C(9,4)*4 = 126*4 = 504`.

**Diagnostic tags:** `ORDER_IGNORED`, `ROLE_NOT_COUNTED`.

## Q2
Units must be odd: 1,3,5 -> 3 choices.

Thousands must be nonzero and different from units: 4 choices among remaining digits.

Hundreds: 4 choices.

Tens: 3 choices.

Total `3*4*4*3=144`.

**Tag:** `LEADING_ZERO`, `CONTROL_POSITION_MISSED`.

## Q3
Multiples of 4: 75.

Multiples of 9: 33.

Both -> lcm 36: 8.

Union `75+33-8=100`.

**Tag:** `OVERLAP_DOUBLE_COUNT`.

## Q4
Remainder classes modulo 12 are 12 boxes. Thirteen integers are pigeons. Two share a box.

**Tag:** `PIGEON_BOX_UNNAMED`.

## Q5
If each box held at most 4, total would be at most `7*4=28`, contradicting 29. Hence some box has at least 5.

**Tag:** `STRONG_PIGEON_BOUND`.

## Q6
`(1+1/2)(1+1/4)(1+1/6)-1`

`=(3/2)(5/4)(7/6)-1=105/48-1=57/48=19/16`.

**Tag:** `SUBSET_PRODUCT_NOT_RECOGNIZED`.

## Q7
Count pairs `i+j=10` with `0<=i<=4`, `0<=j<=8`.

Need `2<=i<=4`, so 3 pairs. Coefficient `3`.

**Tag:** `EXPANSION_BRUTE_FORCE`, `BOUND_MISSED`.

## Q8
There are four odds and four evens. Even sum from 4 selected numbers requires 0, 2 or 4 odds.

`C(4,0)C(4,4)+C(4,2)C(4,2)+C(4,4)C(4,0)`

`=1+36+1=38`.

**Tag:** `CASE_PARITY_WRONG`.

## Q9
All arrangements: `6!=720`.

Adjacent A,B: treat as block -> `5!*2=240`.

Not adjacent: `720-240=480`.

**Tag:** `COMPLEMENT_NOT_USED`, `BLOCK_FACTOR_TWO_MISSED`.

## Q10
State table:

`t0 [1,0,0,0,0]`
`t1 [0,1,0,0,0]`
`t2 [1,0,1,0,0]`
`t3 [0,2,0,1,0]`
`t4 [2,0,3,0,1]`
`t5 [0,5,0,4,0]`
`t6 [5,0,9,0,4]`

Answer `9`.

**Tag:** `PATH_LISTING`, `BOUNDARY_TRANSITION_ERROR`.

## Q11
Singles: 100, 66, 40.

Pair intersections:
- 2&3 -> 6: 33;
- 2&5 -> 10: 20;
- 3&5 -> 15: 13.

Triple -> 30: 6.

Total `100+66+40-33-20-13+6=146`.

**Tag:** `IE_SIGN_ERROR`, `LCM_INTERSECTION_ERROR`.

## Q12
Under the printed wording, odd digits are `{1,3,5,7,9}`. Tens digit: 5 choices. Units digit: 4 different choices. Count = 20.

Because this disagrees with the supplied key, retain both pieces of evidence and mark `SOURCE_KEY_CONFLICT`. Do not silently remove digit 9 or alter the wording to make 12.

**Tag:** `KEY_FORCING`, `SOURCE_INTEGRITY_FAILURE`.

---

# Mastery threshold

Internal pre-publication target:

- at least 10/12 correct;
- Q4 or Q5 must demonstrate an explicit pigeon/box argument;
- Q11 must use correct inclusion–exclusion signs;
- Q12 must preserve source conflict rather than force the key;
- no more than one ordered/unordered classification error.
