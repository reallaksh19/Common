export const Pro2D_toolRegistry = [
  { id: 'pan', label: 'Pan', icon: '✋', zone: 'navigation', implemented: true, priority: 0 },
  { id: 'select', label: 'Select', icon: '🖱', zone: 'draft', implemented: true, shortcut: 'Esc', priority: 1 },
  { id: 'marquee', label: 'Marquee', icon: '▭', zone: 'draft', implemented: true, note: 'Uses select-mode drag in the viewport.', priority: 2 },
  { id: 'measure', label: 'Measure', icon: '📏', zone: 'draft', implemented: false, note: 'Keep disabled until persistent measure overlays and report export exist.', priority: 3 },
  { id: 'line', label: 'Pipe', icon: '／', zone: 'draft', implemented: true, priority: 4 },
  { id: 'polyline', label: 'Polyline', icon: '〰', zone: 'draft', implemented: true, priority: 5 },
  { id: 'spline', label: 'Spline', icon: '∿', zone: 'draft', implemented: true, priority: 6 },
  { id: 'bend', label: 'Bend', icon: '↷', zone: 'fittings', implemented: false, note: 'Keep disabled until bend placement is topology-aware and ASME-driven.', priority: 7 },
  { id: 'tee', label: 'Tee', icon: '┬', zone: 'fittings', implemented: false, note: 'Keep disabled until tee/olet branch splitting and route ownership are wired.', priority: 8 },
  { id: 'support', label: 'Support', icon: '✚', zone: 'fittings', implemented: true, priority: 9 },
  { id: 'valve', label: 'Valve', icon: '◇', zone: 'fittings', implemented: true, priority: 10 },
  { id: 'flange', label: 'Flange', icon: '▮', zone: 'fittings', implemented: true, priority: 11 },
  { id: 'fvf', label: 'FVF', icon: '▮◇▮', zone: 'fittings', implemented: true, priority: 12 },
  { id: 'reducer', label: 'Reducer', icon: '⬘', zone: 'fittings', implemented: true, priority: 13 },
  { id: 'break', label: 'Break', icon: '✂', zone: 'repair', implemented: true, note: 'Click a segment to split it at the snapped location.', priority: 14 },
  { id: 'connect', label: 'Connect', icon: '⛓', zone: 'repair', implemented: true, note: 'Click two endpoints to bridge a gap with a new pipe segment.', priority: 15 },
  { id: 'stretch', label: 'Stretch', icon: '↔', zone: 'repair', implemented: true, note: 'Click an endpoint, then click a new snapped target to move it.', priority: 16 },
  { id: 'gapClean', label: 'Gap Clean', icon: '🧹', zone: 'repair', implemented: true, note: 'Click once to auto-connect small endpoint gaps.', priority: 17 },
  { id: 'overlapSolver', label: 'Overlap', icon: '🧩', zone: 'repair', implemented: true, note: 'Click once to merge collinear overlapping pipe segments.', priority: 18 },
  { id: 'underlay', label: 'Underlay', icon: '🖼', zone: 'interop', implemented: true, note: 'Viewport supports underlay images through the store.', priority: 19 },
  { id: 'annotations', label: 'Issues', icon: '💬', zone: 'interop', implemented: true, note: 'Click to drop issue markers with note text.', priority: 20 },
  { id: 'minimap', label: 'Radar', icon: '🧭', zone: 'interop', implemented: true, note: 'Activate to show radar/minimap and click it to pan.', priority: 21 }
];

export const Pro2D_toolMap = Object.fromEntries(Pro2D_toolRegistry.map((tool) => [tool.id, tool]));
export function Pro2D_getToolsByZone(zone) { return Pro2D_toolRegistry.filter((tool) => tool.zone === zone); }
export function Pro2D_getLeftRailTools() {
  const leftRailIds = ['pan', 'select', 'marquee', 'measure', 'line', 'break', 'connect', 'stretch', 'gapClean', 'overlapSolver', 'underlay', 'annotations', 'minimap'];
  return leftRailIds.map((id) => Pro2D_toolMap[id]).filter(Boolean);
}
