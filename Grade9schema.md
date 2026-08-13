# Grade 9 Learning Content & Question-Bank Production Schema

**Status:** General reusable production standard  
**Default core-bank size:** 30 questions (user may override)  
**Default next-level appendix:** 20 questions (user may override)  
**Primary use cases:** Grade 9 advanced mathematics/science learning material, competitive-foundation problem banks, source-grounded study guides, and textbook-quality PDF production.

---

## 1. Purpose

This schema defines a repeatable process for turning a user-supplied source (PDF, image, notes, question sheet, textbook excerpt, syllabus, or past paper) into:

1. a **source-faithful anchor set**;
2. a **difficulty-calibrated question bank**;
3. pedagogical enrichment (**concepts, helpers, progressive hints, misconceptions, diagnostics, worked solutions, transfer questions**);
4. a **next-level challenge appendix**;
5. a **textbook-quality PDF** with visual QA;
6. a **provenance register** separating uploaded-source content, verified web/PYQ content, and newly authored questions.

The process is intended to be general. The worked examples below use the user-uploaded **`Sequence and series - Math.pdf`** (20 seed questions on pages 1-2) as a calibration case.

---

## 2. Non-negotiable principles

### 2.1 Source fidelity first

Do not silently repair, reinterpret, or replace a source question.

For each extracted question assign one of:

- `VERIFIED_TRANSCRIPTION` - notation is clear and faithfully transcribed.
- `RECONSTRUCTED` - scan/OCR is ambiguous; a mathematically consistent reconstruction is stated explicitly.
- `QC_ALERT` - wording is mathematically defective, incomplete, or internally inconsistent.
- `SOURCE_UNRESOLVED` - do not use as a scored question until resolved.

If a source item is defective, retain the source wording in the provenance record and explain the defect. Do not make the corrected version look like the original.

### 2.2 Difficulty is a cognitive profile, not a label

Do not match questions by `Easy / Medium / Hard` alone. A routine algebra-heavy question is not equivalent to a recognition-heavy contest problem even if both feel time-consuming.

### 2.3 Web search is for retrieval, provenance, and calibration

Use web search to:

- identify an exact PYQ/source when possible;
- find independent analogues;
- verify expected exam level;
- cross-check ambiguous source items;
- find authoritative syllabus/past-paper context.

Do **not** copy large commercial question banks verbatim into the produced book. Prefer:

- user-supplied questions (may be reproduced because the user supplied them);
- official/public exam questions when appropriate and with provenance;
- newly authored questions calibrated from mathematical archetypes;
- concise paraphrase/metadata for commercial-source analogues.

### 2.4 Provenance classes must never be mixed

Every question stores one of:

- `USER_UPLOADED_ANCHOR`
- `OFFICIAL_PYQ`
- `SECONDARY_VERIFIED_PYQ`
- `PUBLISHED_REFERENCE`
- `ORIGINAL_CALIBRATED`
- `RECONSTRUCTED_FROM_SCAN`

The student edition may show a simplified label, but the master data must keep the exact class.

### 2.5 The PDF is a rendered product, not just exported text

Textbook-quality means typography, spacing, hierarchy, equations, callouts, page rhythm, and QA. Every final PDF must be rendered to page images and visually inspected before delivery.

---

## 3. Inputs

Minimum input:

```yaml
subject: Mathematics
level: Grade 9 / competitive foundation
chapter: Sequences and Series
source_files:
  - Sequence and series - Math.pdf
core_question_count: 30       # default; user may specify any number
challenge_question_count: 20  # default; user may override
output:
  - question_bank_pdf
  - textbook_chapters_pdf
  - source_provenance
```

Optional controls:

```yaml
target_exam_style: JEE Foundation / JEE Main / JEE Advanced / Olympiad / School HOTS
solution_depth: concise | full | teacher
hint_levels: 3 | 4 | 5
include_misconceptions: true
include_transfer_questions: true
include_mixed_tests: true
student_or_teacher_edition: student
```

---

## 4. Stage A - Source ingestion and visual extraction

### 4.1 Always inspect rendered pages

For scanned/image PDFs, visual page rendering is authoritative. OCR/text extraction is only an aid.

Workflow:

```text
Source PDF/image
  -> render pages
  -> inspect equations and notation visually
  -> transcribe
  -> compare transcription against source image
  -> assign transcription confidence/status
```

### 4.2 Extract each question into a seed record

Example:

```json
{
  "seed_id": "SEQ-012",
  "source_page": 2,
  "source_question_number": 12,
  "provenance_class": "USER_UPLOADED_ANCHOR",
  "transcription_status": "VERIFIED_TRANSCRIPTION",
  "raw_question": "...",
  "notes": "Function f is positive and multiplicative; a_i are in AP."
}
```

### 4.3 Editorial QC gate

Before enrichment, check:

- missing superscripts/subscripts;
- ambiguous `+/-` signs;
- `R` versus `R+`;
- summation limits;
- strict versus non-strict inequalities;
- denominator grouping;
- whether an integer answer is actually attainable;
- whether the continuation pattern of a series is uniquely defined.

**Example from the Sequence & Series seed:** one triangle-expression item has a strict upper bound but appears to expect the unattainable endpoint. Such an item must be tagged `QC_ALERT`, not silently accepted.

---

## 5. Stage B - Mathematical fingerprinting

Each anchor question receives a mathematical fingerprint.

### 5.1 Fingerprint fields

```json
{
  "chapter": "Sequences and Series",
  "primary_topic": "Geometric Progression",
  "secondary_topics": ["Polynomial roots", "Vieta relations"],
  "mechanisms": [
    "roots constrained to GP",
    "symmetric GP parametrisation",
    "reciprocal-root relation"
  ],
  "answer_type": "numerical",
  "hidden_structure": "odd-length GP represented around middle term",
  "minimum_expert_path": [
    "represent five GP roots symmetrically",
    "use sum of roots",
    "use sum of reciprocals",
    "eliminate common symmetric factor",
    "recover product of roots"
  ]
}
```

### 5.2 Archetype naming

Use stable machine-readable archetypes, e.g.:

```text
POLYNOMIAL_ROOTS_IN_GP
AP_GP_EQUAL_SUM_INTEGER_FILTER
ARITHMETIC_GEOMETRIC_INFINITE_SERIES
RECURRENCE_ZERO_SECOND_DIFFERENCE
FUNCTIONAL_EQUATION_AP_TO_GP
PARTIAL_SUM_TO_TERM_DIFFERENCE
HP_RECIPROCAL_AP
DOUBLE_SUM_SYMMETRY
```

These archetypes power retrieval, question generation, adaptive practice, and analytics.

---

## 6. Stage C - Difficulty calibration

### 6.1 Difficulty vector

Score each dimension from 0-10:

```json
{
  "conceptual": 8.5,
  "recognition": 9.0,
  "reasoning_steps": 8.0,
  "algebra": 6.5,
  "hidden_structure": 9.0,
  "constraints_cases": 8.0,
  "calculation_burden": 5.0,
  "trap_density": 8.0
}
```

`calculation_burden` is stored but should not dominate difficulty.

### 6.2 Composite difficulty

Recommended internal score:

\[
D=0.25C+0.25R+0.15S+0.15A+0.10H+0.10K
\]

where:

- `C` = conceptual demand
- `R` = recognition/non-obviousness
- `S` = reasoning-step depth
- `A` = algebraic demand
- `H` = hidden structure
- `K` = constraints/case handling

### 6.3 Core-bank acceptance window

For an anchor difficulty `D_A`, an equivalent-level core candidate should normally satisfy:

\[
D_A-0.4 \le D_Q \le D_A+0.4
\]

This numeric window is **necessary but not sufficient**. Reject a candidate if its cognitive profile is materially different.

Example rejection:

```text
Anchor: recognition 9.0, algebra 6.5
Candidate: recognition 5.0, algebra 9.5

Result: REJECT even if the overall average is similar.
```

### 6.4 Next-level challenge target

For a challenge paired to an anchor:

\[
D_H \approx D_A+0.8 \text{ to } D_A+1.3
\]

Raise difficulty by:

- hiding the representation;
- adding one concept bridge;
- requiring one extra inference/elimination;
- interacting constraints;
- asking for a less direct symmetric/derived target.

Do **not** raise difficulty primarily by ugly arithmetic or excessive expansion.

---

## 7. Stage D - Web retrieval

### 7.1 Search by mathematical fingerprint, not chapter title

Weak query:

```text
sequence and series hard questions
```

Strong queries:

```text
"roots are in geometric progression" polynomial Vieta JEE
"f(x+y)=f(x)f(y)" arithmetic progression JEE
"sum of first n terms" "6n^3" sequence
"arithmetic geometric series" weighted powers JEE
"harmonic progression" reciprocal arithmetic progression JEE
```

### 7.2 Query expansion

For each anchor generate 5-10 retrieval queries:

1. exact distinctive phrase search;
2. mechanism search;
3. alternate terminology (`G.P.` / `geometric progression`);
4. source-restricted search;
5. exam/year query when clues exist.

### 7.3 Source preference order

1. **Official exam/syllabus source** - e.g. JEE Advanced official past papers, NTA JEE Main archive.
2. **Government/academic learning platform** - e.g. SATHEE (IIT Kanpur / Ministry of Education ecosystem).
3. **Recognized coaching/education repositories** - useful for discovery and solution cross-checking.
4. **General web mirrors/forums** - discovery only; independently verify before assigning provenance.

### 7.4 Similarity classes

```text
A - Near twin
    Same mathematical engine; different numbers/context.

B - Structural analogue
    Same core reasoning; different surface form.

C - Concept reinforcement
    Same concept; slightly easier or more explicit.

D - Advanced transfer
    Same underlying idea plus an additional inference/bridge.
```

### 7.5 Web retrieval record

```json
{
  "anchor_id": "SEQ-012",
  "candidate_url": "https://jeeadv.ac.in/past_qps/2025_1_English.pdf",
  "source_authority": "OFFICIAL_EXAM",
  "match_type": "EXACT_PYQ",
  "verified": true,
  "notes": "Official JEE Advanced 2025 Paper 1, Mathematics Q12."
}
```

---

## 8. Stage E - Core question-bank construction

### 8.1 Default size policy

**Default core = 30 questions.**  
If the user specifies another count, the user count wins.

For a 20-anchor upload, the recommended 30-question core is:

```text
20 uploaded anchor questions
+ 10 original calibrated same-level questions
= 30 core questions
```

If some anchors are unusable (`QC_ALERT` or unresolved scan), replace them with calibrated originals but retain the original source items in the provenance appendix.

### 8.2 Why not automatically create five variants per anchor?

A very large bank can dilute quality and drift in difficulty. The 30-question cap forces selection. Prefer fewer, high-fidelity questions with strong solution and hint design.

### 8.3 Selection balance

Across the 30 core questions:

- preserve the concept weighting of the anchors;
- avoid repeated surface forms;
- include multiple answer formats when appropriate;
- keep difficulty near the uploaded-question distribution.

Suggested relationship mix for the **new** questions:

```text
40% near twins
40% structural variants
20% same-level transfer
```

### 8.4 Original calibrated questions

When web material is used for calibration but the bank question is newly authored:

```json
{
  "provenance_class": "ORIGINAL_CALIBRATED",
  "calibrated_against": ["SEQ-001", "JEE Advanced/PYQ archetype corpus"],
  "copied_from_web": false
}
```

This avoids turning the output into a scraped commercial question bank.

---

## 9. Stage F - Next-level appendix

Default: **20 challenge questions**, one paired to each anchor when there are 20 anchors.

```text
H01 -> anchor SEQ-001
H02 -> anchor SEQ-002
...
H20 -> anchor SEQ-020
```

Challenge rules:

- preserve the same conceptual lineage;
- target +0.8 to +1.3 difficulty points;
- reduce initial scaffolding;
- add synthesis, not arithmetic clutter;
- provide separate hints and solutions after the full challenge set.

Recommended challenge-book order:

```text
Appendix A - H01-H20 Questions
Appendix B - Progressive Hints
Appendix C - Worked Solutions / Answer Key
Appendix D - Anchor-to-Challenge Map
```

---

## 10. Stage G - Pedagogical enrichment schema

A high-quality question object contains more than `question + answer + solution`.

### 10.1 Canonical enriched object

```json
{
  "id": "SEQ-012",
  "provenance": {},
  "classification": {},
  "difficulty": {},
  "concepts": [],
  "prerequisites": [],
  "concept_trigger": "",
  "what_to_notice": [],
  "helper": {},
  "hints": [],
  "misconceptions": [],
  "error_signatures": [],
  "solution": {},
  "takeaway": "",
  "transfer_question": "",
  "similar_questions": []
}
```

### 10.2 Concepts

Concepts answer:

> What mathematical knowledge does this problem exercise?

Example:

```text
Primary:
- geometric progression
- Vieta relations

Supporting:
- symmetric functions
- reciprocal roots

Prerequisites:
- polynomial coefficients
- exponent laws
```

### 10.3 `What should I notice?`

This is a recognition layer, not a solution.

Example:

```text
- Five roots are constrained to one GP.
- The target is a coefficient, not the roots themselves.
- Both the root sum and reciprocal-root sum are symmetric expressions.
```

### 10.4 Helper

A helper answers:

> What should I think about first?

It should not give away the setup.

Recommended types:

```json
{
  "observation": "Which condition reduces the number of independent variables?",
  "representation": "Can the terms be represented around a central term?",
  "connection": "Which theorem links roots and coefficients?"
}
```

### 10.5 Progressive hints

Use 4-5 levels.

```json
[
  {"level": 1, "reveal": 10, "type": "direction", "text": "Exploit the progression first."},
  {"level": 2, "reveal": 25, "type": "concept", "text": "Use a symmetric GP representation."},
  {"level": 3, "reveal": 45, "type": "connection", "text": "Translate the coefficient with Vieta."},
  {"level": 4, "reveal": 70, "type": "setup", "text": "Write the reciprocal sum over the product."},
  {"level": 5, "reveal": 90, "type": "near_solution", "text": "Eliminate the shared symmetric factor."}
]
```

A student who solves after H1 demonstrates more mastery than one who needs H5. Store hint usage in digital implementations.

### 10.6 Misconceptions

Misconceptions must be **specific wrong mental models**, not `be careful` comments.

Example:

```json
{
  "id": "GP-VIETA-RECIP-01",
  "wrong_model": "sum(1/r_i) = 1/sum(r_i)",
  "diagnostic": "Test the claim with 2 and 3.",
  "repair": "Use a common denominator / elementary symmetric functions."
}
```

### 10.7 Error signatures

These support intelligent tutoring.

```json
{
  "trigger": "Student replaces reciprocal sum by reciprocal of root sum",
  "micro_intervention": "1/2 + 1/3 is not 1/(2+3).",
  "recovery_hint": "Express the reciprocal sum using the product of roots."
}
```

### 10.8 Solution architecture

Recommended layers:

```text
Strategy (3-6 steps)
-> compact derivation
-> full worked solution
-> alternative method (when genuinely useful)
-> exam shortcut
-> verification
```

### 10.9 Transfer question

Every strong anchor should have one short transfer prompt testing whether the idea transfers to a changed representation.

---

## 11. Stage H - Textbook-quality PDF design

### 11.1 Visual benchmark

A textbook-quality benchmark used in this project is the *Progress in Mathematics* viewer. The goal is **not to copy its artwork or page design**. Extract only high-level publishing principles:

- clear hierarchy;
- purposeful whitespace: use breathing room, but convert large unused regions into working space, reflection, practice previews, diagnostics, or navigation;
- consistent chapter/page furniture;
- color-coded instructional layers;
- short blocks instead of uninterrupted text;
- examples and practice visually separated;
- strong page-number/navigation discipline.

Reference: `https://secure.viewer.zmags.com/publication/d804a52f#/d804a52f/32`

### 11.2 Recommended linked page system

The textbook and question bank should be two views of one canonical concept/question graph. Use stable IDs (for example `SEQ-C01`) rather than page numbers as the semantic authority.

For a Grade 9 concept hub, prefer a compact 1-2 page learning loop:

```text
YOUR MISSION (anchor problem / phenomenon)
-> SPOT THE PATTERN
-> TOOLBOX
-> FIRST MOVE
-> concise SOLUTION TRAIL / worked anchor
-> WHY IT WORKS
-> MISCONCEPTION CLINIC
-> TRY NOW (same-level practice)
-> LEVEL UP PREVIEW
-> EXIT TICKET
-> purposeful WORK ZONE
```

For a compact question bank:

```text
Mastery / concept map
Core bank (user count; default 30)
Mixed mastery tests (reuse core IDs; do not reveal concept before attempt)
Diagnosis map -> exact concept IDs
Next-level challenge bank
Helper / hint map
Answers + solution paths
Misconception clinic
Source / QC / provenance register
```

The integrated edition is the canonical interactive PDF: concept links must jump to practice/challenge; every bank question must return to its primary concept; mixed-test diagnosis, hints, answers, and misconceptions should also route to the relevant concept/question. Standalone textbook and bank files may use stable IDs instead of cross-document links.

#### Page-density rule

Do not optimize for a fixed percentage mechanically. The practical rule is **no accidental blank zones**. Large remaining regions must have an instructional purpose, such as:

- ruled or grid working space;
- a `First Move` or strategy scratchpad;
- a confidence / mastery check;
- a practice preview;
- a misconception diagnostic;
- a retake plan;
- concept navigation.

Avoid both extremes: report-like pages with one small box and half a page empty, and >90% visual occupancy that removes breathing room.

### 11.3 Design tokens

Store design tokens rather than hand-formatting each page:

```yaml
page: A4
margins_mm: [16, 16, 16, 16]
colors:
  navy: "#183F69"
  teal: "#1A9D9A"
  gold: "#F5C64F"
  orange: "#F28A50"
  purple: "#7B6BB1"
  light_panel: "#F3F5F7"
typography:
  heading: sans-bold
  body: readable serif/sans
  math: vector text / embedded equation glyphs
```

### 11.4 Information hierarchy

Use stable labels:

```text
QUESTION
THINK
HELP
HINTS
LEARN
MISCONCEPTION CLINIC
TRANSFER
PROVENANCE
```

### 11.5 Copyright/design rule

Do not reproduce proprietary textbook artwork, illustrations, exact page templates, or branded elements from a visual reference. Create an original design system that reaches comparable editorial quality.

---

## 12. Stage I - PDF production and QA

Use the render-check loop:

```text
Author PDF/DOCX
-> render every page to PNG
-> inspect at 100%
-> correct layout/equations
-> re-render
-> deliver only after clean visual QA
```

Minimum QA checklist:

- no clipped text;
- no equation overflow;
- no broken glyphs/black squares;
- no overlapping boxes;
- consistent headers/footers/page numbers;
- source/QC labels visible;
- answer keys match question IDs;
- all mathematical results independently recalculated;
- page images reviewed, not only PDF text extraction.

For final production, preserve source citations as normal human-readable references. Do not expose internal tool tokens.

---

## 13. Stage J - Mathematical verification

Every generated/calibrated question must pass:

1. **solvability** - sufficient data, unambiguous target;
2. **domain validity** - all denominators/logs/roots/convergence conditions valid;
3. **unique-answer check** - unless explicitly multiple-answer;
4. **independent recalculation** - preferably symbolic/numerical check when useful;
5. **difficulty re-score after solution** - difficulty often changes after the clean solution is known;
6. **hint leakage check** - H1/H2 must not collapse a high-recognition problem into routine substitution.

---

## 14. Example 1 - GP roots and Vieta

### Anchor fingerprint

```yaml
archetype: POLYNOMIAL_ROOTS_IN_GP
concepts:
  - geometric progression
  - Vieta relations
  - reciprocal roots
recognition: 9.0
algebra: 6.5
hidden_structure: 9.0
```

### Helper

> Can five GP roots be represented so their product is controlled by one central term?

### Progressive hints

```text
H1: Do not solve five roots independently.
H2: Use a symmetric five-term GP.
H3: The root sum and reciprocal-root sum contain the same symmetric factor.
H4: Eliminate that factor to obtain the square of the middle term.
H5: Use the product of roots for the constant coefficient.
```

### Misconception

```text
Wrong:  sum(1/r_i) = 1/sum(r_i)
Repair: express the reciprocal sum with a common denominator/product of roots.
```

### Same-level original calibration example

> The five nonzero roots of a monic fifth-degree polynomial are in GP. The coefficient of `x^4` is `-54`, and the sum of the reciprocals of the roots is `6`. Find the magnitude of the constant term.

This is newly authored but preserves the same engine: symmetric GP + Vieta + reciprocal relation.

---

## 15. Example 2 - Functional equation turns AP into GP

The uploaded Sequence & Series anchor corresponding to this archetype was independently identified as **JEE Advanced 2025 Paper 1, Mathematics Q12**.

Official source: `https://jeeadv.ac.in/past_qps/2025_1_English.pdf`

Fingerprint:

```text
f(x+y)=f(x)f(y), f>0
+ arguments a_i in AP
=> f(a_i) is a GP
=> use a ratio condition and finite-GP sums
```

Key misconception:

> Treating `f(a_i)` as another AP because `a_i` is AP. The multiplicative functional equation converts equal additive increments into a constant multiplicative ratio.

---

## 16. Example 3 - Partial sums reveal terms

Seed mechanism:

```text
S_n known explicitly
=> a_n = S_n - S_{n-1}
=> differences of a_n simplify
=> requested sum collapses to a standard power sum
```

Helper:

> If the cumulative sum is known, can you recover one term without finding the whole sequence recursively?

Typical misconception:

> Substituting `S_n` as though it were `a_n`.

---

## 17. Example 4 - Source QC and reconstruction

If the scan has ambiguous signs in a displayed infinite series:

1. retain a crop/page reference;
2. transcribe what is unambiguous;
3. search exact fragments on the web;
4. if an established version is found, label the bank item `RECONSTRUCTED`;
5. state the assumed pattern before solving;
6. do not claim the reconstruction is identical to the upload unless verified.

This was necessary for some faint items in the Sequence & Series source.

---

## 18. Recommended master JSON shape

```json
{
  "bank": {
    "id": "G9-MATH-SEQUENCES-V1",
    "subject": "Mathematics",
    "grade": 9,
    "chapter": "Sequences and Series",
    "core_limit": 30,
    "challenge_limit": 20,
    "source_set": [],
    "questions": [],
    "difficulty_policy": {
      "core_delta": 0.4,
      "challenge_delta_min": 0.8,
      "challenge_delta_max": 1.3
    },
    "design_system": {},
    "qa": {},
    "references": []
  }
}
```

Per-question:

```json
{
  "id": "SEQ-012",
  "role": "ANCHOR",
  "provenance": {
    "class": "USER_UPLOADED_ANCHOR",
    "source": "Sequence and series - Math.pdf",
    "page": 2,
    "external_verification": [
      {
        "type": "OFFICIAL_PYQ",
        "url": "https://jeeadv.ac.in/past_qps/2025_1_English.pdf",
        "note": "JEE Advanced 2025 Paper 1 Q12"
      }
    ]
  },
  "classification": {},
  "difficulty": {},
  "question": "...",
  "concepts": [],
  "helper": {},
  "hints": [],
  "misconceptions": [],
  "solution": {},
  "answer": "96",
  "transfer": "..."
}
```

---

## 19. Recommended production sequence

```text
1. Read/render uploaded source.
2. Extract anchors with QC status.
3. Solve anchors independently.
4. Build fingerprints and difficulty vectors.
5. Search web for provenance + analogues.
6. Verify exact PYQs against official sources where available.
7. Select/generate core bank up to 30 (or user count).
8. Score all candidates against anchors; reject drift.
9. Generate up to 20 next-level questions.
10. Verify every answer and domain.
11. Add concepts/helpers/hints/misconceptions/solutions.
12. Lay out textbook PDF with original design system.
13. Render every PDF page and inspect.
14. Fix defects and re-render.
15. Publish final PDF + provenance register + schema/master data.
```

---

## 20. Current Sequence & Series calibration sources

These are examples used during development of this schema; future topics should build their own source register.

### User-provided anchor source

- `Sequence and series - Math.pdf` - pages 1-2 contain 20 advanced Sequence & Series seed questions; later pages contain supporting AP/GP/HP notes and worked examples.

### Official / high-authority web references

- JEE Advanced 2025 Paper 1 (official):  
  `https://jeeadv.ac.in/past_qps/2025_1_English.pdf`
- JEE Main / NTA syllabus and question-paper archive entry point:  
  `https://jeemain.nta.nic.in/`
- SATHEE JEE chapter-wise Sequence & Series PYQs:  
  `https://sathee.iitk.ac.in/pyqs/jee/chapterwise/mathematics/sequence-series/`

### Discovery / secondary verification examples

- ALLEN question/solution pages: `https://allen.in/`
- ExamSIDE Sequence & Series PYQ index:  
  `https://questions.examside.com/past-years/jee/jee-advanced/mathematics/sequences-and-series`
- Archive.org text copy of a published high-school problem book containing the 109/100 GP block problem:  
  `https://archive.org/stream/prilepkoproblembookinhighschoolmathematics/Prilepko-Problem-Book-In-High-School-Mathematics_djvu.txt`

### Textbook-layout quality reference

- Progress in Mathematics viewer:  
  `https://secure.viewer.zmags.com/publication/d804a52f#/d804a52f/32`

**Important:** secondary sites are useful for discovery but do not outrank an official paper when an official source exists.

---

## 20A. Proven linked textbook/question-bank architecture

The Sequence & Series v3 implementation established a reusable linked-learning pattern. Treat the metrics below as an implementation example, not universal page-count requirements.

### 20A.1 Canonical graph

```text
Concept ID
  <-> uploaded/source anchor
  <-> same-level calibrated practice
  <-> next-level challenge
  <-> helper / hints
  <-> misconception diagnostic
  <-> answer / solution path
  <-> mixed-test diagnosis
```

Question-to-concept mapping may be many-to-many, but every scored question has exactly one `primary_concept_id` for navigation and analytics.

### 20A.2 Master-data authority

Generate all PDFs from a canonical JSON (or equivalent structured model), not from already-laid-out PDF pages. The model stores concept IDs, questions, difficulty vectors, prerequisites, hints, misconceptions, solutions, QC/provenance, and navigation targets. Page numbers are render outputs only.

### 20A.3 Core-bank allocation

When the core bank is smaller than a fixed number of variants per anchor, allocate the limited new questions to the concepts with the greatest need for additional practice (high recognition load, transfer value, or thin source coverage). Do not distribute mechanically.

### 20A.4 Mixed mastery

Concept-grouped practice teaches recognition but can also leak the intended method. Therefore reuse the core bank in mixed tests that hide concept labels before the attempt. After marking, provide a diagnosis map back to exact concept IDs and suggested retakes.

### 20A.5 PDF link QA

For an integrated linked edition:

1. create named/internal destinations from stable IDs;
2. generate all concept -> question/challenge links;
3. generate question/challenge -> concept return links;
4. link diagnosis, hints, answers, and misconception entries;
5. save the PDF and verify destination resolution;
6. count/inspect PDF link annotations programmatically;
7. render all pages and visually inspect them.

### 20A.6 Sequence & Series v3 implementation reference

The tested v3 example used:

- 20 exact concept hubs (`SEQ-C01` ... `SEQ-C20`);
- Core 30 = 20 uploaded anchors + 10 calibrated originals;
- 20 next-level challenges;
- three 10-question mixed mastery tests reusing Core 30 exactly once;
- a 24-page standalone student textbook;
- a 22-page standalone question bank;
- a 44-page integrated edition with more than 400 internal navigation annotations.

The page counts are not targets. The reusable requirements are stable IDs, purposeful page density, bidirectional concept/practice navigation, source/QC visibility, and render/link QA.

---

## 21. Definition of done

A bank is complete only when:

- [ ] source questions have transcription/QC status;
- [ ] all core questions satisfy the specified count (default 30);
- [ ] difficulty drift has been checked against anchors;
- [ ] next-level questions meet the stated difficulty delta;
- [ ] every answer has been recalculated;
- [ ] helpers do not leak the solution;
- [ ] misconceptions are problem-specific;
- [ ] provenance class is present for every item;
- [ ] copyrighted web material is not bulk-copied;
- [ ] the final PDF uses an original visual design;
- [ ] every PDF page has been rendered and visually inspected;
- [ ] QC alerts/reconstructions are visible to the reader;
- [ ] answer keys and IDs are consistent;
- [ ] every scored bank question has a primary concept ID;
- [ ] integrated-edition concept/practice/challenge return links have been verified;
- [ ] large whitespace regions are purposeful rather than accidental;
- [ ] mixed-test diagnosis routes learners back to exact concepts.

---

## 22. Versioning

Recommended semantic versioning for the bank/schema:

```text
v1.0 - source extraction + core bank + answers
v1.1 - pedagogical enrichment
v1.2 - challenge appendix
v1.3 - mixed mastery tests
v2.0 - adaptive/digital tutor instrumentation
```

When a source transcription or answer changes, record the change explicitly; do not silently replace previously published content.
