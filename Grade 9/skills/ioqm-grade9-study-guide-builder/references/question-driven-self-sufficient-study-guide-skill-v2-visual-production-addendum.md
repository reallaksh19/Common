# Question-Driven Study Guide Skill v2 — Visual Production Addendum

## Status and role

This is a **mandatory addendum** to `question-driven-self-sufficient-study-guide-skill-v2.md` whenever any question, chapter, bridge, appendix, quick-reference row, or short-horizon route has a non-`NONE` visual requirement.

It exists because a visual-pedagogy audit is not enough by itself. A production can correctly *identify* that diagrams would help and still generate a polished PDF in which those diagrams are missing, misplaced, unreadable, or too detached from the point of need.

The corrected rule is:

> **A visual requirement is a traceable teaching obligation, not a design suggestion.**

A final PDF may not claim `VISUAL_PEDAGOGY_GAPS = 0` merely because the source matrix contains a `required visual` column. Every required visual must exist as an asset, be placed where the learner needs it, survive final-size rendering, and pass leakage/correctness checks.

---

## 1. Failure mode this addendum prevents

The weak process is:

```text
question matrix says “visual useful”
-> prose is written
-> visual audit says “add diagrams”
-> PDF is generated
-> reviewer later notices the book is still mostly text
-> package is rebuilt
```

This is too late and too expensive.

The required process is:

```text
question / chapter creates visual obligation
-> register the obligation
-> define the visual teaching job
-> choose an exact visual form
-> create the asset before final layout
-> place it in every learner layer that needs it
-> audit the asset itself
-> generate PDF
-> inspect the rendered page at final size
-> close the obligation only after rendered QA
```

The visual pipeline therefore runs **in parallel with content authoring**, not as cosmetic polish after the book is assembled.

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

When visuals are relevant, replace the loose `required visual, if any` field with the following traceable fields:

- `visual_level` — `NONE / OPTIONAL / REQUIRED / SOURCE_REQUIRED`;
- `visual_job` — one or more teaching-job tags from Section 3;
- `visual_asset_id` — stable ID, e.g. `COMB-VIS-Q20-GAPS-01`;
- `visual_form` — graph / circle / number line / table / state diagram / construction / block schematic / micro-model / other;
- `visual_teaching_claim` — one sentence stating what the learner should see that prose hides;
- `visual_placement` — core / Worked Bridge / Appendix A / Appendix B / Appendix C / Navigator-after-diagnostic;
- `visual_leakage_risk` — `NONE / LOW / MEDIUM / HIGH`;
- `visual_status` — `PLANNED / BUILT / PLACED / RENDERED_QA_PASS`.

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
| first learner location | where it must first appear |
| reuse locations | Appendix A/B/C or Navigator if appropriate |
| leakage constraint | what the figure must not reveal |
| asset status | planned/built/placed/rendered |
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
PLACEMENT:
REUSE VARIANTS:
SOURCE / AUTHORSHIP:
```

The `MUST NOT SHOW` line is mandatory for answer-free practice visuals.

A figure whose only brief is “make this topic more visual” is under-specified.

---

## 7. Choose the right production method

Mathematical correctness outranks visual attractiveness.

### Prefer deterministic mathematical/vector construction when

- exact geometry or topology matters;
- graph adjacency/matching must be correct;
- axes, roots, intersections, intervals, or scale carry meaning;
- labels/equations must be exact;
- a state diagram must preserve exact transitions;
- a number line, residue cycle, exponent grid, table, block layout, or combinatorial configuration can be drawn directly.

Suitable approaches include programmatic/vector drawing, plotting, shape primitives, tables, or faithful reuse/reconstruction of an authoritative source figure when allowed.

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

---

## 8. One concept, several learner layers

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

## 9. Required visual placement rule

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

## 10. Visual density and page economy

Do not maximize figure count.

Use a visual when it reduces cognitive work better than another paragraph.

A small, exact schematic often has higher pedagogical value than a large decorative illustration.

Prefer:

- 1 strong figure over 4 weak ones;
- 2–4 compact panels for contrasts;
- direct labels close to the object they describe;
- whitespace around diagrams;
- short captions explaining the teaching point.

Avoid:

- screenshots of dense source pages when a clean reconstruction is possible;
- tiny multi-panel pages whose labels disappear at final size;
- repeating identical diagrams without a new retrieval/contrast purpose;
- adding visuals only to fill blank space.

---

## 11. Appendix C visual-memory requirement

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

## 12. Transfer-set visual rule

Appendix B has two distinct cases.

### Problem-essential figure

If the transfer problem is not mathematically complete without a figure, include it with the problem.

### Method-revealing figure

If the figure would reveal the hidden method, do not show it before the attempt. Place it in a method-rescue section after the mixed set, or omit it.

This distinction is essential for genuine transfer testing.

---

## 13. Pre-layout visual completeness gate

Before generating the final learner PDF, require:

```text
VISUAL_OBLIGATION_REGISTER = COMPLETE
VISUAL_REQUIRED_ASSETS = BUILT_n_OF_n
VISUAL_SOURCE_REQUIRED_ASSETS = BUILT_n_OF_n
VISUAL_ASSET_ORPHANS = 0
REQUIRED_VISUALS_WITHOUT_PLACEMENT = 0
DECORATIVE_FIGURES_COUNTED_AS_COVERAGE = 0
```

If any required asset is still merely `PLANNED`:

```text
PDF_GENERATION_ALLOWED = FALSE
STATUS = VISUAL_ASSET_BUILD_REQUIRED
```

A contact-sheet review of a text-heavy draft does not substitute for this gate.

---

## 14. Rendered visual QA

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
- visual still works in grayscale/print where relevant.

A visually attractive but mathematically ambiguous diagram fails.

---

## 15. Visual acceptance metrics

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
```

For a visual-memory quick reference, additionally record:

```text
VISUALLY_DRIVEN_CORE_FAMILIES = n
APPENDIX_C_MICROMODEL_COVERAGE = PASS_n_OF_n
```

Do not invent a denominator after seeing the final PDF. Freeze the VOR before layout.

---

## 16. Question-level self-sufficiency integration

A question with `VISUAL_REQUIRED` passes static self-sufficiency only when all of the following are true:

1. the core teaches the representation;
2. the question/Appendix has the locally necessary visual or cue;
3. the visual does not leak the answer;
4. the learner can read it at final size;
5. the required visual passed rendered QA.

Therefore:

```text
QUESTION_SUPPORT_PASS
requires
VISUAL_STATUS = RENDERED_QA_PASS
when visual_level = REQUIRED or SOURCE_REQUIRED
```

This is a hard dependency, not a cosmetic score.

---

## 17. Recommended package artifacts

When the guide has meaningful visual obligations, add:

```text
Visual_Obligation_Register.md or .csv
Visual_Manifest.md or .csv
Visual_Pedagogy_Audit.md
visuals/
```

The Visual Manifest should record at minimum:

- asset ID;
- filename/source;
- teaching job;
- question/skill mapping;
- page/location after PDF generation;
- final-size QA status.

This makes future revisions auditable and prevents a layout rebuild from silently dropping figures.

---

## 18. Production principle

The governing rule is:

> **Do not ask “Does this book have enough pictures?” Ask “Which invisible mathematical structures must become visible for this learner, and can I prove each required visual survived into the delivered PDF?”**

The visual system is complete only when every required representation can be traced from:

**question/skill -> visual obligation -> asset -> placement -> rendered page -> QA pass.**
