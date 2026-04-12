# Pro 2D DXF Import Patch Notes

This patch adds a real DXF import path to Pro 2D.

## Files

* `js/pro2dcanvas/Pro2D\_DxfAdapter.mjs`
* `js/pro2dcanvas/Pro2D\_RibbonConfig.mjs`
* `js/pro2dcanvas/Pro2D\_AppShell.tsx`
* `tests/pro2d\_dxf\_import\_smoke.mjs`

## What changed

* Added `Import DXF` ribbon action.
* Added hidden file input in `Pro2D\_AppShell.tsx`.
* Added async `onDxfFileChosen()` flow.
* Replaced shallow DXF token reader with a layered importer that:

  * tries external parser libs,
  * falls back to internal parsing,
  * builds scene + canonical state,
  * preserves DXF metadata,
  * returns a structured import report.

## Import scope

### Supported

* LINE
* LWPOLYLINE
* POLYLINE
* SPLINE
* ARC
* POINT
* TEXT / MTEXT
* INSERT
* CIRCLE (heuristic or segmentized)

### Not fully supported

* DIMENSION
* HATCH
* MLEADER
* 3DSOLID / BODY
* perfect round-trip of every block variant

## Integration notes

Recommended default import options:

```js
const imported = await Pro2D\_importDxfToState(text, {
  fileName: file.name,
  documentName: file.name.replace(/\\.dxf$/i, ''),
  defaultBore: 250,
  explodeBlocks: true,
  arcMode: 'fitting',
  circleMode: 'report',
});
```

## Smoke test

Run:

```bash
node tests/pro2d\_dxf\_import\_smoke.mjs
```

