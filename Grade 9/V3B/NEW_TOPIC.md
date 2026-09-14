# New-topic entry contract

This is the canonical starting point for a fresh agent. Do not begin by copying a previous topic's lesson or golden. Use a process example to understand file shape; derive the new topic's intellectual content from the actual source and owner requirements.

## Intake

1. Read this file, the selected subject's CoreContracts.json and ProductionKit/KIT_MANIFEST.json, and the shared role contract for your assigned stage.
2. Preserve the owner's learning purpose, practice mode, scope, support and source requirements. Core2A requires an explicit STARTER, PRACTICE, REVISION or COMPETITION mode. Ask only if the owner has not supplied a materially necessary choice. Do not ask again when the conversation already resolves it.
3. Inventory the available original syllabus, sources, questions, keys and figures. Record absent/partial/conflicted inputs honestly. Normalize question records without losing original files; bind the normalization to its source and a review.
4. Establish stable subtopic/capability IDs and prerequisite homes. Assign 1–3 subtopics per bundle; every required subtopic and source question must be accounted for.
5. Prepare request.json, sources.json and an actor registry. Production actor qualifications require independent review evidence. Synthetic actors and examples are process fixtures and cannot authorize production.

## Execute

Run from any working directory:

```bash
python 'Grade 9/V3B/Physics/ProductionKit/run.py' init \
  --request request.json --sources sources.json --actors actors.json \
  --source-root original-evidence --artifact-root teaching-artifacts --out run
python 'Grade 9/V3B/Shared/run.py' next --run run --bundle B01 --out work-order.json
```

Choose the Mathematics or Chemistry entrypoint for those subjects. The subject entry gate rejects a mismatching request.

The work order names the exact next stage, eligible actor/profile, scope and visible packet set. The execution host must create an actually fresh source-only context for either specialist's blind phase. Do not give the second specialist the first answer before it seals its independent analysis. The CLI does not provide an OS sandbox or automatically spawn models.

An agent submission is an object with work_order (unchanged output), visible_packet_digests (exact permitted list) and payload (the stage artifact). Use submit to validate and accept it. Use advance only when next names a deterministic Governor stage. A blocked stage explains the missing evidence or contract; repair that boundary and retain the accepted work.

```bash
python 'Grade 9/V3B/Shared/run.py' submit --run run --submission submission.json
python 'Grade 9/V3B/Shared/run.py' advance --run run --bundle B01
python 'Grade 9/V3B/Shared/run.py' status --run run
python 'Grade 9/V3B/Shared/run.py' export --run run --out handoff
```

## Role order and deliverables

FIRST_CORE → SECOND_CORE_BLIND → CLAIM_REVIEW → JOIN → ASSIMILATION_PLAN → MANUSCRIPT → CONTENT_REVIEW → TEACHING_RECEIPTS → PRACTICE_CANDIDATES → PRACTICE_ELIGIBILITY → PRACTICE_REVIEW → PUBLICATION_IR.

Core1/Core2 order is evidence-driven. CLAIM_REVIEW checks both packages, closing the gap where the second specialist's additions otherwise escape review. Planning and manuscript realization may share the assigned Core1A instance. Independent reviews and Core2A require fresh instances. Accepted artifacts, sources and packet IDs are reusable; conversation memory is not the only handoff.

## Repair and recovery

The state store records accepted and rejected attempts. Export the handoff before changing execution environments. Repeating the same accepted submission is idempotent; conflicting duplicates and stale work orders fail.

Use invalidate with the first affected stage and an explicit reason. It preserves superseded packets/events and requires a new custody epoch. Check dependent bundles before continuing. A changed original source or runtime policy blocks further acceptance and requires a deliberately rebased run; do not overwrite its recorded binding.

Do not edit run.sqlite3 directly, write acceptance flags manually, invent reviewer evidence, use fixtures as production evidence, or weaken a validator to admit an unsupported topic. A new generated family needs a subject-specific validator and independent test case before it becomes eligible.

## Before handoff

Check source and capability coverage globally; exact explanation and visual realization locally; all hints/solutions against teaching support; answer and provenance closure; owner mode/selection; and coherent versions. Publication IR preserves upstream content. Actual PDF/page/font/overlap/visual checks and human approval remain separately evidenced.

The architecture constrains omissions and detects specified drift. It does not guarantee expert pedagogy simply because a JSON packet is accepted.
