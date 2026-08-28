# P0 Number Theory — Modular / Divisibility / Digit Transfer Bank v1

All 18 items are `AUTHOR_CREATED_TRANSFER`, not NMTC PYQs.

Profile order: `C/R/F/S/A/H/K/B/T/P`.

## A — Modular cycles

### A1
Find `3^100 mod 7`.

**Answer:** `4`.
**Solution:** powers of 3 mod7 have period 6; `100≡4 mod6`; `3^4=81≡4`.
**Profile:** `3/4/3/3/2/4/1/2/3/3`.

### A2
Find the last digit of `7^222`.

**Answer:** `9`.
**Solution:** last-digit cycle `7,9,3,1`; `222≡2 mod4`.
**Profile:** `2/3/2/2/1/3/1/1/2/2`.

### A3
Find `(2^50+3^50) mod 5`.

**Answer:** `3`.
**Solution:** both power cycles have period 4; exponent 50 gives position 2. `2^50≡4`, `3^50≡4`; sum `8≡3`.
**Profile:** `4/5/4/4/3/5/2/3/4/4`.

## B — Same remainder: LCM vs GCD

### B1
Find the least integer greater than 5 that leaves remainder 5 when divided by 6, 8 and 9.

**Answer:** `77`.
**Solution:** `N-5` multiple of `lcm(6,8,9)=72`; least nonzero gives `77`.
**Profile:** `3/5/4/3/2/5/2/2/4/4`.

### B2
Find the largest integer below 1000 that leaves remainder 4 when divided by both 12 and 15.

**Answer:** `964`.
**Solution:** `N=60k+4`; `60k+4<1000`; largest `k=16`.
**Profile:** `3/5/4/3/3/5/2/2/4/4`.

### B3
Find the greatest positive integer that leaves the same remainder when dividing 143, 221 and 299. Also find that common remainder.

**Answer:** divisor `78`, remainder `65`.
**Solution:** differences are `78,78,156`; GCD `78`. `143≡65 mod78`.
**Profile:** `4/6/5/4/3/6/2/3/5/5`.

## C — Simultaneous congruences

### C1
Find the least positive integer satisfying `N≡2 mod3`, `N≡3 mod5`.

**Answer:** `8`.
**Solution:** numbers `2 mod3`: `2,5,8,...`; 8 is `3 mod5`.
**Profile:** `2/3/2/2/2/3/1/2/2/2`.

### C2
Find the least positive integer satisfying `N≡1 mod4`, `N≡2 mod5`, `N≡3 mod7`.

**Answer:** `17`.
**Solution:** `17` satisfies all three; constructive progression from `1 mod4` reaches it first.
**Profile:** `5/6/5/5/4/6/3/4/5/5`.

### C3
Find the least positive integer satisfying `N≡4 mod6` and `N≡1 mod5`.

**Answer:** `16`.
**Solution:** `4,10,16,...`; first with residue 1 mod5 is 16.
**Profile:** `2/3/2/2/2/3/1/2/2/2`.

## D — Digit and place-value structure

### D1
A two-digit number has digit sum 11. Its reversal is 27 greater than the original. Find the number.

**Answer:** `47`.
**Solution:** `a+b=11`; `9(b-a)=27`; hence `b-a=3`, so `a=4,b=7`.
**Profile:** `3/4/3/3/3/4/3/2/3/3`.

### D2
How many three-digit numbers of the form `a7b` are divisible by 9, where `a` is nonzero and `b` is any digit?

**Answer:** `10`.
**Solution:** `a+b+7≡0 mod9`. For each `a=1..9` there is one residue class for `b`; when `a=2`, required residue is 0 and both `b=0,9` work. Thus `8·1+2=10`.
**Profile:** `5/6/5/5/3/6/5/4/6/6`.

### D3
Show that every four-digit repeated-block number `ABAB` is divisible by 101.

**Answer:** `ABAB=101·AB`.
**Solution:** `(1000A+100B+10A+B)=101(10A+B)`.
**Profile:** `3/5/4/3/3/5/2/2/3/4`.

## E — Integer-valued rational expressions

### E1
How many positive integers `n` make `(n+7)/(n+2)` an integer?

**Answer:** `1`.
**Solution:** `1+5/(n+2)`; positive `n` means `n+2>=3`; only positive divisor 5 works, giving `n=3`.
**Profile:** `4/6/5/4/3/6/4/3/5/5`.

### E2
How many positive integers `n` make `(2n+5)/(n+1)` an integer?

**Answer:** `1`.
**Solution:** `2+3/(n+1)`; `n+1>=2`; only divisor 3 gives `n=2`.
**Profile:** `4/6/5/4/3/6/4/3/5/5`.

### E3
How many integers `n` make `(n+10)/(n-2)` an integer?

**Answer:** `12`.
**Solution:** `1+12/(n-2)`; `n-2` may be any nonzero integer divisor of 12: `±1,±2,±3,±4,±6,±12`.
**Profile:** `5/6/6/5/4/7/6/4/6/6`.

## F — Factor/coprime structure

### F1
Positive integers `k>n` satisfy `k^2-n^2=45`. Find the sum of all possible values of `k`.

**Answer:** `39`.
**Solution:** factor pairs `(1,45),(3,15),(5,9)` are odd/odd, giving `k=(u+v)/2`: `23,9,7`; sum 39.
**Profile:** `5/6/5/5/3/6/6/4/5/5`.

### F2
Find all positive integers `n` for which `n(n+1)` is a perfect square.

**Answer:** none.
**Solution:** consecutive integers are coprime. If their product is square, both must be squares; no two positive consecutive integers are both squares.
**Profile:** `5/7/6/4/2/7/4/2/6/5`.

### F3
How many ordered coprime positive pairs `(a,b)` satisfy `ab=900`?

**Answer:** `8`.
**Solution:** `900=2^2·3^2·5^2`. Coprimality forces each complete prime-square block to go wholly to `a` or `b`. Three independent choices give `2^3=8` ordered pairs.
**Profile:** `6/7/6/5/3/7/5/3/6/6`.

## Error tags

- `BASE_NOT_REDUCED`
- `POWER_CYCLE_POSITION_ERROR`
- `LCM_GCD_REMAINDER_CONFUSION`
- `CRT_CONDITION_NOT_RECHECKED`
- `PLACE_VALUE_NOT_ENCODED`
- `DIGIT_DOMAIN_IGNORED`
- `RESIDUE_ZERO_DIGIT_UNDERCOUNT`
- `DIVISIBILITY_RULE_USED_WITHOUT_STRUCTURE`
- `INTEGER_DIVISOR_REDUCTION_MISSED`
- `NEGATIVE_DIVISORS_OMITTED`
- `DENOMINATOR_ZERO_INCLUDED`
- `FACTOR_PAIR_PARITY_IGNORED`
- `COPRIMALITY_UNUSED`

## Review state

`MATH_REVIEW: PASS_v1`

All answers above have compact independent derivations. Classroom timing/render QA remains pending.