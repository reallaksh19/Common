# Number Theory Teaching Architecture v5 - Phase 2

# Unit 3 - Huge powers legally

## NT-ORDER-01 · Short residue cycles and multiplicative order

**What you probably remember.** Powers modulo a number often repeat.

**The missing IOQM link.** Use the shortest proven period available; do not automatically reduce exponents modulo the modulus or modulo phi.

**Why this works.** If $\gcd(a,m)=1$, the order $\operatorname{ord}_m(a)$ is the least positive $r$ with $a^r\equiv1\pmod m$, and exponents may be reduced modulo $r$.

**Try this first.** List a short cycle or prove an order before reducing the exponent.

**Non-identical worked bridge.** Modulo 10, $3,9,7,1$ repeats, so $3^{202}\equiv3^2\equiv9\pmod{10}$.

**Close contrast.** If the base is not coprime to the modulus, an order may not exist; use direct cycles or prime-power analysis.

**Legality / boundary check.** The period used must actually return to 1 for multiplicative-order reasoning.

**Visual teaching object.** Residue wheel or four-column cycle table.

**Practice targets.** NT-Q001, NT-Q025, NT-Q041, NT-Q042, NT-Q051, NT-Q072, NT-Q082

## NT-EULER-01 · Fermat, Euler and Euler phi

**What you probably remember.** Fermat and Euler reduce exponents.

**The missing IOQM link.** The theorem hypothesis is the real skill: verify primality/coprimality before reducing.

**Why this works.** Fermat: if $p$ is prime and $p\nmid a$, $a^{p-1}\equiv1\pmod p$. Euler: if $\gcd(a,n)=1$, $a^{\varphi(n)}\equiv1\pmod n$.

**Try this first.** Write the gcd or primality check before the theorem name.

**Non-identical worked bridge.** $2^{100}\pmod{13}$: $13$ is prime and $13\nmid2$, so reduce $100$ modulo $12$: $2^{100}\equiv2^4=16\equiv3$.

**Close contrast.** Euler gives a period, not necessarily the shortest period.

**Legality / boundary check.** Do not apply Euler when the base shares a factor with the modulus.

**Visual teaching object.** Theorem-choice gate: prime modulus? coprime base? short cycle cheaper?

**Practice targets.** NT-Q027, NT-Q028, NT-Q041, NT-Q042, NT-Q082, NT-Q087

## NT-WILSON-01 · Wilson's theorem

**What you probably remember.** Wilson is a prime-modulus factorial identity.

**The missing IOQM link.** It is narrow but decisive when a factorial stops at $p-1$ or can be paired with a few missing factors.

**Why this works.** For prime $p$, $(p-1)!\equiv-1\pmod p$.

**Try this first.** Check that the modulus is prime and try to rewrite the factorial expression around $(p-1)!$.

**Non-identical worked bridge.** $10!\equiv-1\equiv10\pmod{11}$.

**Close contrast.** Wilson is usually inefficient for arbitrary factorial divisibility; valuations are the correct tool there.

**Legality / boundary check.** The converse is also true for $n>1$, but do not assume primality without proving the exact Wilson congruence.

**Visual teaching object.** Inverse-pair diagram in the nonzero residues modulo a prime.

**Practice targets.** NT-Q034, NT-Q086

## NT-LASTDIG-01 · Last digits by prime-power splitting and CRT

**What you probably remember.** Last $k$ decimal digits mean modulo $10^k$.

**The missing IOQM link.** When the base is not coprime to $10^k$, split into $2^k$ and $5^k$ instead of forcing Euler modulo $10^k$.

**Why this works.** Solve the power problem separately modulo $2^k$ and $5^k$, using valuations/cycles/order as appropriate, then recombine by CRT.

**Try this first.** Write $10^k=2^k5^k$.

**Non-identical worked bridge.** For $3^{20}$ modulo 100: modulo 4 it is 1; modulo 25 the order divides 20 and $3^{20}\equiv1$. Hence the last two digits are 01.

**Close contrast.** A single cycle modulo 100 is fine if short and proven; prime-power splitting is the robust default.

**Legality / boundary check.** Pad leading zeros when the requested last $k$ digits form a number shorter than $k$ digits.

**Visual teaching object.** Two-lane mod $2^k$/mod $5^k$ split and CRT merge.

**Practice targets.** NT-Q001, NT-Q017, NT-Q054, NT-Q055, NT-Q072

## NT-EXPGCD-01 · GCDs of exponential expressions

**What you probably remember.** Expressions $a^n-1$ factor when exponents divide.

**The missing IOQM link.** The gcd itself follows the gcd of exponents.

**Why this works.** For $a>1$, $\gcd(a^m-1,a^n-1)=a^{\gcd(m,n)}-1$. Plus/minus variants need parity checks.

**Try this first.** Reduce the exponent pair with the Euclidean algorithm before touching the huge powers.

**Non-identical worked bridge.** $\gcd(2^{18}-1,2^{12}-1)=2^{\gcd(18,12)}-1=63$.

**Close contrast.** The same formula does not apply unchanged to $a^m+1$.

**Legality / boundary check.** Track whether quotient exponents are odd/even in plus/minus cases.

**Visual teaching object.** Exponent Euclidean algorithm above the exponential gcd identity.

**Practice targets.** NT-Q050

# Unit 4 - Prime exponents inside factorials and powers

## NT-VAL-01 · Valuations and Legendre's formula

**What you probably remember.** Factorials contain many repeated prime factors.

**The missing IOQM link.** Valuation turns divisibility by a huge composite into one inequality per prime.

**Why this works.** $v_p(ab)=v_p(a)+v_p(b)$, $v_p(a/b)=v_p(a)-v_p(b)$ when integral, and $v_p(n!)=\sum_{j\ge1}\lfloor n/p^j\rfloor$.

**Try this first.** Factor the target and write one $v_p$ inequality for each prime.

**Non-identical worked bridge.** $v_3(100!)=33+11+3+1=48$. Thus $3^{48}\mid100!$ but $3^{49}\nmid100!$.

**Close contrast.** Legendre's formula is for prime $p$, not a composite base.

**Legality / boundary check.** For $c^k\mid N$ with $c=\prod p_i^{e_i}$, require $e_i k\le v_{p_i}(N)$ for every prime factor.

**Visual teaching object.** Valuation staircase / floor-count ladder.

**Practice targets.** NT-Q003, NT-Q027, NT-Q034, NT-Q049, NT-Q052, NT-Q055, NT-Q071, NT-Q089

## NT-ZEROS-01 · Trailing zeros and last nonzero digits

**What you probably remember.** A decimal zero is a factor $10=2\cdot5$.

**The missing IOQM link.** Trailing zeros are paired 2s and 5s; last nonzero digits require removing the matched pairs before reducing modulo a power of 10.

**Why this works.** The number of trailing zeros of $n!$ is $\min(v_2(n!),v_5(n!))=v_5(n!)$. For last nonzero digits, remove matching $2^z5^z$ and work on the residue of the stripped value.

**Try this first.** Compute $z=v_5(n!)$ first.

**Non-identical worked bridge.** $100!$ has $20+4=24$ trailing zeros.

**Close contrast.** Digit-counting or decimal expansion is never the right route for a large factorial.

**Legality / boundary check.** For last nonzero digits, track leftover powers of 2 after removing the same number of 5s.

**Visual teaching object.** Factorial -> count 5s -> match 2s -> stripped residue pipeline.

**Practice targets.** NT-Q003

## NT-POWER-01 · Perfect powers and squarefree structure

**What you probably remember.** Squares have even prime exponents.

**The missing IOQM link.** Perfect $k$th powers and squarefree numbers are exponent-pattern statements, not shape-recognition by size.

**Why this works.** $n$ is a perfect $k$th power iff every prime exponent is divisible by $k$. It is squarefree iff every prime exponent is 0 or 1.

**Try this first.** Factor and mark each exponent modulo $k$ (or whether it exceeds 1).

**Non-identical worked bridge.** $72=2^3 3^2$. Multiplying by $2$ gives $2^4 3^2=144$, the least square multiple.

**Close contrast.** Checking only whether the numerical square root 'looks close' is not proof.

**Legality / boundary check.** For even powers over integers, sign matters if negative values are allowed.

**Visual teaching object.** Exponent parity/tile grid.

**Practice targets.** NT-Q005, NT-Q016, NT-Q023, NT-Q035, NT-Q040, NT-Q058, NT-Q064

## NT-RESIDUE-01 · Reduced residues, phi sums and unit products

**What you probably remember.** Euler phi counts residues coprime to $n$.

**The missing IOQM link.** Pairing and inverse-pair structure produce useful global sums/products without listing all units.

**Why this works.** For $n>1$, reduced residues pair $k\leftrightarrow n-k$, so their sum is $n\varphi(n)/2$. In many odd prime-power unit groups, inverse pairs leave only $\pm1$, giving total product $-1$.

**Try this first.** Ask whether pairing by $n-k$ or $u^{-1}$ preserves the set.

**Non-identical worked bridge.** Units modulo 10 are $1,3,7,9$; their sum is 20, matching $10\varphi(10)/2=20$.

**Close contrast.** Do not use the product claim for an arbitrary modulus without checking its self-inverse units.

**Legality / boundary check.** Pairing proofs need the set to be closed under the pairing map.

**Visual teaching object.** Reduced-residue pairing arcs / inverse-pair table.

**Practice targets.** NT-Q028, NT-Q087
