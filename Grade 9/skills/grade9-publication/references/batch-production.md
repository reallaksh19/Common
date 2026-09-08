# Batch Production Protocol

Use this protocol once the publication prototype is approved and the book is being reconstructed in successive batches.

The default batch is **two contiguous subtopics** unless a subtopic is unusually large, in which case use one subtopic. Do not choose arbitrary page windows that split a pedagogical unit without recording the split.

## Batch contract

Before building a batch, freeze:

- batch ID;
- first and last source page;
- first and last stable source ID;
- included subtopic IDs;
- frozen core-unit count;
- expected Student Core / Self-Check / Audit outputs;
- previous cumulative release version.

A batch must end with both **batch-only artifacts** and **cumulative artifacts**.

## AD-22 — CONTIGUOUS SOURCE COVERAGE

The next batch must begin immediately after the previous batch's last covered source page / stable source unit unless an explicit exception is recorded.

Release fails if there is:

- a skipped source page containing core material;
- a duplicated primary source unit;
- an unexplained gap between batches;
- a subtopic split without a migration record.

Required counters:

```text
source_gaps = 0
duplicate_primary_units = 0
unexplained_batch_splits = 0
```

## AD-23 — APPROVED-PAGE IMMUTABILITY

Previously approved cumulative pages are frozen. When adding a new batch, append the new Student Core / Self-Check / Audit pages rather than regenerating approved pages, unless a specific regression fix is intentionally applied.

If an old page must change:

1. identify the old page and source units;
2. state the reason;
3. re-run source, layout, typography and collision QA for that page;
4. compare old and new renders;
5. record the change in the batch audit.

For ordinary append-only batches, previous approved-page renders should be identical.

## AD-24 — BATCH DENOMINATOR FREEZE

Freeze the core-unit denominator for the batch before composition. Do not lower it because content becomes difficult to fit.

Required:

```text
batch_core_units = batch_mapped_core_units
batch_unmapped_core_units = 0
```

## AD-25 — CUMULATIVE DENOMINATOR RECONCILIATION

After merging the batch into the cumulative publication:

```text
cumulative_core_units = previous_cumulative_core_units + current_batch_core_units
cumulative_unmapped_core_units = 0
```

Also verify that no prior source unit became unmapped during merge or renumbering.

## AD-26 — CROSS-BATCH LINK CLOSURE

Resolve references after cumulative pagination, not only inside the batch.

Check:

- earlier section -> new section;
- new section -> earlier prerequisite;
- question -> solution/self-check;
- figure/table callouts;
- TOC/bookmarks;
- external source links.

Required counters:

```text
cross_batch_unresolved_references = 0
broken_cumulative_links = 0
```

## AD-27 — STUDENT / SELF-CHECK / AUDIT ROUTING

Route every source obligation to the correct artifact before layout:

- teaching, examples, representations, guided practice, independent transfer -> Student Core;
- retrieval/self-check/checklist items -> Self-Check;
- source focus, provenance, mapping, QA status, production notes -> Audit.

Do not duplicate self-check/audit material in Student Core merely to prove preservation. The audit ledger may map one source page into multiple artifacts.

## AD-28 — BATCH RENDER REGRESSION

For every batch:

1. render batch-only Student Core / Self-Check / Audit;
2. run text-overlap and component-bounds checks;
3. inspect formula completeness and math typography;
4. inspect all batch pages visually;
5. merge into cumulative PDFs;
6. render the cumulative boundary pages (last two old + first two new);
7. verify no merge-time page-size, footer, font or numbering regression.

Required counters:

```text
batch_text_overlap_findings = 0
batch_component_bounds_escape_findings = 0
batch_math_typography_findings = 0
batch_formula_completeness_findings = 0
cumulative_boundary_regressions = 0
```

## AD-29 — BATCH RELEASE PACK

Every completed batch should produce:

- batch-only Student Core PDF;
- batch-only Self-Check PDF;
- batch-only Audit PDF or manifest;
- cumulative Student Core PDF;
- cumulative Self-Check PDF;
- cumulative Audit PDF/manifest;
- collision/layout report;
- math-typography report;
- source-to-publication mapping for the batch.

Do not call a batch complete if only the cumulative PDF exists and the batch cannot be independently audited.

## Batch status language

Use precise release statements:

- `BATCH SOURCE MAPPING COMPLETE; RENDER QA PENDING`
- `BATCH QA PASS; CUMULATIVE MERGE PENDING`
- `BATCH + CUMULATIVE QA PASS`
- `BATCH BLOCKED: 2 UNMAPPED CORE UNITS`

Never state `publisher-ready` for the whole book merely because one batch passes.