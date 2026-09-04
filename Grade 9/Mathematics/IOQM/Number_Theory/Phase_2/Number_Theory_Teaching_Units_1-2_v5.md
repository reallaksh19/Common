# Number Theory Teaching Architecture v5 - Phase 2

# Unit 1 - Integer structure before tricks

## NT-DIV-01 · Divisibility and the Division Algorithm

**What you probably remember.** You know divisibility tests and that division leaves a quotient and remainder.

**The missing IOQM link.** IOQM wording such as 'same remainder', 'largest multiple', or 'not divisible' should be translated into equations or congruences before calculation.

**Why this works.** For integers $a$ and positive $b$, write $a=bq+r$ with $0\le r<b$. Thus $b\mid a\iff r=0$, and equal remainders disappear when two expressions are subtracted.

**Try this first.** Write $A=Bq+r$, $d\mid A$, or $A\equiv r\pmod d$ before manipulating the numbers.

**Non-identical worked bridge.** If $N\equiv5\pmod{37}$ and $M\equiv5\pmod{37}$, then $N-M\equiv0\pmod{37}$. The useful move is subtraction, not finding either large remainder again.

**Close contrast.** Do not use prime factorization merely because the word 'divides' appears; direct remainder algebra is cheaper when the modulus is already visible.

**Legality / boundary check.** Remainders must lie in the legal range; a modulus is positive; divisibility conclusions are exact, not approximate.

**Visual teaching object.** Short remainder-strip diagram only when several same-remainder conditions must be compared.

**Practice targets.** NT-Q009, NT-Q010, NT-Q022, NT-Q024, NT-Q046, NT-Q052, NT-Q071

## NT-GCD-01 · Euclidean Algorithm, GCD and LCM

**What you probably remember.** You know greatest common divisor and least common multiple.

**The missing IOQM link.** The Olympiad upgrade is that gcd is invariant under integer linear replacement: $\gcd(a,b)=\gcd(b,a-qb)$. This is an algorithm and a proof tool.

**Why this works.** Repeatedly replace the larger number by a remainder. Also $\gcd(a,b)\operatorname{lcm}(a,b)=ab$ for positive $a,b$.

**Try this first.** For a huge gcd, subtract or take a remainder immediately: $\gcd(A,B)=\gcd(B,A-qB)$.

**Non-identical worked bridge.** $\gcd(924,630)=\gcd(630,294)=\gcd(294,42)=42$. The same chain records integer combinations useful for Bézout.

**Close contrast.** Prime factorization is fine for small factored inputs, but the Euclidean algorithm is safer for large unfactored expressions.

**Legality / boundary check.** LCM formulas assume positive integers; keep integer coefficients when forming gcd-preserving combinations.

**Visual teaching object.** Euclidean reduction flow: pair -> remainder -> pair -> gcd.

**Practice targets.** NT-Q004, NT-Q038, NT-Q066, NT-Q067, NT-Q075, NT-Q083

## NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking

**What you probably remember.** Every integer greater than 1 factors into primes.

**The missing IOQM link.** Treat prime factorization as an exponent vector. Divisibility, squares, cubes, gcd and lcm are coordinate-wise statements.

**Why this works.** If $n=\prod p^{e_p}$, then $a\mid b$ iff $v_p(a)\le v_p(b)$ for every prime $p$. Euclid's Lemma is legal only when the divisor singled out is prime.

**Try this first.** Write the prime factorization or compare $v_p$ for an arbitrary prime $p$.

**Non-identical worked bridge.** If $p$ is prime and $p\mid x^2$, then $p\mid x$. In exponent language, $v_p(x^2)=2v_p(x)\ge1$, hence $v_p(x)\ge1$.

**Close contrast.** Do not apply 'if d divides ab, then d divides a or b' for a composite $d$; that statement is false.

**Legality / boundary check.** Separate prime factors before comparing exponents; uniqueness of FTA is what makes exponent conditions both necessary and sufficient.

**Visual teaching object.** Prime-exponent columns for two or three competing integers.

**Practice targets.** NT-Q002, NT-Q005, NT-Q013, NT-Q026, NT-Q032, NT-Q043, NT-Q069, NT-Q070

## NT-DIVCNT-01 · Exponent vectors and divisor functions

**What you probably remember.** Divisors come from choosing prime exponents.

**The missing IOQM link.** Many IOQM counting problems are rectangular lattice-point counts in exponent space.

**Why this works.** For $n=\prod p_i^{a_i}$, $\tau(n)=\prod(a_i+1)$ and $\sigma(n)=\prod(1+p_i+\cdots+p_i^{a_i})$. GCD uses coordinate-wise minima; LCM uses maxima.

**Try this first.** Factor $n$ and replace 'choose a divisor' by 'choose each exponent independently'.

**Non-identical worked bridge.** For $n=2^3 3^2$, a divisor is $2^i3^j$ with $0\le i\le3,\ 0\le j\le2$. Hence $\tau(n)=4\cdot3=12$.

**Close contrast.** Do not count numerical divisors one by one once the prime factorization is available.

**Legality / boundary check.** A condition such as 'multiple of 6' imposes lower bounds on selected exponents; 'square divisor' imposes parity conditions.

**Visual teaching object.** Exponent grid/lattice with allowed and forbidden cells.

**Practice targets.** NT-Q004, NT-Q016, NT-Q023, NT-Q027, NT-Q028, NT-Q035, NT-Q040, NT-Q087

# Unit 2 - GCD to congruences to CRT

## NT-DIO-LIN-01 · Bezout and linear Diophantine equations

**What you probably remember.** A gcd is a common divisor.

**The missing IOQM link.** Bézout makes the gcd constructive and gives the exact solvability test for $ax+by=c$.

**Why this works.** If $g=\gcd(a,b)$, then $au+bv=g$ for some integers $u,v$. Thus $ax+by=c$ has integer solutions iff $g\mid c$; from one solution, $x=x_0+(b/g)t,\ y=y_0-(a/g)t$.

**Try this first.** Compute $g=\gcd(a,b)$ and test $g\mid c$ before solving.

**Non-identical worked bridge.** For $14x+35y=7$, $g=7$. Divide by 7: $2x+5y=1$. One solution is $(-2,1)$; all are $x=-2+5t,\ y=1-2t$.

**Close contrast.** Do not impose positivity before writing the full integer family; that can hide valid parameter values.

**Legality / boundary check.** The all-solution formula assumes one integer solution; apply positivity/range restrictions afterward.

**Visual teaching object.** Line of integer solutions with parameter step vector $(b/g,-a/g)$.

**Practice targets.** NT-Q019, NT-Q038, NT-Q066, NT-Q067, NT-Q084, NT-Q090

## NT-MOD-01 · Congruence arithmetic and cancellation legality

**What you probably remember.** Congruence means 'same remainder'.

**The missing IOQM link.** Addition and multiplication are always legal; cancellation is conditional.

**Why this works.** From $ac\equiv bc\pmod m$, dividing by $c$ is legal only after accounting for $g=\gcd(c,m)$. If $g=1$, cancel directly; otherwise the modulus changes.

**Try this first.** Before cancelling, write $g=\gcd(c,m)$.

**Non-identical worked bridge.** $6x\equiv6\pmod{15}$ means $15\mid6(x-1)$. Divide the divisibility relation by $3$: $5\mid2(x-1)$, hence $x\equiv1\pmod5$, not modulo 15.

**Close contrast.** Never 'divide both sides and the modulus' blindly.

**Legality / boundary check.** Negative residues are fine, but state the final residue class modulo the intended modulus.

**Visual teaching object.** Cancellation legality box showing invertible vs non-invertible multiplier.

**Practice targets.** NT-Q009, NT-Q015, NT-Q017, NT-Q025, NT-Q038, NT-Q041, NT-Q042, NT-Q045, NT-Q054, NT-Q072, NT-Q075, NT-Q077, NT-Q080, NT-Q082

## NT-MODINV-01 · Linear congruences and modular inverses

**What you probably remember.** You can solve small congruences by trial.

**The missing IOQM link.** An inverse is a Bézout coefficient. It exists precisely when the coefficient is coprime to the modulus.

**Why this works.** $ax\equiv b\pmod m$ has solutions iff $\gcd(a,m)\mid b$. If $\gcd(a,m)=1$, multiply by $a^{-1}\pmod m$.

**Try this first.** Compute $g=\gcd(a,m)$; only then decide whether an inverse exists.

**Non-identical worked bridge.** $7x\equiv3\pmod{20}$. Since $7\cdot3=21\equiv1$, $7^{-1}\equiv3$, so $x\equiv9\pmod{20}$.

**Close contrast.** Do not search for an inverse when $\gcd(a,m)>1$; reduce the congruence first.

**Legality / boundary check.** Substitute one representative back into the original congruence.

**Visual teaching object.** Bézout -> inverse arrow diagram.

**Practice targets.** NT-Q015, NT-Q051, NT-Q084

## NT-CRT-01 · Constructive CRT, including non-coprime moduli

**What you probably remember.** You may remember CRT only for coprime moduli.

**The missing IOQM link.** For non-coprime moduli, compatibility is the first question; the merged modulus is the lcm, not the product.

**Why this works.** For $x\equiv a\pmod m,\ x\equiv b\pmod n$, solutions exist iff $a\equiv b\pmod{\gcd(m,n)}$. Set $x=a+mt$, substitute, solve the resulting linear congruence, then state the class modulo $\operatorname{lcm}(m,n)$.

**Try this first.** Set $x=a+mt$ and substitute into the other congruence.

**Non-identical worked bridge.** $x\equiv2\pmod6,\ x\equiv5\pmod9$. Compatibility holds mod 3. Put $x=2+6t$: $6t\equiv3\pmod9$, so $2t\equiv1\pmod3$, $t\equiv2\pmod3$. Hence $x\equiv14\pmod{18}$.

**Close contrast.** Multiplying moduli is wrong when they are not coprime.

**Legality / boundary check.** Always test compatibility and substitute the merged residue into every original congruence.

**Visual teaching object.** Split -> substitute -> compatibility -> merge flow.

**Practice targets.** NT-Q015, NT-Q017, NT-Q025, NT-Q054, NT-Q055, NT-Q085
