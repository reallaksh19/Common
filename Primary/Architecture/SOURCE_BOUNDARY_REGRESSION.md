# Primary source-boundary regression

This regression fixture exists because Grade 4 sources often teach simplified classifications that do not cover every natural-language case.

## Canonical failure to prevent

Source rule:

```text
number → opinion → size → age → shape → colour → origin → material → purpose
```

Test phrases include words such as:

```text
large / heavy / brown / leather
colourful / Afghan / woollen / handmade
cheerful / bright / new / classroom
broken / old / metal / cooking
```

## Forbidden behaviour

The tutor must not silently introduce a new source category such as:

```text
quality
condition
physical quality
quality/type
```

and then present that category as though it belonged to the workbook rule.

It must also not switch classifications across turns without explicitly correcting and stabilizing the model.

## Required behaviour

1. Preserve the source rule exactly as the taught model.
2. Classify words that clearly fit the source taxonomy using child-friendly recognition cues.
3. When a word does not fit cleanly, record `SOURCE_BOUNDARY` or `AMBIGUOUS` rather than inventing source truth.
4. Keep fuller canonical linguistic analysis separate from the source-facing explanation.
5. After answering a clarification, give a tiny transfer check when in tutor mode.

Example:

```text
Child: "Large?"

Tutor:
"Yes. Large tells us how big something is, so it goes in SIZE. What about tiny: size, age, or colour?"
```

For a boundary case:

```text
"Heavy is a describing word, but our book's short chart does not give this kind of word its own box. We will keep the book's rule as it is instead of inventing a new box."
```

## Pass conditions

```text
SOURCE_RULE_PRESERVED = PASS
NO_SILENT_CATEGORY_INVENTION = PASS
CROSS_TURN_RULE_STABILITY = PASS
CHILD_FRIENDLY_RECOGNITION_CUE = PASS
BOUNDARY_CASE_EXPLICIT = PASS
TINY_TRANSFER_CHECK = PASS
```

This fixture should be consumed by the Grade 4 English skill/runtime tests before the English vertical slice is considered complete.