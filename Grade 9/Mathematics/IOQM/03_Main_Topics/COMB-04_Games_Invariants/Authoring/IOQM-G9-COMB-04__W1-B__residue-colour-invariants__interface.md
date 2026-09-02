# IOQM-G9-COMB-04 — W1-B Residue / Colour Invariants Interface

```yaml
main_topic_id: IOQM-G9-COMB-04
microstream_id: W1-B
microstream_title: residue and colour invariants
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-04
prerequisite_interfaces:
  - NT-02 stable residue/cycle interface @ 2b5c4fb1b693e1f881068ec51104d36ca46846e7
  - NT-01 stable prerequisite interface @ 5212297212fb097cd508e9fc9d5848b271bc0ad1
source_cutoff: 2026-09-02
```

## A. Scope boundary

Included: residue signatures already supported by NT-02, periodic colourings that encode residue classes, colour-class counts/parities, local move vectors over small finite residues, and dual invariants used to obstruct or characterize reachability.

Excluded: teaching congruence notation, inverses, cancellation, CRT or power-cycle doctrine (NT-02); general graph colouring enumeration (COMB-02); adversarial W/L recursion (W1-D); deterministic state traversal (COMB-03).

COMB-04 owns choosing and applying a residue/colour signature as a game/reachability invariant.

## B. Learner-state model

```text
PRIOR_KNOWLEDGE: remainders, parity, simple board colouring.
LIKELY_HALF_KNOWLEDGE: learner can colour a board but may not know why a colouring is mathematically relevant.
MISSING_BRIDGES: turn a colouring into an algebraic signature; verify every legal move; distinguish obstruction from full reachability classification.
OWNERSHIP_TARGET: use periodic labels only when their move-effect equations simplify the state.
```

## C. Mathematical invariant / governing structure

Assign each elementary state component a label/weight in a small residue system. If state vector is `x` and legal moves add vectors `d_j`, seek a weight vector `c` such that `c·d_j=0` in the chosen modulus for every move. Then `I(x)=c·x` is invariant.

A colouring is therefore not decoration: it is a visual encoding of the coefficients of `c`. Periodic colour patterns arise when the local move equations force repeated weights.

For a reachability claim:

- mismatch of invariant signatures proves impossibility;
- match proves only compatibility unless the invariant family is proved complete or a legal construction is supplied.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| periodic board colouring | local move cancellation | derive labels from move equations | repeated geometry/locality | choose colours aesthetically |
| residue vector | compact signature | reduce only the state data relevant to moves | NT-02 legality already available | reteach modular rules |
| weighted colour sum | dual invariant | assign weights, then test each move | additive local move effect | count one colour only |
| move-incidence equations | all invariant constraints | solve `c·d_j=0` | finitely describable moves | guess a pattern without verification |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| parity colouring | W1-A | W1-B | does mod 2 alone separate targets? | simplest modulus is familiar |
| residue invariant | COMB-04 application | NT-02 teaching | is the arithmetic rule already a prerequisite? | notation can expand into a second chapter |
| board colouring | invariant | COMB-02 colouring count | are colours labels to preserve or assignments to count? | same visual surface |
| invariant match | compatibility | construction | is sufficiency independently established? | one invariant feels decisive |
| local flip | reachability | W/L game | is there an opponent optimizing moves? | both involve move sequences |

## F. Misconception/diagnosis catalogue

```text
ERROR_CODE: DECORATIVE_COLOURING
WRONG_MOVE: choose a colouring and report a pattern without deriving its move effect.
WHY_TEMPTING: olympiad diagrams reward visual experimentation.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: derive colour weights from the condition that every legal move has zero weighted change.
FALSIFIER_OR_CONTRAST: test one legal move crossing the proposed periodic boundary.
```

```text
ERROR_CODE: MODULAR_RETEACH
WRONG_MOVE: rebuild congruence operations inside COMB-04.
WHY_TEMPTING: residue notation appears in the proof.
MISSING_LINK_CLASS: PREREQUISITE
REPAIR_INVARIANT: retrieve NT-02 legality and spend local prose on state/move interpretation.
FALSIFIER_OR_CONTRAST: if the argument becomes a lesson on modular inverses or cycles, ownership has drifted.
```

```text
ERROR_CODE: COLOUR_SIGNATURE_SUFFICIENCY
WRONG_MOVE: target has same signature, therefore target is reachable.
WHY_TEMPTING: small examples may accidentally make the invariant complete.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: require construction or a proof that the invariant family spans all obstructions.
FALSIFIER_OR_CONTRAST: two disconnected components with identical signature.
```

## G. First-move cues

- “flip every vertex of a small local shape” -> write one move vector and seek weights that sum to zero.
- “triangular/periodic board” -> test a short repeating colour pattern induced by the move equations.
- “can all symbols be changed?” -> compare target and initial weighted signatures before simulating.
- “mod 3/mod 2 pattern” -> retrieve arithmetic from NT-02; do not re-derive the arithmetic canon.

Minimum first line: `Let the board labels be weights chosen so that the weighted change of every legal move is 0.`

## H. H3 -> H0 fading plan

- H3: provide a three-colour/weight pattern; verify it is invariant.
- H2: give the local move equations and ask for a periodic weighting.
- H1: cue “search for a periodic colour signature”.
- H0: changed board/local toggle system with no colour hint.

## I. Validated IOQM source anchors

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2023-Q28 | 2023/Q28 | CLEAN_VALIDATED | primary | triangular local flip; `F_2`; period-3 dual invariant | source-controlled if reproduced | embedded validated key; verified 67 |
| IOQM-2025-Q25 | 2025/Q25 | CLEAN_OFFICIAL | bridge | parity/exponent residue obstruction with construction | no | FINAL_OFFICIAL; verified 36 |

Corpus metadata records the 2023-Q28 historical item as validated. Issue #89 separately requires figure custody discipline: no redrawing/relabeling may be presented as the exact historical figure without source control.

## J. Source-independent mathematical trace

**IOQM-2023-Q28.** Model each coin state and each legal triangle flip over `F_2`. A dual invariant assigns vertex weights satisfying the unit-triangle equations; these constraints force a period-3 pattern. The desired global toggle is compatible exactly when `3` does not divide `n`. Hence among `1<=n<=100`, exactly `100-33=67` values satisfy the criterion. Repository Batch C independently verifies the result and identifies the period-3 invariant route.

The pedagogical extraction is not “memorize a three-colouring”; it is “derive weights from the move equations, observe periodicity, then compare initial and target signatures.”

## K. Contrast-pair candidates

1. aesthetic colouring vs algebraically derived colouring;
2. parity-only signature vs a richer period-3 signature;
3. residue invariant application vs NT-02 residue-rule teaching;
4. invariant obstruction vs constructive sufficiency;
5. local toggle reachability vs adversarial game forceability;
6. colour labels as weights vs COMB-02 proper-colouring assignments.

## L. Transfer candidates

- T2 representation: replace triangular coins by binary lamps on a repeating lattice.
- T2 context: colour-class token transfers with a fixed zero-sum move signature.
- T3 geometry: change the local move shape and derive the new weighting recurrence.
- T4 abstraction: pass from visual colours to a short system of linear equations over `F_2`/small residues.

## M. Candidate mastery items

- Recognition-only: choose whether a board colouring is likely to serve as an invariant or a counting device.
- First-line-only: write the local weight equation for one move shape.
- Full solve: derive a periodic weight pattern and use it to prove a target impossible.
- WHY-NOT: explain why a guessed repeating colouring is not evidence until every move is checked.
- Verification: test whether a proposed weighting is invariant for all orientations of a legal move.

No new historical numerical answer is introduced.

## N. Dependency declarations

`REQUIRES`: state/move definition; elementary finite residue arithmetic.  
`BRIDGE_REQUIRES`: NT-02 residue legality; NT-01 divisibility language where needed.  
`APPLIES`: residue/colour signatures as COMB-04 invariant tools.  
Downstream may assume: colourings must be derived/verified, and invariant compatibility requires separate sufficiency evidence.

## O. Lead integration notes

Teach after the generic invariant proof contract and parity stream. Use 2023-Q28 as the main historical model, with figure/source custody explicit. Compress modular syntax to retrieval. Keep the distinction from COMB-02 graph colouring visible. Place constructive sufficiency later with W1-F.

## P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS (repository independent oracle: 2023-Q28=67, Q25=36)
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: historical figure reproduction remains source-controlled; classroom/retention/psychometric/publication evidence NOT_RUN
```
