# Hint prompt/reveal schema

Each learner hint is a semantic pair, not two independent strings.

```yaml
hint:
  rung: H1 | H2 | H3
  prompt:
    context_anchor: "minimum problem context required to understand this hint in isolation"
    open_question: "question requiring the learner to retrieve/construct a concept"
  reveal:
    concept_clarifier: "direct answer to that prompt only"
    representation: "optional diagram/components/frame/geometry"
    equation: "optional relation belonging to this rung"
  forbidden:
    - later_rung_information
    - final_requested_result
```

## H1

Prompt asks for decisive physics: event, invariant, state, direction, observer/frame, or constraint. Reveal states that physical meaning only.

## H2

Prompt asks how to represent the physics. Reveal gives the matching diagram/components/axes/frame/geometry and governing relation. It must answer H2's question directly.

## H3

Prompt asks what the learner would write first. Reveal gives one executable starting equation/constraint/construction and stops before solving it.

## Validation failures

- `HINT_PROMPT_NOT_OPEN_ENDED`
- `HINT_REVEAL_NOT_SELF_CONTAINED`
- `HINT_PROMPT_REVEAL_MISMATCH`
- `HINT_REVEAL_LEAKS_LATER_RUNG`
- `HINT_REVEAL_RESOLVES_FINAL_ANSWER`

The generated Revised Core 2 v2 audit reports zero prompt/reveal validation failures across Q1-Q59.
