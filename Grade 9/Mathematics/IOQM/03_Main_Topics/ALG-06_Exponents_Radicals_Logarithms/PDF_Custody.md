# ALG-06 PDF Custody

Status: `REPOSITORY_CUSTODY_AND_VISUAL_QA_PASS`

Canonical renderer: `Authoring/render_alg06_pdfs.py`
Source render commit: `f4f1a624e389fbfe27dfe47eea1d8efe649f7c10`
Repository custody commit: `2b15b1cec36c5ac10234e4045215f1003fee3cd1`
GitHub Actions run: `33733799950`
Workflow artifact digest: `sha256:f596a2ca88b1a880e66c605a061dffa9ad71fbcc3e1b5a0cec9a9b27b252cd67`

| Artifact | Pages | Bytes | SHA-256 | Git blob SHA |
|---|---:|---:|---|---|
| `PDFs/ALG06_Student_Pack_v1.pdf` | 14 | 94501 | `dc25052968066c9a551027a14043a40a234be3a9fe8ca75d98e68021a926e815` | `4897fd2ea15bd85b6487edefed9a6bd669c82688` |
| `PDFs/ALG06_Teacher_Key_v1.pdf` | 5 | 70951 | `4f215572363694afc94cab5ab9b674c73b4d3fcfc228b1f2a5494d218f1db411` | `442693a4fffce345aac3f1fe15389cd0c6214a1c` |

## Automated custody checks

- A4 page-count contract: PASS — student 14, teacher 5.
- open/text extraction: PASS via `pdfinfo` and `pdftotext`.
- encryption: PASS_NONE.
- canonical renderer execution in GitHub Actions: PASS.
- learner control-plane scrub on rendered student PDF: PASS_STATIC.
- repository binary commit and artifact upload: PASS.

## Exact-binary render verification

The exact PDFs committed by GitHub Actions were downloaded from workflow artifact `alg06-pdf-custody` and independently inspected.

- 120-dpi render regression against the previously approved local reference: PASS_ZERO_DIFF — student 0/14 changed pages; teacher 0/5 changed pages.
- 200-dpi page-by-page inspection of exact custody binaries: PASS — student 14/14, teacher 5/5.
- clipping/overlap/broken-glyph check: PASS_NONE_FOUND.
- radical/logarithm notation rendering: PASS.
- accidental blank/near-empty page check: PASS_NONE_FOUND.
- final learner-facing workflow/topic-control scrub: PASS_STATIC_RENDERED.

## Evidence boundary

This closes the **static artifact custody/render gate** only. Classroom timing/readability, longitudinal retention, psychometric calibration, qualification/pass-mark calibration, and publication approval remain `NOT_RUN`.
