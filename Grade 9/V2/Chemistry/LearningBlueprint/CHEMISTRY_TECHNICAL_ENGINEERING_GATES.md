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

## 4. Complete Grade 9–11 Master Technical Engineering Gate Registry (52 Subtopics)

| Gate ID | Learner Title | Gr | CBSE Ch | JEE Tier | Prereqs | Key Formula / Reaction Constraint |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `CHEM-SYM-LITERACY` | Chemical Symbols, Atomic Notation & Formula Literacy | 9 | Ch 3 | `JEE_MAINS` | MATH-BASIC-ARITHMETIC | `$A = Z + N$` |
| `CHEM-ION-VALENCY` | Ions, Valency, Polyatomic Radicals & Formal Charge | 9 | Ch 3 | `JEE_MAINS` | CHEM-SYM-LITERACY | `$q_ion = (Z - N_e) e$` |
| `CHEM-FORMULA-CONSTRUCTION` | Chemical Formula Construction & Electroneutrality | 9 | Ch 3 | `BOTH` | CHEM-ION-VALENCY | `$n_+ * z_+ + n_- * z_- = 0$` |
| `CHEM-EQ-BALANCING` | Conservation of Mass & Chemical Equation Balancing | 10 | Ch 1 | `BOTH` | CHEM-FORMULA-CONSTRUCTION | `$sum_reactants nu_i * N_{i, k} = sum_products nu_j * N_{j, k}$` |
| `CHEM-STATE-SYMBOLS` | Physical State Symbols, Precipitation & Gas Evolution | 10 | Ch 1 | `JEE_MAINS` | CHEM-EQ-BALANCING | `$BaCl2(aq) + Na2SO4(aq) -> BaSO4(s) + 2NaCl(aq)$` |
| `CHEM-REACTION-CONDITIONS` | Reaction Conditions, Enthalpy & Catalytic Constraints | 10 | Ch 1 | `BOTH` | CHEM-STATE-SYMBOLS | `$6CO2(aq) + 12H2O(l) -> C6H12O6(aq) + 6O2(g) + 6H2O(l) [sunlight, chlorophyll]$` |
| `CHEM-REP-TRANSLATION` | Johnstone's Triplet (Particulate <-> Symbolic <-> Macroscopic) | 9 | Ch 3 | `JEE_MAINS` | CHEM-STATE-SYMBOLS | `$Cu^2+(aq)[blue solution] + 2OH^-(aq)[colorless] -> Cu(OH)2(s)[pale blue precipitate]$` |
| `CHEM-CALC-STOICHIOMETRY` | Stoichiometry, Mole Conversions & Limiting Reagents | 9 | Ch 3 | `BOTH` | CHEM-EQ-BALANCING | `$n = m / M = N / N_A$` |
| `CHEM-ACID-BASE-IONS` | Acids, Bases, Aqueous Ionization & Net Ionic Neutralization | 10 | Ch 2 | `BOTH` | CHEM-STATE-SYMBOLS | `$H+(aq) + OH^-(aq) -> H2O(l)$` |
| `CHEM-REDOX-OXIDATION` | Redox Reactions, Oxidation States & Electron Transfer | 10 | Ch 1 | `BOTH` | CHEM-ION-VALENCY, CHEM-EQ-BALANCING | `$CuO(s) + H2(g) -> Cu(s) + H2O(l)$` |
| `CHEM-MATTER-STATES` | States of Matter: Solid, Liquid, Gas & Kinetic Particle Theory | 9 | Ch 1 | `NOT_IN_JEE` | None | `$KE_{\text{avg}} = \frac{3}{2} k_B T$` |
| `CHEM-MATTER-LATENT-HEAT` | Latent Heat of Fusion/Vaporization & Evaporative Cooling | 9 | Ch 1 | `NOT_IN_JEE` | CHEM-MATTER-STATES | `$Q = m L$` |
| `CHEM-MIXTURE-SEPARATION` | Mixtures: True Solutions, Colloids, Suspensions & Tyndall Effect | 9 | Ch 2 | `NOT_IN_JEE` | CHEM-MATTER-STATES | `$\text{Mass \%} = \frac{\text{Mass of Solute}}{\text{Mass of Solution}} \times 100$` |
| `CHEM-ATOM-RUTHERFORD-BOHR` | Atomic Models: Rutherford Nuclear Planetary Model & Bohr Quantized Shells | 9 | Ch 4 | `JEE_MAINS` | CHEM-SYM-LITERACY | `$m_e v r = n \frac{h}{2\pi}$` |
| `CHEM-ATOM-ISOTOPES-ISOBARS` | Valency, Electronic Configuration, Isotopes & Isobars | 9 | Ch 4 | `JEE_MAINS` | CHEM-ATOM-RUTHERFORD-BOHR, CHEM-ION-VALENCY | `$\bar{A} = \sum (A_i \times f_i)$` |
| `CHEM-RXN-TYPES-DECOMPOSITION` | Types of Reactions: Combination, Thermal/Electrolytic Decomposition & Displacement | 10 | Ch 1 | `JEE_MAINS` | CHEM-EQ-BALANCING, CHEM-STATE-SYMBOLS | `$2 H_2O (l) \xrightarrow{\text{electrolysis}} 2 H_2 (g) + O_2 (g)$` |
| `CHEM-ACID-PH-INDICATORS` | pH Scale, Universal Indicators & Auto-Ionization of Water | 10 | Ch 2 | `JEE_MAINS` | CHEM-ACID-BASE-IONS | `$\text{pH} = -\log_{10}[\text{H}^+], \quad \text{pH} + \text{pOH} = 14 \quad (25^\circ\text{C})$` |
| `CHEM-SALTS-DOMESTIC-INDUSTRIAL` | Salts: Chlor-Alkali Process, Bleaching Powder, Baking/Washing Soda & POP | 10 | Ch 2 | `NOT_IN_JEE` | CHEM-ACID-BASE-IONS, CHEM-EQ-BALANCING | `$2 \text{NaCl} (aq) + 2 \text{H}_2\text{O} (l) \xrightarrow{\text{electrolysis}} 2 \text{NaOH} (aq) + \text{Cl}_2 (g) + \text{H}_2 (g)$` |
| `CHEM-METALS-REACTIVITY-SERIES` | Metals & Non-Metals: Reactivity Series, Amphoteric Oxides & Corrosion | 10 | Ch 3 | `JEE_MAINS` | CHEM-RXN-TYPES-DECOMPOSITION | `$\text{Al}_2\text{O}_3 + 6 \text{HCl} \to 2 \text{AlCl}_3 + 3 \text{H}_2\text{O}, \quad \text{Al}_2\text{O}_3 + 2 \text{NaOH} \to 2 \text{NaAlO}_2 + \text{H}_2\text{O}$` |
| `CHEM-IONIC-BOND-PROPERTIES` | Ionic Bonding: Electron Transfer, Electrostatic Lattice & Ionic Properties | 10 | Ch 3 | `BOTH` | CHEM-ION-VALENCY, CHEM-FORMULA-CONSTRUCTION | `$F = \frac{1}{4\pi\varepsilon_0} \frac{\|q_1 q_2\|}{r^2}, \quad U_{\text{lattice}} \propto -\frac{\|z^+ z^-\|}{r_0}$` |
| `CHEM-METALS-EXTRACTION-METALLURGY` | Metallurgy: Concentration, Calcination, Roasting, Carbon Reduction & Refining | 10 | Ch 3 | `JEE_MAINS` | CHEM-METALS-REACTIVITY-SERIES, CHEM-REDOX-OXIDATION | `$2 \text{ZnS} + 3 \text{O}_2 \xrightarrow{\Delta} 2 \text{ZnO} + 2 \text{SO}_2, \quad \text{ZnCO}_3 \xrightarrow{\Delta} \text{ZnO} + \text{CO}_2$` |
| `CHEM-CARBON-COVALENT-BONDING` | Carbon: Tetravalency, Catenation, Allotropes & Covalent Bond Sharing | 10 | Ch 4 | `JEE_MAINS` | CHEM-SYM-LITERACY, CHEM-IONIC-BOND-PROPERTIES | `$\text{C} + 4 \text{H} \to \text{CH}_4, \quad \sum \text{shared pairs} = 4$` |
| `CHEM-CARBON-HOMOLOGOUS-SERIES` | Homologous Series, Functional Groups & IUPAC Nomenclature Basics | 10 | Ch 4 | `BOTH` | CHEM-CARBON-COVALENT-BONDING | `$\text{Alkane: } \text{C}_n\text{H}_{2n+2}, \quad \text{Alkene: } \text{C}_n\text{H}_{2n}, \quad \text{Alkyne: } \text{C}_n\text{H}_{2n-2}$` |
| `CHEM-CARBON-COMBUSTION-SOAPS` | Carbon Reactions: Combustion, Esterification, Saponification & Micelles | 10 | Ch 4 | `JEE_MAINS` | CHEM-CARBON-HOMOLOGOUS-SERIES, CHEM-EQ-BALANCING | `$\text{CH}_3\text{COOH} + \text{C}_2\text{H}_5\text{OH} \xrightleftharpoons{\text{conc. } \text{H}_2\text{SO}_4} \text{CH}_3\text{COOC}_2\text{H}_5 + \text{H}_2\text{O}$` |
| `CHEM-STOICH-CONCENTRATION-UNITS` | Solution Concentrations: Molarity, Molality, Mole Fraction & Dilution Law | 11 | Ch 1 | `BOTH` | CHEM-CALC-STOICHIOMETRY | `$M = \frac{n_{\text{solute}}}{V_{\text{solution}} \, (\text{L})}, \quad m = \frac{n_{\text{solute}}}{m_{\text{solvent}} \, (\text{kg})}, \quad M_1 V_1 = M_2 V_2$` |
| `CHEM-STOICH-EMPIRICAL-FORMULA` | Empirical & Molecular Formula Determination from Elemental Analysis | 11 | Ch 1 | `BOTH` | CHEM-CALC-STOICHIOMETRY | `$n = \frac{\text{Molar Mass}}{\text{Empirical Formula Mass}}, \quad \text{Molecular Formula} = (\text{Empirical Formula})_n$` |
| `CHEM-ATOM-PHOTOELECTRIC-BOHR` | Photoelectric Effect, Planck's Quantum Theory & Bohr Hydrogen Spectrum | 11 | Ch 2 | `BOTH` | CHEM-ATOM-RUTHERFORD-BOHR | `$h \nu = \Phi + \text{KE}_{\text{max}} = h \nu_0 + \frac{1}{2} m_e v_{\text{max}}^2, \quad \bar{\nu} = R_H Z^2 \left(\frac{1}{n_1^2} - \frac{1}{n_2^2}\right)$` |
| `CHEM-ATOM-DE-BROGLIE-UNCERTAINTY` | de Broglie Wavelength & Heisenberg Uncertainty Principle | 11 | Ch 2 | `BOTH` | CHEM-ATOM-PHOTOELECTRIC-BOHR | `$\lambda = \frac{h}{m v} = \frac{h}{\sqrt{2 m \, \text{KE}}}, \quad \Delta x \cdot \Delta p \ge \frac{h}{4\pi} \implies \Delta x \cdot \Delta v \ge \frac{h}{4\pi m}$` |
| `CHEM-ATOM-QUANTUM-NUMBERS` | Quantum Numbers, Orbital Shapes (s, p, d) & Radial/Angular Nodes | 11 | Ch 2 | `BOTH` | CHEM-ATOM-DE-BROGLIE-UNCERTAINTY | `$\text{Radial Nodes} = n - l - 1, \quad \text{Angular Nodes} = l, \quad \text{Total Nodes} = n - 1$` |
| `CHEM-ATOM-ELECTRONIC-CONFIG` | Electronic Configuration: Aufbau Principle, Pauli Exclusion & Hund's Rule | 11 | Ch 2 | `BOTH` | CHEM-ATOM-QUANTUM-NUMBERS | `$\text{Energy} \propto (n + l), \quad \text{Exchange Energy} \propto \frac{K n(n-1)}{2}$` |
| `CHEM-PERIODIC-TABLE-TRENDS` | Periodic Trends: Effective Nuclear Charge (Z_eff), Atomic & Ionic Radii | 11 | Ch 3 | `BOTH` | CHEM-ATOM-QUANTUM-NUMBERS | `$Z_{\text{eff}} = Z - \sigma$` |
| `CHEM-PERIODIC-IONIZATION-ENERGY` | Ionization Enthalpy, Electron Gain Enthalpy & Electronegativity Trends | 11 | Ch 3 | `BOTH` | CHEM-PERIODIC-TABLE-TRENDS | `$\|\chi_A - \chi_B\| = 0.208 \sqrt{\Delta}, \quad \Delta = E_{A-B} - \sqrt{E_{A-A} \cdot E_{B-B}}$` |
| `CHEM-BOND-LEWIS-FORMAL-CHARGE` | Lewis Electron Structures, Octet Exceptions & Formal Charge Calculation | 11 | Ch 4 | `BOTH` | CHEM-CARBON-COVALENT-BONDING | `$\text{FC} = V - L - \frac{1}{2} B$` |
| `CHEM-BOND-DIPOLE-RESONANCE` | Dipole Moments (mu = q x d), Bond Polarity & Resonance Hybrid Structures | 11 | Ch 4 | `BOTH` | CHEM-BOND-LEWIS-FORMAL-CHARGE | `$\vec{\mu} = \sum q_i \vec{d}_i, \quad \mu = q \times d \quad (1 \text{ Debye} = 3.33564 \times 10^{-30} \text{ C m})$` |
| `CHEM-BOND-VSEPR-GEOMETRY` | VSEPR Theory: Electron Pair Repulsions, Steric Numbers & Molecular Geometries | 11 | Ch 4 | `BOTH` | CHEM-BOND-DIPOLE-RESONANCE | `$\text{SN} = \text{Number of } \sigma \text{ Bonds} + \text{Number of Lone Pairs on Central Atom}$` |
| `CHEM-BOND-HYBRIDIZATION-ORBITAL` | Valence Bond Theory: Orbital Overlap & Hybridization (sp, sp2, sp3, sp3d, sp3d2) | 11 | Ch 4 | `BOTH` | CHEM-BOND-VSEPR-GEOMETRY | `$\text{Hybridization} = s^{1} p^{x} d^{y}, \quad \text{Index } 1 + x + y = \text{SN}$` |
| `CHEM-BOND-MOT-DIATOMIC` | Molecular Orbital Theory: LCAO, Bonding/Antibonding MOs, Bond Order & Paramagnetism | 11 | Ch 4 | `JEE_ADVANCED` | CHEM-BOND-HYBRIDIZATION-ORBITAL | `$\text{Bond Order} = \frac{1}{2} (N_b - N_a), \quad \mu_s = \sqrt{n(n+2)} \, \text{BM}$` |
| `CHEM-BOND-HYDROGEN-BONDING` | Hydrogen Bonding: Intermolecular vs Intramolecular & Anomalous Water Properties | 11 | Ch 4 | `BOTH` | CHEM-BOND-DIPOLE-RESONANCE | `$E_{\text{H-bond}} \approx 10 - 40 \text{ kJ/mol}, \quad \rho_{\text{water}}(4^\circ\text{C}) = \text{maximum}$` |
| `CHEM-THERMO-FIRST-LAW-WORK` | Thermodynamics: State Functions, First Law (Delta U = q + w) & Expansion Work | 11 | Ch 5 | `BOTH` | CHEM-CALC-STOICHIOMETRY | `$\Delta U = q + w, \quad w_{\text{irrev}} = -P_{\text{ext}} \Delta V, \quad w_{\text{rev}} = -2.303 \, n R T \log_{10}\left(\frac{V_2}{V_1}\right)$` |
| `CHEM-THERMO-ENTHALPY-HESS` | Enthalpy (Delta H = Delta U + Delta n_g RT), Heat Capacities & Hess's Law | 11 | Ch 5 | `BOTH` | CHEM-THERMO-FIRST-LAW-WORK | `$\Delta H = \Delta U + \Delta n_g R T, \quad \Delta_r H^\circ = \sum \nu_p \Delta_f H^\circ(\text{products}) - \sum \nu_r \Delta_f H^\circ(\text{reactants})$` |
| `CHEM-THERMO-ENTROPY-SECOND-LAW` | Entropy (Delta S = q_rev / T), Second Law & Spontaneity of Isolated Systems | 11 | Ch 5 | `BOTH` | CHEM-THERMO-ENTHALPY-HESS | `$\Delta S_{\text{univ}} = \Delta S_{\text{sys}} + \Delta S_{\text{surr}} > 0, \quad \Delta S_{\text{surr}} = -\frac{\Delta H_{\text{sys}}}{T}$` |
| `CHEM-THERMO-GIBBS-SPONTANEITY` | Gibbs Free Energy (Delta G = Delta H - T Delta S), Spontaneity & Equilibrium | 11 | Ch 5 | `BOTH` | CHEM-THERMO-ENTROPY-SECOND-LAW | `$\Delta G = \Delta H - T \Delta S, \quad \Delta G^\circ = -R T \ln K = -2.303 \, R T \log_{10} K$` |
| `CHEM-EQUIL-LAW-MASS-ACTION` | Dynamic Equilibrium, Equilibrium Constants (Kc, Kp) & Reaction Quotient (Qc) | 11 | Ch 6 | `BOTH` | CHEM-THERMO-GIBBS-SPONTANEITY | `$K_p = K_c (R T)^{\Delta n_g}, \quad Q_c = \frac{[\text{C}]^c [\text{D}]^d}{[\text{A}]^a [\text{B}]^b}$` |
| `CHEM-EQUIL-LE-CHATELIER` | Le Chatelier's Principle: Temperature, Pressure, Volume & Inert Gas Shifts | 11 | Ch 6 | `BOTH` | CHEM-EQUIL-LAW-MASS-ACTION | `$\ln\left(\frac{K_2}{K_1}\right) = \frac{\Delta H^\circ}{R} \left(\frac{1}{T_1} - \frac{1}{T_2}\right)$` |
| `CHEM-EQUIL-IONIC-PH-OSTWALD` | Ionic Equilibrium: Ostwald Dilution Law, Ka/Kb & Weak Electrolyte pH | 11 | Ch 6 | `BOTH` | CHEM-ACID-PH-INDICATORS, CHEM-EQUIL-LAW-MASS-ACTION | `$K_a = \frac{C \alpha^2}{1 - \alpha} \approx C \alpha^2 \implies \alpha = \sqrt{\frac{K_a}{C}}, \quad [\text{H}^+] = \sqrt{K_a C}$` |
| `CHEM-EQUIL-BUFFERS-COMMON-ION` | Common Ion Effect, Buffer Solutions & Henderson-Hasselbalch Equation | 11 | Ch 6 | `BOTH` | CHEM-EQUIL-IONIC-PH-OSTWALD | `$\text{pH} = \text{p}K_a + \log_{10}\left(\frac{[\text{Conjugate Base / Salt}]}{[\text{Weak Acid}]}\right), \quad \text{pOH} = \text{p}K_b + \log_{10}\left(\frac{[\text{Salt}]}{[\text{Base}]}\right)$` |
| `CHEM-EQUIL-SOLUBILITY-PRODUCT` | Solubility Product (Ksp), Common Ion Suppression & Precipitation Criteria | 11 | Ch 6 | `BOTH` | CHEM-EQUIL-BUFFERS-COMMON-ION | `$K_{\text{sp}} = x^x y^y S^{x+y}, \quad Q_{\text{sp}} > K_{\text{sp}} \implies \text{Precipitation}$` |
| `CHEM-REDOX-BALANCING-CELLS` | Redox Balancing (Ion-Electron Method) & Galvanic Cell Foundations | 11 | Ch 7 | `BOTH` | CHEM-REDOX-OXIDATION | `$E_{\text{cell}} = E^\circ_{\text{cell}} - \frac{R T}{n F} \ln Q = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}} - \frac{0.0591}{n} \log_{10} Q$` |
| `CHEM-ORGANIC-NOMENCLATURE-ISOMER` | IUPAC Polyfunctional Nomenclature & Structural/Geometrical Isomerism | 11 | Ch 8 | `BOTH` | CHEM-CARBON-HOMOLOGOUS-SERIES | `$\text{DBE / IHD} = C + 1 - \frac{H}{2} - \frac{X}{2} + \frac{N}{2}$` |
| `CHEM-ORGANIC-ELECTRONIC-EFFECTS` | Electronic Displacements: Inductive, Resonance, Electromeric & Hyperconjugation | 11 | Ch 8 | `BOTH` | CHEM-ORGANIC-NOMENCLATURE-ISOMER | `$\text{Hyperconjugative Structures} = \alpha\text{-H count} + 1, \quad K_a \propto \text{Electron Withdrawing } (-I, -M)$` |
| `CHEM-ORGANIC-INTERMEDIATES-STABILITY` | Reaction Intermediates: Carbocations, Carbanions & Free Radicals Stability | 11 | Ch 8 | `BOTH` | CHEM-ORGANIC-ELECTRONIC-EFFECTS | `$\text{Carbocation/Radical: } 3^\circ > 2^\circ > 1^\circ > \text{CH}_3^+, \quad \text{Carbanion: } \text{CH}_3^- > 1^\circ > 2^\circ > 3^\circ$` |
| `CHEM-HYDROCARBONS-ALKENE-ADDITION` | Alkenes: Electrophilic Addition (Markovnikov vs Peroxide Effect) & Ozonolysis | 11 | Ch 9 | `BOTH` | CHEM-ORGANIC-INTERMEDIATES-STABILITY | `$R-\text{CH}=\text{CH}_2 + \text{HX} \to R-\text{CHX}-\text{CH}_3, \quad R_1 R_2\text{C}=\text{CH} R_3 \xrightarrow[2. \, \text{Zn}/\text{H}_2\text{O}]{1. \, \text{O}_3} R_1 R_2\text{C}=\text{O} + \text{O}=\text{CH} R_3$` |

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

---

## 6. Comprehensive 52-Subtopic Complexity Dimension Matrix

| Subtopic ID | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Provisional Difficulty | Dominant Complexity Drivers / Basis |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `CHEM-SYM-LITERACY` | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 1 | **EASY** | Direct symbolic literacy and integer particle counting |
| `CHEM-ION-VALENCY` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 1 | **MEDIUM** | Subatomic charge calculation and polyatomic radical bracket rules |
| `CHEM-FORMULA-CONSTRUCTION` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Electroneutrality constraints and polyatomic bracket rules |
| `CHEM-EQ-BALANCING` | 2 | 3 | 2 | 2 | 2 | 1 | 3 | 2 | 3 | 2 | **HARD** | High element interactivity and multi-step linear dependency across coupled equations |
| `CHEM-STATE-SYMBOLS` | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Distinction between pure phases and solvated aqueous species |
| `CHEM-REACTION-CONDITIONS` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Thermodynamic and kinetic condition requirements across reaction pathways |
| `CHEM-REP-TRANSLATION` | 2 | 3 | 2 | 3 | 2 | 1 | 2 | 3 | 3 | 2 | **HARD** | Simultaneous coordination across sensory macroscopic, particulate sub-microscopic, and abstract symbolic representations |
| `CHEM-CALC-STOICHIOMETRY` | 2 | 3 | 2 | 2 | 2 | 1 | 3 | 2 | 3 | 2 | **HARD** | Multi-step quantitative dimensional analysis and limiting reactant branching logic |
| `CHEM-ACID-BASE-IONS` | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 2 | 3 | 2 | **MEDIUM** | Ionization equilibrium distinctions and net ionic spectator cancellations |
| `CHEM-REDOX-OXIDATION` | 2 | 3 | 2 | 2 | 3 | 2 | 2 | 2 | 3 | 2 | **HARD** | Complex simultaneous electron bookkeeping and linguistic role inversion |
| `CHEM-MATTER-STATES` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Kinetic theory of matter and phase properties. |
| `CHEM-MATTER-LATENT-HEAT` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Thermodynamic phase transitions and latent heat. |
| `CHEM-MIXTURE-SEPARATION` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Colloidal dispersion and concentration mathematics. |
| `CHEM-ATOM-RUTHERFORD-BOHR` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Historical atomic models and quantized shell structure. |
| `CHEM-ATOM-ISOTOPES-ISOBARS` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Isotopic composition and fractional atomic weight. |
| `CHEM-RXN-TYPES-DECOMPOSITION` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Reaction taxonomy and displacement thermodynamics. |
| `CHEM-ACID-PH-INDICATORS` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Logarithmic acidity scale and aqueous equilibrium. |
| `CHEM-SALTS-DOMESTIC-INDUSTRIAL` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Industrial salt chemistry and waters of hydration. |
| `CHEM-METALS-REACTIVITY-SERIES` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Metal reactivity and electrochemical oxidation. |
| `CHEM-IONIC-BOND-PROPERTIES` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Ionic bonding, Coulomb attraction, and crystal conduction. |
| `CHEM-METALS-EXTRACTION-METALLURGY` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Extractive metallurgy and pyrometallurgy thermodynamics. |
| `CHEM-CARBON-COVALENT-BONDING` | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | **EASY** | Covalent bonding and allotropic carbon structures. |
| `CHEM-CARBON-HOMOLOGOUS-SERIES` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Organic nomenclature and homologous gradation. |
| `CHEM-CARBON-COMBUSTION-SOAPS` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Organic functional group transformations and micellar colloids. |
| `CHEM-STOICH-CONCENTRATION-UNITS` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Solution stoichiometry and volumetric concentration units. |
| `CHEM-STOICH-EMPIRICAL-FORMULA` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Gravimetric elemental analysis and empirical stoichiometry. |
| `CHEM-ATOM-PHOTOELECTRIC-BOHR` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Quantum electrodynamics and atomic spectroscopy. |
| `CHEM-ATOM-DE-BROGLIE-UNCERTAINTY` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Wave-particle duality and fundamental quantum limits. |
| `CHEM-ATOM-QUANTUM-NUMBERS` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Quantum numbers and orbital wave function geometry. |
| `CHEM-ATOM-ELECTRONIC-CONFIG` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Aufbau subshell ordering, spin multiplicity, and exchange stability. |
| `CHEM-PERIODIC-TABLE-TRENDS` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Periodic trends, Slater shielding, and Coulombic attraction. |
| `CHEM-PERIODIC-IONIZATION-ENERGY` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Periodicity, penetrating power, and exchange energy stability. |
| `CHEM-BOND-LEWIS-FORMAL-CHARGE` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Lewis structures, formal charge algebra, and octet boundary limits. |
| `CHEM-BOND-DIPOLE-RESONANCE` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Vector dipole algebra, molecular geometry, and resonance delocalization. |
| `CHEM-BOND-VSEPR-GEOMETRY` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | VSEPR repulsion dynamics, stereochemistry, and angular distortions. |
| `CHEM-BOND-HYBRIDIZATION-ORBITAL` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Orbital overlap integrals, hybridization mechanics, and pi-bond delocalization. |
| `CHEM-BOND-MOT-DIATOMIC` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Molecular orbital theory, LCAO quantum interference, and s-p orbital mixing. |
| `CHEM-BOND-HYDROGEN-BONDING` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Non-covalent electrostatic interactions and anomalous physical properties. |
| `CHEM-THERMO-FIRST-LAW-WORK` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Thermodynamic state functions, IUPAC sign conventions, and expansion work. |
| `CHEM-THERMO-ENTHALPY-HESS` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Thermochemistry, state function cycles, and gas mole stoichiometry. |
| `CHEM-THERMO-ENTROPY-SECOND-LAW` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Statistical thermodynamics, entropy microstates, and second-law irreversibility. |
| `CHEM-THERMO-GIBBS-SPONTANEITY` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Free energy optimization, entropy-enthalpy compensation, and equilibrium linkage. |
| `CHEM-EQUIL-LAW-MASS-ACTION` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Dynamic mass action kinetics, pressure equilibria, and quotient directionality. |
| `CHEM-EQUIL-LE-CHATELIER` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **MEDIUM** | Dynamic equilibrium perturbations, Van't Hoff temperature dependence, and industrial optimization. |
| `CHEM-EQUIL-IONIC-PH-OSTWALD` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Ionic equilibrium, Ostwald dilution mathematics, and quadratic boundary testing. |
| `CHEM-EQUIL-BUFFERS-COMMON-ION` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Buffer thermodynamics, Henderson-Hasselbalch equilibrium, and common-ion suppression. |
| `CHEM-EQUIL-SOLUBILITY-PRODUCT` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Heterogeneous equilibria, solubility product algebra, and common ion precipitation. |
| `CHEM-REDOX-BALANCING-CELLS` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Redox stoichiometry, electron conservation, and galvanic thermodynamics. |
| `CHEM-ORGANIC-NOMENCLATURE-ISOMER` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | IUPAC hierarchy, stereochemical rotation barriers, and degrees of unsaturation. |
| `CHEM-ORGANIC-ELECTRONIC-EFFECTS` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Electron displacement dynamics, no-bond resonance, and charge dispersal. |
| `CHEM-ORGANIC-INTERMEDIATES-STABILITY` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Reaction intermediates, hyperconjugative orbital stabilization, and Wagner-Meerwein rearrangements. |
| `CHEM-HYDROCARBONS-ALKENE-ADDITION` | 3 | 3 | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 3 | **HARD** | Electrophilic reaction mechanisms, free-radical chain thermodynamics, and oxidative cleavage. |

