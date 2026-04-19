# Student Phase Patch Test & Benchmark Report

## Phase 1
Commands run:
- `npm install`
- `npm run test`
- `npm run build`
- `npm run benchmark:student`

Results:
- tests: **6 files passed**
- build: **passed**
- benchmark (mocked topic of 60 pages × 12 questions):
  - question attempts: **720**
  - revision queue entries: **72**
  - completion: **100%**
  - elapsed: **227.8 ms**

## Phase 2
Commands run:
- `npm install`
- `npm run test`
- `npm run build`
- `npm run benchmark:student`
- `npm run benchmark:revision`

Results:
- tests: **7 files passed**
- build: **passed**
- benchmark student:
  - question attempts: **720**
  - revision queue entries: **72**
  - elapsed: **226.89 ms**
- benchmark revision (400 mocked pages):
  - revision cards selected: **126**
  - elapsed: **0.29 ms**

## Phase 3
Commands run:
- `npm install`
- `npm run test`
- `npm run build`
- `npm run benchmark:student`
- `npm run benchmark:revision`
- `npm run benchmark:exam`

Results:
- tests: **8 files passed**
- build: **passed**
- benchmark student:
  - question attempts: **720**
  - revision queue entries: **72**
  - elapsed: **231.5 ms**
- benchmark revision:
  - revision cards selected: **126**
  - elapsed: **0.30 ms**
- benchmark exam (30 mocked pages × 15 questions, tagged filter):
  - selected exam questions: **90**
  - elapsed: **0.056 ms**
