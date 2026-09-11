# COMB-01 Stable Counting / Model Interface v1

Status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`
Provider: `IOQM-G9-COMB-01`
Primary consumers: `IOQM-G9-COMB-02`, `IOQM-G9-COMB-03`

This interface exports concise counting/model semantics. Consumers retrieve these statements; they do not rebuild the underlying counting chapter.

## Minimum provider payload

### C01-1 — Counted-object definition
**Canonical wording:** Before counting, define one valid object/outcome and state when two objects are considered the same.
Retrieval example: “A state represents one partial tiling with the same remembered boundary data; two construction histories leading to the same defined state are not automatically two states.”

### C01-2 — Addition principle semantics
**Canonical wording:** Add case counts only when the cases are disjoint. If cases overlap, naive addition is invalid.

### C01-3 — Multiplication principle semantics
**Canonical wording:** Multiply stage counts when an object is built through sequential choices and the stated count at each stage is the number of choices available after the earlier stage choices.

### C01-4 — Exhaustiveness discipline
**Canonical wording:** A case split is valid only if every valid object enters at least one case. A disjoint-and-exhaustive split makes every valid object enter exactly one branch.
Checklist question: `Does every valid object enter exactly one branch?`

### C01-5 — Ordered vs unordered decision
**Canonical wording:** Order is structural when exchanging positions/roles/stages changes the object. If exchanging selected elements does not change the object, count unordered selections and remove the permutation overcount.
Retrieval cue: “Would swapping the two selected elements create a different valid object?”

### C01-6 — Direct vs complement decision
**Canonical wording:** When the desired event is difficult but its negation has a simpler description, count `universe - complement`. The universe and complement must use the same object definition.

### C01-7 — Restriction vocabulary
Use these stable terms:
- **allowed choice:** satisfies all restrictions active at that stage;
- **forbidden choice:** violates at least one active restriction;
- **state memory / remembered condition:** information needed so future allowed choices can be determined;
- **local restriction:** depends only on the current position/stage/state;
- **global restriction:** depends on the completed object or on information that must be carried in state;
- **admissible object:** satisfies every original restriction.

### C01-8 — Inclusion-exclusion boundary
**Canonical wording:** If properties/cases overlap, do not add their counts as if disjoint. Either redesign a disjoint split or use inclusion-exclusion from the counting owner. A recurrence consumer must fail closed rather than inventing its own generic IE chapter.

### C01-9 — Repeated-object distinction
**Canonical wording:** Two copies are indistinguishable only if swapping them does not create a new counted object. When labelled arrangements differ only by permutations inside identical classes, divide by those internal permutation counts exactly once.

### C01-10 — Digit-string counting boundary
**Canonical wording:** Counting admissible digit strings belongs here once the arithmetic property/restriction is known. Deriving divisibility, decimal-block, digit-sum/product or place-value arithmetic rules belongs to the number-theory digit owner.

## Compatibility tests

### T1 — Retrieval, not reteaching: PASS
A consumer may write “these first-step cases are disjoint, so add their counts” using C01-2 without deriving the addition principle.

### T2 — Exact-one-branch test: PASS
C01-4 provides the exact canonical question: `Does every valid object enter exactly one branch?`

### T3 — Ordered/unordered stability: PASS
C01-5 defines identity structurally and does not depend on `nPr`/`nCr` notation.

### T4 — Overlap fail-closed: PASS
C01-2 and C01-8 explicitly prohibit naive addition of overlapping branches.

### T5 — Restriction handoff: PASS
C01-7 provides `state memory / remembered condition` plus local/global restriction language sufficient to name previous tile type, carry, boundary occupancy or any other information needed to determine future legal moves.

### T6 — Boundary ownership: PASS
Consumers do not own generic permutation/combination derivation, repeated-object formula derivation, generic complement/IE teaching, or arithmetic digit properties. Those remain with this provider or the digit-arithmetic owner as stated above.

## Retrieval map for COMB-03

| Consumer move | Retrieve here | Consumer adds |
|---|---|---|
| define counted state | C01-1, C01-7 | minimal sufficient state |
| split by first/last move | C01-2, C01-4 | recurrence from smaller states |
| count transition stages | C01-3 | transition-specific choices |
| avoid double count | C01-5, C01-8 | recurrence branch validation |
| compare direct/complement/recursive routes | C01-6 | recursion usefulness test |

No student-facing control codes are exported from this authoring interface into learner materials.
