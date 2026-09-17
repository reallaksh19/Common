# Recurrence, Tilings & State Evolution

The common idea is **remember exactly what the future needs**. A recurrence is not a pattern guessed from a few numbers. It is a counting identity produced by a precise state and an exactly-once decomposition.

## 1. Reconnect: a symbol must name an object

Suppose `T_n` counts tilings of a `2 x n` rectangle by `2 x 1` dominoes. Before any recurrence is written, the object is fixed: one complete domino tiling of that rectangle.

Look at the left edge. Either one vertical domino is placed, leaving a `2 x (n-1)` rectangle, or two horizontal dominoes start together, leaving a `2 x (n-2)` rectangle. These cases are disjoint and exhaustive, so

`T_n = T_{n-1} + T_{n-2}`.

The base states have combinatorial meaning: `T_0=1` because the empty board has one empty tiling, and `T_1=1` because the `2 x 1` board has one tiling.

The order of thought is therefore:

`OBJECT -> STATE -> EXACTLY-ONCE SPLIT -> SMALLER STATE -> BASE STATES -> RECURRENCE`.

## 2. State sufficiency: can two histories with the same state have different futures?

A state is sufficient when it remembers every fact that can change future legal choices, and no irrelevant history.

Consider compositions of `n` using parts 1 and 2, with no two consecutive 2s. The remaining sum alone is not sufficient: arriving with previous part 1 and arriving with previous part 2 give different legal next moves. Add one memory bit: whether the previous part was 2.

A useful falsifier is:

**Can two histories with this same proposed state have different legal futures?**

If yes, the state is too small. If no coordinate affects future choices, the state may be too large.

## 3. One-state recurrence versus hidden memory

For binary strings with no consecutive 1s, a one-state recurrence can still work after a structural first-symbol split. Let `A_n` count valid strings of length `n`.

- first symbol 0: append any valid string of length `n-1`;
- first symbols 10: append any valid string of length `n-2`.

Thus `A_n=A_{n-1}+A_{n-2}` with `A_0=1, A_1=2`.

But if the condition also requires an even number of 1s, the future acceptance condition depends on parity. A state must now remember both the last-bit restriction and the parity of the number of 1s used so far. The recurrence becomes a small transition table rather than one scalar formula.

The lesson is **state first, not scalar recurrence always**.

## 4. Tilings: freeze the first unresolved region

For a board or strip, identify the first unresolved cell or column. List all legal ways to cover it, and stop each branch as soon as the remaining region becomes a previously defined state.

Three checks are mandatory:
1. every complete tiling begins in one listed branch;
2. no complete tiling begins in two branches;
3. each branch leaves a smaller canonical state.

If a special tile can be used at most once, the board size alone may not determine the future. Add a flag recording whether the special tile has already been used.

## 5. Deterministic state graphs and reverse search

A process with legal moves creates a directed graph: states are vertices and legal moves are directed edges. Multiple choices do **not** make the problem a game unless an opponent is choosing moves to optimize an outcome.

For the machine `x -> x+1` or `x -> 2x`, a forward search from 1 can branch rapidly. If the target is fixed, reverse predecessors are often simpler:

- predecessor `y-1` always exists for the `+1` move;
- predecessor `y/2` exists when `y` is even for the doubling move.

Searching backward from the target explores the same reachability structure in the opposite direction. The direction is a representation choice, not a change in the mathematics.

## 6. Carry state: local memory can replace global enumeration

Suppose a number is represented as a sum of powers of 2, with each power usable at most twice. A global list of partitions is possible but quickly becomes messy. Process binary positions from low to high.

At each position, the legal choice depends on the target digit and the incoming carry. Therefore a local state such as

`(digit position, incoming carry)`

contains the information needed for future choices. The arithmetic rule producing the carry must already be understood; the new combinatorial work is to count the legal state transitions.

## 7. Recurrence is not always the best endpoint

State thinking may reveal a simpler non-recursive representation.

Example: words containing 4 E's and 3 N's with no consecutive N's. Place the four E's first. They create five gaps, and choose three of those gaps for the N's. The count is `C(5,3)=10`.

A state recurrence can count the same objects, but the gap representation is smaller. A strong solver asks for the cheapest correct representation rather than forcing recurrence.

## 8. Mandatory contrasts

### Supplied algebraic recurrence vs counting recurrence

If a recurrence is given and the main work is algebraic manipulation, use recurrence algebra already learned. If the relation itself must be proved from what is counted, define the state and derive it structurally here.

### Direct count vs recursive decomposition

A recurrence is natural when a first or last structural move leaves smaller copies of the same state. A direct count is better when a single representation, symmetry, or gap choice collapses the whole problem.

### Deterministic evolution vs adversarial game

A deterministic reachability problem may have many legal moves, but there is no opponent. Winning/losing strategy belongs only when another player chooses against you.

### One state vs hidden memory

If two histories with the same proposed state can have different futures, enrich the state. If they cannot, do not carry unnecessary history.

## 9. Historical source anchors

The validated IOQM anchors illustrate five different representations:

- `2023 Q08`: tiling decomposition from the first unresolved region;
- `2024 Q20`: deterministic reverse-state search;
- `2024 Q14`: sparse near-boundary state history, where recurrence is not forced;
- `2023 Q21`: residual/partition representation;
- `2023 Q26`: carry-state representation counting.

Their verified answers are `59, 10, 80, 15, 19` respectively. Historical stems remain source-controlled; the lesson is the representation and first move, not memorization of a paper solution.

## 10. Adopt the router

For a new problem, write these questions before arithmetic:

1. What exactly is one object or reachable state?
2. What information must the state remember for future legality?
3. Can every object be assigned to exactly one first or last transition?
4. What smaller state remains in each branch?
5. What do the base states mean?
6. Is one state enough, or is hidden memory required?
7. Would reverse search, symmetry, gaps, residual structure, or a carry table be smaller than a recurrence?
8. Can small cases independently verify the model?

**Define the state before writing the recurrence.**
