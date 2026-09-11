# 9. Number-theoretic counting and divisibility

Some counting questions are really divisor-structure problems. The fastest solution often comes from prime exponents rather than from combinatorial enumeration.

## 9.1 Divisor count

If

\[
n=p_1^{a_1}p_2^{a_2}\cdots p_r^{a_r},
\]

then

\[
\tau(n)=(a_1+1)(a_2+1)\cdots(a_r+1).
\]

Each divisor is determined by independently choosing the exponent of every prime:

\[
0\le e_i\le a_i.
\]

This is a multiplication-principle argument in prime-exponent form.

## 9.2 Unordered factor pairs

Divisors pair as \(d\) and \(n/d\).

- If \(n\) is not a square, the number of unordered factor pairs is \(\tau(n)/2\).
- If \(n\) is a square, \(\sqrt n\) pairs with itself, so the count is

\[
\frac{\tau(n)+1}{2}.
\]

### Teacher check

Always test whether \(n\) is a square before halving the divisor count.

## 9.3 Product of all divisors

For a nonsquare \(n\), pair each divisor \(d\) with \(n/d\). Every pair has product \(n\), and there are \(\tau(n)/2\) pairs. Hence

\[
\prod_{d\mid n}d=n^{\tau(n)/2}.
\]

For a square, the same pairing leaves \(\sqrt n\) unpaired; handle that middle divisor explicitly if you want to stay entirely in integer exponents.

## 9.4 Greatest power of a composite divisor

To ask how large a power of a composite number \(m\) divides a quantity, factor \(m\) and compare prime exponents.

If

\[
m=2^\alpha3^\beta,
\]

then \(m^x\mid N\) requires

\[
\alpha x\le v_2(N),\qquad \beta x\le v_3(N).
\]

So the maximum \(x\) is determined by the most restrictive prime.

This is safer than repeatedly dividing by the composite number.

## 9.5 Divisors lost after lowering an exponent

Divisors of

\[
p^aq^b
\]

correspond to lattice points

\[
(i,j),\qquad0\le i\le a,\quad0\le j\le b.
\]

Comparing \(p^aq^b\) with \(p^{a-1}q^{b-1}\) removes the top row and right column of the exponent grid, with the top-right corner counted once.

This picture turns a huge-exponent problem into a boundary count.

## 9.6 Digit divisibility

For divisibility by 3 or 9, use residues or digit sums **before** counting arrangements.

Suppose the allowed digits fall into residue classes modulo 3. First determine which residue triples have sum \(0\pmod3\). Then count actual digit choices realizing those residue patterns.

This order avoids listing all numerical possibilities.

## 9.7 Counting with repetition allowed

When digit repetition is allowed, each position is a fresh choice from the allowed digit set, subject only to the global divisibility condition and any leading-digit rule.

If all allowed digits are nonzero, there is no leading-zero issue. If 0 is allowed, the first position must be handled separately.

## What should I notice?

- factor pairs → compute \(\tau(n)\);
- product of divisors → pair complementary divisors;
- greatest power dividing something → compare prime valuations;
- one exponent lowered → exponent-grid boundary;
- divisible by 3 or 9 → residue/digit-sum filter before enumeration;
- huge numerical exponents → look for structure before calculation.

## Common mistakes

- halving \(\tau(n)\) without checking whether \(n\) is a square;
- comparing powers of a composite number without separating primes;
- counting exponent-grid rows and columns without correcting their intersection;
- counting digit strings before checking divisibility constraints;
- forgetting a leading-zero restriction when 0 is among the allowed digits;
- expanding a huge power numerically instead of working with its prime exponents.

## Appendix A practice

Questions **Q26, Q27, Q29, Q38**.
