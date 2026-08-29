# Counting, P&C, Pigeonhole & Inclusion–Exclusion — First-Step Reference
## Issue #50 · Wave 3

**Compression after teaching — not the teaching layer.**

Fast spine:
`OBJECT → ORDER? → REPETITION? → RESTRICTIONS → ADD/MULTIPLY/OVERLAP → DIRECT/COMPLEMENT → EXACT/GUARANTEE → REPRESENTATION → CHECK`

# 1. Object-definition checklist
Before arithmetic:
- One outcome is a ______.
- Does swapping chosen objects change the outcome?
- Is repetition/replacement allowed?
- Are there position/role restrictions?
- Could two descriptions denote the same outcome?

# 2. Order/repetition decision tree
```text
SELECT / ASSIGN
  |
  +-- swapping changes outcome? YES -> ordered
  |                              |
  |                              +-- distinct roles/positions -> falling product
  |
  +-- NO -> unordered subset
          |
          +-- ordered descriptions overcount by internal permutations
```

Repeated identical objects are a different issue: divide permutations of indistinguishable copies.

# 3. Sample-space composition cards
## Sequential stages
All stages needed -> multiply.
## Disjoint cases
Exactly one case -> add.
## Overlap possible
Correct by inclusion-exclusion or repartition.

# 4. Restriction card
For digits:
1. integer or code?
2. leading zero?
3. last digit controls parity/5?
4. digit-sum/residue?
5. repetition allowed?

Handle the controlling restriction before generic formula use.

# 5. Direct-vs-complement card
Signals:
`at least one`, `not all`, `contains a forbidden feature`.
Test:
`TOTAL - NONE/OPPOSITE`.

# 6. Inclusion–exclusion card
Two sets:
`|A∪B|=|A|+|B|-|A∩B|`.

Three:
`+ singles - pairs + triple`.

# 7. Pigeonhole card
First write:
- pigeons = ?
- boxes = ?
- target occupancy = ?

Strong form:
deny target occupancy, calculate maximum possible total, contradict.

# 8. Subset-product card
`∏(1+a_i)` = sum of products over all subsets.
Non-empty subset sum -> subtract empty product `1`.

# 9. Coefficient-as-count card
Coefficient of `x^k` in finite power-sum product:
- choose exponent from each factor;
- write exponent-sum equation;
- enforce each factor’s bounds;
- count ordered exponent tuples.

# 10. State/path card
If legal next moves depend only on current state:
`define state → transition counts → iterate`.
Do not use raw `2^m` when boundaries invalidate move strings.

# 11. Representation uniqueness card
Before counting digit/sign encodings:
- legal digits?
- all target objects covered?
- unique representation?
If not unique, encoding count ≠ object count.

# 12. Fast contrast table
| Pair | Boundary |
|---|---|
| team vs offices | unordered vs ordered |
| stages vs cases | multiply vs add |
| disjoint vs overlap | plain add vs IE |
| direct vs complement | desired cases vs total-minus-opposite |
| integer vs PIN | leading-zero legality |
| exact count vs guarantee | enumeration vs pigeonhole |
| expansion vs coefficient count | algebra vs exponent tuples |
| path list vs states | histories vs compressed state |
| encodings vs objects | uniqueness required |

# 13. Source warnings
- 2019 Q07: clean subset-product mechanism.
- 2019 Q09: clean classification mechanism.
- 2019 Q12/Q23: figure-gated; do not recreate exact historical diagram.
- 2019 Q28: high-ceiling bridge, not entry.
- 2019 Q30: clean coefficient-as-count.
- 2025 Q21: clean digit/divisibility.
- 2023 Q25: source conflict; printed sample space gives 20, key restriction is unexplained.

# 14. Recognition-only drill
Write only the object + first move.

1. 3-person committee from 9.
2. president/secretary/treasurer from 9.
3. one captain and two ordinary committee members from 8.
4. 4-digit even integer from a restricted digit set.
5. 4-digit PIN containing at least one 0.
6. objects satisfying A or B with overlap.
7. disjoint red or blue code classes.
8. meal with one main and one drink.
9. prove collision among residues mod 7.
10. guarantee at least 5 objects in a box.
11. sum nonempty subset products.
12. coefficient of `x^12` in two finite sums.
13. coefficient in three bounded finite sums.
14. exact-length walk on a bounded line.
15. repeated letters in a word.
16. historical grid/path figure missing.
17. source key conflicts with direct sample-space count.
18. representation with digits `-1,0,1`.
19. 5-digit number divisible by 5.
20. at least one A in a length-6 string.
21. count union of multiples of 2,3,5.
22. classify geometric configurations into several types.
23. two casework rows overlap.
24. fixed-length code allows leading zero.

# 15. Five-second check
`OBJECT? ORDER? RESTRICTION? OVERLAP? TARGET TYPE? REPRESENTATION? EXACTLY ONCE?`
