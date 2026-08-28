# P1 Combinatorics — First-Line Lab v1

Write only the first useful mathematical line/setup. Do not complete the calculation.

Target: 12 items in 10 minutes.

1. Choose a 5-person team from 11 students.
2. Choose captain, vice-captain and secretary from 11 students.
3. Count 4-digit even numbers from digits `0,1,2,3,4,5` without repetition.
4. Count length-6 strings over `{A,B,C}` containing at least one C.
5. Count integers in `1..500` divisible by 6 or 10.
6. Among 17 integers, prove two have same remainder modulo 16.
7. Sum products of all non-empty subsets of `{a,b,c,d}`.
8. Find coefficient of `x^15` in `(1+x+...+x^8)(1+x+...+x^10)`.
9. Count 6-step walks on a graph from start S to target T.
10. Count 3-element subsets of `{1,...,8}` with odd sum.
11. Count arrangements of ABCDEF where A and B are adjacent.
12. A printed two-digit odd-digit problem yields 20 directly, key says 12.

## Acceptable first lines

1. `C(11,5)`.
2. `11*10*9`.
3. `Case units=0; Case units in {2,4}` before multiplying.
4. `3^6-2^6`.
5. `floor(500/6)+floor(500/10)-floor(500/lcm(6,10))`.
6. `17 pigeons -> 16 residue boxes {0,...,15}`.
7. `(1+a)(1+b)(1+c)(1+d)-1`.
8. `count (i,j): i+j=15, 0<=i<=8, 0<=j<=10`.
9. define `C_t(v)=# ways to be at vertex v after t moves`.
10. classify by number of odd selected elements; odd sum means 1 or 3 odds.
11. treat `AB`/`BA` as one block; setup `5!*2`.
12. independently define printed sample space; mark `SOURCE_KEY_CONFLICT` if mismatch survives.
