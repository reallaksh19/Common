# Teacher Diagnostic Key — GEO-01

Status: `AUTHORED_ITEMS_INDEPENDENTLY_CHECKED_V1`

This key covers `04_Recognition_and_First_Line_Lab.md`, `05_Practice_and_Transfer_Bank.md`, and `06_H0_Mastery_Test.md`.

Diagnostic codes:

- `FEASIBILITY_SKIPPED`
- `DEGENERATE_EQUALITY_ALLOWED`
- `LARGEST_SIDE_NOT_IDENTIFIED`
- `CEVIAN_MISCLASSIFIED`
- `VISUAL_PROPERTY_ASSUMED`
- `CHEAPER_GEO03_ROUTE_MISSED`
- `STEWART_OVERUSED`
- `ANGLE_BISECTOR_SIDE_MISCONCEPTION`
- `RADIUS_COMPLEMENT_MISMATCH`
- `INTEGER_FILTER_APPLIED_TOO_EARLY`
- `SOURCE_SELECTION_SEMANTICS_LOST`

---

## Recognition Lab checks

- R1: `|11-17|<x<28`, so `6<x<28`.
- R2: `(8,13)` gives `5<d<21`; `(21,30)` gives `9<d<51`; intersection `9<d<21`.
- R3: `12^2=144 < 8^2+10^2=164`, acute.
- R4: repetition permitted -> repeated minimum is legal; selection semantics must be preserved.
- R5: `BD=DC` -> `D` midpoint -> median.
- R6: ratio `3:2` alone -> arbitrary cevian with known split.
- R7: angle-bisector theorem is legal because equal vertex angles are stated.
- R8: median target -> Apollonius before Stewart.
- R9: arbitrary cevian with split -> Stewart variable map first.
- R10: right-triangle altitude -> `h^2=pq`/projection identities before Stewart.
- R11: exradii -> complement variables through area.
- R12: `Delta=rs` is direct.
- R13: geometry interval precedes integer listing.
- R14: factor pairs require parity/order/positivity checks inherited from the geometry.
- R15: parallel/similar surface -> retrieve GEO-03.
- R16: structure first; representation chosen by cost, not habit.

---

## Practice Bank solutions

### F0-1
`|10-7|<x<17`, so `3<x<17`. Integer values `4,...,16`: **13**.

### F0-2
Largest side `12`; `12^2=144<8^2+10^2=164`: **acute**.

### F0-3
`13^2=5^2+12^2`: **right**. Equality is the right-triangle boundary, not acute.

### F1-1
`BM=7`. Apollonius:

`13^2+15^2=2(AM^2+7^2)`.

`394=2AM^2+98`, so `AM^2=148`; therefore `AM=2sqrt(37)`.

### F1-2
`BD:DC=3:5` and `BD+DC=24`, so **`BD=9`, `DC=15`**.

### F1-3
No special-cevian property is legal from visual symmetry alone. Treat `AD` as an **arbitrary cevian** until a special property is stated/proved. Diagnostic: `VISUAL_PROPERTY_ASSUMED`.

### F2-1
Map `BD=m=6`, `DC=n=8`, `AC=b=15`, `AB=c=13`, `AD=d`.

Stewart:

`15^2*6 + 13^2*8 = 14(d^2+48)`.

`1350+1352=14d^2+672`, hence `14d^2=2030`, so **`AD^2=145`**.

### F2-2
`h^2=9*16=144`, so **`h=12`**. Hypotenuse `=25`.

Leg squares: `25*9=225` and `25*16=400`, so legs **`15,20`**.

### F2-3
Let `x=s-a`, `y=s-b`, `z=s-c`. With exradii `6,3,2`,

`x=Delta/6`, `y=Delta/3`, `z=Delta/2`.

Then `s=x+y+z=Delta`, while Heron gives

`Delta^2=sxyz = Delta*(Delta^3/36)`.

For positive area, `Delta=6`. Thus `x=1,y=2,z=3`, giving

**`a=5,b=4,c=3`**.

### F3-1
Equal sides `a`, base `31-2a`.

Positivity: `a<=15`. Triangle inequality: `31-2a<2a`, so `a>=8`.

`a=8,...,15`: **8 triangles**.

### F3-2
Repetition is permitted, so hardest triple is `(n,n,n+30)`.

Require `(n+30)^2<2n^2`, equivalent to `n>30(1+sqrt2)≈72.43`.

Least integer: **73**.

### F3-3
If legs are `a,b`, hypotenuse `c`, altitude `10`, area gives `ab=10c`. Let `L=a+b`; integer perimeter and integer `c` make `L` integer.

`L^2=a^2+b^2+2ab=c^2+20c`.

Hence

**`(c+10)^2-L^2=100`**, i.e. **`(c+10-L)(c+10+L)=100`**.

Only after this point should factor-pair filtering begin.

### F4-1
For `(9,16)`, `7<d<25`; for `(25,40)`, `15<d<65`. Intersection: `15<d<25`. Only **20** works.

### F4-2
Parallel information naturally produces similarity/ratio structure already frozen in GEO-03. Stewart adds unnecessary metric algebra. Diagnostic if missed: `CHEAPER_GEO03_ROUTE_MISSED`.

### F4-3
`BD:DC=2:1` does not prove an angle bisector. Legal first routes include treating `AD` as an arbitrary ratio-marked cevian, then using stated right-triangle relations or Stewart only if needed. Diagnostic: `CEVIAN_MISCLASSIFIED`.

### F4-4
Coordinates are cheaper when a natural axis placement makes the target one or two equations; synthetic metric remains preferable when a direct theorem closes the target immediately.

---

## H0 Mastery solutions

### M1
`8<x<32`. Integers `9,...,31`: **23**.

### M2
Three values must be distinct. The hardest legal triple is `(n,n+4,n+24)`.

Require

`(n+24)^2 < n^2+(n+4)^2`.

This becomes

`n^2-40n-560>0`.

Positive root is `20+8sqrt(15)≈50.98`, so least integer **`n=51`**.

If the learner instead uses `(n,n,n+24)`, diagnose `SOURCE_SELECTION_SEMANTICS_LOST`.

### M3
`BD=DC` proves `D` is midpoint and `AD` is a **median**. No altitude or angle-bisector property follows without additional proof.

### M4
`BM=6`. Apollonius:

`10^2+14^2=2(AM^2+6^2)`.

`296=2AM^2+72`, so **`AM^2=112`**.

### M5
Angle-bisector theorem gives `BD:DC=7:5`. With sum `36`, one part is `3`; hence **`BD=21`, `DC=15`**.

### M6
Map `m=5`, `n=9`, `b=AC=13`, `c=AB=15`.

`13^2*5+15^2*9=14(AD^2+45)`.

`845+2025=14AD^2+630`, so `14AD^2=2240`; therefore **`AD^2=160`**.

### M7
**Altitude `12`, hypotenuse `25`, legs `15,20`** by `h^2=pq` and leg-projection identities.

### M8
Same complement reconstruction as F2-3: **`a=5,b=4,c=3`**.

### M9
Equal sides `a`, base `25-2a`. Positivity gives `a<=12`; triangle inequality gives `25<4a`, so `a>=7`. Values `7,...,12`: **6 triangles**.

### M10
The drawing cannot establish perpendicularity or angle bisection. The strongest legal classification from `BD:DC=2:1` is **arbitrary cevian with a known side split**. Diagnostics: `VISUAL_PROPERTY_ASSUMED`, `CEVIAN_MISCLASSIFIED`.

---

## Readiness interpretation

Static item mathematics above has been independently recomputed in this key. This does **not** constitute classroom timing, readability, retention, psychometric, qualification/pass-mark or publication calibration; those remain `NOT_RUN` until separately performed.
