# Pro 2D icon-by-icon addendum

This addendum is scoped to the Pro 2D icons you called out:

- Keep disabled: `Measure`, `Bend`, `Tee`
- Bring up and running: `Break`, `Connect`, `Stretch`, `Gap Clean`, `Overlap`, `Annotations`, `Radar`

## Verdict

### Keep disabled

| Icon | Current verdict | Why keep disabled |
|---|---|---|
| Measure | Correctly disabled | A professional measure tool needs persistent dimension overlays, chained measurements, snapping history, and report/export. The current viewport has none of that. |
| Bend | Correctly disabled | A piping bend tool must be topology-aware, support ASME/pipe-spec geometry, and split upstream/downstream segments correctly. Current code does not. |
| Tee | Correctly disabled | A tee tool must handle branch ownership, route continuity, node splitting, and canonical branch fitting semantics. Current code does not. |

### Enable now

| Icon | Current problem in ZIP | Addendum fix |
|---|---|---|
| Break | Only a disabled placeholder | Click a segment to split it at the snapped point |
| Connect | Only a disabled placeholder | Click two snapped endpoints to create a bridging segment |
| Stretch | Only a disabled placeholder | Click an endpoint, then click a target point to move that endpoint |
| Gap Clean | Placeholder only | One-click endpoint gap auto-connector |
| Overlap | Placeholder only | One-click collinear overlap merge |
| Annotations / Issues | Planned only | Click to place visible issue markers with note text |
| Radar / Minimap | Planned only | Activate to show minimap overlay; click the minimap to pan |

## What this addendum changes

### 1) Tool contract
`Pro2D_ToolRegistry.mjs`
- leaves `measure`, `bend`, `tee` as `implemented: false`
- marks `break`, `connect`, `stretch`, `gapClean`, `overlapSolver`, `annotations`, `minimap` as `implemented: true`
- adds `annotations` to the left rail
- adds explicit user-facing notes for each active repair tool

### 2) Viewport controller behavior
`Smart2Dcanvas_CanvasViewport.tsx`
- turns the viewport from a static preview into a command surface for the enabled repair tools
- adds wheel zoom + pan drag
- uses snap results for repair commands
- renders annotations
- renders a working radar/minimap overlay

### 3) Scene-state support
`Smart2Dcanvas_GeometryTypes.ts`
- adds `Annotation`

`Smart2Dcanvas_SceneStore.ts`
- adds `annotations`
- adds `addAnnotation`, `updateAnnotation`, `removeAnnotation`
- adds `replaceSceneBundle()` so repair ops can update the scene in one undoable step

### 4) Geometry/repair engine
`Pro2D_RepairOps.mjs`
- `Pro2D_splitSegmentAtPoint()`
- `Pro2D_findNearestEndpoint()`
- `Pro2D_connectEndpoints()`
- `Pro2D_stretchEndpointToPoint()`
- `Pro2D_gapCleanScene()`
- `Pro2D_mergeOverlappingLineSegments()`

## Interaction model after patch

### Break
1. Click `Break`
2. Hover until snap marker is on the target segment
3. Click to split the segment at that point

### Connect
1. Click `Connect`
2. Click first snapped endpoint
3. Click second snapped endpoint
4. A bridging segment is created

### Stretch
1. Click `Stretch`
2. Click the endpoint to stretch
3. Click a second snapped point as the new endpoint location

### Gap Clean
1. Click `Gap Clean`
2. Click once in the viewport
3. Small endpoint gaps are auto-bridged
4. Tool returns to `Select`

### Overlap
1. Click `Overlap`
2. Click once in the viewport
3. Collinear overlapping segments are merged
4. Tool returns to `Select`

### Annotations
1. Click `Issues`
2. Click the viewport
3. Enter note text in the prompt
4. Issue marker and label are rendered

### Radar
1. Click `Radar`
2. A minimap appears top-right
3. Click the minimap to pan the current view

## Why this is the right phase boundary

This addendum deliberately does **not** pretend to solve the full professional versions of Measure / Bend / Tee. It only enables the icons that can be made honest and useful with the current scene model.

That keeps the product trustworthy:
- no fake measure reports
- no fake bend insertion
- no fake tee routing
- no no-op repair icons

## Smoke check

Included test:
- `tests/pro2d_icon_addendum_smoke.mjs`

Verified locally in this environment:
- segment split works
- endpoint connect works
- endpoint stretch works
- gap clean creates bridge segment(s)
- overlap merge reduces overlapping segments

## Files in this ZIP

- `PRO2D_ICON_AUDIT_ADDENDUM.md`
- `js/pro2dcanvas/Pro2D_ToolRegistry.mjs`
- `js/pro2dcanvas/Pro2D_RepairOps.mjs`
- `js/smart2dcanvas/Smart2Dcanvas_GeometryTypes.ts`
- `js/smart2dcanvas/Smart2Dcanvas_SceneStore.ts`
- `js/smart2dcanvas/Smart2Dcanvas_CanvasViewport.tsx`
- `tests/pro2d_icon_addendum_smoke.mjs`

## Follow-on items not included here

These are still the next phase after this addendum:
- persistent measurement overlays and dimension reports
- topology-correct bend insertion
- topology-correct tee/olet insertion
- canonical doc persistence for annotations
- route-aware repair audit logs in the debug dock
