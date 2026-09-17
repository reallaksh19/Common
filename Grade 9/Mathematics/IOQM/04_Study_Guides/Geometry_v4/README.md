# IOQM Grade 9 Geometry — Question-Driven Visual Study Guide v4

Repository source/data package for the Grade 9 IOQM Geometry rebuild produced against the question-driven study-guide contract merged through PR #140.

## Saved learner/build data

The repository copy keeps the auditable text/data layer that defines the guide:

- `Build/questions_part1.json` … `Build/questions_part4.json` — all 52 supplied Appendix A questions, exact v4 statements, stable skill routing, adaptive hint depth, H1/H2/H3 text, answers, figure requirements, and support status.
- `Build/geometry_skill_content_part1.json` … `Build/geometry_skill_content_part3.json` — the 29 stable Geometry skill cards used in the learner guide.
- `Build/geometry_bridges_content.json` — all 16 non-identical Advanced Worked Bridges.
- `Build/appendixB_v4.json` — the 20-question Appendix B mixed-transfer/audit set.

## Visual data

- `Figures/manifest.json` — figure-to-core/question/Appendix-B mapping used by the build.
- The complete release package contains the corresponding authored PNG assets. The GitHub connector used for this save supports UTF-8 repository writes, so the repository records the visual manifest, mathematical obligations, and final binary identities while the PDF/DOCX/PNG binaries remain in the complete release artifact.

## Review/audit

- `Review/Question_to_Method_Matrix.md`
- `Review/Self_Sufficiency_Audit.md`
- `Review/Appendix_B_Method_Coverage.md`
- `Review/Sources_and_Citations.md`
- `Review/PR140_Alignment.md`
- `QA/QA.md`

## Release identity

Final PDF from the complete package:

- File: `IOQM_Grade9_Geometry_Question_Driven_Visual_Study_Guide_v4_FINAL.pdf`
- Pages: 68
- Page size: US Letter
- SHA-256: `8a70fc24f8356f0272023c084713b4474b9a8cbfd7d7b09c1868fdc60029b409`

Editable DOCX:

- File: `IOQM_Grade9_Geometry_Question_Driven_Visual_Study_Guide_v4_FINAL.docx`
- SHA-256: `4729c52ed74b1a38a0c82170ad21366f66c77af209105c5430eb3f692c5ed119`

Complete binary release package generated in the authoring run:

- `IOQM_Grade9_Geometry_v4_Complete_Package.zip`
- Contains PDF, editable DOCX, 55 authored figure PNGs, build scripts/data, source-custody PDF, review files, and final QA records.

## Static gate status

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
```

The optional 72-Hour Exam Navigator is not included because short-horizon mode was not requested for this build.