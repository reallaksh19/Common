---
main_topic_id: IOQM-G9-ALG-06
microstream_id: W1-G
microstream_title: Historical source, PYQ and misconception audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-06
prerequisite_interfaces:
  - ALG01_Stable_Prerequisite_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-G — Historical Source, PYQ and Misconception Audit

## A. Scope boundary
Included: exact stable IDs, source/key authority, Q28 correction-overlay custody, independent numerical closure, mechanism classification, learner-safe source use, and source-integrity contrasts. Excluded: inventing source text, silently repairing historical items, or inferring topic weightage from two anchors.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: not applicable as a source-custody stream; learner may encounter cleaned historical extracts.
LIKELY_HALF_KNOWLEDGE: historical notation is trusted even when a repository extraction is stale.
MISSING_BRIDGES: source object and classifier metadata are different; exact stem controls mathematics.
OWNERSHIP_TARGET: SOURCE ID -> EXACT STEM -> INDEPENDENT SOLVE -> KEY CHECK -> TEACHING CLASSIFICATION.
```

## C. Mathematical invariant / governing structure
Source integrity is a mathematical condition: changing nesting, signs, bounds or domains changes the problem. `IOQM-2025-Q28` demonstrates this sharply—the stale classifier `sqrt(x)-sqrt(x+a)=...` is not equivalent to the controlled nested stem `sqrt(x-sqrt(x+a))=...`.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| official/validated paper | historical mathematical object | copy exact stem | source accessible | trust summary string |
| correction overlay | known extraction defects | override classifier only | listed stable ID | alter official source |
| verification ledger | answer check | compare after independent solve | stable ID match | use key as derivation |
| topic source map | teaching mechanism | classify after source lock | no unresolved source conflict | classify from answer alone |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| paper vs ledger wording differs | paper + overlay control | ledger classifier | is ID listed in active overlay? | CSV seems canonical |
| official answer available | independently solve then compare | reverse-engineer key | is solution independently closed? | faster to trust key |
| historical item used for practice | source-linked excerpt | paraphrase as new item | does wording/structure matter? | simplification seems harmless |
| two anchors in topic | mechanism evidence | “weightage” claim | is frequency officially representative? | counts invite percentages |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: ALG06-SRC-01
WRONG_MOVE: use the stale flattened Q28 classifier as the question.
WHY_TEMPTING: it appears in the first-pass 90Q ledger.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: official paper + active correction overlay outrank extraction metadata.
FALSIFIER_OR_CONTRAST: nested-root derivation gives 91; flattened equation is a different problem.

ERROR_CODE: ALG06-SRC-02
WRONG_MOVE: call an answer independently verified after reading/copying the key solution.
WHY_TEMPTING: numerical agreement is mistaken for independent derivation.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: derive first, compare answer second.
FALSIFIER_OR_CONTRAST: preserve the independent audit trace with checkpoints.
```

## G. First-move cues
- stable ID `IOQM-2025-Q28` -> open correction overlay before using any classifier text.
- historical numerical answer -> locate verification-ledger row, but do not derive from it.
- learner export -> remove source-control jargon while retaining year/Q citation.
- any unresolved source conflict -> fail closed; do not promote.

## H. H3 -> H0 fading plan
- H3: present official stem and stale classifier side by side; identify the mathematical difference.
- H2: provide stable ID and ask which repository authority controls it.
- H1: show a suspicious radical extraction and a source-integrity flag.
- H0: audit a new source record for stem/key/classifier consistency without prompting.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q28 | 2025/Q28 | CLEAN_OFFICIAL; `REPOSITORY_METADATA_CORRECTION_REQUIRED` | primary | nested radical; domain; discrete filter | no | FINAL_OFFICIAL 91; independently verified |
| IOQM-2023-Q02 | 2023/Q02 | CLEAN_VALIDATED | primary | reciprocal logs; exponent relation; bounded integer count | no | HBCSE-linked embedded key 54; independently verified |

## J. Source-independent mathematical trace
Q28: prove `y=0`, reduce to `a=t(t-1)/2`, obtain largest nonsquare `<100` as 91. Q02: `t=log_a b>0`, solve `t+6/t=5` -> `t=2,3`; count `b=a^2` and `b=a^3` under 2023 -> 43+11=54. Full traces live in `Independent_Math_and_Source_Audit.md`; official answers agree 2/2.

## K. Contrast-pair candidates
1. nested radical vs flattened radical;
2. source stem vs classifier metadata;
3. independent derivation vs key imitation;
4. answer verification vs source verification;
5. source-linked PYQ vs author-created lookalike;
6. topic evidence vs unsupported weightage claim.

## L. Transfer candidates
- T2: identify a sign lost in an OCR/classifier extraction.
- T2: compare two source versions with different bounds.
- T3: source record where answer is correct but mechanism metadata is stale.
- T4: apply the same custody workflow to a geometry item with a figure.

## M. Candidate mastery items
- recognition: choose the controlling source for Q28.
- first-line: state what must be checked before promoting a historical item.
- full solve: independently solve one short source anchor then compare with key.
- WHY-NOT: explain why a correct answer does not validate a corrupted stem.
- verification/source-integrity: audit stable ID, source status, overlay and key status.

## N. Dependency declarations
`REQUIRES`: repository source provenance contract and verification ledger.  
`BRIDGE_REQUIRES`: W1-C/W1-E mathematics for independent checks.  
`APPLIES`: all historical material in ALG-06.  
Downstream may assume Q28 is controlled by the nested-radical stem and both source answers are independently closed.

## O. Lead integration notes
Student prose should show only clean historical citations and mathematics. Keep overlay/classifier details in Teacher/Authoring custody. Q28 must never be copied from the stale 90Q classifier field. Do not infer topic frequency/weightage from the two anchors.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration; classroom calibration NOT_RUN
```
