# ALG-01 - Wave-1 Research Interfaces

Authoring-only. Each microstream below is evidence for the single pedagogical owner; none is a standalone student chapter.

```yaml
main_topic_id: IOQM-G9-ALG-01
owner_role: RESEARCH_INTERFACE_ONLY
canonical_teaching_owner: IOQM-G9-ALG-01
status: READY_FOR_LEAD
source_cutoff: 2026-08-31
prerequisite_interfaces: [F0_G9_CORE, F1_IOQM_BRIDGE]
```

## A. Scope boundary

Included:
- target-led factor/expand;
- repeated-block substitution;
- symmetric reconstruction from already-given sum/product data;
- identity vs relation-on-solutions;
- equivalence/implication;
- elementary low-degree relation rewriting.

Excluded / owned elsewhere:
- Vieta, discriminant, root canon, polynomial remainder/reduction -> ALG-03;
- AM-GM/equality/attainment -> ALG-02;
- radical/log domain doctrine -> ALG-06.

## B. Learner-state model

`PRIOR_KNOWLEDGE:` routine school manipulation.  
`LIKELY_HALF_KNOWLEDGE:` identities remembered but direction not chosen from target.  
`MISSING_BRIDGES:` representation choice; logical custody of transformations; stop-when-target-fixed.  
`OWNERSHIP_TARGET:` target -> representation -> first move -> conditions -> check.

## C. Mathematical invariant / governing structure

Equivalent algebraic forms carry the same admissible information, but some expose the requested target more cheaply.

A relation such as `x^2=ax+b` may be reused *on its solution set* to rewrite higher powers. It is not promoted to a global identity.

## D. Representation inventory

| Representation | Exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| factored | products/zeros | factor | exact identity | expand automatically |
| expanded | coefficients/sums | expand | exact identity | factor automatically |
| substituted block | repeated structure | `t=F(x)` | preserve original restrictions | cosmetic renaming |
| sum/product | symmetric targets | reconstruct | target must be determined by data | solve variables |
| low-degree relation | high-power rewrite | isolate highest power | relation valid only on solutions | solve roots |
| original equation | validity | check candidates | all original restrictions | trust squared/cancelled equation |

## E. Decision boundaries

1. factor vs expand -> target asks product/zeros or coefficients?
2. solve variables vs reconstruct target -> is target symmetric?
3. identity vs relation -> true for all inputs or only admissible solutions?
4. substitution vs renaming -> did degree/repetition/unknown count shrink?
5. cancellation vs branching -> can divisor be zero?
6. reversible vs one-way -> does reverse implication hold?
7. relation rewriting vs ALG-03 reduction -> elementary one-relation rewrite or general polynomial method?

## F. Misconception catalogue

`ALG01-R1` WRONG_MOVE: manipulate before reading target. MISSING_LINK: RECOGNITION. REPAIR: target-first question.  
`ALG01-R2` WRONG_MOVE: always expand. MISSING_LINK: REPRESENTATION. REPAIR: factor/expand contrast.  
`ALG01-R3` WRONG_MOVE: substitute without compression. MISSING_LINK: REPRESENTATION. REPAIR: demand complexity reduction.  
`ALG01-R4` WRONG_MOVE: solve individual variables for symmetric target. MISSING_LINK: INVARIANT. REPAIR: swap test + sum/product identities.  
`ALG01-R5` WRONG_MOVE: ignore low-degree relation. MISSING_LINK: INVARIANT. REPAIR: rewrite highest power.  
`ALG01-R6` WRONG_MOVE: trust squaring/cancellation. MISSING_LINK: DOMAIN_CONDITION. REPAIR: direction + original check.  
`ALG01-R7` WRONG_MOVE: import downstream canon. MISSING_LINK: PREREQUISITE. REPAIR: retrieve/route to canonical owner.

## G. First-move cues

- product/zero target -> factor;
- coefficient target -> expand only as far as needed;
- repeated block -> name it;
- symmetric target -> write in sum/product data;
- high power under low-degree relation -> replace highest power;
- one-way operation -> record conditions/candidate check.

## H. H3 -> H0 fading plan

- H3: identity/execution relation supplied.
- H2: representation supplied, execution omitted.
- H1: recognition clue only.
- H0: mixed surface; learner chooses route and check.

All promoted numerical items are independently recomputed in `Independent_Mathematics_Audit.md`.

## I. Validated IOQM source anchors

| Stable ID | Role | Key status | Independent status |
|---|---|---|---|
| IOQM-2025-Q01 | primary | FINAL_OFFICIAL | PASS |
| IOQM-2025-Q21 | primary | FINAL_OFFICIAL | PASS |
| IOQM-2024-Q05 | primary | OFFICIAL_HBCSE_KEY | PASS |
| IOQM-2024-Q11 | primary | OFFICIAL_HBCSE_KEY | PASS |

## J. Source-independent mathematical traces

- 2025-Q01 -> both relational quantities reduce to `0.6x`; answer 40.
- 2025-Q21 -> low-degree relation + integer/square admissibility; answer 49.
- 2024-Q05 -> ratio substitution with product 1; expansion yields difference 1.
- 2024-Q11 -> reciprocal substitution; equality of transformed variables; answer 12.

No source correction overlay is needed for these IDs.

## K. Contrast-pair candidates

1. coefficient target in bracket product vs zero target in quadratic;
2. symmetric square target vs signed difference target;
3. compressing repeated block vs cosmetic shift;
4. identity valid everywhere vs relation usable only on solutions;
5. square-and-check vs reversible linear transformation;
6. cancel nonzero known constant vs divide by possibly-zero variable;
7. relation rewrite here vs polynomial remainder method in ALG-03;
8. supplied sum/product reconstruction here vs Vieta derivation in ALG-03.

## L. Transfer candidates

- T2: same invariant under expression/equation representation change.
- T3: rectangle perimeter/area -> symmetric side expressions.
- T3: functional repeated block -> strategic substitution bridge.
- T3: integer equation -> factor form for NT-04.
- T4: target-first representation -> inequality representation in ALG-02.

## M. Candidate mastery items

Integrated into `06_H0_Mastery_Test.md`: recognition, first-line, full solve, WHY-NOT and transfer.

## N. Dependency declarations

`REQUIRES:` G9 expansion/factorisation, linear equations, rational arithmetic.  
`BRIDGE_REQUIRES:` implication/equivalence/check discipline.  
`APPLIES:` no downstream canon as prerequisite.  
`EXPORTS:` factor/expand selection; strategic substitution; identity/relation distinction; equivalence/reversibility; symmetric reconstruction habit; elementary relation rewriting.

## O. Lead integration notes

Teach one governing question globally. Do not create separate identity, substitution and equivalence mini-books. Revisit the router at every contrast. Keep Vieta/discriminant/remainder and AM-GM/equality outside canonical ALG-01 prose.

## P. Independent QA status

`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE affecting downstream interface`
