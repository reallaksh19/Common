# COMB-02 Source Coverage Map

Status: `SOURCE_LEDGER_LOCKED_EXACT_SOURCE_AUDIT_PENDING`

This file locks the six historical anchors to the corpus/verification authorities while preserving the distinction between a verified numerical answer and a completed topic-lead source audit.

## Authorities

- 90Q corpus ledger: `IOQM_2023_2025_90Q_Ledger_v1.csv`.
- independent-answer authority: `Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`.
- prompt authority: `02_Production/IOQM_G9_Main_Topic_Prompt_Pack_v1.md`.
- prerequisite provider: `COMB01_Stable_Counting_Model_Interface_v1.md`.

All six anchors have `PASS,true` in the independent-answer verification ledger.

## Historical anchors

| ID | verified answer | graph/incidence model | required contrast | exact-source custody |
|---|---:|---|---|---|
| `IOQM-2025-Q08` | `48` | quadrilateral with diagonal `AC` becomes a graph equivalent to `K4` minus one edge; count proper 4-colourings by adjacency | proper colouring vs unrestricted assignments | `PENDING_EXACT_STEM/FIGURE_CHECK` |
| `IOQM-2025-Q29` | `19` | cyclic word / cycle-power colouring: any five consecutive vertices must have distinct colours | linear local rule vs cyclic closure | `PENDING_EXACT_STEM_CHECK` |
| `IOQM-2024-Q09` | `48` | knight graph on a `5×5` grid; sum local degrees / directed moves and divide by two | direct pair enumeration vs degree sum | `PENDING_EXACT_STEM_CHECK` |
| `IOQM-2024-Q19` | `12` | red/blue colouring of `K5` edges with no monochromatic triangle; force degree pattern / 5-cycle structure | raw `2^10` enumeration vs Ramsey structure | `PENDING_EXACT_STEM_CHECK` |
| `IOQM-2023-Q16` | `94` | hexagon with fixed red sides; diagonal colouring under triangle-avoidance constraint | independent edge choices vs forbidden-subgraph structure | `PENDING_EXACT_STEM/FIGURE_CHECK` |
| `IOQM-2023-Q22` | `77` | side pegs joined to opposite vertices; region count becomes an incidence/intersection-count problem | coordinate drawing vs incidence graph | `PENDING_EXACT_STEM/FIGURE_CHECK` |

## Independent-answer closure

Repository verification authority:

- `2025-Q08 = 48` — PASS, independently verified.
- `2025-Q29 = 19` — PASS, independently verified.
- `2024-Q09 = 48` — PASS, independently verified.
- `2024-Q19 = 12` — PASS, independently verified.
- `2023-Q16 = 94` — PASS, independently verified.
- `2023-Q22 = 77` — PASS, independently verified.

The topic lead still has to reconstruct each solution from the exact source and independently confirm the count; the verified answer is a target check, not a derivation source.

## COMB-01 retrieval boundary

Retrieve only these stable semantics as needed:

- define one counted object/outcome and object identity;
- add only disjoint cases;
- multiply sequential choices under the stated conditional-choice count;
- require exhaustive case splits;
- distinguish ordered from unordered objects;
- use complement when it is genuinely simpler;
- retain stable restriction/state vocabulary;
- fail closed on overlapping cases rather than silently using naive addition.

Do **not** recreate generic P&C, repeated-object, complement or inclusion-exclusion chapters inside COMB-02.

COMB-02 owns graph modelling, vertices/edges, degree sums/handshaking, proper colouring, incidence double counting, grid/knight graphs and simple Ramsey-style inevitability.

## Source/figure gate

For the geometry-surface graph items (`2025-Q08`, `2023-Q16`, `2023-Q22`), inspect the exact paper before modelling. A graph model may discard irrelevant geometry only **after** incidence/adjacency information has been copied correctly. Record source page and any printed figure provenance in the later audit.

Current disposition: `ANSWERS_VERIFIED; TOPIC_LEAD_EXACT_SOURCE_AUDIT_NOT_YET_COMPLETE`.
