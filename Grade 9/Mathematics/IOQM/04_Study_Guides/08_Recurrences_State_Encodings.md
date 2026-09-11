# 8. Recurrences and state encodings

Recurrence problems are easiest when the state has a precise meaning. A recurrence is not a guessed formula; it is a counting identity supported by a disjoint decomposition.

## 8.1 Define what is being counted

Do not start with a symbol such as \(a_n\) unless you can finish the sentence:

> \(a_n\) counts ...

A useful state remembers exactly enough information to determine future choices.

Ask:

> Can two partial objects with the same proposed state have different legal continuations?

If yes, the state has forgotten something important.

## 8.2 Forbidden-substring encodings

Sometimes the original restriction becomes simpler after encoding changes between consecutive symbols.

For a binary string \(b_1b_2\ldots b_n\), define

\[
d_i=
\begin{cases}
1,&b_i\ne b_{i+1},\\
0,&b_i=b_{i+1}.
\end{cases}
\]

A complicated alternating pattern in \(b\) may become a simple “no adjacent 1s” condition in \(d\).

Binary strings of length \(m\) with no adjacent 1s satisfy a Fibonacci recurrence.

## 8.3 The standard no-adjacent-1 recurrence

Let \(s_n\) be the number of binary strings of length \(n\) with no adjacent 1s.

Split by the last digit:

- ending in 0: any valid length \(n-1\) string;
- ending in 1: the previous digit must be 0, so remove the final 01 and obtain any valid length \(n-2\) string.

Thus

\[
s_n=s_{n-1}+s_{n-2}.
\]

The structural split is the proof. Matching a few Fibonacci numbers is not the proof.

## 8.4 First stable piece

For permutations with a special prefix condition, classify every permutation by the **first** prefix at which a specified event occurs.

If every permutation has exactly one first such prefix, the classes are disjoint and exhaustive. This often yields a recurrence of the form

\[
n!=\sum_k (\text{admissible first block of size }k)(n-k)!.
\]

The word “first” is what prevents overlap.

## 8.5 Ratio substitution in nonlinear recurrences

A recurrence that looks nonlinear may become linear after dividing consecutive terms.

If terms contain

\[
\frac{a_{n-1}^2}{a_{n-2}},
\]

try dividing by \(a_{n-1}\) and define

\[
r_n=\frac{a_n}{a_{n-1}}.
\]

The recurrence for \(r_n\) may be much simpler than the recurrence for \(a_n\).

Before dividing, confirm the denominator is nonzero in the relevant sequence.

## 8.6 Base cases need meaning

If you write \(s_0=1\), explain what it counts. Usually it represents one empty configuration.

A recurrence without correct starting values does not determine the desired sequence.

## 8.7 Small-case verification

After deriving a recurrence, compute the first few cases independently. This catches:

- incorrect base values;
- a missing state;
- a branch counted twice;
- an impossible transition.

Small-case verification checks the derivation; it does not replace the derivation.

## What should I notice?

- local forbidden pattern → remember the smallest amount of recent history needed;
- alternating behavior → encode changes;
- unique first/last structural event → split there;
- nonlinear quotient pattern → try consecutive ratios;
- recurrence guess → verify the structural correspondence and base cases.

## Common mistakes

- guessing Fibonacci because early numbers look familiar;
- using a state that forgets information needed for future legality;
- writing base values without explaining what they count;
- dividing by a term without confirming it is nonzero;
- adding recurrence branches that overlap;
- using “first occurrence” language but then counting blocks that are not actually first.

## Appendix A practice

Questions **Q12, Q14, Q16**.
