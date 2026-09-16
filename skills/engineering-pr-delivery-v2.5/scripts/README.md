# V2.5 validator commands

From the downstream repository root run the validators from this directory. Primary entrypoints:

```bash
python validate_relay_conformance.py <repo-root>
python cold_start_check.py <repo-root>
python stress_test_relay.py <repo-root> [<repo-root> ...]
python render_handover.py <repo-root>
```

Aggregate relay conformance verifies repository routing, roadmap topology/frontier, self-contained EPs, acceptance mapping, EP staleness, report contract, calculated progress, execution policy, independent status planes, last-checkpoint → active-EP baton linkage, phase-transition Q1-Q5, issue graph/closure/supersession, and roadmap transactions.

Focused validators remain independently callable for diagnosis. `stress_test_relay.py` is read-only and repository-agnostic; real repositories are validation targets only.

PyYAML is required. Generated Markdown is a projection, not an authority source.