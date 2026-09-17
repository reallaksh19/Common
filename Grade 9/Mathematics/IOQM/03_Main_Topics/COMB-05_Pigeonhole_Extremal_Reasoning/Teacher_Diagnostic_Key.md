# COMB-05 - Teacher Diagnostic Key

## Recognition / First-Line Lab
1. Boxes are residues modulo 16.
2. Ten club boxes; if every box had at most 3, total capacity would be 30.
3. Divide the square into four `1/2 x 1/2` squares; each has diameter `sqrt(2)/2`.
4. Pair boxes `{1,10},{2,9},{3,8},{4,7},{5,6}`.
5. Select an element extremal for the property used by the closure operation; the extremal choice must forbid a strictly better admissible element.
6. Choose a shortest interval.
7. Inclusion-exclusion/complement counting: the task asks for an exact count with overlapping forbidden properties.
8. Inequality optimization: the domain is continuous and the target is a numerical extremum.
9. Twelve residue boxes modulo 12; two coincide.
10. Partition the triangle into 9 congruent equilateral triangles of side `1/3`; 10 points force a shared small triangle, whose diameter is `1/3`.
11. Pair `{1,2},{3,4},...,{99,100}`; 51 choices force a full pair.
12. Pick one person P. Among the other 5, at least 3 are all acquaintances of P or all strangers to P. If P knows all three and any two know each other, there is an acquaintance triangle; otherwise those three form a stranger triangle. The complementary case is analogous.

## Practice / Transfer
1. `ceil(25/6)=5`.
2. Seven residue classes modulo 7.
3. One hundred residue classes modulo 100.
4. `ceil(40/12)=4`.
5. Ten boxes `{1,2},{3,4},...,{19,20}`.
6. Four half-size squares.
7. Nine congruent subtriangles of side `1/3`.
8. Six pair boxes summing to 13.
9. Four residue classes modulo 4.
10. The stated consequence is the defining no-improvement property of the closest pair.
11. `deg(v_max)>=deg(v)` for every vertex v.
12. A strictly smaller nonempty member of the family would contradict the choice.
13. Same adjacent-pair proof as item 5, with 50 boxes. Enumeration is irrelevant because only forced existence is requested.
14. Partition the side-2 square into 16 squares of side `1/2`; 25 points force two in one cell, distance at most `sqrt(2)/2`.
15. Same six-person proof as Recognition item 12.
16. There are `C(20,4)=4845` increasing quadruples. Direct counting of `a+c=b+d` gives 525 balanced, hence 4320 unbalanced. Among 4411 selected, at least `4411-4320=91` are balanced.
17. An average forces an inequality threshold, not an exact occupancy.
18. Twelve residue classes solve the existence claim immediately; exact overlap counts are unnecessary.
19. The structure is discrete/local; the chosen edge must be used to forbid a smaller admissible edge or force a structural contradiction.
20. Same-cell membership is useful only if it implies the desired distance bound; diameter, not area, controls that implication.

## Mastery
1. residues modulo 19.
2. `ceil(37/9)=5`.
3. Seven boxes `{1,14},...,{7,8}`.
4. four half-size squares.
5. fifty adjacent pairs.
6. elementary `R(3,3)=6` proof as above.
7. Choosing an extreme object is useful only when the operation or constraints would produce a strictly smaller/larger admissible object, contradicting extremality. No such consequence has been supplied.
8. Pigeonhole establishes existence/capacity, not the exact union size with overlaps.
9. This is a continuous numerical bound; use an inequality/equivalent algebraic representation.
10. 525. For each `b<d`, let `s=b+d`; count `a<b` with `c=s-a>d` and `c<=20`. Summing gives 525.
11. 91.
12. Partition the side-2 square into 16 half-unit squares; 17 points force two in one, giving distance at most `sqrt(2)/2`, which is stronger than `sqrt(2)`.

## Historical source audit
- `IOQM-2023-Q18`: verified answer 71. Add all 50 polygon sides to the selected diagonals. The selected-diagonal condition gives an outer 1-planar graph; the tight edge bound is `5n/2-4=121`, so at most 71 diagonals. A fan of 47 diagonals from one vertex plus 24 alternating short diagonals attains 71. This density lemma is source-analysis material, not a Grade-9 prerequisite doctrine.
- `IOQM-2023-Q27`: verified answer 91 by the 525-balanced / 4320-unbalanced count above.

All learner items and answers were independently recomputed before freezing.
