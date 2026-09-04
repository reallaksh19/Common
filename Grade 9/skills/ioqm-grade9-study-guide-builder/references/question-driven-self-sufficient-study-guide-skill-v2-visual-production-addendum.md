# Question-Driven Study Guide Skill v2 — Visual Production Addendum

## Status and role

This is a **mandatory addendum** to `question-driven-self-sufficient-study-guide-skill-v2.md` whenever any question, chapter, bridge, appendix, quick-reference row, or short-horizon route has a non-`NONE` visual requirement.

It exists because a visual-pedagogy audit is not enough by itself. A production can correctly *identify* that diagrams would help and still generate a polished PDF in which those diagrams are missing, misplaced, mathematically wrong, unreadable, oversized, too text-heavy, or detached from the point of need.

The corrected rule is:

> **A visual requirement is a traceable teaching obligation with a final physical size, not a design suggestion.**

A final PDF may not claim `VISUAL_PEDAGOGY_GAPS = 0` merely because the source matrix contains a `required visual` column. Every required visual must exist as an asset, preserve the required mathematics, be placed where the learner needs it, fit the page at the intended size, survive final-size rendering, and pass leakage/correctness checks.

The core traceability rule is:

> **visual requirement -> obligation -> brief -> asset -> final-size placement -> rendered page -> QA pass**

---

## 1. Failure mode this addendum prevents

The weak process is:

```text
question matrix says “visual useful”
-> prose is written
-> visual audit says “add diagrams”
-> figures are generated at arbitrary canvas size
-> document inserts them at maximum width
-> PDF is generated
-> diagrams look oversized / labels overlap / text shrinks
-> reviewer notices the visual system still does not teach well
-> package is rebuilt
```

This is too late and too expensive.

A second weak process is:

```text
visual asset looks good by itself
-> asset is accepted
-> it is later shrunk to fit the PDF
-> labels/formulas become tiny
-> page-level contact sheet looks “fine”
-> learner cannot actually read or use the figure
```

The required process is:

```text
question / chapter creates visual obligation
-> register the obligation
-> define the visual teaching job
-> define mathematical MUST SHOW / MUST NOT SHOW
-> choose representation
-> specify target final footprint
-> prototype representative assets in the real document
-> export sample PDF and calibrate scale / labels / line weight
-> freeze the visual style contract
-> build remaining assets
-> place them in every learner layer that needs them
-> audit the assets themselves
-> generate final PDF
-> inspect every required visual on its rendered page at final size
-> close the obligation only after rendered QA
```

The visual pipeline therefore runs **in parallel with content authoring**, not as cosmetic polish after the book is assembled.

Late global resizing is a repair, not a production strategy.

---

## 2. Visual obligation levels

Every relevant matrix row and major teaching section must classify visual need as one of:

- `VISUAL_NONE` — prose/equations are sufficient;
- `VISUAL_OPTIONAL` — may improve fluency but is not needed for self-sufficiency;
- `VISUAL_REQUIRED` — materially lowers cognitive load, reveals the representation, preserves problem conditions, or prevents a predictable misconception;
- `VISUAL_SOURCE_REQUIRED` — the original mathematical problem depends on a supplied/authoritative figure or diagram and cannot be faithfully reconstructed from prose alone.

`VISUAL_REQUIRED` and `VISUAL_SOURCE_REQUIRED` create hard production obligations.

A decorative cover image, icon, border, or aesthetic illustration never satisfies one of these obligations.

---

## 3. Visual teaching-job taxonomy

For every required visual, state the **job** it performs. Use one or more of:

### `REPRESENTATION_UNLOCK`
Makes the hidden model visible.

Examples:
- combinatorics conflict graph;
- circular-gap model;
- divisor exponent grid;
- algebra sign/domain number line;
- geometry auxiliary construction.

### `STATE_OR_PROCESS`
Shows a transition, recurrence state, case evolution, finite difference, game state, or algorithmic sequence.

### `CASE_STRUCTURE`
Makes a case split, overlap, block merge, branch, or exact-one decomposition visible.

### `SYMMETRY_IDENTITY`
Shows which arrangements/objects are considered the same or different under rotation, reflection, relabeling, or orbit action.

### `CONSTRAINT_PRESERVATION`
Carries mathematical information that must remain visible: adjacency, incidence, equality, angle, length, order, region, position, or other problem conditions.

### `CONTRAST_OR_ANTITRIGGER`
Places nearby representations side by side so the learner can distinguish methods that are easily confused.

### `RETRIEVAL_MICROMODEL`
A tiny reusable memory picture for Appendix C / quick reference: gaps, blocks, state arrows, graph, cycle, residue loop, exponent grid, etc.

### `DECORATIVE`
Aesthetic only. `DECORATIVE` never counts toward visual-pedagogy coverage.

---

## 4. Upgrade the question-to-method matrix

When visuals are relevant, replace the loose `required visual, if any` field with traceable fields:

- `visual_level` — `NONE / OPTIONAL / REQUIRED / SOURCE_REQUIRED`;
- `visual_job` — one or more teaching-job tags from Section 3;
- `visual_asset_id` — stable ID, e.g. `COMB-VIS-Q20-GAPS-01`;
- `visual_form` — graph / circle / number line / table / state diagram / construction / block schematic / micro-model / other;
- `visual_teaching_claim` — one sentence stating what the learner should see that prose hides;
- `visual_required_facts` — mathematical relationships that must be preserved;
- `visual_forbidden_implications` — facts the sketch must not silently add;
- `visual_placement` — core / Worked Bridge / Appendix A / Appendix B / Appendix C / Navigator-after-diagnostic;
- `visual_footprint` — `S / M / L / XL` or an equivalent declared target;
- `visual_leakage_risk` — `NONE / LOW / MEDIUM / HIGH`;
- `visual_status` — `PLANNED / SPECIFIED / PROTOTYPE_PASS / BUILT / PLACED / RENDERED_QA_PASS`.

A row with `VISUAL_REQUIRED` cannot have question support status `PASS` while `visual_status` is earlier than `RENDERED_QA_PASS` for the final PDF gate.

---

## 5. Build a Visual Obligation Register before final prose freeze

Create a **Visual Obligation Register (VOR)** after the first orphan-method audit and before final layout.

Minimum columns:

| Field | Purpose |
|---|---|
| obligation ID | stable reviewer reference |
| skill/question | what creates the obligation |
| visual level | optional vs hard obligation |
| teaching job | why the visual exists |
| misconception / hidden structure | what it repairs |
| asset ID | stable visual asset reference |
| exact visual form | what will be drawn |
| required facts | mathematical facts that must survive |
| forbidden implications | facts/solution moves the figure must not add |
| first learner location | where it must first appear |
| reuse locations | Appendix A/B/C or Navigator if appropriate |
| target footprint | intended final-size class |
| asset status | planned/specified/prototyped/built/placed/rendered |
| final-size QA | pass/fail |

Do **not** wait for the complete PDF to discover which pages need diagrams.

The VOR is the authoritative denominator for visual completion.

---

## 6. Visual brief contract

Before creating a required asset, write a compact visual brief.

Template:

```text
VISUAL_ASSET_ID:
TARGET_SKILL / QUESTION:
TEACHING_JOB:
LEARNER SHOULD NOTICE:
MISCONCEPTION PREVENTED:
MUST SHOW:
MUST NOT SHOW:
NOTATION / LABELS:
REPRESENTATION:
TARGET_FOOTPRINT:
CAPTION / NEARBY TEXT:
PLACEMENT:
REUSE VARIANTS:
SOURCE / AUTHORSHIP:
```

The `MUST NOT SHOW` line is mandatory for answer-free practice visuals.

The `TARGET_FOOTPRINT` line is mandatory for every required visual in a static PDF build.

A figure whose only brief is “make this topic more visual” is under-specified.

---

## 7. Choose the representation before choosing the tool

Mathematical correctness outranks visual attractiveness.

### Prefer deterministic mathematical/vector construction when

- exact geometry or topology matters;
- graph adjacency/matching must be correct;
- axes, roots, intersections, intervals, or scale carry meaning;
- labels/equations must be exact;
- a state diagram must preserve exact transitions;
- a number line, residue cycle, exponent grid, table, block layout, or combinatorial configuration can be drawn directly.

Suitable approaches include programmatic/vector drawing, plotting, shape primitives, tables, or faithful reuse/reconstruction of an authoritative source figure when allowed.

The important property is **reproducibility of the mathematical source**, not a particular software package.

### Image generation may be used when

- the image is conceptual or illustrative rather than answer-critical;
- exact mathematical relationships are independently checked;
- the asset does not need reliable embedded text/equations;
- it is a cover/section visual or non-critical conceptual illustration.

### Do not use generative illustration as the authority for

- exact geometry conditions;
- graph edges/matching constraints;
- coordinate graphs whose intersections/roots matter;
- mathematical labels/equations;
- source-required contest figures.

If an AI-generated image is used, treat it as an illustration to verify, not mathematical evidence.

If generated text or labels are unreliable, use the generated visual only as a base and overlay mathematical notation deterministically.

---

## 8. Mathematical fidelity contract

Every theorem-critical visual must be checked against its `MUST SHOW` and `MUST NOT SHOW` brief before document placement.

### Geometry-specific checklist

Verify, as applicable:

- correct point count and exact labels;
- correct point order;
- stated collinear points are actually collinear;
- stated points lie on the required segment, line, arc, or circle;
- midpoint/ratio placement is consistent with the problem;
- right-angle, parallel, tangent, equal-length, and equal-angle marks correspond only to given/proved facts at that teaching stage;
- circle centers, radii, chords, and tangency points are correctly related;
- cyclic points lie on one circle when cyclicity is given;
- extensions are visibly extensions of the correct line;
- auxiliary constructions are not shown before the learner is supposed to discover them;
- accidental symmetry does not suggest an unstated equality;
- orientation does not contradict required point order;
- no final answer or decisive hidden construction is leaked in answer-free practice.

`NOT_TO_SCALE` permits non-proportional lengths. It does **not** permit wrong incidence, topology, or point order.

### Other domains

Apply the same principle to exact graph edges, state transitions, number-line intervals, coordinate intersections, residue cycles, block/gap structure, table values, and other mathematical constraints.

---

## 9. Final physical size and figure-footprint contract

A source canvas does not determine the learner's reading size.

A 1400-pixel image can still be unreadable if it is shrunk aggressively in the PDF, and a mathematically simple figure can still waste space if it is inserted at full text width.

Before asset production, assign a target footprint using the document's **usable body width**, not the physical page width.

Calibration defaults:

| Footprint | Typical usable-body width | Typical use |
|---|---:|---|
| `S` | 35–45% | one relation / small schematic / micro-model |
| `M` | 50–65% | ordinary theorem or recognition figure |
| `L` | 65–80% | worked figure with several labels |
| `XL` | 80–95% | dense figure where smaller placement harms legibility |

These are calibration defaults, not rigid layout laws.

Routine teaching figures should usually not consume more than roughly 30–40% of usable page-body height. Complex worked figures may use roughly 45–55%. A full-page figure should be deliberate and figure-dominant, not the side effect of an automatic `width = text_width` rule.

### Final-size label rule

Judge labels **after placement** in the PDF.

If a figure must be shrunk until labels become too small, do not keep shrinking it. Redesign the figure:

- remove non-essential in-image text;
- move explanation to document text;
- simplify the drawing;
- split it into panels;
- or intentionally assign a larger footprint.

### Raster source rule

Raster assets must have enough source pixels for their declared physical placement. Final PDF inspection still occurs at 200 dpi, but source artwork must not be marginal before insertion.

---

## 10. Separate mathematical artwork from document typography

As a default:

- keep page/chapter titles outside the image;
- keep long teacher explanations outside the image;
- keep captions outside the image unless the asset is intentionally a self-contained card;
- put only labels, short formulas, measurements, and indispensable annotations inside the figure;
- prefer document-native/typeset formulas when a rasterized formula would become small after scaling;
- do not repeat the same heading in both the page and the image;
- keep in-image wording short enough that figure scaling does not become a typography problem.

This improves accessibility, text extraction, style consistency, and scale robustness.

---

## 11. Prototype before batch visual production

Do not create the full figure set before proving that the visual system works in the real document.

### Minimum representative prototype set

When the guide has a substantial visual load, prototype at least:

1. one simple figure;
2. one label/text-dense figure;
3. one complex theorem-critical figure;
4. one Appendix A figure with local hints if the domain is diagram-heavy.

Insert the prototypes into the actual document template at their declared footprints and export a sample PDF.

Inspect:

- figure scale relative to page and prose;
- label size at final reading size;
- line weight;
- whitespace;
- page balance;
- caption spacing;
- duplicated headings;
- interaction with H1/H2/H3 strips;
- whether document conversion changes the intended size;
- whether the figure remains usable on an ordinary screen and printout.

Only after the prototype set passes should the remaining visual set be produced in bulk.

Then freeze the visual style contract: line weights, label hierarchy, accent usage, caption treatment, footprint rules, and any domain-specific conventions.

This gate prevents a late whole-book resize cycle.

---

## 12. One concept, several learner layers

A visual obligation may need different **variants**, not repeated copies of the same picture.

### Core / Worked Bridge

Use the most explanatory version: labels, arrows, contrast panels, and enough structure to teach the representation.

### Appendix A

Use a smaller local cue only when it helps recognition or preserves problem conditions. It must not reveal the solution path beyond the assigned hint depth.

### Appendix B

Do not insert a method-revealing visual before the student attempts a transfer problem unless the problem itself requires that figure. A method-only rescue visual may appear after the problem set / answer section if the design calls for it.

### Appendix C

Use a `RETRIEVAL_MICROMODEL`: tiny, low-text visual anchors for method families that are inherently spatial/structural.

### Short-horizon Navigator

Do not place method-revealing visual routers **before** unaided Quick Check scoring. Visual routing can appear afterward.

This prevents the Navigator from contaminating the diagnostic signal.

---

## 13. Required visual placement rule

For a representation-heavy method, the first useful visual should appear **at the point where the representation is introduced**, not only in a later gallery or appendix.

Bad:

```text
Chapter teaches circular gaps in prose
...
30 pages later: Visual Bridge on circular gaps
```

Good:

```text
Chapter introduces circular gaps
-> compact visual immediately
-> Worked Bridge deepens it
-> Appendix A reuses a quieter cue
-> Appendix C carries a micro-model
```

Visual Bridge pages are reinforcement/contrast tools. They do not excuse missing local visuals at the first teaching point.

---

## 14. Visual density and page economy

Do not maximize figure count and do not maximize figure size.

Use a visual when it reduces cognitive work better than another paragraph.

A small, exact schematic often has higher pedagogical value than a large decorative illustration.

Prefer:

- 1 strong figure over 4 weak ones;
- 2–4 compact panels for contrasts;
- direct labels close to the object they describe;
- whitespace around diagrams;
- short captions explaining the teaching point;
- figure size proportional to information density.

Avoid:

- screenshots of dense source pages when a clean reconstruction is possible;
- tiny multi-panel pages whose labels disappear at final size;
- making every image use maximum body width;
- repeating identical diagrams without a new retrieval/contrast purpose;
- adding visuals only to fill blank space;
- scaling a text-heavy image down after generation instead of redesigning it.

---

## 15. Appendix A visual and hint interaction

For diagram-driven practice:

- the problem statement and figure remain visually dominant;
- the figure should be compact enough to preserve the problem-set rhythm but large enough for the learner to mark/use;
- H1 may refer directly to a mark the learner should add;
- H2 points back to previously taught learning;
- H3 gives the first executable move without drawing the hidden solution for the learner;
- do not show auxiliary lines, reflection images, completed constructions, or decisive decompositions in the base figure when discovering them is the key move;
- design the figure and hint ladder together rather than writing H1 after the figure is frozen;
- if one problem cannot remain legible with local hints, enlarge only that problem or use the Hint Bank fallback instead of globally enlarging all Appendix figures.

Aim for 2–3 questions per page where the actual statement/figure complexity permits.

---

## 16. Transfer-set visual rule

Appendix B has two distinct cases.

### Problem-essential figure

If the transfer problem is not mathematically complete without a figure, include it with the problem.

### Method-revealing figure

If the figure would reveal the hidden method, do not show it before the attempt. Place it in a method-rescue section after the mixed set, or omit it.

This distinction is essential for genuine transfer testing.

---

## 17. Appendix C visual-memory requirement

If the domain contains visually driven method families, Appendix C should not remain a prose/table-only summary.

For each high-value visually driven family, ask:

> Can the learner retrieve this method faster from a 2–5 second micro-model than from another sentence?

If yes, include the micro-model.

Examples:

- combinatorics: gaps, blocks, circle identity, graph, state arrows, pigeonhole boxes;
- algebra: root/tangency sketch, sign number line, recurrence arrows, smoothing picture;
- number theory: residue cycle, exponent grid, valuation ladder;
- geometry: similarity/cyclicity/tangent mini-configuration, angle/ratio markings.

Appendix C visual completeness is audited against **method families**, not raw figure count.

---

## 18. Visual Bridge composition rules

Use thematic **Visual Bridge** pages when several related methods become clearer through a common representation.

Prefer 2–4 compact panels rather than one oversized poster.

Each panel should have:

- one visual model;
- one recognition phrase;
- one first move;
- one boundary/contrast if useful.

Keep one consistent notation/color system and short panel captions.

If one panel becomes dense enough to require long prose, promote it to an Advanced Worked Bridge rather than shrinking the whole page.

Visual Bridges should be interleaved near the relevant core chapters rather than collected as decorative plates at the end.

---

## 19. Required visual production loop

When one or more hard visual obligations exist, use this production pipeline:

```text
QUESTION-TO-METHOD MATRIX
-> MARK VISUAL OBLIGATIONS
-> BUILD / FREEZE VOR DENOMINATOR
-> WRITE VISUAL BRIEFS
-> ASSIGN STABLE ASSET IDS
-> CHOOSE REPRESENTATION
-> SPECIFY FINAL FOOTPRINTS
-> BUILD REPRESENTATIVE PROTOTYPE SET
-> INSERT PROTOTYPES INTO REAL DOCUMENT TEMPLATE
-> EXPORT SAMPLE PDF
-> CALIBRATE SCALE / LABELS / LINE WEIGHT / PAGE BALANCE
-> FREEZE VISUAL STYLE CONTRACT
-> PRODUCE REMAINING ASSETS
-> RUN MATHEMATICAL FIDELITY AUDIT
-> PLACE AT DECLARED FOOTPRINTS
-> RUN FIGURE-LEVEL FINAL-SIZE QA
-> RUN PAGE-LEVEL 200-DPI QA
-> REPAIR SOURCE FIGURES OR LAYOUT AS APPROPRIATE
-> RE-RENDER AFFECTED PAGES
-> FINAL VISUAL PASS
```

### Repair classification

If a figure fails because of geometry, labels, topology, omitted conditions, answer leakage, or internal clutter, repair the **asset source**.

If the asset is correct but fails because of page placement, scaling, spacing, or a page break, repair the **document layout**.

Do not use placement changes to hide an asset-content defect, and do not redraw a correct asset when the failure is only layout.

---

## 20. Pre-layout and pre-PDF visual gates

Before generating the final learner PDF, require:

```text
VISUAL_OBLIGATION_REGISTER = COMPLETE
VISUAL_REQUIRED_ASSETS = BUILT_n_OF_n
VISUAL_SOURCE_REQUIRED_ASSETS = BUILT_n_OF_n
VISUAL_ASSET_ORPHANS = 0
REQUIRED_VISUALS_WITHOUT_PLACEMENT = 0
DECORATIVE_FIGURES_COUNTED_AS_COVERAGE = 0
REQUIRED_VISUAL_FOOTPRINTS_SPECIFIED = PASS_n_OF_n
REPRESENTATIVE_VISUAL_PROTOTYPE = PASS
```

If any required asset is still merely `PLANNED` or `SPECIFIED`:

```text
PDF_GENERATION_ALLOWED = FALSE
STATUS = VISUAL_ASSET_BUILD_REQUIRED
```

If the prototype/calibration set fails:

```text
FULL_VISUAL_BATCH_ALLOWED = FALSE
STATUS = VISUAL_STYLE_CALIBRATION_REQUIRED
```

Before the normal hard PDF gate, additionally require:

```text
VISUAL_REQUIRED_FACTS_PRESERVED = PASS_n_OF_n
VISUAL_FORBIDDEN_IMPLICATIONS = 0
ANSWER_FREE_VISUAL_LEAKAGE = 0
VISUAL_FINAL_SIZE_LEGIBILITY = PASS_n_OF_n
VISUAL_SCALE_BUDGET = PASS_n_OF_n
VISUAL_HINT_INTERACTION = PASS_n_OF_n_WHERE_APPLICABLE
VISUAL_SOURCE_REPRODUCIBILITY = PASS_n_OF_n_FOR_THEOREM_CRITICAL_ASSETS
```

For Geometry, additionally require:

```text
THEOREM_CRITICAL_FIGURE_FIDELITY = PASS_n_OF_n
```

A contact-sheet review of a text-heavy draft does not substitute for these gates.

---

## 21. Rendered visual QA

After PDF generation, render **every page at 200 dpi** as required by the parent skill.

Use contact sheets for whole-book scanning, but do not stop there.

Every required/critical visual must also be inspected on its actual rendered page at final reading size.

Check:

- mathematical correctness;
- all required relationships/edges/regions/labels present;
- no accidental relationship introduced by the drawing;
- text/labels readable at final size;
- adequate contrast;
- no crop, overlap, clipping, or broken glyph;
- figure appears close enough to the teaching text/question;
- caption/nearby sentence states the intended teaching point;
- no answer leakage beyond the allowed hint depth;
- source-required figure preserves the source condition;
- visual still works in grayscale/print where relevant;
- conversion did not enlarge/shrink the asset unexpectedly;
- page heading is not redundantly embedded inside the figure;
- dense figures are inspected as crops when whole-page viewing is insufficient.

A visually attractive but mathematically ambiguous diagram fails.

Record figure-content failures separately from page-layout failures.

---

## 22. Visual acceptance metrics

Use counts only against the explicit VOR denominator.

Recommended gates:

```text
VISUAL_OBLIGATIONS = PASS_n_OF_n
VISUAL_REQUIRED_ASSETS = PASS_n_OF_n
VISUAL_PLACEMENT = PASS_n_OF_n
CRITICAL_VISUAL_FINAL_SIZE_QA = PASS_n_OF_n
SOURCE_REQUIRED_FIGURE_CUSTODY = PASS_n_OF_n
ANSWER_FREE_VISUAL_LEAKAGE = 0
BROKEN_OR_MISSING_FIGURES = 0
VISUAL_ASSET_ORPHANS = 0
DECORATIVE_FIGURES_COUNTED_AS_COVERAGE = 0
VISUAL_SCALE_BUDGET = PASS_n_OF_n
VISUAL_FOOTPRINT_DRIFT = 0
```

For a visual-memory quick reference, additionally record:

```text
VISUALLY_DRIVEN_CORE_FAMILIES = n
APPENDIX_C_MICROMODEL_COVERAGE = PASS_n_OF_n
```

Do not invent a denominator after seeing the final PDF. Freeze the VOR before layout.

---

## 23. Question-level self-sufficiency integration

A question with `VISUAL_REQUIRED` passes static self-sufficiency only when all of the following are true:

1. the core teaches the representation;
2. the question/Appendix has the locally necessary visual or cue;
3. the visual preserves all required mathematical facts;
4. the visual does not leak the answer;
5. the learner can read/use it at final size;
6. the figure/hint interaction matches the assigned hint depth;
7. the required visual passed rendered QA.

Therefore:

```text
QUESTION_SUPPORT_PASS
requires
VISUAL_STATUS = RENDERED_QA_PASS
when visual_level = REQUIRED or SOURCE_REQUIRED
```

This is a hard dependency, not a cosmetic score.

---

## 24. Recommended package artifacts

When the guide has meaningful visual obligations, add:

```text
Visual_Obligation_Register.md or .csv
Visual_Manifest.md or .csv
Visual_Pedagogy_Audit.md
Figure_QA.md
visuals/
  source/
  rendered/
```

The Visual Manifest should record at minimum:

- asset ID;
- filename/source;
- teaching job;
- question/skill mapping;
- required facts / forbidden implications;
- target footprint;
- page/location after PDF generation;
- final-size QA status.

`Figure_QA.md` should record at minimum:

- required and optional asset counts;
- prototype/calibration result;
- mathematical fidelity result;
- scale/footprint result;
- final-size legibility result;
- 200-dpi page/crop inspection result;
- intentional `not to scale` assets;
- unresolved visual failures, which must be zero for final delivery.

This makes future revisions auditable and prevents a layout rebuild from silently dropping or rescaling figures.

---

## 25. Production principle

The governing rule is:

> **Do not ask “Does this book have enough pictures?” Ask “Which invisible mathematical structures must become visible for this learner, at what final size, and can I prove each required visual survived into the delivered PDF without misleading them?”**

The visual system is complete only when every required representation can be traced from:

**question/skill -> visual obligation -> brief -> asset -> declared footprint -> placement -> rendered page -> QA pass.**

The final standard is not:

> “Did we add a picture?”

It is:

> **“Can the learner use this visual, at the size they will actually see it, to recognize or execute the intended mathematics without being misled?”**
