# LEGACY — QUARANTINED. Do not wire new work to this directory.

`Grade 9/V2/Physics/LearningDesign/` belongs to the **pre-assessment-gate** Physics chain
built under issues #221–#233, alongside `../Publication/`. It predates P-A/P-B/P-C and
therefore has no assessment-intake, item-validity or scope-reconciliation authority above
it.

It is kept for repository history and reference only.

## What replaced it in the P-chain

| this directory's role | replacement |
|---|---|
| choosing what to teach | P-F `../StudySynthesis/` — scope from the assessment, treatment from learner evidence |
| instructional design of a lesson | P-G `../CoreAuthoring/` — promoted-pilot PCK, SEE → REALIZE → UNDERSTAND |
| choosing representations | P-H `../Representation/` — teaching-primitive registry driven by P-F obligations |
| transfer and hints | P-I `../Core2Transfer/` — H1 Notice → H2 Model → H3 Start |

## How the quarantine is enforced

`../GENERATION_AUTHORITY_MANIFEST.json` does not declare any file in this directory, and
the P-K cold-start validator rejects any runtime read outside the manifest with
`RUNTIME_READ_OUTSIDE_AUTHORITY_MANIFEST`.
