# Number Theory Question-Driven Study Guide Profile v3

Status: `PHASE1_PR140_FOUNDATION_FROZEN`

## Learner objective

Teach a roughly 50%-prepared Grade 9 learner to move from:

**wording -> arithmetic structure -> legal representation -> cheapest method -> first line -> execution -> boundary check.**

The learner may remember divisibility tests and routine modular patterns but may not reliably distinguish nearby methods or remember theorem hypotheses.

## Stable skill families

- `NT-DIV-01 · Divisibility and the Division Algorithm`
- `NT-GCD-01 · Euclidean Algorithm, GCD and LCM`
- `NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking`
- `NT-DIVCNT-01 · Exponent vectors and divisor functions`
- `NT-DIO-LIN-01 · Bezout and linear Diophantine equations`
- `NT-MOD-01 · Congruence arithmetic and cancellation legality`
- `NT-MODINV-01 · Linear congruences and modular inverses`
- `NT-CRT-01 · Constructive CRT, including non-coprime moduli`
- `NT-ORDER-01 · Short residue cycles and multiplicative order`
- `NT-EULER-01 · Fermat, Euler and Euler phi`
- `NT-WILSON-01 · Wilson's theorem`
- `NT-LASTDIG-01 · Last digits by prime-power splitting and CRT`
- `NT-EXPGCD-01 · GCDs of exponential expressions`
- `NT-VAL-01 · Valuations and Legendre's formula`
- `NT-ZEROS-01 · Trailing zeros and last nonzero digits`
- `NT-POWER-01 · Perfect powers and squarefree structure`
- `NT-RESIDUE-01 · Reduced residues, phi sums and unit products`
- `NT-FACT-01 · Factorisation engines for integer equations`
- `NT-FACT-POW-01 · Difference/sum-of-powers factorisation`
- `NT-FACT-SFFT-01 · Manufactured factorisation and fixed-product forms`
- `NT-FACT-POLY-01 · Polynomial-to-consecutive-factor factorisation`
- `NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters`
- `NT-GCDNORM-01 · GCD/LCM normalisation`
- `NT-PYTH-01 · Primitive Pythagorean triples`
- `NT-CONSUM-01 · Consecutive sums and odd-divisor structure`
- `NT-DIGIT-01 · Decimal place value, concatenation and deletion`
- `NT-BASE-01 · Other bases and digit validity`
- `NT-DIGSUM-01 · Digit-sum congruence and bounded digit sums`
- `NT-CARRY-01 · Exact carry accounting`
- `NT-FLOOR-01 · Floor functions as half-open intervals`
- `NT-REC-01 · Affine recurrences modulo a target`
- `NT-WINDOW-01 · Overlapping-window cancellation`
- `NT-COUNT-01 · Fixed-multiplicity and digit-choice counting`
- `NT-PIGEON-01 · Small-prime / residue-class obstruction`
- `NT-SQUAREGAP-01 · Monotone square-gap extremal reasoning`
- `NT-PRIMEGRAPH-01 · Shared-prime graph model`

## Stable advanced bridges

- `NT-A01 · Zero-stripped factorials: valuations plus a ratio`
- `NT-A02 · Idempotents: same ending for N and N^2`
- `NT-A03 · Complete unit-group products`
- `NT-A04 · Two-adic filtering through Euler phi`
- `NT-A05 · Reduced-residue sums plus geometric series`
- `NT-A06 · GCD of several linear forms`
- `NT-A07 · Exponential GCDs and parity of exponents`
- `NT-A08 · Last nonzero digits of a factorial`
- `NT-A09 · Binary modular inverses as periodic expansions`
- `NT-A10 · Recurrences modulo the target`
- `NT-A11 · Nested floors and roots`
- `NT-A12 · Exact carry accounting in digit sums`
- `NT-A13 · Minimising a base-b number with prescribed digit sum`
- `NT-A14 · Moving square intervals`
- `NT-A15 · GCD/LCM equations with shape normalisation`
- `NT-A16 · Squarefree polynomial values`

## Recommended dependency order

1. divisibility, gcd/lcm, prime exponents;
2. Bezout, congruence legality, inverses, CRT;
3. cycles, Fermat/Euler/Wilson, last digits;
4. valuations, factorial zeros, perfect powers, reduced residues;
5. factorisation engines, filters, gcd/lcm normalisation, Pythagorean triples;
6. digits, bases, digit sums, exact carries;
7. floors, windows, recurrences, counting/extremal bridges;
8. mixed method-selection lab and advanced bridges;
9. Appendix A with adaptive local hints;
10. Appendix B/C and final gates.

## Number Theory orphan-method traps

- "Use modular arithmetic" is not enough: teach the modulus choice, cancellation legality, and whether order/Euler applies.
- "Use CRT" is not enough: teach non-coprime compatibility and a constructive merge.
- "Use factorisation" is not enough: distinguish powers, manufactured fixed-product forms, and polynomial/consecutive-factor forms.
- "Use valuations" is not enough: factor the target and write one prime-exponent inequality per prime.
- "Use digit sum" is not enough: distinguish modulo-9 information from exact carry accounting.
- "Use gcd/lcm" is not enough: teach normalisation a=dx, b=dy when both appear together.
- "Count" is not enough: identify whether the invariant is fixed multiplicity, exponent-lattice choices, residue obstruction, or a graph of shared primes.
- "Floor" is not enough: write the exact half-open interval and recheck endpoints.

## Number Theory visual profile

Use structural visuals only when they reduce cognitive load: residue cycles, CRT split/merge diagrams, exponent grids, valuation pipelines, carry columns, base place-value blocks, interval intersections, square-gap sketches, and Diophantine/factor-pair schematics. Do not add decorative number imagery.

## Appendix A hint policy

- H1: one question-specific recognition sentence.
- H2: retrieve one or two stable skills/bridges already taught.
- H3: at most the first setup/equation; no route summary.
- Easy items: H1. Medium: H1-H2. Hard: H1-H3.
- Local IDs are `NT-Q001` to `NT-Q090`; provenance is kept in a separate source ledger.

## Badge contract

Appendix badges are orientation metadata, not hints.

For Appendix A, each item receives:

- level: `CORE`, `BRIDGE`, or `CHALLENGE`;
- broad family: e.g. `MODULAR`, `DIVISORS`, `DIGITS`, `DIOPHANTINE`;
- mode: `TRANSFER`, `MIXED`, or `ADVANCED BRIDGE`.

Do not place the decisive trick or exact theorem in a badge. H1/H2 own recognition/retrieval.

Appendix B additionally receives a `PYQ` badge because source identity is part of the challenge-bank role.

## Deliverables-inside-PDF contract

The final PDF has two layers:

1. **Student Book** - teaching units, worked bridges, first-step reference, Appendix A, Appendix B, Appendix C.
2. **Reviewer / Build Dossier** - Number Theory profile, full question-to-method matrix, Appendix B method-coverage matrix, source/custody ledger, self-sufficiency audit, and final QA record.

## Hard gate

```text
QUESTION_INVENTORY = PASS_90_OF_90
QUESTION_TO_METHOD_MATRIX = PASS_90_OF_90
ORPHAN_METHOD_AUDIT = PASS_90_OF_90
VISUAL_PEDAGOGY_AUDIT = PASS_90_OF_90
APPENDIX_A_CUSTODY = PASS_90_OF_90
APPENDIX_A_HINT_AUDIT = PASS_90_OF_90
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_90_OF_90
```

These are document-level checks, not classroom evidence.

## Phase gate

Phase 1 freezes corpus custody, stable IDs, matrix schema, badge vocabulary and PDF inclusion map. It does not claim the final PR140 content gates have passed.
