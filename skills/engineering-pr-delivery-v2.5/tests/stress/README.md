# Generic V2.5 stress scenarios

These tests are synthetic. They must not encode names, IDs, branches, formulas, paths or workflow semantics from any downstream project.

Current stress coverage includes:

- infrastructure `NOT_RUN` without automatic hard stop;
- overloaded blocker-state rejection;
- topology-derived executable frontier;
- progress denominator changes without erasing earned work;
- context-dependent instruction rejection;
- checkpoint → successor baton linkage;
- Owner-intent roadmap mutation with frontier/progress-basis reconciliation;
- incoming-phase Q1-Q5 anchor grounding;
- supersession transfer into the successor;
- issue closure only after terminal roadmap/evidence state;
- hard-stop/execution consistency;
- terminal relay with empty frontier and no active EP;
- Owner-approved parallel routing with exact lane/frontier equality;
- unique branch/worktree routing and lane EP cold-start validation;
- write-domain overlap rejection unless explicitly Owner-approved;
- integration dependency on every parallel lane;
- `INITIALIZING` bootstrap with no fabricated executable EP;
- V2 inventory/reconciliation that never auto-promotes a legacy endpoint;
- lifecycle-aware status and handover rendering for parallel/initializing states.

Real repositories may be inspected read-only to discover additional failure modes. Every discovered mode must be reduced to a repository-neutral synthetic regression here before changing Common protocol logic.

The scoped `.github/workflows/engineering-pr-delivery-v2.5.yml` workflow compiles the V2.5 Python and executes the complete unit/stress suite with PyYAML whenever the V2.5 skill changes.
