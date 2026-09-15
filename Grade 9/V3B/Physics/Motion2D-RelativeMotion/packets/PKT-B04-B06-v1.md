# PKT-B04-B06-v1 — planar motion and relative velocity

**Buckets:** B04–B06. **State:** reviewable self-review packet; cold independent restart NOT_RUN.

Immutable dependencies: frozen corpus `SYN-M2D-20260915-V1` SHA-256 `6aac1841445e051244c3ad41f2d1ccab0d21e486b92efd0da68a87298bb29648`; 159-atom inventory; baseline coverage/registers; V3B PR #364 `6be71db1a321c449131a26ee3084b6b9c0edca28`. Live PR #350 scope transition is documented in `../qa/live-authority-reconciliation.md` and does not replace V3B 2D semantics.

## Source/data obligations

Q02: positions (0,0) at 0 s, (6,8) at 2 s, (12,16) at 4 s, then stationary through 6 s; correct 0–4 velocity is (3,4) m/s and full-run average velocity is (2,8/3) m/s. Q04: A=8 m/s east, B=5 m/s east, initial gap 30 m; relative +3 m/s, catch at 10 s/x=80 m. Q05: 50 m apart, velocities +6 and -4 m/s; meet in 5 s at x=30 m. Q06: relative vector (3,-4) m/s, magnitude 5 m/s; 50 m relative displacement after 10 s; observer reversal negates the vector. Q11: 36 km/h=10 m/s, other speed 2 m/s same direction, relative 8 m/s, 160 m in 20 s. Q12 has missing directions and remains scientifically underdetermined.

## Equation/semantic obligations

Constant planar motion uses `x=x0+vx t`, `y=y0+vy t` with one clock. Relative velocity is target minus observer, component by component, in a common frame and unit system. Relative position evolves as `r_A/B(t)=r_A/B(0)+v_A/B t`; zero relative velocity does not imply zero separation. Observer reversal negates relative velocity. No trigonometric component resolution is required.

## Representations

Canonical assets: `xy-time-graphs.svg`, `relative-1d-signline.svg`, `relative-subtraction.svg`, plus `frames-axes-clock.svg`. Check graph time axes, sign conventions and subtraction-arrow direction.

The B05E extension reuses the relative-position equation: equal ground velocities preserve a possibly nonzero initial separation. It is isolated under `../changes/extension-equal-velocity-v1/`; frozen Core2 and baseline registers remain historical.

**Next action:** open B04–B06 inventory/coverage rows and linked Core anchors; verify units/sign order and extension staleness receipt before any modification.
