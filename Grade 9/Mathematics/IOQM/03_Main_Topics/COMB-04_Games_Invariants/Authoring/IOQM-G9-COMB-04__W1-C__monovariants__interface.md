# IOQM-G9-COMB-04 — W1-C Monovariants Interface

```yaml
main_topic_id: IOQM-G9-COMB-04
microstream_id: W1-C
microstream_title: monovariants
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-04
prerequisite_interfaces:
  - NT-01 stable prerequisite interface @ 5212297212fb097cd508e9fc9d5848b271bc0ad1
source_cutoff: 2026-09-02
```

## A. Scope boundary

Included: strictly increasing/decreasing quantities, lexicographic or well-founded state measures, termination/bound arguments, and proof obligations for monotonicity plus boundedness.

Excluded: using a monovariant alone to identify a winner; generic optimization theory; deterministic recurrence counting (COMB-03); modular arithmetic teaching (NT-02).

COMB-04 owns monovariants when they explain why a legal game/process cannot cycle forever or when they bound the number/type of strategic moves.

## B. Learner-state model

```text
PRIOR_KNOWLEDGE: inequalities, integer bounds, finite processes.
LIKELY_HALF_KNOWLEDGE: learner notices that a quantity seems to go down, but does not check strictness or a lower bound.
MISSING_BRIDGES: distinguish invariant from monovariant; state exactly what termination/bound follows; separate termination from winner identity.
OWNERSHIP_TARGET: search for a bounded one-way measure when exact preservation is unavailable.
```

## C. Mathematical invariant / governing structure

A monovariant is a function `M(state)` taking values in a well-founded ordered set such that every legal move changes `M` strictly in one direction. If `M` is integer-valued, decreases by at least 1, and is bounded below by `L`, then any play starting at `M_0` has at most `M_0-L` moves.

Proof contract:

1. define `M`;
2. prove **every** legal move changes it in the asserted direction;
3. prove strictness where termination is claimed;
4. identify a lower/upper bound or other well-founded order;
5. state only the valid conclusion: termination, an upper bound, or exclusion of cycles. Winner identity requires separate game analysis unless terminal parity/outcome is also controlled.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| integer potential | quantitative progress | compute change under an arbitrary move | all moves change it one way | inspect only sample moves |
| lexicographic pair | progress when one scalar is insufficient | order two state features | primary coordinate never increases; tie-break decreases | use an unproved weighted sum |
| inversion/disorder count | local simplification | count bad pairs/defects | each move removes defects | assume visual simplification |
| finite rank/order | no cycles | identify strict descent in a finite order | state space finite/well-founded | infer winner from termination |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| exact preservation | invariant | monovariant | is the quantity unchanged or one-way changing? | both compress move sequences |
| termination | monovariant | W/L | is the question only whether play ends, or who can force the outcome? | finite game often suggests winner |
| decreasing count | direct bound | strategic recursion | does every move reduce the same measure regardless of player choice? | opponent choices look central even when bound is choice-independent |
| deterministic process | COMB-03 | COMB-04 | is there an opposing player with an objective? | move sequences can look game-like |

## F. Misconception/diagnosis catalogue

```text
ERROR_CODE: NONSTRICT_MONOVARIANT
WRONG_MOVE: claim termination from a quantity that may stay unchanged.
WHY_TEMPTING: nonincrease feels like progress.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: prove strict descent on every move or refine the measure lexicographically.
FALSIFIER_OR_CONTRAST: exhibit a legal zero-change cycle.
```

```text
ERROR_CODE: UNBOUNDED_DESCENT
WRONG_MOVE: claim termination from strict decrease without a lower bound.
WHY_TEMPTING: finite-looking examples hide an infinite state domain.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: state the range/bound explicitly.
FALSIFIER_OR_CONTRAST: integer-valued descent with no lower bound can continue indefinitely.
```

```text
ERROR_CODE: MONOVARIANT_WINNER_LEAP
WRONG_MOVE: conclude a named player wins because all games terminate.
WHY_TEMPTING: termination makes backward induction possible, but does not itself perform it.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: after proving finiteness, apply W/L classification if winner identity is required.
FALSIFIER_OR_CONTRAST: two terminating games with the same move-count bound can have opposite winners.
```

## G. First-move cues

- “process cannot continue forever” -> seek an integer measure with strict bounded descent.
- “each move simplifies/reduces disorder” -> quantify the alleged simplification.
- “no invariant seems preserved” -> test a monovariant before simulating.
- “maximum number of moves” -> bound total descent divided by minimum per-move change.

Minimum first line: `Define M(state)=... and compute M(after)-M(before) for an arbitrary legal move.`

## H. H3 -> H0 fading plan

- H3: provide the potential and ask for monotonicity + bound proof.
- H2: name the two state features that should form a lexicographic measure.
- H1: cue “look for strict bounded progress”.
- H0: changed-surface finite process with no invariant/monovariant label.

## I. Validated IOQM source anchors

No seed-corpus item is promoted as a canonical monovariant anchor in the frozen COMB-04 issue. The three mandatory historical anchors serve parity/residue, W/L, and construction/obstruction. This stream therefore uses author-created structural examples only and does not manufacture historical weightage.

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| NONE | — | — | no direct promoted PYQ | monovariant transfer stream | — | — |

## J. Source-independent mathematical trace

Generic checked lemma: if `M` is integer-valued, `M>=L` on all legal states, and every legal move satisfies `M(next)<=M(current)-1`, then no play from state `s` has more than `M(s)-L` moves. Proof: after `t` moves, `M_t<=M_0-t`; since `M_t>=L`, one has `t<=M_0-L`.

Lexicographic checked lemma: if `(A,B)` lies in a finite subset of nonnegative integer pairs and each move either lowers `A`, or leaves `A` fixed and lowers `B`, then cycles are impossible.

Neither lemma determines the winner without an additional terminal-outcome/WL argument.

## K. Contrast-pair candidates

1. invariant unchanged vs monovariant strictly decreasing;
2. nonincrease vs strict decrease;
3. strict decrease with bound vs strict decrease without bound;
4. termination proof vs winner proof;
5. scalar potential vs lexicographic potential;
6. adversarial finite game vs deterministic finite process.

## L. Transfer candidates

- T2 context: token-removal process where total weight drops each move.
- T2 representation: inversion count for a local swap process.
- T3 structure: replace scalar by a lexicographic pair when one move can keep the primary measure fixed.
- T4 strategy bridge: use a monovariant only to prove the game graph is acyclic, then hand off to W/L retrograde analysis.

## M. Candidate mastery items

- Recognition-only: decide whether a proposed quantity is invariant, monovariant, or neither.
- First-line-only: define a potential for a process where every move removes a defect.
- Full solve: prove termination and an explicit move bound from a decreasing integer potential.
- WHY-NOT: explain why a merely nonincreasing potential does not rule out cycles.
- Strategy contrast: explain why a termination proof alone does not identify a winning player.

No numerical historical answer is promoted.

## N. Dependency declarations

`REQUIRES`: inequalities, nonnegative integers, proof by contradiction/bounds.  
`BRIDGE_REQUIRES`: F1 proof habits; state definition discipline.  
`APPLIES`: monotone progress measures in COMB-04 game/process settings.  
Downstream may assume: strictness + well-foundedness contract and the termination-not-winner warning.

## O. Lead integration notes

Teach invariant vs monovariant as an explicit contrast. Keep the first example non-adversarial enough to isolate the proof mechanism, then re-enter game settings only to show that termination can feed but not replace W/L analysis. Do not imply historical frequency or calibration from the lack of a direct seed anchor.

## P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS (direct symbolic lemmas above)
PROMOTED_NUMERICAL_ANSWERS_CHECKED: NOT_APPLICABLE
SOURCE_IDS_VERIFIED: PASS (no direct historical anchor promoted)
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: classroom/retention/psychometric/publication evidence remains NOT_RUN
```
