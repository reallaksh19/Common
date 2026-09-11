# COMB-03 — Overlap and Ownership Ledger

Status: `CURRENT_CORPUS_REVALIDATED__PASS`

Revalidated against production base `47af427f65a3370676931f885df09494524b9424` and accepted provider artifacts:
- COMB-01 `COMB01_Stable_Counting_Model_Interface_v1.md` (`c4d80b...`);
- ALG-04 `ALG04_Recurrence_Interface_v1.md` (`12891c...`).

## Canonical ownership table

| Concept / mechanism | Owner | COMB-03 treatment |
|---|---|---|
| sequence notation/indexed terms | ALG-04 | retrieve only |
| explicit vs recursive sequence description | ALG-04 | retrieve only |
| recurrence initialization form / valid indices | ALG-04 | retrieve; COMB-03 supplies combinatorial base-state meaning |
| algebraic recurrence verification/manipulation | ALG-04 | retrieve only after COMB-03 structural derivation |
| AP/GP, telescoping, generic sequence algebra | ALG-04 | outside COMB-03 canon |
| counted-object identity | COMB-01 | retrieve C01-1; extend to state identity |
| addition/multiplication semantics | COMB-01 | retrieve C01-2/C01-3 |
| disjoint/exhaustive discipline | COMB-01 | retrieve C01-4; COMB-03 proves recurrence branches meet it |
| ordered/unordered identity | COMB-01 | retrieve C01-5 |
| complement/IE | COMB-01 | one-line decision cue; generic teaching routed out |
| restriction/state-memory vocabulary | COMB-01 | retrieve C01-7; COMB-03 designs sufficient state |
| overlap fail-closed | COMB-01 | retrieve C01-8; overlapping recurrence branches block derivation |
| repeated-object distinction | COMB-01 | retrieve C01-9 when identity requires it; no formula lesson |
| admissible digit-string counting | COMB-01 | applies only after arithmetic rule is supplied |
| arithmetic digit/place-value/divisibility rule | NT-05 | route out |
| minimal sufficient state | COMB-03 | canonical owner |
| state sufficiency falsifier | COMB-03 | canonical owner |
| first/last transition decomposition | COMB-03 | canonical owner |
| recurrence from counting structure | COMB-03 | canonical owner |
| multi-state / finite-memory recurrence | COMB-03 | canonical owner |
| tiling/path state recurrence | COMB-03 | canonical owner |
| deterministic transition graph | COMB-03 | canonical owner |
| forward vs reverse-state search | COMB-03 | canonical owner |
| carry-state transition after arithmetic rule supplied | COMB-03 | canonical owner |
| residual/partition representation as state alternative | COMB-03 | representation choice only; generic partition theory not inflated |
| adversarial player-to-move strategy | COMB-04 | route out |
| winning/losing state / minimax / game invariant | COMB-04 | route out |

## Current-corpus boundary tests

### B1 — COMB-01 vs COMB-03: PASS
If the decisive work is generic permutation/combination, repeated-object counting, complement/IE or non-evolving admissible-string counting, COMB-01 owns it. COMB-03 begins only when a state/transition decomposition or state representation is decisive. Q08 uses C01-2/C01-4 as retrieval but COMB-03 proves the tiling recurrence.

### B2 — ALG-04 vs COMB-03: PASS
If a recurrence is supplied and the work is sequence manipulation, ALG-04 owns it. COMB-03 owns deriving a relation from counted states. ALG-04 Sections 1/3/4/5 may be retrieved only after state/branch derivation. No AP/GP, telescoping or generic recurrence-solving lesson appears in COMB-03.

### B3 — COMB-03 deterministic evolution vs COMB-04 adversarial games: PASS
Multiple legal moves alone do not create a game. Q20 is deterministic reachability/shortest path and remains COMB-03. Once an opponent chooses moves to optimize an outcome, player-to-move strategy belongs to COMB-04.

### B4 — NT-05 arithmetic digit restrictions vs counting/state representation: PASS
NT-05 derives place-value/divisibility/digit arithmetic rules. COMB-01 counts admissible strings once such restrictions are known. COMB-03 may design a digit/carry state only when the arithmetic transition condition is supplied; Q26 is owned here because bounded carry/state evolution is decisive, not because COMB-03 teaches digit arithmetic.

### B5 — ordered/unordered identity: PASS
C01-5 remains the semantic source. COMB-03 applies it when deciding whether histories, paths, states or partition parts are distinct; no `nPr`/`nCr` doctrine is imported.

### B6 — overlapping branches fail closed: PASS
C01-2/C01-8 prohibit naive addition. A proposed recurrence with overlap is rejected or redesigned into disjoint states. Generic inclusion-exclusion is never invented inside COMB-03.

### B7 — state-memory sufficiency: PASS
Every proposed state must survive the falsifier: two histories with the same proposed state may not have different future legal choices/counts. Previous tile type, boundary occupancy, carry, special-resource flag or residual data are retained exactly when required.

### B8 — recurrence vs better representation: PASS
COMB-03 does not force recurrence merely because of topic title. Q14 and Q21 demonstrate sparse/residual/partition representations where recurrence is not the cheapest endpoint.

## Duplication bans

COMB-03 learner material must not contain standalone teaching of:
- `nPr`/`nCr`, factorial formulas or repeated-object formulas;
- generic complement/inclusion-exclusion;
- AP/GP, telescoping or generic supplied-recurrence solution methods;
- decimal/divisibility/digit-arithmetic derivations;
- adversarial game strategy.

Short retrieval is allowed only when immediately used for a state/transition decision.

## Historical-anchor disposition

| Anchor | Primary COMB-03 role | Boundary protected |
|---|---|---|
| IOQM-2023-Q08 | first-step tiling decomposition | counting addition/exhaustiveness retrieved from COMB-01 |
| IOQM-2024-Q20 | deterministic reverse-state search | no adversarial game |
| IOQM-2024-Q14 | sparse/deficit representation | recurrence not forced |
| IOQM-2023-Q21 | residual/partition representation | identity/order semantics retrieved from COMB-01 |
| IOQM-2023-Q26 | carry-state DP | arithmetic rule not retaught; state sufficiency owned here |

## Student-export scrub

Do not expose owner codes, issue/PR/branch references, provider IDs, acceptance-test codes, wave states or QA status strings in learner artifacts.

## Gate

`OVERLAP_AND_OWNERSHIP_CURRENT_CORPUS_PASS`

No overlap blocker remains for integrated COMB-03 authoring.