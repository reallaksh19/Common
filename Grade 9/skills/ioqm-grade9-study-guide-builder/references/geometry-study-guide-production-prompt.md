# COPY-PASTE PROMPT — IOQM Grade 9 Plane Geometry Study Guide

You are the lead teacher-author for a Grade 9 IOQM Plane Geometry study guide. Build a self-sufficient guide for a learner with roughly 50% prior knowledge: they may remember basic school geometry facts, but cannot be assumed to recognize hidden constructions, know theorem hypotheses, or choose between synthetic, trigonometric, coordinate and vector methods without teaching.

The goal is to move the learner from:

**diagram/givens -> recognize the structure -> justify the theorem -> make the first construction/equation -> complete the proof/calculation -> check degeneracy and figure assumptions.**

## Repository and skill authority

Repository: `reallaksh19/Common`

Read first:

1. `Grade 9/skills/ioqm-grade9-study-guide-builder/SKILL.md`
2. `Grade 9/skills/ioqm-grade9-study-guide-builder/references/syllabus-benchmark-and-refinement-contract.md`
3. `Grade 9/Mathematics/IOQM/README.md`
4. all relevant geometry packages under:
   - `Grade 9/Mathematics/IOQM/03_Main_Topics/GEO-*`
5. relevant algebra/number-theory interfaces when the geometry problem legitimately crosses domains.

Read every supplied Geometry question/tip/source file completely.

Treat coaching reconstructions and user notes as comparison/practice material, not official figure/stem authority.

## Syllabus scope to cover and audit

Use the supplied Plane Geometry syllabus as a scope reference:

- triangles
- quadrilaterals
- circles and their properties
- standard Euclidean constructions
- concurrency and collinearity
- Ceva's theorem
- Menelaus' theorem
- basic trigonometric identities
- compound angles
- multiple and submultiple angles
- general solutions
- sine rule
- cosine rule
- properties of triangles and polygons
- Coordinate Geometry:
  - straight line
  - circle
  - conics
  - 3-D geometry
- vectors

Also preserve the existing repository Grade-9 IOQM geometry coverage, including:
- angle/parallel/polygon structure;
- triangle feasibility;
- right/acute/obtuse metric tests;
- similarity;
- area ratios;
- centroid structure;
- medians/Apollonius;
- Stewart;
- angle bisectors;
- radius bridges;
- cyclicity;
- tangency;
- power of a point;
- integer metric geometry;
- coordinate geometry where canonically owned.

For each syllabus item mark:
- fully taught;
- bridge-level;
- represented under another heading;
- intentionally scope-limited for Grade 9;
- missing and needing a bridge.

Do not silently claim full conics, 3-D geometry, vector geometry, or general trigonometric-equation mastery if the guide only gives introductory bridges. State the depth honestly.

## Benchmarks — quality comparators only

Inspect:

- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`
- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/Quadratics_Assimilation_Benchmark_v2.pdf`

Also inspect the revised study-guide benchmark:

- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/README.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Combinatorics_Study_Guide_v2.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Self_Sufficiency_Audit.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Advanced_Worked_Bridges.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Quick_Reference_2pp.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Appendix_B_20_IOQM_Style_Mock.md`
- `Grade 9/Mathematics/IOQM/04_Study_Guides/Combinatorics_v2/Sources_and_Citations.md`

Use them for the rigor of explanation and audit, not for geometry content or visual design.

## Work process — execute in full

### 1. Syllabus and theorem map

Before prose, create a map with:
- syllabus item;
- repository owner;
- prerequisite theorem;
- Grade-9 derivation/bridge needed;
- figure/source requirements;
- planned depth.

### 2. Inventory every supplied geometry question

For each problem record:

- question number;
- exact givens;
- target;
- primary geometric structure;
- secondary structure;
- source-controlled figure or author-created illustration;
- theorem/criterion needed;
- theorem hypotheses that must be established first;
- first construction or equation;
- alternate method options;
- likely half-knowledge mistake;
- current-guide sufficiency.

Important distinctions include:

- diagram appearance vs proved fact;
- similarity criterion vs mere proportional-looking sides;
- cyclicity proof vs assuming a quadrilateral is cyclic;
- tangent facts only at the tangent point;
- angle bisector vs arbitrary cevian;
- median/Apollonius vs Stewart;
- Ceva for concurrency vs Menelaus for collinearity;
- sine/cosine rule vs Pythagoras;
- synthetic solution vs coordinate overkill;
- coordinate line/circle representation vs conic/3-D/vector scope;
- degenerate triangles and sign/orientation issues.

### 3. Design the 50%-knowledge chapter order

A strong default sequence is:

1. angle language, parallel lines and polygons;
2. triangle feasibility and basic metric facts;
3. congruence and similarity;
4. area ratios and centroid;
5. medians, Apollonius and Stewart;
6. angle bisectors and special cevians;
7. Ceva and Menelaus;
8. circles: cyclicity, chords, angles;
9. tangency, radius relations and power of a point;
10. sine rule, cosine rule and basic triangle trigonometry;
11. standard Euclidean constructions;
12. coordinate geometry: line and circle first;
13. conics/3-D/vectors only as explicit bridge modules if required;
14. integer/metric geometry and mixed method choice.

If the supplied question set demands a different prerequisite order, regroup.

### 4. First draft — write like a geometry teacher at the board

Each substantial subtopic must include:

- what the student probably remembers;
- the missing Olympiad link;
- a clean diagram or precise verbal structure where useful;
- theorem statement;
- why it works / accessible derivation;
- hypotheses;
- non-identical worked example;
- **What should I notice?**
- **Try this first**
- near-miss where the theorem is illegal;
- common mistakes;
- degeneracy/orientation checks;
- practice references.

Do not use learner-facing internal production jargon.

### 5. Orphan-method audit — distrust the first draft

For each supplied problem ask:

> Could a half-prepared student actually execute the solution from this guide, or did I just say the name of a theorem?

Typical Geometry orphan failures:

- “use Ceva” without deriving/teaching the product relation and segment orientation;
- “Menelaus” without explaining transversal/collinearity conditions and directed-sign conventions appropriate to the chosen presentation;
- “by Stewart” without naming the cevian segments correctly;
- “power of a point” without teaching secant/tangent forms and point location;
- “apply sine rule” without side-opposite-angle matching;
- “use cosine rule” without identifying the included/opposite angle relation;
- “coordinate geometry” without choosing coordinates that simplify the constraints;
- “use vectors” without teaching components/dot product required by the problem;
- “draw the perpendicular” without explaining why that construction is useful;
- assuming a point lies inside/on a segment because the sketch looks that way.

Repair every orphan with an executable worked bridge.

### 6. Revisit grouping and method choice

After the first repair pass, question the chapter structure.

Check:
- angle foundations before cyclic angle-chasing;
- similarity before area scaling;
- generic cevians before Ceva/Menelaus;
- median/angle-bisector special cases distinguished from Stewart;
- circle basics before power/tangency;
- right-triangle trig before sine/cosine rules if needed;
- synthetic methods before coordinates where the latter would hide the idea;
- coordinates before vectors/conics/3-D bridges if those are retained.

Regroup for the learner, not for source-document order.

### 7. Broader syllabus audit

Compare the revised guide against:
- the supplied Plane Geometry syllabus;
- all `GEO-*` repository topics;
- verified historical IOQM geometry source maps.

Add appropriate bridges for syllabus items underrepresented in the supplied questions, especially Ceva/Menelaus and sine/cosine rule if absent but within intended scope.

For compound/multiple/submultiple angles, general trig solutions, conics, 3-D and vectors, state clearly whether the guide gives:
- full usable coverage;
- an introductory bridge;
- a deferred/out-of-scope note.

Do not hide these boundaries.

### 8. Appendix A — supplied questions

Create clean Appendix A:
- every supplied geometry question exactly once;
- questions only;
- no solutions/tips/method labels/source commentary;
- preserve every necessary diagram condition;
- if an exact official printed figure is required, use validated source custody rather than silently redrawing;
- answers only after the final Appendix A question.

Record figure/source provenance separately.

### 9. Appendix B — 20-question audit mock

Create 20 fresh IOQM-style geometry questions spanning the guide. Include a balanced sample of:

- angle/polygon structure;
- triangle feasibility/metric tests;
- similarity/area;
- centroid/median/Stewart;
- angle bisector;
- Ceva/Menelaus;
- cyclic geometry;
- tangency/power;
- sine/cosine rule or triangle trig;
- coordinate line/circle;
- one construction/representation-choice item;
- any bridge module actually taught.

Use verified historical mechanisms as design references. Clearly label author-created status in the source ledger.

Answers only after B20.

Independently recompute/prove all answers.

### 10. Quick-reference handout

Create a 1-2 page Geometry Quick Reference with:
- triangle inequality;
- angle sums;
- congruence/similarity criteria;
- area scaling;
- centroid ratios;
- median/Apollonius;
- Stewart;
- angle-bisector theorem;
- Ceva;
- Menelaus;
- cyclic angle tests;
- power of a point;
- tangent-radius facts;
- sine rule;
- cosine rule;
- selected trig identities actually used;
- coordinate distance/slope/midpoint/line/circle facts;
- vector formulas only if the guide genuinely teaches vector methods;
- theorem-legality checklist.

No full solutions.

### 11. Citations and provenance

Create `Sources_and_Citations.md`.

Cite:
- official paper/key/stable IOQM IDs;
- source/figure custody;
- repository source maps;
- comparison material;
- benchmark files.

Keep official figures separate from illustrative redraws and label them accordingly.

### 12. Self-sufficiency audit

Every Appendix A question must have:

1. prerequisite refresh;
2. recognition cue;
3. first construction/equation;
4. execution bridge;
5. theorem-legality/error check;
6. answer-free practice isolation.

Use:
`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n`

only when all pass.

No classroom-effectiveness claim follows from static completeness.

### 13. PDF is the final output

Before final PDF creation or editing, read:

`/home/oai/skills/pdfs/SKILL.md`

Final student PDF:

`Grade 9/Mathematics/IOQM/04_Study_Guides/Geometry_v1/PDFs/Geometry_IOQM_Grade9_Study_Guide_v1.pdf`

Use the PDF skill's recommended authoring/conversion workflow for a long text-heavy document. Preserve vector-quality diagrams where possible.

The final PDF should integrate:
- guide;
- quick reference;
- Appendix A;
- Appendix B;
- student-appropriate citations/source notes.

Detailed QA/custody can remain companion repository files.

Mandatory PDF QA:
- structural preflight;
- render every page at 200 dpi;
- inspect every page, including diagrams;
- no clipping/overlap/broken glyphs/black squares;
- no missing labels, truncated diagrams or malformed geometry notation;
- page count recorded;
- SHA-256 recorded;
- exact final binary committed;
- no workflow required.

## Required repository package

Under:

`Grade 9/Mathematics/IOQM/04_Study_Guides/Geometry_v1/`

create:

- `README.md`
- `Geometry_Study_Guide_v1.md`
- `Quick_Reference_2pp.md`
- `Appendix_A_<source-set>.md`
- `Appendix_B_20_IOQM_Style_Mock.md`
- `Self_Sufficiency_Audit.md`
- `Sources_and_Citations.md`
- `QA.md`
- `PDFs/Geometry_IOQM_Grade9_Study_Guide_v1.pdf`

## Final revisit/refinement report

Document fully:

1. what the first draft missed;
2. which questions exposed missing theorems or hidden constructions;
3. which methods were orphaned;
4. which worked bridges were added;
5. what chapter regrouping was made for a 50%-prepared learner;
6. which syllabus topics required new bridges;
7. which advanced syllabus items remain scope-limited;
8. how figure custody was handled;
9. whether Appendix A is fully supported;
10. whether Appendix B covers the revised guide;
11. whether the quick-reference sheet contains only useful recall facts;
12. citation/provenance completeness;
13. final PDF visual/preflight result.

Do not call the guide complete until both mathematical self-sufficiency and exact-PDF quality gates are closed.