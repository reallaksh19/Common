# Final PDF / Package QA

## Exact delivered PDF

File: `PDF/IOQM_Grade9_Geometry_Question_Driven_Visual_Study_Guide_v4.pdf`

- SHA-256: `8a70fc24f8356f0272023c084713b4474b9a8cbfd7d7b09c1868fdc60029b409`
- Pages: 68
- Page size: 612 x 792 pt (US Letter)
- PDF version: 1.7
- Encrypted: no
- Openable with PyMuPDF: yes
- Likely scanned: no
- XFA: none

## Content hard gate

Copied from the completed self-sufficiency audit:

```text
QUESTION_INVENTORY = PASS_52_OF_52
QUESTION_TO_METHOD_MATRIX = PASS_52_OF_52
ORPHAN_METHOD_AUDIT = PASS_52_OF_52
VISUAL_PEDAGOGY_AUDIT = PASS_52_OF_52
APPENDIX_A_CUSTODY = PASS_52_OF_52
APPENDIX_A_HINT_AUDIT = PASS_52_OF_52
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_52_OF_52
ORPHAN_METHODS = 0
VISUAL_PEDAGOGY_GAPS = 0
ADVANCED_BRIDGES_REQUIRED = ADVANCED_BRIDGES_PRESENT
PDF_GENERATION_ALLOWED = TRUE
```

## Authoring-source parity

The delivered DOCX was rebuilt from the packaged `Build/` data and converted with LibreOffice 25.2.3.2.

- DOCX SHA-256: `4729c52ed74b1a38a0c82170ad21366f66c77af209105c5430eb3f692c5ed119`
- DOCX conversion page count: 68
- Render comparison between the reference 68-page PDF and the regenerated PDF at 72 dpi: **0 changed pages out of 68**.

This verifies that the packaged editable DOCX is the source for the delivered visual layout rather than an unrelated 81-page draft.

## 200-dpi final render QA

The exact delivered 68-page PDF was rendered at 200 dpi using the required render-first workflow.

- Rendered pages: 68/68
- Pixel comparison against the previously inspected 200-dpi final render set: **68/68 exact matches**
- Visual inspection status inherited from that exact-matching inspected set: **PASS_68_OF_68**
- Figure/hint layout: no known clipping, overlap, missing-figure, or unreadable-hint failures in the inspected final render set.

## Figure / hint inventory

- Stable Geometry skills: 29
- Advanced Worked Bridges: 16
- Appendix A questions: 52
- Appendix A hint depth: 12 H1; 25 H1-H2; 15 H1-H3
- Core authored figures: 16
- Appendix A authored figures: 31
- Appendix B authored figures: 7

## Scope note

The PASS claims above are static document-level QA claims only. They are not claims about classroom solve rate, retention, psychometric calibration, qualification probability, or timing.