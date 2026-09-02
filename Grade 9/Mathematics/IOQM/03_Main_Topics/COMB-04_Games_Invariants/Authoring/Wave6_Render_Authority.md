# COMB-04 Wave-6 Unified Render Authority

Status: `ACTIVE_FINAL_RENDER_AUTHORITY`

Issue: `#89`  
Owner waiver basis: `agents/chains/IOQM-G9-COMB-04-ISSUE-89/issue-basis/IB-0002.md`

## Authority rule

All final COMB-04 PDFs in this wave use one production system. No microstream-specific PDF styling is allowed.

## Render system

- source format: accepted UTF-8 Markdown;
- renderer: Pandoc -> XeLaTeX;
- page size: A4;
- margins: 16 mm;
- body font: DejaVu Sans, 10 pt;
- monospace font: DejaVu Sans Mono;
- colour links: disabled;
- mathematical notation: Unicode/source notation preserved where XeLaTeX supports it;
- page inspection renderer: repository PDF skill render helper at 150 DPI;
- structural preflight: repository PDF skill `pdf_preflight.py`.

Canonical command shape:

```text
pandoc <source.md> -o <target.pdf> \
  --pdf-engine=xelatex \
  -V papersize=a4 \
  -V geometry:margin=16mm \
  -V mainfont='DejaVu Sans' \
  -V monofont='DejaVu Sans Mono' \
  -V fontsize=10pt \
  -V colorlinks=false
```

## Final PDF set

- `PDFs/COMB-04_Concept_Map.pdf`
- `PDFs/COMB-04_Assimilation_Book.pdf`
- `PDFs/COMB-04_First_Step_Reference.pdf`
- `PDFs/COMB-04_H0_Mastery.pdf`
- `PDFs/COMB-04_Teacher_Diagnostic_Key.pdf`
- `PDFs/COMB-04_Complete_Learner_Pack.pdf`

## Source mapping

- Concept Map PDF: student-safe render derivative of `00_Concept_and_Dependency_Map.md`; issue/wave/blob/provider controls are removed while the learner router, state model, proof contracts, boundaries, contrasts and self-check are preserved.
- Assimilation Book PDF: `02_Assimilation_Book.md`.
- First-Step Reference PDF: `03_First_Step_Reference.md`.
- H0 Mastery PDF: `06_H0_Mastery_Test.md` with the first attempt unlabelled and unhinted.
- Teacher Diagnostic PDF: `Teacher_Diagnostic_Key.md`; teacher-only labels and the Owner-waiver disclosure are permitted here.
- Complete Learner Pack PDF: student-safe Concept Map + `02` + `03` + `04` + `05` + `06`, with hard page breaks between major artifacts.

## Leakage policy

Learner PDFs must contain none of:

- GitHub Issue/PR controls;
- Wave labels;
- agent/interface names;
- chain endpoint/sync IDs;
- blob hashes;
- Owner-waiver/process text;
- F0/F1/F2/F3/F4/XF teacher progression labels;
- teacher item IDs.

Historical stable source IDs such as `IOQM-2025-Q22` are allowed where pedagogically useful.

## Historical figure custody

The 2023 Q28 historical figure is not reconstructed or represented as an exact official figure in this render set.

## Validation truth

`WAVE5_INDEPENDENT_QA_PASS` remains `NOT_ASSERTED`. Fresh-reviewer separation was explicitly waived by the Owner in `IB-0002`. The same-custodian second pass recorded `NO_DEFECT_FOUND`; this render authority does not relabel it as independent.

Wave-6 render/preflight/page-inspection gates themselves are not waived and must pass before endpoint acceptance.
