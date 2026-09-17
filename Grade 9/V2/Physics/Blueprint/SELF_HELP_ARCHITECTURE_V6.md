# Physics Self-Help Architecture V6 — reconstruction-complete TTUs

V6 strengthens the Technical Teaching Unit (TTU). V5 correctly rejected decorative or semantically weak diagrams, but a technically valid complete diagram could still count without forcing the learner to reconstruct the important structure.

A V6 TTU is therefore a **stateful teaching object** with two linked states:

```text
CANONICAL COMPLETED STATE
        ↕ exact element identity / bindings
LEARNER RECONSTRUCTION STATE
```

The TTU is authored once at the semantic level. A-layers may render the canonical state; B-layers render a deliberately incomplete reconstruction state. B-layers may not invent new omissions or semantics downstream.

## 1. What a TTU must contain

Every TTU v2 contains:

1. **AUTHORITY BINDING** — the semantic/source authority from which the TTU is derived;
2. **SEMANTIC TARGET** — capability, learning atoms, inferential jump and success claim;
3. **PHYSICAL SETUP** — objects, event, knowns, unknown, frame, sign/axes and model conditions;
4. **CANONICAL COMPLETED STATE** — complete domain representation, governing relations, element-to-relation bindings, intermediate working and final result;
5. **RECONSTRUCTION CONTRACT** — deliberately omitted domain elements, learner task, fixed help, reveal rule and anti-triviality checks;
6. **INDEPENDENT VERIFICATION** — a rule the learner can apply before seeing the canonical answer;
7. **LAYER REALIZATION** — whether the current Core renders the complete or reconstruction state;
8. **LAYOUT CONTRACT** — visible omission targets, separated help/reveal states and legible technical composition.

A diagram alone is not a TTU. An equation alone is not a TTU. A diagram plus an equation is not a TTU unless the learner-facing reconstruction and verification contracts are present where the layer requires them.

## 2. Deliberate omission is the key generative mechanism

For a reconstruction TTU, missing elements must be **physically meaningful**.

Examples in Physics:

- an omitted reference-frame label;
- a missing vector direction or resultant;
- a missing component projection;
- a missing force on a free-body diagram;
- a missing event marker on a timeline;
- a missing graph feature such as slope/sign/turning point;
- a missing equation term that corresponds to a visible physical quantity;
- a missing boundary/model condition;
- a missing intermediate state in a multi-step transformation.

The omission must target a real inferential step. It must change the learner's reasoning state.

These do **not** count:

- cosmetic blanks;
- hiding an arbitrary number with no conceptual role;
- removing a label that is never used in the reasoning;
- asking the learner to copy a visible answer;
- deleting the entire representation so no meaningful reconstruction anchor remains.

## 3. Canonical completed state is mandatory

Every reconstruction state is derived from an explicit canonical completed state.

The completed state contains stable element IDs. Every omission references those IDs. Every help step references the same IDs. Every representation-to-equation binding references the same IDs.

This prevents a B-layer from inventing a different diagram, equation interpretation or answer after Core1A/Core2A authoring.

## 4. Fixed help, not ad-hoc rescue

Help is preauthored and bounded.

For a substantive task, the default functions remain:

```text
H1 NOTICE
H2 REPRESENT
H3 START
```

Each hint must name the omitted element(s) it supports. Dynamic new Physics semantics may not be injected before the canonical reveal.

Micro reconstruction tasks may use fewer help steps when a full ladder would be redundant.

This preserves self-help without turning every prompt into a conversational tutoring transcript.

## 5. Independent verification must work before answer reveal

"Compare with the answer" is not verification.

A TTU needs at least one structural check the learner can apply to their own proposed state before seeing the canonical completion.

Allowed examples:

- inverse relation;
- substitution back into the governing relation;
- limiting case;
- dimensional or units check;
- sign/direction check;
- conservation law;
- graph behaviour;
- boundary condition;
- alternate representation;
- model-validity check.

For M2D-SBA-23, a strong verification is:

```text
proposed v_BG - v_TG  → should recover the given v_BT
```

A second check is the zero-source-speed limit.

## 6. Layer realization

### Core1A

Core1A normally renders the **canonical complete state** because it is declarative-dominant.

However the underlying TTU must already define the reconstruction contract so Core1B does not invent its own missing pieces later.

### Core1B

Core1B renders the **reconstruction state**.

The learner must reconstruct, select, label, derive or calculate the omitted meaningful structure before canonical reveal.

For a Hard substantive TTU, at least two meaningful omissions are expected, including at least one representation/model element when material.

### Core2A

Core2A renders a complete worked application TTU for a representative legal problem family. It may allow an initial attempt, but the expert state must be explicit.

### Core2B

Core2B renders a transfer reconstruction TTU using a fresh legal item where possible. The learner must select or reconstruct material model/representation structure rather than replay a Core2A worked state.

## 7. Research basis

V6 follows several established instructional findings:

- **Completion problems** are effective because learners receive a partial solution that they must understand and complete; they provide a bridge from worked examples toward independent problem solving.
- **Guidance fading** supports moving from more complete worked states toward more learner-generated states as expertise grows.
- **Generative learning** is useful when the learner selects, organizes or integrates meaningful information; merely drawing or filling arbitrary blanks is not enough.
- **Self-explanation prompts** are not automatically beneficial; redundant prompting can add unnecessary load, so help should target unresolved structure rather than repeat already-complete information.

The architecture therefore treats omission quality, bounded help and independent verification as part of the TTU itself.

## 8. Normative files

- `Blueprint/contracts/technical-teaching-unit-v2.schema.json`
- `Blueprint/policy/technical-teaching-unit.v2.json`
- `Blueprint/policy/self-help-core-publication.v6.json`
- `Blueprint/fixtures/technical-ttu-v2/m2d-moving-launcher-frame-conversion.json`
- `Blueprint/policy/physics-representation-semantic-quality.v1.json`
- `Blueprint/policy/pdf-layout-integrity.v2.json`

V6 supersedes V5 for TTU semantics. V5 remains useful history for the transition from figure-counting to semantic technical representations; V6 adds the missing reconstruction-state contract.
