# Optics Sample Pack — Quantitative Smoke Test Results

These results come from a real import simulation run against the patched app structure.

## Executed checks

1. Validated `content-pack.json` against the app schema.
2. Imported the ZIP into a fresh temporary `public/` tree using the same topic/page/asset rules as the app.
3. Verified expected filesystem outputs.
4. Counted pages, assets, blocks, clarifiers, attachments, and questions.
5. Verified supported student question types and rich block coverage.
6. Rebuilt the app after the schema fix.

## Measured results

- Topic count: **1**
- Page count: **5**
- Asset count: **7**
- Attachment count: **10**
- Clarifier count: **12**
- Question count: **14**
- Block count: **31**

### Question types covered
- `mcq`
- `short_answer`
- `numeric`
- `true_false`
- `concept_strengthener`

### Rich block types covered
- `equation`
- `svg`
- `image`
- `pdf_embed`
- `worked_solution`
- `table`
- `link_card`
- `image_link`
- plus headings, paragraphs, bullets, callouts, warnings, misconceptions, and tips

## Pass/fail assertions

- Schema validation: **PASS**
- Topic file created: **PASS**
- Pages directory created: **PASS**
- Assets directory created: **PASS**
- Minimum 5 pages: **PASS**
- Minimum 6 assets: **PASS**
- Student question coverage met: **PASS**
- Rich block coverage met: **PASS**
- Attachment coverage met: **PASS**
- Clarifier coverage met: **PASS**
- Question coverage met: **PASS**
- App webpack build after schema fix: **PASS**

## Recommended acceptance gate for future AI runs

The AI should not mark the Parent UI / Kid UI work as complete unless all of the following are true:

### Parent UI gate
- pack import completes without validation error
- topic appears under the correct subject
- imported topic retains cover asset and helper text
- each imported page opens in the editor
- content / clarifiers / questions / resources tabs all load
- at least one local asset can be reused in a block after import
- exporting the same topic again produces a non-empty ZIP

### Kid UI gate
- topic home renders correct title, page count, difficulty, and helper text
- at least 5 pages are navigable in order
- right sidebar shows clarifiers and helpful resources on relevant pages
- PDF attachment opens successfully
- SVG/image content is visible on the page
- supported question types render without “unsupported type” warnings
- page-read progress is saved in localStorage

### Quantitative gate
Use these minimum thresholds for a sample validation pack:
- pages >= 5
- assets >= 6
- attachments >= 6
- clarifiers >= 10
- questions >= 12
- supported question types >= 5
- rich block types >= 8
