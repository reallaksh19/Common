# Advanced Worked Bridges

Read this after the main guide and before Appendix A. These are the four places where a short formula or recognition cue is not enough for a half-prepared student; the execution itself must be visible.

## 1. A 2×2 coloring by opposite cells

Suppose the four cells of a 2×2 square are colored with 3 colors so that cells sharing an edge have different colors.

Call opposite cells \(X,Z\). They are not adjacent.

Choose the color of \(X\): 3 choices.

### Case 1: \(Z\) has the same color as \(X\)

Then each of the other two cells only needs to avoid that one color. They are not adjacent to each other, so each has 2 choices.

Contribution:

\[
3\cdot1\cdot2^2=12.
\]

### Case 2: \(Z\) has a different color from \(X\)

There are 2 choices for \(Z\). Each remaining cell is adjacent to both \(X\) and \(Z\), so it must use the third color.

Contribution:

\[
3\cdot2\cdot1^2=6.
\]

Total:

\[
12+6=18.
\]

The important move is not the number 18. It is choosing **nonadjacent opposite cells first**, because that makes the remaining choices independent.

This is the execution bridge for Q8-style problems.

---

## 2. Circular gaps with an extra spacing cap

Five boys sit around a circle. We want to place three girls with no two girls adjacent, and we also want at most two boys between consecutive girls.

After the boys are arranged, label the five circular gaps \(0,1,2,3,4\). Choose three gaps for the girls.

There are initially

\[
inom53=10
\]

sets of gaps.

Now check the **cyclic distances** between consecutive chosen gaps. If two chosen gaps have two unchosen gaps between them, then the corresponding girls have three boys between them, which is not allowed.

A clean hand check is to list the five rotations of the forbidden gap pattern

\[
1,0,0,1,1,
\]

where 1 means “girl placed in this gap.” These are exactly the five bad 3-gap selections.

Therefore 5 of the 10 gap selections satisfy the extra spacing condition.

The lesson is:

> The ordinary gap method enforces nonadjacency. An extra distance condition must still be imposed on the chosen gaps themselves.

This is the missing execution step for Q20-style circular spacing.

---

## 3. Counting a labeled degree-2 graph from its cycle sizes

Every finite simple graph in which every vertex has degree 2 is a disjoint union of cycles.

Consider 7 labeled vertices. The only possible cycle-size types are

\[
7
\]

or

\[
3+4.
\]

### One 7-cycle

On a fixed 7-set, the number of undirected cycles is

\[
rac{(7-1)!}{2}=360.
\]

We divide by 7 for rotations when turning a linear ordering into a cycle, and by 2 for reversing direction; equivalently this is \((7-1)!/2\).

### One 3-cycle and one 4-cycle

Choose the 3 vertices of the triangle:

\[
inom73=35.
\]

A 3-set supports exactly one undirected 3-cycle.

The remaining 4 vertices support

\[
rac{(4-1)!}{2}=3
\]

undirected 4-cycles.

Contribution:

\[
35\cdot3=105.
\]

Total degree-2 labeled graphs:

\[
360+105=465.
\]

If two cycle components have the same size, remember that swapping the two whole components does not create a new graph; divide by the corresponding component factorial when necessary.

This is the execution bridge needed for Q34-style problems.

---

## 4. First stable prefix: why the recurrence does not overlap

Suppose a permutation of \(\{1,\ldots,n\}\) is called **indecomposable** if no proper first \(k\) positions contain exactly the set \(\{1,\ldots,k\}\).

Let \(c_n\) be the number of indecomposable permutations.

Every permutation has a unique **first** stable prefix. If that first stable prefix has size \(k\), then:

- the first \(k\) entries form an indecomposable permutation of \(\{1,\ldots,k\}\): \(c_k\) choices;
- the remaining \(n-k\) entries can be arranged freely: \((n-k)!\) choices.

Therefore

\[
n!=\sum_{k=1}^{n}c_k(n-k)!.
\]

The word **first** is what makes the cases disjoint. If we merely classified by “a stable prefix of size \(k\),” one permutation could appear in several classes.

For example:

\[
c_1=1,
\]

\[
c_2=2!-c_1(1!)=1,
\]

\[
c_3=3!-c_1(2!)-c_2(1!)=6-2-1=3.
\]

Now the recurrence is executable rather than just recognizable. This is the bridge for Q14-style prefix problems.
