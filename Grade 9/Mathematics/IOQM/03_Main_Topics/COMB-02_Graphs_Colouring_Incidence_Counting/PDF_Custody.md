# COMB-02 PDF Custody

Status: `RENDERED_PREFLIGHTED_REPOSITORY_CUSTODY_PENDING_EXACT_BINARY_VISUAL_CONFIRMATION`

Canonical renderer: `Authoring/render_comb02_pdfs.py`
Source render commit: `1a9dec623dd5c6a2281670a8f53ad50b4c2a85b4`

| Artifact | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| `PDFs/COMB02_Student_Pack_v1.pdf` | 14 | 92707 | `00508760f437f830c6cfc4aca913640f9efb45b1a2b663a25b6004b66f390007` |
| `PDFs/COMB02_Teacher_Key_v1.pdf` | 6 | 80420 | `f048a33555360a0466b22e2317930944c01e3268eb5b342feeeeca312de367ea` |

Automated checks in this run:
- A4 page-count contract: PASS (student 14, teacher 6)
- open/text extraction: PASS via `pdfinfo` and `pdftotext`
- encryption: PASS_NONE
- learner control-plane scrub: PASS_STATIC
- exact repository binary visual inspection: PENDING until artifact retrieval and page-render inspection

Independent source note: exact stems are closed 6/6; exact page-image confirmation for `IOQM-2023-Q22` remains a separate fail-closed source gate.

Classroom timing/readability, retention, psychometrics, qualification/pass-mark calibration, and publication approval remain `NOT_RUN`.
