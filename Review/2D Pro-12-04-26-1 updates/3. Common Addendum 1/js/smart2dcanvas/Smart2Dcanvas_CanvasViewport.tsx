import React, { useMemo, useRef, useState } from 'react';
import { useSceneStore } from './Smart2Dcanvas_SceneStore';
import { calculateSnap } from './Smart2Dcanvas_SnapEngine';
import {
  Pro2D_splitSegmentAtPoint,
  Pro2D_findNearestEndpoint,
  Pro2D_connectEndpoints,
  Pro2D_stretchEndpointToPoint,
  Pro2D_gapCleanScene,
  Pro2D_mergeOverlappingLineSegments,
} from '../pro2dcanvas/Pro2D_RepairOps.mjs';
import { useShallow } from 'zustand/react/shallow';

const VIEW_W = 800;
const VIEW_H = 520;
const COLORS: any = {
  segment: '#e2e8f0',
  inline: '#f59e0b',
  support: '#22c55e',
  fitting: '#38bdf8',
  annotation: '#f472b6',
};

function uid(prefix: string) {
  return `${prefix}_${Math.random().toString(36).slice(2, 9)}`;
}

function dist(a: any, b: any) {
  return Math.hypot((a.x || 0) - (b.x || 0), (a.y || 0) - (b.y || 0));
}

function clientToSvg(ev: any, svg: SVGSVGElement | null) {
  const rect = svg?.getBoundingClientRect();
  if (!rect) return { x: 0, y: 0 };
  return {
    x: ((ev.clientX - rect.left) / rect.width) * VIEW_W,
    y: ((ev.clientY - rect.top) / rect.height) * VIEW_H,
  };
}

function svgToWorld(svgPt: any, scale: number, panX: number, panY: number) {
  return {
    x: (svgPt.x - panX) / Math.max(scale || 1, 0.001),
    y: (svgPt.y - panY) / Math.max(scale || 1, 0.001),
  };
}

function worldToSvg(world: any, scale: number, panX: number, panY: number) {
  return {
    x: world.x * scale + panX,
    y: world.y * scale + panY,
  };
}

function distanceToSegment(pt: any, a: any, b: any) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len2 = dx * dx + dy * dy;
  if (len2 <= 1e-9) return dist(pt, a);
  const t = Math.max(0, Math.min(1, ((pt.x - a.x) * dx + (pt.y - a.y) * dy) / len2));
  const proj = { x: a.x + t * dx, y: a.y + t * dy };
  return dist(pt, proj);
}

function pickObjectAt(state: any, world: any, threshold = 12) {
  const all: Array<{ id: string; kind: string; distance: number }> = [];
  Object.values(state.annotations || {}).forEach((ann: any) => all.push({ id: ann.id, kind: 'annotation', distance: dist(world, ann) }));
  Object.values(state.inlineItems || {}).forEach((item: any) => all.push({ id: item.id, kind: 'inline', distance: dist(world, item) }));
  Object.values(state.supports || {}).forEach((item: any) => all.push({ id: item.id, kind: 'support', distance: dist(world, item) }));
  Object.values(state.fittings || {}).forEach((item: any) => all.push({ id: item.id, kind: 'fitting', distance: dist(world, item) }));
  Object.values(state.segments || {}).forEach((seg: any) => {
    const pts = seg.points || [];
    const a = pts[0];
    const b = pts[pts.length - 1];
    if (!a || !b) return;
    all.push({ id: seg.id, kind: 'segment', distance: distanceToSegment(world, a, b) });
  });
  const hits = all.filter((x) => x.distance <= threshold).sort((a, b) => a.distance - b.distance);
  return hits[0] || null;
}

function computeSceneBounds(state: any) {
  const pts: any[] = [];
  Object.values(state.segments || {}).forEach((seg: any) => (seg.points || []).forEach((p: any) => pts.push(p)));
  Object.values(state.inlineItems || {}).forEach((x: any) => pts.push(x));
  Object.values(state.supports || {}).forEach((x: any) => pts.push(x));
  Object.values(state.fittings || {}).forEach((x: any) => pts.push(x));
  Object.values(state.annotations || {}).forEach((x: any) => pts.push(x));
  if (!pts.length) return { minX: 0, minY: 0, maxX: VIEW_W, maxY: VIEW_H };
  const xs = pts.map((p) => p.x);
  const ys = pts.map((p) => p.y);
  return {
    minX: Math.min(...xs),
    minY: Math.min(...ys),
    maxX: Math.max(...xs),
    maxY: Math.max(...ys),
  };
}

const Smart2Dcanvas_CanvasViewport: React.FC = () => {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [hoverSnap, setHoverSnap] = useState<any>(null);
  const [panDrag, setPanDrag] = useState<any>(null);
  const [pendingConnect, setPendingConnect] = useState<any>(null);
  const [pendingStretch, setPendingStretch] = useState<any>(null);

  const state = useSceneStore(useShallow((s: any) => ({
    nodes: s.nodes,
    segments: s.segments,
    inlineItems: s.inlineItems,
    supports: s.supports,
    fittings: s.fittings,
    underlayImages: s.underlayImages,
    annotations: s.annotations,
    selectedIds: s.selectedIds,
    activeTool: s.activeTool,
    scale: s.scale,
    panX: s.panX,
    panY: s.panY,
    isOsnap: s.isOsnap,
    setScale: s.setScale,
    setPan: s.setPan,
    setCursor: s.setCursor,
    setActiveTool: s.setActiveTool,
    selectObject: s.selectObject,
    clearSelection: s.clearSelection,
    addAnnotation: s.addAnnotation,
    replaceSceneBundle: s.replaceSceneBundle,
  })));

  const bounds = useMemo(() => computeSceneBounds(state), [state.segments, state.inlineItems, state.supports, state.fittings, state.annotations]);

  const onPointerMove = (ev: any) => {
    const svgPt = clientToSvg(ev, svgRef.current);
    const world = svgToWorld(svgPt, state.scale, state.panX, state.panY);
    state.setCursor(world.x, world.y);

    if (panDrag) {
      state.setPan(state.panX + (svgPt.x - panDrag.lastX), state.panY + (svgPt.y - panDrag.lastY));
      setPanDrag({ lastX: svgPt.x, lastY: svgPt.y });
      return;
    }

    const snap = state.isOsnap ? calculateSnap(world.x, world.y, state.scale) : null;
    setHoverSnap(snap);
  };

  const onPointerUp = () => setPanDrag(null);

  const runRepairTransform = (result: any) => {
    if (result?.changed) state.replaceSceneBundle(result.bundle);
    return !!result?.changed;
  };

  const onPointerDown = (ev: any) => {
    const svgPt = clientToSvg(ev, svgRef.current);
    const worldRaw = svgToWorld(svgPt, state.scale, state.panX, state.panY);
    const snap = state.isOsnap ? calculateSnap(worldRaw.x, worldRaw.y, state.scale) : null;
    const world = snap?.pt || worldRaw;

    if (state.activeTool === 'pan' || ev.button === 1) {
      setPanDrag({ lastX: svgPt.x, lastY: svgPt.y });
      return;
    }

    if (state.activeTool === 'select' || state.activeTool === 'marquee') {
      const hit = pickObjectAt(state, world);
      if (hit) state.selectObject(hit.id, !!ev.ctrlKey);
      else state.clearSelection();
      return;
    }

    if (state.activeTool === 'annotations') {
      const text = typeof window !== 'undefined' && typeof window.prompt === 'function'
        ? (window.prompt('Issue / annotation text', 'Issue') || '').trim()
        : 'Issue';
      if (!text) return;
      state.addAnnotation({
        id: uid('ann'),
        x: Number(world.x.toFixed(2)),
        y: Number(world.y.toFixed(2)),
        text,
        severity: 'info',
        metadata: { createdBy: 'annotations' },
      });
      return;
    }

    if (state.activeTool === 'break') {
      runRepairTransform(Pro2D_splitSegmentAtPoint(state, world, 16 / Math.max(state.scale || 1, 0.001)));
      return;
    }

    if (state.activeTool === 'connect') {
      const endpoint = Pro2D_findNearestEndpoint(state, world, 16 / Math.max(state.scale || 1, 0.001));
      if (!endpoint) return;
      if (!pendingConnect) {
        setPendingConnect(endpoint);
        return;
      }
      runRepairTransform(Pro2D_connectEndpoints(state, pendingConnect, endpoint));
      setPendingConnect(null);
      return;
    }

    if (state.activeTool === 'stretch') {
      const endpoint = Pro2D_findNearestEndpoint(state, world, 16 / Math.max(state.scale || 1, 0.001));
      if (!pendingStretch) {
        if (endpoint) setPendingStretch(endpoint);
        return;
      }
      runRepairTransform(Pro2D_stretchEndpointToPoint(state, pendingStretch, world));
      setPendingStretch(null);
      return;
    }

    if (state.activeTool === 'gapClean') {
      runRepairTransform(Pro2D_gapCleanScene(state, 12 / Math.max(state.scale || 1, 0.001)));
      state.setActiveTool('select');
      return;
    }

    if (state.activeTool === 'overlapSolver') {
      runRepairTransform(Pro2D_mergeOverlappingLineSegments(state, 1.2 / Math.max(state.scale || 1, 0.001)));
      state.setActiveTool('select');
      return;
    }
  };

  const onWheel = (ev: any) => {
    ev.preventDefault();
    const svgPt = clientToSvg(ev, svgRef.current);
    const worldBefore = svgToWorld(svgPt, state.scale, state.panX, state.panY);
    const nextScale = Math.max(0.2, Math.min(8, state.scale * (ev.deltaY < 0 ? 1.1 : 0.9)));
    const nextPanX = svgPt.x - worldBefore.x * nextScale;
    const nextPanY = svgPt.y - worldBefore.y * nextScale;
    state.setScale(nextScale);
    state.setPan(nextPanX, nextPanY);
  };

  const radarBox = { x: VIEW_W - 170, y: 16, w: 150, h: 110 };
  const worldW = Math.max(bounds.maxX - bounds.minX, 1);
  const worldH = Math.max(bounds.maxY - bounds.minY, 1);

  const onRadarPointerDown = (ev: any) => {
    ev.stopPropagation();
    const svgPt = clientToSvg(ev, svgRef.current);
    if (svgPt.x < radarBox.x || svgPt.x > radarBox.x + radarBox.w || svgPt.y < radarBox.y || svgPt.y > radarBox.y + radarBox.h) return;
    const rx = (svgPt.x - radarBox.x) / radarBox.w;
    const ry = (svgPt.y - radarBox.y) / radarBox.h;
    const targetWorld = {
      x: bounds.minX + rx * worldW,
      y: bounds.minY + ry * worldH,
    };
    state.setPan(VIEW_W / 2 - targetWorld.x * state.scale, VIEW_H / 2 - targetWorld.y * state.scale);
  };

  const viewTopLeftWorld = svgToWorld({ x: 0, y: 0 }, state.scale, state.panX, state.panY);
  const viewBottomRightWorld = svgToWorld({ x: VIEW_W, y: VIEW_H }, state.scale, state.panX, state.panY);
  const radarView = {
    x: radarBox.x + ((viewTopLeftWorld.x - bounds.minX) / worldW) * radarBox.w,
    y: radarBox.y + ((viewTopLeftWorld.y - bounds.minY) / worldH) * radarBox.h,
    w: ((viewBottomRightWorld.x - viewTopLeftWorld.x) / worldW) * radarBox.w,
    h: ((viewBottomRightWorld.y - viewTopLeftWorld.y) / worldH) * radarBox.h,
  };

  return (
    <div className="absolute inset-0 bg-slate-950">
      <svg
        ref={svgRef}
        viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
        className="w-full h-full"
        onPointerMove={onPointerMove}
        onPointerDown={onPointerDown}
        onPointerUp={onPointerUp}
        onPointerLeave={onPointerUp}
        onWheel={onWheel}
      >
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" strokeWidth="1" />
          </pattern>
        </defs>
        <rect x="0" y="0" width={VIEW_W} height={VIEW_H} fill="url(#grid)" />

        <g transform={`translate(${state.panX} ${state.panY}) scale(${state.scale})`}>
          {Object.values(state.underlayImages).map((img: any) => (
            <g key={img.id} opacity={img.opacity || 0.25}>
              <rect x={img.x} y={img.y} width={120 * (img.scaleX || 1)} height={80 * (img.scaleY || 1)} fill="#334155" stroke="#64748b" />
              <text x={img.x + 8} y={img.y + 20} fontSize={11 / state.scale} fill="#cbd5e1">Underlay</text>
            </g>
          ))}

          {Object.values(state.segments).map((seg: any) => {
            const pts = seg.points || [];
            const a = pts[0];
            const b = pts[pts.length - 1];
            if (!a || !b) return null;
            const selected = state.selectedIds.has(seg.id);
            return (
              <g key={seg.id}>
                <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={selected ? '#f59e0b' : COLORS.segment} strokeWidth={(selected ? 4 : 3) / state.scale} />
                <circle cx={a.x} cy={a.y} r={3 / state.scale} fill="#94a3b8" />
                <circle cx={b.x} cy={b.y} r={3 / state.scale} fill="#94a3b8" />
              </g>
            );
          })}

          {Object.values(state.inlineItems).map((item: any) => {
            const selected = state.selectedIds.has(item.id);
            return (
              <g key={item.id}>
                <circle cx={item.x} cy={item.y} r={(selected ? 8 : 6) / state.scale} fill={COLORS.inline} />
                <text x={item.x + 8 / state.scale} y={item.y - 8 / state.scale} fontSize={10 / state.scale} fill="#f8fafc">{item.type}</text>
              </g>
            );
          })}

          {Object.values(state.supports).map((support: any) => {
            const selected = state.selectedIds.has(support.id);
            const s = 6 / state.scale;
            return (
              <g key={support.id}>
                <path d={`M ${support.x-s} ${support.y} L ${support.x+s} ${support.y} M ${support.x} ${support.y-s} L ${support.x} ${support.y+s}`} stroke={selected ? '#f59e0b' : COLORS.support} strokeWidth={2 / state.scale} />
                <text x={support.x + 8 / state.scale} y={support.y - 8 / state.scale} fontSize={10 / state.scale} fill="#86efac">{support.supportType}</text>
              </g>
            );
          })}

          {Object.values(state.fittings).map((fit: any) => {
            const selected = state.selectedIds.has(fit.id);
            const s = 6 / state.scale;
            return (
              <g key={fit.id}>
                <rect x={fit.x - s} y={fit.y - s} width={2 * s} height={2 * s} fill={selected ? '#f59e0b' : COLORS.fitting} />
                <text x={fit.x + 8 / state.scale} y={fit.y - 8 / state.scale} fontSize={10 / state.scale} fill="#7dd3fc">{fit.type}</text>
              </g>
            );
          })}

          {Object.values(state.annotations || {}).map((ann: any) => {
            const selected = state.selectedIds.has(ann.id);
            return (
              <g key={ann.id}>
                <circle cx={ann.x} cy={ann.y} r={(selected ? 7 : 5) / state.scale} fill={COLORS.annotation} />
                <text x={ann.x + 10 / state.scale} y={ann.y + 4 / state.scale} fontSize={10 / state.scale} fill="#fbcfe8">{ann.text}</text>
              </g>
            );
          })}

          {hoverSnap ? (
            <g>
              <circle cx={hoverSnap.pt.x} cy={hoverSnap.pt.y} r={5 / state.scale} fill="none" stroke="#22d3ee" strokeWidth={1.5 / state.scale} />
              <text x={hoverSnap.pt.x + 8 / state.scale} y={hoverSnap.pt.y + 8 / state.scale} fontSize={10 / state.scale} fill="#22d3ee">snap:{hoverSnap.kind}</text>
            </g>
          ) : null}

          {pendingConnect ? (
            <g>
              <circle cx={pendingConnect.point.x} cy={pendingConnect.point.y} r={7 / state.scale} fill="none" stroke="#facc15" strokeWidth={2 / state.scale} />
              <text x={pendingConnect.point.x + 8 / state.scale} y={pendingConnect.point.y - 8 / state.scale} fontSize={10 / state.scale} fill="#fde68a">connect:start</text>
            </g>
          ) : null}

          {pendingStretch ? (
            <g>
              <circle cx={pendingStretch.point.x} cy={pendingStretch.point.y} r={7 / state.scale} fill="none" stroke="#a78bfa" strokeWidth={2 / state.scale} />
              <text x={pendingStretch.point.x + 8 / state.scale} y={pendingStretch.point.y - 8 / state.scale} fontSize={10 / state.scale} fill="#ddd6fe">stretch:endpoint</text>
            </g>
          ) : null}
        </g>

        <text x="12" y="20" fontSize="12" fill="#94a3b8">active tool: {state.activeTool}</text>

        {state.activeTool === 'minimap' ? (
          <g onPointerDown={onRadarPointerDown} style={{ cursor: 'pointer' }}>
            <rect x={radarBox.x} y={radarBox.y} width={radarBox.w} height={radarBox.h} rx="8" fill="#020617cc" stroke="#334155" />
            {Object.values(state.segments).map((seg: any) => {
              const a = seg.points?.[0];
              const b = seg.points?.[seg.points.length - 1];
              if (!a || !b) return null;
              const sa = { x: radarBox.x + ((a.x - bounds.minX) / worldW) * radarBox.w, y: radarBox.y + ((a.y - bounds.minY) / worldH) * radarBox.h };
              const sb = { x: radarBox.x + ((b.x - bounds.minX) / worldW) * radarBox.w, y: radarBox.y + ((b.y - bounds.minY) / worldH) * radarBox.h };
              return <line key={`radar_${seg.id}`} x1={sa.x} y1={sa.y} x2={sb.x} y2={sb.y} stroke="#cbd5e1" strokeWidth="1" />;
            })}
            <rect x={radarView.x} y={radarView.y} width={Math.max(radarView.w, 6)} height={Math.max(radarView.h, 6)} fill="none" stroke="#22d3ee" strokeWidth="1.5" />
            <text x={radarBox.x + 8} y={radarBox.y + 14} fontSize="10" fill="#7dd3fc">Radar</text>
          </g>
        ) : null}
      </svg>
    </div>
  );
};

export default Smart2Dcanvas_CanvasViewport;
