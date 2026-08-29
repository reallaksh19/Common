# Modular / Divisibility / Digit Structure — Source Coverage Map

## Authority rule

Only the solution-qualified Bhaskara Preliminary corpus may define PYQ grounding. Author-created examples remain explicitly separate.

## Clean scored anchors by mechanism

### Remainder compression / cycles

- `NMTC-BH-P-2018-Q29` — last-digit cycle of a power.
- `NMTC-BH-P-2025-Q13` — square a known residue modulo 11.
- `NMTC-BH-P-2019-Q26` — high-ceiling prime-divisor filtering through multiplicative order.

### Same remainder — two different structures

- `NMTC-BH-P-2025-Q01` — same remainder under several divisors: subtract the residue, then use LCM.
- `NMTC-BH-P-2024-Q21` — greatest divisor leaving the same remainder on several numbers: take pairwise differences, then GCD.

These two must be taught as a contrast pair.

### Simultaneous congruences

No exact clean historical anchor is currently frozen for the generic CRT-style interface. This mechanism remains required by Issue #47 and is taught with `AUTHOR_CREATED_FOUNDATION` / `AUTHOR_CREATED_TRANSFER` until a qualified exact anchor is identified.

### Digit / place-value structure

- `NMTC-BH-P-2018-Q28` — encode a two-digit number and its reversal.
- `NMTC-BH-P-2019-Q01` — `ABCABC=1001·ABC`; place-value factorization makes divisibility visible.
- `NMTC-BH-P-2019-Q16` — encode a number through quotient/remainder/digit conditions.
- `NMTC-BH-P-2019-Q17` — digit sum plus algebraic relation.
- `NMTC-BH-P-2025-Q14` — encode two-digit numbers directly from digit relations.
- `NMTC-BH-P-2025-Q21` — count digit choices using divisibility by 9.

### Integer-valued / factor-divisor constraints

- `NMTC-BH-P-2018-Q10` — coprimality converts a rational condition into divisor restrictions.
- `NMTC-BH-P-2018-Q18` — difference-of-squares factorization plus the same-parity condition on `(k-n),(k+n)`.
- `NMTC-BH-P-2018-Q19` — integrality/perfect-square restriction after algebraic reduction.
- `NMTC-BH-P-2019-Q27` — factor a difference of squares and combine divisibility with bounds.
- `NMTC-BH-P-2025-Q26` — substitution `t=2n-1` converts integrality to `t | 25`.

### Prefix residues / attainable totals / representation ceiling

- `NMTC-BH-P-2019-Q06` — divisible consecutive-block sums via equal prefix residues modulo 11.
- `NMTC-BH-P-2019-Q14` — score attainability through congruence restrictions.
- `NMTC-BH-P-2019-Q28` — balanced ternary; high-ceiling canonical representation/counting bridge.

### Coprime perfect-power structure

- `NMTC-BH-P-2023-Q18` — if the product of coprime consecutive positive integers is a square, each factor must itself be a square; no positive consecutive square pair exists.

## Source-sensitive / blocked evidence

### `NMTC-BH-P-2023-Q12`

- searchable statement is corrupted;
- recovered solution indicates a modulo-4 parity/residue mechanism;
- exact question is **not** a canonical student anchor until original wording is recovered.

Disposition: `SOURCE_SENSITIVE_EVIDENCE — BLOCKED_EXACT_ANCHOR`.

### `NMTC-BH-P-2024-Q20`

The reproduced stem says Simon was asked to divide a number by 120 and “divided the number by 5, 6 and 7 and got 3, 2 and 2 as remainders respectively.” The 2024 answer key records `43*`.

A published worked solution interprets the wording as **successive quotient division**:

`N=5q1+3`, `q1=6q2+2`, `q2=7q3+2`,

which gives `N=210q3+73`. It then chooses `q3=1` on the unstated assumption that `N>120`, yielding `N=283` and remainder 43 modulo 120.

This is not a clean simultaneous-congruence item, and the step forcing `q3=1` is not justified by the reproduced stem. Therefore Q20 is demoted for Issue #47 to:

`SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`.

Allowed use: source-QC / representation-boundary discussion only.  
Forbidden use: clean CRT anchor or canonical solved student exercise.

## Upstream ledger note

The repository's 2024 qualification ledger currently summarizes Q20 as three simultaneous congruences while also retaining answer 43. That summary is mathematically inconsistent. Issue #47 source custody supersedes that row for teaching use; the global qualification-ledger summary remains an upstream correction debt.

## Coverage conclusion

The five-year evidence supports a connected Number Theory package with the following homes:

1. remainder language and congruence operations;
2. cycles and power residues;
3. same-remainder LCM vs GCD contrast;
4. simultaneous congruence reconstruction as author-created foundation pending a clean historical anchor;
5. place-value and divisibility tests;
6. integer-valued rational/divisor reduction;
7. factor-pair parity and coprime restrictions;
8. prefix-residue and multiplicative-order ceiling bridges;
9. source-integrity checking, including 2023 Q12 and 2024 Q20.

Do not describe the frequency or item counts as official AMTI weightage.