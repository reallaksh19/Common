# P0 Algebra — Radical / Exponent / Log Recognition Lab v1

## Purpose

Train the Preliminary bottleneck: **identify the useful representation before calculating**.

All items are `AUTHOR_CREATED_FOUNDATION` or `AUTHOR_CREATED_TRANSFER`. None is an NMTC PYQ.

Suggested training protocol:

- 20 items;
- 12 seconds per item on first pass;
- write only the recognition code;
- no calculation during Round A.

This timing is an internal practice target, not an official NMTC claim.

## Recognition codes

- `CB` — common radical/exponent basis
- `HS` — hidden square / hidden surd reconstruction
- `RI` — reciprocal invariant such as `t+1/t`
- `RE` — radical equation; isolate then transform with domain check
- `EN` — exponential normalization to one base/variable
- `LS` — logarithmic substitution
- `LI` — logarithm-to-algebra inverse relation
- `DR` — domain/reversibility check before accepting transformed roots
- `QC` — source/statement consistency check

---

# Round A — recognize only

For each item, write the best code. Do not solve.

1. Simplify `(sqrt(50)+sqrt(8))/sqrt(2)`.
2. Simplify `sqrt(11+6sqrt(2))`.
3. If `u+1/u=5`, find `u^4+1/u^4`.
4. Solve `sqrt(x+5)=2sqrt(x-1)`.
5. Solve `27^x=9^(x+1)`.
6. Solve `4^x-7·2^x+12=0`.
7. Solve `(log_3 x)^2-5log_3 x+6=0`.
8. Solve `log_2 x-5sqrt(log_2 x)+6=0`.
9. Positive `x,y` satisfy `log_4 x=log_2 y` and another algebraic relation.
10. Evaluate exactly `16^(log_2 3)`.
11. Simplify `cuberoot(16)+cuberoot(54)-cuberoot(2)`.
12. Simplify `sqrt(17-4sqrt(15))`.
13. Let `z=(sqrt7+sqrt3)/(sqrt7-sqrt3)`; find `z+1/z`.
14. Solve `25^x-6·5^x+5=0`.
15. Solve `(log_5 x)^2=1`.
16. Solve `sqrt(x+9)=x-3`.
17. A solution obtained after squaring does not satisfy the original radical equation. What type of issue is this?
18. A printed problem uses `sqrt(a^2)=a` although `a` is not stated positive. What should you notice first?
19. A key says `x=4`, but substituting into the printed logarithmic equation makes a log argument non-positive. What is the first action?
20. `8^(log_2 5)` appears. What structural move should be tested before numerical approximation?

---

# Answer key

1. `CB`
2. `HS`
3. `RI`
4. `RE`
5. `EN`
6. `EN`
7. `LS`
8. `LS`
9. `LI`
10. `LI`
11. `CB`
12. `HS`
13. `RI`
14. `EN`
15. `LS`
16. `RE` + `DR`
17. `DR`
18. `DR` — principal-root sign: `sqrt(a^2)=|a|`
19. `QC` + `DR`
20. `LI` / exponent-log inverse structure

---

# Diagnostic interpretation

## 18–20 correct

`RECOGNITION_READY`

Proceed to First-Line Lab.

## 14–17 correct

`RECOGNITION_PARTIAL`

Repeat only the missed families, then retest with shuffled items.

## <=13 correct

`REPRESENTATION_GAP`

Return to the Concept Book sections for common basis, hidden surds, exponential normalization and log substitution before doing more full solutions.

## Error tags

- `COMMON_BASIS_NOT_FOUND`
- `HIDDEN_SURD_NOT_RECONSTRUCTED`
- `RECIPROCAL_INVARIANT_MISSED`
- `RADICAL_DOMAIN_NOT_NOTICED`
- `EXPONENTIAL_BASES_NOT_NORMALIZED`
- `WRONG_LOG_SUBSTITUTION_OBJECT`
- `LOG_TO_ALGEBRA_LINK_MISSED`
- `PRINCIPAL_ROOT_SIGN_ERROR`
- `SOURCE_CONFLICT_NOT_FLAGGED`

## Review status

`MATH_REVIEW: PASS_v1`

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`
