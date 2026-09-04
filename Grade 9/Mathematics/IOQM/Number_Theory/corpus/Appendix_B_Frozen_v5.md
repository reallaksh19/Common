# Appendix B - 20 Reliable-Source Number Theory Challenges

These items retain their published contest IDs. They are an audit set beyond Appendix A, not evidence of marathon provenance. Answers were independently checked in the prior build and retained here.

## B01 · 2019 AIME I, Problem 1

Let $N$ be the sum of the numbers consisting of $1,2,\ldots,321$ consecutive digits $9$ respectively. Find the sum of the decimal digits of $N$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
A long sum of strings of 9s is best rewritten through powers of 10, not added digit-by-digit.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-DIGIT-01 · Decimal place value, concatenation and deletion` and `NT-DIGSUM-01 · Digit-sum congruence and bounded digit sums` before continuing.
\end{tcolorbox}
\medskip
## B02 · 2019 AIME I, Problem 7

Positive integers $x,y$ satisfy

$$
\log_{10}x+2\log_{10}(\gcd(x,y))=60,
$$
$$
\log_{10}y+2\log_{10}(\operatorname{lcm}(x,y))=570.
$$

Let $m,n$ be the numbers of prime factors of $x,y$, respectively, counted with multiplicity. Find $3m+2n$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
The logarithms turn products into prime-exponent equations; the gcd controls the shared exponents.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-GCD-01 · Euclidean Algorithm, GCD and LCM` and `NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking` before continuing.
\end{tcolorbox}
\medskip
## B03 · 2019 AIME I, Problem 9

Let $\tau(n)$ be the number of positive divisors of $n$. Find the sum of the six least positive integers $n$ satisfying

$$
\tau(n)+\tau(n+1)=7.
$$

\begin{tcolorbox}[hintone,title={H1 - Notice}]
The equation tau(n)+tau(n+1)=7 leaves only a few divisor-count patterns.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-DIVCNT-01 · Exponent vectors and divisor functions` and `NT-COUNT-01 · Fixed-multiplicity and digit-choice counting` before continuing.
\end{tcolorbox}
\medskip
## B04 · 2019 AIME II, Problem 9

Call $n$ *20-pretty* if $20\mid n$ and $n$ has exactly $20$ positive divisors. Let $S$ be the sum of all 20-pretty positive integers below $2019$. Find $S/20$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Exactly 20 divisors means a short list of exponent patterns before the divisibility-by-20 condition is applied.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-DIVCNT-01 · Exponent vectors and divisor functions` and `NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters` before continuing.
\end{tcolorbox}
\medskip
## B05 · 2020 AIME I, Problem 10

Positive integers $m,n$ satisfy $\gcd(m+n,210)=1$, $n^n\mid m^m$, and $n\nmid m$. Find the least possible $m+n$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
The divisibility n^n | m^m is a prime-exponent comparison, and gcd(m+n,210)=1 removes small-prime coincidences.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-VAL-01 · Valuations and Legendre's formula` and `NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking` before continuing.
\end{tcolorbox}
\medskip
## B06 · 2020 AIME II, Problem 1

Find the number of ordered pairs of positive integers $(m,n)$ such that

$$
m^2n=20^{20}.
$$

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Factor 20^20 and compare prime exponents in m^2n.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-POWER-01 · Perfect powers and squarefree structure` and `NT-DIVCNT-01 · Exponent vectors and divisor functions` before continuing.
\end{tcolorbox}
\medskip
## B07 · 2020 AMC 10B, Problem 24

How many positive integers $n$ satisfy

$$
\frac{n+1000}{70}=\lfloor\sqrt n\rfloor?
$$

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Replace floor(sqrt n) by an integer k and convert the equation into an interval condition.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-FLOOR-01 · Floor functions as half-open intervals` and `NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters` before continuing.
\end{tcolorbox}
\begin{tcolorbox}[hintthree,title={H3 - Start}]
Set k=floor(sqrt n), so k^2<=n<(k+1)^2, and substitute n=70k-1000.
\end{tcolorbox}
\medskip
## B08 · 2020 AMC 10B, Problem 25

Let $D(N)$ be the number of ordered factorizations of $N$ into integers greater than $1$, including the one-factor factorization. For example $D(6)=3$ from $6,2\cdot3,3\cdot2$. Find $D(96)$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Ordered factorisations of 96 are compositions of its prime-exponent multiset, not just unordered divisor pairs.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-DIVCNT-01 · Exponent vectors and divisor functions` and `NT-COUNT-01 · Fixed-multiplicity and digit-choice counting` before continuing.
\end{tcolorbox}
\medskip
## B09 · 2021 AIME II, Problem 1

Find the arithmetic mean of all three-digit palindromes.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Three-digit palindromes are linear in the first and middle digits, so average by symmetry.
\end{tcolorbox}
\medskip
## B10 · 2021 AIME II, Problem 3

Find the number of permutations $x_1,\ldots,x_5$ of $1,2,3,4,5$ such that

$$
x_1x_2x_3+x_2x_3x_4+x_3x_4x_5+x_4x_5x_1+x_5x_1x_2
$$

is divisible by $3$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
The expression is cyclic and symmetric over a permutation; count by a structural invariant rather than 120 raw cases.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-COUNT-01 · Fixed-multiplicity and digit-choice counting` before continuing.
\end{tcolorbox}
\medskip
## B11 · 2022 AIME II, Problem 14

For $a<b<c$, consider stamp collections using denominations $a,b,c$, with at least one of each, capable through subcollections of forming every value from $1$ through $1000$. Let $f(a,b,c)$ be the minimum collection size. Find the sum of the three least $c$ for which $f(a,b,c)=97$ for some $a,b$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
The subcollection requirement is a coverage condition; small denominations force successive gap bounds.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-DIO-LIN-01 · Bezout and linear Diophantine equations` and `NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters` before continuing.
\end{tcolorbox}
\medskip
## B12 · 2014 AIME I, Problem 8

A positive integer $N$ and $N^2$ end in the same four-digit block $abcd$, with $a\ne0$. Find the three-digit number $abc$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Same four-digit ending is the idempotent congruence N^2 congruent to N modulo 10000.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-CRT-01 · Constructive CRT, including non-coprime moduli` and `NT-A02 · Idempotents: same ending for N and N^2` before continuing.
\end{tcolorbox}
\begin{tcolorbox}[hintthree,title={H3 - Start}]
Split N^2 congruent to N modulo 10000 into mod 16 and mod 625.
\end{tcolorbox}
\medskip
## B13 · 2005 AMC 10A, Problem 24

Let $P(n)$ be the greatest prime factor of $n>1$. For how many positive integers $n$ do both

$$
P(n)=\sqrt n,\qquad P(n+48)=\sqrt{n+48}
$$

hold?

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Greatest prime factor equal to the square root forces a prime square.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking` and `NT-FACT-POW-01 · Difference/sum-of-powers factorisation` before continuing.
\end{tcolorbox}
\medskip
## B14 · 2021 AIME I, Problem 5

A strictly increasing three-term integer arithmetic progression is called special when the sum of the squares of its terms equals the middle term times the square of the common difference. Find the sum of the third terms of all special progressions.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Center the arithmetic progression and turn the condition into a finite Diophantine equation.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-FACT-SFFT-01 · Manufactured factorisation and fixed-product forms` and `NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters` before continuing.
\end{tcolorbox}
\medskip
## B15 · 2016 AIME II, Problem 11

Call $N$ *$k$-nice* if some $a^k$ has exactly $N$ positive divisors. How many positive integers below $1000$ are neither 7-nice nor 8-nice?

\begin{tcolorbox}[hintone,title={H1 - Notice}]
For tau(a^k), every factor is 1 modulo k.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-DIVCNT-01 · Exponent vectors and divisor functions` and `NT-POWER-01 · Perfect powers and squarefree structure` before continuing.
\end{tcolorbox}
\medskip
## B16 · 2008 AIME II, Problem 15

Find the largest integer $n$ such that $n^2$ is the difference of two consecutive positive cubes and $2n+79$ is a perfect square.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Factor the difference of consecutive cubes before combining with the second square condition.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-FACT-POW-01 · Difference/sum-of-powers factorisation` and `NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters` before continuing.
\end{tcolorbox}
\begin{tcolorbox}[hintthree,title={H3 - Start}]
Write (m+1)^3-m^3 explicitly and equate it to n^2.
\end{tcolorbox}
\medskip
## B17 · 2022 AIME I, Problem 2

Find the three-digit decimal integer $\overline{abc}$ whose base-$9$ representation is $\overline{bca}_9$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Write the decimal and base-9 place-value equations for the same digit triple.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-BASE-01 · Other bases and digit validity` and `NT-DIGIT-01 · Decimal place value, concatenation and deletion` before continuing.
\end{tcolorbox}
\medskip
## B18 · 2012 AIME I, Problem 1

How many three-digit positive integers $\overline{abc}$ with $a,c\ne0$ have both $\overline{abc}$ and $\overline{cba}$ divisible by $4$?

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Divisibility by 4 depends only on the final two digits of each orientation.
\end{tcolorbox}
\medskip
## B19 · 2021 AMC 12A, Problem 5

A student multiplies $66$ by $1.\overline{ab}$ but misreads it as the terminating decimal $1.ab$. The incorrect result is $0.5$ less than the correct result. Find the two-digit number $\overline{ab}$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
The error between repeating and terminating decimals is a rational expression in the two-digit block.
\end{tcolorbox}
\medskip
## B20 · 2017 AIME I, Problem 9

Let $a_{10}=10$ and, for $n>10$,

$$
a_n=100a_{n-1}+n.
$$

Find the least $n>10$ such that $99\mid a_n$.

\begin{tcolorbox}[hintone,title={H1 - Notice}]
Reduce the recurrence modulo 99 before iterating.
\end{tcolorbox}
\begin{tcolorbox}[hinttwo,title={H2 - Recall}]
Review `NT-REC-01 · Affine recurrences modulo a target` and `NT-MOD-01 · Congruence arithmetic and cancellation legality` before continuing.
\end{tcolorbox}
\begin{tcolorbox}[hintthree,title={H3 - Start}]
Use 100 congruent to 1 modulo 99 to obtain a_n congruent to a_{n-1}+n.
\end{tcolorbox}
\medskip

## Appendix B method-coverage table

| Item | Primary methods |
|---|---|
| B01 | NT-DIGIT-01 · Decimal place value, concatenation and deletion; NT-DIGSUM-01 · Digit-sum congruence and bounded digit sums |
| B02 | NT-GCD-01 · Euclidean Algorithm, GCD and LCM; NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking |
| B03 | NT-DIVCNT-01 · Exponent vectors and divisor functions; NT-COUNT-01 · Fixed-multiplicity and digit-choice counting |
| B04 | NT-DIVCNT-01 · Exponent vectors and divisor functions; NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters |
| B05 | NT-VAL-01 · Valuations and Legendre's formula; NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking |
| B06 | NT-POWER-01 · Perfect powers and squarefree structure; NT-DIVCNT-01 · Exponent vectors and divisor functions |
| B07 | NT-FLOOR-01 · Floor functions as half-open intervals; NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters |
| B08 | NT-DIVCNT-01 · Exponent vectors and divisor functions; NT-COUNT-01 · Fixed-multiplicity and digit-choice counting |
| B09 | NT-DIGIT-01 · Decimal place value, concatenation and deletion; NT-COUNT-01 · Fixed-multiplicity and digit-choice counting |
| B10 | NT-COUNT-01 · Fixed-multiplicity and digit-choice counting |
| B11 | NT-DIO-LIN-01 · Bezout and linear Diophantine equations; NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters |
| B12 | NT-CRT-01 · Constructive CRT, including non-coprime moduli; NT-A02 · Idempotents: same ending for N and N^2 |
| B13 | NT-PRIME-01 · Euclid's Lemma, FTA and prime-exponent thinking; NT-FACT-POW-01 · Difference/sum-of-powers factorisation |
| B14 | NT-FACT-SFFT-01 · Manufactured factorisation and fixed-product forms; NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters |
| B15 | NT-DIVCNT-01 · Exponent vectors and divisor functions; NT-POWER-01 · Perfect powers and squarefree structure |
| B16 | NT-FACT-POW-01 · Difference/sum-of-powers factorisation; NT-FILTER-01 · Parity, bounds, discriminants and admissibility filters |
| B17 | NT-BASE-01 · Other bases and digit validity; NT-DIGIT-01 · Decimal place value, concatenation and deletion |
| B18 | NT-DIV-01 · Divisibility and the Division Algorithm; NT-DIGIT-01 · Decimal place value, concatenation and deletion |
| B19 | NT-DIGIT-01 · Decimal place value, concatenation and deletion; NT-DIGSUM-01 · Digit-sum congruence and bounded digit sums |
| B20 | NT-REC-01 · Affine recurrences modulo a target; NT-MOD-01 · Congruence arithmetic and cancellation legality |

# Appendix B Answer Key

| B | Answer | B | Answer |
|---:|---:|---:|---:|
| 1 | 342 | 11 | 188 |
| 2 | 880 | 12 | 937 |
| 3 | 540 | 13 | 1 |
| 4 | 472 | 14 | 31 |
| 5 | 407 | 15 | 749 |
| 6 | 231 | 16 | 181 |
| 7 | 6 | 17 | 227 |
| 8 | 112 | 18 | 40 |
| 9 | 550 | 19 | 75 |
| 10 | 80 | 20 | 45 |

\newpage
