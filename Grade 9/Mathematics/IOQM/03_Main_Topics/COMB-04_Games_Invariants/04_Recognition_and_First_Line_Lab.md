# Recognition & First-Line Lab

The goal is to choose the right first representation before doing full arithmetic or casework.

For Questions 1–6, choose the best first move. For Questions 7–12, write only the first structural line you would put on paper. Do not solve the whole problem.

## Recognition

1. A row of lamps changes by legal moves, each of which toggles four lamps. The question asks whether a target configuration can be reached. What should be tested first?
   A. Enumerate move sequences.  B. Compare a parity signature before searching.  C. Build a W/L table.  D. Guess a recurrence.

2. A finite process has a quantity that never increases, but one legal move can leave the quantity unchanged. Which conclusion is justified immediately?
   A. The process terminates.  B. The first player wins.  C. Neither conclusion follows without more work.  D. The quantity is an invariant.

3. Two players alternate removing objects, both play optimally, and the question asks who can force the stated terminal outcome. What should be fixed before pattern hunting?
   A. A sample winning line.  B. The exact terminal outcomes and complete position state.  C. A board colouring.  D. The total number of historical examples.

4. The start and target states have the same value of a proved invariant. What has been established?
   A. The target is reachable.  B. The target is strategically forceable.  C. This invariant gives no obstruction, but sufficiency still needs proof.  D. Every legal move is reversible.

5. A local move acts on a repeating triangular board, ordinary parity is too weak, and a three-step pattern appears in small cases. What is the strongest first action?
   A. Adopt the observed colouring immediately.  B. Derive weights from the local move equations and verify every move.  C. Simulate to a large size.  D. Treat the board as a two-player game.

6. A construction is known for parameter values 2 and 3, and a legal operation extends every construction from `n` to `n+2`. What must be checked before claiming all `n>=2` work?
   A. Only one more example.  B. That the two bases cover both parity classes and the extension preserves the property.  C. A W/L table.  D. That the move count is monotone.

## First line only

7. A move transfers two counters out of one box and one counter into each of two other boxes. The question asks whether one configuration can reach another. Write the first line that starts an invariant analysis.

8. A process repeatedly swaps an adjacent inverted pair in a list. Write the first line that starts a termination proof.

9. Two players remove 1 or 2 stones from a heap; the player taking the last stone wins. Write the first line needed for a rigorous backward classification.

10. A move on a cyclic board toggles three consecutive binary lamps. Ordinary parity does not settle the target. Write the first line that starts a colour/weight invariant search.

11. A parameterized existence claim appears to have some impossible residue classes and some successful examples. Write the first line that prevents a necessity/sufficiency mix-up.

12. A state machine has several legal next states, and a target is specified. Write the single question that decides whether the problem is ordinary reachability or adversarial strategy.

## Self-check standard

A strong first line should identify the state, move effect, terminal rule, bounded one-way quantity, or proof direction that actually controls the problem. It should not be a disguised instruction to simulate many cases.
