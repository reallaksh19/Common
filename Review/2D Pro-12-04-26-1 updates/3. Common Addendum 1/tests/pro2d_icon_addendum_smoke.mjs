import assert from 'node:assert/strict';
import {
  Pro2D_splitSegmentAtPoint,
  Pro2D_findNearestEndpoint,
  Pro2D_connectEndpoints,
  Pro2D_stretchEndpointToPoint,
  Pro2D_gapCleanScene,
  Pro2D_mergeOverlappingLineSegments,
  Pro2D_sceneStats,
} from '../js/pro2dcanvas/Pro2D_RepairOps.mjs';

const base = {
  nodes: {
    n1: { id: 'n1', x: 0, y: 0 },
    n2: { id: 'n2', x: 100, y: 0 },
    n3: { id: 'n3', x: 110, y: 0 },
    n4: { id: 'n4', x: 200, y: 0 },
    n5: { id: 'n5', x: 60, y: 0 },
    n6: { id: 'n6', x: 140, y: 0 },
  },
  segments: {
    s1: { id: 's1', startNodeId: 'n1', endNodeId: 'n2', geometryKind: 'line', points: [{ x: 0, y: 0 }, { x: 100, y: 0 }], metadata: {} },
    s2: { id: 's2', startNodeId: 'n3', endNodeId: 'n4', geometryKind: 'line', points: [{ x: 110, y: 0 }, { x: 200, y: 0 }], metadata: {} },
    s3: { id: 's3', startNodeId: 'n5', endNodeId: 'n6', geometryKind: 'line', points: [{ x: 60, y: 0 }, { x: 140, y: 0 }], metadata: {} },
  },
  inlineItems: {},
  supports: {},
  fittings: {},
  underlayImages: {},
  annotations: {},
};

const split = Pro2D_splitSegmentAtPoint(base, { x: 50, y: 0 }, 10);
assert.equal(split.changed, true);
assert.equal(Object.keys(split.bundle.segments).length, 4);

const epA = Pro2D_findNearestEndpoint(base, { x: 100, y: 0 }, 5);
const epB = Pro2D_findNearestEndpoint(base, { x: 110, y: 0 }, 5);
const connect = Pro2D_connectEndpoints(base, epA, epB);
assert.equal(connect.changed, true);
assert.equal(Object.keys(connect.bundle.segments).length, 4);

const stretch = Pro2D_stretchEndpointToPoint(base, epA, { x: 105, y: 5 });
assert.equal(stretch.changed, true);
assert.equal(stretch.bundle.segments.s1.points[1].x, 105);
assert.equal(stretch.bundle.segments.s1.points[1].y, 5);

const gap = Pro2D_gapCleanScene(base, 12);
assert.equal(gap.changed, true);
assert.ok(gap.connections >= 1);

const overlap = Pro2D_mergeOverlappingLineSegments(base, 1.2);
assert.equal(overlap.changed, true);
assert.ok(overlap.merges >= 1);

const stats = Pro2D_sceneStats(overlap.bundle);
assert.ok(stats.segments < 3);

console.log(JSON.stringify({
  splitSegments: Object.keys(split.bundle.segments).length,
  connectSegments: Object.keys(connect.bundle.segments).length,
  stretchedEnd: stretch.bundle.segments.s1.points[1],
  gapConnections: gap.connections,
  overlapMerges: overlap.merges,
  overlapStats: stats,
}, null, 2));
