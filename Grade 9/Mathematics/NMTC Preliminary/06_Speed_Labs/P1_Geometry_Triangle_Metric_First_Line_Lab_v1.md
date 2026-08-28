# P1 Geometry — Triangle Metric First-Line Lab v1

Write only the first useful mathematical line.

1. `D` is midpoint of `BC`; sides around `A` are `b,c`; `BC=a`; median `AD=m_a`.
2. `AD perpendicular BC`, with `BD=p`, `DC=q`; target `AB^2-AC^2`.
3. General cevian `AD=d`, `BD=m`, `DC=n`, `AB=c`, `AC=b`.
4. `AD` bisects angle `A`, with `AB=c`, `AC=b`.
5. Right triangle has circumradius `R`.
6. Right triangle has hypotenuse `h` and inradius `r`.
7. Two medians are perpendicular and coordinates are permitted.
8. A median length is known and one side is unknown.
9. An angle bisector length is asked after `BD,DC` are known.
10. A source solution's numerical angle disagrees with an independent side check.
11. Stewart is forgotten but the general cevian configuration is available.
12. A right triangle gives only `R:r`; leg ratio is requested.

## First-line key

1. `b^2+c^2=2m_a^2+a^2/2`.
2. `AB^2-AC^2=BD^2-DC^2=p^2-q^2`.
3. `b^2m+c^2n=(m+n)(d^2+mn)`.
4. `BD/DC=AB/AC=c/b`.
5. `h=2R`.
6. `p+q=h+2r`.
7. choose origin/coordinate vectors and write a dot-product condition.
8. rearrange Apollonius before solving any angle.
9. `AD^2=AB*AC-BD*DC` after the bisector split is established.
10. mark `SOURCE_CONFLICT`; recompute instead of reconciling by assumption.
11. drop an altitude and write the two Pythagorean equations.
12. normalize `h=2R`, then use `p+q=h+2r` and Pythagoras.

## Timing target

12 correct first lines in <=4 minutes, with at most one label error.
