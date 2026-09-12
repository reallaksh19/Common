# Learning-representation regression fixtures

This directory freezes publisher-neutral learning-support cases for #338 / PR #339.

Current coverage:

- `MONEY_TWO_PART` — separate groups -> two cost branches -> combine;
- `REMAINDER_REPRESENTATIVE_SAMPLE` — honest representative sample with continuation marker;
- `LONG_DIVISION_7048_24` — estimate/multiples/first-step hints plus semantic long-division work surface;
- `ANGLE_DRAWING` — actual angle geometry plus learner drawing workspace;
- `SAME_RATE_HATS_120_240` — one linked scale factor must apply to both money and count;
- `DIVISION_TABLE_720_480` — row/column roles, one modeled cell, and a validated table workspace.

`build_learning_representation()` emits a publisher-complete `LearningRepresentationPlan` containing:

```text
primary_visual
all_visual_states
hint_visuals
resolved hint_ladder
resolved thinking_path
thinking_path_micro_visual_refs
resolved work_surface (when required)
stable refs
fresh_retry_support_policy
visual_language_key
publisher_invention_allowed = false
```

The publisher must consume these resolved objects. It must not reconstruct hint visuals,
procedural work surfaces, or child-facing reasoning steps from question text.
