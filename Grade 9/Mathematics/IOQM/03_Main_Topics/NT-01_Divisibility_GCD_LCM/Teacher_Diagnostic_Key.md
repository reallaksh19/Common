# NT-01 - Teacher Diagnostic Key

This key is teacher/authoring material. It is not included in the student PDF.

## Recognition and First-Line Lab

1. `d | (296-188)`, so `d|108`.
2. `N=lcm(14,20,35)` for the least positive common multiple; value 140 if completed.
3. `12345=2(5432)+1481`; continue Euclid.
4. `ab=9*252=2268`.
5. `3(5x+7y)-7(2x+3y)=x`, so `d|x`. Also `5(2x+3y)-2(5x+7y)=y`.
6. `N-4=lcm(6,10,15)=30` for the least solution, so `N=34` if completed.
7. `d|(1046-812)=234` and `d|(1280-1046)=234`.
8. `lcm(18,24)=72` minutes.
9. `gcd(u,v)=1`.
10. `1260=84*15`.
11. `7(4n+7)-4(7n+13)=-3`, so `d|3`.
12. `6|x|72`.
13. Differences are `1457-1001=456` and `1913-1457=456`; start with their gcd.
14. `ab=12*420=5040`; stop because only the product is requested.
15. `a=12u`, `b=12v`, `gcd(u,v)=1`, `uv=420/12=35`.
16. Write one division-with-remainder equation `a=qb+r` and replace the gcd pair by `(b,r)`.

### Recognition diagnostic

- `NT01-R1`: divisor-vs-multiple confusion.
- `NT01-R2`: same-remainder fork not recognized.
- `NT01-R3`: Euclidean reduction not recognized as invariant-preserving.
- `NT01-R4`: structural divisibility replaced by an irrelevant digit test.
- `NT01-R5`: gcd/lcm product used without deciding whether reconstruction is required.
- `NT01-R6`: divisibility chain/transitivity missed.

## Practice and Transfer Bank

### F0

1. Yes: `234=18*13`.
2. `48-30=18`; common divisibility is closed under subtraction.
3. `gcd(84,126)=42`, `lcm(84,126)=252`.
4. From `8|24` and `24|120`, `8|120`. Also `gcd(24,120)=24` and `lcm(24,120)=120`.

### F1

5. `239-155=84`; greatest divisor 84.
6. `lcm(16,20,24)=240`.
7. Euclid gives `gcd(2025,748)=1`.
8. `lcm(12,18,30)=180`; `N=7+180=187`.
9. `ab=12*420=5040`.

### F2

10. Differences are 144 and 144; answer 144.
11. Differences are 168 and 168. All positive divisors of 168 work:
   `1,2,3,4,6,7,8,12,14,21,24,28,42,56,84,168`.
12. `lcm(12,15,20)=60`; `N=69`.
13. Normalize: `a=12u`, `b=12v`, `gcd(u,v)=1`, `uv=35`. Unordered pairs:
   `(12,420)` and `(60,84)`.
14. Write `x=6k` and require `6k|72`, hence `k|12`. Values:
   `x in {6,12,18,24,36,72}`.

### F3

15. From
   `2(7x+5y)-5(3x+2y)=-x` and
   `3(7x+5y)-7(3x+2y)=y`,
   any common divisor divides both `x` and `y`. If `gcd(x,y)=1`, only `d=1` is possible; therefore no `d>1` satisfies the premise.
16. `lcm(18,24,40)=360` minutes; next reset is 15:00.
17. `7(4n+7)-4(7n+13)=-3`, so `d|3`. Values 1 and 3 are both attainable; for `d=3`, take `n congruent 2 (mod 3)` in ordinary remainder language.
18. `uv=900/15=60`, `gcd(u,v)=1`. Unordered coprime splits:
   `(1,60),(3,20),(4,15),(5,12)`. Thus
   `(a,b)=(15,900),(45,300),(60,225),(75,180)` up to order.
19. Differences are 456 and 456; largest step 456 mm.

### F4

20. 456.
21. `N+5` must be a multiple of `lcm(18,24,30)=360`; least positive `N=355`.
22. `11(7n+5)-7(11n+8)=-1`; largest possible positive divisor is 1.
23. Let `x=gcd(a,c)`, `y=gcd(b,c)`. The relation reduces to
   `a(27/x-26)+b(27/y-26)=0`. Exactly one of `x,y` is 1. Under `a,b<=50`, the other is forced to 2, yielding the two symmetric core pairs `(25,2)` and `(2,25)` before counting admissible `c`. A completed independent count gives 40, matching the validated anchor.
24. `N-5` is a multiple of `lcm(12,18)=36`, so `N=5+36k`. Requiring `5|N` gives `k divisible by 5`. For `N>5`, least `k=5`, hence `N=185`.

### Transfer prompts

25. `d|(a-b)`.
26. Largest equal spacing is a common-divisor target -> gcd; first synchronization is a common-multiple target -> lcm.
27. Product is fixed: `ab=18*630=11340`. The actual pair is not unique because after `a=18u,b=18v`, one has `uv=35`, `gcd(u,v)=1`, allowing `(u,v)=(1,35)` or `(5,7)` and their reversals.
28. Retrieve `d|(a-b)` from the equal-remainder condition; do not reteach modular legality here.
29. The target is a divisor of differences, not a common multiple. Start with differences 144,144 and gcd them.
30. `gL=ab` alone does not determine a unique pair. Normalize and enforce `gcd(u,v)=1`; `(60,84)` is a second unordered pair besides `(12,420)`.

## H0 Mastery Test

1. `d|(596-428)=168` and `d|(764-596)=168`.
2. `N-11=lcm(18,24,30)`.
3. `8(13n+9)-13(8n+5)=7`, so `d|7`.
4. `ab=14*840=11760`.
5. Euclid gives `gcd(123456,7890)=6`.
6. 168.
7. `lcm(18,24,30)=360`; `N=371`.
8. 11760.
9. `11(7n+5)-7(11n+8)=-1`; answer 1.
10. All positive divisors of 168:
   `1,2,3,4,6,7,8,12,14,21,24,28,42,56,84,168`.
11. `ab=12*360=4320`; with `a=72`, the other number is 60. Check: `gcd(72,60)=12`, `lcm(72,60)=360`.
12. `lcm(28,42,63)=252` days.
13. A: differences are 102 and 102 -> greatest divisor 102. B: `N-5=lcm(6,10,15)=30` -> least `N=35`. First moves differ because A asks for an unknown divisor, while B constructs an unknown number with a prescribed remainder.
14. A: digit sum of 7425 is 18, so it is divisible by 9. B: the linear combination is `7(4n+7)-4(7n+13)=-3`, so possible positive `d` are 1 and 3, both attainable. A is a local one-number test; B is a structural common-divisor relation.
15. Differences are 234 and 234, so the largest unit is 234 m. Hidden model: equal offsets mean equal remainders, so the unit divides all position differences.
16. Counterexample: item 6 mentions same remainders but asks for the divisor, so the correct route is gcd of differences. Decision boundary: identify whether the unknown is the divisor or the number being constructed.

## Source-anchor audit

### IOQM-2025-Q02

Independent count: `floor(100/3)-floor(100/6)=33-16=17`. Final official key: 17. `PASS`.

### IOQM-2025-Q27

Independent reduction through `lcm(x,c)=xc/gcd(x,c)` forces the two symmetric core pairs `(25,2)` and `(2,25)` and 20 admissible `c` values for each. Total 40. Final official key: 40. `PASS`.

## H0 diagnostic rule

Static diagnostic only, not psychometric calibration:

- if a learner repeatedly needs a method label before writing a first useful line, route back to the First-Step Reference;
- if the learner calculates correctly but confuses divisor/multiple or unknown-divisor/unknown-number boundaries, classify as a recognition error rather than an arithmetic error;
- no classroom time threshold, pass probability, percentile or psychometric cutoff is claimed here.
