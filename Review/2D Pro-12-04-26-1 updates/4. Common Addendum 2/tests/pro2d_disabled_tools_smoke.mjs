import assert from 'node:assert/strict';
import {
  Pro2D_toolMap,
  Pro2D_blockedToolIds,
  Pro2D_getBlockedToolMessage,
} from '../js/pro2dcanvas/Pro2D_ToolRegistry.mjs';

const mustStayBlocked = ['measure', 'bend', 'tee'];

for (const id of mustStayBlocked) {
  assert.equal(Pro2D_toolMap[id].implemented, false, `${id} must stay disabled`);
  assert.ok(Pro2D_blockedToolIds.includes(id), `${id} must appear in blocked list`);
  assert.ok(Pro2D_toolMap[id].enableCriteria?.length > 0, `${id} must declare enable criteria`);
  assert.ok(Pro2D_getBlockedToolMessage(Pro2D_toolMap[id]).length > 10, `${id} must have readable blocked message`);
}

assert.ok(Pro2D_toolMap.measure.note.includes('persistent measure overlays'));
assert.ok(Pro2D_toolMap.bend.note.includes('topology-aware'));
assert.ok(Pro2D_toolMap.tee.note.includes('branch'));

console.log('PASS pro2d_disabled_tools_smoke');
