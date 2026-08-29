# P2 Greatest / Least Integer Functions — Mixed Mastery Test v1

No chapter labels or first-move hints are shown.

## Questions

1. Solve `floor((2x-1)/3)=-2`.

2. Solve `ceil((1-x)/2)=3`.

3. Solve `floor(x)+ceil(x)=7`.

4. Solve `floor(x)=floor(-x)`.

5. How many real numbers of the form `n+2/3`, with integer `n`, lie in `(-3,2]`?

6. How many positive integers `n` satisfy `floor(sqrt(2n))=5`?

7. How many integers `x` satisfy `ceil(x/4)=3`?

8. Characterize all real `x` satisfying `floor(2x)=2floor(x)`.

9. Prove

`floor(x)+floor(x+1/3)+floor(x+2/3)=floor(3x)`.

10. Evaluate `floor(x)+floor(1-x)` separately for integer and noninteger `x`.

11. How many positive multiples of 7 are at most 100? Express the first move using floor notation.

12. A source-qualified Previous-Year problem is primarily an infinite-GP problem but its final instruction is to take the floor of the resulting real number. Should it be included as evidence that Greatest Integer Function is a recurrent PYQ mechanism? Explain.

---

# Answer key / audit

## 1
`-2<=(2x-1)/3<-1`.

`-6<=2x-1<-3`.

`-5<=2x<-2`.

**Answer:** `-5/2<=x<-1`.

## 2
`2<(1-x)/2<=3`.

`4<1-x<=6`.

**Answer:** `-5<=x<-3`.

## 3
If `x` is integer, sum is `2x`, never 7.

If noninteger, `ceil(x)=floor(x)+1`.

So `2floor(x)+1=7`, hence `floor(x)=3`.

**Answer:** `3<x<4`.

## 4
If `x` is integer, equation gives `x=-x`, so `x=0`.

If noninteger, `floor(-x)=-floor(x)-1`, impossible to equal `floor(x)`.

**Answer:** `x=0`.

## 5
`x=n+2/3` and `-3<x<=2`.

This gives `n=-3,-2,-1,0,1`.

**Answer:** `5`.

## 6
`5<=sqrt(2n)<6`.

`25<=2n<36`.

**Answer:** `n=13,14,15,16,17`, so `5`.

## 7
`2<x/4<=3`.

`8<x<=12`.

**Answer:** `9,10,11,12`, so `4`.

## 8
Write `x=n+r`, `0<=r<1`.

`floor(2x)=2n+floor(2r)`.

Equality with `2floor(x)=2n` requires `floor(2r)=0`.

**Answer:** `{x}<1/2`.

## 9
Write `x=n+r`, `0<=r<1` and split at `r=1/3,2/3`.

The extra floors on the left are respectively `0,1,2`, exactly matching `floor(3r)`.

**Identity proved.**

## 10
If `x=n` is integer:

`floor(x)+floor(1-x)=n+(1-n)=1`.

If `x=n+r`, `0<r<1`:

`floor(1-x)=floor(1-n-r)=-n`.

**Answer:** `1` for integer `x`; `0` otherwise.

## 11
Count is

`floor(100/7)=14`.

## 12
**No.** It is valid `BRIDGE_EVIDENCE` for applying floor after another mechanism. Its primary mechanism remains GP, so using it to claim a recurrent Greatest Integer Function PYQ family would inflate the evidence.

---

# Mastery target

- 10/12 correct;
- Questions 1–2 must have correct endpoint orientation;
- Questions 3–4 must separate integer/noninteger cases;
- Question 8 must use fractional-part reasoning;
- Question 12 must preserve the source-evidence boundary.
