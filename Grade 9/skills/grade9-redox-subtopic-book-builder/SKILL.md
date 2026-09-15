---
name: grade9-redox-subtopic-book-builder
description: Apply the Redox-specific reasoning layer inside the Grade 9 Chemistry topic-builder contract. Build each Redox topic as exactly two learner-facing PDFs: a Core Study Guide with Appendix A Core Practice, Appendix B Core Solutions and Appendix C Printable Handout, plus an ExamSIDE Solution & Transfer book with Redox concept segregation, badges, progressive hints, transfer support, source links and complete solutions.
---

# Grade 9 Redox Subtopic Book Builder

Use this skill as the **Redox-specific adapter** under `$grade9-chemistry-topic-builder`.

The Chemistry-wide delivery contract is authoritative. For every Redox topic create exactly:

```text
1. Core Study Guide
   + Appendix A Core Practice
   + Appendix B Core Solutions
   + Appendix C Printable Handout

2. ExamSIDE Solution & Transfer Book
   + attempt-first question pages
   + concept segregation labels
   + source/difficulty/transfer badges
   + H1/H2/H3 optional hints as required
   + Core/source links
   + complete solutions
```

Do not emit a separate handout PDF. Appendix C is mandatory inside the Core Study Guide.

## 1. Source boundary first

Treat the supplied Redox source as authoritative for scope and terminology.

For each topic create a source-obligation ledger before writing:

```text
SOURCE_OBLIGATION_ID
source page / locator
required concept
required example(s)
required exception(s)
required terminology
status
```

Do not silently introduce balancing, equivalent weight, titration, electrochemistry, medium-dependent reagent chemistry, or other content absent from the source. If an external question needs such knowledge, defer or exclude it explicitly.

## 2. Approved instructional grammar

The teaching body of the Core Study Guide should follow:

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

```text
read formula -> apply fixed rules -> check H/O exceptions -> sum = 0 or ion charge -> solve -> check
```

Distinguish subscripts, ionic charge, assigned oxidation numbers, average oxidation number, and actual non-equivalent sites.

### Oxidation / reduction

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

Attach the role to the reactant species and identify spectators where useful.

### Redox vs non-redox

```text
no oxidation-number change -> non-redox
one UP + one DOWN -> redox
```

Reaction appearance, oxygen presence, gas formation, combination, or decomposition alone never proves redox.

### Redox reaction types

Keep reaction type and redox status separate.

```text
combination: many reactants -> one product
decomposition: one reactant -> many products
displacement: element displaces another element from a compound
disproportionation: one initial ON -> lower + higher
comproportionation: lower + higher -> one intermediate ON
intermolecular: oxidation/reduction in different reactant species
intramolecular: oxidation/reduction within the same reactant species
```

## 4. Familiar bridge, helpers and misconception repair

For each core topic include one safe familiar bridge when useful. If none is safe, record `FAMILIAR_CONTEXT_NOT_APPLICABLE`.

Preferred Redox helpers include formula anatomy, rule-priority ladders, charge-balance visuals, before/after ON lanes, electron-token models, SELF vs OTHER, redox fingerprint trees and split/converge topology.

Use explicit `wrong model -> why it fails -> repair -> retry` treatment for high-risk misconceptions.

## 5. Core Study Guide appendices — blocking

### Appendix A — Core Practice

Include independent/faded Redox practice tied to stable concept IDs. Use varied equations/formulas so learners must recognise the method, not copy surface features.

### Appendix B — Core Solutions

Provide a complete reasoning solution for every Appendix A item. Show the minimum justified Redox path and the final check. Do not leak Appendix B answers onto Appendix A attempt pages.

### Appendix C — Printable Handout

Appendix C is mandatory. It must be a standalone printable Redox handout for that topic containing only the minimum high-value revision layer, for example:

- first-move decision strip;
- key oxidation-number/agent/type rules relevant to the topic;
- essential exception reminder;
- one reusable representation/helper;
- common trap list;
- short retrieval/self-check prompts.

It must not introduce new chemistry and must not become a compressed answer key.

Required counters:

```text
APPENDIX_A_PRESENT = 1
APPENDIX_B_PRESENT = 1
APPENDIX_C_HANDOUT_PRESENT = 1
HANDOUT_STANDALONE_USABLE = 1
HANDOUT_SCOPE_LEAKS = 0
```

## 6. Chemistry typography contract — blocking

Use tested Unicode-complete fonts. Learner-facing chemistry must use proper notation such as:

```text
e⁻, 2e⁻
Fe³⁺, Fe²⁺, Cl⁻, S²⁻, I⁻
H₂O₂, K₂Cr₂O₇, Cr₂O₇²⁻
```

Do not publish baseline ASCII chemistry such as `e-`, `Fe3+`, `Cr2O7^2-` in display text.

Emit:

```text
CHEMISTRY_ASCII_LEAKS = 0
SUPERSCRIPT_FAILURES = 0
SUBSCRIPT_FAILURES = 0
FONT_FALLBACK_FAILURES = 0
```

## 7. ExamSIDE Solution & Transfer contract

Before publication, freeze the canonical required set for the topic. Each eligible external question has exactly one primary topic/concept home.

Each question must contain:

```text
question ID + source/date/shift
source badge + original source link
PRIMARY concept label
SUPPORTS prerequisite/secondary concept label(s) when needed
concept segregation label
question-family / difficulty badge
transfer badge
Core Study Guide cross-link
H0 independent attempt
H1 / H2 / H3 according to difficulty
question-specific helper when needed
misconception watch when relevant
complete solution in the same ExamSIDE PDF
```

Difficulty support:

```text
1/3 -> H1
2/3 -> H1-H2
3/3 -> H1-H3 + stronger representation/helper
```

Hints progressively reveal the route; they do not repeat the full solution.

The existing Redox ExamSIDE convention of placing full solutions in an end solution section may be retained, but Core Appendix A/B/C labels are reserved for the Core Study Guide contract.

## 8. Transfer-coverage audit

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

Reverse evidence:

```text
question -> primary topic/concept -> Core link -> badges -> hint support -> complete solution -> source link -> COMPLETE
```

## 9. Render-first QA

For both PDFs:

```text
GENERATE
-> RENDER EVERY PAGE
-> INSPECT LONGEST TITLE
-> INSPECT DENSEST CHEMISTRY PAGE
-> INSPECT APPENDIX A
-> INSPECT APPENDIX B
-> INSPECT APPENDIX C HANDOUT
-> INSPECT H1-H3 PAGE
-> INSPECT COMPLETE SOLUTION PAGE
-> INSPECT FINAL AUDIT PAGE
-> REPAIR
-> RE-RENDER
-> PASS
```

The rendered page is authoritative.

## 10. Final topic gate

Do not declare a Redox topic final until all are PASS:

```text
SOURCE = PASS
PEDAGOGY = PASS
APPENDIX_A = PASS
APPENDIX_B = PASS
APPENDIX_C_HANDOUT = PASS
TRANSFER = PASS
CONCEPT_SEGREGATION = PASS
BADGES = PASS
TYPOGRAPHY = PASS
LAYOUT = PASS
```
