# Grade 9 ChatGPT Skills

ChatGPT-ready conversion of the Grade 9 Agent Skills family.

Current package version: **1.1.0**

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

## v1.1.0 Physics concept-book update

This version adds the reusable Physics Concept Book methodology:

`SEE THE EQUATION -> REALIZE -> UNDERSTAND`

with source traceability through `CONNECT`.

It also adds:

- SRU-01..SRU-15 concept-book authoring/QA gates;
- Grade 9 depth protection against stopping at elementary intuition;
- symbolic derivation, model-validity, sign, dimensional, graph and scaling requirements;
- a Motion in a Straight Line worked exemplar;
- equation/font/glyph publication QA;
- umbrella routing from `grade9` to `grade9-physics` for Physics Concept Books.

## Design decisions

- The existing Grade 9 master schema is unchanged.
- Relative sibling-skill filesystem references are avoided so each ChatGPT Skill can be installed independently.
- References inside an individual skill package are allowed and travel with that skill.
- Cross-skill coordination uses skill names rather than filesystem paths.
- Existing difficulty thresholds and page-density percentage remain only as local engineering heuristics.
- Full builds are expected to use the umbrella skill plus relevant specialists.
- Specialist skills remain useful independently for narrow tasks.

## Installation / refresh

Upload each skill folder/package as one ChatGPT Skill.

For an existing **v1.0.0** installation, only these skills changed in v1.1.0 and need to be refreshed:

- `grade9`
- `grade9-physics`

The other seven skills are unchanged.

For a fresh full installation, install all nine skills.

Typical explicit uses:

- `@grade9` — full multi-stage workflow
- `@grade9-source-grounding` — source/QC only
- `@grade9-question-bank` — same-level/challenge bank
- `@grade9-math`, `@grade9-physics`, `@grade9-chemistry` — subject reasoning
- `@grade9-physics` — Physics Concept Book mode using SEE -> REALIZE -> UNDERSTAND
- `@grade9-textbook-publisher` — publication

The ChatGPT conversion is intentionally separate from `Grade 9/skills/` so the operational/Codex-oriented skill family remains independently maintainable.
