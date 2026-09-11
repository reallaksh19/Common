---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-F
microstream_title: Inradius, Exradius and Circumradius Bridges
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: area-radius bridges `Delta=rs`, `Delta=r_a(s-a)=r_b(s-b)=r_c(s-c)`, circumradius bridge `Delta=abc/(4R)` when useful, and reconstruction from exradii.

Excluded: full circle/cyclicity/tangency canon; advanced triangle-center theory; memorizing center coordinates; Vieta as a canonical polynomial chapter.

# B. Learner-state model
PRIOR_KNOWLEDGE: area formulas, semiperimeter, incenter/circumcenter names.
LIKELY_HALF_KNOWLEDGE: knows `Delta=rs` but not why exradii pair with `s-a`, or when a radius relation is the cheapest bridge.
MISSING_BRIDGES: radius quantities convert distances-to-sides into area equations; semiperimeter complements `s-a,s-b,s-c` reconstruct side lengths cleanly.
OWNERSHIP_TARGET: treat radius formulas as metric bridges, not a separate catalog of triangle centers.

# C. Mathematical invariant / governing structure
Area is the common currency:
- inradius: `Delta=rs`;
- exradius opposite A: `Delta=r_a(s-a)` and cyclically;
- circumradius: `Delta=abc/(4R)`.

For exradii, set `x=s-a`, `y=s-b`, `z=s-c`. Then `a=y+z`, `b=z+x`, `c=x+y`, so recovering `x,y,z` reconstructs the triangle.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| area split from incenter | `Delta=rs` | sum three base-height triangles | equal distance r to all sides | use perimeter without semiperimeter |
| exradius complement | `Delta=r_a(s-a)` | set `x=s-a` etc. | exradius labels matched correctly | pair `r_a` with `a` directly |
| complement variables x,y,z | side reconstruction | use `a=y+z` etc. | semiperimeter definitions | solve three sides from scratch |
| circumradius bridge | product of sides + area | write `abc=4RDelta` | R given/needed | invoke circle theorem machinery |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| inradius/exradius data | area bridge | coordinate center equations | can area/semiperimeter close it directly? | center coordinates feel explicit |
| exradii + side reconstruction | complement variables | polynomial roots | do `s-a,s-b,s-c` give sides immediately? | source may mention a cubic afterward |
| circumradius + all sides | `abc/(4R)` | law of sines/trig | is only area/radius requested? | trigonometry is standard for R |
| circle tangent to triangle sides | GEO-01 radius bridge | GEO-04 tangency chapter | is the target triangle metric rather than circle structure? | tangent vocabulary suggests GEO-04 |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-RAD-01
WRONG_MOVE: use `Delta=r_a s` for an exradius.
WHY_TEMPTING: overgeneralizes `Delta=rs`.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: excircle area decomposition leaves the complementary semiperimeter factor `s-a`.
FALSIFIER_OR_CONTRAST: compare dimensions/numerical values in a `13-14-15` triangle.

ERROR_CODE: G01-RAD-02
WRONG_MOVE: pair `r_a` with side `a` instead of `s-a`.
WHY_TEMPTING: matching subscripts.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: subscript identifies opposite vertex; tangent-length complement is `s-a`.
FALSIFIER_OR_CONTRAST: reconstruct sides from x,y,z and verify.

ERROR_CODE: G01-RAD-03
WRONG_MOVE: import a full Vieta chapter when a source packages the recovered sides as polynomial roots.
WHY_TEMPTING: polynomial wording appears in the final step.
MISSING_LINK_CLASS: PREREQUISITE
REPAIR_INVARIANT: use only elementary symmetric sums after geometry has recovered the roots.
FALSIFIER_OR_CONTRAST: compute p,q,r directly from `13,14,15` without solving a cubic.

# G. First-move cues
- inradius + area/perimeter -> write `Delta=rs`.
- exradii -> set `x=s-a=Delta/r_a`, etc.
- after x,y,z -> reconstruct `a=y+z`, `b=z+x`, `c=x+y`.
- circumradius + sides/area -> test `Delta=abc/(4R)` before trigonometric expansion.

# H. H3 -> H0 fading plan
- H3: substitute into supplied area-radius formulas.
- H2: choose `Delta=rs` vs `Delta=r_a(s-a)`.
- H1: recognize complement variables as the reconstruction route.
- H0: changed-surface triangle-center data requiring a radius-to-area bridge with no method label.

# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2023-Q13 | 2023 Q13 | CLEAN_VALIDATED | primary | exradii -> complements -> sides -> symmetric sums | no essential source figure | EMBEDDED_KEY |

# J. Source-independent mathematical trace
For Q13, `r_a=21/2`, `r_b=12`, `r_c=14`. Using `x=Delta/r_a`, `y=Delta/r_b`, `z=Delta/r_c` and Heron in complement form yields `Delta=84`, hence `(x,y,z)=(8,7,6)` and sides `(13,14,15)`. Their elementary symmetric sums give `p=42,q=587,r=2730`; nearest integer to `sqrt(p+q+r)=sqrt3359` is `58`. Answer `58` matches authority.

# K. Contrast-pair candidates
1. inradius `rs` vs exradius `r_a(s-a)`;
2. radius bridge vs circle theorem;
3. semiperimeter complements vs direct side variables;
4. geometry reconstruction vs polynomial solving;
5. circumradius product formula vs trigonometric expansion;
6. correct exradius subscript meaning vs naive side pairing.

# L. Transfer candidates
- T2: recover sides from three exradii.
- T2: find inradius from Heron area and semiperimeter.
- T3: compare area decomposition with coordinate distance-to-side computation.
- T4: integer/rational radius data followed by arithmetic filtering.

# M. Candidate mastery items
- recognition-only: choose the correct area-radius bridge.
- first-line-only: define `x=s-a,y=s-b,z=s-c`.
- full solve: reconstruct a triangle from exradii.
- WHY-NOT: explain why `Delta=r_as` is wrong.
- verification: check all radius formulas on a `13-14-15` triangle.

# N. Dependency declarations
REQUIRES: semiperimeter; area; Heron's formula where reconstruction needs closure.
BRIDGE_REQUIRES: elementary symmetric sums only as an application, not ALG-03 canon.
APPLIES: GEO-04 only if a later circle-specific structure is genuinely needed.
DOWNSTREAM MAY ASSUME: inradius/exradius/circumradius area bridges and complement-variable reconstruction.

# O. Lead integration notes
Place after basic cevian metrics, when learners have a stable “choose a bridge by target” habit. Use Q13 as a high-transfer anchor. Keep polynomial language at the final packaging step; geometry should do the reconstruction.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none mathematically; classroom readability of exradius reconstruction remains NOT_RUN.
