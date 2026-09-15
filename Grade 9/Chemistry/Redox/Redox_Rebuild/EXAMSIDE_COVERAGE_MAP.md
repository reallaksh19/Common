# ExamSIDE coverage map

Frozen Redox index audit: **74 candidates** = 29 numerical + 45 MCQ.

## Scope result

| Status | Count | Publication treatment |
|---|---:|---|
| `ELIGIBLE_IN_SCOPE` | 24 | Exactly one canonical primary subtopic; must appear in the relevant transfer book. |
| `PARTIAL_SCOPE` | 8 | Retained in the ledger with explicit outside dependency; not silently simplified into an original PYQ. |
| `OUT_OF_SCOPE` | 42 | Excluded because the minimum solution path depends mainly on chemistry outside the supplied source boundary. |

## Canonical primary placement

| Subtopic | Required | Placed | Status |
|---|---:|---:|---|
| RX-ST01 Oxidation Number | 7 | 7 | PASS |
| RX-ST02 Oxidation & Reduction | 2 | 2 | PASS |
| RX-ST03 Oxidising / Reducing Agents | 4 | 4 | PASS |
| RX-ST04 Redox vs Non-redox | 3 | 3 | PASS |
| RX-ST05 Types of Redox Reactions | 8 | 8 | PASS |
| RX-ST06 Integrated Pipeline | 0 new | 0 new | cumulative reuse only |

`CHAPTER_ELIGIBLE_TOTAL = 24`  
`CHAPTER_PLACED_UNIQUE = 24`  
`CHAPTER_MISSING = 0`  
`CHAPTER_DUPLICATE_PRIMARY_PLACEMENTS = 0`

## Important full-corpus correction

The first incremental RX-ST05 audit used a denominator of 5. The later 74-candidate reverse audit found three additional eligible disproportionation PYQs. They add no new teaching architecture, but each still requires a canonical transfer placement. RX-ST05 was backfilled to **8/8** before chapter closeout.

This is the main reason chapter acceptance must enumerate the full external corpus instead of inferring the denominator from incremental subtopic builds.
