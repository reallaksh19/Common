# Number Theory Teaching Architecture v5 - Phase 2

# Unit 7 - Discrete structure after arithmetic

## NT-FLOOR-01 · Floor functions as half-open intervals

**What you probably remember.** $\lfloor x\rfloor$ is the greatest integer $\le x$.

**The missing IOQM link.** The floor equality is an interval, and the strict upper endpoint is essential.

**Why this works.** $\lfloor x\rfloor=k\iff k\le x<k+1$. Convert first, then solve the ordinary inequalities.

**Try this first.** Introduce $k=\lfloor X\rfloor$ and write $k\le X<k+1$.

**Non-identical worked bridge.** $\lfloor(n+3)/5\rfloor=7$ gives $35\le n+3<40$, hence integer $n\in\{32,33,34,35,36\}$.

**Close contrast.** Replacing $\lfloor X\rfloor=k$ by $X=k$ loses almost all solutions.

**Legality / boundary check.** Recheck both endpoints after squaring or other monotone transformations.

**Visual teaching object.** Half-open number line with closed left/open right endpoint.

**Practice targets.** NT-Q047, NT-Q060, NT-Q061, NT-Q062, NT-Q076

## NT-REC-01 · Affine recurrences modulo a target

**What you probably remember.** A recurrence defines each term from previous terms.

**The missing IOQM link.** Reduce the recurrence modulo the target before expanding large coefficients.

**Why this works.** For $a_n=ca_{n-1}+f(n)$, if $c\equiv1\pmod m$, then modulo $m$ the recurrence telescopes into a sum. More generally track the state modulo $m$, not the enormous integer.

**Try this first.** Reduce every coefficient modulo the target modulus.

**Non-identical worked bridge.** If $a_n=10a_{n-1}+n$, then mod 9, $a_n\equiv a_{n-1}+n$; iterate by summing the added indices.

**Close contrast.** Expanding the recurrence in decimal form creates huge numbers while discarding the modular structure.

**Legality / boundary check.** If claiming a period, verify the entire required state repeats, not only one term.

**Visual teaching object.** State arrow modulo $m$.

**Practice targets.** NT-Q048, NT-Q063

## NT-WINDOW-01 · Overlapping-window cancellation

**What you probably remember.** Two nearby sums share most terms.

**The missing IOQM link.** Subtract equal overlapping windows to cancel the shared block instantly.

**Why this works.** If $\sum_{j=0}^{r-1}a_{i+j}$ is constant in $i$, subtract consecutive windows to get $a_i=a_{i+r}$.

**Try this first.** Write the window at $i$ and $i+1$ underneath each other and subtract.

**Non-identical worked bridge.** If every four consecutive terms have the same sum, then $(a_i+\cdots+a_{i+3})-(a_{i+1}+\cdots+a_{i+4})=0$, so $a_i=a_{i+4}$.

**Close contrast.** Do not solve for individual terms by many simultaneous equations before using cancellation.

**Legality / boundary check.** State the valid index range for the derived periodic relation.

**Visual teaching object.** Two overlapping colored windows.

**Practice targets.** NT-Q007

## NT-COUNT-01 · Fixed-multiplicity and digit-choice counting

**What you probably remember.** Count by cases or multiplication.

**The missing IOQM link.** Find a quantity that every object contributes to the same number of times, or convert digit conditions into independent choices.

**Why this works.** Fixed multiplicity turns a large list of sums into one weighted total; place-value constraints often turn into a small product/sum of digit choices.

**Try this first.** Ask: how many times does one underlying object get counted?

**Non-identical worked bridge.** For six numbers, the sum of all $\binom62=15$ pairwise sums equals $5$ times the sum of the six numbers, because each original number appears with each of the other five.

**Close contrast.** Do not reconstruct every hidden variable when only a symmetric total is requested.

**Legality / boundary check.** Distinguish ordered from unordered choices and enforce leading-digit constraints.

**Visual teaching object.** Incidence count diagram or compact choice tree.

**Practice targets.** NT-Q006, NT-Q030, NT-Q037, NT-Q043, NT-Q047, NT-Q069, NT-Q079, NT-Q081

## NT-PIGEON-01 · Small-prime and residue-class obstruction

**What you probably remember.** Pigeonhole says too many objects in too few boxes force repetition.

**The missing IOQM link.** In number theory, the boxes are often residue classes; repeated multiples of a small prime can violate pairwise coprimality or primality conditions.

**Why this works.** If an arithmetic progression samples many residues modulo $p$ and $p\nmid d$, residues cycle, forcing multiple terms divisible by $p$. To avoid that, $p\mid d$.

**Try this first.** Test the smallest primes first and ask whether two forbidden multiples are unavoidable.

**Non-identical worked bridge.** In an 8-term arithmetic progression whose terms must be pairwise coprime, $2\mid d$, $3\mid d$, and $5\mid d$; otherwise at least two terms hit the same zero residue modulo that prime.

**Close contrast.** Checking primality term by term misses the structural obstruction.

**Legality / boundary check.** If $p\mid d$, all terms have the same residue mod $p$; ensure that residue itself is not 0 when pairwise coprimality is required.

**Visual teaching object.** Residue-class boxes around a small prime.

**Practice targets.** NT-Q022, NT-Q039

## NT-SQUAREGAP-01 · Monotone square-gap extremal reasoning

**What you probably remember.** Consecutive squares get farther apart.

**The missing IOQM link.** A fixed-length interval contains weakly fewer squares as it moves to the right.

**Why this works.** $(k+1)^2-k^2=2k+1$ increases with $k$. Compare the span from the first included square to the last included square rather than recounting every interval.

**Try this first.** Write the square-gap formula and identify the leftmost/rightmost candidate interval.

**Non-identical worked bridge.** An interval of fixed length 100 can contain more squares near 1 than near 10,000 because local gaps are much smaller on the left.

**Close contrast.** Do not enumerate hundreds of translated intervals when monotonicity determines the extremal positions.

**Legality / boundary check.** Use the actual inclusive interval length/endpoints when counting squares.

**Visual teaching object.** Number line with widening gaps between squares.

**Practice targets.** NT-Q068

## NT-PRIMEGRAPH-01 · Shared-prime graph model

**What you probably remember.** A gcd greater than 1 means two numbers share a prime factor.

**The missing IOQM link.** Pairwise gcd conditions can be represented by a graph whose edges carry shared primes.

**Why this works.** Assign a prime to each required-sharing edge. Nonadjacent vertices must not inherit the same edge-prime. This converts gcd constraints into a combinatorial design.

**Try this first.** Draw vertices for the integers and an edge exactly where gcd must exceed 1.

**Non-identical worked bridge.** For a path $a_1-a_2-a_3-a_4$, use fresh primes $p,q,r$ on edges and let internal vertices contain the two adjacent edge-primes; then nonadjacent gcds stay 1.

**Close contrast.** Choosing arbitrary composite numbers first makes accidental common factors hard to control.

**Legality / boundary check.** Verify every required edge shares a factor and every forbidden pair is coprime.

**Visual teaching object.** Prime-labelled path graph.

**Practice targets.** NT-Q044

# Unit 8 - Mixed method-selection lab

The learner should not choose a method because a theorem name looks familiar.
Use this six-step router:

1. **What is requested?** divisor, remainder, count, largest/smallest, digit block, integer solutions?
2. **What structure is visible?** prime exponents, same remainder, huge power, fixed product, digit representation, floor interval?
3. **Which representation compresses it?** factorization, exponent vector, congruence, gcd-normalization, place value, half-open interval?
4. **What is the cheapest legal theorem?** short cycle before Euler; direct factorization before heavy modular arithmetic; a bound before brute force.
5. **What is the first useful line?** write it explicitly.
6. **What could make the route illegal?** non-coprime cancellation, incompatible CRT residues, wrong floor endpoint, missing positivity, extraneous case?

## Close decision boundaries

| Nearby choices | Correct discriminator |
|---|---|
| divisibility vs congruence | Is a modulus/remainder already visible? |
| short cycle vs Euler | Is a tiny cycle easier, and is the base coprime? |
| Euler vs order | Need only a working period or the least period? |
| CRT vs one modulus | Does splitting expose prime-power structure? |
| divisor count vs valuation | Counting divisors or measuring exponent supply? |
| digit sum mod 9 vs carries | Congruence-only information or exact change? |
| factorization vs bounds | Can the equation become a fixed product immediately? |
| gcd/lcm formula vs normalization | Do both gcd and lcm occur with unknown numbers? |
| floor algebra vs interval | Always interval first; algebra comes afterward. |
| counting vs pigeonhole | Count legal objects, or prove repetition/obstruction? |
