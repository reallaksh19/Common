# IOQM-G9-COMB-04 — W1-F Construction / Obstruction Interface

```yaml
main_topic_id: IOQM-G9-COMB-04
microstream_id: W1-F
microstream_title: construction versus obstruction
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-04
prerequisite_interfaces:
  - IOQM-G9-COMB-04 W1-A parity invariants
  - IOQM-G9-COMB-04 W1-B residue/colour invariants
source_cutoff: 2026-09-02
```

## A. Scope boundary

Included: necessary-condition obstructions, explicit legal constructions for existence/reachability, inductive extension of constructions, and the distinction between “compatible with every known invariant” and “actually realizable”.

Excluded: generic constructive combinatorics owned by other topics, unsupported search-based existence claims, and treating one construction as a forceable strategy in an adversarial game.

COMB-04 owns the proof architecture “obstruct impossible classes; construct possible classes” when invariants and move systems are central.

## B. Learner-state model

```text
PRIOR_KNOWLEDGE: direct examples, parity, induction at elementary level.
LIKELY_HALF_KNOWLEDGE: learner proves a necessary parity condition and stops, or finds several examples and assumes all remaining cases work.
MISSING_BRIDGES: label proof direction; separate necessity from sufficiency; turn examples into a recursive construction; verify every construction step is legal.
OWNERSHIP_TARGET: know which side of an iff needs obstruction and which side needs construction.
```

## C. Mathematical invariant / governing structure

For a classification claim `property P holds iff condition C`:

- **obstruction direction:** prove `P => C` by an invariant, parity, residue, or structural impossibility;
- **construction direction:** prove `C => P` by an explicit finite legal realization, recursive extension, or complete generation argument.

A correct construction must specify:

1. base configuration(s);
2. legal operation extending a valid construction;
3. proof the target property survives the extension;
4. coverage: every admissible parameter value is reached from a base.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| invariant signature | impossible classes | compare target with required class | invariant truly preserved | call match sufficient |
| explicit move/pair list | existence certificate | write the construction | legality check manageable | show only small examples |
| inductive extension | infinite family | identify base classes and step size | step preserves property | omit residue classes not hit by step |
| reverse construction | reachability certificate | undo target toward a base | reverse moves correspond to legal forward moves | confuse with adversarial strategy |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| invariant proof | obstruction | full iff proof | is the question only impossibility? | necessary conditions feel complete |
| examples | construction seed | proof | is there a repeatable legal extension covering all cases? | pattern recognition is persuasive |
| legal sequence | reachability construction | winning strategy | is there an opponent who can block the sequence? | both describe moves |
| induction by +2 | complete family | partial family | are all required residue classes represented among bases? | induction step alone hides gaps |

## F. Misconception/diagnosis catalogue

```text
ERROR_CODE: INVARIANT_SUFFICIENCY_LEAP
WRONG_MOVE: conclude reachable because invariant values match.
WHY_TEMPTING: invariant often partitions examples cleanly.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: demand an explicit construction or prove the invariant family is complete.
FALSIFIER_OR_CONTRAST: disconnected states with the same invariant signature.
```

```text
ERROR_CODE: EXAMPLES_AS_CONSTRUCTION
WRONG_MOVE: show cases n=2,3,4 and assert the rest.
WHY_TEMPTING: olympiad patterns stabilize early.
MISSING_LINK_CLASS: EXECUTION
REPAIR_INVARIANT: supply a legal recurrence/extension and prove coverage of all admissible n.
FALSIFIER_OR_CONTRAST: an extension by +2 with only one parity base misses half the integers.
```

```text
ERROR_CODE: PATH_AS_FORCEABILITY
WRONG_MOVE: use a legal move sequence as a winning strategy when an opponent chooses turns.
WHY_TEMPTING: both are constructive narratives.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: if adversarial, replace path existence by W/L strategy proof.
FALSIFIER_OR_CONTRAST: opponent deviates from the constructed path.
```

## G. First-move cues

- “for which n does there exist…” -> split into impossible classes and a construction for possible classes.
- “show cannot” -> search for a preserved signature violated by the target.
- “show can” -> write a legal certificate or an inductive extension.
- “if and only if” -> visibly label necessity and sufficiency before solving.

Minimum first line: `Separate the claim into obstruction (necessary) and construction (sufficient) directions.`

## H. H3 -> H0 fading plan

- H3: provide invariant obstruction and construction step; learner fills proof details.
- H2: provide only base cases and ask for a repeatable extension.
- H1: cue “prove both directions: obstruct and construct”.
- H0: changed-surface existence classification with no proof-direction labels.

## I. Validated IOQM source anchors

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q25 | 2025/Q25 | CLEAN_OFFICIAL | primary | square-product pairing; obstruction plus inductive construction | no | FINAL_OFFICIAL; independently verified 36 |
| IOQM-2023-Q28 | 2023/Q28 | CLEAN_VALIDATED | primary transfer | invariant compatibility plus constructive sufficiency for a flip system | source-controlled if reproduced | validated key; independently verified 67 |
| IOQM-2025-Q22 | 2025/Q22 | CLEAN_OFFICIAL | contrast | forceability requires W/L, not a single construction | no | independently verified 66 |

## J. Source-independent mathematical trace

**IOQM-2025-Q25.** Independent verification records the full two-sided architecture: `n=1` is impossible; valid constructions exist for `n=2` and `n=3`; from any valid size `n`, append four new numbers and pair `(2n+1,2n+4)` and `(2n+2,2n+3)`. The equal new pair sums multiply to a perfect square, so the property propagates to `n+2`. The two bases cover both parity classes, hence every `2<=n<=37` works and the count is `36`.

**IOQM-2023-Q28.** The verified `F_2` dual invariant gives the obstruction/class condition `3 ∤ n`; the repository verification states the target works exactly for that class, so the final theorem contains constructive sufficiency beyond mere invariant compatibility. The learner-facing treatment must not collapse these two directions.

## K. Contrast-pair candidates

1. necessary parity condition vs explicit sufficiency construction;
2. three successful examples vs inductive family proof;
3. +2 induction with one base vs +2 induction with bases for both parities;
4. reachable sequence vs forceable adversarial strategy;
5. obstruction certificate vs construction certificate;
6. invariant compatibility vs complete invariant characterization.

## L. Transfer candidates

- T2 pairing target changed while preserving an extension gadget.
- T2 board reachability with a new local move requiring a different obstruction.
- T3 parameter classification where two base residue classes plus step `+k` cover all admissible values.
- T4 combine source-independent invariant proof with a constructive algorithm that generates target states.

## M. Candidate mastery items

- Recognition-only: label each proof fragment as necessity, sufficiency, both, or neither.
- First-line-only: split an iff classification into two proof obligations.
- Full solve: establish an impossible residue class and construct all remaining parameter classes.
- WHY-NOT: explain why four examples plus an invariant match do not establish existence for all n.
- Verification: audit an induction to see whether its bases cover every residue class reached by the step.

No new historical numerical answer is introduced beyond verified anchors.

## N. Dependency declarations

`REQUIRES`: invariant proof contract; elementary induction/construction reasoning.  
`BRIDGE_REQUIRES`: W1-A/W1-B for obstruction candidates.  
`APPLIES`: W1-D only as a contrast; a construction is not a strategy under opposition.  
Downstream may assume: necessity/sufficiency split and base+extension+coverage construction contract.

## O. Lead integration notes

Use Q25 as the canonical two-direction model. Make proof-direction labels explicit early, then fade them before H0. Reuse the same distinction in Q28 without reproducing an uncontrolled historical figure. Place this stream before transfer/mastery so every “possible iff …” item is audited for both directions.

## P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS (repository independent oracle: Q25=36, 2023-Q28=67, Q22=66 contrast)
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact constructive details for historical figures remain source-controlled; classroom/retention/psychometric/publication evidence NOT_RUN
```
