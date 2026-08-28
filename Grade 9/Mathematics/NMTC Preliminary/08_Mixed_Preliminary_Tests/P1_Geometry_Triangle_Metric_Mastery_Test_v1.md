# P1 Geometry — Triangle Metric Mastery Test v1

All questions are author-created and unlabeled by method.

## Questions

1. An altitude from `A` meets `BC` at `D`. If `BD=15`, `DC=8`, find `AB^2-AC^2`.
2. A triangle has sides `9,11,14`. Find the median to side `14`.
3. In triangle `ABC`, `AB=5`, `AC=7`, `BD=3`, `DC=5`. Find `AD^2`.
4. `AD` bisects angle `A`; `AB=8`, `AC=12`, `BC=15`. Find `AD^2`.
5. A right triangle has `R:r=13:4`. Find the primitive side ratio.
6. A triangle has a side of length `12`; its median to that side is `7`; one adjacent side is `10`. Find the square of the other adjacent side.
7. A cevian splits the opposite side into `4` and `6`. The adjacent sides are `8` and `9`, with side `8` adjacent to the segment `6`. Find the square of the cevian.
8. An altitude splits the base into `5x` and `3x`. The difference of the squares of the adjacent sides is `64`. Find the base length.
9. `A=(0,0)`, `B=(10,0)`, `C=(0,6)`. Find the median from `A` to `BC`.
10. An angle bisector joins the vertex between sides `7` and `14` to an opposite side of length `12`. Find the square of the angle-bisector length.
11. A right triangle has legs `9,12`. Find `R:r`.
12. A reproduced historical solution uses a legitimate median theorem but later asserts an angle inconsistent with the printed side lengths. State the correct publication/solution disposition.

---

# Answers and review

1. `15^2-8^2=161`.
2. `m^2=[2(81)+2(121)-196]/4=52`; `m=2sqrt13`.
3. `19`.
4. Angle-bisector split is `6,9`; `AD^2=8*12-6*9=42`.
5. normalize to hypotenuse `26`, inradius `4`; legs `10,24`; ratio `5:12:13`.
6. `4(49)=2(100)+2c^2-144`; `196=56+2c^2`; `c^2=70`.
7. Label `AB=8=c`, `AC=9=b`, `BD=4=m`, `DC=6=n`, base `10`: `81(4)+64(6)=10(d^2+24)`; `708=10d^2+240`; `d^2=234/5`.
8. `(25-9)x^2=64`; `x=2`; base `8x=16`.
9. midpoint `(5,3)`; median `sqrt34`.
10. split `4,8`; `d^2=7*14-4*8=66`.
11. hypotenuse `15`; `R=15/2`, `r=(9+12-15)/2=3`; ratio `5:2`.
12. preserve source evidence, independently recompute, classify `SOURCE_CONFLICT`, and do not silently change the stem/figure or force the supplied angle.

## Diagnostic tags

- Q1/Q8: `ALTITUDE_CANCELLATION`
- Q2/Q6: `APOLLONIUS`
- Q3/Q7: `STEWART_LABELING`
- Q4/Q10: `ANGLE_BISECTOR_STEWART`
- Q5/Q11: `RIGHT_TRIANGLE_RADIUS_METRIC`
- Q9: `COORDINATE_ROUTE`
- Q12: `SOURCE_INTEGRITY`

## Internal mastery gate

- 10/12 correct: strong transfer readiness.
- 8–9/12: repair tagged mechanisms.
- <=7/12: return to first-step cards and F1–F3 ladders before mixed Preliminary practice.
