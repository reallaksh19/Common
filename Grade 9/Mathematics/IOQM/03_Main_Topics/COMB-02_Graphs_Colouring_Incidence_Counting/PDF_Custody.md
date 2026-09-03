# COMB-02 PDF Custody

Status: `REPOSITORY_CUSTODY_AND_VISUAL_QA_PASS_SOURCE_Q22_PAGE_VISUAL_PENDING`

Canonical renderer: `Authoring/render_comb02_pdfs.py`
Source render commit: `1a9dec623dd5c6a2281670a8f53ad50b4c2a85b4`
Repository custody commit: `adee63ac889e9ba02377ab965f6292f26fbcd21c`
GitHub Actions run: `33740386772`
Workflow artifact digest: `sha256:08554f123128ea4f494f52384a9382a8fa855d98fa750d6013e9d4d28c75221a`

| Artifact | Pages | Bytes | SHA-256 | Git blob SHA |
|---|---:|---:|---|---|
| `PDFs/COMB02_Student_Pack_v1.pdf` | 14 | 92707 | `00508760f437f830c6cfc4aca913640f9efb45b1a2b663a25b6004b66f390007` | `a6c4bfb00f33cdfe02d3cf599928536e0e14149e` |
| `PDFs/COMB02_Teacher_Key_v1.pdf` | 6 | 80420 | `f048a33555360a0466b22e2317930944c01e3268eb5b342feeeeca312de367ea` | `1dd544493965123e94fee45be758e4520da54f6f` |

## Automated custody checks

- A4 page-count contract: PASS — student 14, teacher 6.
- open/text extraction: PASS via `pdfinfo` and `pdftotext`.
- encryption: PASS_NONE.
- canonical renderer execution in GitHub Actions: PASS.
- learner control-plane scrub on rendered student PDF: PASS_STATIC.
- repository binary commit and workflow-artifact upload: PASS.

## Exact-binary render verification

The exact PDFs committed by GitHub Actions were downloaded from workflow artifact `comb02-pdf-custody` and independently inspected.

- 200-dpi page regression against the approved final audit candidate: PASS_ZERO_DIFF — student 0/14 changed pages; teacher 0/6 changed pages.
- 200-dpi page-by-page visual inspection: PASS — student 14/14, teacher 6/6.
- clipping/overlap/broken-glyph check: PASS_NONE_FOUND.
- graph notation, degree notation, cycle/K_n notation and mathematical typography: PASS.
- accidental blank/near-empty page check: PASS_NONE_FOUND.
- final learner-facing workflow/topic-control scrub: PASS_STATIC_RENDERED.

## Independent source boundary

Exact source stems are closed 6/6. Page/figure custody is closed for all promoted learner historical anchors. `IOQM-2023-Q22` remains deliberately source-map/teacher controlled: its exact controlled stem, embedded key and independent mathematics are closed, but exact organizer page-image confirmation remains `PENDING` because the source screenshot endpoint repeatedly cache-missed.

This source-page debt is separate from the student/teacher PDF artifact gate and must remain visible in production custody.

## Evidence boundary

Classroom timing/readability, longitudinal retention, psychometric calibration, qualification/pass-mark calibration and publication approval remain `NOT_RUN`.
