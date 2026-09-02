# Practice & Transfer Bank

Attempt each item without a method label. The stages gradually remove support, but the governing habit is unchanged: define the state before the recurrence.

## Stage 0

1. Let `a_n` count tilings of a `1 x n` strip by tiles of lengths 1 and 2. Derive the recurrence from the first tile and find `a_6`.

2. Let `b_n` count binary strings of length `n` with no consecutive 1s. Derive a first-symbol recurrence and find `b_5`.

3. Let `T_n` count domino tilings of a `2 x n` rectangle. Explain the two left-edge branches and find `T_5`.

4. A staircase has 7 steps. Each move climbs 1 or 2 steps. Classify by the final move and count the routes.

## Stage 1

5. A `1 x 7` strip is tiled by pieces of lengths 1 and 3. Derive the recurrence and count the tilings.

6. How many length-5 words over `{A,B,C}` have adjacent letters different? Give both a state-transition explanation and the shorter symmetry count.

7. A `2 x n` board may be tiled by dominoes and by `2 x 2` square tiles. A width-2 block can therefore be filled in two structurally different ways. Derive the recurrence and find the count for `n=5`.

8. Count binary strings of length 7 with no consecutive 1s. Your proof must explain why the first-step branches are disjoint and exhaustive.

## Stage 2

9. How many compositions of 8 using parts 1 and 2 contain no consecutive 2s? Use enough state to make future legality well-defined.

10. How many length-6 binary strings have no consecutive 1s and an even number of 1s? Use a state that remembers both local legality and acceptance parity.

11. How many length-6 binary strings contain no run of three equal bits? Use a finite-memory state or an equivalent recurrence whose state meaning is explicit.

12. How many length-6 words over `{A,B,C}` have adjacent letters different and contain an even number of A's? Identify the memory that a transition table must retain.

## Stage 3

13. Starting from 1, a move replaces `x` by `x+1` or `2x`. Find the minimum number of moves needed to reach 31. Justify minimality, not only a path.

14. For the same machine, find the minimum number of moves needed to reach 100. Compare forward and reverse search before choosing a direction.

15. How many partitions of 8 into distinct positive parts are there? Use an include/exclude state or another compact representation and verify the result independently.

16. In how many ways can 10 be written as a sum of powers of 2 if each power may be used 0, 1, or 2 times? Use a bounded-part or carry-state representation.

## Stage 4

17. A `1 x 10` strip is tiled by pieces of lengths 1 and 3. Count the tilings and state the base cases needed by your recurrence.

18. Count length-8 binary strings with no consecutive 1s and an even number of 1s. Do not list all 256 strings.

19. Starting from 2, a machine allows `x -> 2x` and `x -> x+3`. Find the minimum number of moves to reach 29 and prove that fewer moves are impossible.

20. Arrange four E's and three N's with no consecutive N's. Count the arrangements. Then explain why a gap representation is cleaner here than a recurrence, even though a recurrence is possible.
