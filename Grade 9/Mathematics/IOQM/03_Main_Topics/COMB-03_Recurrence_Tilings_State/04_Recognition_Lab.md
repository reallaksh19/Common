# Recognition Lab

Choose the most useful first representation or diagnosis. Do not solve the whole problem unless needed.

1. A `2 x n` board is tiled by dominoes. Which first move is most useful?
   A. List complete tilings.  B. Freeze the leftmost unresolved column.  C. Guess a Fibonacci pattern.  D. Use inclusion-exclusion.

2. Binary strings have no consecutive 1s and must contain an even number of 1s. What extra information must a local state remember besides position?
   A. The entire prefix.  B. Last bit and parity of the 1-count.  C. Only the number of zeros.  D. Nothing.

3. A machine permits `x -> x+1` and `x -> 2x`; one fixed large target is given. What should be compared first?
   A. Forward and reverse branching.  B. AP and GP formulas.  C. Inclusion-exclusion.  D. Prime factorization only.

4. Four E's and three N's must be arranged with no adjacent N's. Which representation is smallest?
   A. A recurrence table is mandatory.  B. Choose three of the five gaps around the E's.  C. A game tree.  D. A geometric diagram.

5. A proposed recurrence uses two first-step cases, but one object satisfies both descriptions. What is wrong?
   A. Initial values are too small.  B. Cases overlap, so naive addition double-counts.  C. The state is too large.  D. Reverse search is impossible.

6. Two prefixes have the same remaining length but different legal next symbols. What does this prove?
   A. Remaining length alone is an insufficient state.  B. A recurrence cannot exist.  C. The problem is adversarial.  D. Complement counting is required.

7. A problem already supplies `a_{n+2}=3a_{n+1}-2a_n` and asks for a high-index term. Which work is central?
   A. Derive a counting-state recurrence.  B. Use the supplied recurrence algebra/sequence tools.  C. Build a tiling.  D. Search backward in a state graph.

8. A process offers several legal moves, but no opponent chooses against you. Which description is correct?
   A. It is automatically a two-player game.  B. It is a deterministic state/reachability problem with branching choices.  C. It must use minimax.  D. It cannot be represented by a graph.
