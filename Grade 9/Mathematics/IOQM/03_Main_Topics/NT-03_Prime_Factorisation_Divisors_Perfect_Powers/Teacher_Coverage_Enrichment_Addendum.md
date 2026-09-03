# NT-03 — Teacher Coverage Enrichment Addendum

Status: `STATIC_DIAGNOSTIC_ADDENDUM_V1`
Issue: `#134`

This addendum synchronizes the learner-facing consecutive-sum / odd-divisor transfer added to `03_First_Step_Reference.md`. It does not alter the existing historical-anchor keys.

## Structural derivation

For consecutive positive integers

`a, a+1, ..., a+r-1`

with `a>=1` and `r>=2`,

`n = r(2a+r-1)/2`, hence `2n=r(2a+r-1)`.

The two factors `r` and `2a+r-1` have opposite parity because their difference is `2a-1`, an odd integer.

Therefore representability is governed by the presence of a nontrivial odd factor:

> `n` is a sum of at least two consecutive positive integers iff `n` is not a power of `2`.

Equivalent statement:

> `n` is representable iff `n` has an odd divisor greater than `1`.

## Diagnostic A — existence only

Is `64` representable as a sum of at least two consecutive positive integers?

No. `64` is a power of `2`.

## Diagnostic B — existence with an odd divisor

Is `45` representable?

Yes. It has odd divisors greater than `1`; for example `45=14+15+16`.

The example verifies existence, but the structural criterion is the reason a search is unnecessary.

## Diagnostic C — ownership boundary

For `n=105`, a learner is asked to list **all** consecutive-positive-integer representations. The first move may use NT-03's odd-divisor structure to identify viable lengths, but actual recovery of start terms, positivity and complete enumeration are NT-04 reconstruction work.

## Misconception diagnostics

- `NT03-CONSEC-1`: counts consecutive sums by brute force before checking the power-of-two obstruction.
- `NT03-CONSEC-2`: forgets the requirement `r>=2` and treats the one-term representation as sufficient.
- `NT03-CONSEC-3`: ignores positivity of the starting term.
- `NT03-CONSEC-4`: knows the existence criterion but cannot derive `2n=r(2a+r-1)`.
- `NT03-CONSEC-5`: expands into full Diophantine reconstruction instead of routing that work to NT-04.

## Evidence truth

The external DOCX motivated this comparison check but is not source authority. This addendum records static curriculum coverage only; classroom timing/readability, retention, psychometrics, qualification/pass-mark calibration and publication approval remain `NOT_RUN`.