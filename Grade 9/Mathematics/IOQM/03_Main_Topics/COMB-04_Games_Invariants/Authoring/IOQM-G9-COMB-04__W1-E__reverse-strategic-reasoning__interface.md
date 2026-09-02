# IOQM-G9-COMB-04 — W1-E Reverse Strategic Reasoning Interface

```yaml
main_topic_id: IOQM-G9-COMB-04
microstream_id: W1-E
microstream_title: reverse strategic reasoning
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-04
prerequisite_interfaces:
  - COMB-03 stable state/recurrence interface @ f50a3b53dcf2f07ec80d4adcc94511cc3d4a99f1
  - IOQM-G9-COMB-04 W1-D winning/losing states
source_cutoff: 2026-09-02
```

## A. Scope boundary

Included: retrograde reasoning from terminal states, predecessor analysis under adversarial choice, strategy extraction by maintaining the opponent in certified losing classes, and pattern induction after a finite backward table is established.

Excluded: generic deterministic predecessor search as a standalone technique (COMB-03), source-free claims that reverse search always beats forward search, and invariant-only reachability where no opponent chooses moves.

The COMB-03 interface supplies direction-choice/state-graph discipline; COMB-04 owns the strategic quantifiers attached to predecessors and successors.

## B. Learner-state model

```text
PRIOR_KNOWLEDGE: can enumerate legal next moves from a state.
LIKELY_HALF_KNOWLEDGE: learner explores the opening tree forward and loses track of opponent alternatives.
MISSING_BRIDGES: begin from known terminal outcomes; reason by predecessor classes; convert a recurring backward pattern into a proof.
OWNERSHIP_TARGET: ask “what positions can move into this losing class?” before expanding the whole forward tree.
```

## C. Mathematical invariant / governing structure

Retrograde game analysis is an alternating predecessor rule:

- once `L` states are known, every predecessor with **some** move into `L` is `W`;
- once all successors of a state are known `W`, that state is `L`.

In a finite acyclic or terminating game graph, repeated application of these rules classifies all states. The strategic content is asymmetric: W classification is existential; L classification is universal.

A discovered arithmetic pattern in backward labels becomes a theorem only after successor behavior is proved for the entire claimed class.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| terminal frontier | known outcomes | mark exact terminal states | terminal rule unambiguous | assume standard normal play |
| predecessor layers | retrograde propagation | list states that can reach known L | predecessor rule exact | use COMB-03 deterministic semantics without opponent quantifiers |
| W/L residue table | periodic strategic pattern | classify small states first | successor classes repeat | guess period from too few cases |
| strategy invariant | “return opponent to L” rule | identify target L class | every opponent reply from L exits to W | state one sample response |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| forward simulation | reverse W/L | forward tree | are terminal classes simpler than opening branches? | play starts at the opening |
| reverse deterministic search | COMB-03 | W1-E | do predecessor labels depend on adversarial quantifiers? | both traverse reversed edges |
| observed periodic W/L pattern | theorem | heuristic | have all move classes been proved to map correctly? | small tables look convincing |
| invariant maintenance | W1-E strategy | W1-A/B obstruction | does the player actively choose moves to restore a class? | both use a preserved-looking pattern |

## F. Misconception/diagnosis catalogue

```text
ERROR_CODE: RETROGRADE_WITHOUT_TERMINALS
WRONG_MOVE: label states backward before establishing terminal outcomes.
WHY_TEMPTING: familiar subtraction games suggest remembered patterns.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: write the exact terminal rule first.
FALSIFIER_OR_CONTRAST: change normal play to a special last-move rule; all seeds may change.
```

```text
ERROR_CODE: PATTERN_FROM_SMALL_TABLE
WRONG_MOVE: extrapolate a residue pattern from a few W/L rows.
WHY_TEMPTING: periodicity is visually strong.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: prove W->L existence and L->W closure for every residue/state class.
FALSIFIER_OR_CONTRAST: test the first state beyond the observed table where a new move becomes legal.
```

```text
ERROR_CODE: PREDECESSOR_QUANTIFIER_SWAP
WRONG_MOVE: call a predecessor winning because all moves go to L, or losing because one move goes to W.
WHY_TEMPTING: reverse edges obscure who chooses.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: keep `W: exists L-successor`, `L: all W-successors` visible during reverse propagation.
FALSIFIER_OR_CONTRAST: a state with one L and one W successor is W, not L.
```

## G. First-move cues

- “optimal play / winning starts” -> write terminal states and work backward one layer.
- “huge forward case tree” -> search for a repeating predecessor class.
- “winning response after any opponent move” -> try to maintain/restore a certified L class for the opponent.
- “reverse-state” -> first ask whether the task is strategic COMB-04 or deterministic COMB-03.

Minimum first line: `Seed the exact terminal W/L states, then classify their predecessors using the correct existential/universal rule.`

## H. H3 -> H0 fading plan

- H3: terminal states and predecessor graph supplied; learner propagates labels.
- H2: only terminal states supplied; learner generates predecessors.
- H1: cue “work backward from the ending”.
- H0: changed terminal/move rules with no reverse hint.

## I. Validated IOQM source anchors

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q22 | 2025/Q22 | CLEAN_OFFICIAL | primary | backward winning/losing classification on marble-count state | no | FINAL_OFFICIAL; independently verified 66 |
| IOQM-2023-Q28 | 2023/Q28 | CLEAN_VALIDATED | contrast | reverse construction/reachability but no adversarial opponent | source-controlled if used | verified 67 |

## J. Source-independent mathematical trace

For Q22, the frozen independent verification evaluates the finite `(blue,red)` state grid recursively under the historical legal moves and special terminal rule and obtains 66 winning starts among 121 states. This is precisely the kind of task where reverse classification prevents the learner from mistaking one favorable forward branch for a forced strategy.

Generic retrograde theorem: in a finite acyclic game graph with correctly seeded terminal labels, repeatedly labeling any state W if it has an L-successor and labeling a state L once all successors are W yields the unique W/L classification. Induction on maximum remaining path length proves correctness.

## K. Contrast-pair candidates

1. opening-tree expansion vs terminal-first retrograde;
2. deterministic reverse BFS vs adversarial retrograde labels;
3. guessed period vs proved successor-class period;
4. W predecessor existential rule vs L universal rule;
5. maintaining a losing class for opponent vs passive invariant obstruction;
6. reverse construction of a reachable path vs reverse proof of a forced strategy.

## L. Transfer candidates

- T2 move-set change in a subtraction/removal game.
- T2 terminal-rule change to expose seed sensitivity.
- T3 two-coordinate state table compressed to residue classes after proof.
- T4 combine a monovariant ensuring acyclicity with reverse W/L classification.

## M. Candidate mastery items

- Recognition-only: choose forward simulation or retrograde analysis and justify.
- First-line-only: write terminal labels and the first predecessor layer.
- Full solve: prove a periodic W/L class by both successor directions.
- WHY-NOT: refute a pattern inferred only from the first five states.
- Verification: audit a retrograde table for a quantifier swap.

No new numerical historical answer is introduced beyond Q22=66.

## N. Dependency declarations

`REQUIRES`: W1-D W/L semantics; finite-state reasoning.  
`BRIDGE_REQUIRES`: COMB-03 predecessor/direction language, without importing deterministic ownership.  
`APPLIES`: parity/residue classes if successor behavior respects them.  
Downstream may assume: terminal-first retrograde algorithm and proof-by-successor-class induction.

## O. Lead integration notes

Place immediately after W1-D. Make the COMB-03 contrast explicit: reverse traversal is shared vocabulary, but adversarial predecessor labeling belongs here. Use small tables only as conjecture generators; require a class proof before compressing to a strategy card.

## P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS (repository independent oracle: IOQM-2025-Q22=66)
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact historical legal moves remain source-controlled; classroom/retention/psychometric/publication evidence NOT_RUN
```
