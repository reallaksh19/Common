# P2 Greatest / Least Integer Functions — Practice Ladder

Every family uses:

`F0 FOUNDATION -> F1 DIRECT -> F2 STANDARD -> F3 DISGUISED -> F4 PRELIMINARY -> XF TRANSFER`

Because no clean direct five-year PYQ family is established, this package does **not** insert a fake PYQ rung. Where relevant, bridge evidence is named separately.

## A — Definitions and negatives

- F0: evaluate floor/ceiling of positive decimals.
- F1: evaluate negative nonintegers.
- F2: compare `floor(x),ceil(x)` across integer boundaries.
- F3: recover an interval from a claimed floor/ceiling value.
- F4: mixed signs with absolute values/rational inputs.
- XF: detect truncation-based wrong reasoning.

## B — Floor equations

- F0: `floor(x)=3`.
- F1: `floor(2x+1)=4`.
- F2: `floor((x-1)/3)=-2`.
- F3: quadratic/radical inner expression with domain.
- F4: intersect translated interval with an independent constraint.
- XF: count integer solutions to the resulting real interval.

## C — Ceiling equations

Same progression with endpoint reversal and reflection identity.

## D — Inequalities

- F0: `floor(x)>=2`.
- F1: `floor(3x-1)<=5`.
- F2: ceiling inequalities.
- F3: compound inequalities involving two floor terms.
- F4: parameter threshold problems.
- XF: convert to integer count or feasible parameter interval.

## E — Fractional part

- F0: positive examples.
- F1: negative examples.
- F2: solve `{x}=c` under a bounded domain.
- F3: `{2x}` versus `{x}`.
- F4: identities using `x=n+r`.
- XF: combine with parity/integer constraints.

## F — x plus floor(x)

- F0: set `n=floor(x)`.
- F1: `x+floor(x)=c`.
- F2: `2x-floor(x)=c`.
- F3: two nested integer-part terms.
- F4: parameter count of solutions.
- XF: prove uniqueness/nonexistence by interval consistency.

## G — Sum identities

- F0: test examples.
- F1: prove floor-sum bounds.
- F2: characterize equality.
- F3: prove `floor(x)+floor(x+1/2)=floor(2x)`.
- F4: generalize to shifted sums.
- XF: connect to counting residue classes/fractional partitions.

## H — Integer counting

- F0: count integers in closed interval.
- F1: open/half-open intervals.
- F2: endpoints defined by radicals/rationals.
- F3: parameterized interval counts.
- F4: count integer solutions after floor translation.
- XF: lattice/grouping interpretations.

## I — Square-root and quotient bridges

- F0: `floor(sqrt(n))=k`.
- F1: count integer n.
- F2: `ceil(N/d)` minimum groups.
- F3: quotient/remainder interpretation.
- F4: mixed floor with divisibility.
- XF: bridge to number theory or sequence indexing.

## J — Source integrity and method selection

- F0: distinguish direct floor-function problem from final rounding operation.
- F1: identify `AUTHOR_CREATED_FOUNDATION` vs `BRIDGE_EVIDENCE`.
- F2: reject invented historical frequency.
- F3: compare two plausible endpoint conventions against the definition.
- F4: diagnose a supplied solution that truncates negatives.
- XF: write a corrected solution without altering the source claim.

## Promotion standard

Student should pass:

- 90% first-move classification;
- 80% mixed equation/inequality accuracy;
- zero negative-truncation errors;
- zero systematic endpoint-direction errors;
- one successful proof/derivation using `x=n+r`;
- one source-QC discrimination between primary and bridge evidence.
