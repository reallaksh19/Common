# 4. Linear arrangements, blocks and adjacency

## 4.1 Permutations of distinct objects

\(n\) distinct objects in a row can be arranged in

\[
n!
\]

ways.

If some objects are identical, divide by the factorials of their multiplicities:

\[
\frac{n!}{m_1!m_2!\cdots}.
\]

This division is not a trick. It corrects for swaps of identical copies that do not change the visible arrangement.

## 4.2 The block method

If two specified objects must be adjacent, temporarily treat them as one block.

If \(A,B\) must be together among 6 distinct objects, count the block plus the other 4 objects:

\[
5!\cdot2!,
\]

because the internal order \(AB\) or \(BA\) also matters.

If repeated identical letters form the block, there may be no internal factor. For example, an identical pair \(AA\) contributes only one internal order.

## 4.3 Inclusion–exclusion for several adjacency restrictions

If several different pairs are forbidden from being adjacent, define one bad event for each pair.

For two bad events \(E_1,E_2\),

\[
|E_1\cup E_2|=|E_1|+|E_2|-|E_1\cap E_2|.
\]

For three events, continue with alternating signs.

A subtle point: intersections may form either **separate blocks** or a **longer chained block**.

For example, requiring both \(AB\) and \(BC\) forces the block \(ABC\), not two independent blocks.

## 4.4 Gap method

When objects of one type must be separated, arrange the other type first.

If 5 distinct boys are arranged in a row, they create 6 gaps:

\[
\_B\_B\_B\_B\_B\_.
\]

Placing at most one girl in each gap guarantees that no two girls are adjacent.

The gap method is strongest when one class of objects provides the separators. If several repeated categories can each violate adjacency, inclusion–exclusion may be cleaner.

## 4.5 Precedence conditions

For disjoint pairs \((A_i,B_i)\) requiring \(A_i\) before \(B_i\), symmetry is often useful.

Among all orders of one pair, exactly half have \(A_i\) before \(B_i\). For \(r\) disjoint labelled pairs, the count is often

\[
\frac{(2r)!}{2^r},
\]

provided there are no additional interacting restrictions.

### Why the powers of 2 appear

For every unconstrained arrangement of the \(2r\) distinct objects, flipping the relative order within each pair creates one of \(2^r\) equally sized orientation classes. Exactly one orientation satisfies all \(r\) precedence requirements.

## 4.6 Fixed separation patterns

A statement such as “exactly two students between successive teachers” should first be translated into possible **position patterns**.

Do not assign people until the allowed slots are known. Once the positions are fixed, distinct people can usually be assigned by factorials.

This position-first habit prevents accidental counting of arrangements that violate the spacing condition.

## 4.7 Exact adjacency counts

“Exactly two equal pairs are adjacent” is more delicate than “at least two.”

A reliable plan is:

1. choose which adjacency events occur;
2. form the required blocks;
3. count arrangements of those blocks and remaining objects;
4. subtract arrangements in which an extra forbidden adjacency also occurs.

## 4.8 Complement by total block formation

If the required condition is “at least one color is broken apart,” the complement may be “every color stays in one block.” Count that smaller block arrangement and subtract it from the full count.

If objects inside a color block are distinguishable, restore their internal permutations.

## Teacher example

Arrange the letters of \(AABC\) so that the A's are not adjacent.

Total distinct arrangements:

\[
\frac{4!}{2!}=12.
\]

Bad arrangements with \(AA\) as a block:

\[
3!=6.
\]

Therefore the valid count is \(12-6\).

## What should I notice?

- “together” → block;
- “not together” → complement or inclusion–exclusion;
- one type separated by another → gap method;
- several forbidden consecutive pairs → inspect how bad blocks overlap;
- “exactly \(r\)” adjacency events → require \(r\), then remove extra events;
- fixed distance between special people → determine positions first;
- paired precedence conditions → symmetry may remove a factor of 2 per pair.

## Common mistakes

- forgetting internal permutations inside a block;
- applying the gap method when several different categories can create violations and inclusion–exclusion is shorter;
- treating overlapping blocks as independent;
- forgetting identical-object division;
- dividing by \(2^r\) for precedence pairs when the pair restrictions interact with other positional conditions;
- counting “at least two adjacent pairs” when the problem asks for exactly two.

## Appendix A practice

Questions **Q9, Q25, Q30, Q31, Q32, Q35, Q36, Q37, Q40, Q41, Q42**.
