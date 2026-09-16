# Adoption from Physics PR350

Pinned head: f2f22f0cea1c31ebf09da10241db8be0fde39789. Source PR remains draft and read-only.

| Source anchor under Grade 9/V2/Physics/Blueprint | Adopted | V3B treatment |
|---|---|---|
| PHYSICS_TECHNICAL_ENGINEERING_GATES_V2.md | Domain requirements precede CCU and authoring | Owner-visible topic setup and separate structural/subject/material/release states |
| engine/validate_engineering_gates_v2.py | Stable codes, canonical obligations, source-held rule, cross references | Manifest-driven extension baseline; cycle detection; scoped relation bindings; exact version checks |
| engine/validate_technical_gate_binding.py | Computed prerequisite closure equals declared closure | Unknown, held and cyclic prerequisites remain visible; external prerequisites require explicit records |
| SELF_HELP_ARCHITECTURE_V9.md | Deterministic invariants separate from engineering heuristics | Similarity only opens review; no score alone grants or denies pedagogical validity |
| policy/content-custody-coverage-unit.v2.json | Per-Core dispositions, question/source/answer closure, purposeful reuse | Universal prompt closure, original-number retention, all required assets resolved to actual objects |
| policy/calibration-audit-layer.v1.json | ENGINEERING/CALIBRATING/VALIDATED, held-out evaluation | Current difficulty/similarity/fit remain ENGINEERING |
| SELF_HELP_ARCHITECTURE_V5.md and later TTU grammar | Setup/representation/relation/working/result/check | Concrete energy-flow and p-V specimens; no decorative-box substitute |

## Deliberate differences

- Existing PR350 EXPECTED obligations are hard-coded for 15 known gates. New IDs receive generic checks unless further expectations are added. V3B makes the required content a separately versioned baseline so adding Thermodynamics is a data/authority change with focused falsifiers, not permission to accept any nonempty new gate.
- Parent closure traversal avoids recursion loops with a seen set but does not establish acyclicity. V3B explicitly rejects a prerequisite cycle.
- Parent representation checks accept any known relation in the registry. V3B requires relation ownership within the gate's prerequisite closure.
- Non-Physics prerequisite strings in the parent need further explicit custody for reusable cross-domain work. V3B records external requirements rather than assuming any arbitrary prefix is satisfied.
- Source citations and a correctly shaped gate do not establish expert review. V3B never promotes STRUCTURE_CHECKED to SUBJECT_APPROVED automatically.
- Exact repeated numeric data can serve conceptual contrast as well as fading. V3B requires a documented instructional transformation; it does not ban identical numbers while accepting the same solution with cosmetically changed numbers.
- Similarity: retain parent 5-shingle Jaccard 0.65/0.80/0.90 as candidate/review/high-review and add 0.80 containment for copied excerpts. Scores are provisional triage. These are not interchangeable metrics.
- Core1B shares the owner's bucket badge and approximate 10/20/30 capacity planning. It covers fragile reasoning and misconceptions without duplicating Core1A page-for-page. No fixed minimum or padding.
- Printable self-tutoring is the baseline. Parent live-response Core1B/2B behavior is an optional adapter, not a prerequisite for using a printed B product.
- Research depth is an explicit overlay, never a hidden expansion of exam scope.

## Reading and validation limits

The engineering documents, real gate/binding validators and selected V9 policies were read at the pinned head. The entire 321-file PR was not reviewed and its Python tests were not rerun in this environment. No claim of complete PR review, current CI reproduction or human pedagogy approval is made.

This folder does not copy the parent registry as a second independent authority. Existing Vectors/Newtonian/M2D gates remain pinned upstream references for future imports. The executable local registry proves extension for the specified Thermodynamics and Gravity gates only.
