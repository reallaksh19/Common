# ALG-04 — Source Coverage Map

Status: `SOURCE_GROUNDED__2_PRIMARY_ANCHORS__90Q_VERIFICATION_JOINED`

Primary-count rule: these are the two historical questions whose frozen primary owner is `IOQM-G9-ALG-04`. Secondary/bridge tags do not inflate recurrence.

| Stable ID | Year/Q | Key status | Official answer | Source integrity | Primary mechanism | Independent answer status |
|---|---|---|---:|---|---|---|
| `IOQM-2025-Q26` | 2025 Q26 | `FINAL_OFFICIAL` | 10 | `CLEAN_OFFICIAL` | sliding-window averages -> index-shift inequalities | PASS |
| `IOQM-2023-Q10` | 2023 Q10 | `HBCSE_LINKED_MTAI_EMBEDDED_KEY` | 51 | `CLEAN_VALIDATED` | second-order recurrence -> Cassini-type neighboring-term invariant | PASS |

## Source authority

- 2025 Q26: HBCSE official paper and final official key.
- 2023 Q10: HBCSE-linked MTAI paper with embedded answer key.
- Both answers are independently recomputed in the 90-question verification authority and agree with the corresponding key.

Exact historical wording remains under validated-paper custody. This package cites year/question provenance and teaches the mechanism without pretending author-created exercises are historical questions.

## Mathematical source traces

### `IOQM-2025-Q26`

Verified mechanism:
- increasing 4-term averages imply `a_{i+4}>a_i`;
- decreasing 7-term averages imply `a_{i+7}<a_i`;
- subtracting adjacent windows is the first move;
- the two index-shift inequalities create a strict cycle at length 11, while a length-10 construction exists;
- verified answer: `10`.

Pedagogical use:
- canonical anchor for local/window subtraction;
- changed-surface transfer uses rolling totals and moving measurements.

### `IOQM-2023-Q10`

Frozen recurrence mechanism:
`a_{n+2}=-4a_{n+1}-7a_n`.

For a second-order recurrence
`a_{n+2}=p a_{n+1}+q a_n`,
define
`D_n=a_n^2-a_{n-1}a_{n+1}`.

Then:
`D_{n+1}=-qD_n`.

For the anchor, `q=-7`, so the neighboring-term determinant scales by `7`. The validated problem's initialization makes the target a pure power of 7; its divisor count is independently verified as `51`.

Pedagogical use:
- canonical anchor for “high index -> transform/invariant before iteration”;
- the student book derives the scaling law but does not reproduce the full historical stem.

## Secondary bridges and owner boundaries

- `ALG-01`: transformation/equivalence habits may be retrieved.
- `COMB-03`: recurrence notation is borrowed from ALG-04, but state definition and recurrence derivation remain COMB-03 ownership.
- No COMB-03 historical item is counted as an ALG-04 primary recurrence.

## Author-created coverage required by sparse historical ownership

Two primary anchors do **not** justify shrinking the unit to two tricks. Author-created, distinctly labelled material therefore covers:
- sequence notation and indexing;
- term vs partial sum;
- AP vs GP recognition;
- explicit vs recursive definitions;
- initialization and recurrence verification;
- shifted-recurrence subtraction;
- telescoping;
- local/window cancellation;
- simple high-index invariants;
- real T2-T4 changed-surface transfer.

No author-created item receives an `IOQM-YYYY-QNN` ID.
