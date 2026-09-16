# Performance blueprint

## WHEN TO APPLY
Apply when the slice can materially affect latency, throughput, memory, CPU, I/O, startup, payload size, rendering responsiveness, solver time, or scaling behavior. Do not apply to trivial edits without a credible performance path.

## REQUIRED INPUTS
Performance-sensitive path, workload/profile, baseline measurement, target/budget where authoritative, environment, representative data, and acceptance criteria.

## PROCEDURE
1. Identify the user/system metric that matters and the code path that controls it.
2. Establish a reproducible baseline under representative conditions.
3. Measure the changed implementation using the same method.
4. Attribute material regressions/improvements to concrete causes; avoid optimizing noise.
5. Check worst-case or scale-sensitive behavior when the algorithm/data shape changed.

## BEST-PRACTICE CHECKLIST
- Same environment/workload for comparison.
- Warmup/cache effects understood where relevant.
- Measure before optimizing.
- Complexity and allocation/I/O changes reviewed.
- User-perceived responsiveness considered, not only aggregate throughput.

## ANTI-PATTERNS
Microbenchmarking irrelevant code, single noisy samples, changing benchmark and implementation together without basis, performance claims without data, and sacrificing correctness/clarity for unmeasured speed.

## REQUIRED ARTIFACTS
Baseline/after measurements, command/workload/environment, interpretation, and QRV finding for unresolved regressions or uncertainty.

## VERIFICATION
Repeat representative measurements enough to distinguish signal from noise and reconcile against any authoritative budget/tolerance.

## QUALITY FINDING CLASSIFICATION
Use PERFORMANCE. A regression can be HIGH/CRITICAL while still separate from hard-stop semantics unless acceptance/safety/authority makes it non-negotiable.

## TRUE HARD-STOP CONDITIONS
Only map to an existing hard stop when the regression violates a protected invariant, required safe operating bound, or other explicit authority. Ordinary optimization opportunity is not a stop.

## OWNER REPORT
Report metric, baseline/after, user/system consequence, confidence, and whether a product tradeoff decision is required.

## SUCCESSOR HANDOVER
Transfer workload, commands, environment, baseline, observed variance, unresolved bottleneck, and exact next measurement.
