# P0 Algebra — Inequalities / Bounds First-Line Lab v1

## Purpose

Write only the first mathematically useful line. Do not finish the problem.

Suggested internal target: 12 items in 8 minutes after recognition mastery. Not an official NMTC timing claim.

## Student sheet

### Q1
Positive `a,b` satisfy `ab=25`. Find the minimum of `a+b`.

### Q2
Positive `a,b` satisfy `ab=1`. Find the maximum of `a+b`.

### Q3
Positive `x,y` satisfy `4/x+9/y=1`. Find the least `x+y`.

### Q4
Find the minimum of `x^2-10x+29`.

### Q5
Real `p,q` satisfy `(p+2)^2+(q-5)^2=0`. Find `p+q`.

### Q6
For what `m` does `x^2+mx+12=0` have real roots?

### Q7
Solve `|x-4|<7`.

### Q8
Solve `(x-2)/(x+5)>=0`.

### Q9
How many integers satisfy `2/|x-9|>1`?

### Q10
Find maximum of `6-5cos t`.

### Q11
Positive integers `a,b` satisfy `a+b=9`. Find maximum `ab`.

### Q12
A key says the maximum of `a+b`, `ab=4`, is 4.

## First-line key

### Q1
`a+b >= 2sqrt(ab)=10`, equality candidate `a=b=5`.

### Q2
`Set a=t, b=1/t; test t->infinity before applying AM-GM.`

### Q3
`4/x+9/y >= (2+3)^2/(x+y)=25/(x+y)`.

### Q4
`x^2-10x+29=(x-5)^2+4`.

### Q5
`Both squares are non-negative and sum to 0, so p+2=0 and q-5=0.`

### Q6
`D=m^2-48 >=0`.

### Q7
`-7 < x-4 < 7`.

### Q8
`Critical points are -5 (excluded) and 2; make a sign chart.`

### Q9
`Domain x!=9; 2/|x-9|>1 -> |x-9|<2.`

### Q10
`-1<=cos t<=1`, so inspect `6-5cos t` at the lower cosine bound for the maximum.

### Q11
`ab <= ((a+b)/2)^2=81/4`, but equality `a=b=4.5` is not integer-feasible.

### Q12
`Solve the printed constraint independently: set a=t, b=4/t and test boundedness; do not force the key.`

## Error tags

- `BOUND_DIRECTION_WRONG`
- `BOUNDEDNESS_NOT_TESTED`
- `CAUCHY_STRUCTURE_MISSED`
- `SQUARE_NOT_COMPLETED`
- `ZERO_SUM_SQUARE_NOT_COLLAPSED`
- `DISCRIMINANT_NOT_USED`
- `ABSOLUTE_DISTANCE_MISREAD`
- `RATIONAL_CRITICAL_POINT_MISSED`
- `DENOMINATOR_DOMAIN_MISSED`
- `DIRECT_BOUND_DIRECTION_WRONG`
- `EQUALITY_FEASIBILITY_NOT_CHECKED`
- `SOURCE_KEY_FORCED`
