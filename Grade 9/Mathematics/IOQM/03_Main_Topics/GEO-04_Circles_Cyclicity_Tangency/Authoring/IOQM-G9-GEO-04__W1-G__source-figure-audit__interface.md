---
main_topic_id: IOQM-G9-GEO-04
microstream_id: W1-G
microstream_title: Source and Figure Audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-04
prerequisite_interfaces:
  - GEO02_Stable_Angle_Polygon_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: source-ID custody, exact-stem reconciliation, figure-dependency classification, independent-answer trace, non-degeneracy notes, and render-time figure safeguards for the five GEO-04 anchors.

Excluded: circle theorem teaching itself; generic angle teaching; final student layout; any redrawing that changes incidence, tangency, ordering, labels, or metric meaning.

Canonical ownership: GEO-04 owns circle-specific interpretation; GEO-02 supplies only generic angle facts.

# B. Learner-state model
PRIOR_KNOWLEDGE: school angle facts and elementary circle vocabulary.
LIKELY_HALF_KNOWLEDGE: learners trust diagrams and attach the first remembered circle theorem.
MISSING_BRIDGES: source figure is data only when encoded by stated marks/relations; theorem selection must follow proved structure.
OWNERSHIP_TARGET: preserve exact historical meaning while converting it into a clean recognition chain.

# C. Mathematical invariant / governing structure
A historical geometry item is promotable only when `exact source statement + exact figure meaning + independent solution + verified answer` all agree.

The independent audit closes the numerical answers: `2025-Q19=29`, `2025-Q23=03`, `2025-Q30=10`, `2024-Q17=25`, `2023-Q15=03`. Page-image custody remains a separate publication gate for the HBCSE-hosted items.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| exact source stem | logical hypotheses | list givens before solving | wording recovered from controlled paper/overlay | paraphrase that adds a relation |
| historical figure | incidence/tangency/order | inventory explicit marks and labels | exact page-image custody | infer equality/parallelism from appearance |
| coordinate reconstruction | independent numerical check | choose symmetry-preserving axes | coordinates preserve all stated relations | redraw a different configuration |
| source ledger | stable ID and answer authority | match `IOQM-YYYY-QNN` | exact ID verified | treat classifier text as source text |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| diagram looks tangent | use tangency theorem | ordinary chord/line geometry | is tangency stated or proved? | picture looks convincing |
| four points look cyclic | use cyclic relation | generic quadrilateral closure | is concyclicity stated/proved? | circle-shaped layout |
| source figure vs redraw | preserve/source-crop | author-created schematic | is the historical picture itself needed for custody? | cleaner redraw seems harmless |
| classifier text vs paper | paper/overlay controls | ledger mechanism hint | is this exact wording or metadata? | ledger is easier to search |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G04-SRC-01
WRONG_MOVE: infer a geometric relation from visual appearance.
WHY_TEMPTING: diagrams are usually approximately drawn.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: only stated/proved marks are hypotheses.
FALSIFIER_OR_CONTRAST: redraw the same incidence with visibly different lengths/angles.

ERROR_CODE: G04-SRC-02
WRONG_MOVE: copy a metadata paraphrase as the historical stem.
WHY_TEMPTING: metadata is compact.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: paper/validated overlay outranks classifier strings.
FALSIFIER_OR_CONTRAST: Q23 degeneracy note shows wording details can alter admissible branches.

ERROR_CODE: G04-SRC-03
WRONG_MOVE: accept the official key without an independent solution.
WHY_TEMPTING: answer authority exists.
MISSING_LINK_CLASS: EXECUTION
REPAIR_INVARIANT: source-independent trace must reproduce the answer.
FALSIFIER_OR_CONTRAST: solve numerically from coordinates before reading the key.

# G. First-move cues
- Historical figure present -> write a `GIVENS / PROVED / APPEARANCE-ONLY` inventory.
- Metadata and paper wording differ -> paper/active correction overlay controls.
- Degenerate interpretation possible -> test whether source/final-key custody explicitly excludes it.
- Before promotion -> reproduce the verified numerical answer independently.

# H. H3 -> H0 fading plan
- H3: mark which diagram facts are explicitly encoded.
- H2: classify each fact as GIVEN / PROVED / APPEARANCE-ONLY.
- H1: ask which exact source relation unlocks the circle structure.
- H0: solve an author-created circle diagram in which the drawing is deliberately misleading but the stated relations are sufficient.

# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q19 | 2025 Q19 | CLEAN_OFFICIAL | primary | circle + embedded square | custody pending | FINAL_OFFICIAL |
| IOQM-2025-Q23 | 2025 Q23 | CLEAN_OFFICIAL | primary | cyclic rectangle constraint | custody pending | FINAL_OFFICIAL |
| IOQM-2025-Q30 | 2025 Q30 | CLEAN_OFFICIAL | primary | tangent circles / radical axis | custody pending | FINAL_OFFICIAL |
| IOQM-2024-Q17 | 2024 Q17 | CLEAN_OFFICIAL | primary | circumcircle chord | custody pending | OFFICIAL_HBCSE_KEY |
| IOQM-2023-Q15 | 2023 Q15 | CLEAN_VALIDATED | primary | circumcentres | source statement visually confirmed | EMBEDDED_KEY |

# J. Source-independent mathematical trace
Independent audit checkpoints:
- Q19: coordinate square side `s=2/5`, area `4/25`, answer `29`.
- Q23: non-degenerate cyclic branch gives `h^2=1/2`, ratio square `2`, answer `03`.
- Q30: common-chord geometry yields `r1+r2=10`.
- Q17: symmetric circumcircle gives horizontal chord length `25`.
- Q15: perimeter condition reduces circumcentre ratio to `OP^2/OA^2=1/2`, answer `03`.
All agree with verification authority. No unresolved mathematical contradiction remains.

# K. Contrast-pair candidates
1. stated tangency vs apparent tangency;
2. stated cyclicity vs visually cyclic quadrilateral;
3. exact source crop vs author schematic;
4. metadata paraphrase vs controlled stem;
5. official answer vs independent derivation;
6. non-degenerate source reading vs algebraically possible degenerate branch.

# L. Transfer candidates
- T2: same circle theorem with a deliberately distorted figure.
- T2: convert a source diagram into a givens graph before solving.
- T3: solve once synthetically, once by coordinates, compare which source facts each route consumes.
- T4: detect a source-integrity error where a redraw silently changes point order.

# M. Candidate mastery items
- recognition-only: label five diagram facts as GIVEN/PROVED/APPEARANCE.
- first-line-only: identify the one source statement that proves cyclicity.
- WHY-NOT: explain why a tangent theorem is invalid from appearance alone.
- verification: compare an exact source description with a flawed redraw and identify the changed mathematical relation.

# N. Dependency declarations
REQUIRES: source provenance contract; GEO-02 generic angle retrieval.
BRIDGE_REQUIRES: exact paper/figure custody at publication time.
APPLIES: independent source traces from the GEO-04 audit.
DOWNSTREAM MAY ASSUME: promoted GEO-04 anchors have stable IDs, independently checked answers, and explicit custody status.

# O. Lead integration notes
Teach source discipline once globally near the first historical anchor. Compress later to a small `read the marks, not the picture` reminder. Do not expose GitHub/PR/custody-control jargon in student prose. Keep page-image custody notes teacher-side only. This stream should sit before final PYQ promotion and before rendering.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact HBCSE page-image/figure custody remains PENDING for 2025-Q19,Q23,Q30 and 2024-Q17; this blocks publication/render promotion, not topic-lead mathematical integration.
