# Grade 9 ChatGPT Skills

ChatGPT-ready conversion of the existing Grade 9 Agent Skills family.

## Skills

1. `grade9` — umbrella/orchestrator
2. `grade9-source-grounding`
3. `grade9-concept-architect`
4. `grade9-question-bank`
5. `grade9-learning-enrichment`
6. `grade9-textbook-publisher`
7. `grade9-math`
8. `grade9-physics`
9. `grade9-chemistry`

## Design decisions

- The existing Grade 9 master schema is unchanged.
- Relative sibling-file references were removed so each ChatGPT Skill can be installed independently.
- Cross-skill coordination uses skill names rather than filesystem paths.
- Existing difficulty thresholds and page-density percentage remain only as local engineering heuristics.
- Full builds are expected to use the umbrella skill plus relevant specialists.
- Specialist skills remain useful independently for narrow tasks.

## Installation

Upload each skill folder/package as one ChatGPT Skill. Install all nine for the complete workflow.

Typical explicit uses:

- `@grade9` — full multi-stage workflow
- `@grade9-source-grounding` — source/QC only
- `@grade9-question-bank` — same-level/challenge bank
- `@grade9-math`, `@grade9-physics`, `@grade9-chemistry` — subject reasoning
- `@grade9-textbook-publisher` — publication

The ChatGPT conversion is intentionally separate from `Grade 9/skills/` so the existing operational/Codex-oriented skill family remains unchanged.
