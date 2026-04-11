# Comprehensive Audit Plan and Gap Analysis

## Scope audited
Bundle inspected:
- `GLB_Viewer_Editor/`
- `CRF_with_GLB_viewer/`
- original work instruction in `1.WI.md`

This audit is based on direct code inspection and build verification, not generic recommendations.

---

## Executive findings

### P0 blockers
1. **`GLB_Viewer_Editor` does not build**.
   - `src/core/app.js` imports:
     - `../js/pcf2glb/pro-editor/ui/ProGlbEditorPanel.js`
     - `../js/pcf2glb/pro2-editor/ui/PRO2EDITOR_Panel.js`
   - Neither folder exists in this ZIP.
   - Result: Vite build fails before runtime.

2. **`CRF_with_GLB_viewer` does not build**.
   - `src/js/pcf2glb/glb/exportSceneToGLB.js` imports `gltf-exporter`.
   - That package is not present and is not the correct Three.js exporter import path.
   - Result: Rollup import resolution fails.

3. **PRO2 Editor is only referenced, not implemented**.
   - The original work instruction asked for a cloned second-generation editor.
   - Current bundle contains only the tab registration/import, with no `pro2-editor` source tree.

### P1 high-impact defects
4. **Advanced viewer export path is broken**.
   - `AdvancedGlbViewerPanel.js` calls `viewerApp.getSceneIndex()` during PCFX export.
   - `createViewerApp()` does not expose `getSceneIndex()`.
   - So export is functionally dead even if the scene loads.

5. **Advanced viewer leaks object URLs and panel runtime**.
   - `URL.createObjectURL()` is used on load.
   - No `destroy()` lifecycle is returned from the panel.
   - No revoke occurs on tab switch.

6. **Geometry tab has visible toolbar controls with missing click handlers**.
   - `#btn-fit-sel` exists but no click listener is wired.
   - `#btn-fly` exists but no click listener is wired.
   - This creates false affordances and breaks UX trust.

7. **Tab lifecycle cleanup is missing in both apps**.
   - Tab router calls `tab.render(content)` only.
   - Outgoing tab cleanup is not called.
   - Renderers, object URLs, event listeners, debug overlays, and WebGL resources can leak.

### P2 structural quality issues
8. **Geometry tab is visually and functionally sub-standard**.
   - crowded single-row toolbar
   - weak status model
   - brittle use of private renderer methods (`_clearSelection`)
   - no responsive collapse strategy
   - no professional docking or inspection workflow

9. **Debug UX is flat and low-signal**.
   - Advanced debug is just a raw log box.
   - No channels, severity filters, counters, timestamps, or export.

10. **Build warnings show poor asset/module hygiene**.
   - stylesheets referenced in a way Vite cannot resolve cleanly at build time
   - oversized chunks in both patched builds, indicating poor code-splitting strategy

---

## Build verification

### Original state
- `GLB_Viewer_Editor`: **build failed** due to missing Pro/PRO2 imports.
- `CRF_with_GLB_viewer`: **build failed** due to unresolved `gltf-exporter` import.

### After the attached high-ROI patch
- `GLB_Viewer_Editor`: **build passed**.
- `CRF_with_GLB_viewer`: **build passed**.

---

## Original work-instruction gap analysis for GLB2Editor

The original WI required a professional GLB viewer/editor architecture with staged delivery. The current bundle only partially reflects that intent.

### Requirement vs current reality

| WI expectation | Current bundle status | Gap |
|---|---|---|
| Pro GLB tab integrated after Advanced GLB | `pro-glb` referenced only in `GLB_Viewer_Editor` | source missing entirely |
| PRO2 editor cloned as a separate tab | `pro2-glb` referenced only | no implementation folder exists |
| destroy lifecycle on tab switch | not implemented | memory/runtime leak risk |
| Advanced viewer + professional editor coexist | not true in buildable state | app fails before boot |
| direct PCF → professional viewer path | not implemented in Advanced viewer | only PCFX import exists |
| property panel evolution | not present for Pro/PRO2 | source missing |
| structured debug console | not implemented | current debug is flat text only |
| measurement tool | absent in visible shipped code | no working PRO2 tool layer |
| screenshots / phased proof | artifacts exist in root, but code tree does not match promised implementation | delivery mismatch |

### Conclusion on GLB2Editor
The current GLB2Editor state is **placeholder registration, not a delivered feature**. It should be treated as **not implemented** rather than “partially working”. The highest-ROI immediate fix is to either:
1. add the missing `pro-editor/` and `pro2-editor/` source trees, or
2. replace the broken imports with explicit fallback tabs that say the feature is not present.

The attached patch implements option 2 so the app becomes buildable and the gap is explicit.

---

## Tool icon functionality audit

## 1) Geometry tab (`src/tabs/geometry-tab.js`)

| Control | Present in UI | Wired | Runtime target | Status |
|---|---:|---:|---|---|
| Select | yes | yes | `setNavMode('select')` | OK |
| Orbit | yes | yes | `setNavMode('orbit')` | OK |
| Plan | yes | yes | `setNavMode('plan')` | OK |
| Rotate Y | yes | yes | `setNavMode('rotateY')` | OK |
| Rotate Z | yes | yes | `setNavMode('rotateZ')` | OK |
| Pan | yes | yes | `setNavMode('pan')` | OK |
| Fit All | yes | yes | `_renderer.resetView()` | OK |
| **Fit Selection** | yes | **no** | none | **BROKEN** |
| Projection | yes | yes | `_renderer.toggleProjection()` | OK |
| Section | yes | indirectly | renderer binds button internally | weak but works |
| **Fly icon** | yes | **no** | none | **BROKEN** |
| Settings | yes | yes | settings drawer | OK |
| Display All | yes | yes | `_renderer._clearSelection()` + `resetView()` | brittle/private API |
| Legend select | yes | yes | emits `legend-changed` | OK |
| Heat map select | yes | yes | emits `legend-changed` | OK |
| Show Labels | yes | yes | emits viewer settings change | OK |
| Show Support Labels | yes | yes | emits viewer settings change | OK |
| Label Mode | yes | yes | emits viewer settings change | OK |

### Geometry tab verdict
- two visible buttons are dead (`Fit Selection`, `Fly`)
- one action uses private internal API (`_clearSelection`)
- toolbar is crowded and ungrouped
- panel system is not professional enough for a geometry-first workflow

## 2) Advanced GLB Viewer (`src/js/pcf2glb/ui/AdvancedGlbViewerPanel.js`)

| Control | Present | Wired | Status |
|---|---:|---:|---|
| Load File | yes | yes | OK |
| Import from PCFX | yes | yes | OK for PCFX only |
| Export to PCFX | yes | **broken end-to-end** | viewer app does not expose `getSceneIndex()` |
| Debug toggle | yes | yes | basic only |
| Close debug | yes | yes | OK |
| Property close | yes | yes | OK |
| Toolbar color-by | yes | yes | OK |
| ISO/TOP/FRONT/SIDE | yes | yes | OK |
| Fit All | yes | yes | OK |
| Section toggle | yes | yes | OK |
| Direct PCF import | **no** | no | WI gap |
| Cleanup on tab switch | **no** | no | leak risk |

## 3) Simple GLB Exporter (`src/js/pcf2glb/ui/PcfGlbExporterPanel.js`)

| Control | Present | Wired | Status |
|---|---:|---:|---|
| file input | yes | yes | OK |
| export pipeline | yes | yes | blocked by bad GLTFExporter import in original |
| color-by | yes | yes | OK |
| ISO/TOP/FRONT | yes | yes | OK |
| heatmap legend | yes | yes | OK |
| property panel close | yes | yes | OK |

### Exporter verdict
The UI is mostly wired, but the build is blocked by the wrong exporter import. That makes the entire tool unusable in packaged form.

---

## Comprehensive audit plan

## Stage A — Build and bootstrap
1. `npm install && npm run build` for each app:
   - `GLB_Viewer_Editor`
   - `CRF_with_GLB_viewer`
2. fail test if any import cannot be resolved
3. fail test if tab router references missing panel modules
4. record Vite warnings separately from hard failures

## Stage B — Tab routing and lifecycle
For every visible tab:
- render tab
- switch away
- verify cleanup path called
- verify no stale canvas/debug overlay remains
- verify no object URL remains retained
- verify no duplicated keyboard listeners after 5 switch cycles

## Stage C — Tool/button audit
For each toolbar button/icon:
- verify DOM control exists
- verify click handler exists
- verify handler calls public API
- verify expected state mutation occurs
- verify disabled/enabled state matches readiness
- verify keyboard shortcut exists where title promises one

### Geometry tab exact checklist
- select/orbit/plan/rotateY/rotateZ/pan buttons
- fit all
- fit selection
- projection toggle
- section toggle
- fly toggle
- settings drawer
- legend mode
- heatmap mode
- labels toggle
- support labels toggle
- label mode
- display all
- side tabs: props / restraints / legend

### Advanced GLB exact checklist
- file load
- PCFX import
- PCFX export
- debug open/close
- property close
- color-by
- iso/top/front/side
- fit all
- section clip
- scene export readiness state

### Exporter exact checklist
- PCF file path
- parsed state path
- GLB export generation
- GLB preview render
- view presets
- color-by / heatmap
- property panel selection

## Stage D — Layout/UI audit
Check all of the following at 1280px, 1024px, and 768px widths:
- toolbar overflow / clipping
- canvas remaining visible under side panes
- side panel width stability
- debug panel overlap
- property panel overlap
- label readability on dark and light themes
- tab bar readability
- disabled-state affordance

## Stage E — Debugging surface audit
For each viewer surface verify:
- log timestamps present or absent
- severity differentiation
- category / channel differentiation
- exportability
- selection and camera events logged or not
- import/export errors surfaced to user without blocking alerts where avoidable

## Stage F — Geometry quality audit
- frame selection path
- projection consistency
- section box clipping correctness
- fly mode camera consistency
- selection highlight / property sync
- support symbol and label readability
- cleanup after repeated rebuilds
- public API vs private method usage

---

## High-ROI improvement recommendations

## A. GLB2Editor / Pro editor family
### Highest ROI
1. **Stop shipping broken imports**
   - either include `pro-editor` / `pro2-editor`
   - or ship guarded fallback tabs
2. **Make tab lifecycle real**
   - support `destroy()` / `dispose()` from renderers
3. **Separate “referenced” from “implemented”**
   - if PRO2 is still under development, say so in UI instead of breaking build

### Reasoning
These changes unblock packaging immediately and prevent the project from looking complete while being non-runnable.

## B. Advanced viewer
### Highest ROI
1. add **direct PCF import** using existing parse/normalize/buildExportScene pipeline
2. expose `getSceneIndex()` from viewer app so PCFX export works
3. return `destroy()` and revoke object URLs
4. replace `alert()`-driven error UX with inline error surface in the left panel

### Reasoning
The codebase already contains the pieces. This is low-code, high-value wiring rather than new architecture.

## C. Geometry tab
### Highest ROI
1. wire `Fit Selection`
2. wire `Fly` icon
3. replace private `_clearSelection()` usage with public renderer API
4. split toolbar into grouped clusters:
   - navigation
   - framing
   - display
   - sectioning
   - settings
5. add compact responsive overflow for narrow widths
6. move status/version into a real footer band with camera/projection/selection info

### Reasoning
This tab is currently the weakest UX surface relative to how central it is supposed to be.

## D. Basic / CRF viewer app
### Highest ROI
1. fix exporter import path
2. add tab destroy lifecycle
3. code-split heavy geometry/viewer modules
4. consolidate repeated viewer utilities shared with GLB_Viewer_Editor

### Reasoning
CRF is closer to working than GLB_Viewer_Editor. A few structural fixes make it stable enough to iterate.

---

## Attached patch summary
The attached patch focuses on the quickest fixes that unlock the codebase:

1. **build unblockers**
   - fix `GLTFExporter` import in both apps
   - replace missing Pro/PRO2 imports with guarded fallback tabs in `GLB_Viewer_Editor`

2. **tab lifecycle support**
   - update both app routers to honor `destroy()` / `dispose()` returned from tabs

3. **geometry tab fixes**
   - wire `Fit Selection`
   - wire `Fly` icon
   - expose `fitSelection()` as a public renderer API
   - slightly improve renderer destroy cleanup

4. **advanced viewer fixes**
   - expose `getSceneIndex()` from `createViewerApp`
   - enable direct `.pcf` import in the Advanced viewer
   - add `destroy()` to the panel
   - revoke object URLs on cleanup and reload

---

## Recommended next audit after patch lands
1. Playwright-based tab smoke suite
2. multi-switch memory profile (20 tab swaps)
3. geometry renderer listener leak audit
4. structured debug console implementation
5. PRO2 editor delivery audit only after the actual source tree exists
