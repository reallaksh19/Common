# IOQM-G9-COMB-04 — W1-D Winning / Losing States Interface

```yaml
main_topic_id: IOQM-G9-COMB-04
microstream_id: W1-D
microstream_title: winning and losing states
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-04
prerequisite_interfaces:
  - COMB-03 stable state/recurrence interface @ f50a3b53dcf2f07ec80d4adcc94511cc3d4a99f1
source_cutoff: 2026-09-02
```

## A. Scope boundary

Included: player-to-move semantics, terminal outcomes, W/L recursive classification, strategy extraction from a W->L witness, proof of L closure, and finite impartial game graphs at Grade-9 depth.

Excluded: deterministic state traversal without an optimizing opponent (COMB-03), invariant-only reachability (W1-A/W1-B), generic game theory terminology beyond what the learner needs, and probabilistic games.

COMB-04 canon begins when another player controls legal moves with an opposing objective.

## B. Learner-state model

```text
PRIOR_KNOWLEDGE: turn-taking games; legal moves; finite case checking.
LIKELY_HALF_KNOWLEDGE: learner finds a good-looking move or successful line and calls it a winning strategy.
MISSING_BRIDGES: define the full state including player-to-move; classify terminals; prove both W and L directions; extract a strategy that survives every reply.
OWNERSHIP_TARGET: replace forward wishful play by rigorous W/L recursion.
```

## C. Mathematical invariant / governing structure

For a finite normal-form position graph with outcome convention fixed by the problem:

- an `L` position is one from which **every** legal move goes to a `W` position;
- a `W` position is one with **at least one** legal move to an `L` position.

Terminal positions are seeded from the actual win/loss rule; they are not assumed losing if the problem has a special “last red wins”, misère, or other terminal convention.

Proof contract for a claimed classification:

1. state the terminal outcome exactly;
2. define the state variables and whose turn is implicit/explicit;
3. prove every claimed `W` state has a legal move to `L`;
4. prove every legal move from every claimed `L` state lands in `W`;
5. give the strategy rule as “move to the certified L class”, not as one sample play.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| state tuple | all future-relevant data | apply COMB-03 sufficiency test, then add turn semantics | histories with same state have same legal future | retain irrelevant history |
| W/L table | recursive status | seed terminal rows and work backward | finite/bounded state set | simulate one line |
| directed game graph | options under opponent choice | mark terminals, then retrograde | legal moves known exactly | treat every branch as controllable |
| residue/invariant class + W/L | compressed strategic classification | test whether classes have uniform successors | move effects respect class partition | assume invariant alone decides winner |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| one successful path | reachability | forceability/WL | can the opponent choose a different reply? | a successful line looks strategic |
| branching state graph | COMB-03 | COMB-04 | is branch choice adversarial? | both have multiple successors |
| invariant class | W1-A/B | W1-D | does preservation alone decide outcome, or do option directions matter? | compact classes can resemble W/L classes |
| terminal process | monovariant | W/L | is the claim “must end” or “who wins”? | finiteness enables but does not equal strategy |
| W proof | existential | L proof | do we need one good move or all replies? | quantifiers are easy to swap |

## F. Misconception/diagnosis catalogue

```text
ERROR_CODE: PATH_IS_NOT_STRATEGY
WRONG_MOVE: give one line ending in a win.
WHY_TEMPTING: forward play produces persuasive examples.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: classify the opponent positions reached after the proposed move and prove all replies preserve the winning plan.
FALSIFIER_OR_CONTRAST: one alternate legal opponent reply that escapes the line.
```

```text
ERROR_CODE: WL_ONE_DIRECTION
WRONG_MOVE: show W states can move to L but never prove L states have no move to L.
WHY_TEMPTING: witness moves are easier than universal checks.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: explicitly prove both quantifiers: W has at least one L-successor; L has only W-successors.
FALSIFIER_OR_CONTRAST: locate an L-labeled state with an L-successor.
```

```text
ERROR_CODE: WRONG_TERMINAL_SEED
WRONG_MOVE: automatically label “no moves” or “last move” by normal-play convention.
WHY_TEMPTING: familiar games share a default rule.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: read the exact terminal outcome before recursion.
FALSIFIER_OR_CONTRAST: a misère or colour-specific final move reverses the seed.
```

## G. First-move cues

- “players alternate / optimal play / can force” -> define player-to-move state and terminal outcome.
- “last red wins” or another special ending -> seed terminals from that rule before pattern hunting.
- “find all winning starts” -> build small W/L states backward, then conjecture a class rule.
- “there exists a winning move” -> identify the target L class and prove it really is L.

Minimum first line: `Define the complete position state and label the terminal positions from the stated win condition.`

## H. H3 -> H0 fading plan

- H3: supply a small successor table and ask for W/L labels with both-direction proof.
- H2: give terminal seeds but require the learner to build the table.
- H1: cue “work backward from terminal positions”.
- H0: changed move set / terminal rule with no W/L label or hint.

## I. Validated IOQM source anchors

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q22 | 2025/Q22 | CLEAN_OFFICIAL | primary | impartial/adversarial marble game; winning states; backward classification | no | FINAL_OFFICIAL; independently verified 66 |
| IOQM-2023-Q28 | 2023/Q28 | CLEAN_VALIDATED | contrast | reachability without an optimizing opponent | source-controlled if reproduced | validated embedded key; verified 67 |

## J. Source-independent mathematical trace

**IOQM-2025-Q22.** The frozen ledger identifies the state by blue/red marble counts and the special “last red wins” terminal rule. Repository verification Batch C independently performs exact recursive game-state evaluation on `(blue,red)` using the paper’s legal-move relation and counts `66` winning starting states among the `121` pairs `1<=m,n<=11`.

The pedagogical trace is:

1. preserve the special terminal convention;
2. evaluate small positions backward rather than by one forward line;
3. separate the existential W step from the universal L step;
4. count only after the classification is certified.

No additional move rule is invented in this interface; the historical stem remains the authority.

## K. Contrast-pair candidates

1. successful path vs forced strategy;
2. W witness move vs L all-moves closure;
3. normal-play terminal seed vs special terminal convention;
4. deterministic branching vs adversarial branching;
5. reachability invariant vs strategic W/L class;
6. termination proof vs winner classification.

## L. Transfer candidates

- T2 move-set change: alter legal removals while retaining the same state tuple.
- T2 terminal change: normal vs special last-object rule.
- T3 representation: compress a W/L table into parity/residue classes only after successor-uniformity is proved.
- T4 cross-stream: use a monovariant to prove finite play, then retrograde classify W/L.

## M. Candidate mastery items

- Recognition-only: decide whether a stated solution proves reachability or forceability.
- First-line-only: define a sufficient game state and terminal labels.
- Full solve: certify a proposed W/L partition with both quantifier directions.
- WHY-NOT: refute “I found a winning line, so the start is winning.”
- Verification: find a mislabeled L state by checking all successors.

No new numerical historical answer is introduced beyond the verified Q22 count.

## N. Dependency declarations

`REQUIRES`: finite-state reasoning; explicit legal move relation.  
`BRIDGE_REQUIRES`: COMB-03 state sufficiency and graph vocabulary only; W/L semantics remain COMB-04.  
`APPLIES`: parity/residue/monovariant compression only after strategic validity is shown.  
Downstream may assume: terminal-first retrograde rule and the two-direction W/L proof contract.

## O. Lead integration notes

Use this stream as the decisive boundary from deterministic COMB-03 work. Teach the quantifiers visually and verbally: `W = exists move to L`; `L = all moves to W`. Keep Q22’s exact stem/source in teacher/source material rather than paraphrasing missing move details. Pair closely with W1-E reverse strategic reasoning.

## P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS (repository independent oracle: IOQM-2025-Q22=66)
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: historical stem controls exact legal move relation; classroom/retention/psychometric/publication evidence NOT_RUN
```
