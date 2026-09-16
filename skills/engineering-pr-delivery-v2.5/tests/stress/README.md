# Generic V2.5 stress scenarios

These tests are synthetic. They must not encode names, IDs, branches, formulas, paths or workflow semantics from any downstream project.

Current stress coverage includes:

- rich semantic serial and parallel-lane EP admission;
- typed current-required input and benchmark/oracle semantics;
- `DSTEP-*` discovery, bounded scope, structured anti-drift and implementation-step validation;
- structured ordered `next_work.steps[]` with current EP input/test/benchmark/acceptance references;
- non-contiguous/vague next-work rejection;
- report headings without source/reconciliation payload rejection;
- complete Objective -> Phase -> WP progress-row coverage;
- active EP -> implementation-step -> acceptance-criterion progress coverage;
- calculated bucket percentages and progress-basis binding;
- stale REPO_STATE phase/EP progress mirrors rejected;
- status/handover rendering derived from PROGRESS rather than stale mirrors;
- complete handover checklist rendering Objective -> Phase -> WP -> Step -> AC;
- acceptance status/percent/basis rendered from authoritative progress rows;
- exact ordered next work rendered with targets, inputs, tests, benchmarks, acceptance, expected result and stop conditions;
- derived structured report projection source-bound to roadmap/progress/EP/checkpoint/issue/state digests;
- report projection changing when source progress changes rather than retaining stale generated truth;
- bootstrap producing a complete zero-weight progress hierarchy without fabricating executable work;
- parallel join reconciling integration progress before cold start;
- parallel/join/replan custody detail preserved through WP-04 renderer changes;
- missing `REPO_PROFILE.yaml` and placeholder protocol basis rejection;
- candidate-independent `BATON_READY` before a replacement exists;
- zero-context candidate DISC/TC admission and candidate self-certification rejection;
- route/candidate-scoped parallel takeover and live `MATERIAL_WRITE_READY`;
- strong QSET/QUAL qualification for phase and material-boundary changes;
- quantitative reconstruction, falsifier, independent oracle and first-safe-slice qualification checks;
- QUAL mutation after TC issuance invalidating takeover;
- legacy inline phase-question rejection;
- infrastructure `NOT_RUN` without automatic hard stop;
- overloaded blocker-state rejection;
- independent material authority from execution continuation;
- Owner deferral preserving pending-not-satisfied truth without granting write authority;
- topology-derived frontier and roadmap continuity across revisions;
- checkpoint -> successor EP baton linkage;
- Owner-intent roadmap mutation with frontier/progress-basis reconciliation;
- evidence-preserving single- and multi-generation issue supersession;
- deep parent/child issue projection and closure rules;
- hard-stop/execution consistency and terminal/idle recovery;
- Owner-approved parallel routing, join, partial failure/replan and multi-generation replan history;
- stale predecessor-plan route rejection;
- projection generation crash recovery and stale external projection convergence;
- live serial/parallel route selection from branch/worktree;
- four-way base drift classification and qualified-boundary confirmation;
- checkpoint evidence bound to the exact material reference.

The scoped CI must explicitly execute this directory with its own unittest-discovery command. Compiling these modules or discovering only the parent `tests/` directory is not stress-execution evidence.

Real repositories may be inspected read-only to discover additional failure modes. Every discovered mode must be reduced to a repository-neutral synthetic regression here before changing Common protocol logic. No downstream-project names or semantics belong in these fixtures.
