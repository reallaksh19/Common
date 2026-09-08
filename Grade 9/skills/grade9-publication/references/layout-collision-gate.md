# Publication Layout Collision Gate

Use this gate for every generated student, self-check, teacher, and audit PDF before release. It exists because a page can pass content-preservation checks while still being unusable when one reusable component draws outside its assigned box and collides with the next component.

## Governing rule

> A reusable layout component may draw only inside the bounding box it was given.

If a component is called with `(x, y, width, height)`, every text baseline, rule, shape, label, diagram, and nested object created by that component must remain inside that rectangle unless the API explicitly declares an overflow contract.

Never assume that a component previously designed for a 140 pt-high box will also fit a 90 pt-high box. Either make positions derive from `height`, use a compact mode, or allocate the full required height.

## Anti-drift checkpoint AD16 - ZERO TEXT COLLISION

A release candidate fails when extracted text boxes from different lines/blocks materially overlap.

Minimum release condition:

```text
text_overlap_findings = 0
component_bounds_escape_findings = 0
critical_equation_collision_findings = 0
```

The deterministic detector is only a baseline. Visual render inspection is still required.

## Anti-drift checkpoint AD17 - COMPONENT BOUNDS CONTRACT

Before reusing any layout function, verify:

1. the caller supplies enough height for the requested mode;
2. all child positions are calculated from the supplied `x`, `y`, `width`, and `height`;
3. the function returns or exposes its consumed height/bottom coordinate when content is variable;
4. the next component starts below the actual consumed bottom plus the design-system gap;
5. no label is positioned using a constant that can escape the component at smaller sizes.

### Bad pattern

```python
def weighting_diagram(c, x, y, w, h):
    # h is ignored.
    c.drawString(x + 10, y - 20, "EQUAL TIME")
    c.drawString(x + 10, y - 95, "EQUAL DISTANCE")
    c.drawString(x + 10, y - 145, "slower leg lasts longer")
```

This silently fails when the caller gives `h=92`.

### Acceptable pattern

```python
def weighting_diagram(c, x, y, w, h, mode="both"):
    if mode == "equal_time":
        # Compact layout kept inside h.
        ...
        return h

    top = y - 18
    bottom = y - h
    # Derive all section positions from h, or assert a documented minimum h.
    ...
    return h
```

A documented minimum-height assertion is preferable to silent escape:

```python
if mode == "both" and h < 128:
    raise ValueError("weighting_diagram(mode='both') requires h >= 128")
```

## Page-building rule: reserve, draw, advance

For every vertical composition:

```text
1. RESERVE the component height.
2. DRAW inside the reserved rectangle.
3. ADVANCE the page cursor to component_bottom - standard_gap.
4. Never estimate the next start position independently.
```

For variable text, first measure/wrap the text and derive the consumed height. Do not draw first and hope the next object is far enough away.

## Guided-practice rule

Full-support guided pages are especially collision-prone because they combine:

- governing formula;
- prompt;
- diagram;
- model/calculation chain;
- hints;
- writing space.

The support hierarchy must also prevent cognitive collision:

- show only the diagram/model needed by the active worked problem;
- keep alternative models in the formula/reference band or a separate comparison panel;
- do not place an unrelated formula route directly beneath a worked calculation merely because it belongs to the same subtopic;
- full support = show the active relation and reasoning clearly;
- faded support = reduce scaffolding deliberately, not by shrinking or crowding.

## Deterministic check

Run:

```bash
python scripts/check_text_overlaps.py publication.pdf
```

The script checks:

- material overlap between words belonging to different extracted lines/blocks;
- extracted words outside page bounds;
- page number and token pair for every finding.

A non-zero exit code blocks release.

Recommended pipeline:

```text
generate PDF
-> render every page
-> run check_text_overlaps.py
-> inspect contact sheet
-> inspect every flagged/dense page at 100%
-> repair
-> regenerate
-> rerun until zero
```

## Visual inspection after zero detector findings

Zero machine-detected overlaps is necessary, not sufficient. Check for:

- text visually touching rules or shapes;
- equation labels sitting on diagram labels;
- too little separation between two semantic groups;
- formulas wrapping into adjacent columns;
- callout text crossing its tinted background;
- labels whose descenders/ascenders appear clipped;
- dense lines that technically do not overlap but read as one block;
- large blank space caused by over-reserving height after a collision fix.

## Release evidence

Record these fields in `render_qa`:

```json
{
  "all_pages_rendered": true,
  "text_overlap_findings": 0,
  "component_bounds_escape_findings": 0,
  "critical_equation_collision_findings": 0
}
```

Keep a rendered contact sheet or page-image set as evidence. For a known repaired page, keep a before/after image during QA even if only the final image is shipped.
