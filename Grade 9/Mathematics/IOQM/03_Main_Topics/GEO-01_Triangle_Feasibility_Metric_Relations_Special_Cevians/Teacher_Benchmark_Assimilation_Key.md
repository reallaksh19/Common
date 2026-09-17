# Teacher Benchmark Assimilation Key — GEO-01

Status: `STATIC_BENCHMARK_KEY_V1`

Use this key to diagnose method selection, not merely final arithmetic.

## A. RECONNECT expected responses

1. `|p-q|<d<p+q`; equality is degenerate.
2. Sort the side lengths and identify the largest side `c` before comparing `c^2` with `a^2+b^2`.
3. `BD=DC` (or equivalent proved midpoint condition) makes `AD` a median.
4. `angle BAD=angle DAC` makes `AD` an angle bisector.
5. When the cevian is a median and the target is metric from side lengths, Apollonius is the special cheaper relation.
6. Write the Stewart variable map: which side is `m`, `n`, `b`, `c`, and which cevian is `d`.
7. Test `h^2=pq` and the projection/area identities before a general cevian theorem.
8. `x=s-a`, `y=s-b`, `z=s-c`.
9. Derive the continuous geometric interval/equation first; filter integers afterward.
10. Retrieve GEO-03 when the surface is fundamentally similarity, parallel transfer, area-ratio or centroid structure.

## B. Error-lab repairs

### Error 1
Positive lengths are insufficient. Require all strict triangle inequalities, or the compressed interval when two sides are fixed. Code: `FEASIBILITY_SKIPPED`.

### Error 2
The square test is controlled by the largest side. Code: `LARGEST_SIDE_NOT_IDENTIFIED`.

### Error 3
Visual symmetry has no evidentiary force. Midpoint must be stated/proved. Codes: `VISUAL_PROPERTY_ASSUMED`, `CEVIAN_MISCLASSIFIED`.

### Error 4
Angle-bisector theorem gives `BD/DC=AB/AC`; midpoint follows only if `AB=AC`. Code: `ANGLE_BISECTOR_SIDE_MISCONCEPTION`.

### Error 5
Use the hierarchy: GEO-03/special cevian/right-triangle direct route before Stewart when cheaper. Code: `STEWART_OVERUSED` or `CHEAPER_GEO03_ROUTE_MISSED`.

### Error 6
Continuous geometry first, integer filtering second. Code: `INTEGER_FILTER_APPLIED_TOO_EARLY`.

### Error 7
Selection semantics are source data. “Distinct” and “with repetition/not necessarily distinct” produce different extremal triples. Code: `SOURCE_SELECTION_SEMANTICS_LOST`.

### Error 8
Numerical answer verification does not establish exact printed incidence/marks/labels. Publication requires exact source-page/figure custody.

## C. ADOPT reference first lines

1. `|19-14|<x<33`, so `5<x<33`.
2. Largest side is `15`; compare `15^2` with `10^2+11^2` after confirming feasibility.
3. `BM=CM=BC/2`; use Apollonius.
4. `BD/DC=AB/AC` and `BD+DC=BC`.
5. Treat `AD` as arbitrary with known split `2:3`; use a direct special structure only if separately stated/proved, otherwise Stewart may be the fallback.
6. `h^2=pq`, `c=p+q`.
7. `x=Delta/r_a`, `y=Delta/r_b`, `z=Delta/r_c`, with `x=s-a`, etc.
8. Write a strict feasibility interval for the diagonal from each side-pair, then intersect.
9. State the real-valued metric equation/interval before divisibility/factor/integer tests.
10. Name corresponding similar triangles and retrieve the GEO-03 ratio relation.

## D. TRANSFER interpretation

1. Invariant: one diagonal must be a legal third side in two triangles simultaneously.
2. Algebra produces candidates; strict triangle feasibility can reject algebraically valid but geometrically impossible candidates.
3. The extremal acute condition is `c^2<a^2+b^2`; source rules determine the legal maximum `c` and legal minimum `a,b`.
4. Ratio-marked does not mean special. If right-triangle Pythagorean/projection structure directly targets the unknown, use it before Stewart.
5. Exradius data and complement data are linked through `Delta=r_a(s-a)` etc.; the reconstruction invariant is the complement triple.
6. Midpoint/perpendicular/angle-bisector/ratio information must remain explicit after changing representation.
7. If similarity already closes the target, GEO-03 is cheaper and avoids duplicate teaching.
8. Mechanism summaries and independently verified answers may remain in audit/teacher records; exact historical figure/stem must not be rendered/promoted until custody closes.

## E. Assimilation-test scoring

Award one point for each of the six responses only when the learner:

- names a legal structure rather than a visual impression;
- cites the earning hypothesis;
- writes a relation that directly targets the quantity;
- identifies a genuinely tempting wrong/inefficient route;
- preserves the exact discrete/source condition;
- transfers the invariant without importing an unstated property.

Suggested static interpretation:

- `6/6`: method-selection behavior demonstrated on this prompt;
- `4-5/6`: targeted repair required;
- `0-3/6`: return to Recognition/First-Line Lab.

This rubric is a static authoring rubric only. It is **not** a psychometric cut score or classroom qualification threshold.
