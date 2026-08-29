# Counting, P&C, Pigeonhole & Inclusion–Exclusion — Wave 0 Topic Concept Map
## Issue #50 — NMTC Bhaskara Preliminary / Grade IX–X

**State:** `DRAFT_CONCEPT_MAP_COMPLETE_READY_FOR_WAVE1`

**Authoring rule:** This concept map is the pre-prose authority. The integrated Assimilation Book must not be written before the Wave-1 interfaces stabilize.

# 0. Governing model

The main question is not:

> Which formula do I remember?

It is:

> **What exactly is one outcome, and when are two descriptions the same outcome?**

```text
DEFINE ONE OUTCOME
        |
        v
ORDER MATTERS?
        |
        v
REPETITION / REPLACEMENT?
        |
        v
RESTRICTIONS BEFORE COUNTING
        |
        v
HOW IS THE SAMPLE SPACE BUILT?
  +----------------+----------------+----------------+
  |                |                |                |
SEQUENTIAL       DISJOINT        OVERLAPPING       EXISTENCE /
CHOICES          CASES           PROPERTIES        GUARANTEE
  |                |                |                |
multiply           add           inclusion-       pigeonhole /
                                  exclusion        extremal bound
        \              |              |              /
         \             |              |             /
          +------------+--------------+------------+
                       |
                       v
DIRECT OR COMPLEMENT?
                       |
                       v
BEST REPRESENTATION?
tuple / subset / digit string / case table / exponent tuple /
state graph / subset product / residue boxes / signed representation
                       |
                       v
COUNT
                       |
                       v
OVERCOUNT + OMISSION CHECK
                       |
                       v
SECOND-METHOD RECOUNT WHERE FEASIBLE
```

## Master invariant

> **A count is valid only when the counted object is defined, every valid object is counted, and each is counted exactly once.**

This turns combinatorics into a sample-space and representation discipline rather than formula selection.

---

# 1. PRIOR_KNOWLEDGE

A roughly 50%-prepared learner is likely to know:

- factorial notation;
- simple multiplication principle;
- `nPr` and `nCr` formulas;
- basic arrangements and selections;
- simple digit counting;
- elementary set union/intersection language;
- parity, divisibility, residues;
- basic algebraic expansion;
- simple paths in a grid/graph.

## Reliable fragments

The learner can often:
- evaluate `7P3` or `8C2`;
- multiply choices once stages are supplied;
- use a familiar formula after the problem is labeled;
- perform straightforward inclusion–exclusion arithmetic.

## What those fragments do not prove

They do not show that the learner can:
- define one outcome;
- decide whether swapping selected objects changes the outcome;
- separate repetition of **objects** from repetition of **descriptions**;
- make cases disjoint and exhaustive;
- decide direct vs complement;
- detect overlap before adding;
- identify pigeons and boxes;
- convert a coefficient to bounded integer-tuples;
- compress path enumeration into states;
- verify uniqueness before counting high-ceiling representations.

---

# 2. LIKELY_HALF_KNOWLEDGE

| Remembered fragment | Missing connection |
|---|---|
| `nPr` means arrangement | must decide whether roles/order actually distinguish outcomes |
| `nCr` means selection | must define whether internal order is irrelevant |
| “and” means multiply | only when a complete outcome requires sequential choices |
| “or” means add | only after the alternatives are disjoint, or overlap is corrected |
| “at least one” | often cheaper through complement |
| digit counting | leading zero and controlling position must be handled first |
| inclusion–exclusion formula | must identify actual intersections and avoid wrong signs |
| pigeonhole theorem | must define valid boxes and the occupancy contradiction |
| coefficient extraction | coefficient can be a count of bounded exponent choices |
| list paths | repeated transitions may be compressed by state |
| unusual representation | uniqueness must be proved before counting sign/digit choices |

---

# 3. MISSING_BRIDGES

## B1 — Outcome-object bridge

Complete the sentence before arithmetic:

`One outcome is a ________.`

Possible objects:
- ordered tuple;
- unordered subset;
- role assignment;
- digit string / integer;
- disjoint case type;
- path;
- state sequence;
- exponent tuple;
- selected subset of factors;
- residue-class placement;
- signed representation.

## B2 — Identity / sameness bridge

Ask:

> If I swap or reorder the selected objects, did I create a new outcome?

- yes → ordered;
- no → unordered.

This is the conceptual source of permutation vs combination.

## B3 — Repetition / replacement bridge

Separate:
- repeated choice allowed;
- repeated objects already present;
- replacement after selection;
- repeated descriptions of the **same** outcome caused by counting method.

The last one is overcount, not an allowed repetition.

## B4 — Restriction-first bridge

Restrictions alter the sample space before formulas:
- leading zero;
- parity via last digit;
- divisibility via residues/digit sum;
- distinctness;
- adjacency/separation;
- exact number of moves;
- allowed states/transitions.

## B5 — Add/multiply bridge

`SEQUENTIAL STAGES -> MULTIPLY`

`DISJOINT ALTERNATIVES -> ADD`

If alternatives overlap, plain addition is illegal until overlap is corrected.

## B6 — Case-partition bridge

Good casework is:
- mutually exclusive;
- collectively exhaustive.

Every case table must answer:
1. Why can no outcome appear twice?
2. Why can no valid outcome be missing?

## B7 — Direct/complement bridge

For:
- at least one;
- not all;
- contains a forbidden feature;
- avoids none;

test whether:

`TOTAL - COMPLEMENT`

is shorter and safer than direct casework.

## B8 — Exact-count vs guarantee bridge

`HOW MANY?` → construct/count sample space.

`PROVE SOME PAIR / BOX / CLASS MUST EXIST` → pigeonhole/extremal occupancy.

Pigeonhole is not a formula for the exact number of configurations.

## B9 — Overlap bridge

For `A or B`:
- if disjoint: add;
- if overlap possible: inclusion–exclusion.

The core invariant is counting each object exactly once.

## B10 — Algebra-to-count bridge

A coefficient in a product of finite sums can be interpreted as the number of bounded exponent tuples satisfying a sum equation.

## B11 — Product-to-subset bridge

In `∏(1+a_i)`, choosing `1` or `a_i` from each factor is equivalent to excluding/including element `i`.

## B12 — Path-to-state bridge

When transition rules repeat, define:
`state = current position/configuration after t moves`,
then count transitions rather than raw path strings.

## B13 — Representation-uniqueness bridge

For signed-power / balanced representations:
1. establish which representations are legal;
2. establish whether representation is unique;
3. only then count digit/sign patterns.

---

# 4. CORE INVARIANTS / STRUCTURES

## I1 — Exactly-once invariant

`VALID COUNT = all valid outcomes included - no duplicate counting`.

This is the umbrella invariant for casework, combinations, IE, complement, states and coefficient counting.

## I2 — Ordered selection

Choosing `r` distinct roles from `n` distinct objects gives a falling product because each role remains distinguishable.

`n(n-1)...(n-r+1)`.

The permutation formula is compression of this structure.

## I3 — Unordered selection

If internal reordering does not change the outcome, each selected `r`-set appears `r!` times in the ordered count.

So division by `r!` removes description-level overcount.

## I4 — Addition/multiplication

- one complete outcome requires all stages → product;
- one complete outcome lies in exactly one case → sum.

## I5 — Inclusion–exclusion

For two sets:
`|A∪B| = |A| + |B| - |A∩B|`.

For three:
`+ singles - pair intersections + triple intersection`.

It is bookkeeping for duplicate descriptions.

## I6 — Complement

`desired = total - forbidden/opposite`.

Use only when total and complement are both easier to define than direct desired cases.

## I7 — Pigeonhole occupancy

If `N` objects enter `k` boxes, some box contains at least `ceil(N/k)` objects.

Strong form is often proved by contradiction:
if every box had at most `m-1`, total ≤ `(m-1)k`.

## I8 — Subset-product expansion

Each factor contributes either inclusion or exclusion:
`∏(1+a_i)` enumerates products indexed by subsets.
The empty subset contributes `1`.

## I9 — Coefficient-as-count

Coefficient of `x^k` in a product of finite power sums equals the number of legal exponent tuples whose sum is `k`, subject to factor bounds.

## I10 — State recurrence

If the future only depends on the current state, path histories can be compressed into state counts.

## I11 — Representation uniqueness

A representation count is only meaningful after confirming whether one number/configuration can have multiple encodings.

---

# 5. REPRESENTATIONS

## R1 — Outcome sentence
`One outcome is a ...`

The primary Wave-2 representation.

## R2 — Ordered tuple / role table
Useful for positions, offices, digit slots, stages.

## R3 — Unordered subset
Useful for teams/committees/groups with no roles.

## R4 — Decision tree
Useful for restrictive first-position/last-position digit cases.

## R5 — Disjoint case table
Columns:
- case definition;
- restrictions;
- count;
- non-overlap reason;
- coverage reason.

## R6 — Set/Venn representation
Useful for overlap and inclusion–exclusion.

## R7 — Complement partition
`all = desired + forbidden`.

## R8 — Pigeon/box mapping
Explicitly name:
- pigeons;
- boxes;
- occupancy threshold.

## R9 — Exponent-tuple representation
Coefficient target:
`e1+e2+...=k` with bounds.

## R10 — Include/exclude factor representation
Subset products via binary choice per factor.

## R11 — State transition table/graph
Rows = time; columns = states; entries = path counts.

## R12 — Signed-digit / balanced representation
High-ceiling only; uniqueness checked first.

---

# 6. DECISION BOUNDARIES

## D1 — Ordered vs unordered

Same objects:
- choose 3 team members → unordered;
- assign president/secretary/treasurer → ordered.

## D2 — Addition vs multiplication

- choose a shirt **and** trousers → multiply;
- choose a red code **or** a blue code from disjoint classes → add.

## D3 — Plain addition vs inclusion–exclusion

- disjoint alternatives → add;
- `A or B` with overlap → add singles, subtract overlap.

## D4 — Direct vs complement

“at least one 7”:
- direct cases possible;
- total minus no 7 is usually shorter.

## D5 — Formula vs casework

A restriction can destroy the symmetry needed for one global `nPr/nCr`.
Use cases when a controlling position/residue changes the remaining choices.

## D6 — Distinct digits vs leading zero

A position may have fewer legal choices even before repetition is considered.

## D7 — Exact count vs pigeonhole guarantee

- exact number of residue patterns → counting;
- prove two integers share a residue → pigeonhole.

## D8 — Subset-product vs ordinary expansion

If every factor independently contributes `1` or `a_i`, think subset choices before expanding term-by-term.

## D9 — Coefficient algebra vs coefficient count

If exponents come from bounded finite sums, count exponent tuples before expanding.

## D10 — Raw path listing vs state compression

When many paths share the same current state, recurrence/state table is the cheaper representation.

## D11 — High-ceiling representation vs routine P&C

Balanced/signed representations require a uniqueness argument, not reflexive `2^n` or `3^n`.

## D12 — Clean source anchor vs source conflict / figure-gated item

Mechanism evidence does not authorize reconstruction of a missing state/grid diagram or forced reconciliation with a conflicting key.

---

# 7. MISCONCEPTION_TRAPS

1. `FORMULA_BEFORE_OBJECT`
2. `ORDER_ASSUMED_FROM_WORD_CHOOSE`
3. `ORDER_IGNORED_WHEN_ROLES_DIFFER`
4. `ADD_SEQUENTIAL_CHOICES`
5. `MULTIPLY_DISJOINT_ALTERNATIVES`
6. `OVERLAPPING_CASES_ADDED_DIRECTLY`
7. `CASEWORK_NOT_EXHAUSTIVE`
8. `LEADING_ZERO_COUNTED_AS_FULL_LENGTH`
9. `REPETITION_RULE_IGNORED`
10. `COMPLEMENT_COUNTS_WRONG_UNIVERSE`
11. `IE_INTERSECTION_NOT_COMPUTED`
12. `IE_SIGN_PATTERN_ERROR`
13. `PIGEONHOLE_WITHOUT_BOX_DEFINITION`
14. `PIGEONHOLE_USED_FOR_EXACT_COUNT`
15. `COEFFICIENT_EXPANDED_BEFORE_TUPLE_MODEL`
16. `EXPONENT_BOUNDS_IGNORED`
17. `EMPTY_SUBSET_FORGOTTEN_OR_DOUBLE_SUBTRACTED`
18. `RAW_PATH_LIST_OVERCOUNT`
19. `REPRESENTATION_UNIQUENESS_ASSUMED`
20. `SOURCE_KEY_FORCED_TO_AGREE`

---

# 8. FIRST-MOVE CUES

| Visible cue | First move |
|---|---|
| choose/assign objects | define one outcome; ask if swapping changes it |
| several successive slots/stages | write choices per stage |
| one of several structural types | define disjoint cases |
| digit number with restrictions | identify controlling position/residue first |
| “at least one” / “not all” | test complement |
| `A or B` with overlap possible | identify intersections |
| prove repetition/existence | name pigeons and boxes |
| sum over subset products | model include/exclude per element |
| coefficient of finite product | introduce bounded exponent variables |
| exact-length walk | define states and transitions |
| signed/base representation | prove legality/uniqueness before counting |
| key conflicts with direct count | independently define sample space; preserve conflict |

---

# 9. TRANSFER ENDPOINTS

Ownership is shown when the learner can:

1. classify the same objects as ordered in one prompt and unordered in another;
2. build a mixed role+group outcome (one role distinguished, remaining group unordered);
3. handle leading zero plus parity/divisibility in one digit problem;
4. choose disjoint casework rather than force one global formula;
5. switch an “at least one” problem to complement;
6. recognize overlap and invoke inclusion–exclusion;
7. distinguish exact count from minimum-guarantee pigeonhole reasoning;
8. create valid residue/interval boxes for a new pigeonhole problem;
9. reinterpret a product expansion as subset choices;
10. reinterpret a coefficient as a bounded integer-tuple count;
11. replace raw path listing by states;
12. solve a smaller balanced/signed representation problem after proving uniqueness;
13. reject a source/key conflict rather than mutate the sample space.

---

# 10. SOURCE / FIGURE CUSTODY

Repository-native evidence states:

- `CLEAN_SCORED_ANCHOR`
- `FIGURE_GATED_ANCHOR`
- `BRIDGE_EVIDENCE`
- `SOURCE_CONFLICT_EVIDENCE`
- `SYLLABUS_FIRST_AUTHOR_CREATED`

## Current qualified mechanism map

- `NMTC-BH-P-2019-Q07` — subset-product expansion — `CLEAN_SCORED_ANCHOR`.
- `NMTC-BH-P-2019-Q09` — geometric configuration classification — `CLEAN_SCORED_ANCHOR_WITH_MODEL_HELPFUL`.
- `NMTC-BH-P-2019-Q12` — connected configuration count — `FIGURE_GATED_ANCHOR`.
- `NMTC-BH-P-2019-Q22` — exceptional-case enumeration — `BRIDGE_EVIDENCE`.
- `NMTC-BH-P-2019-Q23` — exact-move path/state count — `FIGURE_GATED_ANCHOR`.
- `NMTC-BH-P-2019-Q28` — balanced representation count — `CLEAN_HIGH_CEILING_BRIDGE`.
- `NMTC-BH-P-2019-Q30` — coefficient as count — `CLEAN_SCORED_ANCHOR`.
- `NMTC-BH-P-2025-Q21` — digit restriction/divisibility count — `CLEAN_SCORED_ANCHOR`.
- `NMTC-BH-P-2025-Q10` — inequality-to-integer count — `BRIDGE_EVIDENCE`.
- `NMTC-BH-P-2023-Q25` — odd-digit count with unexplained key restriction — `SOURCE_CONFLICT_EVIDENCE`.

## Wave-0 custody rule

- Do not reconstruct 2019 Q12/Q23 figures/state diagrams from prose.
- Do not use 2023 Q25 as answer authority.
- Do not treat high-ceiling 2019 Q28 as entry-level.
- Pigeonhole and inclusion–exclusion remain syllabus-first and use clearly labeled author-created material where clean recurrence is sparse.
- No five-year domain percentage is promoted as official NMTC weightage.

---

# 11. SEVEN WAVE-1 PATHS

Every stream must instantiate:

`PRIOR -> OUTCOME OBJECT -> REPRESENTATION -> INVARIANT -> FIRST MOVE -> OVERCOUNT CHECK -> CONTRAST -> TRANSFER -> SOURCE`

## W1-A — Define the counted object
Prior: nPr/nCr recall.
Bridge: outcome identity and swap test.
Representation: tuple/subset/string/configuration.
Invariant: same outcome must not receive multiple descriptions.
First move: `One outcome is ...`
Overcount risk: treating internal order as new when it is not.
Transfer: one distinguished role + unordered remainder.

## W1-B — Addition / multiplication / casework
Prior: multiplication principle.
Bridge: sequential vs alternative construction.
Representation: stage tree / case table.
Invariant: multiply stages; add disjoint cases.
Overcount risk: overlapping cases.
Transfer: hidden case partition.

## W1-C — P&C from structure
Prior: factorial formulas.
Bridge: derive ordered falling product; divide description-level order when irrelevant.
Representation: positions/roles vs subset.
Invariant: order identity.
Overcount risk: `r!` internal permutations.
Transfer: constrained arrangements/repeated objects without formula reflex.

## W1-D — Digit restrictions & complement
Prior: place value.
Bridge: controlling position + universe definition.
Representation: slot table / complement partition.
Invariant: leading position and divisibility/parity constraints define legal sample space.
Overcount risk: leading zero, repeated digit.
Transfer: simultaneous parity + digit-sum/residue restrictions.

## W1-E — Inclusion–exclusion & pigeonhole
Prior: sets/remainders.
Bridge: exact-count vs guarantee.
Representation: Venn/set counts vs boxes.
Invariant: correct overlap accounting / forced occupancy.
Overcount risk: double-counted intersections or invalid boxes.
Transfer: divisibility union; residue/interval pigeonhole.

## W1-F — Subset-product / coefficient-as-count
Prior: algebraic expansion.
Bridge: term choice = combinatorial choice.
Representation: subset indicator / bounded exponent tuple.
Invariant: one term-selection tuple produces an exponent/product contribution.
Overcount risk: empty subset or exponent bounds.
Transfer: three-factor coefficient with asymmetric bounds.

## W1-G — State/path/high-ceiling representations
Prior: small path listing, powers/base representation.
Bridge: compress histories into states; prove representation uniqueness.
Representation: transition table / signed digits.
Invariant: same state summarizes future; unique encoding before pattern count.
Overcount risk: multiple encodings of same object.
Transfer: text-complete graph; smaller balanced representation.
Source gate: figure-gated historical paths stay gated.

---

# 12. WAVE-0 PROMOTION CONDITIONS

- [x] prior knowledge mapped;
- [x] half-knowledge mapped;
- [x] outcome-definition bridge explicit;
- [x] ordered/unordered boundary explicit;
- [x] repetition/replacement/description-overcount separated;
- [x] add/multiply/casework boundary explicit;
- [x] direct/complement boundary explicit;
- [x] overlap/inclusion–exclusion explicit;
- [x] exact-count/pigeonhole boundary explicit;
- [x] coefficient/subset/state representations explicit;
- [x] high-ceiling lane separated from foundations;
- [x] source/figure custody explicit;
- [x] all seven Wave-1 paths represented;
- [x] no figure-gated historical object reconstructed;
- [x] no integrated student prose authored before interface stabilization.
