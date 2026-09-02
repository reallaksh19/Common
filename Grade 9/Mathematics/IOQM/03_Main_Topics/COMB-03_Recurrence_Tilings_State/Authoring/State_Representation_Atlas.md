# COMB-03 — State Representation Atlas

Status: `AUTHORING_RESEARCH_ONLY`

Purpose: freeze the representation decisions COMB-03 must own once the COMB-01 counting/model interface is available. This file is not student prose and does not teach generic counting foundations.

## Governing question

`WHAT INFORMATION ABOUT THE CURRENT SITUATION IS SUFFICIENT TO DETERMINE ALL LEGAL NEXT MOVES AND THEIR COUNTS?`

A valid state must be:
1. sufficient — no future transition depends on forgotten information;
2. minimal — remove information that does not change future behavior;
3. canonical — two histories with the same future behavior map to the same state;
4. verifiable — base states and transitions can be checked directly.

## Representation families

| Family | State example | Transition type | Typical failure |
|---|---|---|---|
| remaining-size | `T_n` = number of completions of length/size `n` | first/last-piece decomposition | branches overlap or omit a piece type |
| finite memory | `(n,s)` where `s` stores previous local condition | local transition table | one-state recurrence forgets necessary memory |
| graph vertex | current integer/configuration `x` | legal operation edge `x -> y` | forward search explodes while reverse predecessors are sparse |
| residual quantity | remaining excess/deficit `r` | partition/composition of residual | forcing a recurrence when direct representation is cheaper |
| carry state | `(position,carry,remaining count)` | digit/binary carry transition | treating columns independently when carry couples them |

## Anchor A — IOQM-2023-Q08: tiling / first-step decomposition

### Minimal state
`T_n`: number of admissible tilings of the remaining `2 x n` strip under the relevant tile inventory.

### Why sufficient
After fixing the leftmost legal tile/block, the unsolved part is again a strip of the same type with smaller width. No earlier history changes its legal completions.

### Required validation
- every completed tiling has exactly one leftmost first piece/configuration;
- branches are disjoint;
- every branch leaves a smaller canonical strip state;
- base widths are defined explicitly.

### Wrong representations
- `state = number of tiles already used`: insufficient because different remaining widths/configurations may share the same tile count;
- listing full partial tilings: sufficient but not minimal;
- recurrence without base states: semantically incomplete.

### Transfer signature
Changed surface: words, paths, stair steps, strings with local blocks.
Invariant: first choice leaves the same kind of smaller object.

## Anchor B — IOQM-2024-Q20: deterministic operation graph / reverse search

### State
Current integer `x`.

### Forward transitions
Edges are the allowed operations from `x`.

### Reverse representation
For a fixed target `t`, study legal predecessors of a state. Reverse search is preferred when each target state has few predecessors even though forward branching is wide.

### Sufficiency test
The legality and result of the next operation depend only on current `x`, not the path used to reach `x`.

### Wrong representations
- storing the entire path in the state: not minimal for shortest-distance BFS;
- assuming a greedy forward move without a monotone invariant;
- calling the problem a game when no opponent chooses a move.

### Verified research path
A 10-move witness exists:
`11 -> 8 -> 5 -> 10 -> 20 -> 17 -> 34 -> 31 -> 62 -> 124 -> 121`.
Independent BFS/reverse-state research confirms no shorter path.

## Anchor C — IOQM-2024-Q14: near-boundary sparse history

### Representation
Do not build a large recurrence automatically. Represent the total displacement relative to the maximum possible displacement.

If an extremal path would use the maximal step at every position, a target only slightly below that maximum is encoded by a small deficit. The history collapses to the location/type of exceptional step(s).

### Decision lesson
`STATE-FIRST` does not mean `RECURRENCE-ALWAYS`.
A compressed deficit representation may turn a long process into a small counting problem.

### Wrong representation
Tracking all 80 step choices independently when the target sum forces exactly one exceptional event.

## Anchor D — IOQM-2023-Q21: partition residual

### Representation
Choose the maximal forced baseline first. Encode only the residual amount `r` that remains to be distributed.

For the verified anchor, the residual is `7`; the count becomes the partition number `p(7)=15`.

### Why recurrence may be unnecessary
The right representation is the residual partition, not necessarily a time-indexed recurrence. COMB-03 owns the representation decision; it should not force recursion onto every counting problem.

### Wrong representations
- treating order as significant when the representation is an unordered partition;
- expanding a long dynamic program when a tiny residual can be enumerated/recognized directly.

## Anchor E — IOQM-2023-Q26: carry-state counting

### Minimal state family
A column-by-column state must retain enough information to determine legal next digit/count choices. Typical coordinates:
`(column index, incoming carry, remaining multiplicity/count information)`.

### Why one-state recurrence fails
Two partial histories at the same column can have different incoming carries; their future possibilities differ. Therefore `T_n` alone is insufficient.

### Canonical merge rule
Histories may be merged only when all retained state coordinates agree and hence they have identical future transition sets/counts.

### Research verification
Independent direct DP and binary carry-state DP both return `19` for the anchor.

## State sufficiency falsifiers

Before accepting a state, attempt to produce two histories with the same proposed state but different legal futures.

If such a pair exists, the state is insufficient.

Examples:
- same remaining length but different previous symbol when adjacency restrictions exist;
- same column but different carry;
- same current score but different player-to-move in an adversarial game;
- same number of chosen objects but different restriction status.

## Minimality test

For each coordinate in a proposed state:
1. delete the coordinate;
2. ask whether two previously distinct states now merge;
3. test whether their future transition sets/counts are still identical.

If yes, the coordinate was unnecessary. If no, retain it.

## Forward vs reverse decision

Prefer reverse-state search when:
- target is fixed;
- predecessor map is simpler/sparser than successor map;
- inverse moves are well-defined enough to enumerate;
- shortest distance or reachability is the target.

Prefer forward DP/recurrence when:
- base state is natural;
- transitions increase size/index monotonically;
- many targets share the same computed table.

## Deterministic state vs adversarial game boundary

COMB-03 owns deterministic state evolution and counting paths through states.
COMB-04 owns adversarial strategy, player-to-move semantics, winning/losing states, and minimax-style reasoning.

A process is not a game merely because it has multiple legal moves.

## Algebraic recurrence vs counting recurrence boundary

ALG-04 supplies recurrence notation, initialization, semantics, verification, and local algebraic cancellation.
COMB-03 adds the derivation:
`counted object -> disjoint/exhaustive first-step classes -> smaller states -> counting recurrence`.

Do not reteach AP/GP or generic recurrence algebra here.

## Promotion condition

This atlas may be promoted into student-facing examples only after the COMB-01 interface passes `C01-1..C01-10` and `T1..T6` in `COMB01_Interface_Acceptance_Contract.md`.