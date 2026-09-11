# GEO-03 Source Coverage Map

## Historical anchor custody
| Stable ID | Authority | Paper / key | Source-page observation | Figure custody | Independent answer |
|---|---|---|---|---|---:|
| IOQM-2024-Q12 | HBCSE official | `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf` / `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf` | question 12 appears on paper page 3 (PDF index 2); square/trisection/intersection described entirely in text | `figure_required=false`; no historical figure is reproduced | 96 |
| IOQM-2023-Q05 | HBCSE-linked MTAI | `https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf` | question 5 appears on printed page 3 (PDF index 2); medians/midpoints described entirely in text | `figure_required=false`; source page visually inspected; no historical figure is reproduced | 10 |

## Independent mathematics traces
### IOQM-2024-Q12
Use a square of side 16 with coordinates `A=(0,16), B=(16,16), C=(16,0), D=(0,0)`. Trisection gives `E=(32/3,0)` and `F=(16/3,0)`. Lines `AE` and `BF` intersect at `M=(8,4)`. Triangle `MAB` has base 16 and height 12, so its area is `16*12/2 = 96`.

### IOQM-2023-Q05
Because the requested ratio is shape-independent, take `A=(0,0), B=(1,0), C=(0,1)`. Then `E=(0,1/2)`, `F=(1/2,0)`, centroid `G=(1/3,1/3)`, `Y=(1/2,1/4)`, `Z=(1/4,1/2)`. Determinants give `[GYZ]/[ABC]=1/48`; with `[ABC]=480`, the answer is `10`.

## Use policy
The learner pack cites only stable IDs and mechanism summaries, not full historical stems. Any teaching figure is author-created and explicitly not a reconstruction of a source figure.
