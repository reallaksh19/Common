# Generic V2.5 stress scenarios

These tests are synthetic. They must not encode names, IDs, branches, formulas, paths or workflow semantics from any downstream project.

Current stress coverage includes:

- rich semantic serial EP admission;
- rich semantic parallel-lane EP admission;
- semantically empty current-required input rejection;
- unresolved current-required input rejection while EP claims executable state;
- semantically empty required benchmark/oracle rejection;
- `DSTEP-*` forward discovery enforcement with `DISC-*` candidate evidence;
- vague discovery instruction rejection;
- empty executable write-scope rejection;
- unstructured/empty anti-drift rejection;
- vague implementation-step rejection;
- report headings without source/reconciliation payload rejection;
- missing `REPO_PROFILE.yaml` and placeholder protocol basis rejection;
- candidate-independent `BATON_READY` before a replacement exists;
- zero-context candidate DISC/TC admission;
- candidate self-preparation/self-certification rejection;
- EP-contract digest mutation invalidating TC;
- exact DSTEP expected-output coverage in DISC receipts;
- parallel-lane takeover certification scoped to exact route/candidate;
- live candidate-specific `MATERIAL_WRITE_READY` with branch/material/hard-stop checks;
- durable `QSET-*` for `PHASE_CHANGED` qualification;
- durable `QSET-*` for same-phase `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`;
- quantitative Q2 requiring concrete payload values;
- Q3 requiring an explicit mutation, protected invariant and falsifier;
- Q4 requiring an incoming independent benchmark/oracle;
- Q5 requiring an incoming first implementation step and predicted verification;
- candidate-authored QSET rejection;
- candidate-as-independent-QUAL-evaluator rejection;
- missing required structured Q1-Q5 answer output rejection;
- QUAL result requiring five independently evaluated PASS results;
- TC requiring current QUAL id/path/digest for qualification-required routes;
- QUAL mutation after TC issuance invalidating takeover;
- legacy inline `phase_transition.questions` rejection;
- infrastructure `NOT_RUN` without automatic hard stop;
- overloaded blocker-state rejection;
- independent material authority from execution continuation;
- Owner deferral preserving pending-not-satisfied truth without granting write authority;
- topology-derived executable frontier and calculated progress denominator changes;
- context-dependent instruction rejection;
- checkpoint → successor EP baton linkage;
- Owner-intent roadmap mutation with frontier/progress-basis reconciliation;
- long-running EP continuity across explicit unaffected roadmap revisions;
- broken/missing continuity-chain rejection;
- changed contract forcing `RECONCILE_REQUIRED + READ_ONLY`;
- active use after invalidation rejection;
- evidence-preserving single- and multi-generation issue supersession;
- explicit resolution versus silent loss/mutation of inherited unresolved items;
- supersession branching/multiple-predecessor/cycle rejection;
- deep `PARENT_OF` issue projection rollups and stale-snapshot rejection;
- aggregate parent closure blocked by open child work;
- issue closure refusing hidden FAIL/NOT_RUN or unresolved work;
- hard-stop/execution consistency;
- terminal/idle empty frontier/no active EP;
- Owner-approved parallel routing, lane isolation and deferred integration;
- lane checkpoint JOIN and multi-parent convergence;
- partial lane invalidation freezing old plan and durable replan;
- completed sibling retention and exact unresolved transfer partitions;
- replan to new parallel topology with `previous_replan` binding;
- superseded plan routes no longer executable;
- multi-generation PLAN/REPLAN history, forward-link and cycle checks;
- checkpoint/join/replan predecessor-baton exclusivity;
- bootstrap/migration truth preservation;
- lifecycle-aware status/handover rendering;
- projection pending/stale versus baton/handover readiness separation;
- crash-safe projection publication and stable operation identity;
- stale external projection across multiple repository generations;
- observed generation versus newest desired generation;
- superseded projection operations with no retry authority;
- projection supersession-chain termination and obsolete receipt preservation;
- newest projection convergence to IN_SYNC;
- live serial/parallel route selection from branch/worktree;
- four-way base drift classification;
- qualified-boundary drift read-only recovery pending confirmation;
- overlapping/unknown drift withholding write authority;
- checkpoint evidence bound to the exact material reference.

The scoped CI must explicitly execute this directory with its own unittest-discovery command. Compiling these modules or discovering only the parent `tests/` directory is not stress-execution evidence.

Real repositories may be inspected read-only to discover additional failure modes. Every discovered mode must be reduced to a repository-neutral synthetic regression here before changing Common protocol logic. No downstream-project names or semantics belong in these fixtures.
