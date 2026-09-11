# Physics V2 — Instructional Knowledge / PCK Candidates (P-G)

Tracking: #255. This layer turns Physics problem semantics and the P-F learner-study contract into **reviewable teaching knowledge**, without allowing an AI-authored draft to silently become producer authority.

## Authority boundary

`registry/physics_pck_candidates.py` deterministically materializes 18 Physics-specific candidate PCK assets covering the full current P-C capability authority and the 17 pilot topics named in #255. Every asset carries physical anchors, system/frame setup, representation paths, ordinary-language bridges, model-validity cues, relation reconstruction, minimal contrasts, misconception repair, verification, fading, transfer, limitations, provenance and review state.

All current assets are:

```text
lifecycle_status = CANDIDATE
review.status = PENDING_HUMAN_REVIEW
authoring_origin = AI_ASSISTED_DRAFT
```

The promotion registry is intentionally empty. P-G does **not** invent human review evidence. Production Core1 authoring therefore fails closed with `PCK_PROMOTION_REQUIRED` until explicit SUBJECT and PEDAGOGY approval is recorded.

## Physics teaching contract

Candidate assets implement the established Grade-9 Physics semantics:

```text
SEE THE EQUATION
→ REALIZE what every term means physically
→ UNDERSTAND origin, assumptions, representation, scaling and limits
→ CONNECT to source and transfer families
```

They also preserve:

```text
physical situation
→ system
→ frame/sign
→ representation
→ decisive feature
→ ordinary-language bridge
→ model-validity gate
→ reconstruction
→ contrast/repair
→ verification
→ transfer
```

No candidate asset owns learner treatment. P-F remains the authority for `READY_VERIFY_ONLY`, `ACTIVE_STUDY`, `REPAIR_BEFORE`, `REPAIR_IN_UNIT` and `PROBE_FIRST`.
