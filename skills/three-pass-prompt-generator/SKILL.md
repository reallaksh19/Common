# Three-Pass Prompt Generator — Standalone Launcher

This skill exists only to generate the three sequential prompts defined by its canonical schema.

It is deliberately isolated from engineering-delivery, takeover, certification, qualification, execution-package, relay, and admission workflows.

## Canonical files

```text
LAUNCHER:
skills/three-pass-prompt-generator/SKILL.md

SCHEMA:
skills/three-pass-prompt-generator/schema.md

VALIDATOR:
skills/three-pass-prompt-generator/validate.py
```

## Entry rule — before target reasoning

When the user asks to create, regenerate, review, or apply three-pass prompts, including wording such as:

```text
3 pass
three-pass
Prompt 1 / Prompt 2 / Prompt 3
complex Q1 to Q5
complex Q1–Q5
```

execute this sequence exactly:

1. **Do not inspect the target issue/repository/product yet.**
2. Fetch `skills/three-pass-prompt-generator/schema.md` from current `main`.
3. Read the protocol revision from that live file.
4. Record the actual fetched blob/content SHA.
5. Only if the live fetch succeeded, enter `GENERATOR MODE = THREE_PASS_ONLY`.
6. The generated artifact must start with the schema's required `# SCHEMA EXECUTION HANDSHAKE`.
7. Only after the handshake basis is established may you inspect the user-named target and supporting evidence.
8. Generate exactly the artifact required by the live schema.
9. Validate the artifact with `skills/three-pass-prompt-generator/validate.py` using the fetched schema SHA when executable validation is available.
10. Return the schema-defined artifact and **STOP**.

## Isolation rule

For this task, do **not** load or apply:

```text
skills/engineering-pr-delivery-v2.5/SKILL.md
skills/engineering-pr-delivery-v2.5/operating-model/**
skills/engineering-pr-delivery-v2.5/templates/**
skills/engineering-pr-delivery-v2.5/schemas/**
```

except when the user explicitly asks to combine protocols.

Those files govern a different engineering-delivery workflow.

They are not supplementary instructions for three-pass prompt generation.

Repository and issue files for the **user's target** may of course be inspected after the schema handshake because they are evidence, not generator-control instructions.

## Complex Q1–Q5

When the user requests complex Q1–Q5, those are the five human reasoning lenses defined by the live standalone schema.

They remain inside Prompt 1.

Do not create any additional question package, qualification gate, admission gate, evaluator step, route metadata, execution-package fields, or fourth stage.

If visible Q1–Q5 headings are requested, write them in natural target-specific practitioner language.

## Fail closed

If the canonical schema cannot be fetched from current `main`, do not reconstruct it from memory, prior chat context, another skill, or an older revision.

Return only the schema handshake failure required by the schema and stop.

If an output begins with target analysis or Prompt 1 before proving the live schema handshake, that run is invalid.
