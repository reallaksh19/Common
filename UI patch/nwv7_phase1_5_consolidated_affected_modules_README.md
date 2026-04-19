# NWv-7 consolidated patch (phases 1–5, affected modules only)

This patch is a **consolidated diff** between:
- original repo: `NWv-7-11-04-26.zip`
- final integrated repo state: `nwv7_phase5_integrated_code.zip`

## Included files (28)
- src/App.jsx
- src/components/BottomNav.jsx
- src/pages/InsightPage.jsx
- src/pages/MarketPage.jsx
- src/pages/MyPlannerPage.jsx
- src/pages/UpAheadPage.jsx
- src/pages/MorePage.jsx
- src/ui/shared/PageIntroCard.jsx
- src/ui/shared/InlineSegmentTabs.jsx
- src/ui/planner/PlannerSummaryCard.jsx
- src/ui/planner/PlannerDayCard.jsx
- src/ui/upahead/UpAheadHeroCard.jsx
- src/ui/more/MoreLinkCard.jsx
- src/ui/insight/InsightPulseCard.jsx
- src/ui/insight/InsightStatStrip.jsx
- src/ui/insight/InsightExpandedPanel.jsx
- src/ui/insight/InsightRankedCard.jsx
- src/ui/insight/CoverageGrid.jsx
- src/ui/insight/InsightPageView.jsx
- src/ui/market/MarketMoodBanner.jsx
- src/ui/market/IndexGrid.jsx
- src/ui/market/GlobalRail.jsx
- src/ui/market/MoversCard.jsx
- src/ui/market/SectorHeatmap.jsx
- src/ui/market/MacroCard.jsx
- src/ui/market/FlowCard.jsx
- src/ui/market/IpoList.jsx
- src/ui/market/MarketPageView.jsx

## Notes
- This patch includes **only the modules that are actually different** between the original repo and the final phase-5 integrated state.
- It intentionally does **not** include the whole repo.
- Some earlier phase files such as `src/main.jsx`, `src/components/Header.jsx`, and `src/pages/MainPage.jsx` are **not present** here because the final phase-5 ZIP does not differ from the original repo for those files.

## Apply
From the repo root, try:
```bash
git apply nwv7_phase1_5_consolidated_affected_modules.patch
```

If `git apply` is unavailable, you can also try:
```bash
patch -p1 < nwv7_phase1_5_consolidated_affected_modules.patch
```
