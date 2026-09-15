# Study Synthesis methodology

## 1. Preserve obligations before adaptation

Start from `CanonicalTargetScope`. Learner state can change treatment of an obligation, not erase the requested target.

## 2. Consume, do not recreate, diagnosis

Use `ResearchLearnerView` capability states and reason references. Raw attempts, psychological causes, and new diagnostic inference are outside this authority.

## 3. Select engagement and readiness independently

Engagement answers how much active study a target needs:

- `VERIFY_ONLY`: demonstrated and only confirmation is needed.
- `COMPRESS`: demonstrated, but concise consolidation is still required by policy/goal.
- `USE_AS_ENTRY_POINT`: demonstrated capability is intentionally preserved and used to connect into a downstream repair target.
- `ACTIVE_STUDY`: target needs substantive learner work.

Readiness answers whether a blocker/probe must precede or accompany target work:

- `READY`
- `REPAIR_BEFORE`
- `REPAIR_IN_UNIT`
- `PROBE_FIRST`

These are study decisions, not lesson sequence.

## 4. Bind every material obligation twice when learner-conditioned

A learner-conditioned obligation requires:

```text
canonical_refs[]                why the subject obligation is true
learner_state_reason_refs[]     why this learner needs this treatment
policy_version                  why this decision rule was selected
```

Canonical-only obligations may omit learner reason refs only when they are genuinely unconditional for the target.

## 5. Missing truth fails upstream

If a needed bridge, representation meaning, misconception contrast, verification rule, or transfer condition lacks a canonical binding, return `CANONICAL_KNOWLEDGE_GAP`. Never author subject truth inside Study Synthesis.

## 6. Preserve successful upstream capability

A downstream failure cannot rewrite a demonstrated upstream target to weak. A demonstrated dependency may be `USE_AS_ENTRY_POINT` while its downstream target is `REPAIR_BEFORE`.

## 7. Ambiguity stays ambiguous

`PROBE_REQUIRED`, `AMBIGUOUS`, or `UNKNOWN` cannot become a confirmed misconception or `REPAIR_REQUIRED` inside Study Synthesis. Use `PROBE_FIRST`.

## 8. Stop before choreography

A complete StudyModel says what must be learned, reconstructed, contrasted, verified, transferred, and evidenced. V2-05 decides explanation order, examples, hints, fading, guided/independent choreography, practice realization, and interaction support.
