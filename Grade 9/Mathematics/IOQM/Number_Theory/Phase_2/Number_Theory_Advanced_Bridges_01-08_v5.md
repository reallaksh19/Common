# Number Theory Advanced Worked Bridges v5 - Phase 2

## NT-A01 · Zero-stripped factorials: valuations plus a ratio

**Recognition cue.** Two neighboring factorials are compared after deleting trailing zeros.

**Why this method fits.** Let $Z(n)$ be $n!$ with trailing zeros removed. If $t=v_5(n+1)$, multiplying by $n+1$ creates exactly $t$ new factors of 5; pair them with $t$ available 2s.

**First line.** Write $t=v_5(n+1)$ and compare $Z(n+1)/Z(n)$ after removing the $10^t$ contribution.

**Execution bridge.** Factor $n+1=5^t u$ with $5\nmid u$. Before zero deletion, $(n+1)!=(n+1)n!$. The new $5^t$ must be paired with $2^t$, so the zero-stripped ratio is controlled by $u/2^t$ together with the excess 2-adic supply already present. This turns a factorial comparison into a small valuation case split.

**Legality / equality check.** Track both 2s and 5s; zero deletion removes matched pairs only.

**Nearby wrong approach.** Computing the factorials or their decimal endings directly.

**Transfer prompt.** Transfer: compare zero-stripped $49!$ and $50!$ without expanding either factorial.

## NT-A02 · Idempotents: same ending for N and N^2

**Recognition cue.** A number and its square have the same final $k$ digits.

**Why this method fits.** Translate to $N^2\equiv N\pmod{10^k}$, hence $N(N-1)\equiv0$. Consecutive factors are coprime.

**First line.** Split $10^k$ into $2^k$ and $5^k$; on each prime-power side $N\equiv0$ or $1$.

**Execution bridge.** Because $\gcd(N,N-1)=1$, a full prime power dividing the product must lie entirely in one factor. Thus each prime-power modulus gives two idempotent choices. Recombine choices by CRT. For decimal moduli this gives only a small finite set of possible endings.

**Legality / equality check.** The conclusion 0 or 1 is prime-power-by-prime-power, not automatically modulo a composite modulus.

**Nearby wrong approach.** Trying to solve the quadratic congruence by ordinary real factoring alone.

**Transfer prompt.** Transfer: list idempotents modulo 100.

## NT-A03 · Complete unit-group products

**Recognition cue.** A huge product runs through all invertible residues, possibly after a permutation.

**Why this method fits.** Pair each unit with its inverse; most pairs multiply to 1.

**First line.** Prove the indexing map permutes the unit set, then replace the product by the product of all units.

**Execution bridge.** For an odd prime power, the only self-inverse units are typically $\pm1$. Every other unit pairs with a distinct inverse, so the product collapses to $-1$. If a translation or exponent map permutes the units, the original product has the same value.

**Legality / equality check.** Check the modulus and self-inverse solutions; the statement is not universal for every composite modulus.

**Nearby wrong approach.** Multiplying a long block term by term.

**Transfer prompt.** Transfer: evaluate the product of all nonzero residues modulo an odd prime.

## NT-A04 · Two-adic filtering through Euler phi

**Recognition cue.** A divisibility by $\varphi(n)$ is constrained by the exact power of 2 in another expression.

**Why this method fits.** Write $n=2^a\prod p_i^{e_i}$ and inspect $v_2(\varphi(n))$.

**First line.** Compare the required $v_2$ on both sides before considering odd factors.

**Execution bridge.** $\varphi(n)=2^{a-1}\prod p_i^{e_i-1}(p_i-1)$. Each odd prime contributes at least one factor 2 through $p_i-1$. Therefore a tiny upper bound on $v_2(\varphi(n))$ sharply limits the number of odd prime factors and the value of $a$. Only then inspect remaining divisibility conditions.

**Legality / equality check.** Do not forget the $2^{a-1}$ contribution when $a\ge1$.

**Nearby wrong approach.** Enumerating n first and computing phi repeatedly.

**Transfer prompt.** Transfer: classify $n$ for which $v_2(\varphi(n))\le1$.

## NT-A05 · Reduced-residue sums plus geometric series

**Recognition cue.** A sum ranges over numbers with independent prime exponents and contains a reduced-residue statistic.

**Why this method fits.** Use $\sum_{(k,n)=1}k=n\varphi(n)/2$ first; then write the allowed integer as a prime-power product.

**First line.** Separate the multiple sum into one geometric series per prime exponent.

**Execution bridge.** After substituting the phi formula, the summand often factors as $A_aB_bC_c$. Independence of exponents gives $\sum_{a,b,c}A_aB_bC_c=(\sum A_a)(\sum B_b)(\sum C_c)$. The apparently infinite number-theory sum becomes elementary geometric series.

**Legality / equality check.** Check lower bounds on exponents: 'divisible by 2,3,5' means each exponent starts at 1.

**Nearby wrong approach.** Adding sample values and guessing convergence.

**Transfer prompt.** Transfer: evaluate a reciprocal sum over numbers $2^a3^b$ with $a,b\ge1$.

## NT-A06 · GCD of several linear forms

**Recognition cue.** A gcd is taken across several linear expressions in primitive variables.

**Why this method fits.** Any common divisor of the forms divides every integer linear combination of them.

**First line.** Search for integer combinations that isolate $Ca,Cb,Cc$.

**Execution bridge.** If $g\mid L_1,L_2,L_3$, construct combinations such as $\alpha L_1+\beta L_2+\gamma L_3=Ca$. Repeat for $b,c$. If $\gcd(a,b,c)=1$, then $g\mid C$. The whole gcd is now bounded by a small constant; finish by constructing equality.

**Legality / equality check.** Coefficients in the combinations must be integers.

**Nearby wrong approach.** Factoring each linear form separately.

**Transfer prompt.** Transfer: bound $\gcd(a+b,b+c,c+a)$ when $\gcd(a,b,c)=1$.

## NT-A07 · Exponential GCDs and parity of exponents

**Recognition cue.** A gcd mixes $a^m+1$ with $a^n-1$.

**Why this method fits.** Convert the plus expression using $(a^m+1)(a^m-1)=a^{2m}-1$.

**First line.** Reduce to gcds of minus-one expressions and compare 2-adic valuations of exponents.

**Execution bridge.** The identity for $a^r-1$ reduces the problem to $\gcd(2m,n)$ and $\gcd(m,n)$. The extra factor from $a^m+1$ survives precisely when the power of 2 in $n$ exceeds that in $m$. Only after this reduction should a counting problem over pairs $(m,n)$ begin.

**Legality / equality check.** Parity conditions are essential; do not copy the minus-minus formula to a plus-minus gcd.

**Nearby wrong approach.** Testing many exponent pairs numerically.

**Transfer prompt.** Transfer: determine when $3^m+1$ and $3^n-1$ can share an odd factor.

## NT-A08 · Last nonzero digits of a factorial

**Recognition cue.** The target is the last one/two nonzero digits of $n!$.

**Why this method fits.** Count zeros by $v_5$, remove matched 2s and 5s, then work modulo the required power of 10.

**First line.** For two digits, split the stripped residue modulo 4 and 25.

**Execution bridge.** Let $z=v_5(n!)$. Remove $5^z$ and $2^z$. Modulo 4, excess powers of 2 often force 0. Modulo 25, multiply the 5-free parts of factors and the leftover 2-powers, exploiting short cycles. Recombine the two residues by CRT.

**Legality / equality check.** Never reduce $n!$ modulo 100 before removing zeros: it becomes 0 and loses the information.

**Nearby wrong approach.** Computing the decimal factorial or repeatedly deleting zeros.

**Transfer prompt.** Transfer: design the calculation for the last two nonzero digits of $50!$.
