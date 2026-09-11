---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-E
microstream_title: Angle Bisector Metric Relations
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: recognizing an internal angle bisector, angle-bisector side ratio, metric use when the split ratio is known, and distinguishing angle bisector from median/altitude/arbitrary cevian.

Excluded: generic similarity proof chapter; external angle-bisector canon unless needed as an extension; Stewart as the default route; circle angle-bisector theorems.

# B. Learner-state model
PRIOR_KNOWLEDGE: “angle bisector divides an angle into two equal angles.”
LIKELY_HALF_KNOWLEDGE: assumes it also bisects the opposite side, or recognizes it only from a symmetric picture.
MISSING_BRIDGES: equal vertex angles imply a side-division ratio, not usually equal segments; theorem use requires the equal-angle hypothesis.
OWNERSHIP_TARGET: connect angle structure to metric side ratio with explicit hypotheses.

# C. Mathematical invariant / governing structure
If `AD` bisects `angle A` in triangle `ABC` with `D` on `BC`, then

`BD/DC = AB/AC`.

Derivation using area: triangles `ABD` and `ACD` share the same altitude to line `BC`, so `[ABD]/[ACD]=BD/DC`. Also using area formula with the equal included angles at A, `[ABD]/[ACD]=(AB*AD*sin∠BAD)/(AC*AD*sin∠DAC)=AB/AC`. Equate the ratios.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| equal angle marks at vertex | angle-bisector theorem | write `BD/DC=AB/AC` | D lies on opposite side | assume midpoint |
| side ratio on BC | possible converse clue | compare with adjacent-side ratio | enough side data | declare angle bisector from drawing |
| area ratio | clean derivation | compare two area expressions | same altitude and equal included angles | invoke similarity without proof |
| general cevian metric | fallback | use Stewart only if target needs length | bisector ratio alone insufficient | Stewart immediately |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| equal base segments | median | angle bisector | is midpoint stated or are vertex angles equal? | symmetric sketches conflate both |
| right angle at foot | altitude | angle bisector | is perpendicularity given? | bisectors can look perpendicular |
| split ratio equals adjacent sides | angle-bisector converse/structure | arbitrary cevian | is the equality proved from data? | ratio coincidence may be accidental if not established |
| target only side split | ratio theorem | Stewart | is a cevian length even needed? | general metric theorem is available |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-AB-01
WRONG_MOVE: angle bisector implies `BD=DC`.
WHY_TEMPTING: word “bisector” is overgeneralized.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: it bisects the angle; side split follows adjacent side ratio.
FALSIFIER_OR_CONTRAST: triangle with `AB:AC=2:3` forces `BD:DC=2:3`.

ERROR_CODE: G01-AB-02
WRONG_MOVE: infer angle bisector from appearance.
WHY_TEMPTING: drawn symmetrically.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: equal angles must be stated or proved.
FALSIFIER_OR_CONTRAST: redraw the same cevian slightly off-center.

ERROR_CODE: G01-AB-03
WRONG_MOVE: apply Stewart before using the ratio theorem.
WHY_TEMPTING: all cevian problems look metric.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: use the cheapest relation that targets the requested information.
FALSIFIER_OR_CONTRAST: ask only for `BD:DC`.

# G. First-move cues
- equal angles at a vertex and cevian to opposite side -> `BD/DC=AB/AC`.
- asked for base split only -> stop once ratio and total side determine segments.
- no equal-angle evidence -> do not use angle-bisector theorem.
- target asks cevian length too -> use ratio first, then choose Stewart or another metric relation if still needed.

# H. H3 -> H0 fading plan
- H3: substitute known adjacent sides into the ratio theorem.
- H2: learner identifies the equal-angle condition and writes the ratio.
- H1: choose angle-bisector vs median/altitude from givens.
- H0: changed-surface problem where equal angles are encoded indirectly by a construction.

# I. Validated IOQM source anchors
No named anchor is a pure angle-bisector-theorem item. `IOQM-2024-Q22` is a contrast anchor: the split `BD:DC=2:1` is given, but no equal-angle hypothesis licenses calling `AD` an angle bisector.

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q22 | 2024 Q22 | CLEAN_OFFICIAL | contrast | ratio-marked cevian, not angle-bisector by default | custody pending | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Q22 closes by the actual right-triangle metric relation and given side split, producing answer `34`. No angle-bisector assumption is used or needed; this is the intended boundary example.

# K. Contrast-pair candidates
1. angle bisector vs median;
2. angle bisector vs altitude;
3. stated equal angles vs visual symmetry;
4. ratio theorem vs Stewart;
5. side ratio conclusion vs equal-segment misconception;
6. direct area derivation vs unproved similarity.

# L. Transfer candidates
- T2: angle bisector hidden inside equal-angle construction.
- T2: determine base split from adjacent side ratio and total base.
- T3: derive theorem with areas, then verify with coordinates.
- T4: integer base-length filter after a rational side ratio.

# M. Candidate mastery items
- recognition-only: classify median/altitude/bisector/arbitrary cevian from givens.
- first-line-only: write the correct ratio.
- full solve: recover split lengths from side ratio and base total.
- WHY-NOT: explain why a given `2:1` split does not prove an angle bisector without adjacent-side information.
- verification: compare area ratios on both sides of the derivation.

# N. Dependency declarations
REQUIRES: area ratio for triangles sharing an altitude; sine area formula or equivalent equal-angle area reasoning.
BRIDGE_REQUIRES: GEO-03 shared-altitude area fact.
APPLIES: Stewart only after ratio information is exhausted.
DOWNSTREAM MAY ASSUME: internal angle-bisector ratio and hypothesis discipline.

# O. Lead integration notes
Teach after median and before/alongside general cevian routing. The area derivation is ideal for reconnecting to GEO-03 rather than duplicating similarity. Make the “bisects angle, not side” contrast explicit early.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: authored angle-bisector items require independent key verification before learner promotion.
