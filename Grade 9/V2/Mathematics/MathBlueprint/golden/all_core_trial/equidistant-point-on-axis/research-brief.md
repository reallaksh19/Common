# Research brief — MEDIUM bucket

Reference: `RESEARCH-BRIEF-EQDIST-MEDIUM-v1`

Subtopic: **Point on an Axis Equidistant from Two Fixed Points**

This is pedagogy/representation research only. It does **not** expand curriculum authority.

## Representation finding 1 — derive coordinate distance from a right triangle

OpenStax presents the coordinate distance formula through the Pythagorean theorem: horizontal and vertical coordinate differences are the legs of a right triangle and the point-to-point distance is the hypotenuse.

Pedagogical consequence for Core1A:

1. Do not begin with a memorised distance formula.
2. Show `P=(x,0)` on the axis.
3. Draw the horizontal and vertical offsets from `P` to each fixed point.
4. Compress each right triangle into a squared-distance expression.
5. Only then equate the two squared distances.

Source:
https://openstax.org/books/college-algebra-2e/pages/2-1-the-rectangular-coordinate-systems-and-graphs

## Representation finding 2 — equidistance is a locus, not a shortcut

GeoGebra's perpendicular-bisector material makes visible that points equidistant from the endpoints of a segment lie on its perpendicular bisector.

Pedagogical consequence for Core1A:

- use a secondary locus diagram after the coordinate-distance model;
- show the desired answer as the intersection of the equidistant locus with the required axis;
- explicitly prevent the misconception that the axis itself must be the perpendicular bisector;
- use the locus as a geometric check, not as a replacement for the general coordinate model.

Source:
https://www.geogebra.org/m/rmpnhgc5

## Chosen visual sequence

`axis constraint -> two right triangles -> two squared distances -> equality -> cancellation -> solution -> locus cross-check`

The first two representations are primary because they explain the algebra. The perpendicular-bisector view is secondary because it gives geometric structure and a transfer bridge.

## Misconception contrast

Averaging the x-coordinates is legitimate in a symmetric case such as fixed points with the same y-coordinate. It is not a general rule. The anchor case `A(-1,4), B(7,2)` is intentionally asymmetric: averaging gives `x=3`, but the correct result is `x=9/4`.

This contrast should be shown visually before being stated algebraically.
