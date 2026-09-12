# Core (1A) learner UI specification

This specification is normative for the learner surface produced by Core (1A). It exists to prevent a visual from replacing the teaching and to keep Core (1A) bidirectionally linked with Core (2).

## 1. Teaching is primary; illustration is support

A learner concept is not complete merely because a diagram exists. For `FULL_LEARNING`, the publication layer should preserve the semantic teaching from Core (1) and compose it in this order when applicable:

```text
PHYSICAL STORY / PHENOMENON
→ PLAIN-LANGUAGE EXPLANATION
→ PHYSICS WORD / MODEL / FRAME
→ STAGED ILLUSTRATION (supporting the explanation)
→ TRANSLATE THE PICTURE INTO MATHEMATICS
→ MODEL / VALIDITY CHECK
→ WORKED REASONING
→ COMMON TRAP / MISCONCEPTION REPAIR
→ CHECK
→ APPLY
→ CORE (2) TRANSFER
```

A staged illustration must never substitute for the ordinary-language explanation, model conditions, equation meaning, worked reasoning, or misconception repair.

## 2. Difficulty badges control scaffolding depth

Difficulty is a learner-facing support level, not a score.

| Badge | Meaning | Required support |
| --- | --- | --- |
| `D1 FOUNDATION` | direct/essential idea | at least one explanatory visual or representation and a direct check |
| `D2 THINK CAREFULLY` | picture-to-equation or frame/event reasoning required | at least two visual stages plus misconception/model support |
| `D3 CHALLENGING` | inverse reasoning, hidden state, or multiple representations | at least three staged reasoning moves plus worked reasoning and guided application |
| `D4 EXTENSION` | optional source-visible advanced content | must be visibly marked as extension and may not be presented as core mastery |

A D2/D3 badge without the required learner support is a publication defect.

## 3. Bidirectional Core (1A) ↔ Core (2) links

Core (1A) points forward to the transfer question that demonstrates mastery. Core (2) points back to the exact teaching concept/stage needed for repair.

```text
Core (1A) concept
    ↓
CHECK → APPLY → CORE (2) TRANSFER
                     ↓
              protected attempt
                 ↙       ↘
             success     stuck
                         ↓
               exact repair target
                         ↓
             Core (1A) concept/stage
```

The learner surface should show a compact `CORE 2 → Txx` badge on concepts with an exact transfer target.

The end of a concept uses the three-part gateway:

- `CHECK` — conceptual recall/explanation;
- `APPLY` — near-transfer application;
- `TRANSFER` — exact Core (2) protected-attempt identifier.

## 4. Typography and layout

The textbook surface uses readable typography rather than dense dashboard/card typography.

- A4, 16 mm left/right margins.
- Textbook body target: 10.5–11 pt.
- Diagram labels target: 8 pt or larger.
- Badge text must remain a single readable line; do not clip or wrap inside a fixed-height pill.
- Headings must wrap within their own column and never collide with difficulty/Core (2) badges.
- Equations use real Greek symbols, subscripts and superscripts; raw strings such as `sqrt(...)`, `theta`, `v_A/B`, or `u^2` are not acceptable on the learner surface.
- Major diagrams must have captions and enough area for labels without touching page or figure bounds.
- Avoid one-card-per-page rhythm. Explanation, diagram, equation and reasoning should share the page when they form one learning unit.

## 5. Visual audit

Automated checks are necessary but not sufficient. A release candidate must be rendered to page images and visually inspected.

At minimum, the audit should reject:

- text outside page bounds;
- clipped or wrapped badge text;
- overlapping diagram labels;
- broken symbols or raw math notation;
- blank pages;
- D2/D3 pages with an illustration but no explanatory teaching;
- Core (2) links without a corresponding concept or repair route;
- topic leakage beyond the declared source scope.

## 6. Reference implementation

`examples/render_motion2d_through_relative_motion.py` is a concrete source-aligned reference layout from the chapter opening through source Relative Motion / Illustration 11. It deliberately stops before `6.1 Motion of Boat in a Stream` and demonstrates:

- DejaVu Sans headings + DejaVu Serif body typography;
- difficulty badges;
- staged illustrations;
- full Core (1A) teaching around the illustrations;
- `CHECK → APPLY → TRANSFER` gateways;
- Core (2) T01–T08 links;
- proper Greek symbols, subscripts and superscripts;
- source-QC callout for the horizontal-projectile velocity typo.
