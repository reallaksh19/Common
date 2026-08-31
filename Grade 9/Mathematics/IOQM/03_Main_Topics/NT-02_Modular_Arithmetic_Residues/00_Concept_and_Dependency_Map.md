# IOQM Grade 9 - NT-02 Modular Arithmetic, Residues & Power Cycles

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Learner entry model

Assume the learner owns NT-01 divisibility meaning and can compute gcd when needed. The missing bridge is to treat a remainder class as a state, operate on that state legally, and recognize when powers repeat instead of expanding.

## Governing router

`TARGET MODULUS -> REDUCE STATE -> LEGAL OPERATIONS -> CYCLE / SIMULTANEOUS STRUCTURE -> CHECK`

Before calculating:
1. What modulus is actually relevant?
2. Can I replace large numbers by residues now?
3. Is the operation legal under congruence?
4. If cancelling, is the cancelled factor invertible modulo the modulus?
5. Do powers repeat in a short cycle?
6. Are several congruences compatible, and what period do their solutions repeat with?

## Dependency map

| Concept | Tag/disposition |
|---|---|
| `m|(a-b)` and gcd meaning | `PREREQUISITE_RETRIEVAL_ONLY` from NT-01 |
| congruence notation/meaning | `IOQM_BRIDGE`, NT-02 owner |
| legal addition/subtraction/multiplication/powers | NT-02 owner |
| inverse existence and cancellation legality | NT-02 owner; retrieve gcd test only |
| power cycles / last digits | NT-02 owner |
| simultaneous congruences at Grade-9 depth | NT-02 owner |
| prime-exponent/divisor-count theory | deferred to NT-03 |
| place-value/digit canon | deferred to NT-05; residues may be applied |

## Method-selection map

| Similar surface | Route A | Route B | Boundary question | First line |
|---|---|---|---|---|
| equality vs congruence | exact same integer | same residue class | Must values be identical or only differ by a multiple of m? | `a-b = km` |
| divisibility vs congruence | `m|N` | `a congruent b (mod m)` | Is one expression compared with zero or two expressions compared by remainder? | rewrite difference |
| huge power | direct expansion | power cycle | Does the residue repeat after a few powers? | list first residues |
| cancellation | divide both sides | multiply by inverse | Is gcd(factor,m)=1? | test invertibility |
| last digit vs last two digits | mod 10 | mod 100 | How many terminal decimal digits matter? | choose modulus |
| two congruences | independent lists | combine compatible cycles | Do solution lists intersect; what is lcm period? | parametrize one class |

## Required contrasts

1. equality vs congruence;
2. divisibility vs congruence;
3. brute-force powers vs power cycle;
4. legal vs illegal modular cancellation;
5. mod 10 vs mod 100 target;
6. residue reduction before vs after expansion;
7. inverse exists vs no inverse;
8. compatible vs incompatible simultaneous congruences;
9. base-period vs exponent-period in `n^n`-type problems.

## Transfer map

- T2: divisibility difference statement -> congruence notation.
- T2: huge integer power -> short finite residue state.
- T3: last-digit / clock / cyclic schedule surfaces.
- T3: simultaneous schedules -> simultaneous congruences.
- T4: residues become invariant states in COMB-04 and digit filters in NT-05.

## Stable prerequisite consumption

NT-01 is retrieved only for: `m|(a-b)`, gcd meaning, and the fact that gcd detects invertibility eligibility. No Euclidean/gcd/lcm teaching sequence is repeated here.
