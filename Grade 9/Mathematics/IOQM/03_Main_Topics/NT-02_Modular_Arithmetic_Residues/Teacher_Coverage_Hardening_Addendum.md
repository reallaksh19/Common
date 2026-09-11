# NT-02 — Teacher Coverage Hardening Addendum

Status: `STATIC_DIAGNOSTIC_ADDENDUM_V1`
Issue: `#132`

This addendum synchronizes the learner-facing bounded Euler bridge in `03_First_Step_Reference.md`. It does not alter historical-anchor answers or existing authored-item keys.

## Euler's theorem

If `gcd(a,n)=1`, then

`a^phi(n) congruent 1 (mod n)`,

where `phi(n)` counts the integers in `1,...,n` that are coprime to `n`.

### Independent proof-idea check

Let `r_1,...,r_phi` be a complete list of invertible residue classes modulo `n`. Multiplication by `a` permutes these classes because `a` is invertible. Therefore

`(ar_1)...(ar_phi) congruent r_1...r_phi (mod n)`.

The product `r_1...r_phi` is invertible, so cancellation is legal, yielding

`a^phi(n) congruent 1 (mod n)`.

### Decision boundary

A large exponent does not automatically call for Euler. First reduce the base and inspect a short cycle/order. Use Euler only when `gcd(a,n)=1` is explicit or cheaply checked and the theorem reduces work.

## Fermat's little theorem — design companion

For prime `p` with `p` not dividing `a`,

`a^(p-1) congruent 1 (mod p)`.

This is included as a curriculum-design prime-modulus companion/corollary. The supplied preparation routine explicitly names Euler's theorem, not Fermat's little theorem.

## Diagnostic codes

- `NT02-EULER-1`: coprimality not checked before Euler.
- `NT02-EULER-2`: exponent reduced by `phi(n)` in a non-coprime case.
- `NT02-EULER-3`: totient machinery overused where a two- or three-step residue cycle is cheaper.
- `NT02-FERMAT-1`: modulus not checked prime.
- `NT02-FERMAT-2`: base divisible by prime modulus but Fermat invoked anyway.
- `NT02-POWER-ROUTE`: theorem/cycle choice not justified.

## Evidence truth

This addendum is a static mathematics/diagnostic synchronization. It does not constitute classroom timing/readability, retention, psychometric, qualification/pass-mark or publication calibration; those remain `NOT_RUN`.