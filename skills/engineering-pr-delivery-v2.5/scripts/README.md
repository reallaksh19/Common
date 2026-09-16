# V2.5 validator commands

From the downstream repository root run the validators from this directory. Primary entrypoints:
```bash
python validate_relay_conformance.py <repo-root>
python cold_start_check.py <repo-root>
python render_handover.py <repo-root>
```
Focused validators cover REPO_STATE, roadmap graph, execution frontier, EP context independence, acceptance mapping, progress, serial/parallel policy, phase-transition Q1-Q5, checkpoints and Owner Decision Records.

PyYAML is required. Generated Markdown is a projection, not an authority source.