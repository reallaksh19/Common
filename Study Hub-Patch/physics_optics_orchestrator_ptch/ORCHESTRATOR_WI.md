# Physics Optics Orchestrator WI

## Goal
Produce a **Study-Hub-ready Physics Optics upload set** by coordinating three agents:
- **A1**: Structure / Pack Engineer
- **A2**: Lesson Writer
- **A3**: Question Bank Specialist

The final deliverable must be a clean merged topic pack for:

**Subject:** Physics  
**Class:** 10  
**Topic:** Light — Reflection and Plane Mirror Systems

## Scope
- Rectilinear Propagation of Light
- Reflection of Light
- Regular and Irregular Reflection
- Laws of Reflection
- Deviation on Reflection
- Rotation of Plane Mirror / Turn of Reflected Ray
- Image Formation in a Plane Mirror
- Object Distance and Image Distance

## Orchestrator responsibilities
1. Send the correct WI to A1, A2, and A3.
2. Enforce the output contract for each agent.
3. Reject weak/generic outputs before merge.
4. Normalize IDs, slugs, question-set names, and concept tags.
5. Merge lesson content + structure + questions into one clean app-ready topic.
6. Produce a final upload set and QA report.

## Workflow

### Step 1 — Run A1
Collect:
- `output/topic.json`
- `output/assets-manifest.json`
- `output/question-set-map.json`
- `output/schema-notes.md`
- `output/pages/*.json`

Acceptance:
- Stable ids/slugs
- Logically sequenced pages
- Question bundles defined
- Support hooks included for difficult concepts

### Step 2 — Run A2
Collect:
- `output/lesson-pack.md`
- `output/resource-links.md`
- `output/asset-briefs.md`
- `output/recap-and-helper-notes.md`

Acceptance:
- Enough depth for ~1 hour learning
- No generic filler
- Strong misconceptions/helper notes
- Resource links curated and useful

### Step 3 — Run A3
Collect:
- `output/question-library.json`
- `output/topic_question_map.json`
- `output/bundle_map.json`
- `output/qa_report.md`

Acceptance:
- 100+ questions
- Explanations and support hints are useful
- Balanced difficulty/categories
- Rescue/remediation questions included

### Step 4 — Normalize
Use the ID and slug policy from A1 as the source of truth unless A1 is clearly broken.
Normalize:
- `topicId`
- `pageId`
- `slug`
- `questionSetId`
- `conceptTags`
- `assetId`

### Step 5 — Merge
Create final:
- `topic.json`
- `pages/*.json`
- `question-library.json`
- `assets-manifest.json`
- `resource-links.md`
- `MERGE_SUMMARY.md`

Merging rules:
- A1 defines the page shell and page order
- A2 provides the page prose, helpers, recap, and resource intent
- A3 provides the question bank and question bundle mapping
- Weak/generic content must be rewritten or dropped
- Empty placeholders must be removed or replaced

### Step 6 — Build final upload set
Expected final structure:

```text
Physics/
  optics/
    topic.json
    pages/
      *.json
    assets/
      *.svg / *.png / *.jpg / *.pdf
    assets-manifest.json
    question-library.json
    resource-links.md
```

Optional:
- `content-pack.json` if your Study Hub branch supports pack import

### Step 7 — QA gate
The output is accepted only if:

#### Structure
- All page refs resolve
- Slugs and file names are stable
- No duplicate concept tags unless intentional
- All related/prerequisite refs resolve

#### Content
- At least ~60 min real learning value
- Beginner-friendly
- Exam-friendly
- No obvious generic filler
- Misconceptions + helper notes included

#### Questions
- 100+ total
- No junk repetition
- Difficulty spread exists
- Category spread exists
- Rescue questions exist for hard topics

#### Assets/Resources
- Asset placeholders or actual assets are listed consistently
- Resource links are useful and topic-matched
- Difficult topics have at least one alternate explanation resource

### Step 8 — Upload guidance
Best upload path:
- Copy `Physics/optics/` into the Study Hub content folder
- Verify it appears in topic discovery
- Verify page load, helper rendering, and question rendering

## Reject conditions
Reject the run if:
- A1 IDs are unstable or inconsistent
- A2 is mostly generic filler
- A3 question bank is low-value or repetitive
- The final merged pack still contains broken refs
- The pack cannot be loaded into Study Hub without manual repair

## Final deliverables
- `merged_physics_optics_upload_set.zip`
- `MERGE_SUMMARY.md`
- `QA_REPORT.md`
- `UPLOAD_STEPS.md`
