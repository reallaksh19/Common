---
name: grade9-question-bucket-builder
description: Convert Grade 9 mathematics source questions into concept-first buckets with pattern analysis, solved anchor questions, extensions, CBSE/IOQM/IMO-style transfer variants, source citations, and PDF-ready layout contracts.
---

# Grade 9 Question Bucket Builder Skill

## Purpose

Use this skill when the user asks to analyse a Grade 9 Mathematics question set by pattern, group questions into concept buckets, create source-traced question-bank pages, or produce PDF-ready concept-bucket material.

This skill is separate from a general `grade9-math` skill because its primary object is not a chapter or formula list. Its primary object is the **question-pattern bucket**:

```text
SOURCE QUESTIONS
  -> PATTERN FAMILY
  -> CORE QUESTION
  -> CONCEPT / APPLICATION / SOLUTION
  -> EXTENSION QUESTIONS
  -> CBSE / IOQM / IMO-FOUNDATION VARIATIONS
  -> CITED PDF / WORKBOOK PAGE
```

## Trigger phrases

Use this skill for requests such as:

- "Analyse the pattern, not just answer."
- "Crack the concept."
- "Group the questions."
- "Create Group 1 / Group 2."
- "Bucket 1 / Bucket 2."
- "Concept -> application -> solution."
- "Similar variation from CBSE / IOQM / IMO."
- "Create PDF with citations."
- "How many groups still?"

## Mandatory source rule

Do not silently replace uploaded/source questions with generic questions.

For every bucket:

1. identify the source question IDs/pages;
2. preserve the original mathematical intent;
3. state whether an extension is:
   - **Source**: directly from uploaded/source file;
   - **Adapted**: structurally similar but not verbatim;
   - **External cited**: from CBSE/NCERT/IOQM/IMO source;
   - **Author-created transfer**: generated for practice.

When an exact year/source cannot be verified, label it **adapted**, not "IOQM 2023" or "CBSE 2020".

## Core pedagogy

Follow the Grade 9 Mathematics method:

```text
SEE -> REALIZE -> UNDERSTAND -> ADOPT
```

Question-bank solving should follow:

```text
RECOGNIZE -> SOLVE -> CHECK -> TRANSFER
```

Mathematics mastery target:

```text
PATTERN -> INVARIANT -> STRUCTURE -> TRANSFER
```

## Bucket format

Every bucket must use this sequence:

```text
Group N / Bucket N — <concept title>

1. Source trace
2. Why these questions belong together
3. Core pattern
4. Anchor Question 1
   - Question
   - Concept
   - Application
   - Solution
   - Check
5. Extension of the core concept
   - Questions 2, 3, ...
   - what changes / what stays invariant
6. Similar variations
   - CBSE / NCERT-aligned
   - IOQM bridge, with exact citation if verified
   - IMO-foundation / Olympiad transfer
7. Misconceptions and traps
8. First-move recognition card
9. Exit ticket
10. Answer key / compact solutions
```

## Grouping logic

Group by **hidden invariant**, not by surface wording.

Examples:

- Line through intersection, price-demand model, collinearity, intercepts, and area with x-axis may belong together if the invariant is "straight line fixed by two independent conditions".
- Equilateral triangle third vertex belongs separately because the invariant is "rotate a segment by 60 degrees / perpendicular-bisector symmetry".
- Boat/current and plane/wind problems belong together because the invariant is "relative speed creates simultaneous linear equations".
- Fractional linear equations belong together because the invariant is "clear denominators while preserving signs".
- Parameterised ordered pairs belong together because the invariant is "decode hidden variables from coordinates/line membership".
- Redistribution word problems belong together because the invariant is "before-after conservation and balance".

## Required analysis for each source question

For each included source question, record:

```text
source_id:
page:
question_number:
surface_form:
hidden_invariant:
first_useful_line:
common_wrong_start:
solution_method:
check_method:
extension_role: anchor | direct extension | bridge | exit-ticket
```

## Citation policy

### Uploaded/source files

Cite the uploaded file or repository file line/page used to identify the source question.

### External examples

Use web or official repository sources only when the user asks for CBSE/IOQM/IMO citations or recent/current source references.

Priority order:

1. official CBSE / NCERT pages where available;
2. official HBCSE / MTAI / olympiad organizing body pages for IOQM/RMO/INMO;
3. published official PDF question papers / answer keys;
4. reputable educational sources only when official sources are not available.

Never invent year tags. Use:

- "IOQM 2023, Qxx" only after verifying the official paper;
- "IOQM-style adapted" when the structure is inspired but not a verified exact question;
- "CBSE/NCERT-aligned" when based on syllabus style, not an official past exam.

## PDF layout contract

When creating PDFs, use a clean textbook/workbook layout:

- A4 portrait by default; landscape only when diagrams/tables need it.
- Header with group number, bucket title, and source status.
- Use cards for Concept, Application, Formula/Tool, Misconception, First Move, and Exit Ticket.
- Keep source questions visibly separate from generated variations.
- Put citations/source notes at the bottom of the page or in a final reference page.
- Avoid cramped full-page algebra; split long solutions into numbered steps.
- Include at least one diagram where the concept is geometric.
- Render and inspect pages before delivery; fix clipping, blank pages, equation overflow, and unreadable text.

## Output quality gates

Before final delivery, verify:

- every source question in the selected group appears in the source trace;
- no generated variation is mislabeled as an official past-paper item;
- answers are mathematically checked;
- the bucket has one clear hidden invariant;
- the extension questions are not just repetitions of the anchor;
- the PDF has readable typography and no layout clipping;
- remaining ungrouped questions are listed separately if the whole source set is being mapped.

## Recommended group planning for uploaded mixed Grade 9 linear/geometry sets

Use this default grouping if the source resembles the current `math.pdf` mixed set:

1. **Straight line as hidden object** — line through intersection, price-demand line, graphical systems and area, collinearity, intercepts.
2. **Equilateral vertex from two coordinates** — rotation/symmetry/perpendicular-bisector structure.
3. **Relative speed as simultaneous linear equations** — boat/current and plane/wind.
4. **Fractional linear equations** — clearing denominators and sign safety.
5. **Hidden variables in coordinates** — ordered-pair parameter decoding and line membership.
6. **Redistribution before-after balance** — conservation, transfer, equalisation.
7. **Euclid foundations** — optional MCQ/definition/axiom bucket if present.

## Final response style

When reporting completion, include:

- branch/PR status if repository changes were made;
- files changed;
- whether a PDF was created;
- validation summary;
- any NOT_RUN or unverifiable citation items.
