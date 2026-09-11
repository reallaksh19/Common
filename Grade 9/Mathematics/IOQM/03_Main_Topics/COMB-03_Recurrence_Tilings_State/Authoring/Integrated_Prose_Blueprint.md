# COMB-03 — Integrated Prose Blueprint

Status: `PROVIDER_BOUND__WAVE0_ARCHITECTURE_FROZEN`

Provider locators:
- COMB-01 `COMB01_Stable_Counting_Model_Interface_v1.md`: retrieve C01-1/C01-7 for object/state identity, C01-2/C01-4 for disjoint/exhaustive branches, C01-5 for ordered/unordered identity, C01-8 for overlap fail-closed.
- ALG-04 `ALG04_Recurrence_Interface_v1.md`: retrieve Sections 1, 3, 4 and 5 for notation, explicit/recursive distinction, initialization and verification after derivation.

## One canonical teaching path

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

The learner experiences one idea becoming more powerful:

`DEFINE THE OBJECT -> DEFINE THE STATE -> SPLIT BY FIRST/LAST MOVE -> VERIFY EXACTLY-ONCE COVERAGE -> WRITE/USE THE RECURRENCE OR CHOOSE A BETTER REPRESENTATION`

## Core router

`WHAT IS BEING COUNTED / REACHED?`
`-> WHAT IS THE MINIMAL SUFFICIENT STATE?`
`-> DOES EVERY VALID OBJECT/PATH ENTER EXACTLY ONE FIRST/LAST TRANSITION?`
`-> WHAT SMALLER STATE REMAINS?`
`-> WHAT DOES EACH BASE STATE MEAN?`
`-> SHOULD WE COMPUTE FORWARD, SEARCH BACKWARD, OR AVOID RECURRENCE?`
`-> VERIFY`.

## Section architecture

### 1. RECONNECT — supplied recurrence is not the same as derived recurrence
Retrieve only ALG-04 recurrence notation, initialization and explicit-vs-recursive language. New COMB-03 contrast: a supplied recurrence may be manipulated; a counting recurrence must first be proved from the counted structure. No AP/GP or generic recurrence lesson.

### 2. DISCOVER — define the state before the equation
Use two histories of the same visible size whose legal futures differ unless one extra memory bit is retained. Learner discovery: **a recurrence is only as correct as its state definition.**

### 3. MAKE SENSE — first-step decomposition
Retrieve from COMB-01 only:
- C01-1: define one counted object and identity;
- C01-2: add only disjoint cases;
- C01-4: ask `Does every valid object enter exactly one branch?`;
- C01-7: use `state memory / remembered condition` for future-relevant restrictions.

COMB-03 then owns the new work: choose the structural first/last event, map each branch to a smaller canonical state, prove exactly-once coverage, and derive the recurrence.

### 4. TRY — one-state recurrence
First attempt is unsupported. Learner must supply state meaning, base-state meaning, branches, recurrence and a small-case verification. Optional support is revealed only after attempt.

### 5. DIAGNOSE — why a plausible recurrence can be wrong
Include overlapping branches, omitted branch, insufficient state, oversized state, wrong base state, ordered/unordered mismatch, counting paths when states are requested, and deterministic process confused with an adversarial game. Ordered/unordered and overlap language is retrieval from C01-5/C01-8, not a local counting chapter.

### 6. MAKE SENSE II — hidden memory / multi-state recurrence
Use the sufficiency falsifier: `Can two histories with this same proposed state have different futures?` If yes, enrich the state minimally.

### 7. TRY II — carry/state table
Use a checked author-created case before the historical carry anchor. The arithmetic constraint is supplied; COMB-03 owns the local state/transition design, while arithmetic digit-rule derivation remains NT-05.

### 8. DISCOVER II — recurrence is not always the best endpoint
Contrast a genuine recursive decomposition with a residual/near-extremal problem where a compressed representation beats recurrence. Canonical lesson: **STATE-FIRST, NOT RECURRENCE-ALWAYS.**

### 9. MAKE SENSE III — forward vs reverse-state search
Use a deterministic operation graph. Compare successor and predecessor descriptions; choose the direction with lower branching while preserving reachability/shortest-path correctness. If an opponent controls moves for a strategic objective, route to COMB-04 instead.

### 10. ADOPT — unlabelled mixed decisions
Mix one-state recurrence, finite-memory recurrence, reverse search, residual/partition representation, carry state and WHY-NOT-recurrence items with no method labels.

### 11. FADE
Support is distributed across separate items rather than exposed as internal codes to learners: state+branches supplied -> state only -> recognition cue -> no support. The first mastery attempt is always unhinted.

### 12. TRANSFER
Use genuine changed surfaces: tiling -> strings/steps/path blocks; operation process -> state graph; binary carry -> another local-balance state; residual partition -> constrained resource distribution.

## First-Step Reference blueprint

1. What is the object/target?
2. What must the state remember?
3. Does every valid object enter exactly one branch?
4. What smaller state remains?
5. What do the base states mean?
6. Does one scalar state suffice?
7. Forward, reverse, recurrence, or no recurrence?
8. Verify small cases.

## Mastery blueprint

Include recognition-only state choice, first-line state definition, complete recurrence derivation, recurrence verification, hidden-memory diagnosis, forward-vs-reverse choice, direct/residual representation where recurrence is inferior, deterministic-vs-game boundary, changed-surface transfer and WHY-NOT explanations.

## Historical-anchor role

- 2023-Q08: tiling/first-step recurrence;
- 2024-Q20: reverse-state search;
- 2024-Q14: sparse near-boundary representation;
- 2023-Q21: residual/partition representation;
- 2023-Q26: carry-state counting.

Exact historical wording remains source-controlled. Historical anchors are high-ceiling evidence, not the only teaching examples.

## Promotion decision

Provider placeholders are fully resolved. C01-1..C01-10 and T1..T6 pass; ALG-04 boundary and overlap ledger pass.

`WAVE0_ARCHITECTURE_FROZEN__INTEGRATED_AUTHORING_ALLOWED`