# COMB-05 - Source Coverage Map

## Authority

Canonical historical IDs follow the frozen 90-question corpus. This topic owns pigeonhole and extremal selection; geometry and number theory are transfer surfaces, not alternate canonical owners.

| Stable ID | Source/key status | Verified answer | Role | Source-integrity status |
|---|---|---:|---|---|
| IOQM-2023-Q18 | HBCSE-linked MTAI paper with embedded key | 71 | primary extremal/geometry anchor | CLEAN_VALIDATED |
| IOQM-2023-Q27 | HBCSE-linked MTAI paper with embedded key | 91 | primary extremal-complement anchor | CLEAN_VALIDATED |

Validated paper/key: `https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf`.

The metadata-correction overlay does not modify either anchor.

## Independent mathematical traces

### IOQM-2023-Q18

The source surface is a convex 50-gon with a selected family of diagonals under the local rule that each selected diagonal intersects at most one other selected diagonal. Add the 50 polygon sides. The resulting drawing is an outer 1-planar graph, whose tight edge bound is `5n/2-4`. With `n=50`, at most 121 total edges occur, hence at most `121-50=71` selected diagonals. A construction with 47 fan diagonals from one vertex plus 24 alternating short diagonals attains 71. Independent result: **71**, agreeing with the validated key.

The outer-one-crossing density lemma belongs in teacher/source analysis; the learner-facing doctrine is the extremal translation from a local crossing cap to a global density restriction.

### IOQM-2023-Q27

Each increasing 4-subset of `{1,...,20}` is uniquely written `a<b<d<c`. Call it balanced when `a+c=b+d`. There are `C(20,4)=4845` increasing quadruples. Direct summation over the middle pair `(b,d)` gives 525 balanced quadruples, so there are 4320 unbalanced. A selected family of 4411 can contain all 4320 unbalanced quadruples, but every additional member must be balanced. Hence at least `4411-4320=91` balanced quadruples are forced. Independent result: **91**, agreeing with the validated key.

## Coverage implications

Historical recurrence is not treated as official weightage. The two anchors support different mechanisms: local-to-global extremal density and extremal complement/capacity. Direct/generalized pigeonhole, geometric cells, residue classes, nearest/farthest choices, and close method contrasts are completed with author-created items whose provenance is explicit in `Item_Metadata.csv`.
