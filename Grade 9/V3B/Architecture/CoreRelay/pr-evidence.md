# Three-PR architecture evidence

Status: SOURCE_INSPECTION. This is bounded architectural context, not a line-by-line PR review, approval, CI audit or production validation.

## Frozen review basis

| PR | Reviewed head | Base branch |
|---|---|---|
| [350 Physics](https://github.com/reallaksh19/Common/pull/350) | c44cc1815308c2b3468f8b33bed1286adacc06ea | v2-physics-upgrade-full-chain-g-to-l |
| [351 Mathematics](https://github.com/reallaksh19/Common/pull/351) | d4b9fe87ba87c8460ec8b9a6481d9c91d7ae7359 | v2-math-upgrade-pck-renderer-mature-gates |
| [362 Chemistry](https://github.com/reallaksh19/Common/pull/362) | 81bdc15598f49fcc1941a6da1d6df0388c56b1a7 | draft/chemistry-ncert-core-workbench |

Physics and Mathematics retained their initially inspected heads. Chemistry advanced from 58c2300b8fbfc8ced5f38f39acf352736db42cd1; relevant sources were re-fetched at the head above. Later updates require a separate evidence refresh.

The review branch starts from main at 805094cc3d208e5a8342c41c2d9d54243d35ebc3. Open follow-ons 359, 360 and 361 were observed for coordination; their implementation is not reviewed here.

## Physics: preserve semantic and question-link granularity

The [runbook](https://github.com/reallaksh19/Common/blob/c44cc1815308c2b3468f8b33bed1286adacc06ea/Grade%209/V2/Physics/Core1A/AGENT_RUNBOOK.md) establishes an SBA sequence with source/question audit, decomposition, hint pre-teaching, problem families, visual audit and durable handoff.

The [SBA04 profile](https://github.com/reallaksh19/Common/blob/c44cc1815308c2b3468f8b33bed1286adacc06ea/Grade%209/V2/Physics/Core1A/registry/physics-core1a-motion-in-a-plane-sba04-20pct-v1.json) contains concrete atoms, prerequisite support, misconception targets and question-specific hint mappings. Its Q14/Q27 dependencies illustrate why one primary question home cannot replace all prerequisite edges.

The [linking specification](https://github.com/reallaksh19/Common/blob/c44cc1815308c2b3468f8b33bed1286adacc06ea/Grade%209/V2/Physics/Core1A/CORE1A_CORE2_LINKING.md) ties return links to concepts/stages. Preserve that granularity in T receipts.

The [SBA schema](https://github.com/reallaksh19/Common/blob/c44cc1815308c2b3468f8b33bed1286adacc06ea/Grade%209/V2/Physics/Core1A/contracts/physics-core1a-subtopic-bucket.schema.json) and [SBA tests](https://github.com/reallaksh19/Common/blob/c44cc1815308c2b3468f8b33bed1286adacc06ea/Grade%209/V2/Physics/Core1A/tests/test_physics_core1a_sba.py) enforce IDs, counts, hint fields and zero-primary skipping. The proposed architecture explicitly differs on the latter: question absence must not decide teaching importance. This is a proposal-level distinction, not a patch in this PR.

The [publication compiler](https://github.com/reallaksh19/Common/blob/c44cc1815308c2b3468f8b33bed1286adacc06ea/Grade%209/V2/Physics/Core1A/engine/build_physics_core1a.py) largely composes already-authored upstream fields into modules. The architecture must identify who authors and checks any missing intellectual bridge before composition.

## Mathematics: preserve bindings while exposing judgment

The [execution contract](https://github.com/reallaksh19/Common/blob/d4b9fe87ba87c8460ec8b9a6481d9c91d7ae7359/Grade%209/V2/Mathematics/LearnerProduct/EXECUTION_CONTRACT.md) separates schema, policy, engine and a concrete reference. It specifies representations, source preservation, staged help and per-question provenance.

The [bucket synthesis engine](https://github.com/reallaksh19/Common/blob/d4b9fe87ba87c8460ec8b9a6481d9c91d7ae7359/Grade%209/V2/Mathematics/Core1A/engine/core1a_bucket_synthesis.py), particularly _validate_binding, _assign_supports and _atoms_for_capability, preserves learner-study bindings, creates bridge homes for shared support, and derives atoms from PCK anchors/reconstruction routes. These are useful seams for a richer relay; their presence alone does not prove a new topic's decomposition sufficient.

The [Core2A policy](https://github.com/reallaksh19/Common/blob/d4b9fe87ba87c8460ec8b9a6481d9c91d7ae7359/Grade%209/V2/Mathematics/LearnerProduct/policies/math-core2a-execution-policy.json) preserves source items and specifies near-transfer/structural-variation slots. The owner's clarified range requires a separate practice brief that can request elementary items and different mixes.

The [canonical runner](https://github.com/reallaksh19/Common/blob/d4b9fe87ba87c8460ec8b9a6481d9c91d7ae7359/Grade%209/V2/Mathematics/LearnerProduct/engine/run_learner_product.py) has an empty STAGE_RUNNERS mapping and rejects normal generation when runners are missing. Contract completeness and executable completeness must remain separate claims.

The [Theory of Equations reference](https://github.com/reallaksh19/Common/blob/d4b9fe87ba87c8460ec8b9a6481d9c91d7ae7359/Grade%209/V2/Mathematics/LearnerProduct/golden/theory-of-equations/EXPECTED_STRUCTURE.json) specifies semantic groups and invariants rather than fixed PDF geometry. Copy the process while independently designing another topic.

## Chemistry: preserve artifact and answer custody

The [execution contract](https://github.com/reallaksh19/Common/blob/81bdc15598f49fcc1941a6da1d6df0388c56b1a7/Grade%209/V2/Chemistry/LearnerProduct/EXECUTION_CONTRACT.md) includes source denominators, integrity classification, atom and representation stages, source/generated practice, answer closure and frozen handoff.

The [manuscript engine](https://github.com/reallaksh19/Common/blob/81bdc15598f49fcc1941a6da1d6df0388c56b1a7/Grade%209/V2/Chemistry/Core1A/engine/build_chemistry_core1a_manuscript.py), teaching_section, projects atoms and representations into teaching sections. A relay must preserve their semantic content and approved interpretation, not only their references.

The [challenge engine](https://github.com/reallaksh19/Common/blob/81bdc15598f49fcc1941a6da1d6df0388c56b1a7/Grade%209/V2/Chemistry/Core2A/engine/build_chemistry_core2a_challenges.py) has governed family recipes and checks. An implementation named independent_validate still needs a stated independence basis; mechanical recomputation, source inspection and expert assessment are different evidence classes.

The [finalizer](https://github.com/reallaksh19/Common/blob/81bdc15598f49fcc1941a6da1d6df0388c56b1a7/Grade%209/V2/Chemistry/LearnerProduct/engine/finalize_chemistry_learner_products.py) binds artifact hashes and answer counts and leaves human gates pending with release_authorized=false. Preserve this distinction in the shared design.

The [small process reference](https://github.com/reallaksh19/Common/blob/81bdc15598f49fcc1941a6da1d6df0388c56b1a7/Grade%209/V2/Chemistry/LearnerProduct/golden/some-basic-concepts/expected-semantic-slice.json) explicitly calls itself synthetic and makes no NCERT production claim. The redox profile was also retrieved as a broader concrete input; it is not a validated full-chapter output in this review.

## Shared architectural implications

1. Keep exact source and learner-policy bindings.
2. Preserve all prerequisite and reasoning dependencies despite unique primary homes.
3. Give Core1A explicit authority to propose teaching elaborations and a route to validate their subject claims.
4. Add the owner practice brief independently of percentage and source-question difficulty.
5. Distinguish intellectual production, deterministic composition, independent assessment and rendered-product checking.
6. Treat stage completion as evidence-backed acceptance rather than presence of fields.
7. Use small concrete references plus withheld new topics to evaluate transfer of the process.

No assertion that all tests in these PRs only check containers is adopted. The inspected tests include useful invariants, and the larger suite was not exhaustively audited or executed. The owner's concern is preserved as an evaluation requirement rather than repeated as an unverified blanket finding.

See [source inventory](source-inventory.json) for retrieved file bindings. Retrieval is not equivalent to full-file review; the decisive inspected anchors are the ones identified above.
