# 2D Apps Technical Audit

## Verified high-level findings

### Pro 2D \[Refer DXF\_IMPORT\_PATCH\_NOTES.MD]

* It exists as a tab/panel inside Pro 2D (`Pro2D\_CoorOpsPanel`) and via import helper `Pro2D\_fromCoord2PcfSnapshot`, but not as a standalone shell/app.
* `Pro2D\_fromCoord2PcfSnapshot()` only reads `safe.parsedRuns\[0]`; remaining runs are ignored.
* `routeToPcf` in `Pro2D\_AppShell` does not generate PCF text. It only recomputes pipeline metrics.

### Smart 2D

* `Smart2Dcanvas\_SceneStore` is strong: typed scene objects, undo/redo, scene load/reset, selection state.
* `Smart2Dcanvas\_SnapEngine.calculateSnap()` uses `useSceneStore.getState()` and computes endpoint/midpoint/intersection/nearest snaps correctly.
* `Smart2Dcanvas\_CanvasViewport` is still a placeholder renderer. It calculates snap only at the fixed point `(300,180)` and does not feed snap into pointer-driven drawing.
* There are no draw/insert interactions for pipe/support/inline tools even though the store supports those object types.

### Build/packaging verification

* `npm ci` required `PUPPETEER\_SKIP\_DOWNLOAD=1` because `puppeteer` attempts a browser download.
* `npm run build` fails because there is no `index.html` entry module in the ZIP. This means the artifact is not independently buildable as delivered.

## App 2 — Coor→PCF

## Architecture assessment

Current state is **embedded operator surface**, not a standalone app.

### Severity-ranked issues

#### P0 — It does not generate PCF text

`routeToPcf` only reruns metrics.

**Patch direction**
Split converter into:

* `Coor2Pcf\_Normalizer.mjs`
* `Coor2Pcf\_Emitter.mjs`
* `Coor2Pcf\_AppShell.tsx`

```js
export function Coor2Pcf\_normalizeSnapshot(snapshot) {
  const safe = Pro2D\_safeCoordSnapshot(snapshot);
  return {
    runs: (safe.parsedRuns || \[]).map((run, idx) => ({
      id: run.id || `run\_${idx + 1}`,
      route: Array.isArray(run.route) ? run.route.map((pt) => ({ x: Number(pt.x) || 0, y: Number(pt.y) || 0, z: Number(pt.z) || 0 })) : \[],
    })),
    supports: (safe.supportPoints || \[]).map((sp, idx) => ({
      id: `support\_${idx + 1}`,
      x: Number(sp.x) || 0,
      y: Number(sp.y) || 0,
      z: Number(sp.z) || 0,
      refNo: sp.refNo || `SUP-${idx + 1}`,
      seqNo: sp.seqNo || idx + 1,
      name: sp.name || 'REST',
      guid: sp.guid || `UCI:SUP-${idx + 1}`,
    })),
    fittings: safe.canvasFittings || \[],
    options: safe.options || {},
  };
}

export function Coor2Pcf\_emitPcfText(model) {
  const out = \[];
  out.push('ISOGEN-FILES');
  out.push('    ISOGEN.FLS');
  out.push(`PIPELINE-REFERENCE ${model.options.pipelineRef || 'COOR2PCF'}`);

  model.runs.forEach((run) => {
    for (let i = 0; i < run.route.length - 1; i += 1) {
      const a = run.route\[i];
      const b = run.route\[i + 1];
      out.push('PIPE');
      out.push(`    CO-ORDS    ${a.x.toFixed(4)} ${a.y.toFixed(4)} ${a.z.toFixed(4)} ${b.x.toFixed(4)} ${b.y.toFixed(4)} ${b.z.toFixed(4)}`);
    }
  });

  model.supports.forEach((support) => {
    out.push('MESSAGE-SQUARE');
    out.push(`    SUPPORT, RefNo:=${support.refNo}, SeqNo:${support.seqNo}, ${support.name}, ${support.guid}`);
    out.push('SUPPORT');
    out.push(`    CO-ORDS    ${support.x.toFixed(4)} ${support.y.toFixed(4)} ${support.z.toFixed(4)} 0.0000`);
    out.push(`    <SUPPORT\_NAME>    ${support.name}`);
    out.push(`    <SUPPORT\_GUID>    ${support.guid}`);
  });

  return out.join('\\n');
}
```

**Reasoning**
A converter must output the target format, not only metrics.

\---

#### P0 — Multi-run input is dropped

`Pro2D\_fromCoord2PcfSnapshot()` uses `safe.parsedRuns\[0]`.

**Impact**

* disconnected runs disappear,
* route coverage is incomplete,
* converter silently lies about imported topology.

**Patch direction**
Iterate all runs and either:

* create one route per run, or
* merge only when topology is explicitly continuous.

```js
safe.parsedRuns.forEach((run, runIdx) => {
  const routeId = `route\_${runIdx + 1}`;
  const points = Array.isArray(run.route) ? run.route : \[];
  // create nodes and segments for every run
});
```

**Reasoning**
Silent topology loss is unacceptable in a format utility.

\---

#### P1 — Needs a standalone shell

Right now it is only a panel in Pro 2D.

**Recommended shell**

* Input source section
* Snapshot summary
* Diagnostics list
* PCF preview pane
* Copy / download actions
* Unit selection / options

\---

## Coor→PCF tests

### Unit tests

```js
it('imports all runs from snapshot', () => {
  const doc = Pro2D\_fromCoord2PcfSnapshot({
    parsedRuns: \[
      { route: \[{ x: 0, y: 0 }, { x: 10, y: 0 }] },
      { route: \[{ x: 100, y: 0 }, { x: 110, y: 0 }] },
    ],
    supportPoints: \[],
    canvasFittings: \[],
    options: {},
  });

  const pipeCount = Object.values(doc.entities).filter((e) => e.type === 'PIPE').length;
  expect(pipeCount).toBe(2);
});
```

### Golden-text tests

```js
it('emits support block in PCF syntax', () => {
  const text = Coor2Pcf\_emitPcfText({
    runs: \[],
    supports: \[{ id: 's1', x: 1, y: 2, z: 3, refNo: 'R1', seqNo: 1, name: 'CA150', guid: 'UCI:PS00178.1' }],
    fittings: \[],
    options: {},
  });

  expect(text).toContain('MESSAGE-SQUARE');
  expect(text).toContain('SUPPORT, RefNo:=R1, SeqNo:1, CA150, UCI:PS00178.1');
  expect(text).toContain('<SUPPORT\_NAME>    CA150');
});
```

### UI tests

* Pull snapshot
* Show run count > 1
* Generate PCF preview
* Copy PCF
* Download `.pcf`
* Warn on unsupported fitting types

\---

## App 3 — Smart 2D (`js/smart2dcanvas`)

## Architecture assessment

Best store foundation in the bundle, but still **interaction-incomplete**.

### Severity-ranked issues

#### P0 — Viewport is placeholder-only

`Smart2Dcanvas\_CanvasViewport.tsx` renders objects and selection clicks, but:

* no pointer move handling,
* no pointer down/up drafting,
* no wheel zoom,
* no pan,
* snap fixed at `(300,180)`,
* active tool does not change interaction.

**Patch direction**
Turn it into a real controller-backed viewport.

```tsx
const Smart2Dcanvas\_CanvasViewport: React.FC = () => {
  const {
    segments,
    inlineItems,
    supports,
    fittings,
    underlayImages,
    selectedIds,
    activeTool,
    scale,
    panX,
    panY,
    setScale,
    setPan,
    setCursor,
    addSegment,
    addSupport,
    addInlineItem,
    selectObject,
  } = useSceneStore((state) => ({
    segments: state.segments,
    inlineItems: state.inlineItems,
    supports: state.supports,
    fittings: state.fittings,
    underlayImages: state.underlayImages,
    selectedIds: state.selectedIds,
    activeTool: state.activeTool,
    scale: state.scale,
    panX: state.panX,
    panY: state.panY,
    setScale: state.setScale,
    setPan: state.setPan,
    setCursor: state.setCursor,
    addSegment: state.addSegment,
    addSupport: state.addSupport,
    addInlineItem: state.addInlineItem,
    selectObject: state.selectObject,
  }));

  const \[draftStart, setDraftStart] = React.useState(null);
  const \[hoverSnap, setHoverSnap] = React.useState(null);

  const worldFromEvent = (ev) => {
    const rect = ev.currentTarget.getBoundingClientRect();
    return {
      x: (ev.clientX - rect.left - panX) / scale,
      y: (ev.clientY - rect.top - panY) / scale,
    };
  };

  const onPointerMove = (ev) => {
    const world = worldFromEvent(ev);
    setCursor(world.x, world.y);
    setHoverSnap(calculateSnap(world.x, world.y, scale));
  };

  const onPointerDown = (ev) => {
    const world = worldFromEvent(ev);
    const snap = calculateSnap(world.x, world.y, scale);
    const pt = snap?.pt || world;

    if (activeTool === 'line') {
      if (!draftStart) {
        setDraftStart(pt);
        return;
      }
      const id = crypto.randomUUID();
      addSegment({
        id,
        startNodeId: `${id}\_a`,
        endNodeId: `${id}\_b`,
        geometryKind: 'line',
        points: \[
          { id: `${id}\_a`, x: draftStart.x, y: draftStart.y },
          { id: `${id}\_b`, x: pt.x, y: pt.y },
        ],
      });
      setDraftStart(null);
      return;
    }

    if (activeTool === 'support') {
      addSupport({ id: crypto.randomUUID(), nodeId: '', supportType: 'REST', x: pt.x, y: pt.y });
      return;
    }

    if (activeTool === 'valve') {
      addInlineItem({ id: crypto.randomUUID(), type: 'valve', insertionStation: 0.5, occupiedLength: 100, x: pt.x, y: pt.y, angle: 0 });
      return;
    }
  };

  return (
    <div className="absolute inset-0 bg-slate-950" onPointerMove={onPointerMove} onPointerDown={onPointerDown}>
      {/\* render scene \*/}
      {hoverSnap ? <circle cx={hoverSnap.pt.x} cy={hoverSnap.pt.y} r="4" /> : null}
    </div>
  );
};
```

**Reasoning**
Smart 2D should become the minimal working editor first.

\---

#### P1 — Snap engine is not connected to input

It computes well, but is not used for drafting.

**Patch direction**
Always resolve cursor → snap → command point in placement tools.

\---

#### P1 — Inline item placement should be topology-aware

Valve/flange/FVF/reducer placement should not merely drop symbols; it should split a host segment or record host relationship.

**Patch direction**
Start with host-segment split.

```js
export function Smart2Dcanvas\_insertInlineOnSegment(scene, segmentId, point, item) {
  const seg = scene.segments\[segmentId];
  if (!seg || !seg.points?.length) return scene;
  const a = seg.points\[0];
  const b = seg.points\[seg.points.length - 1];
  const mid = { id: `${item.id}\_node`, x: point.x, y: point.y };

  return {
    ...scene,
    segments: {
      ...scene.segments,
      \[`${seg.id}\_a`]: { ...seg, id: `${seg.id}\_a`, endNodeId: mid.id, points: \[a, mid] },
      \[`${seg.id}\_b`]: { ...seg, id: `${seg.id}\_b`, startNodeId: mid.id, points: \[mid, b] },
    },
    inlineItems: {
      ...scene.inlineItems,
      \[item.id]: { ...item, x: point.x, y: point.y },
    },
  };
}
```

**Reasoning**
This matches piping topology much better than floating icons.

\---

## Smart 2D icon/functionality audit

|Tool|Current state|Verified behavior|Fix|
|-|-|-|-|
|Select|Partial|object click selection works|add marquee + hit test|
|Marquee|Not real|only label/state|implement drag box|
|Pan|Not real|state only|implement mouse middle/space-drag|
|Pipe|Not real|state only|implement 2-click segment creation|
|Polyline|Not real|state only|implement multi-point draft|
|Spline|Not real|state only|implement control-point draft|
|Support|Not real|state only|implement snap-based insert|
|Valve/Flange/FVF/Reducer|Not real|state only|implement segment-aware insert|
|Underlay|Not real|rendered if already in store|add import picker / drag-drop|
|Snap|Partial|math works|wire to pointer interaction|
|Undo/Redo|Good store support|available in store, not exposed in UI|add buttons + shortcuts|

\---

## Smart 2D tests

### Unit tests

```js
import { describe, it, expect } from 'vitest';
import { calculateSnap } from './Smart2Dcanvas\_SnapEngine';
import { useSceneStore } from './Smart2Dcanvas\_SceneStore';

describe('snap engine', () => {
  it('snaps to segment midpoint', () => {
    useSceneStore.getState().loadSceneBundle({
      segments: {
        s1: {
          id: 's1',
          startNodeId: 'a',
          endNodeId: 'b',
          geometryKind: 'line',
          points: \[{ id: 'a', x: 0, y: 0 }, { id: 'b', x: 100, y: 0 }],
        },
      },
    });
    const snap = calculateSnap(50, 1, 1);
    expect(snap?.kind).toBe('midpoint');
  });
});
```

### Playwright tests

```ts
test('pipe tool draws one segment with two clicks', async ({ page }) => {
  await page.goto('/smart2d');
  await page.getByTestId('tool-line').click();
  const vp = page.getByTestId('smart2d-viewport');
  await vp.click({ position: { x: 100, y: 100 } });
  await vp.click({ position: { x: 200, y: 100 } });
  await expect(page.getByText(/Selection:/)).toBeVisible();
});
```

### Smoke test

* Draw 20 segments.
* Insert 5 supports.
* Insert valve/flange/fvf/reducer on host segments.
* Undo 10 times, redo 10 times.
* No scene corruption.

\---

## Cross-app fixes to do first

### Phase 1 — Honesty and product boundaries

1. Remove mock fallback from pipeline extraction.
2. Fix 10k benchmark naming/count.
3. Remove duplicated fitting tools from left rail.
4. Add real PCF text generation.
5. Support all input runs in Coor→PCF.

### Phase 2 — Shared viewport/input layer

1. Shared screen↔world transforms.
2. Shared zoom/pan controller.
3. Shared snapping-to-command-point path.
4. Shared keyboard shortcuts.
5. Shared hit testing / selection model.

### Phase 3 — Topology-aware editing

1. Segment split on inline insert.
2. Support node attach rules.
3. Bend/tee insertion commands.
4. Break/connect/stretch.
5. Gap/overlap repair tools.

\---

## Quantitative pass criteria

### Coor→PCF

* Multi-run import: 100% of runs represented in normalized model.
* PCF preview generation: deterministic text output.
* Support block syntax present exactly once per support.
* Unsupported fitting types produce diagnostics, not silent drop.

### Smart 2D

* Two-click pipe draw adds exactly one segment.
* Snap-to-midpoint distance tolerance within threshold.
* Undo/redo stable over 50 operations.
* Inline item insert splits one host segment into two segments.
* 0 console/runtime errors during 5-minute draw/edit smoke.
* 

