# COMB-04 <- COMB-03 Boundary Acceptance Contract

Provider: `IOQM-G9-COMB-03`  
Pinned stable-interface blob: `f50a3b53dcf2f07ec80d4adcc94511cc3d4a99f1`  
Provider status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`  
Acceptance: `PASS`

## Retrieved boundary tools

COMB-04 may retrieve:

- define the state before reasoning about transitions;
- minimal-state sufficiency falsifier: two histories assigned the same state must have the same relevant legal futures;
- forward/reverse directed-state viewpoint where useful.

## Hard ownership boundary

COMB-03 owns deterministic state evolution, counting recurrences, generic finite-memory state design, and deterministic predecessor search.

COMB-04 owns the additional adversarial layer: another player controls choices with an opposing strategic objective; states are classified by what the player to move can force.

The stable provider rule S03-8 is binding:

> Multiple legal moves do not create an adversarial game. Game doctrine begins when another player controls choices with an opposing strategic objective.

## Required student contrast

Every integrated COMB-04 journey must include a close pair where the surface has similar state transitions but:

- one problem is deterministic/reachability-only and routes to COMB-03;
- the other has an optimizing opponent and requires COMB-04 W/L or invariant strategy.

`GAME_BOUNDARY: PASS`  
`DETERMINISTIC_RETEACH: FORBIDDEN`  
`DOWNSTREAM_ACCEPTANCE: PASS`