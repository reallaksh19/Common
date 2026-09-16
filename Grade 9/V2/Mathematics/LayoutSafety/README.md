# Mathematics V2 — LayoutSafety (M-UPGRADE-2 item 7)

Proof readability and layout safety are **release semantics, not cosmetic QA**. A page can
be structurally valid, deterministic and inside its bounds while still being unreadable,
collided or silently truncated — and the seven-topic stress test produced all four:

| Topic | What the page did | What the existing check could see |
| --- | --- | --- |
| Euclid | microtype beside large unused whitespace; two-up solution blocks collided | both in bounds |
| Polynomials | multipart workspace overflowed its rectangle | the rectangle was on the page |
| Linear Equations | a following panel covered the tail of an option set | all options present in JSON |
| Number Systems | large empty lined regions beside a generic verify box | page capacity "fine" |

## One object model, two audits

This phase consumes the **same** `math-rendered-object-map` that `SourceLedger` uses, so
completeness and readability are audited over one description of what was actually placed
rather than two. Item 7 added three fields to it:

```text
container_id        objects sharing a container are siblings and may not intersect;
                    a child inside its container is legal containment, not a collision
content_height_pt   the height the content MEASURES, distinct from the height it was GIVEN
response_mode       for WORKSPACE objects, the response the question actually demands
```

`tests/test_math_layout_safety.py` runs the source-ledger witness over the layout probe to
keep the two phases honest about sharing the model.

## Minimum readable size is per semantic role

A global floor cannot express that a 9.0 pt diagram label is fine while a 9.0 pt question
body is not. `registry/math-typography-role-registry.json` sets `min_pt` and `preferred_pt`
per role:

```text
HEADING 12.0/14.0    QUESTION_BODY 9.5/11.0   LEARNER_BODY 9.5/10.5
MATH_DISPLAY 10.0/12.0                        MATH_INLINE 9.5/10.5
DIAGRAM_LABEL 7.5/9.0                         ROUTE_STATE_LABEL 8.0/9.5
ROUTE_STATE_BODY 9.0/10.5                     SOLUTION_BODY 9.0/10.5
WORKSPACE 8.0/9.5    FOOTNOTE 7.0/8.0         SOURCE_META 7.0/8.0
PAGE_FURNITURE 7.0/8.0
```

`min_pt` is the hard gate. `preferred_pt` is what makes
`MICROTYPE_USED_WHILE_EXPANDABLE_SPACE_EXISTS` meaningful: unused whitespace on its own is
*not* a failure, and neither is slightly small type on a full page. The failure is the
combination — a learner-visible object set below its preferred size while at least 30% of
the page is unused. That is a layout-policy choice, not a page-capacity limit, which is
exactly what the Euclid run demonstrated.

## Collision is pairwise between siblings

A page-bounds check cannot see two solution blocks overlapping in the middle of a page. One
test asserts this explicitly: it moves a block so it collides, then confirms the moved block
is still comfortably inside the printable area, and still fails
`LAYOUT_COMPONENT_INTERSECTION`.

## Measure-then-place, measure-then-pack

```text
semantic object -> measure content -> determine response mode -> determine representation
demand -> determine workspace demand -> paginate / place -> inspect final composition
```

`CONTENT_OVERFLOW` fires when `content_height_pt` exceeds the allocated box.
`NEGATIVE_REMAINING_HEIGHT` fires when a container's children measure taller than the
container. `measure_then_pack()` assigns solution blocks to pages from their measured
heights, so **one solution per page is correct when the content demands it** — two-up is an
optimisation, and `SOLUTION_BLOCK_PACKING_OVERFLOW` catches fixed-density packing.

## Workspace follows the response mode

The renderer must not allocate a fixed rectangle because a component is called `WORKSPACE`.
The registry sets a minimum height per response mode, so a proof gets room for
`GIVEN → licensed fact → derived statement → conclusion` while an MCQ does not get a lined
page it cannot use:

```text
MCQ_SELECTION 26pt   ONE_LINE_JUSTIFICATION 42pt   ALGEBRA_CHAIN 120pt
TABLE 110pt          NUMBER_LINE 70pt              MODEL_UNIT_CALCULATION 130pt
MULTIPART 150pt      COORDINATE_PLANE 170pt        PROOF 190pt   CONSTRUCTION 190pt
```

## Falsifiers

```text
LEARNER_TEXT_BELOW_MIN_READABLE_SIZE
DIAGRAM_LABEL_BELOW_MIN_READABLE_SIZE
MICROTYPE_USED_WHILE_EXPANDABLE_SPACE_EXISTS
LAYOUT_COMPONENT_INTERSECTION
CONTENT_OVERFLOW
NEGATIVE_REMAINING_HEIGHT
WORKSPACE_RESPONSE_MODE_MISMATCH
SOLUTION_BLOCK_PACKING_OVERFLOW
LAYOUT_SAFETY_GATE_FAILED
```

`audit_layout()` never raises and reports `status: PASS | BLOCKED`;
`assert_layout_safe()` is the fail-closed wrapper that raises each finding under its own
named gate.

## Release meaning

`PUBLICATION_ENGINEERING` only. Passing these gates means the page is readable, uncollided
and complete after layout. It is not a visual-usability or expert-review PASS — both remain
`PENDING`.
