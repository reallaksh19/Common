# NMTC Bhaskara Preliminary — Topic Item Metadata Coverage Ledger v1

## Purpose

Track which source banks must be indexed under `Topic_Item_Metadata_Schema_v1.md` before topic machine metadata can be called complete.

This is a **coverage/debt ledger**, not the item ledger itself.

## Package coverage

| Package | First-Step | Ladder | Recognition Lab | First-Line Lab | Transfer Bank | Mastery Test | Machine-indexed |
|---|---|---|---|---|---|---|---|
| P0-1 Polynomial & Root Structure | present | present | present | present | present | present | `NO` |
| P0-2 Radicals / Exponents / Logs | present | present | present | present | present | present | `NO` |
| P0-3 Inequalities / Bounds | present | present | present | present | present | present | `NO` |
| P0-4 Modular / Divisibility / Digits | present | present | present | present | present | present | `NO` |
| P0-5 Circle / Tangent | present | present | present | present | present | present | `NO` |
| P1-1 Sequence & Series | present | present | present | present | present | present | `NO` |
| P1-2 Combinatorics | present | present | present | present | present | present | `NO` |
| P1-3 Triangle Metric | present | present | present | present | present | present | `NO` |
| P2-1 Mathematical Induction | present | present | present | present | present | present | `NO` |
| P2-2 Greatest / Least Integer | present | present | present | present | present | present | `NO` |

## Known package-scale asset pattern

The completed packages generally contain the following reviewed layers:

- First-Step cards;
- 10 mechanism ladders;
- 18 transfer items;
- 20 recognition items;
- 12 first-line items;
- 12-question mastery test.

Counts must be taken from the live source file when indexing; this ledger does not substitute a remembered count for machine parsing.

## Indexing order

Use the following order because it yields the most immediate production value:

1. mastery tests;
2. transfer banks;
3. recognition labs;
4. first-line labs;
5. First-Step cards;
6. practice ladders;
7. worked examples inside concept books.

## Why mastery/transfer first

These assets are closest to reusable production-bank questions and need:

- stable IDs;
- answer custody;
- student/teacher projection;
- provenance;
- mechanism;
- figure/source status;
- calibration fields.

## Historical/PYQ linking rule

Metadata indexing must not convert a mechanism link into historical identity.

Example:

An author-created tangent-secant problem may have:

```text
historical_anchor_id = NMTC-BH-P-2024-Qxx
provenance = AUTHOR_CREATED_TRANSFER
```

only when the source map explicitly supports that mechanism link. The author-created item itself remains non-official.

## Figure-gated debt

For P0-5, P1-2 and P1-3, metadata must retain exact figure/source state. `FIGURE_GATED` historical items cannot be exported as canonical historical questions merely because an answer or mechanism is known.

## Completion criterion

`TOPIC_METADATA_LEDGER = PASS_STATIC` only when:

- every eligible bank item has a unique ID;
- every row resolves to a source file/local item;
- answer/provenance/figure status is present;
- package-bank counts reconcile against live files;
- validation reports zero duplicate IDs and zero silent omissions.

## Current state

```text
PACKAGES_WITH_REQUIRED_BANK_LAYERS = 10/10
PACKAGES_MACHINE_INDEXED = 0/10
TOPIC_METADATA_SCHEMA = DEFINED
TOPIC_METADATA_LEDGER = NOT_RUN
```
