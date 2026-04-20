# Guided Learning Student-Side Plan

Base used: `Study-hub-PG-jules-parent-dashboard-8515523173282237722 (6).zip`

## Goal
Turn the current student experience from a page viewer with quizzes into a guided learning flow with:
- topic entry with progression and prerequisites
- mastery tracking and revision queue
- adaptive help after wrong answers
- mobile help access
- revision mode
- exam drill mode
- AI provider abstraction so support tooling can be swapped later without UI rewrites

## Phase plan

### Phase 1 — Progression and mastery foundation
Scope:
- add `StudyContext` with persisted learner state
- add `learningProgressService`
- route `#/topic/:topicId` to `TopicHome.jsx`
- show completion, mastery, next recommended page, prerequisite locks
- merge page metadata (`estimatedMinutes`, prerequisites, related pages) into loaded page data
- record page open/read and question outcomes
- add mocked tests + benchmark

Files added/changed:
- `src/contexts/StudyContext.jsx`
- `src/services/learningProgressService.js`
- `src/services/learningProgressService.test.js`
- `src/services/jsonContentService.js`
- `src/components/student/TopicHome.jsx`
- `src/components/StudyGuide/index.jsx`
- `src/components/QuizSection/index.jsx`
- `src/Grade8_StudyHub_Complete.jsx`
- `src/index.jsx`
- `scripts/run-tests.mjs`
- `scripts/benchmark-learning.mjs`
- `package.json`

Outcome:
- better topic entry
- topic progression is visible
- mastery starts accumulating from page reads and quiz results

### Phase 2 — Adaptive help and revision mode
Scope:
- add `revisionService`
- add `RevisionMode.jsx`
- add mobile help drawer
- improve support card to include related pages/resources and save-for-revision
- surface attached resources in sidebar/help flow
- add revision benchmark/test

Files added/changed:
- `src/services/revisionService.js`
- `src/services/revisionService.test.js`
- `src/components/student/RevisionMode.jsx`
- `src/components/student/MobileHelpDrawer.jsx`
- `src/components/questions/SupportMaterialCard.jsx`
- `src/components/QuizSection/index.jsx`
- `src/components/StudyGuide/index.jsx`
- `src/components/StudyGuide/RightSidebar.jsx`
- `src/contexts/StudyContext.jsx`
- `src/Grade8_StudyHub_Complete.jsx`
- `scripts/benchmark-revision.mjs`
- `package.json`

Outcome:
- child can revise weak pages in a dedicated mode
- support becomes more actionable
- help is available on mobile

### Phase 3 — Exam drill and AI abstraction
Scope:
- add `ExamMode.jsx`
- add AI provider layer (`mock` + `gemini` provider)
- make sidebar use provider instead of direct Gemini UI coupling
- add exam benchmark/test

Files added/changed:
- `src/ai/aiProvider.js`
- `src/ai/mockProvider.js`
- `src/ai/geminiProvider.js`
- `src/ai/aiProvider.test.js`
- `src/components/student/ExamMode.jsx`
- `src/components/StudyGuide/RightSidebar.jsx`
- `src/Grade8_StudyHub_Complete.jsx`
- `src/components/student/TopicHome.jsx`
- `scripts/benchmark-exam.mjs`
- `package.json`

Outcome:
- exam-drill route exists
- AI support can later move to serverless/Firebase AI Logic without UI churn

## Recommended rollout
1. Apply Phase 1 first and verify student progression.
2. Apply Phase 2 when you want guided revision and mobile help.
3. Apply Phase 3 when you want exam mode and cleaner AI architecture.

## Testing method used
All phases were tested with:
- `npm install`
- `npm run test`
- `npm run build`
- mocked-data benchmarks:
  - `npm run benchmark:student`
  - `npm run benchmark:revision`
  - `npm run benchmark:exam` (phase 3)

## Current limits after phase 3
- parent-side authoring still needs dedicated UI for concept tags, revision summaries, and exam-drill metadata
- attached resources are shown, but not yet deeply adaptive by question type beyond linked IDs
- AI provider abstraction is in place, but only mock/direct Gemini providers are included
