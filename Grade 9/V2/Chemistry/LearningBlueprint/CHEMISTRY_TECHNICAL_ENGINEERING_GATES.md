# Chemistry Technical Engineering Gate Registry

**Authority Tier:** `CANONICAL_DOMAIN_REGISTRY`  
**Governing Policy:** `skills/engineering-pr-delivery-v2/references/repository-agent-policy.md`  
**Maturity:** `ENGINEERING` (Fail-closed technical engineering readiness; strictly zero psychometric or empirical calibration claims)  
**Upstream Boundary:** Sits between Canonical Domain Registry and Content Custody & Coverage Units (CCU) / Core Differentiation Units (CDAU). Upstream of authored Teaching-Task Units (TTUs).

---

## 1. Architectural Role & Boundary Separation

In the Grade 9–11 Chemistry self-learning architecture (`Grade 9/V2/Chemistry/LearningBlueprint`), content custody and adaptive sequencing cannot compensate for an underspecified or chemically flawed foundation. If an authoring track (Core1A, Core1B, Core2A, Core2B) generates learning tasks before technical chemistry constraints are locked down, critical defects leak into learner materials:
- Chemical formulas written without charge balance or missing polyatomic ion brackets ($MgCl$, $Al_2SO_4_3$).
- Chemical equations balanced by mutating formula subscripts ($H_2 + O_2 \to H_2O_2$ to form water).
- Conflating pure liquids $(l)$ with aqueous solutions $(aq)$, or omitting state symbols during precipitation.
- Hand-waving reaction conditions (temperature $\Delta$, pressure, catalysts) as spontaneous room-temperature events.
- Disconnected macroscopic observations from particulate species transformations.
- Computing stoichiometric quantities by mass ratios instead of molar ratios.
- Asserting acidity for dry anhydrous species without water/hydronium ionization.
- Inverting redox roles by claiming the oxidizing agent is the oxidized species.

To eliminate these omission defects at the source, the **Chemistry Technical Engineering Gate Registry** operates at the **CANONICAL DOMAIN REGISTRY** boundary. Every subtopic must satisfy **fail-closed engineering readiness** before any TTU can be authored.

### Strict Layer Boundary Separation:
```text
Technical Engineering Gate
  = what chemical structure MUST exist (concepts, equations, representations, boundaries, traps, checks)

CCU (Content Custody & Coverage)
  = did we preserve it / source it / answer it / avoid skipping or duplicating it

CDAU (Core Differentiation)
  = does it belong in this Core track / is it differentiated from neighboring Cores

SDU / LAU
  = intrinsic difficulty profile (Core1) vs learner-fit routing (Core2)

TTU (Teaching-Task Unit)
  = micro-interaction graph of learning, reconstruction, reveal, and repair
```

---

## 2. The Fail-Closed Enforcement Principle

> **A gate is not fail-closed because a test knows what was deleted. It is fail-closed only when the production validator, using the exact contract future products will use, rejects the defective state with a deterministic, typed error code.**

No subtopic may claim `technical_readiness: ENGINEERING_GATE_READY` unless:
1. It validates against the closed JSON Schema (`additionalProperties: false` on all governed objects).
2. It satisfies all global uniqueness and cross-reference integrity constraints.
3. It fulfills all 16 technical gate points (A through P).
4. Its 10-point release checklist is 100% complete and verified.
5. It passes all mutation falsifiers executed against the production validator.

---

## 3. Core Role Terminology

To prevent pedagogical role drift across authoring kits, all Chemistry gates conform strictly to canonical Core roles:
- `CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION`: Declarative-dominant complete conceptual construction and technical study reference.
- `CORE1B_GENERATIVE_RECONSTRUCTION`: Generative-dominant concept reconstruction, diagnosis, and teach-back.
- `CORE2A_DECLARATIVE_WORKED_PROBLEM`: Declarative worked Problem TTU with complete canonical solution and why-steps.
- `CORE2B_GENERATIVE_TRANSFER`: Generative transfer, independent problem-solving commitment, and repair.

---

## 4. Decomposed Subtopic Gates (10 Technically Coherent Gates)

The registry decomposes Chemistry by **technical coherence** rather than textbook chapter headings:

| Subtopic ID | Title | Authority Tier | Key Gate Enforcement |
| :--- | :--- | :--- | :--- |
| `CHEM-SYM-LITERACY` | Chemical Symbols, Atomic Notation & Formula Literacy | SOURCE-DEFINED | Subscripts vs coefficients; isotopic notation $^A_Z X$; diatomic molecules |
| `CHEM-ION-VALENCY` | Ions, Valency, Polyatomic Radicals & Formal Charge | SOURCE-DEFINED | Charge magnitude & sign; polyatomic radicals bracketed $(SO_4^{2-})$ |
| `CHEM-FORMULA-CONSTRUCTION` | Chemical Formula Construction & Electroneutrality | SOURCE-DEFINED | $\sum q_i = 0$; criss-cross valency; rejection of unneutralized ionic formulas |
| `CHEM-EQ-BALANCING` | Conservation of Mass & Equation Balancing | SOURCE-DEFINED | Atom conservation per element; coefficient-only balancing; subscript immutability |
| `CHEM-STATE-SYMBOLS` | Physical State Symbols, Precipitation & Gas Evolution | SOURCE-DEFINED | $(s), (l), (g), (aq)$; distinguishing $(l)$ vs $(aq)$; precipitation $(\downarrow)$ and gas $(\uparrow)$ |
| `CHEM-REACTION-CONDITIONS` | Reaction Conditions, Enthalpy & Catalytic Constraints | STANDARD-CHEMISTRY-DERIVED | Reversible $(\rightleftharpoons)$ vs forward $(\to)$; catalysts, $T, P$; exothermic vs endothermic |
| `CHEM-REP-TRANSLATION` | Johnstone's Triplet (Particulate ↔ Symbolic ↔ Macroscopic) | STANDARD-CHEMISTRY-DERIVED | Sensory observation mapped to sub-microscopic species and chemical formula |
| `CHEM-CALC-STOICHIOMETRY` | Stoichiometry, Mole Conversions & Limiting Reagents | SOURCE-DEFINED | $n = m/M$; molar ratio from coefficients; mass-ratio fallacy prevention |
| `CHEM-ACID-BASE-IONS` | Acids, Bases, Aqueous Ionization & Net Ionic Neutralization | SOURCE-DEFINED | $H^+/H_3O^+$ production; moisture required for acidity; net ionic $H^+ + OH^- \to H_2O$ |
| `CHEM-REDOX-OXIDATION` | Redox Reactions, Oxidation States & Electron Transfer | SOURCE-DEFINED | Electron conservation; oxidation state rules; oxidizing agent is the species reduced |

---

## 5. Canonical 16-Point Gate Structure (Per Subtopic)

Every registered subtopic satisfies all 16 mandatory technical gate dimensions:

1. **Subtopic Identity & Maturity:** Unique `CHEM-*` ID, learner title, authority tier, and strict `maturity: ENGINEERING`.
2. **Provenance:** Traceable curriculum authority (`source_curriculum`, `source_reference`, `source_scope`, `claim_status`).
3. **Prerequisites & Cross-Bindings:** Explicit dependencies on prior chemistry or mathematics gates with cycle prevention.
4. **Technical Core (Point A):** Canonical concept statements, physical rationale, and failure consequences if omitted.
5. **Mandatory Equations & Species (Point B):** Formal chemical equations with structured symbol/species dictionaries (`symbol`, `name`, `si_unit` or state, `dimension`), conditions of validity, and obligations (`EXPLAIN`, `DERIVE`, `INTERPRET`, `REPRESENT`, `APPLY`, `INVERT`, `VERIFY`).
6. **Canonical Representations (Point C):** Visual models (Lewis structures, particulate diagrams, reaction arrows, BCA tables, phase schematics), mandatory labels, what cannot be omitted, and common incorrect diagrams.
7. **Model Conditions & Boundaries (Point D):** Domain validity limits (dilute aqueous solutions, ideal gases, room conditions), breakdown thresholds, asymptotic/limiting behaviors.
8. **Reasoning Sequence (Point E):** Step-by-step inferential sequence with classified jump fragilities (`LOW`, `MEDIUM`, `HIGH_FRAGILITY`); zero hand-waving permitted.
9. **Required Transformations (Point F):** Explicit mapping across Core1A, Core1B, Core2A, and Core2B.
10. **Misconceptions & Traps (Point G):** Systematic intuitive errors, psychological roots, discrimination challenges, and refutation proofs.
11. **Mandatory Verifications (Point H):** Atom balance checks, charge balance checks, state consistency, conservation constraints, limiting reactant checks.
12. **Canonical Problem Families (Point I):** Standard problem archetypes, recognition cues, first technical moves, and fatal error traps.
13. **Difficulty Profile (Point J):** 10-dimension objective complexity rating (0–3 scale), `maturity: ENGINEERING` (strictly zero psychometric calibration overclaims).
14. **Release Checklist (Point K):** 10 automated boolean checks; gate cannot be `ENGINEERING_GATE_READY` unless 100% satisfied.
15. **Badges (Point L):** Syllabus alignment, bucket links, cognitive demand tags.
16. **Falsification Cases (Point M):** Test fixtures asserting gate rejection if key invariants are violated.
