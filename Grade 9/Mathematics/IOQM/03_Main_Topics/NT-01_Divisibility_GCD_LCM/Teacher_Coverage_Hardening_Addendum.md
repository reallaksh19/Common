# NT-01 — Teacher Coverage Hardening Addendum

Status: `STATIC_DIAGNOSTIC_ADDENDUM_V1`
Issue: `#132`

This addendum synchronizes the learner-facing Euclid's Lemma bridge added to `03_First_Step_Reference.md`. It does not alter historical-anchor answers or existing authored-item keys.

## Euclid's Lemma

Statement:

If `p` is prime and `p|ab`, then `p|a` or `p|b`.

### Independent proof check

If `p` does not divide `a`, primality implies `gcd(p,a)=1`. By Bezout/linear-combination structure there are integers `r,s` with

`rp+sa=1`.

Multiplying by `b` gives

`rpb+sab=b`.

Since `p` divides both left-hand terms, `p|b`. Thus either `p|a` or `p|b`.

### Required diagnostic contrast

The primality hypothesis is necessary. `6|2*3`, but `6` divides neither factor. A learner who applies the lemma to an arbitrary composite divisor has not checked the theorem hypothesis.

### Diagnostic codes

- `NT01-EUCLID-1`: prime hypothesis not checked.
- `NT01-EUCLID-2`: composite divisor incorrectly split across a product.
- `NT01-EUCLID-3`: theorem name recalled but no link to divisibility/gcd structure.
- `NT01-EUCLID-4`: Euclid's Lemma confused with the Euclidean algorithm.

## Downstream boundary

NT-03 may retrieve Euclid's Lemma as an NT-01 export when prime divisibility must split across a product. NT-03 remains the canonical owner of prime factorisation, valuations, divisor counts and perfect-power structure.

## Evidence truth

This addendum is a static mathematics/diagnostic synchronization. It does not constitute classroom timing/readability, retention, psychometric, qualification/pass-mark or publication calibration; those remain `NOT_RUN`.