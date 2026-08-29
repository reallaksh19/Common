# Issue #50 Wave 4 Teacher Key

## A recognition
1 unordered subset
2 ordered four-role assignment
3 captain first + unordered 3-subset from remaining
4 digit slots; leading + even last restriction
5 ordered string; leading zero legal
6 complement candidate
7 IE
8 disjoint casework by last digit
9 sequential multiply
10 pigeonhole residues mod9
11 strong pigeonhole
12 subset product
13 bounded exponent pair
14 bounded exponent triple
15 state recurrence
16 repeated-object arrangement
17 `FIGURE_GATED_ANCHOR`
18 `SOURCE_CONFLICT_EVIDENCE`
19 three-set IE
20 uniqueness before encoding count
21 repair case partition
22 leading-zero defect

## B first lines
23 `C(12,3)`
24 `12·11·10`
25 `9*C(8,2)`
26 split by last digit 0 vs 2/4 and enforce nonzero first digit
27 `3^6-2^6`
28 `50+20-10`
29 `60+40+24-20-12-8+4`
30 13 residue boxes for 14 integers
31 `ceil(31/6)=6`
32 `(1+1)(1+3)(1+5)-1`
33 count `(i,j)` with `i+j=9`, `0≤i≤4`, `0≤j≤7`
34 define state recurrence; answer later is 3
35 `7!/(2!2!)`
36 printed sample space gives `5·4=20`; preserve conflict

## C answers
37 `C(10,4)=210`
38 `10·9·8=720`
39 `10*C(9,3)=840`
40 `5·5·4·3=300`
41 `156`
42 `4^5-3^5=781`
43 `3^5=243`
44 `90+60-30=120`
45 `90+60+36-30-18-12+6=132`
46 16 residue boxes for 17 integers
47 `ceil(52/9)=6`
48 `(3)(5)(6)-1=89`
49 2
50 9
51 `6!/(3!2!)=60`
52 `7!/(2!2!)=1260`
53 8
54 9
55 `10^4-9^4=3439`
56 `9·9·8·7=4536`
57 `C(12,3)=220`
58 `12·11·10=1320`
59 9
60 27

## D WHY NOT
61 internal order does not change the team; ordered count counts each team `3!` times.
62 roles differ; swapping office holders changes the outcome.
63 shared objects are double-counted.
64 leading zero does not create a 4-digit integer.
65 direct cases can overlap/omit; complement partitions the universe cleanly.
66 factor-specific exponent caps are part of the sample space.
67 box design is the proof; without it the claimed collision is unsupported.
68 encoding count may count the same object more than once.

## E
69 `C_{t+1}(j)=sum C_t(i)` over legal predecessor states `i` adjacent to `j`.
70 boundary-forbidden moves make some L/R strings illegal; different path histories may also be better compressed by state.
71 if `a0+3a1=b0+3b1`, then `3(a1-b1)=b0-a0`; RHS has magnitude ≤2, so both differences are 0.
72 `9 > 2(1+3)=8`.
73 `FIGURE_GATED_ANCHOR`; mechanism may be taught with an author-created text-complete model, not reconstructed as exact historical figure.
74 `SOURCE_CONFLICT_EVIDENCE`; preserve independent recount and do not alter sample space to force key agreement.
