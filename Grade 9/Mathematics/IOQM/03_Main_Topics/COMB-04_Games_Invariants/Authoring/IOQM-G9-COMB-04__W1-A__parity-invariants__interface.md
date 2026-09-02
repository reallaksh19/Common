# IOQM-G9-COMB-04 — W1-A Parity Invariants Interface

```yaml
main_topic_id: IOQM-G9-COMB-04
microstream_id: W1-A
microstream_title: parity invariants
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-04
prerequisite_interfaces:
  - NT-01 stable prerequisite interface @ 5212297212fb097cd508e9fc9d5848b271bc0ad1
  - NT-02 stable residue/cycle interface @ 2b5c4fb1b693e1f881068ec51104d36ca46846e7
source_cutoff: 2026-09-02
```

## A. Scope boundary

Included: parity vectors, parity of counts, mod-2 move effects, parity/colour signatures used as invariants or obstructions, and the proof obligation connecting a preserved parity class to a target state.

Excluded: teaching congruence notation or modular cancellation (NT-02), deterministic transition counting (COMB-03), and strategic W/L recursion when opponent choice matters (W1-D/W1-E).

Canonical ownership: COMB-04 owns the use and design of parity invariants inside game/reachability arguments; NT-01/NT-02 remain the arithmetic providers.

## B. Learner-state model

```text
PRIOR_KNOWLEDGE: odd/even arithmetic; basic divisibility by 2; simple state counting.
LIKELY_HALF_KNOWLEDGE: learner can notice parity after examples but may not prove every move preserves it.
MISSING_BRIDGES: encode the state first; compute one-move parity delta; separate necessary obstruction from constructive sufficiency.
OWNERSHIP_TARGET: automatically test parity signatures before forward simulation when every move has the same mod-2 effect.
```

## C. Mathematical invariant / governing structure

Represent the parity-relevant part of a state as `p in F_2^k`. A legal move changes it by a move vector `d`. A parity functional `I(p)=c·p mod 2` is invariant exactly when `c·d=0` for every legal move vector.

Proof template:

1. define the parity state `p` and candidate `I`;
2. compute `I(p+d)-I(p)=c·d` for an arbitrary legal move;
3. prove this is `0 mod 2` for every legal move;
4. compare the initial and target invariant values;
5. if they differ, conclude impossibility; if they agree, do **not** claim reachability until a construction or completeness argument is supplied.

This is the minimal algebraic form of the issue-level rule: state -> move effect -> invariant -> conclusion.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| parity of one count | odd/even obstruction | write count mod 2 | each move changes count by fixed parity | simulate cases |
| parity vector | several coupled parity classes | record each relevant count mod 2 | move effect is local/linear mod 2 | track full history |
| binary colouring | a linear parity functional visually | sum/toggle one colour class | board has a useful periodic colouring | assume colouring is automatically invariant |
| move-vector table | candidate invariant equations | list deltas for every legal move type | finitely many move types | check only one move type |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| many moves | parity invariant | simulation | do all moves share a fixed mod-2 signature? | examples invite tree search |
| preserved parity | obstruction | construction | is the question impossibility or possibility? | matching parity feels sufficient |
| parity vs residue | W1-A | W1-B | does mod 2 distinguish the required states? | parity is the first familiar modulus |
| reachability vs game | invariant | W/L recursion | does an opponent choose moves to defeat you? | both use states and legal moves |
| deterministic graph vs adversarial game | COMB-03 | COMB-04 | is there an optimizing opponent? | multiple branches look game-like |

## F. Misconception/diagnosis catalogue

```text
ERROR_CODE: PARITY_FROM_EXAMPLES
WRONG_MOVE: infer invariance because several sample moves preserve parity.
WHY_TEMPTING: local evidence looks universal.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: compute the parity delta for every legal move type.
FALSIFIER_OR_CONTRAST: add one legal move type whose delta is odd; the proposed invariant immediately fails.
```

```text
ERROR_CODE: INVARIANT_SUFFICIENCY_LEAP
WRONG_MOVE: equal initial/target parity is treated as proof of reachability.
WHY_TEMPTING: obstruction tests feel like classifications.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: label parity compatibility as necessary only unless a legal construction or spanning/completeness proof is given.
FALSIFIER_OR_CONTRAST: exhibit a system with two disconnected states sharing the same parity signature.
```

```text
ERROR_CODE: PARTIAL_MOVE_CHECK
WRONG_MOVE: verify the invariant for one move but not all legal moves.
WHY_TEMPTING: diagrams emphasize a representative move.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: enumerate move types and check each delta.
FALSIFIER_OR_CONTRAST: a second move type with different parity effect destroys the proof.
```

## G. First-move cues

- “flip/toggle/change an even number” -> encode the changed coordinates mod 2.
- “can this configuration be reached?” -> compare initial/target parity signatures before searching.
- “every move affects a local cluster” -> write the move vector over `F_2`.
- “odd/even number of …” -> test whether that count or a linear combination is preserved.

Minimum first line: `Let p record the relevant counts modulo 2; compute the delta of one arbitrary legal move.`

## H. H3 -> H0 fading plan

- H3: provide the candidate parity functional and ask the learner to verify every move preserves it.
- H2: provide only the parity-vector representation.
- H1: cue “compare one-move parity effects before simulating”.
- H0: changed-surface toggle/reachability item with no parity label or hint.

The first H0 mastery attempt must remain unlabelled and unhinted in learner material.

## I. Validated IOQM source anchors

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q25 | 2025/Q25 | CLEAN_OFFICIAL | primary | pairing invariant; parity; square-product obstruction/construction | no | FINAL_OFFICIAL; verified 36 |
| IOQM-2023-Q28 | 2023/Q28 | CLEAN_VALIDATED | bridge | local flips; `F_2`; colour/parity invariant | source-controlled if used | embedded validated key; verified 67 |
| IOQM-2025-Q22 | 2025/Q22 | CLEAN_OFFICIAL | contrast | game-state parity may compress state but strategic status requires W/L recursion | no | FINAL_OFFICIAL; verified 66 |

## J. Source-independent mathematical trace

**IOQM-2025-Q25.** The independent repository verification establishes: `n=1` is impossible; constructions exist for `n=2` and `n=3`; if a construction exists for `n`, append `2n+1,...,2n+4` and pair `(2n+1,2n+4)` with `(2n+2,2n+3)`. The two new pair sums are equal, so their product contributes a square factor. Hence existence propagates by `n -> n+2`; every `2<=n<=37` works, giving `36`. Parity/exponent structure is an obstruction tool, but the answer requires the construction step as well.

**IOQM-2023-Q28.** The verified route models toggles over `F_2` and finds a dual period-3 invariant. The all-heads/all-tails difference is compatible exactly when `3` does not divide `n`; among `1..100`, this gives `100-floor(100/3)=67`. The interface uses this as evidence that parity invariants can be vector-valued/colour-weighted rather than a single odd/even count.

## K. Contrast-pair candidates

1. same parity but disconnected state vs parity mismatch obstruction;
2. one conserved parity count vs two-coordinate parity vector;
3. parity obstruction vs explicit construction after compatibility;
4. parity reachability puzzle vs adversarial game requiring W/L status;
5. local toggle system vs deterministic recurrence problem owned by COMB-03;
6. mod-2 sufficient discrimination vs a case requiring mod 3/colour classes.

## L. Transfer candidates

- T2 representation: replace physical coins by binary lamps while preserving move vectors.
- T2 context: parity of tokens in boxes under local transfers.
- T3 representation: move from one parity count to a vector of colour-class parities.
- T4 cross-domain: translate a board flip problem into linear equations over `F_2` without teaching full linear algebra.

## M. Candidate mastery items

- Recognition-only: given four move descriptions, identify which one makes parity analysis plausible before calculation.
- First-line-only: write the parity state and one-move delta for a toggle system.
- Full solve: prove an unreachable target by a parity functional, explicitly checking every move type.
- WHY-NOT: explain why matching parity values do not by themselves prove reachability.
- Verification: given a claimed invariant, find a legal move that falsifies it or certify all move types.

No new numerical answer is promoted by this interface.

## N. Dependency declarations

`REQUIRES`: G9 odd/even arithmetic; F1 implication/proof habits.  
`BRIDGE_REQUIRES`: NT-01 divisibility/parity language; NT-02 legal residue interpretation where notation is used.  
`APPLIES`: parity as an invariant inside COMB-04 states.  
Downstream may assume: move-effect check, invariant proof contract, and necessary-vs-sufficient distinction.

## O. Lead integration notes

Teach once globally: invariant proof contract and the warning that compatibility is only necessary absent construction. Compress later parity uses to retrieval. Pair this stream early with W1-B, then contrast with W1-D strategic W/L classification. Do not reproduce NT-02 modular-arithmetic teaching. Do not expose wave/H-level controls in student prose.

## P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS (repository independent oracle: Q25=36, 2023-Q28=67, Q22=66)
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE_FOR_LEAD_INTEGRATION; classroom/retention/psychometric/publication evidence remains NOT_RUN
```
