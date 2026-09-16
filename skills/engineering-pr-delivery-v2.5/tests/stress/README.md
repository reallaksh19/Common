# Generic V2.5 stress scenarios

These tests are synthetic. They must not encode names, IDs, branches, formulas, paths or workflow semantics from any downstream project.

Current stress coverage includes:

- infrastructure `NOT_RUN` without automatic hard stop;
- overloaded blocker-state rejection;
- topology-derived executable frontier;
- progress denominator changes without erasing earned work;
- context-dependent instruction rejection;
- checkpoint → successor EP baton linkage;
- Owner-intent roadmap mutation with frontier/progress-basis reconciliation;
- incoming-phase Q1-Q5 anchor grounding;
- supersession transfer into the successor;
- issue closure only after terminal roadmap/evidence state;
- hard-stop/execution consistency;
- terminal/idle relay with empty frontier and no active EP;
- Owner-approved parallel routing, lane isolation and deferred integration;
- bootstrap/migration truth preservation;
- lifecycle-aware status/handover rendering;
- required external projection pending/stale without confusing repository recovery with full handover readiness;
- in-sync projection binding to the current roadmap revision and current execution reference;
- serial/parallel EP selection from checked-out branch/worktree with ambiguity rejected;
- base drift requiring an explicit `DISJOINT` receipt before an existing EP remains executable;
- overlapping/unknown base drift invalidating the EP until reconciliation;
- checkpoint PASS/FAIL/NOT_RUN evidence bound to the exact material reference it observed.

Real repositories may be inspected read-only to discover additional failure modes. Every discovered mode must be reduced to a repository-neutral synthetic regression here before changing Common protocol logic. No downstream-project names or semantics belong in these fixtures.
