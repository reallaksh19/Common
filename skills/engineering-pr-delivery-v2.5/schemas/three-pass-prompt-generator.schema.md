# Three-Pass Prompt Generator — Legacy Compatibility Redirect

**Do not generate prompts from this file.**

The three-pass generator has moved out of the engineering-delivery skill so that prompt generation cannot inherit takeover / qualification / relay instructions.

Canonical launcher:

https://github.com/reallaksh19/Common/blob/main/skills/three-pass-prompt-generator/SKILL.md

Canonical schema:

https://github.com/reallaksh19/Common/blob/main/skills/three-pass-prompt-generator/schema.md

Canonical validator:

```text
skills/three-pass-prompt-generator/validate.py
```

Current protocol family:

```text
GENERATOR MODE:
THREE_PASS_ONLY
```

If a user points to this legacy URL:

1. **Do not inspect the target yet.**
2. Fetch the canonical launcher from current `main`.
3. Fetch the canonical schema from current `main`.
4. Use the protocol revision and actual schema SHA from that live fetch.
5. Begin the generated artifact with the canonical schema's execution handshake.
6. Follow only the standalone three-pass generator protocol.
7. After Prompt 3, stop.

Do not load the surrounding `engineering-pr-delivery-v2.5` skill as supplementary instructions for this request.

If the canonical launcher/schema cannot be fetched, fail closed using the canonical schema handshake failure form. Do not reconstruct the generator from memory.
