# Visualization Production Contract v1

## Status and role

This document supplements `question-driven-self-sufficient-study-guide-skill-v2.md` whenever a study-guide build has a non-trivial visualization requirement.

It exists because **“a figure would help” is not a complete production instruction**. A visualization must be planned, specified, rendered, placed, and audited as part of the teaching method — not added as decoration after the prose is finished.

Use this contract when any question-to-method row, chapter, worked bridge, quick-reference item, or Navigator item has:

```text
REQUIRED_VISUAL != NONE
```

The governing principle is:

> **Visual requirement -> visual specification -> representation choice -> final-size prototype -> production -> figure audit -> document audit.**

A good-looking image is not automatically a mathematically valid or pedagogically useful figure.

---

## 1. Why the visualization workflow must be explicit

A visual build can fail even when the underlying mathematics and prose are correct.

Typical failure modes include:

- generating figures before deciding their physical size in the final PDF;
- making every figure full-width by default, causing oversized diagrams and wasted page space;
- shrinking a text-heavy raster image after generation until labels become too small;
- allowing labels, formulas, angle marks, or captions to overlap;
- duplicating the page heading inside the figure;
- placing long teacher prose inside the image instead of in searchable/typeset document text;
- using an aesthetically plausible diagram that does not preserve the stated incidence, tangency, collinearity, cyclicity, or equality conditions;
- letting image-generation artifacts introduce false geometric facts;
- adding visuals late, after the prose layout is stable, and then causing pagination, hint-strip, or appendix crowding failures;
- inspecting only the whole page and missing a figure that is illegible at actual reading size;
- treating a missing or mathematically wrong figure as a cosmetic issue rather than a content failure.

The production system must therefore make visualization a first-class authored artifact with its own IDs, manifest, source files, and acceptance gates.

---

## 2. Add a visual-obligation layer to the question-to-method matrix

When a visual is required, extend the row with:

- `VISUAL_REQUIRED`: `NONE`, `OPTIONAL`, or `REQUIRED`;
- `FIGURE_ID`;
- visual role: `RECOGNIZE`, `EXPLAIN`, `EXECUTE`, `CHECK`, or `REFERENCE`;
- mathematical facts the figure must preserve;
- facts the figure must **not** imply unless proved/given;
- student action on the figure, if any;
- representation type;
- target final footprint class;
- hint interaction, if any;
- current visual support status: `PASS`, `PARTIAL`, or `FAIL`.

### Visual teaching-obligation rule

If a problem materially depends on seeing the configuration, then a usable figure is part of the teaching obligation.

Naming the theorem in prose does not discharge that obligation.

For Geometry in particular, a learner should not be forced to reconstruct a complex diagram mentally before they can even begin recognizing the method.

---

## 3. Stable figure IDs

Give reusable visual assets stable IDs.

Recommended pattern:

```text
<DOMAIN>-FIG-<FAMILY>-<NN>
```

Examples:

```text
GEO-FIG-CYCLIC-01
GEO-FIG-TANGENT-03
ALG-FIG-ROOTS-02
COMB-FIG-GAPS-01
```

Question-specific figures may also use the local question ID in the manifest, for example:

```text
APP-A-Q43 -> GEO-FIG-ISO-07
```

Stable figure IDs allow:

- hints to say what to mark on the correct figure;
- the visual audit to verify every required visual;
- later layout changes without losing source/figure correspondence;
- exact figure regeneration after a wording or notation change;
- reviewer QA to distinguish a prose problem from a rendering problem.

---

## 4. Build a Figure Manifest before rendering

Do not begin batch figure generation from prose alone.

Create `Figure_Manifest.md` or an equivalent structured table first.

Minimum columns:

| Field | Required content |
|---|---|
| Figure ID | stable ID |
| Location | chapter / bridge / Appendix question |
| Purpose | what cognitive load the visual removes |
| Required geometry/data | facts that must be visibly true |
| Forbidden implication | facts the sketch must not silently add |
| Labels | exact notation to appear |
| Student action | e.g. mark equal angles / identify chord / compare areas |
| Representation | deterministic diagram / chart / table / generated illustration / other |
| Footprint | `S`, `M`, `L`, `XL` |
| Caption | short nearby explanation, if needed |
| Hint link | H1/H2/H3 interaction, if any |
| Source | author-created / external source + citation |
| Status | `SPEC`, `PROTOTYPE`, `PASS`, `FAIL` |

### Figure specification rule

The manifest is the source of truth for the visual requirement.

A figure should not be accepted merely because it “looks close enough” to a sentence in the manuscript.

---

## 5. Choose the representation before choosing the tool

The representation should follow the teaching need and mathematical fidelity requirement.

### 5.1 Deterministic mathematical drawing — default for theorem-critical Geometry

Prefer a deterministic/vector or programmatic construction when correctness depends on exact relationships such as:

- collinearity;
- concurrency;
- parallelism or perpendicularity;
- tangency;
- cyclicity;
- equal-length/equal-angle markings;
- midpoint or ratio placement;
- coordinate geometry;
- area decomposition;
- locus or construction steps.

Examples of suitable source forms include SVG, TikZ, geometry primitives, plotting/vector libraries, or another reproducible mathematical drawing system.

The key property is not the specific software; it is that the mathematical source can be regenerated and audited.

### 5.2 Generated illustration — use for conceptual explanation, not unverified geometry

Image generation can be useful for:

- conceptual infographics;
- visual metaphors;
- non-critical explanatory scenes;
- style exploration;
- a cleaned-up conceptual figure whose exact geometry is not itself evidence.

Do **not** rely on an unverified generated image for theorem-critical incidence or exact mathematical labels.

If generated output is used for Geometry, verify every required condition against the Figure Manifest. If text/labels are unreliable, generate the base visual and overlay mathematical labels deterministically.

### 5.3 Chart / table / graph

Use charts, tables, number lines, state diagrams, residue grids, recurrence diagrams, or function graphs when the structure is data- or state-driven rather than spatially geometric.

Do not force every visualization into a picture.

---

## 6. Separate mathematical content from document typography

As a default:

- keep the **page/chapter title outside** the image;
- keep long teacher explanation outside the image;
- keep captions outside the image unless the visual is designed as a self-contained card;
- put only labels, short formulas, measurements, and indispensable annotations inside the figure;
- prefer document-native/type-set formulas when shrinking the image would make formula text too small;
- avoid repeating the same title both in the page heading and in the figure.

This improves accessibility, text extraction, consistency, and scale robustness.

---

## 7. Design at final physical size, not at source-canvas size

A 1400-pixel image is not “large” or “small” until its PDF placement is known.

Before rendering, assign a target footprint.

### Calibration defaults

Use the document's **usable body width**, not page width.

| Footprint | Typical body-width use | Use case |
|---|---:|---|
| `S` | 35–45% | one small relation / icon-like schematic |
| `M` | 50–65% | ordinary theorem or recognition figure |
| `L` | 65–80% | worked example with several labels |
| `XL` | 80–95% | dense figure where smaller placement harms legibility |

These are calibration defaults, not rigid layout laws.

Routine teaching figures should usually not consume more than roughly 30–40% of the usable page body height. Complex worked figures may use roughly 45–55%. A full-page figure should be deliberate and figure-dominant, not the result of automatic image scaling.

### Final-size label rule

Judge label size **after placement** in the PDF.

If a figure must be reduced until labels are too small, do not keep shrinking it. Redesign the figure:

- remove non-essential in-image text;
- move explanation into the document;
- simplify the visual;
- split it into panels;
- or assign a larger footprint intentionally.

### Raster resolution rule

Raster assets should have enough source pixels for their intended physical placement. Final PDF inspection still occurs at 200 dpi, but source artwork should not already be marginal before insertion.

---

## 8. Prototype before batch production

Do not create the full visual set before proving the visual system works.

### Required prototype set

Choose at least:

1. one simple figure;
2. one text/label-dense figure;
3. one complex mathematical figure;
4. one Appendix A figure with local hints if the domain is diagram-heavy.

Insert these into the actual document template at their intended footprint and export a sample PDF.

Inspect:

- scale;
- label size;
- line weight;
- whitespace;
- caption spacing;
- page balance;
- interaction with H1/H2/H3 strips;
- whether the figure is still readable on a normal screen and printout.

Only after the prototype set passes should the remaining visual set be produced in bulk.

### Why this gate exists

Late global resizing is a repair, not a production strategy.

The intended figure box should shape the figure from the beginning.

---

## 9. Geometry-specific fidelity checklist

For every theorem-critical Geometry figure verify, as applicable:

- correct point count and names;
- correct point order;
- collinear points are actually collinear;
- points stated to lie on a segment or circle do so;
- midpoint placement is consistent with the statement;
- right angles are shown only where given/proved for the teaching stage;
- parallel/tangent markers match the statement;
- equal-length and equal-angle marks are consistent;
- circle centers and radii are correctly related;
- cyclic points lie on one circle when cyclicity is given;
- extensions are visibly extensions, not new unrelated lines;
- auxiliary constructions are not shown before the learner is supposed to discover them;
- no accidental symmetry suggests an unstated equality;
- orientation does not contradict the required point order;
- no answer or decisive hidden construction is leaked in answer-free practice.

`NOT_TO_SCALE` permits non-proportional lengths. It does **not** permit a wrong incidence structure.

---

## 10. Figure-first pedagogy and hint interaction

A visual should reduce a specific cognitive burden.

Useful roles include:

### `RECOGNIZE`
Expose the configuration the learner must identify.

Example H1:

> **H1 · Notice** Mark the two isosceles triangles created by the equal-length conditions.

### `EXPLAIN`
Show why a theorem or transformation works.

### `EXECUTE`
Provide the working surface on which the learner marks angles, ratios, or constructions.

### `CHECK`
Help the learner test whether a proposed result still satisfies the original geometry.

### `REFERENCE`
Summarize a recurring visual pattern in a Visual Bridge or quick reference.

The figure and the hint ladder should be designed together. Do not write H1 later and discover that the figure does not actually make the requested marking possible.

---

## 11. Visual Bridge composition rules

For a Visual Bridge page:

- prefer 2–4 compact panels rather than one oversized poster;
- give each panel one teaching job;
- keep recognition phrase and first move adjacent to the relevant panel;
- use one consistent notation/color system;
- avoid decorative background art;
- keep panel captions short;
- do not duplicate a full worked solution inside a bridge that is meant to be a recognition router.

If one panel becomes dense enough to require long prose, promote it to an Advanced Worked Bridge rather than shrinking everything else.

---

## 12. Appendix A figure rules

For diagram-driven practice:

- the problem statement and figure remain visually dominant;
- the figure should be small enough to preserve the compact problem-set rhythm but large enough to act on;
- H1 may refer directly to a mark the learner should add;
- H2 points back to a previously taught skill/bridge;
- H3 gives the first executable move without drawing the hidden solution for the learner;
- do not show auxiliary lines, reflection images, or completed constructions in the base figure if discovering them is the problem's key move;
- if a problem cannot remain legible with local hints, move only that problem to a larger footprint or use the Hint Bank fallback rather than globally enlarging all figures.

Aim for 2–3 questions per page where the actual statement/figure complexity permits.

---

## 13. The visual production loop

When visualization is required, use this pipeline:

```text
QUESTION-TO-METHOD MATRIX
-> MARK VISUAL OBLIGATIONS
-> BUILD FIGURE MANIFEST
-> ASSIGN STABLE FIGURE IDS
-> CHOOSE REPRESENTATION
-> SPECIFY FINAL FOOTPRINT
-> BUILD 4-FIGURE PROTOTYPE SET
-> INSERT PROTOTYPES INTO REAL DOCUMENT TEMPLATE
-> EXPORT SAMPLE PDF
-> CALIBRATE SCALE / LABELS / LINE WEIGHT / PAGE BALANCE
-> FREEZE VISUAL STYLE CONTRACT
-> PRODUCE REMAINING FIGURES
-> RUN MATHEMATICAL FIDELITY AUDIT
-> INSERT AT DECLARED FOOTPRINTS
-> RUN FIGURE-LEVEL FINAL-SIZE QA
-> RUN PAGE-LEVEL 200-DPI QA
-> REPAIR SOURCE FIGURES, NOT ONLY PLACEMENT
-> RE-RENDER AFFECTED PAGES
-> FINAL VISUAL PASS
```

### Repair rule

If a figure fails because of content, labels, or geometry, repair the figure source.

If it fails only because of placement, repair the document layout.

Do not blur those two failure classes.

---

## 14. Visual acceptance gates before PDF generation

If any required visual exists, add these gates before the normal hard PDF gate:

```text
VISUAL_REQUIREMENTS_INVENTORIED = PASS_m_OF_m
FIGURE_MANIFEST_COMPLETE = PASS_m_OF_m
FIGURE_IDS_STABLE = PASS_m_OF_m
FIGURE_REQUIRED_FACTS_PRESERVED = PASS_m_OF_m
FIGURE_FORBIDDEN_IMPLICATIONS = 0
FIGURE_ANSWER_LEAKAGE = 0
FIGURE_FINAL_SIZE_LEGIBILITY = PASS_m_OF_m
FIGURE_SCALE_BUDGET = PASS_m_OF_m
FIGURE_HINT_INTERACTION = PASS_m_OF_m_WHERE_APPLICABLE
FIGURE_SOURCE_REPRODUCIBILITY = PASS_m_OF_m
VISUAL_ORPHANS = 0
```

For Geometry, additionally require:

```text
THEOREM_CRITICAL_FIGURE_FIDELITY = PASS_m_OF_m
```

If any required figure remains `PARTIAL` or `FAIL`:

```text
PDF_GENERATION_ALLOWED = FALSE
STATUS = VISUAL_REWRITE_REQUIRED
```

A polished manuscript does not override this gate.

---

## 15. PDF QA must include figure-level inspection

Whole-page inspection is necessary but insufficient.

At final QA:

1. render every page at 200 dpi;
2. inspect every page as a whole;
3. inspect every required figure at its **actual final placement size**;
4. inspect dense figures as crops when needed;
5. verify labels, mathematical marks, captions, and hint references;
6. confirm no figure was enlarged or reduced unexpectedly by document conversion;
7. verify no figure crosses margins, clips, or forces accidental page-break damage;
8. verify figure text is not the only source of essential searchable content when that would harm accessibility;
9. verify the exact delivered PDF, not a pre-export surrogate.

Record figure failures separately from page-layout failures.

---

## 16. Output-package additions for visual builds

When `REQUIRED_VISUAL != NONE`, extend the recommended output package with:

```text
Figure_Manifest.md
Figure_QA.md
Figures/
  source/
  rendered/
```

Where practical, retain reproducible source files for theorem-critical diagrams.

`Figure_QA.md` should record at minimum:

- figure count;
- required/optional split;
- fidelity audit result;
- final-size legibility result;
- scale/footprint audit result;
- 200-dpi inspection result;
- any intentional `not to scale` figures;
- unresolved visual failures, which must be zero for final delivery.

---

## 17. Visualization acceptance principle

A visualization requirement is complete only when the visual survives all four layers:

1. **mathematical fidelity** — it represents the required structure correctly;
2. **pedagogical purpose** — it reduces the intended cognitive load;
3. **layout fitness** — it occupies the right amount of page space at final size;
4. **production robustness** — it survives export and 200-dpi inspection without overlap, tiny text, clipping, or false implications.

The final standard is not:

> “Did we add a picture?”

It is:

> **“Can the learner use this visual, at the size they will actually see it, to recognize or execute the intended mathematics without being misled?”**
