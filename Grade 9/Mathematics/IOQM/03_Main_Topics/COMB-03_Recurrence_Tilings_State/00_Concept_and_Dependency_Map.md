# IOQM Grade 9 — COMB-03 Recurrence, Tilings & State Evolution

Status: `WAVE0_ARCHITECTURE_FROZEN`

Accepted providers at freeze:
- COMB-01: `Grade 9/Mathematics/IOQM/03_Main_Topics/COMB-01_Basic_Counting_Restrictions_Inclusion_Exclusion/Authoring/COMB01_Stable_Counting_Model_Interface_v1.md`, blob `c4d80bfeed3bca5d2b9cc3bd02b1a92fa7b66152`;
- ALG-04: `Grade 9/Mathematics/IOQM/03_Main_Topics/ALG-04_Sequences_Recurrences/Authoring/ALG04_Recurrence_Interface_v1.md`, blob `12891c65de0e1c26b6fef6623d54246a3d9dfd56`.

Wave-0 acceptance evidence lives in `Authoring/COMB01_Interface_Acceptance_Contract.md`, `Authoring/Wave0_Promotion_Checklist.md` and `Authoring/Overlap_and_Ownership_Ledger.md`.

## Learner entry model

Assume the learner can read a sequence recurrence after ALG-04 and may know routine counting formulas, but does not yet reliably:
- define the smallest useful counting state;
- partition a count by a first/last move;
- distinguish a recurrence **derived from combinatorial structure** from an algebraic recurrence already supplied;
- distinguish deterministic state evolution from adversarial play;
- choose reverse search when forward branching explodes;
- encode representation constraints with a small carry/state description.

## Canonical governing rule

> **DEFINE THE STATE BEFORE WRITING THE RECURRENCE.**

Operational router:

```text
WHAT IS BEING COUNTED OR REACHED?
-> DEFINE THE MINIMAL SUFFICIENT STATE
-> PARTITION BY FIRST/LAST TRANSITION
-> DOES EVERY VALID OBJECT ENTER EXACTLY ONE BRANCH?
-> MAP EACH BRANCH TO SMALLER STATE(S)
-> GIVE BASE-STATE MEANING AND INITIAL VALUES
-> VERIFY SMALL CASES
-> CHOOSE FORWARD / REVERSE / RECURRENCE / BETTER REPRESENTATION
-> COMPUTE
```

## Dependency map

```text
G9 arithmetic + proof/model habits
        |
        +--> COMB-01 stable counting/model interface [REQUIRES, ACCEPTED]
        |       retrieve C01-1 counted-object identity
        |       retrieve C01-2/C01-4 disjoint + exhaustive cases
        |       retrieve C01-3 stage multiplication
        |       retrieve C01-5 identity/order decision
        |       retrieve C01-6 direct/complement cue
        |       retrieve C01-7 restriction/state-memory vocabulary
        |       retrieve C01-8 overlap fail-closed boundary
        |       retrieve C01-9 repeated-object identity
        |       retrieve C01-10 digit-string ownership boundary
        |
        +--> ALG-04 stable recurrence interface [BRIDGE_REQUIRES, ACCEPTED]
                retrieve indexed notation and valid index range
                retrieve initialization form
                retrieve explicit vs recursive distinction
                retrieve algebraic verification only after derivation

COMB-03 owns after retrieval:
        counted state definition
        -> base-state meaning
        -> disjoint/exhaustive transition decomposition
        -> recurrence from counting structure
        -> minimal/finite-memory state design
        -> deterministic state evolution and reverse search
        -> carry/state representation
        -> choice not to use recurrence when a smaller representation wins
```

## Provider boundary in learner prose

COMB-03 may retrieve, without reteaching:
- from COMB-01: “these branches are disjoint, so add”; the exact-one-branch question; object identity; restriction/state-memory language;
- from ALG-04: indexed recurrence notation, initialization, explicit-vs-recursive language, and algebraic verification after a recurrence is structurally justified.

COMB-03 must itself prove:
1. exactly what object/state is counted;
2. what each base state means;
3. why transition branches are disjoint and exhaustive;
4. why each branch maps to the claimed smaller state;
5. therefore why the recurrence follows.

No AP/GP, telescoping, generic sequence algebra, generic P&C/IE or repeated-object formula teaching belongs here.

## Canonical ownership

COMB-03 owns:
- minimal sufficient state and the sufficiency falsifier;
- first/last-step decomposition;
- counting recurrence derived from structure;
- multi-state / finite-memory recurrence;
- tiling/path state recurrences;
- deterministic transition graphs;
- forward vs reverse-state search;
- carry-state counting;
- representation choice where recurrence is inferior.

COMB-01 owns basic counting/model semantics, ordered/unordered identity, complement/IE and repeated-object doctrine.
ALG-04 owns generic recurrence notation/semantics, AP/GP, sequence algebra, cancellation/telescoping and supplied-recurrence transformations.
COMB-04 owns adversarial strategy, player-to-move winning/losing states and game invariants.
NT-05 owns arithmetic digit/place-value/divisibility rules; COMB-03 may use a supplied arithmetic constraint inside a state transition.

## Representation inventory

| Representation | What it exposes | First move | Boundary |
|---|---|---|---|
| board/tiling picture | legal first placements | freeze the leftmost unresolved region | do not list whole tilings first |
| state-count table `T_n` | recurrence candidates | define exactly what `T_n` counts | symbol without state definition is invalid |
| tuple/flag state | hidden future-relevant memory | try to merge histories; seek a falsifier | retain only coordinates that change legal futures |
| directed state graph | legal transitions/reachability | write state + transition rule | deterministic graph is not automatically a game |
| reverse graph/search | shrinking predecessor set | invert legal moves | inverse/predecessor rule must preserve legality |
| digit/carry state | local representation constraints | process one digit with incoming carry | arithmetic digit rule is supplied, not rederived here |
| partition/residual state | monotone or near-boundary structure | encode residual/deficit | do not force recurrence when this is smaller |

## Method-selection boundaries

1. **Direct enumeration vs recurrence** — can every valid object be assigned exactly once by a first/last structural choice to smaller same-type states?
2. **Algebraic recurrence vs counting recurrence** — is the recurrence supplied, or must it be proved from what is counted?
3. **Forward vs reverse search** — which direction has fewer legal predecessor/successor branches?
4. **Deterministic evolution vs adversarial game** — is an opponent choosing moves to optimize an outcome? If yes, route game doctrine to COMB-04.
5. **One-state vs hidden-memory recurrence** — can two histories with the same proposed state have different legal futures? If yes, enrich the state.
6. **State recurrence vs complement/IE** — is local future legality captured by a small state, or is the decisive structure a global forbidden-set count? Generic IE remains COMB-01.
7. **Carry-state counting vs digit arithmetic** — is the arithmetic property already known? If not, route its derivation to NT-05.
8. **Recurrence vs better representation** — does a residual, partition, symmetry or direct representation collapse the problem more cheaply?

## Mandatory contrast set

- supplied algebraic recurrence vs combinatorial recurrence derived;
- direct enumeration vs first-step recursive decomposition;
- deterministic state evolution vs adversarial game;
- forward branching vs reverse-state search;
- one-state recurrence vs hidden-memory/multi-state recurrence;
- recurrence with base-state meaning vs formula alone;
- overlapping branches vs disjoint/exhaustive decomposition;
- ordered object/path vs unordered state identity;
- carry/state representation vs arithmetic digit-rule derivation;
- recurrence vs a better non-recursive representation.

## Transfer map

```text
tiling -> leftmost placement -> smaller-board states
strings -> last-symbol memory -> finite-state recurrence
path count -> last-step partition -> predecessor states
deterministic machine -> transition graph -> reverse predecessor set
binary representation -> supplied digit constraint + carry state -> local transitions
monotone / near-boundary structure -> residual/partition representation -> no forced recurrence
```

## Major misconception traps

- `STATE_UNDEFINED`: recurrence symbol appears before state meaning.
- `CASES_OVERLAP`: branch counts are added although one object can enter two branches.
- `BRANCH_OMITTED`: decomposition is not exhaustive.
- `MISSING_INITIALIZATION`: recurrence written without base-state meaning or enough initial values.
- `ALGEBRA_BEFORE_MODEL`: recurrence manipulated before being proved from the count.
- `FORWARD_BRANCH_EXPLOSION`: forward simulation is used despite sparse predecessors.
- `GAME_CONFUSION`: deterministic evolution is treated as opponent strategy.
- `STATE_TOO_LARGE`: full history retained though futures are identical.
- `STATE_TOO_SMALL`: carry/flag/boundary information needed for future legality is omitted.
- `OWNERSHIP_DRIFT`: generic IE, repeated-object formulas, AP/GP or digit arithmetic is retaught locally.

## Historical anchors

Primary evidence remains:
- `IOQM-2024-Q14 = 80` — sparse/near-boundary state representation;
- `IOQM-2024-Q20 = 10` — deterministic reverse-state search;
- `IOQM-2023-Q08 = 59` — tiling/first-step decomposition;
- `IOQM-2023-Q21 = 15` — residual/partition representation;
- `IOQM-2023-Q26 = 19` — carry-state representation.

All five were independently checked in the frozen verification authority; no metadata-correction overlay event affects them.

## Wave-0 decision

C01-1..C01-10: PASS 10/10.
T1..T6: PASS 6/6.
ALG-04 retrieval/ownership boundary: PASS.
Current-corpus COMB-01/ALG-04/COMB-04/NT-05 overlap revalidation: PASS.

`WAVE0_ARCHITECTURE_FROZEN`

Integrated learner authoring may now proceed on this same PR/branch. Human classroom, retention, psychometric and publication gates remain separate and `NOT_RUN`.