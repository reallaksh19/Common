# GEO-02 Stable Angle / Polygon Interface v1

Status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`  
Provider: `IOQM-G9-GEO-02`  
Primary consumer: `IOQM-G9-GEO-04`

Consumers retrieve these statements; they do not rebuild basic angle/polygon teaching.

## Export payload
### G02-1 - Local angle closure
Use straight-line 180 degrees, angles around a point 360 degrees, vertical equality, and triangle 180 degrees to close the smallest local network.

### G02-2 - Parallel theorem/converse discipline
Given parallel lines, corresponding/alternate relations may be used. Without given parallelism, an appropriate proved angle equality may establish parallelism by the converse. Appearance is never sufficient.

### G02-3 - Generic quadrilateral closure
Interior angles of a nondegenerate quadrilateral total 360 degrees, reconstructible by one diagonal into two triangles. Special-quadrilateral properties require separate hypotheses.

### G02-4 - Diagonal method boundary
A diagonal is useful when it decomposes the figure or exposes a proved relation; adding one that creates more independent unknowns is not automatically progress.

### G02-5 - Regular-polygon turns
For a regular n-gon: exterior turn = 360/n; interior angle = 180-360/n. For a proposed interior angle theta, feasibility requires n=360/(180-theta) to be an integer >=3.

### G02-6 - Diagonal counting
An n-gon has n(n-3)/2 diagonals by counting n-3 from each vertex and dividing the double count by 2.

### G02-7 - Proved symmetry only
Rotational/reflection symmetry may be used only when regularity, congruence, equal-distance structure or another sufficient condition has been established. Never infer it from the drawing.

### G02-8 - Representation boundary
Use local synthetic relations when they close quickly. Coordinate/vector representation is an alternate route when numerical lengths/directions make it cheaper; its canonical teaching remains GEO-05.

## GEO-04 retrieval map
| Circle consumer need | Retrieve | GEO-04 adds |
|---|---|---|
| angle chase around a circle figure | G02-1 | circle-specific angle theorem |
| prove/use parallel auxiliaries | G02-2 | circle construction context |
| distinguish cyclic from generic quadrilateral | G02-3 | cyclic criterion/relation |
| symmetry in regular/circle-linked figures | G02-7 | circle-specific consequences |
| coordinate alternative | G02-8 | circle equation/metric only if justified |

## Explicit non-exports
This interface does **not** teach centre/inscribed-angle theorems, cyclic quadrilateral canon, tangent-radius, equal tangents, alternate segment theorem, power of a point, intersecting chords/secants or other circle canon. Those belong to GEO-04.

## Compatibility tests
- retrieval without reteaching: PASS
- theorem/converse distinction: PASS
- generic-vs-cyclic boundary: PASS
- visual-symmetry fail-closed rule: PASS
- coordinate route remains alternate: PASS
