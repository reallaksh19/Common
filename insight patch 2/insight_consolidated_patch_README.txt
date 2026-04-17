Consolidated Insight patch for NWv-7-PG

Files changed:
- src/App.jsx
- src/adapters/embeddingsAdapter.js
- src/adapters/insightFetcher.js
- src/adapters/newsFetcher.js
- src/adapters/nlpAdapter.js
- src/pages/InsightPage.jsx
- src/insight/src/cache/cacheManager.ts
- src/insight/src/cluster/cluster.ts
- src/insight/src/dedup/dedup.ts
- src/insight/src/pipeline/pipeline.ts
- src/insight/src/ranking/ranking.ts
- src/insight/src/tree/treeBuilder.ts

Apply from repo root:
  patch -p1 < insight_consolidated.patch

Notes:
- This patch consolidates the uploaded Insight patch archive plus the missing App.jsx import and a full rewrite of src/adapters/insightFetcher.js.
- I did not complete a full build verification in the extracted sandbox copy because the repo dependencies were not installed there.
- The patch is intended for NWv-7-PG-main as uploaded.
