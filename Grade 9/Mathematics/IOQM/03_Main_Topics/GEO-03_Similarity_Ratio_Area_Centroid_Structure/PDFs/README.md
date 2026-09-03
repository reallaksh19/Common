# GEO-03 PDF Custody

Canonical render inputs are the Markdown sources listed in `Authoring/render_geo03_pdfs.py`. Standard built-in Helvetica fonts are used; no external font file is embedded or distributed.

## Student pack
- file: `GEO03_Student_Pack_v1.pdf`
- pages: 7
- page size: A4, 595.276 x 841.89 pt
- bytes: 13343
- SHA-256: `15f4bed1ccc284a3d98b65db6834c5ae943a549d82f4e457a0fcd81b7365b5f3`
- expected Git blob: `a5b362c40642c763cafe6f1bf675bea640ba8f12`
- aggregate source SHA-256: `7d173876ecf448dc58aee1a57fef9caf7c08b319e4f746288a937621323dd902`

## Teacher key
- file: `GEO03_Teacher_Key_v1.pdf`
- pages: 3
- page size: A4, 595.276 x 841.89 pt
- bytes: 5517
- SHA-256: `b41b6d92891ecfdaa70c763beb7ed47ed61fc4dd9c5176481e78101e4a442ab0`
- expected Git blob: `be96696b64e9da7a0bbdbbfeaca716c85c994a03`
- aggregate source SHA-256: `3ac0113e956f0721708f9ba231b93c4ee8de07ef53db03e7c62764c95ef8a3c6`

## Renderer
- `Authoring/render_geo03_pdfs.py` SHA-256: `3b04a7d8391835b6e25a99bafa78f646a7bf09b47fbb2bdbc79298c81a40e147`

## Verification
Aggregate source hashes are SHA-256 over the rendered Markdown source bytes concatenated in renderer order (no separators).

Both PDFs pass structural preflight and were rendered at 144 dpi after the final canonical build. All 7 student pages and all 3 teacher pages were inspected individually: no clipping, overlaps, broken glyphs or missing content were found. Student PDF leakage scan for internal authoring/control codes passed. Final PDFs were regenerated after the renderer's same-length ASCII header normalization; 144-dpi renders are pixel-identical to the previously inspected canonical renders. Repository blob identity must equal the expected Git blobs above after publication.
