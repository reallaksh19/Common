# COMB-01 - Teacher Diagnostic Key

Teacher/control artifact. Internal topic and support-control language is allowed here; it is not included in the student PDF.

## Governing diagnostic

A wrong numerical count should be classified before correcting arithmetic:
1. counted-object/identity error;
2. ordered-vs-unordered error;
3. non-disjoint or non-exhaustive case split;
4. stage/product error;
5. repeated-object overcount;
6. restriction applied too late;
7. complement universe mismatch;
8. inclusion-exclusion overlap error;
9. counting/arithmetic ownership collision.

## Historical anchors

- `IOQM-2025-Q05 = 45`: sum admissible pair counts `9+8+...+1`.
- `IOQM-2025-Q15 = 40`: restricted injection of three coupon-pairs into distinct envelopes; allowed sets `{3,4,5,6}`, `{1,2,5,6}`, `{1,2,3,4}`. IE check: `120-120+48-8=40`.
- `IOQM-2025-Q18 = 40`: `C(9,2)*C(6,2)=540`, requested remainder mod 100 is 40.
- `IOQM-2024-Q02 = 12`: `2*3!`.
- `IOQM-2023-Q07 = 48`: fix the 1/2 axis, six cyclic orders, `2^3` opposite-pair colour choices.
- `IOQM-2023-Q17 = 66`: fourth order statistic expectation `200/3`, requested floor 66.
- `IOQM-2023-Q20 = 43`: factor cardinality/max constraints, then binomial counts; independent verification gives `N=439`, requested `4+39`.

## Practice answers

1. 12 — product of 3 shirt and 4 cap choices.
2. 8 — disjoint alternatives `5+3`.
3. 15 — `C(6,2)`.
4. 24 — `4!`.
5. 12 — `4!/2!`.
6. 12 — choose units digit 2 or 4, then `3!`.
7. 56 — `C(8,3)`.
8. 60 — `6!/(3!2!)`.
9. 60 — `5*4*3`.
10. 10 — choose positions of two ones: `C(5,2)`.
11. 300 — first digit 5 choices, then `5*4*3`.
12. 360 — symmetry: half of `6!` have 1 before 2.
13. 128 — choose which of 1,2 is present, then any subset of remaining six: `2*2^6`.
14. 60 — ordered injection `5*4*3`.
15. 61 — `5^3-4^3`.
16. 1260 — `7!/(2!2!)`.
17. 1260 — last digit 0 contributes `6*5*4*3=360`; last digit 2/4/6 contributes `3*(5*5*4*3)=900`.
18. 140 — `C(10,4)-C(8,4)=210-70`.
19. 3600 — `7!-2*6!`.
20. 30 — the two pairwise order constraints divide `5!` by 4.
21. 9 — derangements of four; IE gives `24-24+12-4+1=9`.
22. 60 — `50+20-10`.
23. 1560 — `4^6-4*3^6+6*2^6-4`.
24. 30 — fix one 3 last, arrange `11223`: `5!/(2!2!)`.
25. 120 — total `7!/(3!2!2!)=210`; bad first-1 arrangements `6!/(2!2!2!)=90`.
26. 456 — `C(4,2)C(8,3)+C(4,3)C(8,2)+C(4,4)C(8,1)`.
27. 25 at least one; 5 neither — `18+16-9=25`.
28. 360 — choose 2 of the 3 even and all 3 odd digits, then arrange: `C(3,2)*5!`.
29. 60 — total `6!/(2!2!2!)=90`; bad AA-block `5!/(2!2!)=30`.
30. 540 — `3^6-3*2^6+3`.

## Independent mastery answers

1. 56 — ordered roles `8*7`.
2. 28 — unordered `C(8,2)`.
3. 12 — last digit 1 or 3, then `3!`.
4. 30 — `5!/(2!2!)`.
5. 127 — `2^7-1`.
6. 60 — `40+30-10`.
7. 105 — `C(9,4)-C(7,2)=126-21`.
8. 600 — first digit 5 choices, then `5*4*3*2`.
9. 9 — derangements of four.
10. 30 — fix one 2 last, arrange `11223`.
11. 175 — `C(10,4)-C(7,4)=210-35`.
12. 90 — each of three independent pair-order constraints halves `6!`: `720/8`.
13. 150 — `3^5-3*2^5+3`.
14. 60 — `6!/(3!2!)`.
15. 360 — `C(3,2)*C(3,3)*5!`.
16. 36 — `C(8,3)-C(6,3)=56-20`.

## H-control fading map

H3: counted object, representation and first computation line supplied.
H2: counted object/representation supplied; computation withheld.
H1: only the distinguishing clue is supplied.
H0: no route label or default hint.

These H-levels are teacher controls and must not appear in the learner export.
