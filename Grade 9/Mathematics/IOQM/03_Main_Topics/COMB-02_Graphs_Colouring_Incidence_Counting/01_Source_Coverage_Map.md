# COMB-02 Source Coverage Map

Status: `EXACT_STEMS_CLOSED_ONE_PAGE_VISUAL_GATE_PENDING`

This map separates four different claims: exact source-stem custody, independent mathematics, printed-figure dependency, and page-image confirmation. A verified numerical answer alone is never treated as source custody.

## Authorities

- 90Q corpus ledger: `IOQM_2023_2025_90Q_Ledger_v1.csv`.
- independent-answer authority: `Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`.
- prompt authority: `02_Production/IOQM_G9_Main_Topic_Prompt_Pack_v1.md`.
- prerequisite provider: `COMB01_Stable_Counting_Model_Interface_v1.md`.
- 2025 official paper: MTA(I) shared Drive `en.M1.pdf`, file id `13_o0QUmfqZJxc7IWrz6yqKivuyVC-wku`.
- 2025 final key: MTA(I) shared Drive `final-key-7th-September.pdf`, file id `18jKJ_2rUxgOlbg-2If_-oHzcH8JxzwT5`.
- 2024 official English paper: MTA(I) shared Drive `english.pdf`, file id `1z7-3fJuk5BW9zx9SUEumcnuuE080pQJq`.
- 2023 controlled paper/key: HBCSE-linked MTA(I) PDF `IOQM_Sep_2023_Question-paper-with-answer-key.pdf`.

All six anchors have `PASS,true` in the independent-answer verification ledger and are independently re-derived in `Authoring/Independent_Math_and_Source_Audit.md`.

## Historical anchors

| ID | verified answer | source custody | visual / figure custody | publication disposition |
|---|---:|---|---|---|
| `IOQM-2025-Q08` | `48` | `PASS_EXACT_OFFICIAL_STEM_AND_FINAL_KEY` | `PASS_PAGE_3_200DPI`; printed figure: `NONE` | `CLOSED` |
| `IOQM-2025-Q29` | `19` | `PASS_EXACT_OFFICIAL_STEM_AND_FINAL_KEY` | printed figure: `NONE`; text source sufficient | `CLOSED` |
| `IOQM-2024-Q09` | `48` | `PASS_EXACT_OFFICIAL_STEM` | printed figure: `NONE`; pair definition is textual | `CLOSED` |
| `IOQM-2024-Q19` | `12` | `PASS_EXACT_OFFICIAL_STEM` | printed figure: `NONE`; complete-graph relation is textual | `CLOSED` |
| `IOQM-2023-Q16` | `94` | `PASS_EXACT_CONTROLLED_STEM_AND_EMBEDDED_KEY` | `PASS_OFFICIAL_PAGE_5_SCREENSHOT`; printed figure: `NONE` | `CLOSED` |
| `IOQM-2023-Q22` | `77` | `PASS_EXACT_CONTROLLED_STEM_AND_EMBEDDED_KEY` | `PENDING_EXACT_PAGE_IMAGE_CONFIRMATION`; screenshot service cache-missed page 7 | `FAIL_CLOSED_FOR_VERBATIM_PROMOTION` |

## Source-specific notes

### `IOQM-2025-Q08`

Official M1 page 3 was rendered from the exact MTA(I) paper at 200 dpi. The problem is printed as text only: four vertices `A,B,C,D`, all four quadrilateral sides, and diagonal `AC`; adjacent endpoints must receive different colours. No diagram is printed. Therefore the graph model `K4` minus edge `BD` loses no figure information.

### `IOQM-2025-Q29`

The exact M1 stem was checked against the official paper and the final organizer key. The rule is cyclic: a regular polygon with `n>=5`, at most six colours, and every five consecutive vertices differently coloured. The final M1 answer is `19`.

### `IOQM-2024-Q09`

The exact official English stem defines `X={(m,n):0<=m,n<=4}` and explicitly defines an unordered knight-move pair by coordinate differences. No board picture is required to reconstruct the adjacency relation.

### `IOQM-2024-Q19`

The exact official English stem gives five non-collinear points, joins every pair, colours the joining lines red/blue, and forbids a monochromatic triangle. No printed figure is required to recover the complete graph.

### `IOQM-2023-Q16`

The official HBCSE-linked MTA(I) page was visually inspected. The stem is text only: six sides of a convex hexagon are red; every diagonal is red or blue; every vertex-triangle must have at least one red side. No printed hexagon diagram is present.

### `IOQM-2023-Q22`

The exact controlled text and embedded answer key are closed. The stem specifies an equilateral triangle of side 6, five interior side pegs per side, four chosen pegs, joins to opposite vertices, and exactly nine regions. The extraction contains the complete construction and does not reference a printed figure. Nevertheless, because this item is geometry-surface and the official page-image retrieval repeatedly cache-missed, exact page-image confirmation remains a separate fail-closed publication gate.

## COMB-01 retrieval boundary

Retrieve only stable counting semantics: counted-object identity, disjoint addition, conditional multiplication, exhaustive case splits, ordered-vs-unordered distinction, justified complement, stable restriction/state vocabulary, and fail-closed overlap handling.

Do **not** recreate generic P&C, repeated-object, complement or inclusion-exclusion chapters inside COMB-02.

COMB-02 owns graph modelling, vertices/edges, degree sums/handshaking, proper colouring, incidence double counting, grid/knight graphs and simple Ramsey-style inevitability.

## Current disposition

- exact historical stems: `PASS_6_OF_6`;
- independent historical mathematics: `PASS_6_OF_6`;
- exact printed-figure dependency identified: `PASS`;
- page-image confirmation: `PASS` for Q08 and Q16, `PENDING` for Q22 only;
- Q22 verbatim/publication promotion: `FAIL_CLOSED` until its exact page image is inspected.
