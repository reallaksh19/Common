# 5. Order patterns, inequalities and dictionary rank

This family looks diverse, but the common idea is to replace actual values by their **relative order** whenever the numerical values themselves are not important.

## 5.1 Forced order from inequalities

If selected values must satisfy inequalities, sort or compare them before counting assignments.

A pairing condition such as

\[
y\ge2x
\]

often creates a forced split between smaller and larger elements. Start with the largest possible smaller element, because it usually has the fewest legal partners.

This “most restricted first” principle is useful well beyond pairings: whenever one choice has only one or two legal continuations, place it before the flexible choices.

## 5.2 Arithmetic progression with fixed sum

For three numbers in arithmetic progression with total \(S\), the middle number is \(S/3\).

Write the terms as

\[
m-d,\quad m,\quad m+d.
\]

Then a geometry or integer problem often becomes a short count of the allowed integer values of \(d\).

### Teacher example

Three positive integer angles are in arithmetic progression and sum to \(180^\circ\). The middle angle is \(60^\circ\), so the angles are

\[
60-d,\quad60,\quad60+d.
\]

All remaining work is an integer bound on \(d\).

## 5.3 Sign reduction

An algebraic-looking counting problem may depend only on signs.

If a condition becomes

\[
x^2=\frac{u}{v},
\]

then real intersection may reduce to the requirement that \(u\) and \(v\) have the same sign. Instead of solving many equations, count orderings of the chosen coefficients that create the correct sign pattern.

A common error is to keep manipulating the algebra after the real content has already reduced to an ordering condition.

## 5.4 Alternating inequalities

A sequence with no three consecutive increasing and no three consecutive decreasing must have alternating comparison signs:

\[
<,>,<,>\ldots
\]

or

\[
>,<,>,<\ldots
\]

For distinct chosen values, count relative-order patterns before actual values.

When digits are involved, handle 0 separately if it might occupy the leading position.

## 5.5 Relative order of selected digits

Suppose four distinct digits are chosen. If the rule depends only on inequalities among them, first label them

\[
x_1<x_2<x_3<x_4
\]

and count the legal permutations of these ranks. Only afterward choose the actual digits.

This separates two tasks:

1. choose the values;
2. arrange their relative order.

## 5.6 Dictionary rank with distinct letters

To find the rank of a word among all permutations in dictionary order:

1. scan from left to right;
2. at each position count smaller available letters;
3. for each smaller choice, count all permutations of the remaining letters;
4. remove the actual chosen letter and continue;
5. add 1 at the end for the word itself.

### Teacher example

To rank CAB among permutations of A,B,C:

- before C at the first position, A or B could appear: \(2\cdot2!=4\) earlier words;
- after fixing C, before A there is no smaller remaining letter;
- add 1 for CAB itself.

So its rank is \(5\).

## 5.7 Dictionary rank with repeated letters

If remaining letters have multiplicities, divide the suffix permutation count by the corresponding factorials.

For a remaining multiset \(A,A,B,C\), the number of distinct suffixes is

\[
\frac{4!}{2!}.
\]

At every rank step, recompute using the multiplicities **after** the hypothetical smaller letter has been chosen.

## 5.8 Fixed leading digit with a repeated-pair pattern

If a number begins with a fixed digit and must have multiplicity pattern \(2,1,1\), split according to whether the fixed leading digit is the repeated digit or not. This prevents both leading-zero mistakes and incorrect repeated-digit counts.

## What should I notice?

- conditions use only \(<\) and \(>\) → count order patterns;
- “dictionary order” → position-by-position smaller-letter count;
- repeated letters in rank → multiset permutations;
- pairing inequality → start from the most restricted element;
- algebraic intersection → simplify to a sign or ordering condition before counting;
- fixed leading digit plus repeated digit → split according to which digit repeats.

## Common mistakes

- counting actual numerical values when only relative order matters;
- forgetting that 0 cannot lead a number;
- forgetting the final \(+1\) in dictionary rank;
- treating repeated letters as distinct in rank calculations;
- counting both orderings of an unordered pair of curves or objects when the problem says their order does not matter;
- missing a strict inequality or positivity endpoint when counting the parameter \(d\).

## Appendix A practice

Questions **Q1, Q5, Q7, Q13, Q15, Q43, Q44, Q45**.
