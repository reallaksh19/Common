# ALG-07 - Teacher Diagnostic Key

Teacher/authoring material. Not part of the student PDF.

## Recognition and First-Line Lab

1. `3<=3.8<4`, so floor is 3.
2. `-4<-3.8<-3`, so floor is -4.
3. `-4<-3.8<=-3`, so ceiling is -3.
4. `5<=x<6`.
5. `-3<x<=-2`.
6. `4<=(2x+1)/3<5`.
7. `x<3`.
8. Exactly when `x` is an integer.
9. `{-2.3}=-2.3-floor(-2.3)`.
10. First integer `-2`, last integer `3`; count 6.
11. `floor(x+7)=floor(x)+7`.
12. `ceil(x)=-floor(-x)`.
13. `2<=x<3`, then integer filter gives `x=2`.
14. `3<=x^2<4`.
15. Test whether `x` must be an integer.
16. Include 4; exclude 5.

## Practice and Transfer Bank

1. `4,-5,5,-4`.
2. `floor(x)=n <=> n<=x<n+1`; `ceil(x)=n <=> n-1<x<=n`.
3. `0.25` and `0.7`.
4. Direct substitution verifies both cases.
5. `[4,5)`.
6. `(3,4]`.
7. `4<=x<7`.
8. `-4<x<=-3`.
9. `x=3.25`.
10. `2<=x<5/2`.
11. `5/3<x<=2`.
12. `x` is any integer.
13. For noninteger x, write `floor(x)=m`, `ceil(x)=m+1`; `2m+1=7` gives `m=3`, so `x in (3,4)`. Integer x gives an even sum and cannot work.
14. Value 0 if x is integer; value -1 otherwise.
15. `x in (-sqrt(5),-2] union [2,sqrt(5))`.
16. Integers `-3,-2,-1,0,1,2,3,4,5`; count 9.
17. `5<=k<8`; integers `5,6,7`; count 3.
18. Intersection `[5/2,3)`.
19. From the interval definition, reflection gives `ceil(x)=-floor(-x)`.
20. Write `x=n+r`, `0<=r<1`; equality holds iff `{x}<1/2`.
21. Never: the two arguments differ by exactly 1.
22. `x in [5/2,3)`.
23. `x=3.7`.
24. `x in [-4,-3)`; truncation toward zero would misclassify negative nonintegers.
25. Integers `12,13,14,15`.
26. Integers `11,12,13,14,15`; count 5.
27. `1/3<x<=1/2`.
28. Add integer k to `n<=x<n+1`.
29. Floor 2 represents `[2,3)`, not one point.
30. Integer timestamps `3,4,5,6,7`; count 5.

## H0 Mastery Test

1. `5<=(3x-2)/4<6`.
2. `-2<(x+3)/2<=-1`.
3. `7<=x^2<8`.
4. First integer `-4`; last integer `3`; count 8.
5. `11/2<=x<7`.
6. `3<x<=11/3`.
7. `x in (-3,-2)`.
8. `(-sqrt(10),-3] union [3,sqrt(10))`.
9. `k=14,15,16,17`.
10. `0.25`.
11. Exactly `x in Z`.
12. `{x}<0.6`.
13. `floor(x)=4 -> [4,5)`; `ceil(x)=4 -> (3,4]`.
14. `floor(-2.3)=-3`; truncation toward zero gives -2.
15. Integers `13,14,15,16,17,18,19,20`; count 8.
16. Correct translation is `3<=2x<4`, hence `3/2<=x<2`.

## Validated source anchors

- `IOQM-2024-Q21`: independent result 91; verification ledger PASS.
- `IOQM-2024-Q26`: independent result 33; verification ledger PASS.

## Diagnostic tags

- `ALG07-R1`: floor treated as truncation.
- `ALG07-R2`: floor/ceiling endpoint convention reversed.
- `ALG07-R3`: floor equation collapsed to ordinary equality.
- `ALG07-R4`: real interval not separated from integer filter.
- `ALG07-R5`: negative fractional part misread as decimal digits.
- `ALG07-R6`: shift/reflection identity not recognized.
- `ALG07-R7`: endpoint/domain check omitted.

No classroom time threshold, pass probability, percentile or psychometric cutoff is claimed.
