# Grade 9 ChatGPT Skills

ChatGPT-ready conversion of the Grade 9 Agent Skills family.

Current package version: **1.2.0**

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

## v1.2.0 Mathematics concept-book update

This version adds the reusable Mathematics Concept Book methodology:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

with `CONNECT` retained as source traceability/navigation.

It adds:

- MSRU-01..MSRU-15 Mathematics concept-book authoring/QA gates;
- pattern -> invariant -> structure -> transfer learning architecture;
- explicit representation switching and contrast teaching;
- summation taught as repeated addition before sigma manipulation;
- a Sequence & Series worked exemplar with power-sum/hidden-series/JEE bridge guidance;
- umbrella routing from `grade9` to `grade9-math` for Mathematics Concept Books.

## v1.1.0 Physics concept-book update

Physics Concept Book mode remains:

`SEE THE EQUATION -> REALIZE -> UNDERSTAND`

with source traceability through `CONNECT`, SRU-01..SRU-15 gates, and the Motion worked exemplar.

## Design decisions

- The existing Grade 9 master schema is unchanged.
- Relative sibling-skill filesystem references are avoided so each ChatGPT Skill can be installed independently.
- References inside an individual skill package are allowed and travel with that skill.
- Cross-skill coordination uses skill names rather than filesystem paths.
- Existing difficulty thresholds and page-density percentage remain local engineering heuristics.
- Full builds are expected to use the umbrella skill plus relevant specialists.

## Installation / refresh

Upload each skill folder/package as one ChatGPT Skill.

For an existing **v1.1.0** installation, refresh:

- `grade9`
- `grade9-math`

The Physics v1.1.0 additions remain unchanged.

For a fresh full installation, install all nine skills.

Typical explicit uses:

- `@grade9` — full multi-stage workflow
- `@grade9-source-grounding` — source/QC only
- `@grade9-question-bank` — same-level/challenge bank
- `@grade9-math` — Mathematics reasoning or Concept Book mode using SEE -> REALIZE -> UNDERSTAND -> ADOPT
- `@grade9-physics` — Physics Concept Book mode using SEE -> REALIZE -> UNDERSTAND
- `@grade9-textbook-publisher` — publication

The ChatGPT conversion is intentionally separate from `Grade 9/skills/` so the operational/Codex-oriented skill family remains independently maintainable.
