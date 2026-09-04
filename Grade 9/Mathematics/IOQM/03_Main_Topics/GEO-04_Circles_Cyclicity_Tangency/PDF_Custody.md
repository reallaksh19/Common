# GEO-04 PDF Custody

Status: `BENCHMARK_PDF_CUSTODY_PASS`

Canonical renderer: `Authoring/render_geo04_pdfs.py`
Repository binary custody commit: `9b750a7e0e20360a8ca9a90ff6f127fc9fe87110`

| Artifact | Pages | Bytes | SHA-256 | Git blob |
|---|---:|---:|---|---|
| `PDFs/GEO04_Student_Pack_v1.pdf` | 17 | 112973 | `bad005c652f06b4592692e4bdc7db9244c747446aaf1ac9a682c6e0c25c10d7d` | `2a80f6e9677c33316875d95f455d6f75053358a9` |
| `PDFs/GEO04_Teacher_Key_v1.pdf` | 6 | 69061 | `f142ea31e7ce6d119bfe527bbc321bd09bf9cee1b0b147c6f5276b60ca68f157` | `51b42741250544e946cf2b22aa332dccf4d45b70` |

## Custody checks
- A4/page-count contract: PASS — student 17, teacher 6.
- open/text extraction: PASS.
- encryption: PASS_NONE.
- learner control-plane scrub: PASS.
- exact repository-binary visual inspection: PASS — 17/17 student pages and 6/6 teacher pages inspected at 200 dpi.
- render regression against the approved corrected candidate: PASS — 0/17 student pages changed and 0/6 teacher pages changed.
- historical source-page custody: PASS 5/5; exact inspected historical problem pages are text-only, so no printed historical figure requires redraw custody.
- `IOQM-2025-Q23`: canonical non-degenerate reading preserved; the rejected degenerate interpretation is not promoted.

Classroom timing/readability, retention, psychometrics, qualification/pass-mark calibration, and publication approval remain `NOT_RUN`.
