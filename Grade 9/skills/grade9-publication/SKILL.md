---
name: grade9-publication
description: Reconstruct and publish source-grounded Grade 9-11 educational PDFs without replacing core source content. Use for publisher-grade redesign, zero-loss source reconciliation, question-bank reconstruction, figure/option preservation, concept-assimilation solutions, math/science typography, automatic renumbering/linking, render-first QA, and deterministic anti-drift audits.
---

# Grade 9 Publication

Use this skill when an existing educational PDF or book is the source of truth and must be reconstructed as a stronger publication.

The governing rule is:

> **Add value around the source. Do not replace the source.**

A rebuild may change page count, page breaks, orientation, grids, typography, figure placement, exercise grouping, navigation, and visible numbering. It must not silently delete, rewrite, simplify away, correct, or substitute the source's core instructional data.

This is a **control skill**. It exists to stop drift while layout, pedagogy, figures, solutions, and navigation are improved.

## Mandatory routing before work begins

Choose the product mode first.

### Source-PDF textbook / study-guide reconstruction

Read:

- `references/publication-playbook.md`
- `references/student-page-qa.md`
- `references/layout-collision-gate.md`
- `references/audit-manifest-spec.md`

### Question bank / PYQ / transfer book / worksheet collection / question-plus-solution book

Read all of the above **plus**:

- `references/student-first-question-bank-layout.md`
- `references/question-bank-assimilation-integrity.md`

For Physics concept-assimilation/transfer work, also use `../grade9-physics-subtopic-book-builder/SKILL.md` and the relevant Physics skill. For Chemistry, use the relevant Chemistry skill and preserve the chemistry typography contract.

Do not scale a full book before these references have been applied to a representative prototype.

# 1. Non-negotiable publication contract

1. **Source is immutable.** Never overwrite the only source copy.
2. **Source is authority.** General knowledge may not silently fill gaps, fix answers, invent figures, or replace missing options.
3. **Core mapping precedes design.** Extract and classify obligations before layout.
4. **No silent editorial correction.** Suspected source errors become `REVIEW_REQUIRED` unless explicitly approved.
5. **Stable IDs survive repagination.** Page numbers and visible labels are derived data, never canonical identity.
6. **Intentional absence is data.** If the learner is meant to draw/construct something, preserve that instructional choice.
7. **Hidden = lost.** Covered, clipped, off-page, microscopic, unreadable, or missing-context content fails preservation.
8. **Professional layout is not auto-flow.** Recomposition must follow learning function, not merely extracted text order.
9. **Benchmark principles, never clone copyrighted publisher designs.**
10. **The unit of certification is the learner obligation.** For question banks, that unit is the individual question.
11. **Do not claim publisher-ready from page count or visual resemblance.** Release requires source, dependency, pedagogy, link, typography, and render closure.

# 2. Content classes

Classify every item before redesign.

## CORE_SOURCE

Must survive semantically and, where wording matters, textually.

Examples:

- headings and section meaning;
- explanatory paragraphs;
- equations and derivations;
- numerical values and units;
- question wording;
- hints and worked solutions;
- concept/question/difficulty/source IDs;
- graph/table/diagram data and labels;
- option figures and statement sets;
- source citations and hyperlinks;
- model limits and stated misconceptions;
- learner instructions such as `NO DIAGRAM PROVIDED`.

## PRESENTATION_SOURCE

May be redesigned while preserving function and meaning.

Examples:

- coordinates and box dimensions;
- landscape vs portrait;
- decorative colors/rules;
- card shapes;
- page breaks;
- visible numbering.

## VALUE_ADD

New instructional support that does not replace source content.

Allowed reasons:

```text
clarify
connect
diagnose
practice
navigate
reduce_cognitive_load
```

Examples: concept helper, representation bridge, misconception contrast, retrieval cue, glossary cue, teacher note, synthesis map.

## EDITORIAL_CHANGE

Any change to source meaning, wording, numerical data, answer, scope, or scientific claim.

Do not perform silently. Record as `REVIEW_REQUIRED` unless the user explicitly approves it.

# 3. Anti-drift state machine

An agent must follow these phases in order. A failed gate stops the build.

## Phase A — BRIEF LOCK

Record:

- audience/grade band;
- source authority;
- product type;
- allowed additions;
- forbidden changes;
- output artifacts;
- whether page count may change;
- whether student and solution PDFs are separate;
- required preservation level.

**AD0 BRIEF LOCK:** if the agent cannot state what may change and what may not, stop.

## Phase B — SOURCE FREEZE

Record:

- filename/checksum where available;
- page count and dimensions;
- searchable vs scan pages;
- fonts;
- links/bookmarks;
- embedded figures/images;
- obvious clipping/collision/glyph defects.

Render representative source pages, including every template family and known high-risk page.

**AD1 SOURCE FREEZE:** no layout work before the source is preserved separately and page count is known.

## Phase C — SOURCE OBLIGATION LEDGER

Prefer existing IDs such as `EX-M10B-02`, `M4A-C5`, etc. Otherwise assign immutable IDs.

For every source obligation record:

```text
source_id
source_page/range
type
raw locator/content
semantic summary
numbers/units
relationships
learner function
preservation class
mapped target(s)
status
```

Allowed source status:

```text
PRESERVED
RECOMPOSED
MERGED
SPLIT
INTENTIONALLY_ABSENT
REVIEW_REQUIRED
```

There is no `OMITTED` status in a zero-loss build.

**AD2 DENOMINATOR LOCK:** freeze the core-unit denominator before design. It may not shrink because an item is difficult to place.

## Phase D — QUESTION / DEPENDENCY LEDGER

Required for question-bank products.

Create one record per question before layout. Use the schema in `references/question-bank-assimilation-integrity.md` and `references/audit-manifest-spec.md`.

At minimum classify:

```text
question_id
source_page
set_id
question_family
question_recap_complete
representation_dependency
representation_source_status
representation_present_student
representation_present_solution
answer_choice_status
h1/h2/h3 status
hint_progression_ok
method_has_why
method_has_executable_route
method_distinct_from_answer
answer_present
concept_to_keep_present
math_typography_ok
question<->solution links
source_link_ok
copy_paste_drift_check
status
```

**AD3 QUESTION DENOMINATOR:** frozen question count must equal published question count.

## Phase E — RELATIONSHIP GRAPH

Create stable-ID links for:

- question -> concept;
- question -> hints;
- question -> solution;
- solution -> question;
- figure callouts;
- appendix references;
- source URLs;
- prerequisite references.

Never hard-code a page number when a stable target ID can be resolved later.

**AD4 IDENTITY CHECK:** references use stable IDs; visible labels/page numbers are generated after pagination.

## Phase F — TEACHER / CONCEPT ANALYSIS

For every subtopic/question family ask:

1. What is the big idea?
2. What representation exposes it best?
3. What misconception is likely?
4. What must the learner notice before calculating?
5. What source ideas should be visually connected?
6. Which blank area is purposeful work space vs accidental whitespace?
7. Does the question depend on a source graph/table/options/diagram?
8. What concept should the learner retain after checking the solution?

**AD5 ADDITIVE VALUE:** each new object must help the learner while leaving source content present and identifiable.

## Phase G — PROTOTYPE GATE

Before scaling, build 6-8 representative pages or equivalent coverage of template families.

For question banks the prototype must include:

- compact D1/D2 page;
- D3 page with real work space;
- D4/graph-heavy page;
- stacked H1-H3 with real numerical/math detail;
- answer-choice/statement-set case if present;
- representation-dependent solution recap;
- solution with `WHY THIS WORKS -> METHOD -> ANSWER -> CONCEPT TO KEEP`;
- set-level navigation;
- proof of zero overlap/clipping.

Do not generate dozens of pages until this passes.

# 4. Student-first question-bank contract

For question-bank products, learner experience takes priority over old page boundaries.

## Bounded study sets

Prefer 6-10 mixed-difficulty questions per set, fewer for graph-heavy/multi-step sets.

Use `SET n / N` and set-level progress. Do not make the total page count the dominant learner signal.

## Density by difficulty

Default:

```text
D1: 2-3 short questions/page when safe
D2: usually 2/page
D3: 1-2/page
D4/D5 or graph/diagram heavy: generous half-page or full page
```

Do not shrink typography/work space merely to reduce page count.

## Mandatory eye path

Unless source pedagogy explicitly requires otherwise:

```text
QUESTION
-> WORK HERE / representation area
-> STOP / optional hint boundary
-> H1 NOTICE
-> H2 MODEL
-> H3 START
-> method-check link
```

Hints belong **below** the work area so the learner does not read them accidentally.

## H1-H3 semantics

```text
H1 NOTICE  decisive clue/data interpretation
H2 MODEL   representation/model/intermediate quantities
H3 START   first executable equation/substitution/calculation
```

Numerical intermediate detail is allowed and often desirable.

Fail if H1 gives the final answer, H1-H3 repeat each other, or H3 remains generic.

# 5. Representation-dependency integrity

If a question says or implies `from the graph`, `as shown`, `use the table`, `choose the curve`, `which diagram`, or otherwise depends on a representation, that representation is CORE_SOURCE.

Classify:

```text
NONE
GRAPH
DIAGRAM
TABLE
TIMELINE
NUMBER_LINE
OPTION_FIGURES
STATEMENT_SET
MIXED
```

For every non-`NONE` question require:

```text
representation_present_student = true
representation_legible = true
critical_labels/data preserved = true
```

If the solution/method artifact is standalone, also require:

```text
representation_present_solution = true
```

A recap such as `Find distance from a v-t graph` without the graph fails.

## Source crop/redraw rules

When preserving a source figure:

- include all axes, scales, units, labels, dimensions, legends, zero lines, negative regions, option letters, arrows, and values used by reasoning;
- avoid importing unrelated hint/solution text into the crop;
- inspect at normal learner size;
- if unreadable, redraw semantically or allocate more space;
- do not invent missing semantics.

A technically present but unreadable crop counts as missing.

# 6. Answer-choice integrity

Never ask the student to choose an invisible option.

For MCQ, graph-choice, matching, statement-set, or option-figure items, one of these must be true:

1. all source-supported choices are visible;
2. the task is transparently adapted to a standalone `calculate`, `describe`, `sketch`, or `state the criterion` task using only source-supported semantics;
3. missing choices are reconstructed from approved source evidence and audited.

Never invent options from general knowledge.

If the method says `Option D` but choices are not visible there, include semantic meaning:

```text
Option D — straight a-x line with positive slope and negative intercept.
```

Orphan labels such as `D`, `Graph 3`, `A/B/D only`, or `(B),(C),(E)` fail when the choices are absent.

# 7. Solution assimilation contract

A solution is not an answer key with extra words. It must teach the reusable concept.

Default question-bank solution structure:

```text
QUESTION RECAP
<enough wording to identify the task>

QUESTION FIGURE / OPTIONS / TABLE
<when representation-dependent>

WHY THIS WORKS
<physical/mathematical/chemical/conceptual reason>

METHOD
<question-specific executable reasoning route>

ANSWER / CHECK
<explicit result, units/sign/semantic choice meaning>

CONCEPT TO KEEP
<one transferable idea>

RETURN TO QUESTION
```

Short conceptual questions may use concise versions, but the method must remain pedagogically distinct from the answer.

## Blocking method failures

Fail when:

- `METHOD` is identical or near-identical to `ANSWER`;
- `METHOD` only states a formula with no reason it applies;
- the decisive modeling/representation step is absent;
- the route jumps directly to final substitution/result;
- generic boilerplate is copied across questions whose reasoning differs;
- the method depends on a missing graph/table/options;
- stray neighboring-question or template text appears.

The answer is the destination. The method explains **why this route works and how to reuse it**.

# 8. Mathematics and science typography

Treat equations as semantic objects, not plain strings.

Preserve the raw/source representation in the audit model, but publish true notation.

Examples:

```text
v1 -> v₁
v2 -> v₂
s_(n+2) -> properly typeset subscript expression
sqrt(t1 t2) -> √(t₁t₂)
m/s2 -> m/s²
```

Do not guess index vs exponent semantics from typography alone. Resolve meaning from the source relation.

Audit:

- subscripts;
- superscripts;
- fractions;
- radicals;
- Greek symbols;
- vectors;
- signs;
- units;
- chemistry charges/formulae where relevant;
- graph-axis notation.

Run:

```text
python scripts/check_math_typography.py student.pdf
```

Then visually inspect equations because text scanning cannot verify glyph placement.

# 9. Layout and component contract

Define before scaling:

- page size/orientation;
- margins/safe zones;
- baseline grid;
- content-column families;
- type hierarchy;
- equation style;
- figure-label style;
- callout vocabulary;
- header/footer/navigation;
- page-density target;
- accessibility/readability floors.

Aim for roughly 70-85% meaningful occupancy on ordinary learning pages. Working space counts as meaningful occupancy.

Avoid:

- repeated 50/50 layouts regardless of content;
- giant decorative headers;
- tiny body text to save pages;
- large accidental lower-page voids;
- equal visual emphasis for all objects;
- one card for every idea;
- decorative graphics that teach nothing.

## Reserve -> draw -> advance

Every reusable component must declare its bounds. Wrap content before rendering, reserve vertical space, draw, then advance.

Never continue from a guessed y-coordinate after a fixed-height component.

Run:

```text
python scripts/check_text_overlaps.py final.pdf
```

Known real overlap, clipping, bounds escape, or incomplete equation line blocks release.

# 10. Figure policy

Classify each figure:

```text
PRESERVE
REDRAW
RECONSTRUCT
SUPPORT_ADD
INTENTIONALLY_ABSENT
REVIEW_REQUIRED
```

For `RECONSTRUCT`, use evidence in this order:

1. source page text;
2. source solution/answer;
3. neighboring source concept pages;
4. established visual grammar in the same source;
5. outside verification only when user allows it.

Record semantic data: axes, values, arrows, labels, regions, relationships.

Never invent a figure because a page looks empty.

# 11. Automatic numbering and links

Keep two identities:

- immutable source ID;
- generated publication label.

After pagination regenerate:

- section numbers;
- figure/table numbers;
- worked-example numbers;
- question/solution numbers;
- TOC;
- bookmarks;
- page references;
- question -> solution links;
- solution -> question links;
- external source links.

Required closure:

```text
references_discovered = references_resolved
broken_references = 0
ambiguous_references = 0
orphan_targets = 0
duplicate_publication_ids = 0
```

# 12. Four-way reconciliation

Audit separately:

```text
SOURCE PDF
-> EXTRACTED SOURCE MODEL
-> PUBLICATION MODEL
-> FINAL PDF
```

Ask at each transition:

- extraction missed anything?
- reorganization altered/deleted anything?
- rendering hid/clipped/substituted anything?
- final learner artifact still carries every obligation and dependency?

**AD DENOMINATOR RECONCILIATION:** frozen counts must equal mapped/published counts with zero unexplained omissions.

# 13. Per-batch anti-drift gate

After every 5-10 pages, 5-10 questions, or one complete subtopic/set, stop and run the gate before continuing.

General:

```text
core denominator unchanged
unmapped core units = 0
unapproved editorial changes = 0
broken stable-ID links = 0
figure evidence failures = 0
math/science typography failures = 0
text overlaps = 0
component bounds escapes = 0
```

Question-bank additions:

```text
question count frozen = published count
unattemptable questions = 0
representation dependency failures = 0
invisible choice failures = 0
question recap failures = 0
hint progression failures = 0
METHOD≈ANSWER failures = 0
method reasoning failures = 0
solution self-containment failures = 0
copy-paste/template drift failures = 0
question<->solution link failures = 0
```

Any non-zero count stops generation. Repair the current batch before producing more pages.

# 14. Render-first QA

Render every final page to images.

Inspect:

- clipping/overlap;
- formulas and glyphs;
- graph/figure labels;
- source crops;
- page rhythm/density;
- accidental whitespace;
- crowded regions;
- orphan headings;
- awkward page breaks;
- hidden answer/result lines;
- answer-choice visibility;
- representation-dependent questions;
- standalone solution self-containment;
- repeated boilerplate/copy-paste leakage.

Scan a contact sheet for global rhythm, then inspect high-risk pages at full size.

# 15. Required audit artifacts

A serious reconstruction should produce:

1. rebuilt publication PDF(s);
2. source-to-publication manifest;
3. question-level records for question-bank products;
4. cross-reference/link audit;
5. figure/diagram inventory;
6. render QA/contact sheet;
7. exception log;
8. page/section migration map for large books.

For separated products:

- **Student Core / Practice PDF** — learner content only;
- **Check Your Method / Solution PDF** — self-contained solutions;
- **Audit manifest/report** — provenance, QA counters, mappings, exceptions.

Do not leak publisher-process language into the student artifact merely to prove completeness.

# 16. Deterministic checks

Use the manifest schema in `references/audit-manifest-spec.md`.

Run as applicable:

```text
python scripts/check_publication_manifest.py manifest.json
python scripts/check_text_overlaps.py final.pdf
python scripts/check_math_typography.py student.pdf
```

These are baseline gates, not substitutes for subject-matter or visual review.

# 17. Required release counters

General release requires:

```text
unmapped_core_units = 0
unapproved_editorial_changes = 0
broken_internal_references = 0
unresolved_source_links = 0
hidden_or_clipped_core_content = 0
text_overlap_findings = 0
component_bounds_escape_findings = 0
critical_equation_collision_findings = 0
math_typography_failures = 0
```

Question-bank release additionally requires:

```text
questions_frozen = questions_published
unattemptable_questions = 0
representation_dependency_failures = 0
invisible_choice_failures = 0
question_recap_failures = 0
hint_progression_failures = 0
method_answer_duplication_failures = 0
method_reasoning_failures = 0
solution_self_containment_failures = 0
question_solution_link_failures = 0
copy_paste_drift_failures = 0
all question_records = PASS
```

If any blocking counter is non-zero, status is:

`NOT READY FOR PUBLICATION`.

# 18. Common drift patterns to reject

- “All text is present, so the book is complete.”
- “Page count matches, so nothing was lost.”
- “The PDF opens, so overlap is acceptable.”
- “I fixed the font, so reconstruction is done.”
- “The source graph was decorative.” without dependency audit.
- “The question says choose D, so answer D is enough.” when choices are absent.
- “The method can be the formula because the answer is correct.”
- “The recap says from the graph, so the graph need not be repeated.”
- “I can infer the missing option/figure from general knowledge.”
- “v2 is readable enough.” when the intended notation is v₂.
- “H1-H3 can share one generic sentence.”
- “One question per page is safer.” regardless of difficulty/workload.
- “I can shrink to 7 pt to avoid another page.”
- “The source equation is probably wrong, so I corrected it.”
- “The blank space looked ugly, so I inserted an unsupported diagram.”
- “A generic method paragraph can be reused for the whole set.”
- “I will audit the figures after the book is generated.”

# 19. Completion statement

Do not say `publisher-ready`, `100% reconstructed`, or equivalent unless deterministic and visual gates pass.

Use precise status language such as:

- `SOURCE MAPPING COMPLETE; QUESTION DEPENDENCY AUDIT PENDING`
- `PROTOTYPE APPROVED; FULL RECONSTRUCTION NOT YET CERTIFIED`
- `QUESTION RECORDS 61/61 PASS; LINK/RENDER QA PENDING`
- `CORE DATA RECONCILIATION 100%; LINK/RENDER QA PASS`
- `NOT READY: 3 REPRESENTATION-DEPENDENCY FAILURES`

The final question to ask before release is:

> **Can a student attempt and learn from every published question using only the published artifact, with no missing representation, invisible choice, broken notation, or answer-only solution?**

If the answer is not demonstrably yes, the build is not finished.