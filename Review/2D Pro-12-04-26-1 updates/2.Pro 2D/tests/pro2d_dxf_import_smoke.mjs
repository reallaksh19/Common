import assert from 'node:assert/strict';
import { Pro2D_importDxfToState, Pro2D_exportSimpleDxf } from '../js/pro2dcanvas/Pro2D_DxfAdapter.mjs';
import { Pro2D_toSceneBundle } from '../js/pro2dcanvas/Pro2D_Canonical.mjs';

const sample = [
  '0','SECTION','2','ENTITIES',
  '0','LINE','8','PIPING_MAIN','10','0','20','0','11','100','21','0',
  '0','LWPOLYLINE','8','PIPING_MAIN','90','3','10','100','20','0','10','150','20','50','10','200','20','50',
  '0','ARC','8','PIPING_BEND','10','200','20','50','40','25','50','0','51','90',
  '0','TEXT','8','VALVE_TAG','10','150','20','50','1','Gate Valve',
  '0','CIRCLE','8','SUPPORT_LAYER','10','90','20','0','40','6',
  '0','ENDSEC','0','EOF'
].join('\n');

const { doc, report, bundle } = await Pro2D_importDxfToState(sample, {
  fileName: 'sample-piping.dxf',
  documentName: 'sample-piping',
  defaultBore: 250,
  arcMode: 'fitting',
  circleMode: 'report',
});

assert.equal(report.engine, 'fallback-simple');
assert.equal(report.imported.segments, 3, 'expected 1 line + 2 polyline segments');
assert.equal(report.imported.inlineItems, 1, 'expected valve from text heuristic');
assert.equal(report.imported.supports, 1, 'expected support from layer heuristic');
assert.equal(report.imported.fittings, 1, 'expected bend from ARC');
assert.ok(Object.keys(doc.entities).length >= 6, 'canonical doc should contain imported entities');
assert.ok(Object.keys(doc.routes).length >= 1, 'canonical doc should contain routes');

const dxfOut = Pro2D_exportSimpleDxf(bundle);
assert.ok(dxfOut.includes('SECTION'));
assert.ok(dxfOut.includes('LINE'));
assert.ok(dxfOut.includes('ARC'));

console.log(JSON.stringify({
  ok: true,
  imported: report.imported,
  layers: report.layers,
  entityTotal: Object.keys(doc.entities).length,
  routeTotal: Object.keys(doc.routes).length,
}, null, 2));
