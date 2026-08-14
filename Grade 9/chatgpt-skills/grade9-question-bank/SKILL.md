---
name: grade9-question-bank
description: Create and validate Grade 9 question banks that preserve the cognitive demand of source anchors, including Core N banks, same-level calibrated originals, HOTS/competitive-foundation practice, next-level challenges, and mixed mastery tests. Use for similar questions, same-difficulty practice, harder questions, practice sets, or controlled assessments.
---

# Grade 9 Question Bank

Build fewer high-quality questions rather than many superficial numerical variants.

Core default = 30 and challenge default = 20 only when the user gives no count. With 20 usable anchors and Core 30, `20 anchors + 10 calibrated originals` is a useful pattern, not a mandatory law. Unresolved anchors remain in provenance but must not stay scored.

For Mathematics, current difficulty dimensions are `conceptual`, `recognition`, `reasoning_steps`, `algebra`, `hidden_structure`, `constraints_cases`, `calculation_burden`, `trap_density`; subject skills may replace/extend them.

Current scalar screen: `D = 0.25C + 0.25R + 0.15S + 0.15A + 0.10H + 0.10K`.

Current same-level screen: `anchor ±0.4`. Current challenge screen: approximately `anchor +0.8 to +1.3`. These are local engineering heuristics, not psychometric calibration. A scalar pass is never sufficient; require comparable conceptual lineage, mechanism, recognition, representation demand, constraints, and solution-path depth. Challenges should increase synthesis rather than arithmetic clutter.

Relationship classes: `NEAR_TWIN`, `STRUCTURAL_ANALOGUE`, `CONCEPT_REINFORCEMENT`, `ADVANCED_TRANSFER`.

Allocate extra practice by learning need, recognition demand, transfer value, misconceptions, prerequisite importance, and weak coverage—not mechanically.

Concept-grouped learning may expose labels. Mixed mastery should hide labels before attempt, then diagnose errors back to exact concepts.

When code execution is available, `scripts/difficulty_check.py` can screen scalar deltas and `scripts/validate_bank.py` can validate master-data invariants. Their output never replaces expert review.
