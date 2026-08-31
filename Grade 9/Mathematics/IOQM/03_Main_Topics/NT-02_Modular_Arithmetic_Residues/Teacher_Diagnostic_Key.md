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
12. Base mod7 and exponent mod6 for nonzero base states.
13. m divides a-b.
14. 5 inverse mod12 is 5.
15. No: gcd(6,15)=3.
16. `a^2 congruent b^2 (mod9)`.

## Practice answers
1. `6,1,1,1`.
2. difference 30 divisible by10.
3. 3.
4. `0,1,2,3,4`.
5. 2.
6. 9.
7. 25.
8. `x congruent4 (mod7)`.
9. `x congruent8 (mod15)`.
10. 4.
11. 5.
12. `x congruent4 (mod12)`.
13. `x congruent2 (mod3)`; classes `2,5,8,11 mod12`.
14. compatible.
15. 19.
16. last two digits 01.
17. induction from `25*5=125 congruent25 mod100`.
18. period 3.
19. period 6.
20. polynomial operations preserve congruence.
21. `2*1 congruent2*5 (mod8)` but `1` not congruent5 mod8.
22. `x congruent4 (mod5)` -> classes `4,9,14 mod15`.
23. 6.
24. 61.
25. 16.
26. residues `2,5,8,11,14,17,20 mod21`.
27. 31.
28. preserve zero set ->7|T; residue3 has order6 ->6|T.
29. gcd(10,30)=10; only `x congruent2 (mod3)` follows.
30. no solution.

## H0 answers
1. `12|(83-11)`.
2. work mod10; cycle of 7.
3. gcd(4,9)=1; inverse exists.
4. gcd(6,9)=3; difference3 divisible3, compatible.
5. 2.
6. 25.
7. `x congruent11 (mod12)`.
8. classes `2,5,8,11,14,17 mod18`.
9. 9.
10. 4.
11. no solution.
12. 3.
13. divisibility is the zero-residue special case of congruence.
14. mod7: `x congruent2`; mod9: `x congruent2 (mod3)` -> classes 2,5,8.
15. 31.
16. cycle `2,4,1`; `100 mod3=1`; residue2.

## Diagnostic tags
- `NT02-R1` equality/congruence confusion.
- `NT02-R2` divisibility/congruence bridge missing.
- `NT02-R3` wrong target modulus.
- `NT02-R4` brute-force power instead of cycle.
- `NT02-R5` illegal cancellation/inverse gap.
- `NT02-R6` simultaneous-congruence compatibility gap.
- `NT02-R7` base-period/exponent-period confusion.
