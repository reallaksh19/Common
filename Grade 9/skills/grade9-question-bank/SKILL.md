---
name: grade9-question-bank
description: Create and validate Grade 9 question banks that preserve the cognitive difficulty of uploaded anchor questions, including user-specified Core N banks, same-level calibrated originals, HOTS/competitive-foundation variants, next-level challenge appendices, and mixed mastery tests. Use when the user asks for similar questions, a question bank, same difficulty, harder questions, practice sets, or difficulty-controlled assessments.
---

# Grade 9 Question Bank

Build a compact, high-quality bank rather than many superficial variants.

## Defaults

- Core question count: `30` only if the user does not specify a count.
- Challenge question count: `20` only if the user does not specify a count.
- When 20 usable anchors and Core 30 are requested, prefer `20 anchors + 10 calibrated originals`.
- If anchors are unusable because of unresolved source QC, retain them in provenance but replace them in the scored bank with validated calibrated items.

## Difficulty model

Treat difficulty as a vector. For Mathematics, the generic baseline is:

```json
{
  "conceptual": 0,
  "recognition": 0,
  "reasoning_steps": 0,
  "algebra": 0,
  "hidden_structure": 0,
  "constraints_cases": 0,
  "calculation_burden": 0,
  "trap_density": 0
}
```

Subject skills may replace or extend these dimensions.

For the generic Math-like composite, use:

`D = 0.25C + 0.25R + 0.15S + 0.15A + 0.10H + 0.10K`

Use the scalar only as a screening aid. Reject a candidate when its cognitive profile differs materially from the anchor even if the overall score is similar.

## Same-level acceptance

As a default screening window:

`anchor_score - 0.4 <= candidate_score <= anchor_score + 0.4`

Also require comparable reasoning mechanism, recognition load, and expert solution-path depth.

## Next-level challenge target

Target approximately:

`anchor_score + 0.8 to anchor_score + 1.3`

Increase difficulty by deeper synthesis, less obvious representation, an additional inference, interacting constraints, or a richer target. Do not make a challenge hard mainly through ugly arithmetic or excessive expansion.

## Candidate relationships

Classify candidates as:

- `NEAR_TWIN` — same mathematical/scientific engine, changed surface.
- `STRUCTURAL_ANALOGUE` — same core reasoning with different representation/context.
- `CONCEPT_REINFORCEMENT` — same concept, usually more explicit.
- `ADVANCED_TRANSFER` — same lineage plus an added inference/bridge.

When new-question capacity is limited, allocate extra practice to concepts with high recognition load, transfer value, or thin source coverage. Do not distribute mechanically.

## Mixed mastery

Concept-grouped practice teaches method recognition but can leak the intended method. Reuse validated Core questions in mixed tests that hide concept labels before the attempt. After marking, map each error back to an exact concept and recommended retake.

## Question object minimum

```json
{
  "id": "C21",
  "provenance_class": "ORIGINAL_CALIBRATED",
  "primary_concept_id": "SEQ-C01",
  "secondary_concept_ids": [],
  "anchor_ids": ["Q01"],
  "difficulty": {},
  "relationship": "STRUCTURAL_ANALOGUE",
  "question": "...",
  "answer": "...",
  "solution_path": [],
  "verified": true
}
```

## Validation

Run `scripts/difficulty_check.py` when anchor/candidate vectors are available. Run `scripts/validate_bank.py` on master JSON before publication.

Do not pass the bank downstream until counts, IDs, answers, concept links, provenance, and difficulty status are valid.
