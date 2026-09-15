# OWNER BOARD — Motion in Two Dimensions and Relative Motion

Status: **DESIGN/SELF-STUDY REHEARSAL — NOT RELEASED**  
Academic year: **2026–27**  
Topic ID: `PHY-M2D-RM-20260915`  
Source corpus: `SYN-M2D-20260915-V1` (`FROZEN_FOR_TEST`)  
Learner fixture: `K50` synthetic rehearsal input only; aggregate 5/10 is not a real learner diagnosis.  
Work item source: `OWNER_DIRECT`  
Branch: `draft/motion2d-relative-motion-selfstudy-20260915`  
Created first, before learner-manuscript authoring, as required by the topic contract.

## Exact architecture/instruction revisions read before authoring

| Authority | Live state read | Exact revision used | Role in this run |
|---|---|---|---|
| Root `AGENTS.md` | branch inherited from V3B draft | blob `2c1d476e4be59dbcd8b20e6705fdf89fd103c2aa` | Repository overlay; owner-only merge; validation truth |
| Engineering delivery v2 | `skills/engineering-pr-delivery-v2/SKILL.md` | live file on V3B draft branch; minimum basis named by root overlay `36068fde5b860ca1870311b166d28077b4c0bcf8` | Crash/restart, custody, NOT_RUN integrity |
| Physics PR #350 | open draft, current head | `88e7adaac2368bd65dc98537b892e6fae8836994` | **Primary Physics authority**; A/B authority split and self-study semantics |
| Mathematics PR #351 | open draft, current head | `3fbb0e66473462e8365538b5f63b9ae9af3f120f` | Architectural comparison only; no Mathematics edits |
| Chemistry PR #362 | open draft, current head | `23d859a8fa0d07e0790d323767dc7fd08f396c5d` | Architectural comparison only; no Chemistry edits |
| V3B Physics PR #364 | open draft, current head | `6be71db1a321c449131a26ee3084b6b9c0edca28` | V3B six-Core/gate execution contract and specimens |
| `Physics/CoreContracts.json` | PR #364 branch | blob `dee9520c7dee3fa7da97b9276768fa323bec9268` (`contract_version=1.1.0`) | Physics semantic fields and six-Core role binding |
| `Engineering/CORE_CONTRACTS.md` | PR #364 branch | blob `291d42c8999205c6c08660525f262fde0e5d34c1` | Six-Core learner jobs, omission controls, similarity policy |
| `Engineering/PACKET_CONTRACT.md` | PR #364 branch | blob `e84c6e23bf2bba01426f2b5a95c9fa99084b7519` | Relay packet envelope/restart requirements |
| `Engineering/TOPIC_WORKFLOW.md` | PR #364 branch | blob `b968c118cad27ca8e11b9ffe4608a00c539a98b9` | Topic setup, extension, invalidation and research-depth boundary |

`Physics/CoreContracts.json` records `engineering_adoption_head=f2f22f0cea1c31ebf09da10241db8be0fde39789`; this run does **not** treat that older adoption SHA as the live PR head. The live PR #350 and #364 heads above were re-verified on 2026-09-15.

## Official scope evidence already verified

Access date: **2026-09-15**.

- Standard Science, Class IX (2026–27), Motion section on PDF p.14 (viewer page index 13): motion focuses on displacement/velocity/acceleration, straight-line graphical representation and kinematic equations, plus an elementary idea of uniform circular motion; outcomes explicitly differentiate distance/displacement and speed/velocity for straight-line motion and plot/interpret straight-line graphs. URL: `https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf`.
- Optional Advanced Science, Class IX (2026–27), Chapter 2 §§2.1–2.4 on PDF pp.10–12 (viewer indexes 9–11): motion is described relative to a reference point/frame; Activity 2.2 explicitly treats motion as relative; scalars/vectors and graphical vector addition are introduced. The end-of-chapter check asks for graphical vector subtraction. URL: `https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceAd_SecP1_2026-27.pdf`.
- Therefore two-coordinate constant-velocity work, explicit relative-velocity subtraction, meeting/collision logic, boat/current, rain/observer and closest approach are not silently promoted to Standard Science examination requirements. Each outcome will be mapped individually in `scope-map.csv`.

## Gate board

Statuses are intentionally separate. `READY_FOR_REVIEW` means a reviewable package exists; it does **not** mean owner approval, learner validation, publication or release.

| Gate | Purpose in plain language | Prerequisites | Evidence links | Defined | Structure checked | Content checked | Visually checked | Ready for review | Current blocker | Affected buckets/Cores | Next action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G0 Input and scope | Freeze what is being taught, what came from the synthetic corpus, what CBSE actually requires, and what K50 does/does not mean. | Live contracts; official PDFs; supplied corpus/fixture | `scope-map.csv`, `requirements.json`, `source-corpus.md`, `source-inventory.json` | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | Inventory and per-outcome map not yet materialized | B01–B08; all Cores | Build source inventory and scope map; reconcile to frozen source |
| G1 Physics model | Make frame, sign, clock, units, equations and assumptions scientifically explicit and independently recompute examples. | G0 scope; canonical notation | `equation-register.json`, `qa/arithmetic-checks.md`, Core worked examples | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | Equation register/examples not yet authored | B01–B08; all Cores | Build canonical equation register and independent arithmetic table |
| G2 Completeness | Ensure every source atom/subpart and every frozen Core obligation has a real output locator or an honest hold. | G0 inventory; frozen dispositions | `coverage.csv`, `question-register.csv`, `qa/source-fidelity.md` | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | Atom inventory/dispositions not yet frozen | All buckets; all Cores | Freeze dispositions before prose; then realize and verify 100% required realization |
| G3 Core identity | Prove 1/2/1A/1B/2A/2B remain distinct learner experiences. | Core contracts; actual learner files | `qa/core-purpose-review.md`, six Core files | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | Learner files not yet authored | All buckets/Cores | Author to distinct purposes; run self-review |
| G4 Difficulty and practice fit | Separate intrinsic bucket difficulty, question demand and learner support; keep K50 synthetic and low-confidence. | Frozen bucket badges; K50 policy; 2A/2B plan | `question-register.csv`, `qa/difficulty-fit-review.md` | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | New banks not yet authored | B01–B08; 2A/2B | Author exactly 6 entry/4 standard/2 stretch per bank; score each demand dimension |
| G5 Visual and self-help quality | Realize functional diagrams, readable labels, answer links and complete self-help closure. | Content; diagram specifications | `diagrams/`, Core files, `qa/visual-inspection.md` | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | Assets not yet drawn/linked | B01–B08; all Cores | Build exact SVGs, validate references and inspect source-level semantics |
| G6 Reuse and transfer | Detect inappropriate copying and prove transfer changes learner action/structure rather than names/numbers. | Authored blocks; reuse register | `qa/similarity-review.md`, `qa/reuse-register.csv` | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | No authored blocks to compare yet | Cross-Core; especially 1A↔1B and 2A↔2B | Run reproducible shingle/containment + structural review after authoring |
| G7 Relay and regression | Leave complete packet handoffs and honest restart/regression state. | G0–G6 evidence | `packets/`, `qa/executed-tests.md` | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | Packets/tests not yet built; independent cold run unavailable in single instance | All bundles/Cores | Build 3 packets + master; run local validators; mark cold/independent review NOT_RUN |
| G8 Delivery | Confirm all six products/reports exist and unresolved items are conspicuous. | G0–G7 | `README.md`, file/anchor/asset checks, final report | **DEFINED** | HOLD | NOT_RUN | NOT_RUN | HOLD | Deliverables not yet materialized | Whole package | Complete package; run existence/link checks; leave release false |

## Immutable boundaries for this run

- Preserve all existing V2 material.
- Do not edit Mathematics or Chemistry.
- Do not merge, publish, or mark learner/exam readiness.
- Core 2 must preserve Q01–Q12 source wording, numbering, subparts and data exactly; support surrounds the immutable source block.
- Q12 remains underdetermined as written. Any repaired variant gets a new ID and `derived_from=Q12`.
- Core 1A/1B depth is controlled by intrinsic bucket difficulty, not K50.
- Core 2A/2B use K50 only as the explicit synthetic rehearsal input and must each contain exactly 12 authored questions: 6 entry, 4 standard, 2 stretch.
- Projectile derivations, rotating frames, relativity and gravity research are outside the baseline topic; closest approach is a small labelled enrichment only.

## Review independence

Producer/reviewer for this run: one ChatGPT execution instance. Any content/physics/pedagogy review performed by this instance will be labelled **SELF_REVIEW**. No independent reviewer or learner trial is claimed. Cold restart and independent review remain `NOT_RUN` unless a genuinely fresh authorized execution is later performed.
