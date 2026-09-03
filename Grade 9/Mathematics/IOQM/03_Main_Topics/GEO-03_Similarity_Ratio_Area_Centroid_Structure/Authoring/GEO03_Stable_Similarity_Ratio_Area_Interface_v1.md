---
provider: IOQM-G9-GEO-03
status: FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL
primary_consumer: IOQM-G9-GEO-01
other_consumers: geometry-transfer
frozen_on: 2026-09-02
---
# GEO-03 Stable Similarity / Ratio / Area Interface v1

Downstream topics may RETRIEVE these facts without reteaching the GEO-03 chapter.

## Guaranteed payload
- **G03-1 Similarity proof:** AA, SAS and SSS similarity require correct correspondence; equal angles alone never prove congruence.
- **G03-2 Scale factor:** if corresponding lengths scale by `k`, all corresponding linear lengths and perimeters scale by `k`.
- **G03-3 Area scaling:** areas of similar figures scale by `k^2`; conversely an area ratio gives a positive length-scale ratio by square root only when similarity is already known.
- **G03-4 Shared-altitude area:** triangles with a common altitude have area ratio equal to base ratio.
- **G03-5 Shared-base area:** triangles with a common base have area ratio equal to perpendicular-height ratio.
- **G03-6 Parallel transfer:** a proved segment parallel to one side of a triangle creates similar triangles and transfers corresponding side ratios.
- **G03-7 Centroid ratio:** the centroid divides every median in the ratio `2:1` measured from the vertex.
- **G03-8 Centroid area:** each triangle formed by the centroid and one full side has one-third of the original triangle's area; all three medians divide the triangle into six equal-area small triangles.
- **G03-9 Area decomposition:** add/subtract regions only after expressing them on a common area scale; prefer base/height or similarity fractions to unnecessary metric lengths.
- **G03-10 Representation boundary:** ratio/area structure is primary when the answer is shape-independent; coordinates are a valid alternate/check when a line intersection becomes shorter numerically.

## Fail-closed boundaries
This interface does **not** export Stewart's theorem, angle-bisector theorem as a full cevian canon, right-triangle altitude metric packages, or triangle-feasibility canon; those belong to GEO-01. It does not export systematic vector/coordinate technique (GEO-05) or circle/cyclicity/tangency canon (GEO-04).

## Downstream retrieval cue
For GEO-01: first ask whether a cevian problem is actually only a similarity/area-transfer problem. Retrieve G03-1 through G03-9 if yes; teach new metric/cevian canon only if the target cannot be closed by this interface.
