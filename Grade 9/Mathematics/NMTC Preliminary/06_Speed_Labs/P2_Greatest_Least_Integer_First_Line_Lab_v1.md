# P2 Greatest / Least Integer Functions — First-Line Lab v1

Write only the first mathematically useful line, then check against the key.

1. `floor(5.9)`
   - First line: `5<=5.9<6`; answer `5`.

2. `floor(-5.1)`
   - First line: `-6<=-5.1<-5`; answer `-6`.

3. `ceil(-5.1)`
   - First line: `-6<-5.1<=-5`; answer `-5`.

4. Solve `floor(2x+1)=3`.
   - First line: `3<=2x+1<4`; result `1<=x<3/2`.

5. Solve `ceil(3x)=2`.
   - First line: `1<3x<=2`; result `1/3<x<=2/3`.

6. Find `{-11/4}`.
   - First line: `floor(-11/4)=-3`; result `1/4`.

7. If `x` is noninteger, evaluate `floor(x)+floor(-x)`.
   - First line: `ceil(x)=floor(x)+1`; result `-1`.

8. Count integers in `[sqrt2,sqrt50)`.
   - First line: first integer `2`, last integer `7`; count `6`.

9. Count positive integers `n` with `floor(sqrt(n))=4`.
   - First line: `16<=n<25`; count `9`.

10. Solve `floor(x)=ceil(x)`.
    - First line: equality occurs only when `x` is an integer.

11. Prove `floor(x)+floor(x+1/2)=floor(2x)`.
    - First line: set `x=n+r`, `n` integer, `0<=r<1`.

12. A qualified GP problem ends with a floor operation. Classify the evidence.
    - First line: identify the primary mechanism before the final operation; classify as `BRIDGE_EVIDENCE` when GP carries the solution.

## Target

10/12 correct first lines in 5 minutes, with no endpoint-direction or negative-floor error.
