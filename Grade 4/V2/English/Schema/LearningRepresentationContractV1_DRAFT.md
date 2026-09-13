# Grade 4 English Learning Representation Contract V1

This is the executable handoff between extraction and page composition.

```yaml
learning_representation:
  schema_version: "1.0.0"
  task_id: ...
  task_archetype: ...
  scaffold_profile: ...
  source_reference: ...
  answer: ...
  preteach: []
  model: []
  guided: []
  independent_try: ...
  help:
    reveal_mode: ON_DEMAND
    steps: []
  fresh_retry: ...
  components: []
  evidence: ...
  render_constraints: ...
```

## Invariants

1. `task_archetype` is explicit or resolved from structured signature fields. Never infer pedagogy from raw prompt prose.
2. The scaffold profile comes from the production kit.
3. Teaching sequence and help sequence are separate.
4. Help defaults to `ON_DEMAND`; showing all hints before an attempt is invalid unless the page is explicitly a teacher/parent reference surface.
5. Every source task carries a stable `source_reference`.
6. Every task carries an answer contract.
7. Reading source-evidence tasks carry source lines and evidence spans.
8. Source-unresolved tasks cannot render an asserted answer.
9. A fresh retry is required when the scaffold profile requires one.
10. Page components come from the English component library rather than being invented ad hoc by each agent.
