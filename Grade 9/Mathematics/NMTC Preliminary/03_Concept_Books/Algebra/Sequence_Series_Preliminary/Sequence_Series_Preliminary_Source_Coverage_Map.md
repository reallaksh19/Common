# Sequence & Series — NMTC Preliminary Source Coverage Map

## Authority rule

This map uses only solution-qualified Bhaskara Preliminary evidence already present in `01_PYQ_Corpus/`.

The existing `Grade 9/Mathematics/Sequence and Series/` chapter remains concept authority. This file maps NMTC Preliminary mechanisms into that chapter.

## Canonical clean anchors

| PYQ ID | Qualified mechanism | Existing chapter lens | First move | Use |
|---|---|---|---|---|
| `NMTC-BH-P-2019-Q29` | functional recurrence | POSITION + TRANSFORM | substitute strategically chosen indices; climb only as far as needed | clean anchor |
| `NMTC-BH-P-2023-Q15` | weighted polynomial sum | ACCUMULATION | express nth term structurally, then split into standard power sums | clean anchor |
| `NMTC-BH-P-2023-Q29` | selected/high-index GP | RATIO + TRANSFORM | divide relations/cancel common powers before solving `a,r` | clean anchor |
| `NMTC-BH-P-2024-Q10` | weighted-square accumulation | ACCUMULATION | expand kth term into polynomial in `k`; use standard sums | clean anchor |
| `NMTC-BH-P-2024-Q11` | recurrence linearization | TRANSFORM + ACCUMULATION | take reciprocal / neighboring transform so recurrence telescopes | clean anchor |
| `NMTC-BH-P-2024-Q27` | coupled infinite GP sums | RATIO + ACCUMULATION | write both sums in `a,r`, enforce `|r|<1`, then eliminate | clean anchor |

## Cross-domain support

`NMTC-BH-P-2024-Q13` contains a geometric sequence of circle radii. It supports recognition of constant ratio but remains **geometry-primary**; do not use it to inflate Sequence & Series recurrence frequency.

## Foundation-only historical structure

2018 Q17 uses five consecutive integers and average symmetry. It is useful as a POSITION/CHANGE foundation drill but is not treated as a major NMTC Sequence & Series anchor.

## Blocked / contrast evidence

### `NMTC-BH-P-2025-Q30`

The reproduced progression wording and the AMTI provisional key do not agree. The key value is consistent with a different term comparison than the printed text.

Disposition:

`SOURCE_KEY_CONFLICT_NOT_CANONICAL`

Permitted use:

- source-integrity training;
- demonstrate that a GP-looking item must not be silently repaired to fit a key.

Forbidden use:

- exact historical anchor;
- recurrence statistics as a clean GP question;
- student-facing “official solution” without original-source resolution.

## Mechanism coverage required by the overlay

1. term vs sum discrimination;
2. AP difference/nth-term/block-sum recognition;
3. GP ratio/selected-term/high-index cancellation;
4. weighted sums -> standard sums;
5. nested sums -> count how often each term occurs;
6. recurrence linearization by reciprocal/difference/shift;
7. functional recurrence by strategic substitution;
8. infinite GP convergence + coupled constraints;
9. reverse from cumulative sum: `a_n=S_n-S_{n-1}`;
10. telescoping through partial fractions/rationalization;
11. finite differences for polynomial sequences;
12. source QC when term wording and answer key disagree.

## Publication guardrail

The overlay may be internally complete using clean historical mechanisms plus author-created transfers even though 2025 Q30 is blocked. Publication must retain the blocked status rather than inventing a corrected historical stem.