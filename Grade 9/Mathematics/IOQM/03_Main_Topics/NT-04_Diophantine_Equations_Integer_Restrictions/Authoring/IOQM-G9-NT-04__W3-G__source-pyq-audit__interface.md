---
main_topic_id: IOQM-G9-NT-04
microstream_id: W3-G
microstream_title: Source and PYQ audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: []
source_cutoff: 2026-09-02
---

# Source and PYQ audit - Research Interface

## A. Scope boundary
Included: stable IDs, source/key status, correction overlays, independent answer traces, and prevention of source-custody leakage into authored material. Excluded: pedagogical ownership of any mathematical mechanism.

## B. Learner-state model
`PRIOR_KNOWLEDGE:` not applicable to source custody.

`LIKELY_HALF_KNOWLEDGE:` an author may trust a stale extracted stem or provisional key.

`MISSING_BRIDGES:` distinguish historical source correction from repository metadata correction; distinguish official final key from provisional key; independently recompute answers.

`OWNERSHIP_TARGET:` preserve exact source authority while allowing concise learner-facing mechanism use.

## C. Mathematical invariant / governing structure
**Invariant:** `SOURCE -> EXACT STEM STATUS -> KEY STATUS -> INDEPENDENT RECONSTRUCTION -> ONLY THEN PROMOTION`.

The seven NT-04 IDs are fixed by the corpus authority. Two require special custody:
- 2025-Q11: final official key corrected a provisional answer; promote only final 26.
- 2023-Q04: historical paper is clean and contains `x^4`; a stale repository classifier flattened it to `x/4`. The active metadata overlay corrects the extraction. Do not mark the historical source conflicted.

Independent traces must agree with the governing key before promotion. Authored items receive no historical ID.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| stable ID | source identity | resolve paper/key | exact year/Q | invent shorthand ID |
| correction overlay | metadata status | read overlay before ledger stem | overlay active | silently rewrite |
| final vs provisional key | authority | use final official | status explicit | quote provisional |
| authored item | no historical provenance | assign local metadata ID | clearly authored | fake PYQ label |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| wrong extracted stem | metadata correction | source conflict | Is the official paper itself wrong? | any mismatch looks like source error |
| two key values | final official | provisional | Which key status is authoritative? | earlier value may persist |
| answer ledger | independent verification | copied key | Was the math recomputed? | ledger is convenient |
| historical-like authored item | authored metadata | PYQ attribution | Does it originate in a validated paper? | style resembles contest item |

## F. Misconception / diagnosis catalogue
`NT04-SRC-01`
- WRONG_MOVE: solve stale `x/4` for 2023-Q04.
- WHY_TEMPTING: first-pass ledger text is searchable.
- MISSING_LINK_CLASS: SOURCE_INTEGRITY.
- REPAIR_INVARIANT: paper + overlay + verification ledger.
- FALSIFIER_OR_CONTRAST: validated paper visibly contains exponent 4.

`NT04-SRC-02`
- WRONG_MOVE: use 61 for 2025-Q11.
- WHY_TEMPTING: provisional key circulated first.
- MISSING_LINK_CLASS: SOURCE_INTEGRITY.
- REPAIR_INVARIANT: final official key is 26 and independent determinant solution agrees.
- FALSIFIER_OR_CONTRAST: 11/15 yields a+b=26.

`NT04-SRC-03`
- WRONG_MOVE: label authored practice `IOQM-2026-Q...`.
- WHY_TEMPTING: consistent-looking provenance.
- MISSING_LINK_CLASS: SOURCE_INTEGRITY.
- REPAIR_INVARIANT: authored items use local NT04 item IDs only.
- FALSIFIER_OR_CONTRAST: no validated historical paper supports the fake ID.

## G. First-move cues
- any promoted PYQ -> verify stable ID + source status + key status.
- any corrected metadata -> state correction explicitly in teacher/authoring artifacts.
- any learner paraphrase -> preserve mechanism without pretending to quote full stem.
- any authored item -> use a local NT04 ID, never a historical ID.

## H. H3 -> H0 fading plan
- **H3:** distinguish source correction, key correction and metadata correction examples.
- **H2:** given three custody records, choose which source to promote.
- **H1:** identify the risk flag from a mismatching extracted stem.
- **H0:** audit a mixed table containing historical and authored items.

## I. Validated IOQM source anchors
| Stable ID | Answer | Source/key note |
|---|---:|---|
| `IOQM-2025-Q03` | 18 | clean final official |
| `IOQM-2025-Q11` | 26 | final official key corrected provisional 61 |
| `IOQM-2024-Q13` | 19 | clean official |
| `IOQM-2023-Q03` | 23 | clean validated embedded key |
| `IOQM-2023-Q04` | 07 | clean historical source; metadata overlay for `x^4` |
| `IOQM-2023-Q11` | 14 | clean validated embedded key |
| `IOQM-2023-Q29` | 95 | clean validated embedded key |

## J. Source-independent mathematical trace
Independent traces are recorded in `01_Source_Coverage_Map.md` and were recomputed separately using factor-pair enumeration, determinant-gap arguments, divisor reconstruction, exact exponent correction, difference-of-squares factorisation, and multiplicative-partition uniqueness. All seven agree with the verification ledger under the stated custody notes.

## K. Contrast-pair candidates
1. source correction vs metadata correction;
2. provisional key vs final key;
3. historical ID vs authored local ID;
4. copied key vs independent math audit;
5. concise paraphrase vs reproduction of full historical wording.

## L. Transfer candidates
- **T2:** audit a corrupted classifier line against a clean source.
- **T3:** compare two provenance chains with different key statuses.
- **T4:** route an authored transfer item so it retains mechanism tags without historical attribution.

## M. Candidate mastery items
- Verification: explain why 2023-Q04 is not a source conflict.
- Verification: identify authoritative answer for 2025-Q11 and justify independently.
- WHY-NOT: reject invented official topic-weightage percentages from seven anchors.
- Source classification: label historical versus authored items correctly.

## N. Dependency declarations
`REQUIRES:` corpus authority and correction overlay only.

`BRIDGE_REQUIRES:` mathematical interfaces for independent traces.

`APPLIES:` all promoted historical examples.

`EXPORTS:` source-custody notes to topic QA; no student mathematical doctrine.

## O. Lead integration notes
Keep detailed custody in authoring/teacher QA. Student prose may include compact source IDs where useful but should not expose repository workflow language. The 2023-Q04 correction must remain explicit anywhere the exact equation is used, and 2025-Q11 must never regress to provisional 61.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE
