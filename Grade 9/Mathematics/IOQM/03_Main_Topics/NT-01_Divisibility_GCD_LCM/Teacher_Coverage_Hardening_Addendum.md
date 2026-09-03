# NT-01 — Teacher Coverage Hardening Addendum

Status: `STATIC_DIAGNOSTIC_ADDENDUM_V2`
Issues: `#132`, `#134`

This addendum synchronizes the learner-facing Euclid's Lemma and Bézout / extended-Euclid bridges in `03_First_Step_Reference.md`. It does not alter historical-anchor answers or existing authored-item keys.

## Euclid's Lemma

Statement:

If `p` is prime and `p|ab`, then `p|a` or `p|b`.

### Independent proof check

If `p` does not divide `a`, primality implies `gcd(p,a)=1`. By Bézout/linear-combination structure there are integers `r,s` with

`rp+sa=1`.

Multiplying by `b` gives

`rpb+sab=b`.

Since `p` divides both left-hand terms, `p|b`. Thus either `p|a` or `p|b`.

### Required diagnostic contrast

The primality hypothesis is necessary. `6|2*3`, but `6` divides neither factor.

## Bézout / extended Euclid

Statement:

For integers `a,b`, there exist integers `x,y` such that

`ax+by=gcd(a,b)`.

The pedagogical route should be constructive: run Euclid, then back-substitute.

### Diagnostic A — solvability

Does `18x+30y=7` have integer solutions?

`gcd(18,30)=6`, but `6` does not divide `7`. Therefore **no** integer solution exists.

### Diagnostic B — one constructive solution

Find one integer solution of `43x+30y=1`.

Euclid/back-substitution gives

`1=7*43-10*30`,

so one solution is `(x,y)=(7,-10)`.

### Diagnostic C — scale, then hand off

For `43x+30y=5`, scale the preceding identity to obtain one solution `(35,-50)`. If a problem asks for **all** solutions or imposes positivity/bounds, route to NT-04's Diophantine reconstruction rather than expanding NT-01 into a full solution-family chapter.

### Closest-rational boundary

Bézout may show that a determinant such as `|qb-pa|` can reach `1` when `p,q` are coprime. It does **not** by itself prove which admissible bounded denominator gives the closest fraction. Bounds and final comparison still matter.

## Diagnostic codes

- `NT01-EUCLID-1`: prime hypothesis not checked.
- `NT01-EUCLID-2`: composite divisor incorrectly split across a product.
- `NT01-EUCLID-3`: theorem name recalled but no link to divisibility/gcd structure.
- `NT01-EUCLID-4`: Euclid's Lemma confused with the Euclidean algorithm.
- `NT01-BEZOUT-1`: linear equation searched before checking `gcd(a,b)|c`.
- `NT01-BEZOUT-2`: Euclidean algorithm stopped at the gcd when coefficients were required.
- `NT01-BEZOUT-3`: one Bézout representation confused with the full solution family.
- `NT01-BEZOUT-4`: closest-rational claim made without enforcing the stated bounds.

## Downstream boundary

NT-03 may retrieve Euclid's Lemma as an NT-01 export when prime divisibility must split across a product. NT-04 may retrieve Bézout / extended-Euclid solvability for linear Diophantine equations. NT-04 remains the canonical owner of full Diophantine parameterization, positivity/bound filtering and reconstruction.

## Evidence truth

The external DOCX was comparison material only. This addendum is a static mathematics/diagnostic synchronization and does not constitute classroom timing/readability, retention, psychometric, qualification/pass-mark or publication calibration; those remain `NOT_RUN`.