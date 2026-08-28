# P1 Combinatorics — Recognition Lab v1

**Goal:** classify the best first move. Do not solve.

Target: 20 items in 8 minutes.

Choose one label:

`ORDERED`, `UNORDERED`, `MULTIPLY`, `DISJOINT_CASES`, `COMPLEMENT`, `INCLUSION_EXCLUSION`, `PIGEONHOLE`, `SUBSET_PRODUCT`, `COEFFICIENT_COUNT`, `STATE_COUNT`.

1. Choose 4 books from 12 for a reading set.
2. Award first, second and third prizes among 12 students.
3. Form a 5-digit number with no leading zero.
4. Count strings containing at least one A.
5. Count integers divisible by 4 or 7.
6. Prove two of 10 integers have the same remainder mod 9.
7. Sum products over all non-empty subsets of given numbers.
8. Coefficient of `x^30` in two finite geometric sums.
9. Exact 8-step walks on a small graph.
10. Count even numbers by splitting according to final digit.
11. Choose president plus an unordered 3-person committee.
12. Count people in at least one of three clubs with overlap data.
13. Prove one of 7 boxes contains at least 5 of 29 objects.
14. Count arrangements in which two specified objects are adjacent.
15. Count digit strings avoiding a specified digit.
16. Count triangles from a point set after classifying degenerate/non-degenerate triples.
17. A term in an expansion is obtained by independently selecting `1` or `a_i` from each factor.
18. Count solutions to `i+j=70` under finite exponent bounds.
19. A token moves left/right with forbidden boundary exits.
20. Printed count and supplied key disagree after a direct sample-space count.

## Key

1 UNORDERED
2 ORDERED
3 MULTIPLY / DISJOINT_CASES depending digit restrictions; first define controlling positions
4 COMPLEMENT
5 INCLUSION_EXCLUSION
6 PIGEONHOLE
7 SUBSET_PRODUCT
8 COEFFICIENT_COUNT
9 STATE_COUNT
10 DISJOINT_CASES
11 ORDERED then UNORDERED stages
12 INCLUSION_EXCLUSION
13 PIGEONHOLE
14 MULTIPLY after block compression
15 COMPLEMENT
16 DISJOINT_CASES
17 SUBSET_PRODUCT
18 COEFFICIENT_COUNT
19 STATE_COUNT
20 source-integrity check; do not force a counting label/key
