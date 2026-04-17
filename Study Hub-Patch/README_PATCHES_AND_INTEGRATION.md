# Study Hub Patch Lineage and Integration README

This document consolidates the patch history so you do **not** need to guess which ZIP should be applied in what order.

## Recommended rule

If you are starting fresh, use the **latest consolidated codebase** rather than trying to stack older patch ZIPs by hand.

Recommended base for future work:

* `StudyHub-consolidated-with-docs-and-sample-pack.zip` (created in this run)

### What this final consolidation adds

* `README\_PATCHES\_AND\_INTEGRATION.md`
* `OPTICS\_SAMPLE\_PACK\_GUIDE.md`
* `OPTICS\_SAMPLE\_PACK\_TEST\_RESULTS.md`
* `sample-packs/physics-optics-sample-pack.zip`
* `scripts/sample\_pack\_import\_smoke\_test.mjs`

\---

## Suggested final folder strategy

### Static/deployable content

Lives under `public/...`

* `public/Physics/<topic>/topic.json`
* `public/Physics/<topic>/pages/\*.json`
* `public/Physics/<topic>/assets/\*`

### Local browser state

Lives in `localStorage`

* parent page drafts
* parent PIN hash
* student page-read progress

This split is the correct design for a static-hosted study app.

\---

## Why chapter packs are better than single-page imports

A chapter pack lets a parent import a **whole topic bundle** at once:

* topic metadata
* multiple pages
* page-specific questions
* clarifiers and tips
* diagrams/PDFs/images/SVGs
* student-side helper resources

That is a much better educational structure than importing one flat topic page at a time.

