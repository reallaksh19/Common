# Practice & Transfer Bank

Attempt each problem without consulting the First-Step Reference. Choose the representation and proof obligation yourself.

## Full mixed solves

1. Ten lamps are arranged in a row. A legal move toggles exactly four lamps of your choice. Initially exactly three lamps are on. Can all lamps be turned off? Prove your answer.

2. A state is an ordered pair of integers `(a,b)`. A legal move replaces it by either `(a+2,b-2)` or `(a-2,b+2)`. Can `(5,7)` reach `(8,4)`? Give a proof that does not enumerate paths.

3. Six lamps lie on a cycle. A legal move toggles three consecutive lamps. Starting with all lamps off, can a state with exactly one lamp on be reached? Prove your answer.

4. A pair `(a,b)` consists of positive unequal integers. A legal move replaces the larger entry by the positive difference of the two entries, leaving the smaller entry unchanged. Prove that every legal play eventually stops.

5. A heap contains 17 stones. Two players alternate; on each turn a player removes 1 or 2 stones, and the player who removes the last stone wins. Determine the winner under optimal play and give a strategy proof.

6. A heap contains 20 stones. Two players alternate; on each turn a player removes 1, 3, or 4 stones, and the player who removes the last stone wins. Determine the winner under optimal play. Your proof must justify the losing class, not only show one favourable line.

## Same surface, different decision

7. Pair the integers `1,2,...,8` into four pairs so that the product of the four pair sums is a perfect square. Give an explicit construction and verify it.

8. Pair the integers `1,2,...,10` into five pairs so that the product of the five pair sums is a perfect square. Give an explicit construction and verify it.

9. A move on an integer triple adds a permutation of `(2,-1,-1)`. Can `(4,4,4)` reach `(5,4,3)`? Prove your answer without forward search.

10. Two heaps contain 7 and 10 stones. Two players alternate; a move removes exactly one stone from exactly one nonempty heap, and the player making the last move wins. Determine the winner under optimal play and explain whether the choice of heap can change the outcome.

## Changed-surface transfer

11. A list contains distinct numbers. Whenever two adjacent entries are inverted, you may swap that adjacent pair. Prove that no infinite sequence of such swaps is possible.

12. A heap game allows removal of 2 or 5 stones per turn, with normal play. Determine whether a starting heap of 25 stones is winning or losing. Give a complete W/L justification rather than a few computed examples.

## Verification questions

For every solution above, check these before considering it complete:

- If you used an invariant, did you verify every legal move and avoid treating compatibility as sufficiency?
- If you used a monovariant, is the change strict and bounded in the needed direction?
- If you claimed a winning class, did you prove both `W -> some L` and `L -> only W`?
- If you gave a construction, did you verify legality and the target property?
- If a move sequence appears in your proof, is it merely a reachable path, or is an opponent able to deviate?
