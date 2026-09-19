# V3B Physics runtime integration map

Current source comparison: PR #350 at `909326ba1fc3cc1b0754b0c37836694f94a91275`. Implementation base: PR #364 at `d0a756d9ab6cf57aca3eb94fe16f1ee2dbdc3e01`. No V2 files are imported or changed by this host.

## Implemented production path

```text
Physics/ProductionKit/run.py publish
  -> publication_host.inputs: separate baseline, source bytes, required products/objects
  -> publication_host.science: existing Physics validator + candidate comparison
  -> publication_host.figures: quantitative source-bound vector/graph SVG
  -> publication_host.compose: actual A/B HTML, answer sections, source links
  -> publication_host.host/storage: immutable directory + portable input/code copy
  -> publication_host.audit: read exported numbers, objects, files and evidence back
  -> OWNER_BOARD.html + evidence.json + manifest.json
```

`verify-publication` rechecks an existing artifact against an explicitly supplied expected input-basis digest and the current runtime. A changed source, baseline, runtime, object, answer, figure or status receipt cannot silently retain its earlier acceptance. Publish to a new directory for every revision; this command never overwrites an old publication.

This is a real composition and artifact-evidence consumer. It accepts externally authored products; it does not generate teaching with a model, validate source extraction by itself, or implement the entire six-Core authoring state machine. All outputs remain review previews. The existing shared `init/next/submit/advance/status/export/invalidate` commands still execute the earlier four-Core runtime unchanged.

## Adoption from the current parent Physics blueprint

| Parent implementation inspected | Adopted boundary | V3B treatment |
|---|---|---|
| `Blueprint/engine/compile_publication_ir.py` | Upstream semantic authority; lossless publication | Separate frozen sources/baseline and authored plan; composition cannot invent source questions |
| `Core1B/engine/core1b_runtime.py` | Observed learner evidence is distinct from configured readiness | No mastery inferred from percentages, routing or publication; study products remain independent of knowledge percentage |
| `Representation/engine/physics_2d_primitive_renderer.py` | Generic primitive composition; explicit schematic-only status | Do not adopt schematic coordinate defaults as quantitative proof; new SVG instances use source-bound values and equal vector scales |
| `Blueprint/policy/technical-density-and-figure-contract.v1.json` | Technical depth is not prose length or diagram count | Retained as academic review obligations, not replaced by renderer success |
| Existing V3B `Shared/v3b/answers.py` and Physics `validator.py` | Physics calculation belongs to its subject adapter | Reuse `validator.recompute`; source atom bindings supply inputs and exported numeric spans supply candidates |
| Existing V3B `Shared/v3b/publication.py` | Composition-only IR and no machine release authority | Preserve legacy code; expose new A/B publication through the Physics-owned entry point |

## What is enforced, and what is not

| Blueprint rules | Implemented observation | Remaining limit |
|---|---|---|
| SRC-01 / COV-01 | Exact source-file digests, complete declared atom accounting, required Core/object-kind coverage, exported object closure | Source extraction and meaningful realization require independent review; an ID link is not a semantic proof |
| SEM-01 | Original MathML retained; tracked transformations permitted as review drafts; meanings/symbols/conditions and source-bound supported numerical evaluator inputs required | Free prose, derivation validity and general equations need academic review |
| ANS-01 / ANS-02 | Declared questions, original numbers/stems/subparts/options/conditions, answer bodies and steps; actual numeric result spans compared | Embedded prose prompts and explanatory correctness need review; only four scalar evaluator families supported |
| FIG-01 / FIG-02 | Source-bound values/units, compatible per-object atom refs, quantitative vector scale, graph range/domain, exact exported SVG identity | Scientific choice of model/frame/variable mapping and final-size visual suitability need review |
| REUSE-01 / TRANSFER-01 | All declared question pairs compared for source identity/declared family; suspicious fresh-transfer claims exposed | Family labels can be wrong; full semantic, lexical and diagram-family adjudication remains pending |
| FIT-01 / FIT-02 | Study/practice separation; practice purpose; knowledge provenance fields or waiver reference; explicit design preview | Waiver authenticity, calibration, subtopic mastery and measured fit are not established by these fields |
| LAYOUT-01 | Responsive HTML, native MathML, separated answers, compact vector canvas and explicitly labelled graph range | Browser/full-page print review NOT_RUN; standalone SVG inspection is narrower evidence |
| RELAY-01 | Sources, inputs, code and relevant policy copied; relocated packet can regenerate identical HTML | This is process recovery, not independent-agent understanding or full authoring recovery |
| RELEASE-01 | No release-authority input; forged PASS projection, stale bytes and missing manifest members rejected | No authenticated reviewer/owner approval service; learner release remains false |
| DEP-01 / CORE-01 / EXT-01 | Existing blueprint remains controlling | Academic inference/Core differentiation and transitive authoring-extension integration are not implemented here |

The new command does not accept raw scanned figures as if they had been understood. Unrecognized original-question fields, including an unadapted original figure, are held with `SOURCE_QUESTION_FIELDS_UNSUPPORTED`. Extend the source adapter losslessly before accepting such a source; never delete the field to make it pass.

## Numerical and publication limits

Supported numeric result families are `SPEED_FROM_COMPONENTS`, `CONSTANT_ACCELERATION_VELOCITY`, `CONSTANT_ACCELERATION_INITIAL_VELOCITY` and `CONSTANT_ACCELERATION_EVENT_TIME`. Values use the existing SI conventions and 1e-9 relative/absolute candidate comparison. Equivalent numeric formatting is accepted. Automatic unit conversion and symbolic-equivalence inference are not added here; recorded equation adaptations can be scientifically reviewed. Other numerical families can appear as marked review drafts with oracle NONE; their scientific learner-ready acceptance remains held. The host checks transcription only for these candidates.

The scalar result field is compared against the existing subject evaluator; this is not an independent proof of every sentence of the solution. Tests include separate arithmetic/sign/geometry expectations, but they do not grant subject-wide numerical qualification. The original-source/model selection must still be reviewed.

The expected basis digest must come from the accepted work packet or another trusted record. Recomputing it from changed inputs and presenting it as old approval defeats source authority; this host never authenticates owner identity and never authorizes release. Runtime snapshots are command dependencies, not a new source of Physics truth.

## Next integration stage

Connect accepted subtopic authoring packets and gate baselines to this publication input format, with no parallel hand-maintained lesson source. Implement independent academic evidence acceptance, complete example-exposure analysis and transitive extension invalidation in the real state owner. Then run full-medium inspection and qualify additional scientific families. Do not claim that this bounded publication layer completes the full architecture.

## Research flexibility update

Read [research freedom and minimum criteria](../Blueprint/V3B-Research-and-Minimum-Criteria.md). Exploration is not gated by an approved baseline. Candidate mathematical adaptations and unsupported numerical methods can proceed in review drafts with explicit pending scientific acceptance. A/B hints have no fixed count. Original-source fidelity, required coverage, answer closure and existing qualified numerical checks remain enforced. Similarity flags trigger triage; they are not automatic duplication convictions. Full research-promotion scheduling and authoring-state invalidation remain pending integration, rather than constraints on what agents may search.
