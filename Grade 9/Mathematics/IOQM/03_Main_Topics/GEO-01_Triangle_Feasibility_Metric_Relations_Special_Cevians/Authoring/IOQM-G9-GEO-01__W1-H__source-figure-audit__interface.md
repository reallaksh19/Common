---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-H
microstream_title: Source and Figure Audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: stable-ID custody, exact-stem reconciliation, figure-dependency status, independent-answer traces, correction of stale mechanism metadata, and render-time safeguards for all eight GEO-01 anchors.

Excluded: final student figure redrawing, learner-facing repository control language, and any silent repair of historical wording/key.

# B. Learner-state model
PRIOR_KNOWLEDGE: learners read diagrams as part of a geometry problem.
LIKELY_HALF_KNOWLEDGE: may infer midpoint/perpendicular/equal-angle status from a picture or lose a phrase such as “not necessarily distinct.”
MISSING_BRIDGES: source wording is mathematical data; a figure supplies only encoded/stated relations; metadata is not the historical source.
OWNERSHIP_TARGET: preserve exact mathematical meaning while translating the problem into a Grade-9 recognition route.

# C. Mathematical invariant / governing structure
Historical promotion requires agreement among four layers: `exact source + exact figure semantics + independent derivation + verification authority`.

All eight numerical answers are independently closed. One stale mechanism was corrected: 2024-Q15 permits repeated choices, so its extremal triple is `(n,n,n+38)`, not `(n,n+2,n+38)`.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| source stem | exact selection/metric hypotheses | transcribe logical givens | controlled paper/validated recovery | rely on classifier paraphrase |
| source figure | incidence/order/marks | list explicit marks | exact page-image custody | infer unstated special cevian |
| independent audit | mathematical closure | re-solve without key derivation | exact stem available | copy official solution |
| corpus metadata | search/classification hints | reconcile against source | ID verified | treat stale mechanism as source truth |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| “choose three” | repeated or distinct semantics from source | assume distinct | does source explicitly permit repetition? | common combinatorial habit |
| cevian appears centered | classify from marks | call it median | is midpoint stated/proved? | symmetric drawing |
| right-angle-looking segment | use stated right angle only | assume altitude | is perpendicularity encoded? | visual appearance |
| metadata route vs exact stem | source controls | classifier controls | is this wording historical or analytical? | metadata is compact |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-SRC-01
WRONG_MOVE: silently replace “not necessarily distinct” by distinct choices.
WHY_TEMPTING: default set-selection habit.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: preserve quantifier/selection semantics exactly.
FALSIFIER_OR_CONTRAST: Q15 answer changes if repeated choices are disallowed.

ERROR_CODE: G01-SRC-02
WRONG_MOVE: infer a median/altitude/bisector from appearance.
WHY_TEMPTING: textbook diagrams are often schematic but visually suggestive.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: segment class comes only from givens/proof.
FALSIFIER_OR_CONTRAST: Q22 has a `2:1` split and must not be called a median.

ERROR_CODE: G01-SRC-03
WRONG_MOVE: trust first-pass mechanism metadata after exact source recovery contradicts it.
WHY_TEMPTING: corpus rows look authoritative.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: paper/active correction beats stale analysis metadata.
FALSIFIER_OR_CONTRAST: Q15 mechanism correction.

# G. First-move cues
- before solving historical item -> list exact hypotheses and whether a figure is source-essential.
- if segment class matters -> record only marked/proved properties.
- if wording changes admissible cases -> preserve it verbatim in teacher/source custody notes.
- if metadata conflicts with exact source -> correct analysis on-branch; never rewrite history silently.

# H. H3 -> H0 fading plan
- H3: identify which diagram facts are explicitly marked.
- H2: separate GIVEN / PROVED / APPEARANCE-ONLY.
- H1: identify one wording detail that changes the mathematical model.
- H0: audit an author-created flawed transcription and repair only the metadata/analysis, not the source.

# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q04 | 2025 Q04 | CLEAN_OFFICIAL | primary | integer isosceles feasibility | no essential figure | FINAL_OFFICIAL |
| IOQM-2025-Q09 | 2025 Q09 | CLEAN_OFFICIAL | primary | shared-diagonal feasibility | no essential figure | FINAL_OFFICIAL |
| IOQM-2024-Q10 | 2024 Q10 | CLEAN_OFFICIAL | primary | algebraic zero -> side ratio -> feasibility | no essential figure | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q15 | 2024 Q15 | CLEAN_OFFICIAL; mechanism corrected | primary | all chosen triples acute; repetition allowed | no essential figure | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q22 | 2024 Q22 | CLEAN_OFFICIAL | primary | right triangle + divided hypotenuse | custody pending | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q27 | 2024 Q27 | CLEAN_OFFICIAL | primary | special point + pedal triangle | custody pending | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q30 | 2024 Q30 | CLEAN_OFFICIAL | primary | altitude to hypotenuse + integer metric | custody pending | OFFICIAL_HBCSE_KEY |
| IOQM-2023-Q13 | 2023 Q13 | CLEAN_VALIDATED | primary | exradii reconstruction | source statement recovered | EMBEDDED_KEY |

# J. Source-independent mathematical trace
Independent answers and checkpoints:
- Q04: `a=6..11`, answer `06`.
- Q09: shared-diagonal interval intersection admits `28`.
- Q10: square decomposition forces ratio; integer `p=7..11`, answer `05`.
- Q15: repeated-choice extremum `(n,n,n+38)` gives least `n=92`.
- Q22: direct right-triangle metric gives answer `34` without misclassifying the cevian.
- Q27: equal angle differences imply `60°`, pedal triangle equilateral with side `6`, area `9sqrt3`, answer `27`.
- Q30: factorized integer metric gives minimum hypotenuse `25`.
- Q13: exradii reconstruct `13,14,15`; final answer `58`.
All agree with verification authority.

# K. Contrast-pair candidates
1. historical wording vs metadata paraphrase;
2. repeated vs distinct selection;
3. stated midpoint vs apparent midpoint;
4. stated perpendicularity vs apparent perpendicularity;
5. source figure vs mathematically altered redraw;
6. official answer vs independent solution.

# L. Transfer candidates
- T2: deliberately distorted cevian diagram with exact marks preserved.
- T2: wording audit where one quantifier changes the extremal case.
- T3: solve from source semantics, then compare with a coordinate reconstruction.
- T4: identify which parts of a corpus row are source facts and which are analyst classifications.

# M. Candidate mastery items
- recognition-only: mark source-essential phrases.
- first-line-only: classify a cevian using only explicit givens.
- WHY-NOT: explain why visual midpoint evidence is invalid.
- verification: compare Q15-style repeated and distinct-choice models.
- source-integrity: detect a redraw that changes a right-angle or ordering relation.

# N. Dependency declarations
REQUIRES: source provenance contract; verification ledger; GEO-03 provider locator.
BRIDGE_REQUIRES: exact HBCSE page-image custody before historical figures are rendered.
APPLIES: independent audit file as mathematical evidence.
DOWNSTREAM MAY ASSUME: eight stable IDs have independently checked answers and explicit source-custody status.

# O. Lead integration notes
Teach one concise student-facing norm: `read the givens/marks, not the appearance`. Keep detailed provenance, correction history, and custody status teacher-side. Ensure Q15’s repeated-choice semantics survives every rewrite. Figure-bearing Q22/Q27/Q30 must not enter final PDF until page-image custody is closed.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact HBCSE page-image/figure custody remains PENDING for publication of figure-dependent anchors; this does not block topic-lead prose integration.
