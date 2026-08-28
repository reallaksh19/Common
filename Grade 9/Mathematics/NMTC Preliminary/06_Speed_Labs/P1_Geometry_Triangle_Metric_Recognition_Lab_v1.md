# P1 Geometry — Triangle Metric Recognition Lab v1

Target: identify the best first move in <=15 seconds. Do not solve.

## Prompts

1. A cevian meets the midpoint of the opposite side; all three side lengths are known.
2. An altitude splits the base into two known pieces; target is the difference of squares of the other two sides.
3. A general cevian splits the base into unequal known lengths; its length is required.
4. A segment bisects the vertex angle; the two adjacent side lengths are known.
5. A segment is both a median and perpendicular to another median.
6. A right triangle gives `R` and `r`.
7. A median length and two side lengths are given; recover the third side.
8. A general cevian problem has `AB,AC,BD,DC` known.
9. A historical geometry item has a supplied answer but missing exact figure labels.
10. A triangle gives two sides and included angle but no side split.
11. An angle bisector length is required after the base ratio is known.
12. Two right triangles share the same altitude.
13. A midpoint appears, but the target is a side relation rather than the median itself.
14. A right triangle gives hypotenuse and inradius.
15. A triangle problem is dominated by perpendicularity of two vectors.
16. Stewart's formula is forgotten during a test.
17. A reproduced solution uses Apollonius, but later angle data contradict the side lengths.
18. A cevian happens to divide the base equally.
19. A target is `AB^2-AC^2` and an altitude foot is present.
20. A right triangle asks for half-angle information after an `R:r` ratio is given.

## Recognition key

1. Apollonius.
2. Subtract Pythagoras.
3. Stewart.
4. Angle-bisector theorem first.
5. Coordinates/vectors deserve priority consideration.
6. `h=2R`, `p+q=h+2r`.
7. Apollonius rearranged.
8. Stewart.
9. Figure/source gate; do not canonicalize.
10. Cosine law may be cheaper.
11. Stewart after angle-bisector split.
12. Subtract the two Pythagorean equations.
13. Apollonius as an elimination relation.
14. `p+q=h+2r` plus Pythagoras.
15. Dot product / coordinates.
16. Drop an altitude and derive from two Pythagorean equations.
17. `SOURCE_CONFLICT`; recompute independently.
18. Apollonius specialization of Stewart.
19. Altitude cancellation.
20. Convert radius data to side data before half-angle formulas.

## Error tags

- `SEGMENT_TYPE_MISREAD`
- `STEWART_LABEL_SWAP`
- `MEDIAN_ASSUMED_FROM_CEVIAN`
- `ANGLE_BISECTOR_ASSUMED_MEDIAN`
- `ALTITUDE_SOLVED_UNNECESSARILY`
- `VECTOR_ROUTE_MISSED`
- `RADIUS_METRIC_MISSED`
- `SOURCE_FIGURE_ASSUMED`
