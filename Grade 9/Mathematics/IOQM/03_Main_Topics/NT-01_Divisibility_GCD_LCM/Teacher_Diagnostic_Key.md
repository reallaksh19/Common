# NT-01 — Teacher Diagnostic Key

## Recognition lab first lines

1. `d | (296-188)`.
2. `N = lcm(14,20,35)`.
3. `12345 = 2(5432)+1481` then continue Euclid.
4. `ab = 9*252 = 2268`.
5. Any integer linear combination; e.g. subtract suitable multiples to isolate `x` or `y`.
6. `N-4 = lcm(6,10,15)`.
7. `d | 234` and `d | 234`; equivalently take gcd of adjacent differences.
8. `lcm(18,24)`.
9. `gcd(u,v)=1`.
10. `1260=84*15`.

## Practice answers

1. yes, quotient 13.
2. gcd 42; lcm 252.
3. both sides 432.
4. 84.
5. 240.
6. 1.
7. 144.
8. `N=69`.
9. 5040.
10. Accept any valid integer-linear-combination argument; diagnose whether the learner knows closure of divisibility under addition/subtraction.
11. 15:00 (360 minutes later).
12. `uv=60`; coprime unordered factor pairs `(1,60),(3,20),(4,15),(5,12)`.
13. 456.
14. `N=355`.
15. From `7(4n+7)-4(7n+13)=-3`, so `d|3`; possible positive `d` are 1 or 3, with attainability checked.
16–18. Explanatory; look for exact divisibility language and correct decision boundary.

## H0 mastery answers

1. Differences are 168 and 168 -> `168`.
2. `N-11=lcm(18,24,30)=360` -> `371`.
3. Euclid gives `gcd=6`.
4. `11760`.
5. `11(7n+5)-7(11n+8)=-1`; any common positive divisor is 1 -> largest `1`.
6. Differences 168,168 -> positive divisors of 168.
7. `ab=12*360=4320`; `b=60`.
8. `lcm(28,42,63)=252` days.
9. Common divisors of `a,b` are exactly common divisors of `a,a-b`.
10. Subtract the two quotient-remainder forms.

## Diagnostic tags

- `NT01-R1` divisor-vs-multiple confusion.
- `NT01-R2` fails same-remainder subtraction.
- `NT01-R3` Euclidean algorithm not understood as invariant-preserving.
- `NT01-R4` gcd/lcm product used mechanically without positivity/coprime normalization awareness.
- `NT01-R5` incomplete finite divisor set.
- `NT01-R6` linear-combination divisibility gap.

## Gate

A learner is not H0-ready if they need method labels on more than 2 of items 1–8, even if arithmetic is correct.
