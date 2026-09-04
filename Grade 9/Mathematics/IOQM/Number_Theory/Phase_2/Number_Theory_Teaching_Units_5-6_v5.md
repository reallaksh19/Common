# Number Theory Teaching Architecture v5 - Phase 2

# Unit 5 - Integer equations: manufacture structure

## NT-FACT-01 · Factorisation engines for integer equations

**What you probably remember.** You know standard identities.

**The missing IOQM link.** The strategic question is which factorisation converts arithmetic restrictions into a finite divisor problem.

**Why this works.** Three recurring engines are: difference/sum of powers; manufactured fixed-product forms (SFFT); and polynomial-to-consecutive-factor forms. Choose the engine from the surface before expanding.

**Try this first.** Ask: can I turn this into a product equal to a fixed integer, or into consecutive/near-consecutive factors?

**Non-identical worked bridge.** $x^2-y^2=45$ becomes $(x-y)(x+y)=45$, so parity and divisor pairs replace a two-variable search.

**Close contrast.** Expansion is often the opposite of progress when the target is integer factor structure.

**Legality / boundary check.** After factoring, impose sign, parity, ordering and integrality on factor pairs.

**Visual teaching object.** Factorisation router with the three engines.

**Practice targets.** NT-Q032

## NT-FACT-POW-01 · Difference/sum-of-powers factorisation

**What you probably remember.** $a^2-b^2=(a-b)(a+b)$.

**The missing IOQM link.** For huge even exponents, factor repeatedly before doing modular computation.

**Why this works.** $a^n-b^n$ is divisible by $a-b$; if $n$ is even, repeated difference of squares exposes factors $a^{n/2}+b^{n/2}$. Sum-of-cubes and difference-of-cubes have standard cubic factors.

**Try this first.** Inspect exponent parity and factor once before evaluating any power.

**Non-identical worked bridge.** $5^4-3^4=(25-9)(25+9)=16\cdot34$.

**Close contrast.** Computing residues first may hide a large deterministic factor.

**Legality / boundary check.** Sum $a^n+b^n$ has $a+b$ as a factor only when $n$ is odd.

**Visual teaching object.** Factor tree by halving an even exponent.

**Practice targets.** NT-Q002, NT-Q013, NT-Q018, NT-Q020, NT-Q053, NT-Q059, NT-Q065, NT-Q077

## NT-FACT-SFFT-01 · Manufactured factorisation and fixed-product forms

**What you probably remember.** Completing a square is familiar.

**The missing IOQM link.** SFFT completes a rectangle: add exactly what is needed to turn $xy+ax+by$ into a product.

**Why this works.** $xy+ax+by=c$ becomes $(x+b)(y+a)=c+ab$. Reciprocal equations often become fixed products after clearing denominators.

**Try this first.** Move constants, add the missing $ab$, and factor.

**Non-identical worked bridge.** $xy+x+y=35$ becomes $(x+1)(y+1)=36$. Positive integer solutions now correspond to divisor pairs of 36 with both factors at least 2.

**Close contrast.** A quadratic formula is usually unnecessary once both variables appear only bilinearly.

**Legality / boundary check.** Translate factor-pair bounds back to the original variables; count ordered/unordered pairs as requested.

**Visual teaching object.** Rectangle completion diagram / factor-pair table.

**Practice targets.** NT-Q014, NT-Q090

## NT-FACT-POLY-01 · Polynomial-to-consecutive-factor factorisation

**What you probably remember.** Polynomials can factor by identities.

**The missing IOQM link.** Symmetric polynomial values often hide products of consecutive or near-consecutive integers, unlocking factorial divisibility.

**Why this works.** Look for factors in $n^2-a^2$, then multiply symmetric factors. Products of $r$ consecutive integers are automatically divisible by $r!$.

**Try this first.** Factor around symmetric shifts $n-k,\ldots,n+k$ before substituting numbers.

**Non-identical worked bridge.** $n^4-5n^2+4=(n^2-1)(n^2-4)=(n-2)(n-1)(n+1)(n+2)$.

**Close contrast.** Numerically testing several $n$ values does not reveal the universal divisor.

**Legality / boundary check.** If a factor such as $n$ is missing, do not claim a full consecutive block.

**Visual teaching object.** Number-line placement of near-consecutive factors.

**Practice targets.** NT-Q046, NT-Q078

## NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters

**What you probably remember.** Integer answers must satisfy parity and size constraints.

**The missing IOQM link.** Filters are often the main engine: they turn an infinite algebraic family into a handful of cases.

**Why this works.** Use the cheapest restriction first: parity, gcd, modular class, positivity, a square discriminant, smallest-prime-factor bound, or monotonicity.

**Try this first.** Before solving fully, ask which necessary condition destroys most cases.

**Non-identical worked bridge.** For positive integers $x>y$ with $x^2+y^2=25$, $x\le4$. Testing $x=4,3$ gives only $(4,3)$. The bound makes the search finite.

**Close contrast.** Do not brute-force a wide range before deriving a mathematical bound.

**Legality / boundary check.** Necessary filters may not be sufficient; survivors must return to the original equation.

**Visual teaching object.** Funnel diagram: infinite family -> parity -> bound -> finite survivors.

**Practice targets.** NT-Q014, NT-Q019, NT-Q020, NT-Q024, NT-Q026, NT-Q039, NT-Q058, NT-Q059, NT-Q064, NT-Q065, NT-Q068, NT-Q070, NT-Q073

## NT-GCDNORM-01 · GCD/LCM normalisation

**What you probably remember.** $\gcd(a,b)\operatorname{lcm}(a,b)=ab$.

**The missing IOQM link.** When gcd and lcm appear together, separate scale from coprime shape.

**Why this works.** Write $a=dx,\ b=dy$ with $d=\gcd(a,b)$ and $\gcd(x,y)=1$. Then $\operatorname{lcm}(a,b)=dxy$.

**Try this first.** Set $a=dx,\ b=dy,\ \gcd(x,y)=1$.

**Non-identical worked bridge.** If $\gcd(a,b)=6$ and $\operatorname{lcm}(a,b)=180$, then $xy=30$ with $\gcd(x,y)=1$. So each prime-power block $2,3,5$ must go wholly to one of $x,y$.

**Close contrast.** Factoring $a,b$ separately keeps too many variables; normalisation exposes the small shape equation.

**Legality / boundary check.** The shape variables must remain coprime.

**Visual teaching object.** Scale $d$ separated from coprime exponent blocks.

**Practice targets.** NT-Q066, NT-Q067, NT-Q083

## NT-PYTH-01 · Primitive Pythagorean triples

**What you probably remember.** $3,4,5$ and the theorem $a^2+b^2=c^2$.

**The missing IOQM link.** Primitive triples have a complete parametrization with coprimality and parity conditions.

**Why this works.** For primitive triples, $a=m^2-n^2,\ b=2mn,\ c=m^2+n^2$, where $m>n$, $\gcd(m,n)=1$, and $m,n$ have opposite parity.

**Try this first.** First divide out the gcd of the three sides; parametrize only the primitive core.

**Non-identical worked bridge.** For hypotenuse 13, solve $m^2+n^2=13$: $m=3,n=2$, giving $5,12,13$.

**Close contrast.** The parameterization without coprimality/opposite-parity conditions produces nonprimitive duplicates.

**Legality / boundary check.** Swap legs if necessary; scale afterward if the original triple is not primitive.

**Visual teaching object.** Right triangle plus $m,n$ parameter map.

**Practice targets.** NT-Q088

## NT-CONSUM-01 · Consecutive sums and odd-divisor structure

**What you probably remember.** An arithmetic progression has average equal to midpoint.

**The missing IOQM link.** Writing $N$ as consecutive positive integers becomes a divisor equation in the length.

**Why this works.** If $N=a+(a+1)+\cdots+(a+r-1)$, then $2N=r(2a+r-1)$. The two factors have controlled parity, linking representations to divisors of $2N$.

**Try this first.** Write $2N=r(2a+r-1)$.

**Non-identical worked bridge.** For $N=45$, test divisor lengths $r$: $45=22+23=14+15+16=7+8+9+10+11$, with positivity checked from the recovered $a$.

**Close contrast.** Listing consecutive sums by trial is acceptable only after the divisor structure has bounded possible lengths.

**Legality / boundary check.** Require $r\ge2$ for a nontrivial representation and $a>0$ if positive integers are required.

**Visual teaching object.** Centered block / length-times-average rectangle.

**Practice targets.** Transfer / prerequisite support

# Unit 6 - Digits and bases are equations

## NT-DIGIT-01 · Decimal place value, concatenation and deletion

**What you probably remember.** Digits encode powers of 10.

**The missing IOQM link.** Digit manipulation should become algebra immediately.

**Why this works.** $\overline{abc}=100a+10b+c$. Appending an $r$-digit block $B$ to $A$ gives $10^rA+B$. Deleting a leading digit means separating the highest power of 10.

**Try this first.** Translate the digit string to place value before using divisibility or algebra.

**Non-identical worked bridge.** Appending the two-digit block 37 to $n$ gives $100n+37$, not $n+37$.

**Close contrast.** Do not reason verbally about 'moving digits' once a place-value equation is available.

**Legality / boundary check.** Enforce digit bounds and leading-digit nonzero conditions.

**Visual teaching object.** Place-value block diagram.

**Practice targets.** NT-Q011, NT-Q012, NT-Q021, NT-Q036, NT-Q045, NT-Q075, NT-Q079, NT-Q080

## NT-BASE-01 · Other bases and digit validity

**What you probably remember.** Base $b$ uses powers of $b$.

**The missing IOQM link.** Unknown-base problems are polynomial equations plus digit-validity inequalities.

**Why this works.** $(d_k\cdots d_0)_b=\sum d_i b^i$ with $0\le d_i<b$.

**Try this first.** Expand every numeral into powers of its base and immediately record the largest-digit bound on the base.

**Non-identical worked bridge.** $(132)_5=1\cdot25+3\cdot5+2=42$. If the base were unknown, digit 3 would already force $b\ge4$.

**Close contrast.** Do not treat the written digits as a decimal number.

**Legality / boundary check.** Every digit must be less than its base; leading digit must be nonzero.

**Visual teaching object.** Base-$b$ place-value columns.

**Practice targets.** NT-Q008, NT-Q021, NT-Q029, NT-Q030, NT-Q031, NT-Q053, NT-Q056, NT-Q057

## NT-DIGSUM-01 · Digit-sum congruence and bounded digit sums

**What you probably remember.** $n\equiv s(n)\pmod9$.

**The missing IOQM link.** Modulo 9 gives a necessary congruence; exact digit-sum or extremal questions also need digit bounds and sometimes counting.

**Why this works.** Use $n\equiv s(n)\pmod9$ for congruence. For fixed length, digit sum is bounded by $9r$. To minimize a number with a prescribed digit sum, push mass to lower positions subject to digit caps.

**Try this first.** Decide whether the problem asks only for a congruence or for the exact digit sum.

**Non-identical worked bridge.** If $s(n)=37$, then $n\equiv37\equiv1\pmod9$. This does not determine $n$; it is only a congruence filter.

**Close contrast.** Exact change under addition is not controlled by mod 9 alone; use carry accounting.

**Legality / boundary check.** Respect number of digits and leading zeros when counting representations.

**Visual teaching object.** Digit-cap boxes / sum budget bar.

**Practice targets.** NT-Q011, NT-Q037, NT-Q045, NT-Q074

## NT-CARRY-01 · Exact carry accounting

**What you probably remember.** Carries change visible digits in addition.

**The missing IOQM link.** Each decimal carry lowers the naive digit-sum total by exactly 9.

**Why this works.** For ordinary addition, $s(a+b)=s(a)+s(b)-9C$, where $C$ is the total number of carries, including propagated carries.

**Try this first.** Set $C=(s(a)+s(b)-s(a+b))/9$.

**Non-identical worked bridge.** $58+67=125$: input digit sums total 26, output digit sum is 8, so $C=(26-8)/9=2$, matching the carries in units and tens.

**Close contrast.** Digit-sum congruence modulo 9 cannot tell you where or how many carries occur.

**Legality / boundary check.** Count propagated carries separately; a carry can trigger another carry in the next column.

**Visual teaching object.** Column-addition carry arrows.

**Practice targets.** NT-Q033, NT-Q074
