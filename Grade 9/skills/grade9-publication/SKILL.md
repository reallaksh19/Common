---
name: grade9-publication
description: Reconstruct and publish source-grounded Grade 9-11 educational PDFs without replacing core source content. Use for publisher-grade layout revamps, zero-loss reconstruction, teacher-value additions, missing-figure recovery, math/science typography, automatic renumbering and cross-reference preservation, benchmarked page design, render-first QA, and anti-drift audits.
---

# Grade 9 Publication

Use this skill when a source PDF or existing educational book must be **reconstructed as a stronger publication while preserving its core content**.

The governing rule is:

> **Add value around the source. Do not replace the source.**

A publication rebuild may change orientation, page count, page breaks, grids, typography, diagrams, figure placement, exercise grouping, navigation, and visible numbering. It must not silently delete, rewrite, simplify away, correct, or substitute the source's core instructional data.

This skill is deliberately stricter than ordinary PDF cleanup. It combines source preservation, teacher judgement, editorial design, diagram reconstruction, stable-link architecture, benchmarked layout, and release auditing.

## When to use this skill

Use `$grade9-publication` when the user asks to:

- rebuild or republish a supplied PDF;
- make a book look like a professional Grade 9-11 textbook;
- preserve 100% of core source data while redesigning layout;
- add diagrams, concept summaries, teacher prompts, misconceptions, or visual bridges without replacing original content;
- reduce accidental whitespace or dense auto-flow;
- repair mathematical subscripts, superscripts, fractions, symbols, units, graph labels, or science notation;
- renumber lessons/figures/questions after repagination while keeping every citation and internal relationship correct;
- benchmark a layout against reputable educational publishers/sites without copying them;
- certify source-to-publication completeness.

Use `grade9-textbook-publisher` instead when the source of truth is already canonical structured master data and the task is mainly product generation. Use `grade9-publication` when the **existing publication/source PDF itself must be reconstructed and reconciled**.

## Non-negotiable publication contract

1. **The original source is immutable.** Never overwrite the only source copy.
2. **Core data is preserved before layout begins.** Extraction and mapping precede redesign.
3. **Value-add is additive.** Added teaching aids must be distinguishable from source-derived content in the audit model.
4. **No silent editorial correction.** Suspected source errors are flagged, not quietly changed.
5. **Stable IDs survive repagination.** Visible section/page/figure numbers are generated labels, never canonical identity.
6. **Intentional absence is data.** If the source deliberately withholds a diagram so the learner must draw it, preserve that instructional choice.
7. **A technically present but hidden item counts as lost.** Covered, clipped, off-page, microscopic, or unreadable content fails preservation.
8. **Professional layout is not auto-flow.** Do not pour extracted text into generic columns and call it reconstruction.
9. **Benchmark principles, do not clone copyrighted designs.** Learn hierarchy, density, pacing, figure integration, practice rhythm, and accessibility from reputable references.
10. **Do not declare success from page count or visual resemblance alone.** Release requires deterministic source, linkage, rendering, and pedagogical audits.

## Content classes

Classify every item before redesign.

### CORE_SOURCE
Must survive semantically and, where wording matters, textually.

Examples:

- headings and section meaning;
- explanatory paragraphs;
- equations and derivations;
- numerical values and units;
- question wording;
- hints and worked solutions;
- concept IDs, question IDs, difficulty/source tags;
- graph data, labels, relationships, arrows, table values;
- source citations and hyperlinks;
- pedagogical instructions such as `NO DIAGRAM PROVIDED`;
- stated misconceptions and model limits.

### PRESENTATION_SOURCE
May be redesigned while preserving function and meaning.

Examples:

- exact coordinates;
- landscape versus portrait;
- box dimensions;
- colors that do not encode meaning;
- page breaks;
- decorative rules;
- card shapes;
- visible numbering.

### VALUE_ADD
New instructional support that does not replace core source data.

Examples:

- concept synthesis map;
- carefully reconstructed missing/explanatory figure;
- representation bridge;
- prediction prompt;
- compact prerequisite reminder;
- teacher note;
- retrieval check;
- glossary cue;
- visual comparison table.

Every value addition must have a reason: `clarify`, `connect`, `diagnose`, `practice`, `navigate`, or `reduce_cognitive_load`.

### EDITORIAL_CHANGE
A change to source meaning, wording, data, answer, scope, or scientific claim.

Do not perform silently. Record as `REVIEW_REQUIRED` unless the user explicitly approves it.

## Required output artifacts

A serious reconstruction should produce at least:

1. rebuilt publication PDF;
2. source-to-publication audit manifest (CSV or JSON);
3. cross-reference/link audit;
4. figure/diagram inventory;
5. render QA report or contact sheet;
6. exception log for any unresolved source ambiguity or editorial change.

For large books, also produce a page/section migration map.

When the project separates learner and publisher functions, treat these as distinct outputs:

- **Student Core PDF** - teaching, equations, representations, worked/guided practice and independent transfer;
- **Self-Check PDF** - retrieval and self-check items;
- **Audit PDF / manifest** - provenance, source-focus records, mapping, QA counters and exceptions.

## End-to-end methodology

### Phase 0 — Freeze the brief

Write a one-paragraph publication contract before editing:

- audience and grade band;
- source authority;
- allowed value-add;
- forbidden changes;
- benchmark references;
- output format;
- required preservation level;
- whether page count may change.

**Anti-drift checkpoint AD0 — Brief lock**

Before proceeding, answer:

- Am I reconstructing or rewriting?
- Is the source still the authority?
- What exactly may I add?
- What exactly may I not change?

If these answers cannot be stated clearly, stop and clarify.

### Phase 1 — Source preflight

Create an immutable source copy and record:

- filename and checksum if available;
- page count and page dimensions;
- text/image/vector availability;
- embedded fonts and likely substitutions;
- hyperlinks, bookmarks, annotations;
- scan/image pages versus searchable pages;
- obvious clipping/collision/glyph defects.

Render representative pages before redesign. For long books, sample every template family plus known problem pages.

**AD1 — Source freeze**

No layout work starts until the source is separately preserved and its page count is known.

### Phase 2 — Build the source obligation ledger

Segment the source into stable units. Prefer existing IDs such as `M4A-C5`, `EX-M4A-01`, question IDs, lesson IDs, or figure IDs. If none exist, assign immutable source IDs such as:

- `SRC-P012-TXT-003`
- `SRC-P012-EQN-001`
- `SRC-P012-FIG-002`
- `SRC-P012-LINK-001`

For each unit record:

- source ID;
- source page/range;
- type;
- exact/raw content or locator;
- semantic summary;
- numbers/units;
- source relationships;
- intended learner function;
- preservation class;
- reconstruction target(s);
- status.

Recommended source status values:

- `PRESERVED`
- `RECOMPOSED`
- `MERGED`
- `SPLIT`
- `INTENTIONALLY_ABSENT`
- `REVIEW_REQUIRED`

Do not use `OMITTED` for a core item in a zero-loss build.

**AD2 — Coverage denominator lock**

Freeze the number of core source units before design. The denominator must not shrink later because an item became inconvenient to place.

### Phase 3 — Build the relationship graph

Create links using stable source IDs, not page numbers.

Examples:

```text
QUESTION EX-M4A-01
  -> concept M4A-C5
  -> hint H1
  -> solution SOL-M4A-01
  -> source URL
```

Track:

- section-to-section citations;
- concept links;
- question-to-solution links;
- figure callouts;
- appendix references;
- source URLs;
- prerequisite references;
- return links.

Visible labels such as `Section 4.2`, `Figure 6`, or `p. 37` are generated only after pagination.

**AD3 — Identity check**

If a cross-reference points to a visible page number instead of a stable target ID, redesign the reference before continuing.

### Phase 4 — Teacher-value analysis

Review each subtopic as a teacher, not just a designer.

Ask:

1. What is the big idea?
2. Which representation best explains it: words, motion strip, graph, equation, table, timeline, particle model, geometry, or worked example?
3. What misconception is likely?
4. Where does the learner need prediction before calculation?
5. Which source ideas are currently separated but should be visually connected?
6. Which blank area is intentional working space and which is accidental whitespace?
7. Is a missing figure genuinely missing, or intentionally omitted?

Add only support that improves comprehension or navigation without displacing source meaning.

**AD4 — Additive-value test**

For every new object, complete the sentence:

> “This is added because it helps the learner ________, while the original source content remains ________.”

If the addition replaces, paraphrases away, or hides the source, reject it.

### Phase 5 — Benchmark before designing

Benchmark patterns from reputable Grade 9-11 learning systems. Suitable categories include:

- professional textbook page hierarchy and exercise rhythm;
- worked-example anatomy;
- concept-to-practice progression;
- misconception handling;
- learning objectives and retrieval checks;
- diagram integration;
- density and reading comfort.

Benchmark **principles**, not exact visual assets.

Score the intended design out of 100:

- conceptual clarity — 15;
- figure/diagram quality — 15;
- learning sequence — 10;
- worked-example quality — 10;
- practice progression — 15;
- misconception treatment — 8;
- mathematical/scientific typography — 8;
- page hierarchy/readability — 8;
- retrieval/assessment — 6;
- cross-link/revision value — 5.

Target at least 85 before scaling the style to a full book.

**AD5 — Prototype gate**

Do not redesign dozens of pages before 6-8 representative pages prove the visual system. A prototype should include at least a lesson opener, concept/figure page, derivation or explanation page, worked example, misconception page, and practice/review page.

### Phase 6 — Design the publication system

Define before page production:

- trim/page size and orientation;
- margins and safe zones;
- baseline grid;
- column families (single, asymmetric, practice columns, full-width figure);
- type families and exact hierarchy;
- equation style;
- figure label style;
- callout vocabulary;
- header/footer and navigation system;
- page-density target;
- accessibility/readability minimums.

For ordinary learning pages, aim for roughly 70-85% **meaningful occupancy**, where meaningful occupancy includes diagrams, working space, retrieval prompts, and annotation zones. Do not fill space merely to hit a percentage.

Avoid:

- repeated 50/50 columns regardless of content;
- giant decorative headers;
- tiny body text used to save pages;
- large empty lower halves caused by forced breaks;
- a separate rounded card for every idea;
- visually equal emphasis for primary and secondary content;
- decorative graphics that teach nothing.

**AD6 — Layout-system check**

Before adding more pages, verify that at least three different content types can be composed successfully with the same design system without forcing them into identical geometry.

### Phase 7 — Reconstruct mathematics and science notation

Treat equations as semantic objects, not plain text strings.

Preserve raw source representation separately from published notation.

Examples:

```text
source: s_(n+2) - s_n = 2a
published: s_{n+2} - s_n = 2a
```

```text
source: t0 = sqrt(t1 t2)
published: t_0 = √(t_1 t_2)
```

Audit:

- subscripts;
- superscripts;
- fractions;
- radicals;
- Greek symbols;
- vectors;
- signs;
- units;
- chemical formulae/charges where relevant;
- equation alignment;
- graph axis notation.

Do not treat a typographic normalization as permission to alter the underlying formula.

### Phase 8 — Figure policy and reconstruction

Classify each figure need:

- `PRESERVE` — source figure is correct and usable;
- `REDRAW` — same information, cleaner vector execution;
- `RECONSTRUCT` — figure is absent/corrupt but evidence is sufficient;
- `SUPPORT_ADD` — new explanatory figure that adds value;
- `INTENTIONALLY_ABSENT` — learner is expected to construct it.

For `RECONSTRUCT`, use evidence in this order:

1. source page text;
2. source solution/answer;
3. neighbouring source concept pages;
4. established visual grammar elsewhere in the same book;
5. outside verification only when the user allows it.

Record a figure semantic manifest, e.g. axes, values, arrows, regions, labels, and relationships. A pretty redraw that changes these fails.

**AD7 — Figure evidence gate**

Never invent a source figure because a page “looks empty.” If evidence is insufficient, mark `REVIEW_REQUIRED`.

### Phase 9 — Compose by learning sequence, not old coordinates

Zero loss does **not** mean preserving old coordinates or old page boundaries.

Use the source learning sequence and relationships to compose coherent spreads. Keep core wording/data present, but allow related units to merge onto a page or split across pages.

A strong sequence often resembles:

```text
orient/context
-> core idea
-> representation
-> derivation/explanation
-> worked reasoning
-> misconception/model limit
-> guided practice
-> independent/transfer practice
-> retrieval/review
```

Do not compress away source content to achieve this sequence.

**AD8 — No-rewrite check**

At the end of each subtopic, compare the publication against the source ledger. Every core unit must have a target. Teacher-added synthesis may sit between source units but cannot stand in for them.

### Phase 10 — Automatic renumbering and link resolution

Keep two identities:

- immutable source ID;
- generated publication label.

Example:

```text
source target: M4B-C8
publication label after layout: Section 4.2.7, page 19
```

When pagination changes, regenerate:

- section numbers;
- figure/table numbers;
- worked-example numbers;
- question/solution numbers;
- TOC;
- bookmarks;
- page references;
- internal links and return links.

Never manually hard-code a page number into source linkage when a target ID can be used.

**AD9 — Link closure gate**

Required counters:

```text
references_discovered = references_resolved
broken_references = 0
ambiguous_references = 0
orphan_targets = 0
duplicate_publication_ids = 0
```

### Phase 11 — Four-way reconciliation

Audit four layers:

```text
SOURCE PDF
  -> EXTRACTED SOURCE MODEL
  -> PUBLICATION MODEL
  -> FINAL PDF
```

Check each transition separately.

#### Source PDF -> extracted model
Did extraction miss text, numbers, equations, graphics, links, or instructions?

#### Extracted model -> publication model
Did reorganization delete, replace, or alter core content?

#### Publication model -> final PDF
Did rendering hide, clip, shrink, substitute, or overflow anything?

#### Source PDF -> final PDF
Does the finished artifact still carry the complete source obligation set?

**AD10 — Denominator reconciliation**

The frozen core-source count from AD2 must equal the mapped/preserved count, with zero unexplained omissions.

### Phase 12 — Render-first visual QA

Render every final page to images. Inspect at normal reading size and at 100% zoom.

Check:

- clipping and overlap;
- equation glyphs;
- figure labels;
- line lengths and leading;
- page rhythm;
- accidental whitespace;
- crowded regions;
- visible hierarchy;
- repeated templates becoming monotonous;
- orphan headings;
- awkward page breaks;
- unreadably small metadata;
- hidden answer/result lines;
- blank areas that are neither pedagogical nor compositional.

Run a contact-sheet/montage scan for global rhythm, then inspect dense/problem pages individually.

### Phase 13 — Student-page QA and artifact separation

Read `references/student-page-qa.md` and apply the following hard gates to every student-facing batch.

**AD11 — ARTIFACT SEPARATION**

Keep Student Core, Self-Check, and Audit/provenance functions in separate outputs when that is the project contract. Student Core must not carry publisher/audit notices merely to prove completeness.

**AD12 — SCAFFOLD FIDELITY**

The visual support must fade with the learning stage:

- concept/worked/full-support guided -> operative relation + representation visible;
- faded guided -> partial scaffold, not a complete solution;
- independent transfer -> no formula prompt when the source intentionally withholds it; give only task-shaped neutral workspace.

**AD13 — MODEL VISIBILITY**

On a quantitative worked or full-support guided page, the operative relation must be visible on that page or on an intentionally simultaneous facing spread. Prose/hints must not substitute for the equation.

**AD14 — STUDENT-AUDIENCE PURITY**

Student Core must contain zero process language such as `source mapping`, `audit`, `publication`, `reconstruction`, `QA`, `provenance`, or `moved to another PDF`. Put those in the Audit PDF.

**AD15 — TASK-SPECIFIC WORKSPACE**

A work zone must match the actual cognitive task. Prefer prompts such as `mark start and finish`, `separate distance and displacement`, `fill the two numerators`, `draw velocity arrows`, or `inspect the final partial cycle` over generic `facts / reasoning / answer` boxes.

**AD16 — ZERO TEXT COLLISION**

Run `scripts/check_text_overlaps.py` on every final PDF. Material cross-line text overlaps must be zero before release. Re-render after every collision repair.

**AD17 — COMPONENT BOUNDS CONTRACT**

Every reusable diagram/card/component must have declared width and height and render all labels, arrows, equations, captions and notes inside that rectangle. Use `reserve -> draw -> advance`; never continue text from a guessed y-coordinate after a fixed-height component.

**AD18 — COMPONENT CONTENT BUDGET**

Before drawing a bounded component, calculate whether its text/equations fit. Wrap text, fit equation size to available width, reserve vertical lines, and repaginate when necessary. Never truncate a core equation or sentence to make it fit.

**AD19 — FORMULA LINE COMPLETENESS**

Every displayed equation and calculation line must be complete and readable as one mathematical statement. Fail if the right-hand side is clipped, a numerator/denominator separates incorrectly, sub/superscripts collide, or an expression ends as an incomplete fragment such as `use 2v1...`.

**AD20 — NORMAL-VIEW READABILITY**

Inspect renders at normal student viewing size and at 100% zoom. Main question, operative equation and essential diagram must remain identifiable without zoom. Large blank areas must be purposeful work space, not accidental voids.

### Required render/preflight sequence for every batch

1. Render every page to images.
2. Run `scripts/check_text_overlaps.py`.
3. Verify component bounds/content budgets.
4. Scan a contact sheet for page rhythm and density.
5. Inspect every quantitative page for complete formula lines.
6. Inspect every guided/independent page for scaffold fidelity.
7. Confirm Student Core/Self-Check/Audit separation.
8. Repair, re-render and repeat until all gates pass.

## Grade-band layout calibration

Do not use identical density for Grades 9, 10, and 11.

### Grade 9

Prefer more concrete representation, larger diagrams, shorter explanatory chunks, explicit vocabulary, prediction prompts, and guided representation.

### Grade 10

Balance visual and algebraic reasoning, representation conversion, graph interpretation, and more independent application.

### Grade 11

Allow denser formal notation, derivations, model assumptions, compact diagrams, and more independent multi-step problems while retaining readable hierarchy.

These are calibration principles, not quotas.

## Required zero-loss audit

A final report should account for at least:

- source pages;
- source core units;
- mapped core units;
- unmapped units;
- equations detected/matched;
- numerical/unit tokens matched;
- figures preserved/redrawn/reconstructed;
- intentional figure omissions preserved;
- internal references resolved;
- external source links preserved;
- editorial exceptions;
- clipping/overflow/hidden-content findings;
- text-overlap findings;
- component-bounds escapes;
- incomplete or clipped formula lines.

Release requires:

```text
unmapped_core_units = 0
unapproved_editorial_changes = 0
broken_internal_references = 0
unresolved_source_links = 0
hidden_or_clipped_core_content = 0
text_overlap_findings = 0
component_bounds_escape_findings = 0
critical_equation_collision_findings = 0
```

If any counter is non-zero, report `NOT READY FOR PUBLICATION`.

## Anti-drift checklist

Run this short checklist after every major batch (normally every 5-10 pages or one subtopic):

1. **Source authority:** Am I still reconstructing the supplied source rather than writing my own book?
2. **Core denominator:** Has any core item disappeared from the ledger?
3. **Value-add boundary:** Are new teaching objects clearly additive?
4. **No silent correction:** Did I change any fact, number, answer, or claim without approval?
5. **Stable linkage:** Are references still target-ID based rather than page-number based?
6. **Figure evidence:** Did I invent any diagram unsupported by source or approved research?
7. **Typography:** Are equations/units/symbols semantically unchanged and visually correct?
8. **Layout quality:** Am I designing pages, or merely auto-flowing extracted text?
9. **Density:** Are white spaces intentional and useful rather than accidental?
10. **Readability:** Is body text comfortably readable without zoom?
11. **Benchmark:** Does the page meet the approved prototype standard?
12. **Render check:** Did I inspect the actual rendered PDF, not only source code/layout objects?
13. **Artifact separation:** Is publisher/audit language absent from Student Core?
14. **Scaffold fidelity:** Does support visibly fade from guided to independent work?
15. **Formula completeness:** Are all displayed relations complete and unclipped?
16. **Collision gate:** Are automated overlap and component-bounds counters zero?

Any `NO` answer stops the batch until repaired.

## Common drift patterns to reject

- “It contains all the text, so it is complete.”
- “The page count matches, so nothing was lost.”
- “I fixed the font and collisions, so it is reconstructed.”
- “I copied the old layout because preserving content means preserving coordinates.”
- “I condensed three source explanations into my own summary.”
- “The blank area looked ugly, so I inserted a diagram.”
- “The equation is probably wrong, so I corrected it silently.”
- “The source says draw your own diagram, but I added the answer diagram.”
- “I reduced text to 7 pt to avoid another page.”
- “The link text is visible, so the hyperlink must be fine.”
- “A professional benchmark means visually cloning that publisher.”
- “The formula begins in the box, so it must fit.”
- “The PDF opens, so overlapping text is acceptable.”

## Deterministic manifest check

When a JSON publication manifest is available, run:

```text
python scripts/check_publication_manifest.py manifest.json
python scripts/check_text_overlaps.py final.pdf
```

Read `references/publication-playbook.md` for the novice-agent operational playbook, `references/student-page-qa.md` for student-facing page gates, and `references/audit-manifest-spec.md` for the recommended audit schema.

## Completion statement

Do not say “publisher-ready” or “100% reconstructed” unless the deterministic and visual gates pass. Prefer precise status language such as:

- `SOURCE MAPPING COMPLETE; VISUAL QA PENDING`
- `LAYOUT PROTOTYPE APPROVED; FULL RECONSTRUCTION NOT YET CERTIFIED`
- `CORE DATA RECONCILIATION 100%; LINK/RENDER QA PASS`
- `NOT READY: 3 UNMAPPED SOURCE UNITS`
