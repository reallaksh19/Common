# GEO-04 Independent Mathematics and Source Audit

Status: `HISTORICAL_ANSWERS_INDEPENDENTLY_CLOSED_PAGE_IMAGE_CUSTODY_PENDING`

All five historical numerical answers are re-derived below from the controlled source statements. Official/verification answers are used only as final checks. Exact page-image custody remains a separate publication gate.

## IOQM-2025-Q19 — square in a right triangle, one vertex on a circle

Use coordinates

- `B=(0,0)`, `C=(2,0)`, `A=(0,1)`;
- let square `DEFG` have side `s` with `D=(d,0)`, `E=(d+s,0)`, `F=(d+s,s)`, `G=(d,s)`.

Because `F` lies on `AC`, whose equation is `y=1-x/2`,

`s = 1-(d+s)/2`,

so

`d+3s=2`.

The circle through `B` with centre `A` has radius `AB=1`. Since `G=(d,s)` lies on it,

`d^2+(s-1)^2=1`.

Substitute `d=2-3s`:

`(2-3s)^2+(s-1)^2=1`,

which gives the admissible interior-square solution

`s=2/5`, `d=4/5`.

Square area:

`s^2=4/25`.

Therefore `m+n=4+25=29`.

Independent result: `29` — PASS.

---

## IOQM-2025-Q23 — cyclic rectangle constraint

Normalize `AB=CD=1` and place

- `A=(0,0)`, `B=(1,0)`, `C=(1,h)`, `D=(0,h)`;
- `M=(u,0)` on `AB`;
- `N=(1,v)` on `BC`.

### Condition `MC=CD`

`(1-u)^2+h^2=1`, hence

`h^2=2u-u^2`.

### Cyclicity of `C,D,M,N`

The circle through `C,D,M` gives, after substituting `N`,

`(v-h)(hv+u^2-u)=0`.

The source's canonical non-degenerate reading has `N != C`, so `v != h`. Therefore

`hv=u-u^2=u(1-u)`.

Thus

`v^2 = u(1-u)^2/(2-u)`.

### Condition `MD=MN`

`u^2+h^2=(1-u)^2+v^2`,

so using `h^2=2u-u^2`,

`v^2=4u-u^2-1`.

Equating the two formulas for `v^2` simplifies to

`2u^2-4u+1=0`.

The admissible root on the side is

`u=1-sqrt(2)/2`.

Then

`h^2=2u-u^2=1/2`.

Hence

`(AB/BC)^2 = 1/h^2 = 2 = 2/1`.

Therefore `m+n=3`.

Independent result: `03` — PASS.

The degenerate `N=C` branch is deliberately excluded in accordance with the source/final-key custody note.

---

## IOQM-2025-Q30 — two internally tangent circles

Let the outer circle have centre `O=(0,0)` and radius `10`. The two inner circles have radii `r1,r2` and centres `C_i=(t_i,q)`.

The two inner circles intersect at `A,B`, so their common chord `AB` is perpendicular to `C1C2`. Since `angle OAB=90 degrees`, `OA` is also perpendicular to `AB`; therefore choose axes so

`A=(d,0)` and the common line of centres is horizontal.

For each inner circle:

- internal tangency to the outer circle gives
  `t_i^2+q^2=(10-r_i)^2`;
- `A` lies on the inner circle, so
  `(t_i-d)^2+q^2=r_i^2`.

Subtracting gives

`2dt_i-d^2=100-20r_i`,

hence

`r_i = 5+d^2/20 - d t_i/10`.

Substitute this into `t_i^2+q^2=(10-r_i)^2`:

`400t^2+400q^2=(100-d^2+2dt)^2`.

This is a quadratic in `t` whose two roots are `t1,t2`. Its `t^2` and `t` coefficients give

`t1+t2=d`.

Therefore

`r1+r2 = 10+d^2/10 - d(t1+t2)/10 = 10`.

Independent result: `10` — PASS.

---

## IOQM-2024-Q17 — chord through midpoint in an isosceles circumcircle

Place the isosceles triangle symmetrically:

- `B=(-15,0)`, `C=(15,0)`;
- `A=(0,h)` with `h=sqrt(20^2-15^2)=5sqrt(7)`;
- `D=(0,0)` and midpoint `M=(0,h/2)`.

Let circumcentre be `O=(0,k)`. From `OA=OB`:

`(h-k)^2=15^2+k^2`,

so

`k=-5/sqrt(7)`.

Then

`R^2=OB^2=225+25/7=1600/7`.

The chord `PQ` through `M` is horizontal. Its half-length is

`sqrt(R^2-(h/2-k)^2)`.

Now

`h/2-k = 5sqrt(7)/2 + 5/sqrt(7) = 45/(2sqrt(7))`.

Hence the half-chord square is

`1600/7 - 2025/28 = 625/4`,

so the half-length is `25/2` and

`PQ=25`.

Independent result: `25` — PASS.

---

## IOQM-2023-Q15 — two circumcentres in a unit square

Let the unit square be

`A=(0,0)`, `B=(1,0)`, `C=(1,1)`, `D=(0,1)`.

Write

`M=(1,1-u)`, `N=(1-v,1)`

with `u,v>0`. Then

`MC=u`, `CN=v`, `MN=sqrt(u^2+v^2)`.

The perimeter condition for `triangle MCN` is

`u+v+sqrt(u^2+v^2)=2`.

Let `O` be the circumcentre of `triangle MAN`, and `P` the circumcentre of `triangle MON`. Solving the two perpendicular-bisector systems and simplifying gives

`OP^2/OA^2 = [(u^2-2u+2)(v^2-2v+2)] / [4(u+v-2)^2]`.

Set `s=u+v`, `p=uv`. From the perimeter condition,

`u^2+v^2=(2-s)^2`.

Since `u^2+v^2=s^2-2p`, this gives

`p=2s-2`.

The numerator is symmetric and simplifies to

`(u^2-2u+2)(v^2-2v+2)`
`= 2s^2-2sp-4s+p^2+4`
`= 2(s-2)^2`.

Therefore

`OP^2/OA^2 = 2(s-2)^2/[4(s-2)^2] = 1/2`.

Thus `m/n=1/2` and

`m+n=3`.

Independent result: `03` — PASS.

---

## Audit disposition

- historical numerical answers independently re-derived: 5/5 PASS;
- generic angle facts retrieved rather than retaught: PASS;
- circle-specific mechanism ownership retained: PASS;
- non-degenerate Q23 reading preserved: PASS;
- exact HBCSE source page-image visual custody: `PENDING` due current screenshot-fetch failure;
- 2023 source statement visually confirmed from the validated paper page;
- classroom timing/readability: `NOT_RUN`.

Next authoring gate: seven A-P microstream interfaces, with a recognition-chain router that asks `what proves circle structure here?` before theorem selection.
