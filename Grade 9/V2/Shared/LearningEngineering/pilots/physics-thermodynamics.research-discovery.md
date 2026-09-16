# Physics Thermodynamics / RESEARCH — discovery and reconciliation record

Status: **PILOT DISCOVERY / NON-RUNTIME / PROMOTION HELD**

Roadmap pilot: `PILOT-PHYSICS-THERMODYNAMICS-RESEARCH`

This note explains the evidence decisions represented in `physics-thermodynamics.research.prototype.json`. It is not an SKP runtime authority, Engineering readiness receipt, learner model, Blueprint input, or publication authorization.

## 1. Current curriculum truth

The curriculum authority selected for base scope is the official CBSE Physics (Code No. 042) curriculum for **Class XI, academic year 2026–27**:

`https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart2/Physics_SecP2_2026-27.pdf`

Unit VIII / Chapter 11 explicitly includes thermal equilibrium and temperature, the zeroth law, heat, work, internal energy, the first and second laws, thermodynamic state variable/equation of state, and isothermal, adiabatic, reversible, irreversible and cyclic processes.

This source is promoted only for `CURRICULUM_AUTHORITY`. It is not used as empirical learner-conception evidence or as a detailed derivation source.

## 2. External assessment is not curriculum authority

The official NTA JEE Main 2026 syllabus contains a Thermodynamics unit covering thermal equilibrium/temperature, the zeroth law, heat/work/internal energy, the first law, isothermal and adiabatic processes, and reversible/irreversible processes:

`https://jeemain.nta.nic.in/document/syllabus-2026/`

That record is promoted only for `EXTERNAL_ASSESSMENT`. Its presence can establish that a demand is relevant to an external examination; it cannot expand, delete, or supersede the current CBSE curriculum binding.

## 3. Subject-truth and derivation references

MIT thermodynamics references are used for disciplinary semantics that the curriculum listing does not fully specify, especially system/state meaning, first-law sign convention, internal energy as a state property, and advanced second-law/irreversibility context:

- `https://ocw.mit.edu/ans7870/16/16.unified/thermoF03/chapter_4.htm`
- `https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/`

These are not Grade XI curriculum authorities. Advanced topics such as entropy formalism, enthalpy, Gibbs free energy or Carnot analysis therefore remain research/adjacent context unless a separate current curriculum or assessment authority promotes them for its own intent.

## 4. Research-depth learner evidence

The pilot records peer-reviewed Physics Education Research evidence because RESEARCH depth requires a stronger literature dossier. It deliberately preserves population limits.

### Internal energy, work and heat transfer

Brundage, Meltzer & Singh (2024), *Physical Review Physics Education Research* 20, 010115:

`https://doi.org/10.1103/PhysRevPhysEducRes.20.010115`

The study used a validated thermodynamics survey across more than 1000 students in 12 introductory and advanced physics classes at four U.S. public higher-education institutions. It reports persistent difficulties involving internal energy, work and heat transfer, including reasoning that ignores work in adiabatic processes.

Disposition: `MISCONCEPTION_EVIDENCE` for research/pedagogy analysis, **not** canonical Grade XI misconception authority.

### Context dependence and p–V reasoning

Brundage, Meltzer & Singh (2025), *Physical Review Physics Education Research* 21, 010127:

`https://doi.org/10.1103/PhysRevPhysEducRes.21.010127`

The study examines problem-property dependence for concepts including state variables versus path-dependent heat/work and signed area under a pressure-volume curve.

Disposition: population-limited `MISCONCEPTION_EVIDENCE` plus `REPRESENTATION_REFERENCE` candidate evidence. It does not mandate p–V graphs in every learner artifact.

### Entropy and the second law

Brundage, Meltzer & Singh (2024), *Physical Review Physics Education Research* 20, 020110:

`https://doi.org/10.1103/PhysRevPhysEducRes.20.020110`

The study reports a widespread unproductive tendency among introductory university students to reason as if entropy were conserved.

Disposition: population-limited research evidence. Because the current CBSE chapter listing does not explicitly require entropy formalism, the pilot keeps this evidence in the additive RESEARCH layer rather than rewriting the STANDARD curriculum/core claim set.

## 5. STANDARD → RESEARCH invariance

The machine-readable pilot contains a `base_claim_snapshot` whose entries are `depth=STANDARD`. The RESEARCH-only claim list is disjoint and every research claim carries `mutates_base_claims=false`.

Therefore increasing `ENGINEERING_DEPTH` changes evidence obligations and may add literature/applicability detail, but it does not silently alter the confirmed curriculum binding or validated base claims. Any future contradiction or supersession would require an explicit governed mechanism; the planned `research_overlay` module is not yet active.

## 6. Prerequisite and provider boundary

The pilot models two same-subject bridges from earlier Class XI Physics material: work/energy and thermal-properties concepts. It also records a contextual external Mathematics need for graph/area interpretation where p–V reasoning is actually used.

That external prerequisite is **not self-certified**. Two unresolved architecture facts remain:

1. the current shared CrossDomain provider registry points Mathematics to the existing Grade 9 provider root, not a Grade XI authority;
2. the SKP prerequisite contract uses `CAP-*` capability identities while the current CrossDomain provider router uses prefixes such as `MATH-`.

The pilot therefore records this edge with `missing_behavior=UNRESOLVED` and no provider readiness receipt.

## 7. Grade-authority mismatch found by the diversity stress

The currently routed Physics generation manifest explicitly declares `grade: 9`. The official Thermodynamics target is Class XI. Prior to this pilot, AgentTasks resolved subject authority by subject adapter but did not expose task-grade compatibility.

The generic resolver now records:

```text
generation_authority_scope.task_grade
generation_authority_scope.declared_grades
generation_authority_scope.grade_state = MATCH | MISMATCH | UNDECLARED
```

A mismatch permits discovery/reconciliation but holds production/Engineering use of that manifest for the requested grade. This fix contains no Thermodynamics-specific branch.

## 8. Explicit holds

The pilot remains `HELD` because:

- no Grade XI Physics generation authority is currently routed;
- the production SKP→Engineering promotion path is inactive;
- the `research_overlay` module is still PLANNED;
- Grade XI target-population learner-conception evidence is insufficient for canonical misconception promotion;
- the cross-domain identifier/provider seam is unresolved.

These are expected architecture results, not reasons to fabricate readiness or weaken the evidence model.

## 9. Non-claims

This pilot does not claim that:

- the package is a production SKP;
- schema validity establishes semantic correctness;
- university learner research directly represents CBSE Grade XI students;
- JEE Main defines CBSE curriculum scope;
- entropy/Carnot/enthalpy/Gibbs content is current CBSE-required Physics Thermodynamics;
- a Mathematics prerequisite is provider-ready;
- Engineering readiness, consumer permission, publication, or authorized human review has been granted.
