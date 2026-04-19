# Insight remaining gaps patch — reasoning

This patch targets the **remaining implementation gaps** in `NWv-7-PG-jules...zip` after the core Insight engine had already landed.

## Why this patch exists

The earlier source-level audit found that the engine was mostly present, but the app-facing implementation still had four major problems:

1. `newsFetcher.js` accepted a `slot` argument but effectively ignored it, returning the same latest-news feed for every snapshot window.
2. `newsFetcher.js` also assigned fake "now" timestamps, which broke snapshot presence / momentum scoring.
3. `InsightPage.jsx` still rendered a partial parent list and did not resolve children through `storiesById`.
4. `embeddingsAdapter.js` and `nlpAdapter.js` were still too weak for reliable clustering / tree quality.

## What this patch changes

### 1. `src/services/newsService.js`
Adds `publishedAt` to the mapped article objects so downstream consumers can preserve source timestamps instead of relying only on `time`.

### 2. `src/adapters/newsFetcher.js`
Replaces the placeholder fetcher with a slot-aware fetcher that:
- uses different queries per slot
- keeps real timestamps when available
- falls back to slot midpoint only when needed
- maps source names into more stable `sourceGroup` values
- filters stories to the intended age window for each slot
- deduplicates by `url + title`

### 3. `src/adapters/insightFetcher.js`
Adds a cleaner integration layer:
- keeps `slotFetcher`
- adds `fetchAndProcessInsights()`
- adds `refreshInsightsIncrementally()`

This moves the page away from calling the engine directly.

### 4. `src/adapters/embeddingsAdapter.js`
Replaces the near-zero 384-dim stub with:
- 768-dim deterministic fallback embeddings
- optional Gemini embedding path when a browser env key is present
- memoized results

### 5. `src/adapters/nlpAdapter.js`
Strengthens NLP extraction to produce the entity shape the engine expects:
- `people`
- `orgs`
- `places`
- `products`
- `symbols`

Also improves:
- verbs
- numeric fact extraction
- keywords

### 6. `src/pages/InsightPage.jsx`
Rewrites the page integration so it now:
- uses `fetchAndProcessInsights()`
- renders real parent cards
- resolves child stories through `storiesById`
- shows snapshot dots
- shows hidden duplicate count
- shows weak-tree / rising badges
- performs incremental refresh through the adapter layer

## What this patch does **not** do

- It does **not** rewrite the Insight engine.
- It does **not** change clustering/ranking/tree core behavior directly.
- It does **not** add a Node-based smoke test script, because the current repo imports `src/insight/src/index.ts` directly from JS modules and a plain Node smoke script would require a TS-aware runtime.

## Verification performed

This patch was applied to the uploaded `NWv-7-PG-jules-nwv7-phase-3-6-completion-18240861467690822217.zip` working copy and a production build was run successfully with:

```bash
npm ci
npm run build
```

Build result: **pass**.

## Recommended next checks in the real repo

1. Apply the patch
2. Run `npm run build`
3. Open `/insight`
4. Verify:
   - max 5 parent stories
   - children render with titles/sources, not raw IDs
   - snapshot dots vary by slot
   - weak/rising badges surface when applicable
5. Add a browser-based Playwright smoke for the Insight route
