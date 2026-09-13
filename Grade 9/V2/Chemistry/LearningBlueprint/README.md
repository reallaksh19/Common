# Grade 9 V2 Chemistry — Learning Blueprint

This directory is the **Chemistry-specific** evidence, control and pedagogical-reasoning layer above the existing Chemistry Core1/Core2/Core1A/Core2A production system. It is intentionally located under `Grade 9/V2/Chemistry/`: the current contracts and goldens have only been proven against Chemistry. Reuse by Physics or Mathematics requires separate subject validation rather than an assumed cross-subject claim.

The blueprint does **not** contain Chemistry answers. Original evidence remains authority; generated packets remain claims with explicit provenance, confidence and unresolved-state custody.

## v0 — evidence and adaptive routing

`v0` freezes the supplied evidence state and chooses `CORE1_FIRST`, `CORE2_FIRST`, or a blocking state from `SA / SS / QE / QR / UA / CI`. Missing evidence stays missing; zero supplied questions never becomes zero importance; owner overrides change execution without erasing the system finding; handoffs are limited to at most three subtopics without limiting later learning-atom decomposition.

## v1 — independent Core1/Core2 intelligence and Join

`v1` enforces the epistemic relay:

```text
v0 route
  ↓
first specialist: original evidence only
  ↓ freeze
fresh second specialist: original evidence only
  ↓ freeze
only then reveal first packet
  ↓
claim-level V-* comparison
  ↓
Core1 × Core2 Join
  ↓
J-* + OBL-* assimilation obligations
```

The second specialist may not receive upstream packets during its blind pass, may not reuse the first instance ID, and must compare every upstream claim after reveal. Material contradiction and assessment demand without semantic support block the Join.

## v2 — learner state, purpose and Core1A assimilation compiler

`v2` starts only from `J.join_state = READY_FOR_LEARNER_STATE`.

```text
J-* obligations
   ├─ learner readiness prior 20 / 50 / 80
   │        ↓
   │      LS-* capability state
   │
   └─ FIRST_STUDY / REVISION / COMPETITIVE_EXAM
            ↓
          PUR-*
            ↓
CT → LA → IC → EA → RR → RC → RD → MC → SB → FP
            ↓
          A-* assimilation bundle
            ↓
     manuscript_ready = true
     only after all validators pass
            ↓
optional realized-product evidence
            ↓
          T-* taught-state receipt
```

The readiness percentage is a **prior only**. If no capability-level evidence exists, the compiled learner state remains `UNKNOWN`; the system does not fabricate a diagnosis from `20`, `50`, or `80`.

Core1A reasoning is materialized before prose authoring:

- `CT-*`: learner-before → required conceptual change → learner-after;
- `LA-*`: learning atoms, with no three-atom cap;
- `IC-*`: explicit inferential steps and readiness-sensitive bridges;
- `EA-*`: important-equation anatomy, including assumptions, justified derivation, meaning, checks and validity limits;
- `RR/RC/RD-*`: cognitive representation requirement, candidate competition and justified selection;
- `MC-*`: misconception/boundary contrast;
- `SB-*`: picture → words → symbols → equation bridge when required;
- `FP-*`: worked → faded → independent practice with an independent check;
- `A-*`: validated assimilation plan;
- `T-*`: evidence-backed taught-state receipt. A plan alone cannot claim that a capability was actually taught or independently checked.

Purpose changes the terminal learning contract but may never bypass prerequisite closure. `FIRST_STUDY`, `REVISION`, and `COMPETITIVE_EXAM` therefore produce different assimilation/fading behaviour while preserving the same semantic truth.

## v3 — Core2A transfer eligibility compiler

`v3` does **not** generate a challenge merely because a question family is available. It first computes an explicit four-way eligibility intersection:

```text
K = validated semantic scope from A-*
D = explicit Core2 transfer envelope
T = evidence-backed taught state from T-*
P = purpose profile

eligible Core2A candidate = K ∩ D ∩ T ∩ P
                              ↓
                            X-*
```

Every candidate receives four machine-readable booleans:

- `validated_semantic_scope`;
- `transfer_envelope`;
- `taught_state`;
- `purpose`.

Only a candidate for which all four are true is emitted in `eligible_item_ids`. A blocked candidate remains in the decision ledger with reason codes but cannot enter the downstream release list.

The transfer envelope may **narrow** validated semantic scope but may never expand it. A purpose profile may narrow novelty, support mode, or capability-combination width, but may not re-authorize untaught or semantically unsupported content. Any declared `new_semantic_claims` blocks transfer.

Current purpose policy is deliberately asymmetric:

- `FIRST_STUDY`: at most one capability per candidate; `SAME_STRUCTURE` or `NEAR_TRANSFER`; hinted transfer may begin after evidence of `taught + represented + worked`, while independent transfer requires the full `faded + independent + checked` closure;
- `REVISION`: independent transfer only; at most two capabilities; up to `INTERLEAVED_TRANSFER`; full taught-state closure required;
- `COMPETITIVE_EXAM`: independent transfer only; at most three already-authorized capabilities; up to `EXTENDED_WITHIN_SCOPE`; full taught-state closure required.

`EXTENDED_WITHIN_SCOPE` means harder recombination or less familiar surface form **without adding new chemistry semantics**. It is not permission to import higher-grade content.

## Entry points

```bash
python 'Grade 9/V2/Chemistry/LearningBlueprint/engine/run_blueprint_v0.py' ...
python 'Grade 9/V2/Chemistry/LearningBlueprint/engine/run_blueprint_v1.py' ...
python 'Grade 9/V2/Chemistry/LearningBlueprint/engine/run_blueprint_v2.py' \
  --join build/v1/join.json \
  --learner learner.json \
  --purpose purpose.json \
  --design assimilation-design.json \
  --out-dir build/v2

python 'Grade 9/V2/Chemistry/LearningBlueprint/engine/run_blueprint_v3.py' \
  --assimilation build/v2/assimilation.json \
  --taught build/v2/taught_state.json \
  --envelope transfer-envelope.json \
  --request transfer-request.json \
  --out-dir build/v3
```

Add `--realization realization-evidence.json` to v2 only after learner-facing realization exists and there is evidence for the taught-state flags. v3 intentionally requires a `T-*` receipt; it cannot infer taught state from the assimilation plan.

## Not yet claimed

v3 is an **eligibility compiler**, not yet the final one-command Chemistry product generator. The next milestone is to bind `X-*` release custody into the existing Chemistry Core2A challenge builder and ProductionKit, then drive Core1/Core2/Core1A/Core2A render, visual preflight, answer closure and final audit from the same blueprint authority. Human subject, pedagogy, assessment and visual-usability gates remain separate from machine completion.
