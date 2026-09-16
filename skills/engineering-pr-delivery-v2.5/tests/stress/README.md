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
- terminal/idle relay with empty frontier and no active EP.

Real repositories may be inspected read-only to discover additional failure modes. Every discovered mode must be reduced to a repository-neutral synthetic regression here before changing Common protocol logic.
