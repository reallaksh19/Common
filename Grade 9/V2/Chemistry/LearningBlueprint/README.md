# Grade 9 V2 Chemistry — Learning Blueprint

This directory is the **Chemistry-specific** evidence, control and pedagogical-reasoning layer above the existing Chemistry Core1/Core2/Core1A/Core2A production system. It is intentionally located under `Grade 9/V2/Chemistry/`: the current contracts and goldens have only been proven against Chemistry. Reuse by Physics or Mathematics requires separate subject validation rather than an assumed cross-subject claim.

The blueprint does **not** contain Chemistry answers. Original evidence remains authority; generated packets remain claims with explicit provenance, confidence and unresolved-state custody.

---

## Chemistry Technical Engineering Gate Registry (Upstream of Authored TTUs)

Normative specification: `CHEMISTRY_TECHNICAL_ENGINEERING_GATES.md`.  
Schema contract: `contracts/chemistry-technical-engineering-gate.schema.json`.  
Canonical policy & registry: `policies/chemistry-technical-engineering-gates.v1.json`.  
Deterministic validator: `engine/validate_chemistry_engineering_gates.py`.  
Test suite & falsifiers: `tests/test_chemistry_engineering_gates.py`.

At the **CANONICAL DOMAIN REGISTRY** boundary (upstream of CCU, CDAU, and authored TTUs), technical readiness requires fail-closed engineering validation across 10 granular, technically coherent Chemistry subtopics:
- `CHEM-SYM-LITERACY`: Chemical symbols, atomic notation ($^A_Z X$), elemental diatomic molecules ($H_2, O_2, N_2, Cl_2$), subscripts vs coefficients.
- `CHEM-ION-VALENCY`: Monoatomic ions, polyatomic radicals ($SO_4^{2-}, CO_3^{2-}, NH_4^+$), bracket enclosure rules, formal charges.
- `CHEM-FORMULA-CONSTRUCTION`: Electroneutrality constraint ($\sum q_i = 0$), criss-cross valency algorithm, prohibition of unneutralized ionic formulas ($MgCl$, $NaSO_4$).
- `CHEM-EQ-BALANCING`: Conservation of mass, atom conservation per element, coefficient-only balancing (subscript mutation strictly prohibited).
- `CHEM-STATE-SYMBOLS`: Physical state symbols $(s), (l), (g), (aq)$, strict distinction between pure liquid $(l)$ and aqueous solution $(aq)$, precipitation $(\downarrow)$ and gas $(\uparrow)$ indicators.
- `CHEM-REACTION-CONDITIONS`: Reaction arrow semantics (reversibility $\rightleftharpoons$ vs completion $\to$), catalytic/temperature/pressure conditions, thermochemical signs ($\Delta H < 0$ vs $\Delta H > 0$).
- `CHEM-REP-TRANSLATION`: Johnstone's Triplet (Macroscopic observation $\leftrightarrow$ Particulate sub-microscopic model $\leftrightarrow$ Symbolic equation), prohibition of macroscopic property projection onto single particles.
- `CHEM-CALC-STOICHIOMETRY`: Quantitative mole interconversions ($n = m/M$), molar ratios from coefficients (mass-ratio fallacy prevention), limiting reagent derivation.
- `CHEM-ACID-BASE-IONS`: Arrhenius ionization in aqueous media, hydronium/hydroxide generation, moisture requirement for acidity, net ionic neutralization ($H^+ + OH^- \to H_2O$).
- `CHEM-REDOX-OXIDATION`: Electron conservation, oxidation state assignment rules, agent role inversion (oxidizing agent is the species reduced).

All subtopics enforce `maturity: ENGINEERING` and are verified by an automated 12-mutation production validator falsification battery.

---

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

## v4 — Core1 bucket depth and Core2 learner conditioning

`v4` separates two control systems that must not be conflated.

### Core1A / Core1B — intrinsic-difficulty bucket control

Core1A and Core1B are always realized **subtopic bucket by subtopic bucket**. A bucket is the smallest coherent teaching unit selected for learner realization. A difficult bucket may be decomposed further into sub-subtopics when research shows that the concept contains distinct cognitive jobs.

```text
validated Chemistry knowledge
        ↓
subtopic bucket
        ↓
intrinsic difficulty badge
EASY / MEDIUM / HARD
        ↓
shared bucket authority
   ┌───────────────┴───────────────┐
   │                               │
Core1A                         Core1B
exposition-first              elicitation-first
```

The difficulty badge is **intrinsic to the subtopic**. It is not learner readiness, learner mastery, learner knowledge percentage, exam purpose or owner preference.

The normal page envelopes are ceilings, not quotas:

- `EASY`: up to 10 pages; visuals/steps/diagrams required as needed; web research optional by default;
- `MEDIUM`: up to 20 pages; web research required before realization;
- `HARD`: up to 30 pages; deep web research required, including representation/misconception questions; sub-subtopic decomposition is permitted whenever the research indicates that one bucket would otherwise hide distinct learning structures.

More difficult does **not** mean more decorative images. Every visual must perform a named reasoning job such as phenomenon view, particle/species model, symbolic model, quantity model, comparison, causal sequence, boundary contrast, error visual or representation bridge.

Core1A and Core1B consume the same bucket authority:

```text
same capability set
same learning atoms
same prerequisites
same representations
same misconceptions
same validity boundaries
same intrinsic difficulty badge
same research package
```

Only learner realization differs. Core1A explains; Core1B elicits reconstruction. A Core1 bucket contract rejects learner-knowledge fields so knowledge percentage cannot silently change Chemistry depth or page budget.

### Core2A / Core2B — learner-conditioning control

Core2 support requires a resolved learner condition before compilation.

The default route is:

```text
knowledge_percent = 0..100
```

This is a **support prior**, not a mastery score. It controls scaffold density, hint depth, representation support, first-move support and solution delay. It does not change frozen question identity, source provenance, validated semantic scope or legal answer authority.

If knowledge percentage is unknown, the owner may explicitly waive it:

```text
mode = OWNER_OVERRIDE
reason = explicit
support_profile = explicit
demand_profile = explicit
```

The override is auditable and does not fabricate a percentage. It may set support density and the already-authorized demand profile, including transfer distance, interleaving, synthesis width and time pressure.

The fail-closed rule is:

```text
no knowledge percentage
+ no explicit owner override
= BLOCK CORE2A / CORE2B COMPILATION
```

There is no silent default to 50%.

The v4 default support bands are compilation policy rather than empirical mastery claims:

- `0–30`: high support;
- `31–60`: medium support;
- `61–80`: low support;
- `81–100`: minimal initial support.

Owner purpose remains distinct from learner knowledge. Learner knowledge primarily controls **support**; owner purpose controls **transfer distance, mixing, synthesis and time pressure** within existing Core2 legality.

Core2A and Core2B share the same legal question authority. Core2A is exposition-rich guided problem teaching; Core2B is elicitation-first problem-solving tutoring. Open-ended B-layer realization still requires complete static answer closure.

## v4 contracts and policy

```text
contracts/instruction-bucket-v4.schema.json
contracts/core2-learner-conditioning-v4.schema.json
policies/v4-bucket-and-conditioning-policy.json
engine/validate_blueprint_v4.py
```

The v4 validator fails closed for, among other things:

```text
CHEM_V4_CORE1_KNOWLEDGE_CONTAMINATION
CHEM_V4_BUCKET_PAGE_ENVELOPE_INVALID
CHEM_V4_MEDIUM_RESEARCH_MISSING
CHEM_V4_HARD_DEEP_RESEARCH_MISSING
CHEM_V4_BUCKET_VISUAL_JOB_CLOSURE_MISSING
CHEM_V4_CONDITIONING_DUAL_AUTHORITY
CHEM_V4_OWNER_OVERRIDE_REASON_MISSING
CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED
```

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

python 'Grade 9/V2/Chemistry/LearningBlueprint/engine/validate_blueprint_v4.py' \
  --policy 'Grade 9/V2/Chemistry/LearningBlueprint/policies/v4-bucket-and-conditioning-policy.json' \
  --bucket bucket.json

python 'Grade 9/V2/Chemistry/LearningBlueprint/engine/validate_blueprint_v4.py' \
  --policy 'Grade 9/V2/Chemistry/LearningBlueprint/policies/v4-bucket-and-conditioning-policy.json' \
  --conditioning core2-conditioning.json
```

Add `--realization realization-evidence.json` to v2 only after learner-facing realization exists and there is evidence for the taught-state flags. v3 intentionally requires a `T-*` receipt; it cannot infer taught state from the assimilation plan.

## Not yet claimed

v4 establishes **control authority**, not a learner-outcome claim. It does not infer mastery from a percentage, infer taught state from a PDF, or authorize new Chemistry content. Core1A/Core1B and Core2A/Core2B compilers must consume these controls downstream. Human subject, pedagogy, assessment and visual-usability gates remain separate from machine completion.
