# Roadmap Registry Template

Recommended repository path:

```text
docs/roadmaps/ROADMAP_REGISTRY.md
```

Template:

```text
# Engineering Roadmap Registry

ROADMAP_REGISTRY_VERSION: 1
ROADMAP_AUTHORITY: OWNER_CONTROLLED
ROADMAP_WRITE_POLICY: EXPLICIT_OWNER_AUTHORIZATION_REQUIRED
LAST_OWNER_DECISION_REF: <INITIAL_OWNER_BASELINE | agents/chains/.../roadmap-decisions/RD-xxxx.md>

| Roadmap ID | Domain | Path | Applies to paths / authority | State |
|---|---|---|---|---|
| WRC-OVERALL | WRC / EMP.1 | docs/roadmaps/Overallroadmap_wrc.md | src/core/emp1/**; docs/emp1/**; validation/emp1/** | ACTIVE |
| LAFEA-OVERALL | LAFEA | docs/roadmaps/Overallroadmap_lafea.md | src/core/lafea/**; docs/lafea/**; validation/lafea/** | ACTIVE |
| LOADCALC-OVERALL | LoadCalc | docs/roadmaps/Overallroadmap_loadcalc.md | src/core/loadcalc/**; docs/loadcalc/** | ACTIVE |
```

## Routing rules

Before coding:

1. read the registry when present;
2. match the issue, authority domain, expected paths, benchmark/oracle domains, and dependencies;
3. read every matching active roadmap;
4. pin exact roadmap blob SHA(s) in `ACTIVE.md` and the active endpoint;
5. if multiple roadmaps apply, read all of them and reconcile conflicts before coding;
6. if no row applies, record `NO_APPLICABLE_ROADMAP` with discovery evidence rather than silently skipping the gate.

The registry routes agents to strategy; it does not replace live repository/source/benchmark evidence.
