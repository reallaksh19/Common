import { Pro2D_createEmptyState } from './Pro2D_Canonical.mjs';

function fmt(n) { return Number.isFinite(Number(n)) ? String(Number(n)) : '0'; }
function num(v, fallback = 0) { const n = Number(v); return Number.isFinite(n) ? n : fallback; }
function text(v) { return typeof v === 'string' ? v : ''; }
function lower(v) { return text(v).toLowerCase(); }
function keyForPoint(x, y, z = 0, precision = 4) { return `${num(x).toFixed(precision)}|${num(y).toFixed(precision)}|${num(z).toFixed(precision)}`; }
function roundValue(v, precision = 4) { return Number(num(v).toFixed(precision)); }
function safeArray(v) { return Array.isArray(v) ? v : []; }
function degToRad(deg) { return (num(deg) * Math.PI) / 180; }
function dist(a, b) { return Math.hypot(num(b.x) - num(a.x), num(b.y) - num(a.y)); }
function averageAbs(a, b) { return (Math.abs(num(a, 1)) + Math.abs(num(b, 1))) / 2 || 1; }
function uid(prefix, seq) { return `${prefix}_${seq}`; }

const INSUNITS_MAP = {
  0: 'unitless',
  1: 'in',
  2: 'ft',
  4: 'mm',
  5: 'cm',
  6: 'm',
  7: 'km',
};

const INLINE_TOKEN_MAP = [
  { tokens: ['valve', 'gate', 'globe', 'ball', 'butterfly', 'check', 'nrv'], type: 'valve' },
  { tokens: ['flange', 'flg', 'rf', 'wn', 'so'], type: 'flange' },
  { tokens: ['reducer', 'ecc', 'conc'], type: 'reducer' },
  { tokens: ['fvf'], type: 'fvf' },
];

function createImportReport(fileName = 'DXF') {
  return {
    fileName,
    engine: 'fallback-simple',
    entityCounts: {},
    imported: { segments: 0, inlineItems: 0, supports: 0, fittings: 0, ignored: 0 },
    layers: [],
    warnings: [],
    ignoredEntities: [],
    extractedTexts: [],
  };
}

function bumpCount(map, key) {
  map[key] = (map[key] || 0) + 1;
}

function addWarning(report, message) {
  if (!report.warnings.includes(message)) report.warnings.push(message);
}

function getLayerName(entity) {
  return text(entity?.layer || entity?.['8'] || entity?.common?.layer || entity?.dxf?.layer || '0') || '0';
}

function getColorIndex(entity) {
  return entity?.colorNumber ?? entity?.colorIndex ?? entity?.['62'] ?? entity?.dxf?.color ?? null;
}

function getEntityHandle(entity) {
  return text(entity?.handle || entity?.['5'] || entity?.dxf?.handle || '');
}

function getBlockName(entity) {
  return text(entity?.blockName || entity?.name || entity?.['2'] || entity?.dxf?.name || '');
}

function getEntityText(entity) {
  return text(entity?.text || entity?.string || entity?.['1'] || entity?.content || entity?.rawText || '');
}

function getEntityPoint(entity) {
  if (entity?.position) return { x: num(entity.position.x), y: num(entity.position.y), z: num(entity.position.z) };
  if (entity?.location) return { x: num(entity.location.x), y: num(entity.location.y), z: num(entity.location.z) };
  if (entity?.center) return { x: num(entity.center.x), y: num(entity.center.y), z: num(entity.center.z) };
  return { x: num(entity?.['10']), y: num(entity?.['20']), z: num(entity?.['30']) };
}

function getEntityRotationDeg(entity) {
  return num(entity?.rotation || entity?.['50'] || entity?.dxf?.rotation || 0);
}

function getEntityScale(entity) {
  return {
    x: num(entity?.xScale || entity?.['41'] || entity?.scaleX || 1, 1),
    y: num(entity?.yScale || entity?.['42'] || entity?.scaleY || 1, 1),
    z: num(entity?.zScale || entity?.['43'] || entity?.scaleZ || 1, 1),
  };
}

function buildBlockMap(parsed) {
  const map = new Map();
  const blocks = parsed?.blocks;
  if (Array.isArray(blocks)) {
    blocks.forEach((block) => {
      const name = getBlockName(block);
      if (name) map.set(name, safeArray(block.entities));
    });
    return map;
  }
  if (blocks && typeof blocks === 'object') {
    Object.entries(blocks).forEach(([name, block]) => {
      if (Array.isArray(block?.entities)) map.set(name, block.entities);
      else if (Array.isArray(block)) map.set(name, block);
      else if (Array.isArray(block?.children)) map.set(name, block.children);
    });
  }
  return map;
}

function transformPoint(pt, tx) {
  const sx = num(tx?.scaleX, 1);
  const sy = num(tx?.scaleY, 1);
  const angle = degToRad(tx?.rotation || 0);
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  const x0 = num(pt?.x) * sx;
  const y0 = num(pt?.y) * sy;
  return {
    x: roundValue(x0 * cos - y0 * sin + num(tx?.offsetX, 0)),
    y: roundValue(x0 * sin + y0 * cos + num(tx?.offsetY, 0)),
    z: roundValue(num(pt?.z) + num(tx?.offsetZ, 0)),
  };
}

function normalizeVertices(entity) {
  const verts = [];
  if (Array.isArray(entity?.vertices)) {
    entity.vertices.forEach((v, index) => {
      verts.push({
        id: v.id || `${entity.type || 'v'}_${index + 1}`,
        x: num(v.x ?? v[0]),
        y: num(v.y ?? v[1]),
        z: num(v.z ?? v[2]),
        bulge: num(v.bulge, 0),
      });
    });
  }
  if (verts.length === 0 && Array.isArray(entity?.points)) {
    entity.points.forEach((v, index) => {
      verts.push({ id: `${entity.type || 'p'}_${index + 1}`, x: num(v.x ?? v[0]), y: num(v.y ?? v[1]), z: num(v.z ?? v[2]), bulge: num(v.bulge, 0) });
    });
  }
  if (verts.length === 0 && Array.isArray(entity?.controlPoints)) {
    entity.controlPoints.forEach((v, index) => {
      verts.push({ id: `${entity.type || 'cp'}_${index + 1}`, x: num(v.x), y: num(v.y), z: num(v.z), bulge: 0 });
    });
  }
  if (verts.length === 0 && entity?.type === 'LINE') {
    const a = entity?.start || entity?.p1 || { x: entity?.['10'], y: entity?.['20'], z: entity?.['30'] };
    const b = entity?.end || entity?.p2 || { x: entity?.['11'], y: entity?.['21'], z: entity?.['31'] };
    verts.push({ id: 'v1', x: num(a.x), y: num(a.y), z: num(a.z), bulge: 0 });
    verts.push({ id: 'v2', x: num(b.x), y: num(b.y), z: num(b.z), bulge: 0 });
  }
  return verts;
}

function inferSymbolClass({ layer, blockName = '', label = '' }) {
  const hay = `${lower(layer)} ${lower(blockName)} ${lower(label)}`;
  if (!hay.trim()) return null;
  if (hay.includes('support') || hay.includes('shoe') || hay.includes('guide') || hay.includes('hanger') || hay.includes('rest')) {
    return { kind: 'support', type: 'REST' };
  }
  for (const entry of INLINE_TOKEN_MAP) {
    if (entry.tokens.some((token) => hay.includes(token))) return { kind: 'inline', type: entry.type };
  }
  if (hay.includes('bend') || hay.includes('elbow')) return { kind: 'fitting', type: 'BEND' };
  return null;
}

function simpleEntityMetadata(entity, layer, extra = {}) {
  return {
    ...extra,
    layer,
    imported: {
      dxf: {
        layer,
        handle: getEntityHandle(entity),
        entityType: text(entity?.type || 'UNKNOWN'),
        blockName: getBlockName(entity),
        colorIndex: getColorIndex(entity),
      },
    },
  };
}

function createBundleAccumulator(options, report) {
  const bundle = { nodes: {}, segments: {}, inlineItems: {}, supports: {}, fittings: {}, underlayImages: {} };
  const layers = new Map();
  const nodeByKey = new Map();
  let nextNode = 1;
  let nextSegment = 1;
  let nextInline = 1;
  let nextSupport = 1;
  let nextFitting = 1;

  function touchLayer(layer, entity) {
    if (!layers.has(layer)) {
      layers.set(layer, {
        id: layer,
        name: layer,
        color: '#94a3b8',
        metadata: { colorIndex: getColorIndex(entity) },
      });
    }
  }

  function addNode(pt, kind = 'PIPE_ENDPOINT') {
    const key = keyForPoint(pt.x, pt.y, pt.z, options.nodePrecision ?? 4);
    if (nodeByKey.has(key)) return nodeByKey.get(key);
    const id = uid('dxf_node', nextNode++);
    bundle.nodes[id] = { id, x: roundValue(pt.x), y: roundValue(pt.y), z: roundValue(pt.z), kind };
    nodeByKey.set(key, id);
    return id;
  }

  function addSegment(a, b, layer, metadata = {}, geometryKind = 'line') {
    if (dist(a, b) <= num(options.minSegmentLength, 0.0001)) return null;
    touchLayer(layer, metadata?.imported?.dxf ? { colorNumber: metadata.imported.dxf.colorIndex } : null);
    const startNodeId = addNode(a, 'PIPE_ENDPOINT');
    const endNodeId = addNode(b, 'PIPE_ENDPOINT');
    const id = uid('dxf_seg', nextSegment++);
    bundle.segments[id] = {
      id,
      startNodeId,
      endNodeId,
      geometryKind,
      points: [
        { id: `${id}_a`, x: roundValue(a.x), y: roundValue(a.y), z: roundValue(a.z) },
        { id: `${id}_b`, x: roundValue(b.x), y: roundValue(b.y), z: roundValue(b.z) },
      ],
      sizeSpecFields: {
        bore: num(options.defaultBore, 0) || undefined,
        specKey: text(options.defaultSpecKey),
      },
      metadata,
    };
    report.imported.segments += 1;
    return id;
  }

  function addPolyline(points, layer, metadata = {}, closed = false, geometryKind = 'polyline') {
    const safePts = safeArray(points);
    for (let i = 0; i < safePts.length - 1; i += 1) addSegment(safePts[i], safePts[i + 1], layer, metadata, geometryKind);
    if (closed && safePts.length > 2) addSegment(safePts[safePts.length - 1], safePts[0], layer, metadata, geometryKind);
  }

  function addInlineItem(center, type, layer, metadata = {}) {
    touchLayer(layer, metadata?.imported?.dxf ? { colorNumber: metadata.imported.dxf.colorIndex } : null);
    const id = uid('dxf_inline', nextInline++);
    bundle.inlineItems[id] = {
      id,
      type,
      insertionStation: 0.5,
      occupiedLength: num(metadata?.occupiedLength, options.defaultInlineLength || 100),
      x: roundValue(center.x),
      y: roundValue(center.y),
      angle: num(metadata?.angle, 0),
      reducerType: metadata?.reducerType,
      metadata,
    };
    report.imported.inlineItems += 1;
    return id;
  }

  function addSupport(center, supportType, layer, metadata = {}) {
    touchLayer(layer, metadata?.imported?.dxf ? { colorNumber: metadata.imported.dxf.colorIndex } : null);
    const id = uid('dxf_support', nextSupport++);
    const nodeId = addNode(center, 'SUPPORT');
    bundle.supports[id] = {
      id,
      nodeId,
      supportType,
      x: roundValue(center.x),
      y: roundValue(center.y),
      metadata,
    };
    report.imported.supports += 1;
    return id;
  }

  function addFitting(center, type, layer, metadata = {}) {
    touchLayer(layer, metadata?.imported?.dxf ? { colorNumber: metadata.imported.dxf.colorIndex } : null);
    const id = uid('dxf_fit', nextFitting++);
    bundle.fittings[id] = {
      id,
      type,
      x: roundValue(center.x),
      y: roundValue(center.y),
      angle: num(metadata?.angle, 0),
      radius: Number.isFinite(num(metadata?.radius, NaN)) ? num(metadata.radius) : undefined,
      angleDeg: Number.isFinite(num(metadata?.angleDeg, NaN)) ? num(metadata.angleDeg) : undefined,
      startPoint: metadata?.startPoint,
      endPoint: metadata?.endPoint,
      centerPoint: metadata?.centerPoint,
      branchPoint: metadata?.branchPoint,
      metadata,
    };
    report.imported.fittings += 1;
    return id;
  }

  return { bundle, layers, addNode, addSegment, addPolyline, addInlineItem, addSupport, addFitting, touchLayer };
}

function approximateArc(center, radius, startAngleDeg, endAngleDeg, segmentCount = 16) {
  const safeSegments = Math.max(4, Number(segmentCount) || 16);
  const start = degToRad(startAngleDeg);
  const end = degToRad(endAngleDeg);
  const sweep = end - start;
  const pts = [];
  for (let i = 0; i <= safeSegments; i += 1) {
    const t = start + (sweep * i) / safeSegments;
    pts.push({ x: center.x + radius * Math.cos(t), y: center.y + radius * Math.sin(t), z: center.z || 0 });
  }
  return pts;
}

function parsePairs(textContent) {
  const lines = String(textContent || '').split(/\r?\n/);
  const entities = [];
  for (let i = 0; i < lines.length - 1; i += 2) {
    const code = lines[i]?.trim();
    const value = lines[i + 1]?.trim();
    if (code === '0' && ['LINE', 'ARC', 'CIRCLE', 'TEXT', 'LWPOLYLINE', 'POLYLINE', 'VERTEX', 'POINT', 'INSERT'].includes(value)) {
      const entity = { type: value };
      i += 2;
      const vertices = [];
      for (; i < lines.length - 1; i += 2) {
        const c = lines[i]?.trim();
        const v = lines[i + 1]?.trim();
        if (c === '0') {
          if (value === 'POLYLINE' && entity.type !== 'VERTEX' && v === 'VERTEX') {
            const vertex = {};
            i += 2;
            for (; i < lines.length - 1; i += 2) {
              const vc = lines[i]?.trim();
              const vv = lines[i + 1]?.trim();
              if (vc === '0') {
                i -= 2;
                break;
              }
              vertex[vc] = vv;
            }
            vertices.push({ x: num(vertex['10']), y: num(vertex['20']), z: num(vertex['30']), bulge: num(vertex['42']) });
            continue;
          }
          i -= 2;
          break;
        }
        entity[c] = v;
        if (value === 'LWPOLYLINE' && c === '10') {
          const x = num(v);
          const yCode = lines[i + 2]?.trim();
          const yVal = lines[i + 3]?.trim();
          if (yCode === '20') {
            vertices.push({ x, y: num(yVal), z: 0 });
            i += 2;
          }
        }
      }
      if (vertices.length) entity.vertices = vertices;
      entities.push(entity);
    }
  }
  return { entities, header: {}, blocks: {} };
}

async function tryParserByName(moduleName, textContent) {
  try {
    const mod = await import(/* @vite-ignore */ moduleName);
    if (moduleName === 'dxf-parser') {
      const Parser = mod.default || mod.DxfParser || mod;
      const parser = new Parser();
      const parsed = typeof parser.parseSync === 'function' ? parser.parseSync(textContent) : parser.parse(textContent);
      return { engine: 'dxf-parser', parsed: await Promise.resolve(parsed) };
    }
    if (moduleName === '@dxfjs/parser') {
      const Parser = mod.Parser || mod.default?.Parser || mod.default;
      const parser = new Parser();
      const parsed = await parser.parse(textContent);
      return { engine: '@dxfjs/parser', parsed };
    }
  } catch {
    return null;
  }
  return null;
}

export async function Pro2D_parseDxfText(textContent) {
  const viaDxfParser = await tryParserByName('dxf-parser', textContent);
  if (viaDxfParser) return viaDxfParser;
  const viaDxfJs = await tryParserByName('@dxfjs/parser', textContent);
  if (viaDxfJs) return viaDxfJs;
  return { engine: 'fallback-simple', parsed: parsePairs(textContent) };
}

export function Pro2D_importSimpleDxf(textContent) {
  return parsePairs(textContent).entities;
}

function collectEntities(parsed) {
  return safeArray(parsed?.entities || parsed?.modelSpace || parsed?.modelspace || []);
}

function entityIsClosed(entity) {
  return Boolean(entity?.shape || entity?.closed || entity?.isClosed || Number(entity?.['70']) === 1);
}

function nearestSegmentId(bundle, center) {
  let bestId = null;
  let bestDist = Number.POSITIVE_INFINITY;
  Object.values(bundle.segments || {}).forEach((seg) => {
    const a = seg.points?.[0];
    const b = seg.points?.[seg.points.length - 1];
    if (!a || !b) return;
    const mx = (num(a.x) + num(b.x)) / 2;
    const my = (num(a.y) + num(b.y)) / 2;
    const d = Math.hypot(num(center.x) - mx, num(center.y) - my);
    if (d < bestDist) {
      bestDist = d;
      bestId = seg.id;
    }
  });
  return bestId;
}

function attachTextMetadata(bundle, report, options) {
  if (!Array.isArray(report.extractedTexts) || report.extractedTexts.length === 0) return;
  const maxDist = num(options.textAttachMaxDistance, 30);
  report.extractedTexts.forEach((entry) => {
    let target = null;
    let targetCollection = null;
    let bestDist = Number.POSITIVE_INFINITY;
    [['inlineItems', bundle.inlineItems], ['supports', bundle.supports], ['fittings', bundle.fittings], ['segments', bundle.segments]].forEach(([collectionName, collection]) => {
      Object.values(collection || {}).forEach((entity) => {
        const x = entity.x ?? entity.points?.[0]?.x;
        const y = entity.y ?? entity.points?.[0]?.y;
        if (!Number.isFinite(num(x, NaN)) || !Number.isFinite(num(y, NaN))) return;
        const d = Math.hypot(num(entry.x) - num(x), num(entry.y) - num(y));
        if (d < bestDist) {
          bestDist = d;
          target = entity;
          targetCollection = collectionName;
        }
      });
    });
    if (target && bestDist <= maxDist) {
      target.metadata = target.metadata || {};
      target.metadata.imported = target.metadata.imported || {};
      target.metadata.imported.dxf = target.metadata.imported.dxf || {};
      target.metadata.imported.dxf.attachedText = entry.value;
      target.metadata.imported.dxf.attachedTextEntityType = entry.entityType;
      target.metadata.imported.dxf.attachedTextDistance = Number(bestDist.toFixed(2));
      if (!target.metadata.label && targetCollection !== 'segments') target.metadata.label = entry.value;
    }
  });
}

function explodeOrClassifyInsert(entity, tx, blockMap, ctx) {
  const layer = getLayerName(entity);
  const blockName = getBlockName(entity);
  const position = transformPoint(getEntityPoint(entity), tx);
  const meta = simpleEntityMetadata(entity, layer, { blockName, transform: tx });
  const symbolClass = inferSymbolClass({ layer, blockName, label: blockName });

  if (symbolClass?.kind === 'support') {
    ctx.addSupport(position, symbolClass.type || 'REST', layer, meta);
    return;
  }
  if (symbolClass?.kind === 'inline') {
    ctx.addInlineItem(position, symbolClass.type, layer, meta);
    return;
  }
  if (symbolClass?.kind === 'fitting') {
    ctx.addFitting(position, symbolClass.type, layer, { ...meta, centerPoint: position });
    return;
  }

  const blockEntities = blockMap.get(blockName);
  if (ctx.options.explodeBlocks !== false && Array.isArray(blockEntities) && blockEntities.length > 0) {
    normalizeEntities(blockEntities, blockMap, ctx, {
      offsetX: position.x,
      offsetY: position.y,
      offsetZ: position.z,
      scaleX: tx.scaleX,
      scaleY: tx.scaleY,
      scaleZ: tx.scaleZ,
      rotation: tx.rotation,
    });
    return;
  }

  ctx.report.imported.ignored += 1;
  ctx.report.ignoredEntities.push({ type: 'INSERT', blockName, layer, reason: 'Unsupported insert without recognized symbol mapping or explodable block' });
}

function normalizeEntities(entities, blockMap, ctx, tx = { offsetX: 0, offsetY: 0, offsetZ: 0, scaleX: 1, scaleY: 1, scaleZ: 1, rotation: 0 }) {
  safeArray(entities).forEach((entity) => {
    const entityType = text(entity?.type || 'UNKNOWN').toUpperCase();
    bumpCount(ctx.report.entityCounts, entityType);
    const layer = getLayerName(entity);
    ctx.touchLayer(layer, entity);
    const metadata = simpleEntityMetadata(entity, layer, { transform: tx });

    if (entityType === 'INSERT') {
      explodeOrClassifyInsert(entity, { ...tx, ...getEntityScale(entity), rotation: getEntityRotationDeg(entity), offsetX: transformPoint(getEntityPoint(entity), tx).x, offsetY: transformPoint(getEntityPoint(entity), tx).y, offsetZ: transformPoint(getEntityPoint(entity), tx).z }, blockMap, ctx);
      return;
    }

    if (entityType === 'LINE') {
      const verts = normalizeVertices(entity).map((pt) => transformPoint(pt, tx));
      if (verts.length >= 2) ctx.addSegment(verts[0], verts[1], layer, metadata, 'line');
      return;
    }

    if (entityType === 'LWPOLYLINE' || entityType === 'POLYLINE') {
      const verts = normalizeVertices(entity).map((pt) => transformPoint(pt, tx));
      if (verts.length >= 2) ctx.addPolyline(verts, layer, metadata, entityIsClosed(entity), 'polyline');
      else {
        ctx.report.imported.ignored += 1;
        ctx.report.ignoredEntities.push({ type: entityType, layer, reason: 'Polyline has fewer than 2 vertices' });
      }
      return;
    }

    if (entityType === 'SPLINE') {
      const verts = normalizeVertices(entity).map((pt) => transformPoint(pt, tx));
      if (verts.length >= 2) {
        ctx.addPolyline(verts, layer, metadata, false, 'spline');
      } else {
        ctx.report.imported.ignored += 1;
        ctx.report.ignoredEntities.push({ type: entityType, layer, reason: 'Spline missing control points' });
      }
      return;
    }

    if (entityType === 'ARC') {
      const center = transformPoint(entity.center || { x: entity['10'], y: entity['20'], z: entity['30'] }, tx);
      const radius = num(entity.radius ?? entity['40']);
      const startAngle = num(entity.startAngle ?? entity['50']);
      const endAngle = num(entity.endAngle ?? entity['51']);
      const avgScale = averageAbs(tx.scaleX, tx.scaleY);
      const symbolClass = inferSymbolClass({ layer, blockName: getBlockName(entity), label: getEntityText(entity) }) || { kind: 'fitting', type: 'BEND' };
      const startPoint = { x: roundValue(center.x + radius * avgScale * Math.cos(degToRad(startAngle))), y: roundValue(center.y + radius * avgScale * Math.sin(degToRad(startAngle))) };
      const endPoint = { x: roundValue(center.x + radius * avgScale * Math.cos(degToRad(endAngle))), y: roundValue(center.y + radius * avgScale * Math.sin(degToRad(endAngle))) };
      if (ctx.options.arcMode === 'segmentize') {
        const pts = approximateArc(center, radius * avgScale, startAngle, endAngle, ctx.options.arcSegments || 12);
        ctx.addPolyline(pts, layer, metadata, false, 'polyline');
      } else {
        ctx.addFitting(center, symbolClass.type || 'BEND', layer, {
          ...metadata,
          radius: roundValue(radius * avgScale),
          angleDeg: roundValue(endAngle - startAngle),
          angle: startAngle,
          startPoint,
          endPoint,
          centerPoint: center,
        });
      }
      return;
    }

    if (entityType === 'CIRCLE') {
      const center = transformPoint(entity.center || { x: entity['10'], y: entity['20'], z: entity['30'] }, tx);
      const radius = roundValue(num(entity.radius ?? entity['40']) * averageAbs(tx.scaleX, tx.scaleY));
      const symbolClass = inferSymbolClass({ layer, blockName: getBlockName(entity), label: getEntityText(entity) });
      if (symbolClass?.kind === 'support') {
        ctx.addSupport(center, symbolClass.type || 'REST', layer, { ...metadata, radius });
        return;
      }
      if (symbolClass?.kind === 'inline') {
        ctx.addInlineItem(center, symbolClass.type, layer, { ...metadata, occupiedLength: radius * 2 });
        return;
      }
      if (ctx.options.circleMode === 'segmentize') {
        const pts = approximateArc(center, radius, 0, 360, ctx.options.circleSegments || 24);
        ctx.addPolyline(pts, layer, { ...metadata, sourceShape: 'CIRCLE' }, true, 'polyline');
        return;
      }
      ctx.report.imported.ignored += 1;
      ctx.report.ignoredEntities.push({ type: entityType, layer, reason: 'Circle requires layer/block heuristics or circleMode=segmentize', radius });
      return;
    }

    if (entityType === 'POINT') {
      const pt = transformPoint(getEntityPoint(entity), tx);
      ctx.addSupport(pt, 'POINT', layer, metadata);
      return;
    }

    if (entityType === 'TEXT' || entityType === 'MTEXT') {
      const pt = transformPoint(getEntityPoint(entity), tx);
      const value = getEntityText(entity);
      ctx.report.extractedTexts.push({ x: pt.x, y: pt.y, value, layer, entityType, handle: getEntityHandle(entity) });
      const symbolClass = inferSymbolClass({ layer, blockName: getBlockName(entity), label: value });
      if (symbolClass?.kind === 'support') {
        ctx.addSupport(pt, symbolClass.type || 'REST', layer, { ...metadata, text: value });
      } else if (symbolClass?.kind === 'inline') {
        ctx.addInlineItem(pt, symbolClass.type, layer, { ...metadata, text: value });
      }
      return;
    }

    ctx.report.imported.ignored += 1;
    ctx.report.ignoredEntities.push({ type: entityType, layer, reason: 'Unsupported DXF entity for Pro 2D importer' });
  });
}

function inferUnits(parsed) {
  const code = num(parsed?.header?.$INSUNITS ?? parsed?.header?.INSUNITS, 0);
  return INSUNITS_MAP[code] || 'mm';
}

function routeIdForLayer(layer) {
  return `dxf_route_${String(layer || '0').replace(/[^a-zA-Z0-9_]+/g, '_')}`;
}

function applySupportHosts(bundle) {
  Object.values(bundle.supports || {}).forEach((support) => {
    const hostEntityId = nearestSegmentId(bundle, support);
    support.metadata = support.metadata || {};
    support.metadata.hostEntityId = hostEntityId || null;
  });
}

function bundleToCanonicalState(bundle, layers, report, options = {}) {
  const state = Pro2D_createEmptyState(options.documentName || options.fileName || 'DXF Import');
  state.document.sourceKinds = ['dxf'];
  state.document.units = options.units || 'mm';
  state.layers = Object.fromEntries(Array.from(layers.entries()));
  if (!state.layers.Default) state.layers.Default = { id: 'Default', name: 'Default', color: '#94a3b8' };

  state.headers.dynamic['metadata.imported.dxf.layer'] = { key: 'metadata.imported.dxf.layer', label: 'DXF Layer', group: 'dynamic', editable: false, sourceKind: 'dxf' };
  state.headers.dynamic['metadata.imported.dxf.handle'] = { key: 'metadata.imported.dxf.handle', label: 'DXF Handle', group: 'dynamic', editable: false, sourceKind: 'dxf' };
  state.headers.dynamic['metadata.imported.dxf.entityType'] = { key: 'metadata.imported.dxf.entityType', label: 'DXF Entity Type', group: 'dynamic', editable: false, sourceKind: 'dxf' };
  state.headers.dynamic['metadata.imported.dxf.blockName'] = { key: 'metadata.imported.dxf.blockName', label: 'DXF Block Name', group: 'dynamic', editable: false, sourceKind: 'dxf' };
  state.headers.dynamic['metadata.imported.dxf.attachedText'] = { key: 'metadata.imported.dxf.attachedText', label: 'DXF Attached Text', group: 'dynamic', editable: false, sourceKind: 'dxf' };

  Object.values(bundle.nodes || {}).forEach((node) => {
    state.nodes[node.id] = { id: node.id, pt: { x: num(node.x), y: num(node.y), z: num(node.z) }, kind: node.kind || 'PIPE_ENDPOINT', entityIds: [] };
  });

  const routeMap = new Map();

  Object.values(bundle.segments || {}).forEach((seg) => {
    const layerId = seg.metadata?.layer || 'Default';
    const routeId = routeIdForLayer(layerId);
    routeMap.set(routeId, routeMap.get(routeId) || { id: routeId, entityIds: [], startNodeId: seg.startNodeId, endNodeId: seg.endNodeId, routeKind: 'PRIMARY' });
    routeMap.get(routeId).entityIds.push(seg.id);
    routeMap.get(routeId).endNodeId = seg.endNodeId;

    state.entities[seg.id] = {
      id: seg.id,
      type: 'PIPE',
      routeId,
      layerId,
      geometry: { nodeIds: [seg.startNodeId, seg.endNodeId] },
      topology: { connectionNodeIds: [seg.startNodeId, seg.endNodeId], prevEntityId: null, nextEntityId: null },
      engineering: { nd: num(seg.sizeSpecFields?.bore, 0), specKey: text(seg.sizeSpecFields?.specKey) },
      display: { visible: true, label: seg.id },
      metadata: seg.metadata || {},
      provenance: [{ sourceKind: 'dxf', fileName: report.fileName }],
      dynamic: {},
    };
    if (state.nodes[seg.startNodeId]) state.nodes[seg.startNodeId].entityIds.push(seg.id);
    if (state.nodes[seg.endNodeId]) state.nodes[seg.endNodeId].entityIds.push(seg.id);
  });

  Object.values(bundle.inlineItems || {}).forEach((item) => {
    const type = String(item.type || 'valve').toUpperCase();
    const routeId = routeIdForLayer(item.metadata?.layer || 'Default');
    state.entities[item.id] = {
      id: item.id,
      type,
      routeId,
      layerId: item.metadata?.layer || 'Default',
      geometry: { nodeIds: [], center: { x: num(item.x), y: num(item.y) } },
      topology: { connectionNodeIds: [], attachmentRole: 'INLINE' },
      engineering: { reducerType: item.reducerType, occupiedLength: item.occupiedLength },
      display: { visible: true, label: item.metadata?.label || item.id },
      metadata: item.metadata || {},
      provenance: [{ sourceKind: 'dxf', fileName: report.fileName }],
      dynamic: {},
    };
  });

  Object.values(bundle.supports || {}).forEach((support) => {
    const hostEntityId = support.metadata?.hostEntityId || nearestSegmentId(bundle, support) || null;
    state.entities[support.id] = {
      id: support.id,
      type: 'SUPPORT',
      layerId: support.metadata?.layer || 'Default',
      geometry: {
        nodeIds: support.nodeId ? [support.nodeId] : [],
        center: { x: num(support.x), y: num(support.y) },
        anchorRefs: hostEntityId ? [{ hostEntityId, hostNodeId: support.nodeId }] : [],
      },
      topology: {
        connectionNodeIds: support.nodeId ? [support.nodeId] : [],
        attachedToEntityId: hostEntityId,
        attachedAtNodeId: support.nodeId || null,
        attachmentRole: 'POINT',
      },
      engineering: { supportType: support.supportType || 'REST' },
      display: { visible: true, label: support.id },
      metadata: support.metadata || {},
      provenance: [{ sourceKind: 'dxf', fileName: report.fileName }],
      dynamic: {},
    };
    if (support.nodeId && state.nodes[support.nodeId]) state.nodes[support.nodeId].entityIds.push(support.id);
  });

  Object.values(bundle.fittings || {}).forEach((fit) => {
    state.entities[fit.id] = {
      id: fit.id,
      type: fit.type,
      routeId: routeIdForLayer(fit.metadata?.layer || 'Default'),
      layerId: fit.metadata?.layer || 'Default',
      geometry: {
        nodeIds: [],
        center: { x: num(fit.x), y: num(fit.y) },
        radius: fit.radius,
        angleDeg: fit.angleDeg,
      },
      topology: { connectionNodeIds: [] },
      engineering: {},
      display: { visible: true, label: fit.id },
      metadata: fit.metadata || {},
      provenance: [{ sourceKind: 'dxf', fileName: report.fileName }],
      dynamic: {},
    };
  });

  state.routes = Object.fromEntries(Array.from(routeMap.entries()));
  state.provenance.push({
    sourceKind: 'dxf',
    fileName: report.fileName,
    importedAt: new Date().toISOString(),
    engine: report.engine,
    importedSummary: { ...report.imported },
  });
  return state;
}

export async function Pro2D_importDxfToSceneBundle(textContent, options = {}) {
  const parseResult = await Pro2D_parseDxfText(textContent);
  const report = createImportReport(options.fileName || options.documentName || 'DXF');
  report.engine = parseResult.engine;

  const ctx = {
    options: {
      defaultBore: options.defaultBore ?? 250,
      defaultSpecKey: options.defaultSpecKey ?? '',
      defaultInlineLength: options.defaultInlineLength ?? 100,
      nodePrecision: options.nodePrecision ?? 4,
      minSegmentLength: options.minSegmentLength ?? 0.0001,
      arcMode: options.arcMode ?? 'fitting',
      circleMode: options.circleMode ?? 'report',
      circleSegments: options.circleSegments ?? 24,
      arcSegments: options.arcSegments ?? 12,
      explodeBlocks: options.explodeBlocks ?? true,
      textAttachMaxDistance: options.textAttachMaxDistance ?? 30,
    },
    report,
    ...createBundleAccumulator(options, report),
  };

  const blockMap = buildBlockMap(parseResult.parsed);
  normalizeEntities(collectEntities(parseResult.parsed), blockMap, ctx);
  applySupportHosts(ctx.bundle);
  attachTextMetadata(ctx.bundle, report, ctx.options);
  report.layers = Array.from(ctx.layers.keys()).sort();

  return {
    bundle: ctx.bundle,
    layers: ctx.layers,
    report,
    units: inferUnits(parseResult.parsed),
    parsed: parseResult.parsed,
  };
}

export async function Pro2D_importDxfToState(textContent, options = {}) {
  const result = await Pro2D_importDxfToSceneBundle(textContent, options);
  const doc = bundleToCanonicalState(result.bundle, result.layers, result.report, {
    ...options,
    units: result.units,
  });
  return { ...result, doc };
}

export function Pro2D_exportSimpleDxf(scene = {}) {
  const out = ['0', 'SECTION', '2', 'ENTITIES'];
  const segments = Object.values(scene.segments || {});
  for (const seg of segments) {
    const pts = seg.points || [];
    const a = pts[0];
    const b = pts[pts.length - 1];
    if (!a || !b) continue;
    out.push('0', 'LINE', '8', String(seg.metadata?.layer || 'PRO2D'), '10', fmt(a.x), '20', fmt(a.y), '11', fmt(b.x), '21', fmt(b.y));
  }
  const fittings = Object.values(scene.fittings || {});
  for (const fit of fittings) {
    if (fit.type === 'BEND' && fit.centerPoint && Number.isFinite(fit.radius)) {
      out.push('0', 'ARC', '8', String(fit.metadata?.layer || 'PRO2D_FIT'), '10', fmt(fit.centerPoint.x), '20', fmt(fit.centerPoint.y), '40', fmt(fit.radius), '50', fmt(fit.angle || 0), '51', fmt((fit.angle || 0) + (fit.angleDeg || 90)));
    } else {
      out.push('0', 'TEXT', '8', String(fit.metadata?.layer || 'PRO2D_FIT'), '10', fmt(fit.x), '20', fmt(fit.y), '1', String(fit.type));
    }
  }
  for (const item of Object.values(scene.inlineItems || {})) {
    out.push('0', 'TEXT', '8', String(item.metadata?.layer || 'PRO2D_INLINE'), '10', fmt(item.x), '20', fmt(item.y), '1', String(item.type).toUpperCase());
  }
  for (const support of Object.values(scene.supports || {})) {
    out.push('0', 'CIRCLE', '8', String(support.metadata?.layer || 'PRO2D_SUPPORT'), '10', fmt(support.x), '20', fmt(support.y), '40', '5');
  }
  out.push('0', 'ENDSEC', '0', 'EOF');
  return out.join('\n');
}
