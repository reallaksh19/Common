# COMB-05 — Pigeonhole & Extremal Reasoning: Concept and Dependency Map

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Scope and ownership

Canonical owner: `IOQM-G9-COMB-05`.

Owned here:
- direct pigeonhole and box/object modelling;
- generalized pigeonhole;
- extremal choice;
- contradiction through a nearest/farthest/largest/smallest object;
- geometric pigeonhole surfaces;
- number-theoretic pigeonhole surfaces.

Retrieved, not retaught:
- elementary addition/multiplication counting when a finite total is needed;
- elementary remainder language;
- basic convex-polygon facts such as a triangulation having `n-3` diagonals.

Explicit boundaries:
- exact overlap correction by inclusion-exclusion belongs to `COMB-01`;
- inequality optimization belongs to `ALG-02`;
- graph terminology/handshaking belongs to `COMB-02`;
- adversarial optimal-play reasoning belongs to `COMB-04`.

## Learner state

| Layer | Likely state | Repair target |
|---|---|---|
| prior knowledge | informal “some two must…” reasoning | name objects and boxes before claiming inevitability |
| half-knowledge | knows `n+1` objects in `n` boxes forces a collision | choose the right equivalence classes/regions |
| missing bridge | treats averaging, counting and pigeonhole as the same idea | separate exact count, average bound and structural collision |
| missing bridge | searches many cases before choosing an extremal object | choose smallest/largest/nearest/farthest first |
| ownership target | can recognize and prove forced structure under changed surfaces | write the box map or extremal choice as the first line |

## Governing router

`EXISTENCE OR FORCED MULTIPLICITY? -> DEFINE OBJECTS -> DEFINE BOXES/EQUIVALENCE -> COMPARE LOAD WITH CAPACITY -> FORCED COLLISION`

or, when the surface is not naturally a box model:

`FINITE CONFIGURATION -> CHOOSE AN EXTREME OBJECT -> USE WHAT EXTREMALITY FORBIDS -> CONTRADICTION/STRUCTURE`

## Knowledge dependencies

1. `G9_CORE`: finite sets, inequalities between integers, simple division with remainder.
2. `IOQM_BRIDGE`: an exact definition of “same box” as an equivalence class or geometric region.
3. `IOQM_BRIDGE`: capacity formulation: if each box held at most `r`, then `m` boxes could hold at most `rm` objects.
4. `IOQM_BRIDGE`: extremal existence for a finite nonempty set: smallest/largest value and closest/farthest pair exist.
5. Owned synthesis: choose the representation before calculating.

No advanced permutation formula is a prerequisite.

## Method-selection map

| Visible surface | Structural question | First move | Nearby wrong route |
|---|---|---|---|
| “prove two have the same…” | what relation partitions the objects? | name the equivalence classes as boxes | enumerate pairs |
| more objects than classes | what is the maximum load if no collision occurs? | write the capacity contradiction | compute an average and stop |
| “at least k in one group” | what per-box cap would contradict the total? | compare total with `(k-1)×boxes` | use only the basic two-in-one form |
| finite set with closure/descent | which smallest/largest object is impossible? | choose an extremal element | optimize a numerical expression |
| points in a region | how can the region be partitioned so one cell has small diameter? | draw/describe the cells | coordinate every pair |
| divisibility/remainders | which residue/odd-part class makes the target automatic? | define the class map | test differences one by one |
| exact number satisfying overlapping properties | is exact counting actually requested? | route to inclusion-exclusion | force pigeonhole merely because sets overlap |

## Mandatory contrast boundaries

### Pigeonhole vs inclusion-exclusion
Pigeonhole proves that some box exceeds a capacity. Inclusion-exclusion computes a union size after correcting overlap. If an exact count is requested, pigeonhole is usually not the counting engine.

### Extremal choice vs inequality optimization
Extremal choice selects an object already present in a finite configuration and exploits its minimal/maximal status. Inequality optimization bounds a variable expression over a feasible domain.

### Counting average vs structural inevitability
An average may suggest the correct threshold, but the proof is integral capacity: if every box had at most `r`, the total would be at most `rm`. The contradiction is structural, not probabilistic.

## Transfer map

- residue classes -> divisible differences;
- odd-part classes -> divisibility chains;
- interval partitions -> close real numbers;
- square/triangle partitions -> close planar points;
- extremal smallest positive element -> descent/closure contradictions;
- closest pair -> midpoint/perturbation contradictions;
- source extremal counting -> complement capacity bounds.

## Source custody

Primary historical anchors:
- `IOQM-2023-Q18` — validated answer `71`; geometric/extremal diagonal surface.
- `IOQM-2023-Q27` — validated answer `91`; extremal-set/complement-count surface.

Both are `CLEAN_VALIDATED` in the frozen corpus and independently rechecked in `Authoring/Independent_Math_and_Source_Audit.md`.

## Architecture state

`WAVE0_ARCHITECTURE_FROZEN`

Classroom timing/readability, retention, psychometrics, qualification probability, percentile/pass-mark calibration and publication approval: `NOT_RUN`.
