# NT-02 - Teacher Diagnostic Key

Teacher/authoring material; not in the student PDF.

## Recognition lab
1. `5|(38-3)=35`.
2. Not equal; congruent mod 12 because 12 divides 12.
3. `12345 congruent 4 (mod 7)`.
4. `2,4,1,2`.
5. Mod 10.
6. Mod 100.
7. Inverse 3 mod7 is 5: `x congruent 5*6 congruent 2`.
8. gcd(2,6)=2, so 2 has no inverse mod6.
9. `x=2+3k`, then test mod4.
10. Incompatible: residues disagree mod gcd(4,6)=2.
11. Avoid `m|(A-B)`.
12. Base mod7 and exponent mod6 (for nonzero base states).
13. m divides a-b.
14. 5 inverse mod12 is 5.
15. No: gcd(6,15)=3.
16. `a^2 congruent b^2 (mod9)`.

## Practice answers
1. `6,1,1,1`.
2. difference 30 divisible by10.
3. 3.
4. `0,1,2,3,4`.
5. cycle length3; `40 mod3=1`, answer2.
6. 7 powers mod10 cycle 7,9,3,1; `2026 mod4=2`, answer9.
7. 25.
8. inverse3 mod7=5; `x congruent 25 congruent4`.
9. `x congruent 8 (mod15)`.
10. 3 has order6; `100 mod6=4`; `3^4=81 congruent4`.
11. `2^2025` last digit2; `3^2025` last digit3; sum last digit5.
12. inverse5 mod12=5; `x congruent40 congruent4`.
13. divide condition correctly: `4(x-2)` divisible12 -> `x congruent2 (mod3)`; classes `2,5,8,11 mod12`.
14. gcd(6,9)=3; difference3 divisible3, compatible.
15. numbers 3 mod4: 3,7,11,15,19,...; first 5 mod7 is19.
16. `3^20 mod100=1`, so last two digits01.
17. induction from 25*5=125 congruent25 mod100.
18. 3.
19. 6.
20. polynomial operations preserve congruence.
21. `2*1 congruent2*5 (mod8)` but `1` not congruent `5` mod8.
22. `6x=9 (mod15)` has no solution because gcd(6,15)=3 divides9; divide by3 gives `2x congruent3 (mod5)`, x congruent4 mod5 -> classes `4,9,14 mod15`.
23. `2^1000 mod7=2`, `3^1000 mod7=4`; total6.
24. `11^2=121 congruent21`, powers mod100 cycle? Direct binomial `(1+10)^n congruent 1+10n (mod100)`; n=2026 gives61.
25. gcd(6,9)=3; residue difference3 divisible3, compatible. `x=4+6k`; k congruent? 4+6k congruent7 mod9 ->6k congruent3 ->2k congruent1 mod3 ->k congruent2 mod3; least x=16.
26. `7(x-2)` divisible21 -> `x congruent2 (mod3)`; residues `2,5,8,11,14,17,20`.
27. 31.
28. preserve zero set ->7|T; preserve all nonzero base powers ->3^T=1 mod7, order6 ->6|T.
29. gcd(10,30)=10; cancellation only reduces modulus to3; conclusion is `x congruent2 (mod3)`.
30. gcd(4,6)=2 but residue difference3 not divisible2: no solution.

## H0 answers
1. `12|(83-11)`.
2. Work mod10; cycle of 7.
3. gcd(4,9)=1; inverse exists.
4. gcd(6,9)=3; difference3 is divisible3, so compatible.
5. `2026 mod3=1`; answer2.
6. 25.
7. inverse5 mod12=5; x congruent35 congruent11.
8. gcd(6,18)=6 divides12; divide by6: x congruent2 mod3 -> classes `2,5,8,11,14,17`.
9. 9.
10. `1234 mod6=4`; answer `3^4 mod7=4`.
11. gcd(4,6)=2 but residue difference1 not divisible2: no solution.
12. powers of7 mod10 cycle length4; exponent `7^7 mod4 =3`; answer `7^3 mod10=3`.
13. `14|42` is equivalent to `42 congruent0 (mod14)`; divisibility is the zero-residue special case of congruence.
14. Mod7: inverse3 exists ->x congruent2. Mod9: gcd3,9=3; reduce to `x congruent2 (mod3)` -> classes 2,5,8 mod9.
15. 31; below 14 pigeonhole, 14..30 each has a collision, mod31 fourth-power residues are all distinct.
16. `2^n mod7` cycles `2,4,1`; `100 mod3=1`; residue2.

## Diagnostic tags
- `NT02-R1` equality/congruence confusion.
- `NT02-R2` divisibility/congruence bridge missing.
- `NT02-R3` wrong target modulus.
- `NT02-R4` brute-force power instead of cycle.
- `NT02-R5` illegal cancellation/inverse gap.
- `NT02-R6` simultaneous-congruence compatibility gap.
- `NT02-R7` base-period/exponent-period confusion.
