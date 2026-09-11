# Appendix B — Method Coverage and Independent Answer Check

| ID | Primary skill | Hint depth | Figure | Answer | Independent recomputation |
|---|---|---|---|---:|---|
| B1 | GEO-TRI-01 · Check triangle legality and type first | H1 | Not required | 7 | Let sides be a,a,b with 2a+b=29; triangle inequality gives a=8,…,14 → 7. |
| B2 | GEO-TRI-01 · Check triangle legality and type first | H1-H2 | Not required | 92 | Test the three pairings of side pairs across a diagonal; allowable candidates are 10,12,18,22,30 → 92. |
| B3 | GEO-MENS-01 · Read 3D and mensuration data correctly | H1-H2 | Not required | 8 | 2πr(r+h)=2πr²h → (r−1)(h−1)=1 → r=h=2 → k=8. |
| B4 | GEO-POLY-01 · Think in exterior turns | H1 | Not required | 11 | m must divide 360 and 180−360/m must be even; m=3,4,5,6,9,10,12,15,18,20,30 → 11. |
| B5 | GEO-MENS-01 · Read 3D and mensuration data correctly | H1-H2 | Not required | 40 | Distance²=20; interpreting it as a body diagonal minimizes s²=20/3, so surface area=6s²=40. |
| B6 | GEO-COORD-01 · Place coordinates to remove constraints | H1-H3 | Present | 54 | Coordinates give E=(8,12), F=(4,12), AE∩BF=(6,9); [MAB]=12·9/2=54. |
| B7 | GEO-MEDIAN-01 · Classify medians and use the centroid | H1-H2 | Present | 15 | Vector/area computation gives [GYZ]/[ABC]=1/48; 720/48=15. |
| B8 | GEO-TRI-01 · Check triangle legality and type first | H1-H3 | Not required | 49 | Worst triple is n,n,n+20; acute requires (n+20)²<2n² → n≥49. |
| B9 | GEO-RIGHT-01 · Exploit right-triangle structure first | H1 | Not required | 12 | h²=pq=36 and c=p+q≥2√pq=12. |
| B10 | GEO-RIGHT-01 · Exploit right-triangle structure first | H1-H3 | Present | 8 | Set BD=3t, DC=t, AB=x. Equation gives AC=x+2t; Pythagoras gives x=3t, AC=5t → 5+3=8. |
| B11 | GEO-TANGENT-01 · A tangent creates a right angle and equal tangent lengths | H1-H3 | Present | 12 | With AB as common chord and OA⊥AB, the two internal-tangency solutions have radii whose sum is 12. |
| B12 | GEO-CIRCLE-01 · Track the chord or arc | H1-H3 | Present | 15 | Altitude is 3√7; circumradius and centre offset give half-chord 15/2, so PQ=15. |
| B13 | GEO-PTOLEMY-01 · Turn a cyclic quadrilateral into one length equation | H1 | Not required | 13 | Rectangle diagonal √(5²+12²)=13. |
| B14 | GEO-POWER-01 · Choose the correct power product | H1 | Not required | 18 | PT²=PA·PB → 144=8·PB → PB=18. |
| B15 | GEO-CEVA-01 · Use side ratios to test concurrency | H1-H2 | Present | 23 | Ceva: (2/3)(4/5)(AF/FB)=1 → AF:FB=15:8 → 23. |
| B16 | GEO-MENELAUS-01 · Use directed ratios to test collinearity | H1-H2 | Present | 4 | Directed Menelaus gives signed AF/FB=−1/3, so |AF:FB|=1:3 → 4. |
| B17 | GEO-TRIG-01 · Use trigonometry only when it shortens the geometry | H1 | Not required | 72 | Sine rule: b/sin45°=6/sin30° → b=6√2 → b²=72. |
| B18 | GEO-COORD-01 · Place coordinates to remove constraints | H1 | Not required | 8 | y=3 in x²+y²=25 gives x=±4 → PQ=8. |
| B19 | GEO-VECTOR-01 · Use vectors for centroids and repeated parallelograms | H1 | Not required | 10 | D=A+C−B=(7,3) → u+v=10. |
| B20 | GEO-LOCUS-01 · Translate equidistance into a locus or construction | H1 | Not required | 4 | Equidistant from coordinate axes means y=±x; y=2 gives (±2,2), distance 4. |