# IOQM-G9-COMB-04 — W1-G Source / PYQ Audit Interface

```yaml
main_topic_id: IOQM-G9-COMB-04
microstream_id: W1-G
microstream_title: source and PYQ audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-04
prerequisite_interfaces:
  - IOQM Grade 9 source provenance contract
  - IOQM 2023-2025 90Q ledger
  - IOQM independent answer verification ledger and Batch C
source_cutoff: 2026-09-02
```

## A. Scope boundary

Included: source identity, answer-key custody, stable IDs, historical-vs-authored distinction, mechanism tags, figure custody, independent-answer verification status, and safe promotion rules for the three COMB-04 anchors.

Excluded: inventing source IDs, silently repairing source text, inferring official topic weightage from three anchors, reproducing source figures without controlled custody, or treating repository metadata as superior to a validated historical paper when a conflict exists.

This stream audits evidence for the lead; it does not become learner-facing source bureaucracy.

## B. Learner-state model

```text
PRIOR_KNOWLEDGE: not applicable as a direct teaching stream.
LIKELY_HALF_KNOWLEDGE: authors may over-expose provenance machinery or paraphrase a historical item until its mechanism changes.
MISSING_BRIDGES: distinguish source fact, repository classification, independent mathematical verification, and author-created transfer material.
OWNERSHIP_TARGET: every promoted historical claim remains traceable while student prose stays clean.
```

## C. Mathematical invariant / governing structure

Source promotion has four independent checks:

1. **identity** — stable item ID, year/question number, paper/key locator;
2. **integrity** — source status and any known correction/conflict;
3. **mathematical verification** — answer independently recomputed or explicitly marked otherwise;
4. **pedagogical use** — mechanism/role recorded without upgrading recurrence into official weightage.

No one check substitutes for another. A correct answer with uncertain source identity is not source-clean; a clean official key without independent recomputation is not independently verified.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| corpus ledger row | stable metadata and source locators | match exact stable ID | frozen ledger available | copy nearby row by position |
| verification ledger | independent answer verdict | match same stable ID | independent batch exists | infer verification from official key alone |
| source map | pedagogical role | classify primary/bridge/contrast | mechanism checked | infer exam weightage |
| figure custody note | visual provenance | link/reconstruct only under explicit status | source image relevant | redraw as “the official figure” |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| official answer | source key | independent verification | was the value recomputed separately? | both may agree numerically |
| historical item | PYQ | author-created transfer | does a stable corpus ID/source locator exist? | changed-surface items resemble PYQs |
| source correction | metadata repair | historical conflict | is the defect in repository transcription or the source itself? | all discrepancies look like source problems |
| figure recreation | authored schematic | historical figure | is exact visual identity claimed? | a redraw may look equivalent |
| anchor recurrence | evidence of mechanism | official weightage | does source authority publish topic frequency? | repeated examples invite statistical claims |

## F. Misconception/diagnosis catalogue

```text
ERROR_CODE: SOURCE_ID_GUESS
WRONG_MOVE: assign an item ID/year/question from memory.
WHY_TEMPTING: mechanism and answer may be familiar.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: match the frozen ledger row exactly.
FALSIFIER_OR_CONTRAST: a neighboring question with similar domain but different stable ID.
```

```text
ERROR_CODE: KEY_EQUALS_VERIFICATION
WRONG_MOVE: mark an answer independently verified merely because it matches an official key.
WHY_TEMPTING: official authority is strong.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: require the independent verification ledger/batch locator.
FALSIFIER_OR_CONTRAST: a corrected official key demonstrates why source-key status and independent recomputation are distinct.
```

```text
ERROR_CODE: FIGURE_CUSTODY_DRIFT
WRONG_MOVE: redraw or relabel a historical diagram and present it as exact.
WHY_TEMPTING: the mathematical incidence may appear preserved.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: label authored schematics as authored; preserve exact source custody when historical identity matters.
FALSIFIER_OR_CONTRAST: a small geometric/layout change can alter adjacency or interpretation.
```

```text
ERROR_CODE: WEIGHTAGE_INFERENCE
WRONG_MOVE: call a mechanism high-frequency/officially weighted from three years of anchors.
WHY_TEMPTING: corpus recurrence is visible.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: describe only observed validated anchors; keep official weightage/qualification probability NOT_RUN.
FALSIFIER_OR_CONTRAST: source papers do not publish the claimed topic probability.
```

## G. First-move cues

For any historical item: `stable ID -> exact ledger row -> source/key status -> independent verification row -> pedagogical role`.

For any figure: ask whether the learner artifact needs the historical visual at all; if not, use a clearly authored schematic or text-only abstraction.

## H. H3 -> H0 fading plan

This is primarily an authoring-control stream. If provenance awareness appears pedagogically, fade from explicit source notes in teacher material to clean learner tasks. Never expose internal source-status codes, wave labels, H-level controls, hashes, or issue IDs in student prose.

## I. Validated IOQM source anchors

| Stable ID | Year/Q | Paper/key authority | Source status | Mechanism | Official / validated answer | Independent verification |
|---|---|---|---|---|---:|---|
| IOQM-2025-Q22 | 2025/Q22 | HBCSE official paper + final key | CLEAN_OFFICIAL | impartial game; winning states | 66 | PASS, Batch C |
| IOQM-2025-Q25 | 2025/Q25 | HBCSE official paper + final key | CLEAN_OFFICIAL | pairing invariant; square product; construction/obstruction | 36 | PASS, Batch C |
| IOQM-2023-Q28 | 2023/Q28 | HBCSE-linked MTAI paper with embedded key | CLEAN_VALIDATED | invariant game; local flips; `F_2` colour/parity invariant | 67 | PASS, Batch C |

Source locators remain the frozen corpus ledger authorities. No source ID is inferred from prose.

## J. Source-independent mathematical trace

Repository Batch C records:

- `IOQM-2025-Q22 = 66`: exact recursive evaluation of the historical `(blue,red)` game states under the source legal moves and terminal rule; 66 winning starts among 121 starts.
- `IOQM-2025-Q25 = 36`: `n=1` obstruction; valid bases at `n=2,3`; extension `n -> n+2` by adding two equal-sum pairs; every `2<=n<=37` works.
- `IOQM-2023-Q28 = 67`: `F_2` model; period-3 dual invariant; target works iff `3 ∤ n`; count `100-floor(100/3)=67`.

All three are `PASS` in the independent verification authority. These checks validate the answers and mathematical routes, not classroom calibration or publication approval.

## K. Contrast-pair candidates

1. official key agreement vs independent recomputation;
2. historical PYQ vs authored transfer item;
3. clean source vs repository metadata defect;
4. authored schematic vs exact historical figure;
5. observed mechanism recurrence vs unsupported official weightage claim;
6. stable ID lookup vs guessed source identity.

## L. Transfer candidates

- T2: changed-surface authored game derived from Q22 mechanism, clearly labeled authored.
- T2: pairing construction with altered target, not labeled PYQ.
- T3: abstract local toggle system derived from Q28 without copying historical figure.
- T4: source-integrity audit exercise for teacher/reviewer use, not learner mastery.

## M. Candidate mastery items

Authoring/reviewer candidates only:

- given a draft item, classify `HISTORICAL_VALIDATED_PYQ` vs `AUTHOR_CREATED_TRANSFER`;
- trace a promoted answer to both source key and independent verification evidence;
- identify a source claim that improperly implies official weightage;
- inspect a reconstructed diagram and decide whether it is safely labeled as authored.

No new learner-facing numerical item is promoted here.

## N. Dependency declarations

`REQUIRES`: frozen corpus ledger; source provenance contract; independent verification ledger/Batch C.  
`BRIDGE_REQUIRES`: all mathematical streams when their historical anchors are promoted.  
`APPLIES`: source controls to every later learner/teacher artifact.  
Downstream may assume: Q22/Q25/Q28 identities and answers are source-clean and independently verified at the static level.

## O. Lead integration notes

Keep almost all of this stream in authoring/teacher QA. In learner prose, use clean source labels only where pedagogically useful. Never expose hashes, Git blobs, issue/PR controls, H-levels, or source-status codes. For 2023-Q28, preserve issue-mandated figure custody even though the frozen corpus row does not require a figure for classification.

## P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS (against independent Batch C)
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS (66 / 36 / 67)
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact historical visual reproduction, if later used, requires controlled source custody; classroom/retention/psychometric/qualification-probability/weightage/publication evidence NOT_RUN
```
