# Grade 9 Skill Family

This folder contains the reusable Grade 9 learning-production skill family derived from the repository's `Grade9schema.md` and the proven linked textbook/question-bank workflow.

## Skills

| Skill | Purpose |
|---|---|
| `grade9` | Router/orchestrator |
| `grade9-source-grounding` | Source extraction, QC, provenance, verification |
| `grade9-concept-architect` | Stable concept IDs, prerequisites, learning graph, links |
| `grade9-question-bank` | Core N, same-level calibration, Level-Up challenges, mixed tests |
| `grade9-learning-enrichment` | Helpers, hints, misconceptions, diagnostics, transfer |
| `grade9-textbook-publisher` | Kid-friendly linked textbook/question-bank PDF production and QA |
| `grade9-math` | Mathematics reasoning and difficulty profile |
| `grade9-physics` | Physics model/representation/validation profile |
| `grade9-chemistry` | Chemistry macro-particle-symbolic/evidence profile |

## Shared contracts

- `shared/grade9-workflow.md` — operational cross-skill workflow.
- `shared/grade9-master.schema.json` — canonical reusable master-data schema.
- Repository root `Grade9schema.md` — fuller human specification and implementation history.

## Deterministic checks

- `skills/grade9-question-bank/scripts/difficulty_check.py`
- `skills/grade9-question-bank/scripts/validate_bank.py`
- `skills/grade9-textbook-publisher/scripts/check_master_links.py`

## Recommended invocation

Start with `$grade9` for multi-stage work. Invoke a specialist directly for narrow tasks, for example:

```text
Use $grade9-question-bank to build 30 same-level questions from these anchors.
Use $grade9-physics to fingerprint these motion questions.
Use $grade9-textbook-publisher to publish this validated master JSON.
```

Each skill follows the Agent Skills folder structure with required `SKILL.md` and recommended `agents/openai.yaml` metadata.
