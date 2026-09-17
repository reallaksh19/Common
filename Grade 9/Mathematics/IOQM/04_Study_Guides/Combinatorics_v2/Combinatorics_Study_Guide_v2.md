# IOQM Grade 9 — Combinatorics Study Guide v2

## Who this is for

This guide is for a Grade 9 student who already knows some school mathematics but is not yet reliable at Olympiad counting. You may remember factorials, combinations, basic divisibility and simple sequences, yet still get stuck on questions where the method is hidden.

The aim is not to collect tricks. The aim is to make the first useful decision predictable.

When you face a problem, ask:

1. **What exactly is one outcome?**
2. **Does order matter?**
3. **Which restriction is strongest?**
4. **Would the complement be shorter?**
5. **Are my cases disjoint?**
6. **Is there a better picture: gaps, blocks, a graph, a state, or prime exponents?**
7. **What does the problem regard as the same: exact positions, rotations, reflections?**

The examples in this guide are newly written teaching examples. Appendix A contains the 56 attached practice questions only, with answers at the very end. Appendix B contains 20 additional IOQM-style mock questions, again with answers only at the end.

---

# Part I — Foundations you must make automatic

## 1. Counting stages, cases, complements and inclusion–exclusion

### 1.1 Multiplication: choices made in stages

If a complete object is built by making one choice, then another, multiply the number of legal choices at each stage.

Example: a three-character code has 4 choices for the first character, 5 for the second and 3 for the third. The count is

\[
4\cdot5\cdot3.
\]

The important word is **legal**. If the number of choices at stage 2 depends on what happened at stage 1, either split into cases or sum the stage-dependent counts.

### 1.2 Addition: disjoint cases

If every valid object belongs to exactly one of several cases, add the case counts.

Before adding, ask:

> Can the same object appear in two cases?

If yes, the cases overlap and simple addition is wrong.

### 1.3 Complement counting

Phrases such as

- at least one,
- not all,
- at least two are adjacent,
- some color is missing,

often become easier after counting the opposite.

\[
\#(\text{wanted})=\#(\text{all})-\#(\text{opposite}).
\]

**Worked example.** How many subsets of an 8-element set contain at least one of two particular elements \(a,b\)?

All subsets: \(2^8\).

Subsets containing neither: \(2^6\).

Answer:

\[
2^8-2^6.
\]

### 1.4 Inclusion–exclusion

If \(A\) and \(B\) are bad events,

\[
|A\cup B|=|A|+|B|-|A\cap B|.
\]

Therefore

\[
\#(\text{valid})=\#(\text{all})-|A|-|B|+|A\cap B|.
\]

For three bad events,

\[
|A\cup B\cup C|
=
|A|+|B|+|C|
-|A\cap B|-|A\cap C|-|B\cap C|
+|A\cap B\cap C|.
\]

Do not memorize the signs without understanding the reason: objects in two bad sets were subtracted twice, so one copy must be restored.

### 1.5 A self-referential subset condition

Sometimes the rule depends on the size of the subset itself. Then **fix the size first**.

Example: count subsets \(S\subseteq\{1,2,\ldots,8\}\) for which \(|S|\notin S\).

For a fixed size \(k\), the set must avoid the element \(k\), so choose all \(k\) elements from the remaining 7:

\[
\binom7k.
\]

Then sum over the allowed values of \(k\). The confusing self-reference disappears once \(k\) is fixed.

### What to notice

- “at least one” → try complement;
- “first or last position forbidden” → inclusion–exclusion is often short;
- “size of the chosen set appears in the rule” → condition on the size;
- independent categories → count each category and multiply.

---

# Part II — Selecting objects without order

## 2. Combinations, committees and logical restrictions

A committee is usually an unordered selection:

\[
\binom nr=\frac{n!}{r!(n-r)!}.
\]

Choosing \(A,B,C\) is the same committee as choosing \(C,A,B\).

### 2.1 Exactly one from each pair

If a team must contain exactly one person from each of \(r\) pairs, the count is simply

\[
2^r.
\]

Do not use inclusion–exclusion when the rule can be built into the construction.

### 2.2 “Only if” and conditional membership

Translate the English first.

- “\(B\) serves only if \(C\) serves” means \(B\Rightarrow C\).
- “\(A\) refuses to serve with \(B\)” means not both \(A,B\).

A useful habit is to split on the person who triggers the most consequences.

**Worked example.** Choose 4 people from \(A,B,C,D,E,F,G\). If \(B\) is chosen, \(C\) must be chosen; \(A\) and \(B\) cannot both be chosen.

Case 1: \(B\) is chosen. Then \(C\) is chosen and \(A\) is excluded. Choose 2 more from \(D,E,F,G\).

Case 2: \(B\) is not chosen. Choose any 4 from \(A,C,D,E,F,G\).

The cases are disjoint and complete.

### 2.3 Together or neither

If \(A,B\) must either both serve or both stay out, use exactly two cases:

- both in;
- both out.

Apply the remaining restrictions separately in each case.

### 2.4 “At least / at most / exactly”

These words change the model.

- at least one → complement often helps;
- at most one from a pair → neither or exactly one;
- exactly \(k\) special objects → choose those \(k\) first;
- at least one from each independent class → \((2^a-1)(2^b-1)\cdots\).

### What to notice

Questions Q17, Q18 and Q23 require this style of thinking. The important skill is not the binomial formula; it is converting verbal logic into disjoint cases.

---

# Part III — Distributing identical amounts and selecting from repeated copies

## 3. Stars and bars, lower bounds, multinomial terms and bounded multiplicities

### 3.1 Stars and bars

The number of nonnegative integer solutions of

\[
x_1+\cdots+x_r=n
\]

is

\[
\binom{n+r-1}{r-1}.
\]

The method applies when the distributed objects are identical and the recipients are distinguishable.

For positive solutions, give one to each recipient first:

\[
x_i\ge1
\quad\Longrightarrow\quad
\binom{n-1}{r-1}.
\]

### 3.2 Lower bounds

If \(x_i\ge a_i\), satisfy the compulsory minimum first.

**Worked example.**

\[
x+y+z=17,\qquad x\ge2,\ y\ge4,\ z\ge1.
\]

Set

\[
u=x-2,\quad v=y-4,\quad w=z-1.
\]

Then

\[
u+v+w=10,\qquad u,v,w\ge0,
\]

so the number of solutions is

\[
\binom{12}{2}.
\]

### 3.3 Positive exponents in an expansion

A term of

\[
(a+b+c+1)^N
\]

containing \(a,b,c\) with positive powers corresponds to

\[
x+y+z+t=N,
\quad x,y,z\ge1,\quad t\ge0.
\]

Shift the positive variables by 1. This is stars and bars in disguise.

### 3.4 Selecting from repeated letters

Suppose a letter is available at most \(m\) times. The possible copy counts \(0,1,\ldots,m\) are encoded by

\[
1+x+x^2+\cdots+x^m.
\]

For several letter types, multiply the factors. The coefficient of \(x^r\) counts selections of \(r\) letters.

**Worked example.** There are at most 2 A's, 1 B and 3 C's. The generating polynomial is

\[
(1+x+x^2)(1+x)(1+x+x^2+x^3).
\]

To count 4-letter selections, find the coefficient of \(x^4\).

For small targets you need not expand everything. List the feasible exponent triples \(a+b+c=4\) with \(0\le a\le2\), \(0\le b\le1\), \(0\le c\le3\).

### 3.5 Multiplicity patterns

For a short word length, classify by partitions of the length.

A 4-letter word made from repeated letters can have patterns

\[
4,\quad3+1,\quad2+2,\quad2+1+1,\quad1+1+1+1.
\]

Then eliminate patterns that exceed the available copies.

This is particularly effective for questions such as Q39 and Q55.

### 3.6 One parameter controlling several blocks

In a restricted arrangement split into equal blocks, conservation can force all block counts once one parameter is chosen.

**Worked miniature.** Arrange 3 A's, 3 B's and 3 C's into three labeled blocks of 3 positions. Block 1 may not contain A, block 2 may not contain B, and block 3 may not contain C.

Let block 1 contain \(k\) B's. Then block 1 contains \(3-k\) C's.

Because there are 3 B's total and block 2 contains no B, the remaining \(3-k\) B's must go to block 3. Because there are 3 C's total and block 3 contains no C, the remaining \(k\) C's must go to block 2. The A-counts are then forced as well:

- block 1: \(k\) B, \(3-k\) C;
- block 2: \(3-k\) A, \(k\) C;
- block 3: \(k\) A, \(3-k\) B.

For a fixed \(k\), each block has \(\binom3k\) arrangements, so the total is

\[
\sum_{k=0}^3 \binom3k^3.
\]

This smaller example contains the entire reasoning pattern of Q6: one parameter + conservation + a short binomial sum.

### What to notice

- identical objects + named boxes → stars and bars;
- positive lower bounds → subtract them first;
- “term contains all variables” → positive exponent count;
- repeated-letter selection → multiplicity patterns or a generating function;
- repeated-letter arrangement → factorial divided by repeated-copy factorials.

---

# Part IV — Arranging objects in a row

## 4. Permutations, blocks, gaps, derangements and exact adjacency

### 4.1 Distinct and repeated objects

For \(n\) distinct objects:

\[
n!.
\]

If multiplicities are \(m_1,m_2,\ldots\):

\[
\frac{n!}{m_1!m_2!\cdots}.
\]

### 4.2 Blocks

If two specified distinct objects must be adjacent, treat them as one block, then multiply by the number of internal orders.

Example: \(A,B\) together among 6 distinct objects:

\[
5!\cdot2.
\]

If the block is \(AA\) with identical A's, there is no internal factor 2.

### 4.3 Forbidden adjacency: inclusion–exclusion

For repeated or specified pairs that must not be adjacent, define one bad event per adjacency.

A crucial issue is how bad events overlap.

- \(AB\) and \(CD\) form two separate blocks.
- \(AB\) and \(BC\) form one chained block \(ABC\).

Q30, Q31, Q32 and Q36 rely on this distinction.

### 4.4 Gap method

To keep special objects apart, arrange the separators first.

If 6 boys are placed in a row, they create 7 gaps:

\[
\_B\_B\_B\_B\_B\_B\_.
\]

Choose distinct gaps for girls to guarantee no two girls are adjacent.

### 4.5 Precedence pairs

If \(r\) disjoint pairs \((M_i,C_i)\) must satisfy “\(M_i\) before \(C_i\)” and there are no other interacting restrictions, symmetry gives

\[
\frac{(2r)!}{2^r}.
\]

This is the principle behind Q25.

### 4.6 Derangements

A derangement is a permutation with no object in its original position.

Let \(D_n\) be the number of derangements of \(n\) objects.

By inclusion–exclusion,

\[
D_n
=
n!-\binom n1(n-1)!+\binom n2(n-2)!-\cdots+(-1)^n.
\]

For small \(n\), useful values are

\[
D_1=0,\quad D_2=1,\quad D_3=2,\quad D_4=9,\quad D_5=44.
\]

Another recurrence is

\[
D_n=(n-1)(D_{n-1}+D_{n-2}).
\]

Q9 becomes much easier once family positions are reduced to a derangement.

### 4.7 Exact adjacency counts

“Exactly two adjacency events occur” is not the same as “at least two.”

A safe plan:

1. choose the adjacency events that must occur;
2. form the corresponding blocks;
3. count those arrangements;
4. subtract arrangements in which an extra adjacency also occurs.

**Worked miniature.** In permutations of \(A,B,C,D\), count arrangements in which exactly one of the adjacencies \(AB\) and \(CD\) occurs.

Let \(E_1\) mean A and B are adjacent, and \(E_2\) mean C and D are adjacent.

\[
|E_1|=3!\cdot2=12,\qquad |E_2|=12.
\]

If both adjacencies occur, there are two blocks, each with 2 internal orders:

\[
|E_1\cap E_2|=2!\cdot2\cdot2=8.
\]

“Exactly one” counts the intersection zero times, so

\[
12+12-2(8)=8.
\]

This same logic scales to “exactly \(r\) bad adjacencies”: requiring some events is not enough; extra events must be removed.

### 4.8 Fixed separation

If special people must have exactly \(d\) ordinary positions between them, find the allowed position patterns before assigning identities.

This position-first method is the core of Q42.

### What to notice

- “together” → block;
- “not together” → complement or inclusion–exclusion;
- “none in original position” → derangement;
- “separated” → gaps;
- “exactly \(r\) adjacencies” → require \(r\), then remove extra ones;
- “exactly \(d\) people between” → find legal positions first.

---

# Part V — Relative order, alternating patterns and dictionary rank

## 5. When the actual values matter less than their order

Several attached questions look like geometry or algebra but become counting problems after one reduction.

### 5.1 Most-restricted-first pairings

For a condition such as

\[
y\ge2x,
\]

the largest possible smaller value has the fewest legal partners. Place it first, then work downward.

This is the key idea in Q1.

### 5.2 Arithmetic progression with fixed total

For three values in arithmetic progression,

\[
m-d,\quad m,\quad m+d.
\]

If their sum is \(S\), then \(3m=S\), so \(m=S/3\).

In a triangle the angle sum is \(180^\circ\), so the middle angle is \(60^\circ\). Only the integer range of \(d\) remains. That is Q5.

### 5.3 Reduce an equation to a sign condition

Suppose two curves lead to

\[
x^2=\frac{D-B}{A-C}.
\]

Real intersection requires the fraction to be positive, so numerator and denominator must have the same sign. The algebra has become an ordering problem.

Do not keep solving equations after the structure has reduced to signs. This is Q7.

### 5.4 Alternating permutations

If no three consecutive terms may be increasing or decreasing, the comparison signs must alternate:

\[
<,>,<,>\ldots
\]

or

\[
>,<,>,<,\ldots
\]

For small \(n\), count directly from peak and valley positions rather than memorizing a special sequence.

**Worked example: four distinct values.**

For

\[
a_1<a_2>a_3<a_4,
\]

choose the rank at the main peak \(a_2\), then count how the remaining ranks can occupy the three valley/rising positions. There are 5 such relative-order patterns.

The reverse pattern also has 5.

For digits, choose the actual digit set only after counting the legal relative-order patterns; handle 0 separately if it may lead.

### 5.5 Dictionary rank: distinct letters

Scan left to right.

At each position:

\[
(\text{number of smaller available letters})
\times
(\text{number of suffix permutations}).
\]

Add these blocks of earlier words, then continue with the actual letter. Add 1 at the end.

### 5.6 Dictionary rank: repeated letters

If the remaining multiset contains repeats, use

\[
\frac{m!}{r_1!r_2!\cdots}
\]

for each hypothetical suffix.

Recompute multiplicities after the hypothetical smaller letter is chosen.

### 5.7 Fixed leading digit plus one repeated pair

If a number begins with a fixed digit and the full digit multiset has pattern \(2,1,1\), split into:

- the leading digit is the repeated digit;
- some other digit is repeated.

This prevents double counting and is the main structure in Q44.

### What to notice

- only \(<,>\) relations matter → relative-order pattern;
- “no three monotone” → alternating signs;
- “dictionary rank” → smaller-first blocks;
- repeated letters in rank → divide suffix counts by multiplicity factorials;
- algebraic surface → simplify until only sign/order remains.

---

# Part VI — Circular arrangements and symmetry

## 6. Round tables, circular gaps, necklaces and cube rotations

### 6.1 Ordinary round table

For \(n\) distinct people around an unlabeled round table, rotations are the same:

\[
(n-1)!.
\]

The clean proof is to fix one named person and arrange the others relative to that person.

### 6.2 Numbered seats

If the chairs are distinct or numbered, rotations count as different. Then use ordinary position counting, often \(n!\).

Always read the equivalence convention.

### 6.3 Directional neighbours

If the problem says “immediately to the right” or “clockwise,” fix one named person. The remaining seats become ordinary labeled relative positions.

### 6.4 Circular gaps

If 5 boys are arranged around a circle, there are 5 gaps, not 6.

Place girls in selected gaps to prevent girl-girl adjacency.

For extra spacing conditions, count only the allowed gap selections. Q20 requires this second step.

### 6.5 Adjacency by complement

To count arrangements in which at least two special people are adjacent, it is often easier to subtract the arrangements in which no two are adjacent.

### 6.6 Forced local blocks

If a person requires both neighbours to have a certain property, build the forced three-person local block before doing the circular count. This is the kind of reasoning needed in Q48.

### 6.7 Circular multisets

For repeated letters around a circle, dividing a linear multiset count by \(n\) is valid only if every arrangement has orbit size \(n\).

A unique letter can guarantee that no nontrivial rotation fixes the arrangement. If the pattern could repeat periodically, simple division may fail.

### 6.8 Necklaces and garlands

If reflection is also considered identical, rotations are not the only symmetry.

For small two-color problems, a student-friendly method is:

1. fix one color as separators;
2. record the cyclic gap sizes of the other color;
3. identify gap patterns that differ only by rotation or reversal.

**Worked miniature.** A bracelet has 3 red and 3 blue beads. Place the 3 red beads as separators. The 3 blue beads are distributed among the 3 cyclic gaps, so the gap sizes sum to 3. Up to rotation and reversal, the possibilities are represented by

\[
(3,0,0),\qquad (2,1,0),\qquad (1,1,1).
\]

Thus there are 3 bracelet types. This is the kind of hand classification needed before a more general symmetry theorem becomes useful.

For larger problems, the systematic method is Burnside's lemma:

\[
\text{number of distinct objects}
=
\frac{\text{sum of fixed objects over all symmetries}}
{\text{number of symmetries}}.
\]

You do not need to use Burnside when a short gap classification is clearer.

### 6.9 Cube colorings

The cube has 24 rotations.

If all six face colors are distinct, no non-identity rotation fixes a coloring, so

\[
\frac{6!}{24}=30.
\]

If colors repeat, check fixed colorings under rotations instead of blindly dividing by 24.

### 6.10 Empty chairs

Fix a named person to remove rotation. Then treat the remaining chair positions as labeled slots relative to that person. Apply any local occupied-seat requirement first; choose empty slots only afterward.

### What to notice

- ordinary circle → fix one named object;
- numbered circular seats → do not divide by rotation;
- right/clockwise → fix a reference person;
- separated special objects → circular gaps;
- rotation + reflection → necklace/garland symmetry;
- cube with all distinct face colors → divide by 24.

---

# Part VII — Graphs, matchings and colorings

## 7. Turning pairwise restrictions into a picture

A graph has vertices (objects) and edges (allowed or relevant pairwise relations).

Use graph language only if it makes the restriction simpler.

### 7.1 Unordered pairs and handshakes

There are

\[
\binom n2
\]

unordered pairs among \(n\) people.

If one class of pairs is easy to count, subtract it from all pairs to count the other class. This is Q2.

### 7.2 Handshake lemma

\[
\sum_v d(v)=2|E|.
\]

Every edge contributes 1 degree at each endpoint.

### 7.3 Perfect matchings

A pairing of all vertices is a perfect matching.

If the allowed graph is symmetric, classify matchings by a structural feature instead of listing them.

A useful recursion is:

> Choose the partner of the smallest-labeled free vertex; then count perfect matchings of the remaining graph.

**Worked miniature.** Six people \(1,2,3,4,5,6\) are paired, but \(1\) may not pair with \(2\). Unrestricted pairings:

\[
5\cdot3\cdot1=15.
\]

Pairings with \(1\) paired to \(2\):

\[
3\cdot1=3.
\]

Therefore 12 pairings remain.

If the allowed relation is more complicated, start with vertex 1, list its legal partners, and recurse on the four remaining vertices. This gives a systematic path instead of guesswork and is the core method for Q33-style matching graphs.

### 7.4 Counting pairings without restrictions

For \(2n\) labeled people, the number of ways to split them into \(n\) unordered pairs is

\[
(2n-1)(2n-3)\cdots3\cdot1
=
\frac{(2n)!}{2^n n!}.
\]

Use inclusion–exclusion when a few particular pairings are forbidden.

### 7.5 Degree 2 means disjoint cycles

A finite simple graph in which every vertex has degree 2 is a disjoint union of cycles.

For labeled vertices, the number of undirected \(k\)-cycles on a chosen \(k\)-set is

\[
\frac{(k-1)!}{2}.
\]

Why divide by 2? Clockwise and anticlockwise traversals describe the same undirected cycle after rotation has already been removed.

If the graph has several cycles of equal length, divide further for the order of those indistinguishable components.

This is the missing counting tool needed for Q34.

### 7.6 Proper colorings

Adjacent vertices must receive different colors.

For a path of \(n\) vertices and \(q\) colors:

\[
q(q-1)^{n-1}.
\]

For a cycle \(C_n\):

\[
P(C_n,q)=(q-1)^n+(-1)^n(q-1).
\]

A short derivation: color a path first, then separate path colorings according to whether the last vertex has the same color as the first. The correction alternates and leads to the formula above.

For a small cycle, direct casework is also acceptable.

### 7.7 A \(2\times2\) grid

Opposite cells are not adjacent. Condition on the relation between one opposite pair:

- same color;
- forbidden partner colors;
- different compatible colors.

Then the two remaining cells often become independent. This is Q8.

### What to notice

- handshake → unordered pair / edge;
- everyone degree 2 → cycle decomposition;
- pair everyone → perfect matching;
- adjacent colors different → graph coloring;
- small square grid → opposite cells may be a better starting point than adjacent cells.

---

# Part VIII — Recurrences and states

## 8. Count by remembering only what the future needs

### 8.1 Define the state

Complete the sentence:

> \(a_n\) counts ...

Then ask:

> Can two partial objects with the same state have different legal futures?

If yes, the state is missing information.

### 8.2 No adjacent 1s

Let \(s_n\) be the number of length-\(n\) binary strings with no consecutive 1s.

Split by the last digit:

- ends in 0 → \(s_{n-1}\);
- ends in 1 → previous digit must be 0, leaving \(s_{n-2}\).

Thus

\[
s_n=s_{n-1}+s_{n-2}.
\]

With \(s_0=1\), \(s_1=2\), the counts are Fibonacci-shifted.

### 8.3 Encode changes instead of symbols

If the forbidden patterns are \(010\) and \(101\), define

\[
d_i=
\begin{cases}
1,&b_i\ne b_{i+1},\\
0,&b_i=b_{i+1}.
\end{cases}
\]

Then \(010\) or \(101\) means two consecutive changes, i.e. \(d_id_{i+1}=11\).

The original problem becomes a no-adjacent-1 problem. This is Q12.

### 8.4 First stable prefix

If a permutation has a forbidden “stable prefix” property, classify every permutation by the **first** prefix where stability occurs.

The word first makes the cases disjoint.

For example, if \(c_n\) counts permutations with no proper stable prefix and every permutation has a unique first stable prefix of size \(k\),

\[
n!
=
\sum_{k=1}^n c_k(n-k)!.
\]

Then solve recursively for \(c_n\). This is Q14.

### 8.5 Nonlinear recurrence → ratios

If

\[
a_n=a_{n-1}+\frac{a_{n-1}^2}{a_{n-2}},
\]

divide by \(a_{n-1}\) and define

\[
r_n=\frac{a_n}{a_{n-1}}.
\]

Then

\[
r_n=1+r_{n-1}.
\]

The difficult recurrence has become linear. Check that the denominators are nonzero before dividing. This is Q16.

### 8.6 Reverse search

If forward moves branch widely but the target has few possible predecessors, work backward.

For example, if forward moves are \(x\mapsto2x\) or \(x\mapsto x+3\), predecessors of a target \(y\) are:

- \(y/2\), if \(y\) is even;
- \(y-3\).

Breadth-first search on these small predecessor layers often reveals the minimum number of steps.

### What to notice

- local forbidden pattern → state or change encoding;
- “first time a property occurs” → first-occurrence recurrence;
- quotient \(a_{n-1}^2/a_{n-2}\) → try consecutive ratios;
- hard forward process, simple target predecessors → reverse search.

---

# Part IX — Number-theoretic counting

## 9. Prime exponents turn huge numbers into small choices

### 9.1 Divisor count

If

\[
n=p_1^{a_1}\cdots p_r^{a_r},
\]

then

\[
\tau(n)=\prod_{i=1}^r(a_i+1).
\]

A divisor is determined by choosing each prime exponent independently.

### 9.2 Factor pairs

If \(n\) is not a square, unordered factor pairs:

\[
\frac{\tau(n)}2.
\]

If \(n\) is a square:

\[
\frac{\tau(n)+1}{2}.
\]

### 9.3 Product of all divisors

Pair \(d\) with \(n/d\).

For nonsquare \(n\),

\[
\prod_{d\mid n}d=n^{\tau(n)/2}.
\]

For a square, the middle divisor \(\sqrt n\) is unpaired; equivalently the general formula is \(n^{\tau(n)/2}\) if fractional exponents are interpreted, but for Grade 9 integer work it is safer to handle the middle divisor explicitly.

### 9.4 Largest power of a composite divisor

If

\[
m=2^\alpha3^\beta5^\gamma,
\]

then \(m^x\mid N\) requires

\[
\alpha x\le v_2(N),\quad
\beta x\le v_3(N),\quad
\gamma x\le v_5(N).
\]

The smallest resulting bound controls \(x\).

### 9.5 Divisor exponent grids

Divisors of \(p^aq^b\) correspond to lattice points

\[
(i,j),\qquad0\le i\le a,\ 0\le j\le b.
\]

Lowering both exponents by 1 removes the top row and right column, with the corner counted once. Q29 is exactly this picture.

### 9.6 Digit divisibility by 3 and 9

Reduce digits modulo 3 first. Count residue patterns whose sum is \(0\pmod3\), then count actual digit choices producing those residues.

This is usually far shorter than enumerating all numbers.

### What to notice

- huge exponent → work with prime exponents;
- factor pairs → divisor count plus square check;
- power dividing product → valuations;
- compare \(p^aq^b\) with smaller exponents → exponent-grid boundary;
- divisibility by 3/9 → digit residues before arrangement.

---

# Part X — Pigeonhole and extremal reasoning

## 10. Skills needed for the wider IOQM combinatorics syllabus

The attached Q1–Q56 set does not strongly test pigeonhole or extremal reasoning, but the existing Grade 9 IOQM curriculum does. A self-contained guide must include them.

### 10.1 Pigeonhole principle

If more than \(m\) objects are placed into \(m\) boxes, some box contains at least two objects.

The real skill is choosing useful boxes.

Example: select 13 integers from \(\{1,2,\ldots,24\}\). Group the numbers into

\[
\{1,2\},\{3,4\},\ldots,\{23,24\}.
\]

There are 12 boxes. Selecting 13 numbers forces two from one pair, hence two consecutive integers.

### 10.2 Generalized form

If \(N\) objects are placed into \(m\) boxes, some box has at least

\[
\left\lceil\frac Nm\right\rceil
\]

objects.

### 10.3 Extremal choice

Choose a largest, smallest, nearest or farthest object and exploit what its extremeness forbids.

Typical pattern:

1. assume a counterexample exists;
2. choose an extreme object in it;
3. show that the rule would allow an even more extreme object;
4. contradiction.

### 10.4 Pigeonhole versus exact counting

Pigeonhole proves something **must exist**. It usually does not tell you the exact number of valid configurations.

If the question asks “how many?”, return to direct counting, complement or inclusion–exclusion.

---

# Part XI — Invariants and simple games

## 11. What stays unchanged, and which positions are winning?

The attached 56 questions do not cover this enough, but the Grade 9 IOQM program includes it.

### 11.1 Invariant

An invariant is a quantity that does not change after a legal move.

Common invariants:

- parity;
- residue modulo \(m\);
- checkerboard color balance;
- parity of inversions.

**Worked example.** Remove two opposite corners of a chessboard. Both removed corners have the same color, so the remaining board has unequal numbers of black and white squares. Every domino covers one black and one white square. Therefore a domino tiling is impossible.

The color difference is the invariant obstruction.

### 11.2 Monovariant

A monovariant always moves in one direction, for example a nonnegative quantity that strictly decreases. This proves a process must terminate.

### 11.3 Winning and losing positions

In a finite impartial game:

- a losing position has no move to another losing position;
- a winning position has at least one move to a losing position.

For a pile where a player may remove 1, 2 or 3 stones and the player taking the last stone wins, the losing positions are multiples of 4.

Why? From a multiple of 4 every move leaves a nonmultiple of 4; from any nonmultiple of 4 there is a move back to a multiple of 4.

### 11.4 Do not confuse a game with a recurrence

A recurrence counts possible objects. A game asks for an adversarial strategy: your opponent chooses moves to hurt you.

Simulation can suggest the pattern, but the proof is the invariant or winning/losing classification.

---

# Part XII — A practical study order

For a student with about half the background already present:

### Stage 1 — Make the basics reliable

Study Parts I–IV until you can distinguish:

- selection vs arrangement;
- direct count vs complement;
- cases vs inclusion–exclusion;
- stars and bars vs ordinary combinations;
- block vs gap.

### Stage 2 — Learn the less-obvious representations

Study Parts V–IX:

- relative order;
- dictionary rank;
- circular symmetry;
- graph models;
- recurrence states;
- prime-exponent counting.

### Stage 3 — Add the wider Olympiad tools

Study Parts X–XI:

- pigeonhole/extremal;
- invariants/games.

### Stage 4 — Test yourself

1. Attempt Appendix A without chapter labels.
2. Mark every question where you could not write a first useful line within 3 minutes.
3. Re-study the relevant part.
4. Attempt Appendix B.
5. Only then use the two-page quick reference.

---

# What must be memorized, and what must be understood

## Memorize

\[
{}^nP_r=\frac{n!}{(n-r)!},
\qquad
\binom nr=\frac{n!}{r!(n-r)!},
\]

\[
\#\{x_1+\cdots+x_r=n,\ x_i\ge0\}
=
\binom{n+r-1}{r-1},
\]

\[
\sum_vd(v)=2|E|,
\]

\[
\tau\!\left(\prod p_i^{a_i}\right)=\prod(a_i+1),
\]

\[
D_n=(n-1)(D_{n-1}+D_{n-2}),
\]

\[
P(C_n,q)=(q-1)^n+(-1)^n(q-1).
\]

Also remember:

- \(D_3=2,D_4=9,D_5=44\);
- a cube has 24 rotations;
- a circle of \(n\) distinct people has \((n-1)!\) arrangements when rotations are identified.

## Understand rather than memorize

- why the complement is shorter;
- why your cases are disjoint;
- why a block or gap model is valid;
- why a recurrence branch corresponds to exactly one family of objects;
- why division by a symmetry factor is legal;
- why an invariant blocks a construction;
- why the selected graph representation preserves the original restriction.

If you cannot explain one of these in a sentence, the formula alone is not enough.
