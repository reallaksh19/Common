# Grade 4 English Cold-Start Production Kit

This directory is the reference handoff for a new producing agent. It is intentionally structured like the stronger Grade 4 Mathematics V2 pipeline: pedagogy is selected before page composition, and missing evidence fails closed.

## Required pipeline

```text
SCAN / SOURCE
  -> SOURCE EXTRACTION
  -> PRESERVE SOURCE REFERENCES
  -> SEPARATE PRINTED CONTENT FROM HANDWRITING
  -> CREATE ANSWER CONTRACTS
  -> CLASSIFY TASK ARCHETYPES
  -> ATTACH SCAFFOLD PROFILES
  -> BUILD LEARNING REPRESENTATION
  -> VALIDATE
  -> COMPILE PAGE PLAN
  -> RENDER THROUGH SHARED GRADE 4 PUBLISHING
  -> RENDER EVERY PDF PAGE TO IMAGE
  -> VISUAL CHILD-USABILITY QA
  -> REGENERATE UNTIL PASS
```

Do **not** author a final PDF directly from the scan.

## Non-negotiable cold-start behavior

1. Preserve source page/section/question/box identity. Never silently renumber.
2. Store handwriting as observation; never promote it to answer authority.
3. Give every task an answer contract.
4. If source support is missing, use `SOURCE_UNRESOLVED`; do not guess.
5. Select pedagogy from structured task archetypes, not from raw prompt prose.
6. Teaching sequence and help sequence are separate.
7. Hints are on-demand by default.
8. Reading-to-organizer tasks use `SOURCE_STRIP -> EVIDENCE_HIGHLIGHT -> KEYWORD_CHIPS -> ANSWER_BUILDER`.
9. Strong support must lead to a fresh retry when the scaffold profile requires it.
10. Final PDF approval still requires rendered page-image inspection under the shared Grade 4 publishing contract.

## Cold-start acceptance

Give a new agent only the source images plus these contracts/profiles/examples. The agent passes only if an unseen task preserves source references, creates an answer contract, selects the correct scaffold, produces a valid learning representation/page plan, and does not invent unsupported answers.
