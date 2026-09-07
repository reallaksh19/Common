---
name: grade9-redox-subtopic-book-builder
description: Build source-grounded Grade 9/JEE-foundation Redox subtopic Study Guides and ExamSIDE transfer books using the approved textbook-style instructional grammar, chemistry-safe typography, misconception repair, concept helpers, difficulty-based hints, Appendix A solutions, and bidirectional transfer-coverage audits. Use when producing or rebuilding Redox subtopics from a supplied source PDF and linked ExamSIDE questions.
---

# Grade 9 Redox Subtopic Book Builder

Use this skill for the Redox project when the user wants one focused subtopic at a time.

## 1. Source boundary first

Treat the supplied Redox source as authoritative for scope and terminology.

For each subtopic create a source-obligation ledger before writing:

```text
SOURCE_OBLIGATION_ID
source page / line
required concept
required example(s)
required exception(s)
required terminology
status
```

Do not silently introduce balancing, equivalent weight, titration, electrochemistry, medium-dependent reagent chemistry, or other content absent from the source. If an external question needs such knowledge, defer or exclude it explicitly.

## 2. Approved instructional grammar

The learner-facing Study Guide should follow the approved textbook rhythm:

```text
ORIENT / FAMILIAR CONTEXT
-> EXPLAIN THE IDEA IN ORDINARY LANGUAGE
-> SHOW WHAT IT MEANS VISUALLY / SYMBOLICALLY
-> THINGS TO KNOW / KEY RULE
-> WORKED EXAMPLE WITH REASONING STORY
-> CONCEPT HELPER
-> MISCONCEPTION CLINIC
-> TRY WITH ME
-> FADED PRACTICE
-> CHECK YOUR KNOWLEDGE
-> TRANSFER LINK
```

The page should read like a teacher explanation, not a dashboard of independent cards.

## 3. Redox-specific reasoning patterns

### Oxidation number

Use:

```text
read formula -> apply fixed rules -> check H/O exceptions -> sum = 0 or ion charge -> solve -> check
```

Explicitly distinguish subscripts, ionic charge, assigned oxidation numbers, average oxidation number, and actual non-equivalent sites.

### Oxidation / reduction

Use both equivalent languages:

```text
LOSE e⁻ -> oxidation -> oxidation number UP
GAIN e⁻ -> reduction -> oxidation number DOWN
```

For electron-count questions: calculate the oxidation-number jump per atom first, then account for atom count.

### Oxidising / reducing agents

Teach SELF vs OTHER:

```text
oxidised species = reducing agent
reduced species = oxidising agent
```

Agent name describes what the species causes in the other reactant. Attach the role to the reactant species, not only to the tracked atom. Identify spectators explicitly where useful.

### Redox vs non-redox

Use the fingerprint:

```text
no oxidation-number change -> non-redox
one UP + one DOWN -> redox
```

Reaction appearance, oxygen presence, gas formation, combination, or decomposition alone never proves redox.

### Redox reaction types

Keep reaction type and redox status separate.

Use topology helpers:

```text
combination: many reactants -> one product

decomposition: one reactant -> many products

displacement: element displaces another element from a compound

disproportionation: same element, one initial oxidation state -> lower + higher states

comproportionation: same element, lower + higher states -> one intermediate state

intermolecular redox: oxidation and reduction occur in different reactant molecules/species

intramolecular redox: oxidation and reduction occur within the same reactant molecule/species
```

Do not classify combination/decomposition as redox without first proving oxidation-number change.

## 4. Familiar / real-life bridge

For each core subtopic include one safe familiar bridge when it clarifies the source concept without adding a new chemistry dependency. Examples can include a familiar formula label, burning carbon, a visible metal-displacement reaction, or another source-compatible situation.

If no safe bridge exists, mark `FAMILIAR_CONTEXT_NOT_APPLICABLE` rather than inventing one.

## 5. Concept helpers

High-recognition-load Redox concepts require a reusable helper. Preferred helpers include:

- formula anatomy;
- rule-priority ladder;
- charge-balance visual;
- before -> after oxidation-state lane;
- negative-electron token model;
- SELF vs OTHER frame;
- six-move agent decision strip;
- redox fingerprint decision tree;
- split/converge topology for disproportionation/comproportionation;
- inter vs intra molecule map.

A helper should reveal the reasoning representation, not give away the answer.

## 6. Misconception repair

Use explicit `wrong model -> why it fails -> repair -> retry` treatment.

High-priority Redox misconceptions include:

```text
oxygen is always -2
hydrogen is always +1
sum of oxidation numbers is always 0
average oxidation number means every atom has that value
oxidation means adding oxygen only
reduction means removing oxygen only
losing electrons should make oxidation number fall
oxidising agent is itself oxidised
reducing agent is itself reduced
all chemical reactions are redox
contains oxygen / gas forms / visible change -> redox
combination -> redox
decomposition -> redox
same reagent always has same OA/RA role
```

Generic warnings do not count as misconception repair.

## 7. Chemistry typography contract - blocking

Use a Unicode-complete tested font family such as Noto Sans throughout chemistry-heavy programmatic PDFs.

Learner-facing chemistry must use proper notation:

```text
e⁻, 2e⁻
Fe³⁺, Fe²⁺, Cl⁻, S²⁻, I⁻
H₂O₂, K₂Cr₂O₇, Cr₂O₇²⁻
```

Do not publish baseline ASCII chemistry such as `e-`, `Fe3+`, `Cr2O7^2-` in display text.

If the chosen font does not support a required reaction arrow or chemistry glyph, use a tested fallback only for that formula/equation block or draw the symbol programmatically. Never allow missing-glyph squares.

Emit:

```text
CHEMISTRY_ASCII_LEAKS = 0
SUPERSCRIPT_FAILURES = 0
SUBSCRIPT_FAILURES = 0
FONT_FALLBACK_FAILURES = 0
```

Any non-zero count blocks publication.

## 8. Layout contract - blocking

Use independent title and subtitle zones. Long headings must wrap or shrink deterministically before render.

Block publication for:

- clipped title/subtitle;
- title/subtitle collision;
- body text outside boxes;
- overlapping cards;
- helper/hint collision;
- answer strip clipping;
- unreadably small chemistry;
- accidental large voids with no pedagogical purpose;
- broken left-to-right reasoning flow.

For H1-H3 pages use deterministic fixed slots rather than estimating positions from text length.

## 9. Study Guide practice progression

For each core reasoning skill, include where applicable:

```text
worked example
-> TRY WITH ME
-> faded scaffold
-> independent check
-> CHECK YOUR KNOWLEDGE
```

Do not make the independent question an exact surface copy of the worked example.

## 10. ExamSIDE transfer-book contract

Before publication, freeze the canonical required set for the subtopic.

Each eligible external question must receive exactly one primary subtopic. Secondary prerequisite concepts may be linked, but they do not create duplicate primary placement.

Each placed question must contain:

```text
question ID + source/date
original source link
primary concept link to Study Guide
difficulty level
H1 / H2 / H3 according to difficulty
question-specific concept helper
misconception watch when high-risk
Appendix A full solution
```

Difficulty support:

```text
1/3 -> H1
2/3 -> H1-H2
3/3 -> H1-H3 + stronger visual/concept helper
```

Hints must progressively reveal the route, not repeat the full solution.

## 11. Transfer-coverage audit

Run together with `grade9-transfer-coverage-auditor`.

Required counters:

```text
SUBTOPIC_REQUIRED = n
SUBTOPIC_PLACED = n
SUBTOPIC_DEFERRED_VALID = 0 at final acceptance
SUBTOPIC_MISSING = 0
WRONG_PLACEMENT = 0
CONCEPT_LINK_FAILURES = 0
HINT_FAILURES = 0
SOLUTION_FAILURES = 0
BROKEN_SOURCE_LINKS = 0
SCOPE_LEAKS = 0
COVERAGE = 1.00
```

Also provide reverse evidence:

```text
question -> primary subtopic -> Study Guide concept -> hint support -> Appendix A -> source link -> COMPLETE
```

## 12. Render-first QA

For every generated PDF:

```text
GENERATE
-> RENDER EVERY PAGE
-> INSPECT LONGEST TITLE
-> INSPECT DENSEST CHEMISTRY PAGE
-> INSPECT H1-H3 PAGE
-> INSPECT APPENDIX PAGE
-> INSPECT FINAL AUDIT PAGE
-> REPAIR
-> RE-RENDER
-> PASS
```

The rendered page is authoritative, not the source code.

## 13. Final subtopic gate

Do not declare a subtopic final until all are PASS:

```text
SOURCE = PASS
PEDAGOGY = PASS
TRANSFER = PASS
TYPOGRAPHY = PASS
LAYOUT = PASS
```

If any fail, report the exact learner consequence and smallest repair before proceeding to the next subtopic.
