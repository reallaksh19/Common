# Number Theory Advanced Worked Bridges v5 - Phase 2

## NT-A09 · Binary modular inverses as periodic expansions

**Recognition cue.** Bits $x_k$ are defined so partial binary sums invert a fixed odd number modulo $2^n$.

**Why this method fits.** Interpret the compatible residues as a 2-adic inverse rather than solving each n independently.

**First line.** Look for a geometric-series identity when the odd denominator has form $2^r-1$ or $2^r+1$.

**Execution bridge.** For $1/(2^r-1)$, write $-1/(1-2^r)$, giving a repeating block in the 2-adic expansion. Compatibility modulo every $2^n$ means the low $n$ bits of this infinite pattern are exactly the required inverse.

**Legality / equality check.** 2-adic expansion is read from low powers upward; it is not an ordinary convergent real binary fraction.

**Nearby wrong approach.** Solving a fresh inverse congruence for every n.

**Transfer prompt.** Transfer: find the repeating low-bit pattern of the 2-adic inverse of 3.

## NT-A10 · Recurrences modulo the target

**Recognition cue.** The recurrence has a huge multiplier that becomes simple modulo the requested modulus.

**Why this method fits.** Reduce the recurrence first; the coefficient may become 1, -1, or another short-cycle state.

**First line.** Write the recurrence entirely modulo m before iterating.

**Execution bridge.** If $a_n=100a_{n-1}+n$ and the target modulus is 99, then $100\equiv1$, so $a_n\equiv a_{n-1}+n$. Iteration telescopes to a simple arithmetic sum. The enormous decimal growth never matters.

**Legality / equality check.** Use the corrected/original modulus from the authoritative source; an OCR-modulus error changes the mathematics.

**Nearby wrong approach.** Expanding several terms and looking for a decimal pattern.

**Transfer prompt.** Transfer: reduce $a_n=26a_{n-1}+n$ modulo 25.

## NT-A11 · Nested floors and roots

**Recognition cue.** Several square roots/floors are nested and an extremal integer is requested.

**Why this method fits.** Peel from the outside; every floor becomes a half-open interval.

**First line.** From $\lfloor X\rfloor=k$, write $k\le X<k+1$, then undo monotone roots.

**Execution bridge.** Because square root is increasing on nonnegative inputs, squaring preserves inequalities. Continue one layer at a time until the innermost integer is bounded. The strict upper endpoint typically determines the greatest integer as one less than a perfect power.

**Legality / equality check.** Check nonnegativity before squaring and preserve every strict upper endpoint.

**Nearby wrong approach.** Replacing floor values by equalities.

**Transfer prompt.** Transfer: solve $\lfloor\sqrt{\lfloor\sqrt N\rfloor}\rfloor=3$ for the largest N.

## NT-A12 · Exact carry accounting in digit sums

**Recognition cue.** Two exact digit sums before/after addition are given.

**Why this method fits.** Each carry reduces the naive input digit-sum total by exactly 9.

**First line.** Set $C=(s(a)+s(b)-s(a+b))/9$.

**Execution bridge.** First determine the number of carries. Then use column restrictions to place them. This converts a digit-search problem into a small constrained arrangement problem. The formula is exact; modulo-9 reasoning alone is weaker.

**Legality / equality check.** Count propagated carries; each column carry is one event.

**Nearby wrong approach.** Using only $s(n)\equiv n\pmod9$.

**Transfer prompt.** Transfer: determine how many carries occur in any addition with input digit sums 31 and output digit sum 13.

## NT-A13 · Minimising a base-b number with prescribed digit sum

**Recognition cue.** You need the smallest number whose base-b digits have a fixed total.

**Why this method fits.** Digit mass is cheapest in low positions.

**First line.** Fill the least significant digits with $b-1$ as much as possible; put the remainder in the next position.

**Execution bridge.** If total digit sum is $S=q(b-1)+r$ with $0\le r<b-1$, the smallest positive representation has $q$ trailing digits $b-1$ and then digit $r$ (unless $r=0$, in which case use exactly q maximal digits). Any upward move of one digit unit increases value because higher place weights are larger.

**Legality / equality check.** Maintain a nonzero leading digit and the correct base digit cap.

**Nearby wrong approach.** Putting large digits on the left because they 'use fewer digits'.

**Transfer prompt.** Transfer: find the smallest base-5 integer with digit sum 17.

## NT-A14 · Moving square intervals

**Recognition cue.** Equal-length intervals move to the right and you compare numbers of contained squares.

**Why this method fits.** Consecutive square gaps increase monotonically.

**First line.** Use $(k+1)^2-k^2=2k+1$ to compare density at the extreme positions.

**Execution bridge.** A fixed span can cover more consecutive square gaps when those gaps are smaller. Therefore maximum square count occurs as far left as allowed, minimum as far right as allowed. Count only the two extreme intervals, then prove monotonicity.

**Legality / equality check.** Use the exact interval endpoints; inclusive intervals of integers have one more integer than their endpoint difference.

**Nearby wrong approach.** Counting every translated interval.

**Transfer prompt.** Transfer: compare square counts in [101,500] and [10001,10400].

## NT-A15 · GCD/LCM equations with shape normalisation

**Recognition cue.** An equation mixes $a,b,\gcd(a,b)$, and $\operatorname{lcm}(a,b)$.

**Why this method fits.** Separate scale $d$ from coprime shape $x,y$.

**First line.** Set $a=dx,\ b=dy,\ \gcd(x,y)=1$, so lcm $=dxy$.

**Execution bridge.** Substitute and factor out $d$. Frequently $d$ must divide a small constant, giving a few scale cases. The remaining equation in coprime $x,y$ often factors via SFFT. Apply coprimality and range conditions last.

**Legality / equality check.** Keep $\gcd(x,y)=1$ throughout; otherwise the normalization is not canonical.

**Nearby wrong approach.** Replacing lcm by $ab/\gcd$ but keeping raw a,b, which hides the scale.

**Transfer prompt.** Transfer: solve a toy equation $a+b=\gcd(a,b)+2\operatorname{lcm}(a,b)$ under a small bound.

## NT-A16 · Squarefree polynomial values

**Recognition cue.** A large polynomial value must avoid every repeated prime factor.

**Why this method fits.** Factor the polynomial symbolically before checking squarefreeness.

**First line.** Find algebraic factors; then use parity/small congruences to eliminate whole classes.

**Execution bridge.** Once $P(n)=F_1(n)\cdots F_r(n)$, a repeated prime can arise within one factor or as a gcd between factors. Small moduli often force $p^2\mid P(n)$ for entire residue classes. Only a few survivors need explicit factor checks.

**Legality / equality check.** Squarefree means no prime square divides the entire product; pairwise-coprime factors are not automatic.

**Nearby wrong approach.** Evaluating the huge polynomial first and then attempting full factorization.

**Transfer prompt.** Transfer: analyze when $(n-1)n(n+1)$ can be squarefree.
