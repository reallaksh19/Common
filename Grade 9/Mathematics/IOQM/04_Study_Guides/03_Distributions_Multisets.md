# 3. Distributions, binomial counts and multiset selections

## 3.1 Stars and bars

The number of nonnegative integer solutions of

\[
x_1+x_2+\cdots+x_r=n
\]

is

\[
\binom{n+r-1}{r-1}.
\]

Why? Imagine \(n\) identical stars and \(r-1\) bars. The bars divide the stars into \(r\) named boxes.

This method is valid when the objects being distributed are identical and the recipients/categories are distinguishable.

## 3.2 Lower bounds

If

\[
x_i\ge a_i,
\]

satisfy the compulsory minimum first.

Let \(y_i=x_i-a_i\). Then \(y_i\ge0\), and the total is reduced by \(\sum a_i\).

### Teacher example

Find the number of integer solutions of

\[
x+y+z=14,\qquad x\ge2,\ y\ge3,\ z\ge1.
\]

Set

\[
u=x-2,\quad v=y-3,\quad w=z-1.
\]

Then

\[
u+v+w=8,\qquad u,v,w\ge0,
\]

so the count is

\[
\binom{10}{2}.
\]

## 3.3 Positive exponents in multinomial terms

A term such as

\[
a^w b^x c^y d^z
\]

with all four exponents positive is also a distribution problem. Subtract 1 from each required-positive exponent and count nonnegative solutions.

This is why many “how many terms occur?” questions are stars-and-bars problems in disguise.

If the expansion also contains a constant term such as 1, remember that the unused exponent can be a fifth nonnegative variable.

## 3.4 Repeated-letter selections

When letters have multiplicity limits, ordinary \(\binom nr\) may not work.

For a letter available \(m\) times, the choices of how many copies to take are represented by

\[
1+x+x^2+\cdots+x^m.
\]

Multiplying these expressions records all legal multiplicity combinations. The coefficient of \(x^r\) counts selections of \(r\) letters.

For short target lengths, a generating function may be more machinery than necessary. It can be quicker to classify multiplicity patterns such as

\[
2+2,\qquad 2+1+1,\qquad 1+1+1+1.
\]

## 3.5 Selection is different from arrangement

From the letters of a word:

- “select 4 letters” asks for allowed multiplicities, not order;
- “form a 4-letter word” asks for ordered arrangements.

Always decide this before writing a factorial.

## 3.6 One parameter can control several blocks

If equal totals and complementary restrictions force one block count to determine the others, introduce one integer parameter instead of launching a large inclusion–exclusion calculation.

For example, in three equal position-blocks with one letter forbidden from each block, choosing how many copies of one remaining letter go in the first block may force the remaining block counts by conservation of the total number of letters.

## 3.7 Capacity restrictions

If a word supplies only two copies of a letter, a multiplicity pattern requiring three copies is impossible. Before counting permutations, list the feasible multiplicity patterns and eliminate impossible ones.

This simple capacity check is especially valuable when a problem limits the number of distinct letters used.

## What should I notice?

- identical items distributed among named recipients → stars and bars;
- minimum amounts → subtract the minimum first;
- positive exponents in a multinomial term → shift by 1;
- repeated letters selected without order → multiplicity patterns or generating functions;
- several equal blocks with conservation → look for one controlling parameter;
- “at most three distinct letters” → list feasible multiplicity patterns before arranging.

## Common mistakes

- using stars and bars when objects are distinct;
- forgetting upper bounds imposed by limited letter multiplicities;
- confusing “select six letters” with “arrange six letters”;
- ignoring the exponent of a constant term in a multinomial expansion;
- using a generating function when a short multiplicity-pattern case split is easier;
- counting an impossible multiplicity pattern.

## Appendix A practice

Questions **Q6, Q10, Q11, Q22, Q39, Q55**.
