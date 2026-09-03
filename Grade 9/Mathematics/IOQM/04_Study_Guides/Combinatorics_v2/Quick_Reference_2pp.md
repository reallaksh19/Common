# IOQM Grade 9 Combinatorics — Two-Page Quick Reference

Use this only **after** you understand the main guide. It is a memory sheet, not a substitute for reasoning.

# Page 1 — Counting and arrangements

## First six questions to ask

1. What is one outcome?
2. Does order matter?
3. Is there a strong restriction to handle first?
4. Would the complement be shorter?
5. Are my cases disjoint?
6. Is there a better representation: blocks, gaps, graph, state, prime exponents?

## Core formulas

### Ordered choices

\[
{}^nP_r=\frac{n!}{(n-r)!}
\]

### Unordered choices

\[
\binom nr=\frac{n!}{r!(n-r)!}
\]

### Repeated objects

If \(n\) positions contain multiplicities \(m_1,m_2,\ldots\),

\[
\frac{n!}{m_1!m_2!\cdots}.
\]

### Stars and bars

\[
x_1+\cdots+x_r=n,\quad x_i\ge0
\]

has

\[
\binom{n+r-1}{r-1}
\]

solutions.

For positive variables, give 1 to each first.

### Complement

\[
\#(\text{wanted})=\#(\text{all})-\#(\text{opposite}).
\]

Typical words: **at least one, not all, some adjacency**.

### Inclusion–exclusion

Two bad events:

\[
|A\cup B|=|A|+|B|-|A\cap B|.
\]

Three bad events: singles minus pairwise intersections plus triple intersection.

## Blocks, gaps and derangements

- must be together → block;
- must be separated → arrange separators first, then use gaps;
- no one in original position → derangement.

\[
D_1=0,\quad D_2=1,\quad D_3=2,\quad D_4=9,\quad D_5=44
\]

and

\[
D_n=(n-1)(D_{n-1}+D_{n-2}).
\]

## Circular arrangements

- \(n\) distinct people around ordinary round table:

\[
(n-1)!.
\]

- numbered circular seats: usually \(n!\);
- on a circle there are as many gaps as placed separators;
- always check last-first adjacency.

## Dictionary rank

At each position:

\[
(\text{smaller available choices})
\times
(\text{number of suffix arrangements}).
\]

With repeated letters, divide suffix counts by multiplicity factorials.

---

# Page 2 — Graphs, recurrences, number theory and strategy

## Graph counting

### Handshake lemma

\[
\sum_vd(v)=2|E|.
\]

### Pair \(2n\) labeled objects

\[
\frac{(2n)!}{2^n n!}.
\]

### Undirected \(k\)-cycle on a chosen \(k\)-set

\[
\frac{(k-1)!}{2}.
\]

Degree 2 at every vertex means a disjoint union of cycles.

### Proper coloring of a cycle

\[
P(C_n,q)=(q-1)^n+(-1)^n(q-1).
\]

## Recurrence reminders

- define exactly what \(a_n\) counts;
- branches must be disjoint and complete;
- local forbidden strings → remember only recent history;
- \(010/101\) restrictions may simplify by encoding symbol changes;
- nonlinear recurrence with \(a_{n-1}^2/a_{n-2}\) → try \(a_n/a_{n-1}\);
- target has few predecessors → work backward.

No-adjacent-1 strings:

\[
s_n=s_{n-1}+s_{n-2},\quad s_0=1,\ s_1=2.
\]

## Number-theoretic counting

If

\[
n=\prod p_i^{a_i},
\]

then

\[
\tau(n)=\prod(a_i+1).
\]

Factor pairs:

\[
\frac{\tau(n)}2
\]

if \(n\) is nonsquare, and

\[
\frac{\tau(n)+1}{2}
\]

if \(n\) is square.

Largest \(m^k\mid N\): factor \(m\), compare prime valuations, take the smallest resulting bound.

Divisibility by 3 or 9: count digit residue patterns before actual digits.

## Symmetry

- ordinary circle: remove rotational duplication by fixing one object;
- rotation + reflection: classify necklaces/garlands or use Burnside;
- cube rotations: 24;
- never divide by a symmetry number unless every raw object has the expected orbit size.

## Pigeonhole

More objects than boxes forces a collision.

General form:

\[
\text{some box has at least }
\left\lceil\frac Nm\right\rceil.
\]

The hard part is choosing useful boxes.

## Invariants and games

Common invariants: parity, residue, checkerboard color balance.

For a take-away game, find losing positions and move the opponent into one.

Example: remove 1, 2 or 3 stones, last wins → multiples of 4 are losing positions.

## Final 20-second check

Before submitting:

- Did I count the right object?
- Did I confuse ordered and unordered?
- Do my cases overlap?
- Did I forget leading zero or wrap-around?
- Did I divide by symmetry legally?
- Did I count every valid object exactly once?
