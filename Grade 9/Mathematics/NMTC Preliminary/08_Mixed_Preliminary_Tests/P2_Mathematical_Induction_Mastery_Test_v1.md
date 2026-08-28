# P2 Mathematical Induction — Mixed Mastery Test v1

No method labels are shown in the questions. Write the first-move code before the full solution.

## Questions

1. Prove `1+3+...+(2n-1)=n^2` for `n>=1`.
2. Prove `9 | (10^n-1)` for `n>=1`.
3. Prove `2^n>=n+1` for `n>=0`.
4. A claim is stated only for `n>=5`. A proposed proof begins with `P(1)`. Diagnose and repair the start.
5. Verify `a_n=4*3^(n-1)-1` for `a_1=3`, `a_{n+1}=3a_n+2`.
6. A proof establishes `P(k)->P(k+2)` after checking only `P(2)`. What set of integers can it reach, and what is missing if the claim is for all `n>=1`?
7. Prove `n!>=2^(n-1)` for `n>=1`.
8. A student tries induction on `6 | (n^3-n)`. Give the cheaper proof and explain why it is structurally preferable.
9. Let `a_1=1,a_2=2`, `a_{n+2}=a_{n+1}+2a_n`. Prove `a_n=2^(n-1)`.
10. A polished proof says: “Assume `P(k+1)` is true. Rearranging gives `P(k+1)`, hence by induction...” Identify the logical defect.
11. Prove `3^n>n^2` for every integer `n>=2`.
12. A bank item is tagged `NMTC-BH-P-2024-Q31` but no such source record exists. What is the correct source-integrity disposition?

---

# Solution / review key

## 1
Code `SA`.
Base 1. Assume `S_k=k^2`. Then `S_{k+1}=k^2+(2k+1)=(k+1)^2`.

## 2
Code `DV`.
Base `10-1=9`. `10^(k+1)-1=10(10^k-1)+9`.

## 3
Code `IQ`.
Base 0. `2^(k+1)>=2(k+1)>=k+2`.

## 4
Code `BC/BR`.
Correct base is `P(5)`. Testing `P(1)` does not start the required chain.

## 5
Code `RC`.
Base: `4-1=3`. Assume `a_k=4*3^(k-1)-1`; then `a_{k+1}=3a_k+2=12*3^(k-1)-1=4*3^k-1`.

## 6
Code `BR`.
From `P(2)` with step +2, the proof reaches even integers `2,4,6,...`. For all `n>=1`, an odd-chain base such as `P(1)` is also required.

## 7
Code `IQ`.
Base 1. `(k+1)!=(k+1)k!>=(k+1)2^(k-1)>=2^k`.

## 8
Code `DP`.
`n^3-n=n(n-1)(n+1)`, product of three consecutive integers; divisible by 2 and 3, hence 6. It exposes the invariant immediately without an unnecessary recursive proof.

## 9
Code `SI` / two-base induction.
Bases n=1,2. Assume consecutive formulas. Then `a_{k+2}=2^k+2*2^(k-1)=2^(k+1)`.

## 10
Code `BR`.
The proof assumes the very next case it is supposed to prove; it is circular and does not use `P(k)->P(k+1)`.

## 11
Code `IQ`.
Base n=2. From `3^k>k^2`, get `3^(k+1)>3k^2`; for `k>=2`, `3k^2>(k+1)^2`.

## 12
Code `QC`.
Remove/freeze the fabricated historical attribution; retain the item only as author-created until a valid source record exists.

---

# Diagnostic bands

- 11–12 correct with valid first moves: mastery
- 8–10: targeted repair
- 5–7: concept revisit
- <=4: foundation proof-language rebuild

Required qualitative checks:

- no circular hypothesis;
- correct start index;
- step reaches the exact `k+1` target;
- step-size coverage complete;
- source labels not fabricated.
