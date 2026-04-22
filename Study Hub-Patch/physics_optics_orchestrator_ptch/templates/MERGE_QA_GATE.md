# Merge + QA Gate

## Hard gates
- All page ids resolve to actual page files
- All related/prerequisite page refs resolve
- No broken question-set refs
- No duplicate page ids
- No generic filler sections like:
  - "builds strong foundation"
  - "helps students understand better"
  unless followed by concrete teaching content

## Content gate
Each difficult subtopic must have:
- helper note
- misconception note
- recap
- at least one rescue resource

## Question gate
- 100+ total questions
- at least these categories where relevant:
  - MCQ
  - reasoning
  - assertion-reason
  - short answer
  - application
  - diagram/numerical
  - remediation
- explanations must teach, not merely restate the answer

## Output gate
Final pack must contain:
- topic.json
- pages/*.json
- question-library.json
- assets-manifest.json
- resource-links.md
- QA_REPORT.md
