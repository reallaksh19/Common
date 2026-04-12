function clone(v) {
  return JSON.parse(JSON.stringify(v));
}

function uid(prefix) {
  return `${prefix}_${Math.random().toString(36).slice(2, 9)}`;
}

function dist(a, b) {
  return Math.hypot((a.x || 0) - (b.x || 0), (a.y || 0) - (b.y || 0));
}

function getSegEnds(seg) {
  const pts = seg?.points || [];
  const a = pts[0];
  const b = pts[pts.length - 1];
  return a && b ? { a, b } : null;
}

function projectPointToSegment(pt, a, b) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len2 = dx * dx + dy * dy;
  if (len2 <= 1e-9) return { point: { x: a.x, y: a.y }, t: 0, distance: dist(pt, a) };
  const t = Math.max(0, Math.min(1, ((pt.x - a.x) * dx + (pt.y - a.y) * dy) / len2));
  const point = { x: a.x + t * dx, y: a.y + t * dy };
  return { point, t, distance: dist(pt, point) };
}

function normalizePoint(pt) {
  return { x: Number(pt?.x || 0), y: Number(pt?.y || 0), z: pt?.z == null ? undefined : Number(pt.z || 0) };
}

export function Pro2D_sceneStats(bundle) {
  return {
    nodes: Object.keys(bundle?.nodes || {}).length,
    segments: Object.keys(bundle?.segments || {}).length,
    inlineItems: Object.keys(bundle?.inlineItems || {}).length,
    supports: Object.keys(bundle?.supports || {}).length,
    fittings: Object.keys(bundle?.fittings || {}).length,
    annotations: Object.keys(bundle?.annotations || {}).length,
  };
}

export function Pro2D_findNearestSegment(bundle, point, threshold = 14) {
  const segs = Object.values(bundle?.segments || {});
  let best = null;
  for (const seg of segs) {
    const ends = getSegEnds(seg);
    if (!ends) continue;
    const hit = projectPointToSegment(point, ends.a, ends.b);
    if (hit.distance > threshold) continue;
    if (!best || hit.distance < best.distance) best = { segment: seg, ...hit };
  }
  return best;
}

export function Pro2D_findNearestEndpoint(bundle, point, threshold = 14) {
  let best = null;
  for (const seg of Object.values(bundle?.segments || {})) {
    const ends = getSegEnds(seg);
    if (!ends) continue;
    const candidates = [
      { point: ends.a, nodeId: seg.startNodeId, role: 'start', segmentId: seg.id },
      { point: ends.b, nodeId: seg.endNodeId, role: 'end', segmentId: seg.id },
    ];
    for (const cand of candidates) {
      const d = dist(point, cand.point);
      if (d > threshold) continue;
      if (!best || d < best.distance) best = { ...cand, distance: d };
    }
  }
  return best;
}

export function Pro2D_splitSegmentAtPoint(bundle, point, threshold = 14) {
  const hit = Pro2D_findNearestSegment(bundle, point, threshold);
  if (!hit) return { changed: false, bundle, reason: 'no-segment-hit' };
  if (hit.t <= 1e-3 || hit.t >= 1 - 1e-3) return { changed: false, bundle, reason: 'near-endpoint' };

  const next = clone(bundle);
  const seg = hit.segment;
  const splitPoint = normalizePoint(hit.point);
  const splitNodeId = uid('node');
  const leftId = uid('seg');
  const rightId = uid('seg');

  next.nodes = next.nodes || {};
  next.nodes[splitNodeId] = { id: splitNodeId, x: splitPoint.x, y: splitPoint.y, z: splitPoint.z, kind: 'MIDPOINT' };

  const base = {
    geometryKind: seg.geometryKind || 'line',
    sizeSpecFields: clone(seg.sizeSpecFields || {}),
    metadata: clone(seg.metadata || {}),
  };

  next.segments[leftId] = {
    id: leftId,
    startNodeId: seg.startNodeId,
    endNodeId: splitNodeId,
    points: [{ ...seg.points[0] }, { id: splitNodeId, ...splitPoint }],
    ...base,
  };

  next.segments[rightId] = {
    id: rightId,
    startNodeId: splitNodeId,
    endNodeId: seg.endNodeId,
    points: [{ id: splitNodeId, ...splitPoint }, { ...seg.points[seg.points.length - 1] }],
    ...base,
  };

  delete next.segments[seg.id];
  return { changed: true, bundle: next, splitNodeId, leftId, rightId };
}

export function Pro2D_connectEndpoints(bundle, endpointA, endpointB) {
  if (!endpointA || !endpointB) return { changed: false, bundle, reason: 'missing-endpoints' };
  if (endpointA.segmentId === endpointB.segmentId && endpointA.role === endpointB.role) return { changed: false, bundle, reason: 'same-endpoint' };
  if (dist(endpointA.point, endpointB.point) < 1e-6) return { changed: false, bundle, reason: 'zero-length' };

  const next = clone(bundle);
  const segId = uid('seg');
  next.segments = next.segments || {};
  next.segments[segId] = {
    id: segId,
    startNodeId: endpointA.nodeId || uid('node'),
    endNodeId: endpointB.nodeId || uid('node'),
    geometryKind: 'line',
    points: [normalizePoint(endpointA.point), normalizePoint(endpointB.point)],
    sizeSpecFields: {},
    metadata: { createdBy: 'connect' },
  };
  return { changed: true, bundle: next, segmentId: segId };
}

export function Pro2D_stretchEndpointToPoint(bundle, endpoint, targetPoint) {
  if (!endpoint || !targetPoint) return { changed: false, bundle, reason: 'missing-input' };
  const next = clone(bundle);
  const seg = next.segments?.[endpoint.segmentId];
  if (!seg || !Array.isArray(seg.points) || seg.points.length < 2) return { changed: false, bundle, reason: 'bad-segment' };

  const target = normalizePoint(targetPoint);
  const nodeId = endpoint.nodeId;
  if (nodeId && next.nodes?.[nodeId]) {
    next.nodes[nodeId] = { ...next.nodes[nodeId], x: target.x, y: target.y, z: target.z };
    for (const candidate of Object.values(next.segments || {})) {
      if (candidate.startNodeId === nodeId && candidate.points?.[0]) {
        candidate.points[0] = { ...candidate.points[0], ...target };
      }
      if (candidate.endNodeId === nodeId && candidate.points?.length) {
        candidate.points[candidate.points.length - 1] = { ...candidate.points[candidate.points.length - 1], ...target };
      }
    }
  } else {
    if (endpoint.role === 'start') seg.points[0] = { ...seg.points[0], ...target };
    else seg.points[seg.points.length - 1] = { ...seg.points[seg.points.length - 1], ...target };
  }
  return { changed: true, bundle: next };
}

function endpointPairs(bundle) {
  const pairs = [];
  for (const seg of Object.values(bundle?.segments || {})) {
    const ends = getSegEnds(seg);
    if (!ends) continue;
    pairs.push({ segmentId: seg.id, nodeId: seg.startNodeId, role: 'start', point: normalizePoint(ends.a) });
    pairs.push({ segmentId: seg.id, nodeId: seg.endNodeId, role: 'end', point: normalizePoint(ends.b) });
  }
  return pairs;
}

export function Pro2D_gapCleanScene(bundle, tolerance = 8) {
  const endpoints = endpointPairs(bundle);
  const next = clone(bundle);
  let connections = 0;
  for (let i = 0; i < endpoints.length; i += 1) {
    const a = endpoints[i];
    let best = null;
    for (let j = i + 1; j < endpoints.length; j += 1) {
      const b = endpoints[j];
      if (a.segmentId === b.segmentId) continue;
      const d = dist(a.point, b.point);
      if (d <= 1e-6 || d > tolerance) continue;
      if (!best || d < best.distance) best = { a, b, distance: d };
    }
    if (best) {
      const segId = uid('seg');
      next.segments[segId] = {
        id: segId,
        startNodeId: best.a.nodeId || uid('node'),
        endNodeId: best.b.nodeId || uid('node'),
        geometryKind: 'line',
        points: [normalizePoint(best.a.point), normalizePoint(best.b.point)],
        sizeSpecFields: {},
        metadata: { createdBy: 'gapClean' },
      };
      connections += 1;
    }
  }
  return { changed: connections > 0, bundle: next, connections };
}

function segmentAxis(seg) {
  const ends = getSegEnds(seg);
  if (!ends) return null;
  const dx = ends.b.x - ends.a.x;
  const dy = ends.b.y - ends.a.y;
  const len = Math.hypot(dx, dy);
  if (len <= 1e-9) return null;
  return { dx: dx / len, dy: dy / len };
}

function areCollinearOverlapping(segA, segB, tol = 1) {
  const ea = getSegEnds(segA);
  const eb = getSegEnds(segB);
  if (!ea || !eb) return false;
  const ax = segmentAxis(segA);
  const bx = segmentAxis(segB);
  if (!ax || !bx) return false;
  const cross = Math.abs(ax.dx * bx.dy - ax.dy * bx.dx);
  if (cross > 1e-3) return false;
  const perp = Math.abs((eb.a.x - ea.a.x) * ax.dy - (eb.a.y - ea.a.y) * ax.dx);
  if (perp > tol) return false;

  const origin = ea.a;
  const proj = (p) => (p.x - origin.x) * ax.dx + (p.y - origin.y) * ax.dy;
  const a0 = proj(ea.a), a1 = proj(ea.b), b0 = proj(eb.a), b1 = proj(eb.b);
  const amin = Math.min(a0, a1), amax = Math.max(a0, a1), bmin = Math.min(b0, b1), bmax = Math.max(b0, b1);
  return Math.min(amax, bmax) >= Math.max(amin, bmin) - tol;
}

export function Pro2D_mergeOverlappingLineSegments(bundle, tolerance = 1) {
  const next = clone(bundle);
  const segIds = Object.keys(next.segments || {});
  let merges = 0;

  for (let i = 0; i < segIds.length; i += 1) {
    const aId = segIds[i];
    const segA = next.segments[aId];
    if (!segA) continue;
    for (let j = i + 1; j < segIds.length; j += 1) {
      const bId = segIds[j];
      const segB = next.segments[bId];
      if (!segB) continue;
      if (!areCollinearOverlapping(segA, segB, tolerance)) continue;

      const axis = segmentAxis(segA);
      const origin = getSegEnds(segA).a;
      const proj = (p) => (p.x - origin.x) * axis.dx + (p.y - origin.y) * axis.dy;
      const pts = [getSegEnds(segA).a, getSegEnds(segA).b, getSegEnds(segB).a, getSegEnds(segB).b];
      pts.sort((p1, p2) => proj(p1) - proj(p2));
      segA.points = [normalizePoint(pts[0]), normalizePoint(pts[pts.length - 1])];
      delete next.segments[bId];
      merges += 1;
    }
  }

  return { changed: merges > 0, bundle: next, merges };
}
