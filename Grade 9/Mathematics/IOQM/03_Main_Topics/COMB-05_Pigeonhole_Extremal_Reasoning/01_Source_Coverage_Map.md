# COMB-05 — Source Coverage Map

This map records historical custody without turning two source questions into an alleged official topic weightage.

## Historical anchors

| Stable ID | Authority | Key status | Marks | Corpus owner | Mechanism | Figure | Independent result | Use |
|---|---|---|---:|---|---|---|---:|---|
| `IOQM-2023-Q18` | HBCSE-linked MTAI paper/key | HBCSE-linked embedded key | 3 | `IOQM-G9-COMB-05` | extremal diagonals; outer one-crossing structure | no required source figure | 71 | teacher/source trace; stretch transfer |
| `IOQM-2023-Q27` | HBCSE-linked MTAI paper/key | HBCSE-linked embedded key | 5 | `IOQM-G9-COMB-05` | extremal set; balanced quadruples; complement capacity | no | 91 | teacher/source trace; integrated extremal example |

Source paper/key:
`https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf`

## Independent source traces

### IOQM-2023-Q27
Every admissible quadruple is determined by a four-element subset of `{1,...,20}`, so there are
`C(20,4)=4845` total.

Writing the increasing entries in cyclic problem order as `a<b<d<c`, put
`p=b-a`, `q=d-b`, `r=c-d`. Balance is `a+c=b+d`, equivalent to `p=r`.

Thus the number of balanced quadruples is
`sum_{p,q>=1, 2p+q<=19} (20-2p-q)=525`.
So there are `4845-525=4320` unbalanced quadruples. A set of `4411` must therefore contain at least
`4411-4320=91` balanced quadruples, and that bound is attained by taking all unbalanced quadruples plus any 91 balanced ones.

Independent answer: `91`, agreeing with the validated key.

### IOQM-2023-Q18
Add the 50 boundary sides to the chosen diagonals. The resulting convex straight-line drawing has every edge crossed at most once, hence is an outer-1-planar graph. The tight density bound for an outer-1-planar graph on `n` vertices is `5n/2-4` edges. Therefore the chosen diagonals number at most
`(5n/2-4)-n = 3n/2-4`; for `n=50` this is `71`.

Attainment: label the vertices cyclically `A1,...,A50`. Take the 47 fan diagonals from `A1` to every non-neighbour `A3,...,A49`, and add the 24 short diagonals
`A2A4, A4A6, ..., A48A50`. Each added short diagonal crosses exactly one fan diagonal and no selected diagonal has more than one interior crossing. Hence `47+24=71`.

Independent answer: `71`, agreeing with the validated key.

The density lemma is treated as a teacher/authoring extremal lemma, not as a prerequisite graph-theory chapter for the Grade-9 learner.

## Coverage judgment

The two anchors cover:
- geometric extremal structure;
- complement/extremal counting;
- translating a local crossing restriction into a global bound;
- separating an exact count from a forced-existence argument.

Author-created practice supplies the missing direct/generalized pigeonhole, residue, geometric-cell and extremal-choice progression required by the canonical topic boundary.

## Source-integrity state

- source IDs: verified;
- key authority: verified;
- answer values: independently recomputed;
- correction-overlay effect: none on these anchors;
- source conflicts: none;
- official topic weightage claim: not made.
