# Chemistry LearningBlueprint v8 — Blueprint-only execution

## Rule

No Chemistry task may use model memory, conversational memory, or untraced general knowledge as content authority.

Every task begins with a serialized `blueprint-execution-packet-v8` containing the task type, product mode, required authority references, authority-source classes, and bindings for learner-facing technical objects.

If any required authority is absent, execution status is `BLOCKED`. The agent must not fill the gap from memory.

## Memory boundary

Conversation history may be used only to:

- locate a previously named Blueprint packet or repository reference;
- preserve an explicit owner instruction or choice;
- understand which authorized task the owner wants performed.

It may not establish Chemistry facts, equations, examples, questions, difficulty, representations, misconceptions, source identity, answers, or support decisions.

## Authority extension

When the current Blueprint is incomplete, the sequence is:

```text
MISSING AUTHORITY
→ BLOCK PRODUCT TASK
→ research / inspect source / request or consume owner input
→ update governed Blueprint authority
→ validate the new Blueprint packet
→ resume product task
```

Research does not bypass the Blueprint. It first becomes a governed Blueprint input with provenance.

## Output binding

Every learner-facing technical object must map to an authority reference before realization:

```text
output_id
+ object_class
+ authority_ref
```

This applies to concepts, learning atoms, equations, data, examples, representations, misconceptions, boundaries, questions, answers, solutions, TTUs, difficulty badges, and learner-support decisions.

An unbound technical object is a compilation failure.

## Required authorities by task

Core1A generation requires Canonical Domain Registry + CDAU + SDU + Concept TTU + CCBOM + Product Assurance.

Core1B adds Tutor Dialogue.

Core2A requires Canonical Domain Registry + CDAU + LAU + Problem TTU + Question Custody + CCBOM + Product Assurance.

Core2B additionally requires Tutor Dialogue.

Other tasks such as topic selection, audits, question/example/equation selection, difficulty, learner fit, TTU design, similarity audit, and release have their own task-specific requirements in `v8-blueprint-only-execution-policy.json`.

## Relationship to v7

v8 is an execution precondition. v7 still performs coverage, duplication, difficulty/purpose, learner-fit, question-custody, badge, and publication assurance.

A product cannot pass v7 by being well formed if it was authored from memory rather than governed authority.
