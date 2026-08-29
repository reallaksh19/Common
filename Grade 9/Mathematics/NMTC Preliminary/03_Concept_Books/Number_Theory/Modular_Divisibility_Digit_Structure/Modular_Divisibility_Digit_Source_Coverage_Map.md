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

### Successive quotient/remainder reconstruction

- `NMTC-BH-P-2024-Q20` — **successive division**, not simultaneous congruences. The number is divided by 5, then the resulting quotient by 6, then the next quotient by 7, with remainders 3,2,2 respectively. Reconstructing backward gives `N = 5(6(7q+2)+2)+3`, hence `N ≡ 43 (mod 120)`.

**Custody correction:** an earlier qualification/source-map summary flattened Q20 into `N≡3 (mod5), N≡2 (mod6), N≡2 (mod7)`. That interpretation is mathematically incompatible with answer 43 and is superseded. Q20 must not be used as a clean CRT/simultaneous-congruence anchor.

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

- `NMTC-BH-P-2023-Q12` has a corrupted searchable statement. The recovered solution indicates a modulo-4 parity/residue mechanism, but the exact question is **not** a canonical student anchor until the original wording is recovered.

## Upstream ledger note

The repository's 2024 qualification ledger currently summarizes Q20 as three simultaneous congruences while also retaining answer 43. The exact source wording establishes successive quotient/remainder division instead. Issue #47 treats the topic coverage correction in this file as authoritative for teaching custody; the global qualification-ledger summary should be corrected separately when that upstream authority file is next revised.

## Coverage conclusion

The five-year evidence supports a connected Number Theory package with the following homes:

1. remainder language and congruence operations;
2. cycles and power residues;
3. same-remainder LCM vs GCD contrast;
4. successive quotient/remainder reconstruction, with generic simultaneous congruences supplied as author-created foundation pending a clean historical anchor;
5. place-value and divisibility tests;
6. integer-valued rational/divisor reduction;
7. factor-pair parity and coprime restrictions;
8. prefix-residue and multiplicative-order ceiling bridges;
9. source-integrity checking.

Do not describe the frequency or item counts as official AMTI weightage.