# First-Step Reference

## Fast router
1. **Prove the structure.** Never use a visual parallel/symmetry assumption.
2. **Local target?** Start with straight-line, vertical, triangle or quadrilateral closure.
3. **Regular polygon/global target?** Start with exterior turn `360/n`.
4. **Useful diagonal?** Add it only if it splits the problem into simpler pieces.
5. **Numeric lengths + fixed directions?** Test coordinate/vector representation if angle chase does not close.
6. **Discrete side assignment?** Enforce geometric feasibility before counting integer cases.

## Recognition atlas
| Cue | First useful object | Reject |
|---|---|---|
| known parallel lines | write one corresponding/alternate relation | proving parallel again |
| equal alternate/corresponding angles but no parallel given | use converse to prove parallel | assuming from picture |
| generic quadrilateral | sum of interior angles = 360 | special-quadrilateral facts |
| regular n-gon | exterior turn = 360/n | long vertex chase |
| regular polygon interior angle theta | n = 360/(180-theta) | accepting noninteger n |
| diagonal count | n(n-3)/2 | counting edges or double-counting |
| apparent mirror symmetry | identify proof obligation | trust sketch |
| trapezium lengths | |p-q| < base difference < p+q | count degenerate equality |

## Contrast strip
- Local chase vs global polygon formula: use the smallest closure.
- Synthetic vs coordinate: choose the representation with fewer independent unknowns.
- Visible symmetry vs proved symmetry: only the latter licenses equal-angle/length conclusions.
- Parallel theorem vs converse: given parallel -> equal angles; given suitable equal angles -> parallel.

## Final check
Ask: Did I use any fact that the problem never stated or proved? Did I accidentally count a degenerate figure?
