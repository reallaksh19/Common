# P0 Number Theory — Modular / Divisibility / Digit Mastery Test v1

All questions are `AUTHOR_CREATED_TRANSFER`, not NMTC PYQs.

Before solving, write a first-move code:

`MC / LM / GD / CR / PV / D9 / IV / DS / CP / PR / OR / QC`.

Suggested internal window: 45 minutes. Not an official NMTC timing claim.

---

## Student paper

### Q1
Find the last digit of `3^2026`.

### Q2
Find the largest integer below 2000 that leaves remainder 5 when divided by both 12 and 18.

### Q3
Find the greatest positive integer that leaves the same remainder when dividing 101, 161 and 221. Find the common remainder too.

### Q4
Find the least positive integer satisfying

`N≡2 (mod5)`, `N≡3 (mod7)`.

### Q5
A two-digit number has digit sum 10. Its reversal is 18 greater than the original. Find the number.

### Q6
How many three-digit numbers of the form `a4b` are divisible by 9, where `a` is nonzero and `b` is any digit?

### Q7
How many positive integers `n` make

`(n+9)/(n+3)`

an integer?

### Q8
Positive integers `k>n` satisfy

`k^2-n^2=64`.

Find the sum of all possible values of `k`.

### Q9
How many ordered coprime positive pairs `(a,b)` satisfy

`ab=441`?

### Q10
Consider the sequence `1,1,1,1,1`. How many non-empty consecutive blocks have sum divisible by 3?

### Q11
Find the least odd prime divisor of

`2^4+1`.

Give both a direct check and the order/cycle reason that makes the candidate natural.

### Q12 — source integrity

A reproduced paper has a question whose exponent notation is visibly corrupted. A secondary worked solution says the answer comes from reducing odd residues modulo 4. Can the corrupted wording be published as an exact PYQ anchor after “repairing” the missing symbols from that solution?

---

# Answer and review section

## Q1
**Code:** `MC`.

Last-digit cycle of powers of 3 is `3,9,7,1`. Since `2026≡2 mod4`, answer is `9`.

**Error:** `POWER_CYCLE_POSITION_ERROR`.

## Q2
**Code:** `LM`.

`N-5` must be divisible by `lcm(12,18)=36`.

`N=36k+5<2000`; largest `k=55`.

**Answer:** `1985`.

**Error:** `LCM_GCD_REMAINDER_CONFUSION`.

## Q3
**Code:** `GD`.

Differences are `60,60,120`; greatest possible divisor is `60`.

`101≡41 mod60`, and the others have the same remainder.

**Answer:** divisor `60`, remainder `41`.

**Error:** `LCM_GCD_REMAINDER_CONFUSION`.

## Q4
**Code:** `CR`.

Numbers `2 mod5`: `2,7,12,17,...`; first equal to `3 mod7` is `17`.

**Answer:** `17`.

**Error:** `CRT_CONDITION_NOT_RECHECKED`.

## Q5
**Code:** `PV`.

Let original be `10a+b`.

`a+b=10` and `9(b-a)=18`, so `b-a=2`.

Thus `a=4,b=6`.

**Answer:** `46`.

**Error:** `PLACE_VALUE_NOT_ENCODED`.

## Q6
**Code:** `D9`.

Need `a+b+4≡0 mod9`.

For each nonzero tens digit `a`, one residue for `b` works. When `a=5`, required residue for `b` is 0, represented by both digits `0` and `9`.

Thus `8·1+2=10`.

**Answer:** `10`.

**Errors:** `RESIDUE_ZERO_DIGIT_UNDERCOUNT`, `DIGIT_DOMAIN_IGNORED`.

## Q7
**Code:** `IV`.

`(n+9)/(n+3)=1+6/(n+3)`.

For positive `n`, `n+3>=4`. Among positive divisors of 6, only 6 qualifies, so `n=3`.

**Answer:** `1` value.

**Error:** `INTEGER_DIVISOR_REDUCTION_MISSED`.

## Q8
**Code:** `DS`.

`(k-n)(k+n)=64`.

Same-parity positive factor pairs giving positive `n` are `(2,32)` and `(4,16)`.

They give `k=17` and `k=10`.

Pair `(8,8)` gives `n=0`, not positive.

**Answer:** `27`.

**Errors:** `FACTOR_PAIR_PARITY_IGNORED`, `POSITIVE_DOMAIN_IGNORED`.

## Q9
**Code:** `CP`.

`441=3^2·7^2`.

Coprimality forces each complete prime-square block wholly into either `a` or `b`.

Two independent blocks -> `2^2=4` ordered pairs.

**Answer:** `4`.

**Error:** `COPRIMALITY_UNUSED`.

## Q10
**Code:** `PR`.

Prefix sums including `S0` are:

`0,1,2,3,4,5`, residues mod3:

`0,1,2,0,1,2`.

Each residue appears twice, giving one equal-residue pair per class.

**Answer:** `3` divisible non-empty consecutive blocks.

**Errors:** `PREFIX_S0_OMITTED`, `PREFIX_PAIR_COUNT_ERROR`.

## Q11
**Code:** `OR`.

`2^4+1=17`, so directly the least odd prime divisor is 17.

Order view: modulo a prime divisor `p`, `2^4≡-1`, so `2^8≡1` but `2^4≠1`; the order is 8, forcing an odd prime divisor into the compatible `1 mod8` class. The first candidate is 17, and it divides.

**Answer:** `17`.

**Error:** `ORDER_USED_BEFORE_NONZERO_CHECK`.

## Q12
**Code:** `QC`.

No. A secondary solution may support the mechanism, but it does not restore exact source wording. Record `TRANSCRIPTION_SUSPECT`, retain the item as mechanism evidence, and block exact student-facing PYQ use until an authoritative/independently matched copy restores the notation.

**Error:** `SOURCE_CONFLICT_NOT_FLAGGED`.

---

# Mastery bands

### ADOPTED
- at least 10/12 first moves correct;
- at least 9/12 final answers correct;
- Q2/Q3 distinction correct;
- Q6 residue-zero counting correct;
- Q10 includes `S0`;
- Q12 source custody correct.

### CORE_OK_CEILING_WEAK
Core Q1–Q9 strong but Q10/Q11 weak. Remediate prefix residues/order only; do not restart basic modular arithmetic.

### REMAINDER_MODEL_GAP
Confuses Q2 and Q3. Return to LCM-vs-GCD contrast.

### DIGIT_MODEL_GAP
Misses Q5/Q6. Return to place value and residue-to-digit translation.

### DIVISOR_STRUCTURE_GAP
Misses Q7/Q8/Q9. Return to integrality, factor-pair parity and coprimality.

## Review status

`MATH_REVIEW: PASS_v1`

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`

`FINAL_EDITORIAL_RENDER_QA: NOT_RUN`