# ALG-03 PDF custody

The rendered student and teacher PDFs are produced from the canonical topic sources and validated by `../QA.md`.

Repository artifacts:
- `ALG03_Student_Pack_v1.pdf` — 10 A4 pages; SHA-256 `34a0ff155c3c3132aecd858145d70c3a2d72eb756bc99912b67892f1602c0713`.
- `ALG03_Teacher_Key_v1.pdf` — 3 A4 pages; SHA-256 `784a283037ef0c96ec12a6c9674693706bd2ee26fb64939482112537b87fbe52`.

Rebuild both artifacts with `python ../Authoring/render_alg03_pdfs.py`. The previously recorded hashes described unattached local files; they are superseded by these reproducible, committed-source renders.
