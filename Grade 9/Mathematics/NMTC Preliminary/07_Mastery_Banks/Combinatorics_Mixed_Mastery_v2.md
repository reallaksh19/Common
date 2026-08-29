# Counting, P&C, Pigeonhole & Inclusion–Exclusion — Wave 4 Student Mastery
## H0 independent paper

Do not use the First-Step Reference on the first attempt. Define what is being counted before calculating.

# A. Recognition only
Write the object and first useful structure. Do not solve.

1. Choose 4 students from 11 for one committee.
2. Assign four distinct offices among 11 students.
3. Select a captain and three ordinary committee members from 10 students.
4. Form a 5-digit even integer from a stated digit set without repetition.
5. Form a 5-digit PIN; leading zero is allowed.
6. Count codes containing at least one A.
7. Count objects satisfying A or B, where overlap may occur.
8. Count alternatives split by last digit 0 versus last digit 5.
9. Count one shirt, one trouser and one pair of shoes.
10. Prove two of 10 integers have the same remainder modulo 9.
11. Prove some box has at least 6 of 41 objects placed in 8 boxes.
12. Sum all non-empty subset products.
13. Find a coefficient in a product of two finite power sums.
14. Find a coefficient in a product of three bounded finite power sums.
15. Count exact 8-step walks on a bounded line.
16. Arrange the letters of MISSISSIPPI.
17. A historical grid-count problem has no retained grid.
18. Direct counting from printed wording disagrees with its supplied key.
19. Count integers satisfying one of three divisibility properties.
20. A signed-power representation has digits `-1,0,1`.
21. Casework rows are not mutually exclusive.
22. A 4-digit integer count includes strings beginning with zero.

# B. First line only
23. Choose 3 from 12, order irrelevant.
24. Award first, second, third among 12.
25. Choose one president and a 2-person committee from 9.
26. Count 4-digit even integers from `0,1,2,3,4` without repetition.
27. Count 6-letter strings over `{A,B,C}` with at least one A.
28. Count integers `1..100` divisible by 2 or 5.
29. Count integers `1..120` divisible by 2,3 or5.
30. Among 14 integers, prove two have same remainder mod 13.
31. 31 objects enter 6 boxes; state the guaranteed occupancy.
32. Sum all non-empty subset products of `{1,3,5}`.
33. Coefficient of `x^9` in `(1+...+x^4)(1+...+x^7)`.
34. Exact 4-move walk on positions `0..3`, start0 end2.
35. Arrange `BALLOON`.
36. Printed wording gives five odd digits and distinct two-digit numbers, while a key claims 12.

# C. Mixed solve / transfer
37. From 10 students choose a 4-person committee.
38. From 10 students choose president, secretary, treasurer.
39. From 10 students choose one captain and a 3-person committee not including the captain.
40. How many 4-digit integers can be formed from digits `0,1,2,3,4,5` without repetition?
41. How many 4-digit even integers can be formed from `0,1,2,3,4,5` without repetition?
42. How many 5-letter strings over `{A,B,C,D}` contain at least one A?
43. How many 5-letter strings over `{A,B,C,D}` contain no A?
44. How many integers `1..180` are divisible by 2 or 3?
45. How many integers `1..180` are divisible by 2, 3 or 5?
46. Among any 17 integers, prove two have the same remainder modulo 16.
47. If 52 objects enter 9 boxes, what occupancy is guaranteed?
48. Sum all non-empty subset products of `{2,4,5}`.
49. Find coefficient of `x^8` in `(1+x+x^2+x^3)(1+x+...+x^6)`.
50. Find coefficient of `x^7` in `(1+x+x^2)(1+x+x^2+x^3)(1+x+...+x^5)`.
51. How many distinct arrangements of `BANANA`?
52. How many distinct arrangements of `BALLOON`?
53. On positions `0..3`, how many 6-move walks start at 0 and end at 2 with ±1 legal moves?
54. On positions `0..4`, how many 6-move walks start at 0 and end at 2?
55. How many 4-digit PINs contain at least one 0?
56. How many 4-digit integers from digits `0..9` have all digits distinct?
57. How many 3-person subsets of `{1,...,12}`?
58. How many ordered triples of distinct elements of `{1,...,12}`?
59. Digits `a0,a1∈{-1,0,1}` encode `a0+3a1`. How many distinct integers result?
60. Digits `a0,a1,a2∈{-1,0,1}` encode `a0+3a1+9a2`. How many distinct integers result?

# D. WHY NOT?
61. “Choose 3 team members from 8” is counted as `8·7·6`. Why not?
62. “President and secretary from 8” is counted as `C(8,2)`. Why not?
63. Two overlapping cases are counted and simply added. Why not?
64. A 4-digit integer count begins with `10` choices for the first digit. Why not?
65. An at-least-one problem is split into many overlapping direct cases even though the complement is one simple case. Why is that risky?
66. A coefficient problem counts all nonnegative solutions of the exponent sum and ignores factor bounds. Why not?
67. A pigeonhole solution states the theorem but never defines the boxes. Why not?
68. A signed-digit problem multiplies the number of digit choices without proving representation uniqueness. Why not?

# E. High-ceiling / state / source judgments
69. On a line with states `0,1,2`, legal moves are to adjacent states only. Write a state recurrence for the number of ways to be at state `j` after `t+1` moves.
70. Explain why raw `2^m` left/right words can overcount or include illegal paths on a bounded line.
71. For digits `a0,a1∈{-1,0,1}`, prove uniqueness of `a0+3a1`.
72. For digits `a0,a1,a2∈{-1,0,1}`, state the largest-smaller-place inequality that supports uniqueness at the `9` place.
73. Exact historical state-grid is missing but answer/solution survives. State the publication status/action.
74. Source wording and supplied key disagree after an independent recount. State the status/action.
