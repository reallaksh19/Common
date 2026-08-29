# Greatest / Least Integer Functions — Student Draft v0.1

## Goal

Learn to see floor and ceiling as **interval operators**, not strange brackets.

Use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

and while solving:

`TRANSLATE -> SOLVE -> CHECK ENDPOINTS -> TRANSFER`.

---

# 0. Diagnostic

1. Which integers lie in `[-2.4,1.7)`?
2. Is `-2>-3`?
3. Solve `3<=2x+1<5`.
4. What is the greatest integer less than or equal to `4.8`?
5. What is the greatest integer less than or equal to `-1.2`?

Answers: `-2,-1,0,1`; yes; `1<=x<2`; `4`; `-2`.

If Q5 felt surprising, pay special attention to negative inputs.

---

# 1. Floor is not truncation

`floor(x)` means the greatest integer `<=x`.

Examples:

- `floor(3.7)=3`;
- `floor(3)=3`;
- `floor(-1.2)=-2`;
- `floor(-4)=-4`.

Why `floor(-1.2)=-2`? Because `-1` is **greater** than `-1.2`, so it is not allowed. The greatest integer that is still `<=-1.2` is `-2`.

### First move

Never “remove the decimal digits.” Locate the number between consecutive integers.

---

# 2. Ceiling

`ceil(x)` means the least integer `>=x`.

Examples:

- `ceil(3.2)=4`;
- `ceil(3)=3`;
- `ceil(-1.2)=-1`;
- `ceil(-4)=-4`.

Notice the asymmetry for negative non-integers:

`floor(-1.2)=-2`, while `ceil(-1.2)=-1`.

---

# 3. The two master translations

If `m` is an integer,

`floor(x)=m` exactly when

`m<=x<m+1`.

Similarly,

`ceil(x)=m` exactly when

`m-1<x<=m`.

Everything about the step graphs follows from these intervals.

### Worked example

Solve `floor(2x+1)=5`.

Translate first:

`5<=2x+1<6`.

So

`4<=2x<5`, hence

`2<=x<5/2`.

### Ceiling example

Solve `ceil(3x-2)=4`.

`3<3x-2<=4`.

Thus

`5<3x<=6`, so

`5/3<x<=2`.

The endpoint pattern is part of the mathematics.

---

# 4. Integer shifts

Let `n` be an integer. Shifting by `n` simply shifts the floor/ceiling value:

`floor(x+n)=floor(x)+n`,

`ceil(x+n)=ceil(x)+n`.

Why? If `m<=x<m+1`, then

`m+n<=x+n<m+n+1`.

So the new floor is `m+n`.

---

# 5. Reflection

A very useful identity is

`ceil(x)=-floor(-x)`.

Example with `x=2.3`:

`ceil(2.3)=3`, and `-floor(-2.3)=-(-3)=3`.

This lets you convert many ceiling problems into floor problems.

A related fact:

`floor(x)+floor(-x)` equals

- `0` if `x` is an integer;
- `-1` otherwise.

Do not state `floor(x)+floor(-x)=-1` without checking the integer case.

---

# 6. Fractional part

Define

`{x}=x-floor(x)`.

Then always

`0<={x}<1`.

Write

`x=n+r`,

where `n=floor(x)` is an integer and `0<=r<1`.

This is the most useful representation in the chapter.

### Negative example

`x=-1.3`.

`floor(x)=-2`, so

`{x}=-1.3-(-2)=0.7`.

Fractional part is never negative.

---

# 7. Floor inequalities

Let `m` be an integer.

`floor(y)>=m` means `y>=m`.

`floor(y)<=m` means `y<m+1`.

Examples:

`floor(2x-1)>=3`

becomes

`2x-1>=3`, so `x>=2`.

But

`floor(2x-1)<=3`

becomes

`2x-1<4`, so `x<5/2`.

Notice the strict inequality in the second result.

For ceilings:

`ceil(y)<=m <=> y<=m`,

`ceil(y)>=m <=> y>m-1`.

---

# 8. When x itself appears

Suppose

`x+floor(x)=7/2`.

Set `n=floor(x)`. Then `n<=x<n+1` and

`x=7/2-n`.

Require

`n<=7/2-n<n+1`.

First inequality:

`2n<=7/2`, so `n<=1`.

Second:

`7/2<2n+1`, so `n>5/4`.

Thus no integer `n` satisfies both. Therefore the equation has no real solution.

The important lesson is not the answer. It is the method:

`set n=floor(x) -> solve -> enforce n<=x<n+1`.

---

# 9. Nested floor and ceiling

Because `floor(x)` is already an integer,

`floor(floor(x))=floor(x)`

and

`ceil(floor(x))=floor(x)`.

Similarly,

`ceil(ceil(x))=ceil(x)`

and

`floor(ceil(x))=ceil(x)`.

The outer operator does nothing to an integer.

---

# 10. A useful doubling identity

Show that

`floor(x)+floor(x+1/2)=floor(2x)`.

Write `x=n+r`, `0<=r<1`.

Left side:

`n + n + floor(r+1/2)`.

If `r<1/2`, extra term is 0.

If `r>=1/2`, extra term is 1.

Meanwhile `floor(2x)=2n+floor(2r)`, and `floor(2r)` has exactly the same 0/1 split.

So the identity follows.

This is a model for many floor identities: reduce everything to the fractional part.

---

# 11. Floor of a sum

Write

`x=a+r`, `y=b+s`,

where `a=floor(x)`, `b=floor(y)`, and `0<=r,s<1`.

Then

`floor(x+y)=a+b+floor(r+s)`.

Since `0<=r+s<2`, `floor(r+s)` is either 0 or 1.

Therefore

`floor(x)+floor(y) <= floor(x+y) <= floor(x)+floor(y)+1`.

The extra 1 appears exactly when `{x}+{y}>=1`.

---

# 12. Counting integers in an interval

How many integers lie in `[a,b]`?

The first allowed integer is `ceil(a)`.

The last allowed integer is `floor(b)`.

So, when the interval is nonempty, the count is

`floor(b)-ceil(a)+1`.

### Example

Integers in `[-2.4,5.1]` run from `-2` to `5`.

Count:

`5-(-2)+1=8`.

For open endpoints, first decide whether an endpoint integer itself is excluded before applying the same idea.

---

# 13. Square-root intervals

Suppose `floor(sqrt(n))=7` for positive integer `n`.

Then

`7<=sqrt(n)<8`.

Square:

`49<=n<64`.

So integer `n` can be any of `49,50,...,63`, giving 15 possibilities.

This is a common transfer pattern:

`floor of expression -> interval -> algebra -> integer count`.

---

# 14. Complete groups and minimum groups

If 53 students are placed in groups of at most 8, the minimum number of groups is

`ceil(53/8)=7`.

If instead you ask how many **complete** groups of 8 can be formed, the answer is

`floor(53/8)=6`.

Floor and ceiling often encode quotient/remainder ideas.

---

# 15. Bridge evidence vs primary mechanism

A qualified 2024 Preliminary GP problem eventually asks for the floor of a computed quantity. That is legitimate evidence that students should be comfortable applying floor after another method.

But the main work of that problem is infinite GP, not Greatest Integer Function reasoning.

So it is a **bridge**, not proof of a recurrent floor-function PYQ family.

This distinction matters whenever we use previous-year evidence.

---

# 16. Error laboratory

Decide whether each statement is always true.

1. `floor(x+y)=floor(x)+floor(y)`.
2. `floor(2x)=2floor(x)`.
3. `ceil(x)=-floor(-x)`.
4. `{x}` is the decimal part of `x` obtained by truncation.
5. `floor(x)=x` exactly when `x` is an integer.

Answers:

1. No.
2. No.
3. Yes.
4. No, especially for negative numbers.
5. Yes.

---

# 17. ADOPT set

1. Solve `floor(3x-2)=4`.
2. Solve `ceil(2x+1)=-1`.
3. Find `{ -7/3 }`.
4. Solve `floor(sqrt(x))=5` for real `x>=0`.
5. Count integers in `(-3.2,7.8]`.
6. Evaluate `floor(2.7)+floor(-2.7)`.
7. Prove `floor(x)+floor(x+1/2)=floor(2x)`.
8. Decide when `floor(x)+floor(y)=floor(x+y)`.

Answers:

1. `2<=x<7/3`.
2. `-2<2x+1<=-1`, so `-3/2<x<=-1`.
3. `2/3`.
4. `25<=x<36`.
5. integers `-3` through `7`: 11.
6. `2+(-3)=-1`.
7. Use `x=n+r`, `0<=r<1`, split at `r=1/2`.
8. Exactly when `{x}+{y}<1`.

## Mastery signal

You are ready for mixed use when you stop asking “what does this bracket mean?” and automatically ask:

> Which interval does this floor or ceiling statement encode, and which endpoints survive?
