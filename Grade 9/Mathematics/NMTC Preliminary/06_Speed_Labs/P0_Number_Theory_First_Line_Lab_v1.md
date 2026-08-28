# P0 Number Theory — First-Line Lab v1

Write the **first useful mathematical line only**. Do not complete the solution. Suggested internal target: 12 items in 8 minutes; not an official NMTC timing claim.

1. Largest `N<5000` leaving remainder 7 under division by 12,18,30.
2. Greatest divisor leaving the same remainder on 84,129,174.
3. Last digit of `3^2026`.
4. Least `N>0` satisfying `N≡3 mod4`, `N≡2 mod5`.
5. A two-digit number has digits `a,b`; its reversal is 36 larger.
6. Count three-digit numbers `a5b` divisible by 9.
7. `(n+13)/(n+4)` is an integer for positive integer `n`.
8. Positive `k>n` satisfy `k^2-n^2=72`.
9. Coprime positive `a,b` have `ab=1764`, a perfect square.
10. Count consecutive blocks of `a1,...,a20` whose sums are divisible by 7.
11. An odd prime `p` divides `5^8+1`.
12. A reproduced PYQ has unreadable superscript notation but a secondary solution claims a mod-4 answer.

## Reference first lines

1. `N-7` is divisible by `lcm(12,18,30)`.
2. `d | (129-84), (174-129), (174-84)`.
3. Work modulo 10: `3^n` has cycle `3,9,7,1`.
4. `N=3+4k`; impose `3+4k≡2 (mod5)`.
5. `(10b+a)-(10a+b)=36`, so `9(b-a)=36`.
6. `a+5+b≡0 (mod9)` with `a∈{1,...,9}`, `b∈{0,...,9}`.
7. `(n+13)/(n+4)=1+9/(n+4)`.
8. `(k-n)(k+n)=72`, with the two factors of the same parity.
9. `1764=2^2·3^2·7^2`; coprimality forces each prime-square block wholly into one factor.
10. Define prefix sums `S0=0,Sj=a1+...+aj`; require `Sj≡Si (mod7)`.
11. `5^8≡-1 (modp)` implies `5^16≡1 (modp)` but `5^8≠1 (modp)`.
12. `TRANSCRIPTION_SUSPECT`; do not reconstruct missing notation from the claimed answer.

## Pass rule

At least 10/12 first lines structurally correct, with items 1 vs 2 distinguished and item 12 source-safe.