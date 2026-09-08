# Publication Playbook — Novice-Agent Operating Manual

This playbook explains how to use `grade9-publication` when reconstructing an educational PDF or book while preserving the source and adding teacher/publisher value.

The intended operator may be a novice agent. Follow the sequence exactly. Do not skip to page design before the source ledger exists.

---

## 1. Mental model

Think of the publication as four separate layers:

```text
A. ORIGINAL SOURCE
B. SOURCE MODEL
C. PUBLICATION MODEL
D. FINAL RENDERED PDF
```

Never collapse these into one object.

- The **original source** proves what was supplied.
- The **source model** records every obligation.
- The **publication model** decides how those obligations are arranged and what additive teaching support is introduced.
- The **final PDF** is only the rendered delivery format.

If you edit the final PDF without maintaining B and C, zero-loss reconstruction becomes difficult to prove.

---

## 2. First 15 minutes: exact novice procedure

When a PDF arrives:

1. Save or identify the immutable source file.
2. Record page count and dimensions.
3. Render at least:
   - first page;
   - one concept page;
   - one equation-heavy page;
   - one diagram-heavy page;
   - one practice page;
   - one solution/review page;
   - known problem pages if supplied by the user.
4. Extract/search the source text.
5. Identify existing IDs, headings, subtopics, figures, question IDs, source links, and solutions.
6. Write the publication brief in plain language.
7. Build the source obligation ledger.
8. Only then design 6-8 representative prototype pages.

Do **not** begin by choosing fonts, drawing cards, or converting orientation.

---

## 3. Write the publication brief

Use this template:

```text
PUBLICATION BRIEF
Audience:
Subject / grade:
Source authority:
Core-content preservation requirement:
Allowed additions:
Forbidden changes:
Benchmark references:
Output orientation / size if fixed:
May pagination change? YES / NO
May section numbering change? YES / NO
May wording change? YES / NO / APPROVAL ONLY
External research allowed? YES / NO
Release requirement:
```

Example:

```text
Audience: Grade 9 Physics students
Source authority: uploaded Motion PDF
Core preservation: 100% of explanatory text, equations, questions, hints,
solutions, IDs, links and diagram meaning
Allowed additions: teacher-value diagrams, synthesis maps, prediction prompts,
layout/typography improvements
Forbidden changes: silent factual/answer rewrites, deletion, replacing source
explanation with a shorter new explanation
Pagination: may change
Renumbering: generated automatically
External research: benchmark layout only; source remains content authority
Release: zero unmapped core units + zero broken links + render QA pass
```

### Anti-drift question

Ask: **If the finished book were stripped of every teacher-added object, would all source obligations still be present?**

If not, the rebuild is replacing the source.

---

## 4. Build the source obligation ledger

### 4.1 What counts as a source unit?

Create a unit whenever an item could be lost independently.

Examples:

- section heading;
- paragraph or discrete explanation;
- equation or derivation step;
- diagram and each meaningful label if required;
- table;
- question;
- hint;
- answer/solution;
- misconception statement;
- model caveat;
- footnote;
- external source link;
- internal reference;
- instruction such as `draw your own graph`;
- curriculum/source tag.

Avoid making each word a unit. Use pedagogically meaningful blocks.

### 4.2 Minimum fields

Recommended CSV columns:

```text
source_id
source_page
source_range
type
preservation_class
raw_text_or_locator
semantic_summary
numbers_units
relationships
learner_function
publication_target
status
notes
```

### 4.3 Stable ID policy

Use source-native IDs when available.

Good:

```text
M4A-C5
EX-M4A-01
Q17
FIG-M4B-AREA
```

If source-native IDs do not exist:

```text
SRC-P003-TXT-01
SRC-P003-EQN-01
SRC-P003-FIG-01
SRC-P003-LINK-01
```

Never make a page number the only identity. Pages can move.

### 4.4 Freeze the denominator

At the end of extraction, record:

```text
core_source_units = N
```

This number is frozen. It cannot decrease because the layout became difficult.

If later analysis discovers genuinely new source units, increase the denominator and record why.

---

## 5. Separate preservation from interpretation

A novice agent often makes this mistake:

> “I know what the author meant, so I can rewrite it more clearly.”

Do not do that automatically.

Store at least two layers where interpretation is needed:

```text
RAW SOURCE:
s_(n+2) - s_n = 2a

INTERPRETED STRUCTURE:
subscript(s,n+2) - subscript(s,n) = 2a

PUBLISHED FORM:
s_{n+2} - s_n = 2a
```

The raw source remains inspectable.

Use the same principle for diagrams, tables, units, and graph labels.

---

## 6. Build a relationship graph

The relationship graph protects the book when pages and numbers change.

### 6.1 Common relationships

```text
section -> prerequisite section
question -> concept
question -> hint
question -> solution
worked example -> concept
figure -> explanatory paragraph
misconception -> retry question
source item -> external URL
section -> next section
```

### 6.2 Canonical target rule

References should look conceptually like:

```text
<xref target="M4A-C5" />
```

not:

```text
See page 6
```

The renderer later resolves `M4A-C5` to its new visible label and page.

### 6.3 Renumbering example

Before reconstruction:

```text
M4A-C5 is source page 6.
EX-M4A-01 links to M4A-C5.
```

After reconstruction:

```text
M4A-C5 -> Lesson 4.1, section 4, new page 11.
EX-M4A-01 still targets M4A-C5.
```

Displayed text can become:

```text
See Section 4.1.4 on page 11.
```

No source relationship was broken.

---

## 7. Teacher-value analysis

Publication value is not merely decoration.

For each subtopic, complete this worksheet:

```text
BIG IDEA:
SOURCE EXPLANATION THAT MUST REMAIN:
BEST REPRESENTATION:
COMMON MISCONCEPTION:
MODEL LIMIT / CONDITION:
PREDICT-BEFORE-CALCULATE OPPORTUNITY:
WORKED REASONING OPPORTUNITY:
RETRIEVAL QUESTION:
TRANSFER QUESTION:
MISSING OR WEAK FIGURE?:
IS THE FIGURE INTENTIONALLY OMITTED?:
```

### 7.1 Allowed teacher-value patterns

#### A. Concept synthesis map

Purpose: connect source facts already present in different places.

Example:

```text
equal Δv in equal Δt
        ↓
constant acceleration
        ↓
straight v-t slope
        ↓
v = u + at
```

Do not delete the source explanations because the map exists.

#### B. Representation bridge

Put equivalent source meaning side by side:

```text
WORDS | MOTION STRIP | GRAPH | EQUATION
```

This is especially useful in Physics and Mathematics.

#### C. Prediction prompt

Before calculation:

```text
Should the answer increase or decrease?
Should displacement exceed ut?
What sign should acceleration have?
```

#### D. Common-error repair

Use:

```text
COMMON ERROR
WHY IT FAILS
CORRECT MODEL
TRY AGAIN
```

#### E. Retrieval check

Use one short question after a major idea, not a giant review box after every paragraph.

### 7.2 Value-add boundary

Every new object is logged as `VALUE_ADD` and must point to the source IDs it supports.

Example:

```text
VA-M4B-01
supports: M4B-C2, M4B-C3, M4B-C4
purpose: connect rectangle+triangle derivation visually
```

If a value-add has no supported source ID, ask whether it belongs in this source-grounded edition.

---

## 8. Missing-figure decision tree

Do not assume an empty page area means a missing figure.

Use this decision tree:

```text
Does the source explicitly require or describe a figure?
  YES -> Can meaning be reconstructed from source evidence?
           YES -> REDRAW or RECONSTRUCT
           NO  -> REVIEW_REQUIRED
  NO  -> Does a new support figure materially improve comprehension?
           YES -> SUPPORT_ADD, clearly additive
           NO  -> Do not add a figure
```

### 8.1 Evidence order

For reconstruction:

1. source wording;
2. source solution;
3. neighbouring source pages;
4. repeated visual convention in same book;
5. external verification only if allowed.

### 8.2 Intentional absence

If source says:

```text
NO DIAGRAM PROVIDED
Draw your own velocity and acceleration arrows.
```

status is:

```text
INTENTIONALLY_ABSENT
```

Do not supply the answer diagram.

### 8.3 Figure semantic manifest

For each important figure record:

```text
figure_id:
source_support:
axes:
objects:
values:
directions:
labels:
relationships:
color_meaning:
learner_purpose:
```

A redraw passes only if semantic relationships match.

---

## 9. Benchmarking without copying

Use reputable Grade 9-11 educational references to benchmark:

- hierarchy;
- reading rhythm;
- page density;
- use of learning objectives;
- worked examples;
- diagram integration;
- practice progression;
- misconception treatment;
- review architecture;
- typography.

Do not copy exact layouts, illustrations, icons, proprietary page systems, or branded language.

### 9.1 Recommended evaluation dimensions

Score 0-5 for each, then convert to the 100-point weighting in the skill:

```text
conceptual clarity
figure usefulness
learning sequence
worked-example reasoning
practice progression
misconception treatment
math/science typography
page hierarchy/readability
retrieval/assessment
cross-link/revision value
```

### 9.2 Benchmark notes template

```text
REFERENCE:
WHAT IT DOES WELL:
PRINCIPLE TO ADAPT:
WHAT NOT TO COPY:
HOW THIS FITS OUR SOURCE:
```

---

## 10. Prototype strategy

A novice agent should **not** build 50 pages to discover the design is weak.

Build 6-8 pages first:

1. lesson/subtopic opener;
2. concept + hero figure page;
3. derivation/explanation page;
4. worked example page;
5. misconception/model-limit page;
6. guided practice page;
7. independent/transfer practice page;
8. review/solution page if needed.

### Prototype acceptance questions

- Can a teacher identify the learning path in 3 seconds?
- Is there one obvious entry point per page?
- Is body text readable at normal view?
- Are equations treated as mathematical objects?
- Is every large figure instructional?
- Are white spaces intentional?
- Does practice sit near the concept it assesses?
- Does the page look authored rather than auto-flowed?
- Can the same system handle three different content types without identical box geometry?

If not, redesign before scaling.

---

## 11. Page-system design

### 11.1 Define a grid family, not one rigid grid

Example family:

```text
A. single-column explanation
B. 65/35 explanation + sidebar
C. full-width figure + text below
D. 50/50 comparison
E. two-column practice
F. worked-example main column + reasoning rail
```

Use the same margins, baseline, type system, and navigation so pages still feel related.

### 11.2 Density

Aim for 70-85% meaningful occupancy on typical learning pages.

Meaningful occupancy includes:

- readable text;
- useful diagrams;
- deliberate problem-solving space;
- annotations;
- practice;
- reflection/retrieval.

It does not include decorative boxes added only to eliminate white space.

### 11.3 White-space diagnosis

Classify blank area:

```text
INTENTIONAL_REST
WORK_SPACE
FIGURE_BREATHING_ROOM
PAGE_BALANCE
ACCIDENTAL_FLOW_GAP
FORCED_BREAK_GAP
UNDERFILLED_LAYOUT
```

Only the last three require repair.

### 11.4 Common layout repair order

When a page is underfilled:

1. remove unnecessary forced break;
2. pair related source units;
3. enlarge or improve an existing instructional figure;
4. move associated practice onto the page;
5. use a legitimate teacher-value synthesis;
6. adjust grid ratios;
7. only then consider moving content from adjacent pages.

Do **not** simply enlarge headings or add decorative cards.

When a page is overcrowded:

1. split by learning sequence;
2. remove duplicated metadata from student-facing surface;
3. convert repeated prose into a source-faithful diagram/table only if original wording remains somewhere appropriate;
4. move teacher-only provenance to appendix;
5. create a continuation page;
6. never reduce body type below the approved minimum just to fit.

---

## 12. Typography protocol

### 12.1 Body hierarchy

Define explicit roles:

```text
chapter title
lesson title
section heading
subheading
body
caption
metadata
question
hint
solution
callout label
```

A novice agent should not invent font sizes page by page.

### 12.2 Math/science typography

Check:

- italic variables versus upright units;
- true superscripts/subscripts;
- fraction construction;
- radical extent;
- minus sign versus hyphen;
- multiplication sign;
- Greek letters;
- vector notation;
- degree symbols;
- chemical charges/formulae;
- graph labels.

### 12.3 Readability test

At ordinary page view, a learner should not need to zoom merely to read body text or critical diagram labels.

Metadata may be smaller, but it must not compete with teaching content.

---

## 13. Worked-example anatomy

A strong worked example usually contains:

```text
1. Situation / question
2. Representation
3. Known / target
4. Model / why this relation
5. Calculation
6. Answer with unit
7. Physical or mathematical check
8. Optional transfer prompt
```

Do not reduce every example to `formula -> substitution -> answer` if the source contains reasoning.

Do not add reasoning that contradicts the source.

---

## 14. Practice progression

Where source material supports it, organize without deleting:

```text
UNDERSTAND
-> explain / identify / predict

APPLY
-> direct numerical or procedural use

CONNECT
-> graph / words / equation / representation conversion

TRANSFER
-> unfamiliar context or independent model choice

CHALLENGE
-> deeper extension if source or approved value-add supports it
```

If the source already has guided/faded/independent practice, preserve those distinctions.

---

## 15. Source-to-publication mapping statuses

Use only these for core source units:

### PRESERVED
Same core unit appears in one target with only typographic/layout change.

### RECOMPOSED
Same unit is rearranged, reformatted, or visually integrated without changing meaning.

### MERGED
Two or more source units share one publication object/page. Each source ID still maps independently.

### SPLIT
One source unit appears across multiple publication targets.

### INTENTIONALLY_ABSENT
The source explicitly requires absence (e.g., student must draw a diagram).

### REVIEW_REQUIRED
Meaning is ambiguous or a suspected editorial correction needs approval.

Never use `VALUE_ADD` as a status for a source unit. Value additions are separate objects.

---

## 16. Equation reconciliation

String equality is not enough.

Normalize equations conceptually.

Example:

```text
source: 1/2 * a * t^2
published: ½at²
```

These may be semantically equal.

But:

```text
source: ½at²
published: ½a²t
```

must fail even if visually similar.

For high-stakes math/science books, maintain an equation list with:

```text
equation_id
source_form
normalized_structure
published_form
status
```

---

## 17. Numeric and unit fingerprint

Extract a separate list of:

- integers;
- decimals;
- signs;
- percentages;
- powers;
- units;
- variable assignments;
- answer values.

This catches silent transcription errors.

Example:

```text
5 m/s
8 m/s
11 m/s
14 m/s
+3 m/s per second
```

A page can look good while one `14` accidentally became `11`.

---

## 18. Link and citation audit

### 18.1 Internal links

Count:

```text
internal_references_discovered
internal_references_resolved
broken_internal_references
ambiguous_targets
orphan_targets
```

Release requires zero in the last three.

### 18.2 External links

For each source URL record:

```text
source_link_id
source_page
anchor_text
destination
publication_location
retained YES/NO
validated YES/NO
```

Do not assume visible blue text still contains a hyperlink.

### 18.3 Page numbers

Generate them only after layout. If a page moves, rebuild references.

---

## 19. Render QA workflow

1. Export final PDF.
2. Render every page to images.
3. Create a contact sheet/montage.
4. Inspect global rhythm.
5. Inspect every equation-heavy page at 100%.
6. Inspect every dense page.
7. Inspect every figure-heavy page.
8. Inspect first/last page of each subtopic.
9. Inspect pages referenced in the exception log.
10. Repair and re-render.

### Visual QA defect codes

```text
CLIP
OVERLAP
HIDDEN_TEXT
BAD_GLYPH
MATH_BASELINE
SUBSCRIPT
SUPERSCRIPT
FIG_LABEL
FIG_SCALE
LOW_RES
UNDERFILLED
OVERCROWDED
ORPHAN_HEADING
BAD_BREAK
LINK_STYLE
HIERARCHY
READABILITY
```

---

## 20. Anti-drift checkpoint card

Use this at the end of every subtopic or every 5-10 pages.

```text
ANTI-DRIFT CARD

[ ] Source authority unchanged
[ ] Frozen source-unit denominator preserved
[ ] Every core unit mapped
[ ] New objects are VALUE_ADD, not replacements
[ ] No unapproved factual/editorial changes
[ ] Stable IDs still canonical
[ ] No hard-coded page-reference dependency
[ ] Missing figures have evidence
[ ] Intentional omissions preserved
[ ] Equations semantically unchanged
[ ] Numbers/units reconciled
[ ] Layout is authored, not generic auto-flow
[ ] White space is intentional
[ ] Body/labels readable at normal view
[ ] Benchmark prototype standard maintained
[ ] Rendered PDF inspected
[ ] Link counters pass
```

If any box is unchecked, stop the batch.

---

## 21. What “100% core data reconstructed” actually means

It does **not** mean:

- same number of pages;
- same coordinates;
- same font;
- same colors;
- same card structure;
- same visible numbering.

It means:

1. every frozen core source unit is mapped;
2. every equation retains its semantic meaning;
3. all numeric values and units reconcile;
4. figure meaning is preserved;
5. intentional absences remain intentional;
6. all source relationships are preserved;
7. links resolve;
8. no core item is hidden/clipped/unreadable;
9. no source claim is silently replaced by a teacher-added claim;
10. all editorial differences are approved or unresolved, never hidden.

---

## 22. Release report template

Use real counts, not placeholders.

```text
PUBLICATION RELEASE AUDIT

Source file:
Source pages:
Published pages:

CORE SOURCE
Core units detected:
Core units mapped:
Unmapped core units:
Review-required units:

MATH / SCIENCE
Equations detected:
Equations semantically matched:
Equation mismatches:
Numeric/unit tokens checked:
Numeric/unit mismatches:

FIGURES
Source figures:
Preserved:
Redrawn:
Reconstructed:
Support-add figures:
Intentional absences preserved:
Unresolved figures:

LINKAGE
Internal references discovered:
Internal references resolved:
Broken internal references:
External source links discovered:
External source links retained:
Broken/unresolved source links:

RENDER QA
Clipped core objects:
Hidden core objects:
Overflow findings:
Unreadable critical labels:

EDITORIAL
Approved changes:
Unapproved changes:

STATUS:
```

Allowed final status examples:

```text
PASS — CORE DATA RECONCILIATION 100%; LINK QA PASS; RENDER QA PASS
NOT READY — 2 UNMAPPED CORE UNITS
NOT READY — 1 UNAPPROVED EDITORIAL CHANGE
PROTOTYPE ONLY — STYLE APPROVED; FULL SOURCE RECONCILIATION PENDING
```

---

## 23. Common novice failure modes and repair

### Failure: Copy-with-cleanup

Symptom: same old page geometry, only fonts/collisions repaired.

Repair: return to source units and redesign page architecture. Preserve content, not coordinates.

### Failure: Auto-flow dump

Symptom: tiny text poured into columns, metadata visible everywhere, weak hierarchy.

Repair: manually compose prototype families; move metadata to quieter roles; create real figures and practice structure.

### Failure: Too much white space

Symptom: half-empty pages while adjacent pages are crowded.

Repair: diagnose blank-space type; pair related source units; adjust grid; move associated practice; add legitimate support, not decoration.

### Failure: Too many cards

Symptom: every paragraph is boxed; hierarchy disappears.

Repair: use ordinary editorial text for most content. Reserve boxes for genuinely different functions.

### Failure: Over-condensation

Symptom: source explanations replaced by a cleaner summary.

Repair: restore source explanations; keep the summary as additive synthesis.

### Failure: Missing-source evidence

Symptom: new diagram introduced because “it seemed useful” but it changes the answer or reveals a student task.

Repair: apply figure evidence gate; mark intentional absence or review required.

### Failure: Renumbering breakage

Symptom: `See page 12` becomes wrong after repagination.

Repair: replace hard-coded citation with stable target ID and regenerate display label.

### Failure: Invisible data loss

Symptom: extracted text exists in PDF but is covered by a callout.

Repair: render-level visibility audit. Technical presence is not preservation.

---

## 24. Working with the other Grade 9 skills

Recommended routing:

```text
source PDF
-> grade9-source-grounding
-> subject skill (grade9-physics / math / chemistry)
-> grade9-publication for reconstruction/value-add/layout
-> grade9-subtopic-completeness-auditor
-> grade9-transfer-coverage-auditor if external/PYQ corpus exists
-> final render/link/source reconciliation
```

If the project already has canonical validated master data and does not require source-PDF reconstruction, use `grade9-textbook-publisher` for rendering instead.

---

## 25. Final principle

The strongest publication is not the one that changes the most.

It is the one that makes the **original knowledge easier to see, understand, navigate, practise, and verify** while maintaining a provable chain back to every source obligation.
