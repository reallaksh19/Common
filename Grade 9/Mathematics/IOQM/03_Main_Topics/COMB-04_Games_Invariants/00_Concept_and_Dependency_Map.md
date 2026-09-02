# IOQM Grade 9 — COMB-04 Games & Invariants

Status: `WAVE0_ARCHITECTURE_FROZEN`

Issue: `#89`  
Main topic: `IOQM-G9-COMB-04`  
Production wave: `3`

## Accepted prerequisite / boundary providers

- NT-01 stable prerequisite interface: blob `5212297212fb097cd508e9fc9d5848b271bc0ad1`, status `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`.
- NT-02 stable residue/cycle interface: blob `2b5c4fb1b693e1f881068ec51104d36ca46846e7`, status `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`.
- COMB-03 stable state/recurrence interface: blob `f50a3b53dcf2f07ec80d4adcc94511cc3d4a99f1`, status `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`.

Acceptance evidence is recorded under `Authoring/`.

## Learner entry model

Assume a Grade-9 learner with roughly 50% prior knowledge. The learner may know parity, elementary divisibility, basic remainders, and informal game play, but does not yet reliably:

- identify a preserved quantity before simulating;
- distinguish invariant, monovariant, and winning/losing-state arguments;
- distinguish reachability from forceability against an opponent;
- prove both directions of a W/L classification;
- use reverse strategic reasoning rather than forward case explosion;
- separate existence constructions from impossibility obstructions;
- recognize when a deterministic state problem belongs to COMB-03 instead.

## Governing learner router

> **STATE -> MOVE EFFECT -> INVARIANT / MONOVARIANT / W-L CLASS -> PROOF -> STRATEGY OR OBSTRUCTION**

Operational questions:

1. What is the complete state, including whose turn it is when relevant?
2. What does one legal move change?
3. Is something preserved, monotone, or recursively classifiable as W/L?
4. Is the claim only about reachability, or must a player force an outcome?
5. What proof obligation remains: necessity, sufficiency, construction, or obstruction?

## Dependency map

```text
G9 arithmetic + F1 proof habits
        |
        +--> NT-01 [RETRIEVE]
        |       parity/divisibility language; difference/divisibility facts
        |
        +--> NT-02 [RETRIEVE]
        |       residue classes and legal modular operations
        |
        +--> COMB-03 [BOUNDARY / RETRIEVE]
                state sufficiency test; deterministic forward/reverse state search

COMB-04 owns after retrieval:
        adversarial state + player-to-move semantics
        -> parity/residue/colour invariants in game/reachability settings
        -> monovariants and termination/bound arguments
        -> winning/losing-state recursion
        -> reverse strategic reasoning
        -> construction for possibility / obstruction for impossibility
```

## Canonical ownership boundary

COMB-04 owns:

- adversarial games where another player controls legal choices with an opposing objective;
- invariant and monovariant design for game/reachability arguments;
- player-to-move winning/losing states and strategy extraction;
- reverse strategic reasoning from terminal states;
- construction versus obstruction proofs.

COMB-04 may retrieve but must not reteach:

- NT-01 divisibility/gcd/lcm canon;
- NT-02 congruence notation, cancellation legality, inverses, or power-cycle canon;
- COMB-03 deterministic state evolution, counting recurrences, and generic predecessor-search doctrine.

## Proof contracts

### Invariant claim

Every promoted invariant argument must explicitly state:

1. **what** is preserved;
2. **why every legal move** preserves it;
3. **how** the preserved value proves the requested conclusion.

A matching invariant is a necessary condition for reachability unless constructive sufficiency is separately proved.

### Monovariant claim

Every promoted monovariant argument must state:

1. the quantity/order that changes monotonically;
2. the direction and strictness of change;
3. a lower/upper bound or well-foundedness argument;
4. exactly what follows. Termination or a bound does not automatically identify a winner.

### Winning / losing classification

A claimed W/L partition requires both directions:

- every `W` position has at least one legal move to an `L` position;
- every legal move from an `L` position goes to a `W` position.

A single successful line of play proves neither forceability nor a winning strategy.

## Representation inventory

| Representation | What it exposes | First move | Boundary |
|---|---|---|---|
| state tuple + player to move | adversarial future choices | define terminal outcomes and legal moves | omit player only when game is impartial and turn is implicit |
| parity vector | mod-2 move effect | compute delta of one move | parity is not a universal sufficient invariant |
| residue/colour signature | conserved class under moves | label state/board by canonical residue classes | modular arithmetic remains NT-02 retrieval |
| monovariant value/order | progress / termination | prove strict monotonicity and bound | does not alone prove optimal play |
| W/L table or directed game graph | recursive strategic status | seed terminal states and work backward | deterministic graph without opponent is COMB-03 |
| construction certificate | reachability/existence | give a legal finite move sequence or recursive construction | invariant compatibility alone is not construction |
| obstruction certificate | impossibility | find a violated invariant/parity/residue condition | obstruction does not imply converse sufficiency |

## Method-selection boundaries

1. **Simulation vs invariant** — does every move have a common algebraic/parity effect that collapses the tree?
2. **Reachability vs forceability** — is there an opponent choosing moves? If yes, one path is insufficient.
3. **Invariant vs monovariant** — is the quantity exactly preserved or only one-way changing?
4. **Invariant vs W/L recursion** — does a preserved class decide the outcome, or must strategic move options be classified recursively?
5. **Forward vs reverse reasoning** — are terminal states easier to classify backward than the opening tree is to enumerate forward?
6. **Construction vs obstruction** — is the task to exhibit a legal realization or prove none can exist?
7. **COMB-03 vs COMB-04** — if no optimizing opponent controls choices, route generic deterministic state evolution to COMB-03.

## Mandatory contrast set

- adversarial game vs deterministic state evolution;
- reachability vs forceability;
- simulation vs invariant;
- invariant vs monovariant;
- necessary invariant condition vs constructive sufficiency;
- W-state witness move vs L-state all-moves proof;
- existence construction vs impossibility obstruction;
- forward game tree vs reverse W/L classification;
- parity invariant vs richer residue/colour invariant;
- mathematical state sufficiency vs retaining irrelevant history.

## Transfer map

```text
marble-removal game
-> terminal outcomes + W/L recursion
-> changed move-set impartial game

pairing / product-square construction
-> parity/exponent obstruction + inductive construction
-> changed pairing target / residue class

triangular flip system
-> move vectors over F2 + dual colour invariant
-> changed board / local toggle system

monotone token process
-> bounded monovariant
-> termination question vs winner question contrast
```

## Historical anchors

Repository verification authority records:

- `IOQM-2025-Q22 = 66` — exact recursive evaluation of `(blue,red)` game states; verification batch C: PASS.
- `IOQM-2025-Q25 = 36` — `n=1` obstruction; base constructions for `n=2,3`; extension `n -> n+2`; verification batch C: PASS.
- `IOQM-2023-Q28 = 67` — `F_2` flip model, period-3 dual invariant, target possible iff `3` does not divide `n`; verification batch C: PASS.

These answers are inherited from the independently recomputed 90-question verification authority, not newly claimed from unverified prose.

## Major misconception traps

- `PATH_IS_NOT_STRATEGY`: one successful path is presented as a forced win.
- `WL_ONE_DIRECTION`: only W->L witness or only L->W closure is proved.
- `INVARIANT_SUFFICIENCY_LEAP`: matching invariant values are treated as automatic reachability.
- `MONOVARIANT_WINNER_LEAP`: termination is treated as winner identification.
- `SIMULATION_EXPLOSION`: forward tree enumeration is used despite a short preserved structure.
- `PLAYER_OMITTED`: state definition forgets whose turn matters.
- `MODULAR_RETEACH`: NT-02 canon is rebuilt locally instead of retrieved.
- `DETERMINISTIC_GAME_CONFUSION`: COMB-03 state evolution is mislabeled adversarial.
- `FIGURE_CUSTODY_DRIFT`: historical figure is redrawn/relabelled as though exact without source control.

## Wave-0 decision

Provider identities: PASS.  
Canonical overlap ownership: PASS.  
Historical anchor IDs / verified answers: PASS_STATIC via frozen corpus verification.  
Dependency inversion: NONE.  
Learner router and method boundaries: FROZEN.

`WAVE0_ARCHITECTURE_FROZEN`

Wave 1 may materialize the seven A-P research interfaces. Integrated learner prose must not start until those interfaces are individually complete enough for lead consumption.

Human classroom timing/readability, retention, psychometrics, qualification probability, percentile/pass-mark calibration, and publication approval remain `NOT_RUN`.