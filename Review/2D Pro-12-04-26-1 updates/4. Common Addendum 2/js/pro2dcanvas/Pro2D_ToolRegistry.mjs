const PLANNED = 'planned';

export const Pro2D_toolRegistry = [
  { id: 'pan', label: 'Pan', icon: '✋', zone: 'navigation', implemented: true, priority: 0 },
  { id: 'select', label: 'Select', icon: '🖱', zone: 'draft', implemented: true, shortcut: 'Esc', priority: 1 },
  { id: 'marquee', label: 'Marquee', icon: '▭', zone: 'draft', implemented: true, note: 'Uses select-mode drag in the viewport.', priority: 2 },
  {
    id: 'measure',
    label: 'Measure',
    icon: '📏',
    zone: 'draft',
    implemented: false,
    status: PLANNED,
    blockedReasonShort: 'No persistent dimension workflow yet.',
    note: 'Keep disabled until persistent measure overlays, chained dimensions, snapping history, and report/export exist.',
    enableCriteria: [
      'two-point and chained measurement commands',
      'persistent dimension objects saved in canonical doc',
      'snapped references that survive pan/zoom/reload',
      'measure report / export from document state'
    ],
    priority: 3
  },
  { id: 'line', label: 'Pipe', icon: '／', zone: 'draft', implemented: true, priority: 4 },
  { id: 'polyline', label: 'Polyline', icon: '〰', zone: 'draft', implemented: true, priority: 5 },
  { id: 'spline', label: 'Spline', icon: '∿', zone: 'draft', implemented: true, priority: 6 },
  {
    id: 'bend',
    label: 'Bend',
    icon: '↷',
    zone: 'fittings',
    implemented: false,
    status: PLANNED,
    blockedReasonShort: 'No topology-safe bend insertion yet.',
    note: 'Keep disabled until bend placement is topology-aware, ASME-driven, and splits upstream/downstream segments correctly.',
    enableCriteria: [
      'route-aware insertion at elbows/turns',
      'spec/radius lookup by size and schedule',
      'upstream/downstream segment splitting with quantity preservation',
      'canonical fitting persistence and export'
    ],
    priority: 7
  },
  {
    id: 'tee',
    label: 'Tee',
    icon: '┬',
    zone: 'fittings',
    implemented: false,
    status: PLANNED,
    blockedReasonShort: 'No branch ownership or route splitting yet.',
    note: 'Keep disabled until tee/olet branch splitting, route ownership, and canonical branch semantics are wired.',
    enableCriteria: [
      'intersection detection and branch validation',
      'main-run / branch-run ownership model',
      'segment splitting at branch node with continuity checks',
      'canonical tee/olet persistence and export'
    ],
    priority: 8
  },
  { id: 'support', label: 'Support', icon: '✚', zone: 'fittings', implemented: true, priority: 9 },
  { id: 'valve', label: 'Valve', icon: '◇', zone: 'fittings', implemented: true, priority: 10 },
  { id: 'flange', label: 'Flange', icon: '▮', zone: 'fittings', implemented: true, priority: 11 },
  { id: 'fvf', label: 'FVF', icon: '▮◇▮', zone: 'fittings', implemented: true, priority: 12 },
  { id: 'reducer', label: 'Reducer', icon: '⬘', zone: 'fittings', implemented: true, priority: 13 },
  { id: 'break', label: 'Break', icon: '✂', zone: 'repair', implemented: false, note: 'Ribbon command exists but no canonical break pipeline is wired.', priority: 14 },
  { id: 'connect', label: 'Connect', icon: '⛓', zone: 'repair', implemented: false, note: 'No connect-endpoints command is implemented.', priority: 15 },
  { id: 'stretch', label: 'Stretch', icon: '↔', zone: 'repair', implemented: false, note: 'No stretch-endpoint command is implemented.', priority: 16 },
  { id: 'gapClean', label: 'Gap Clean', icon: '🧹', zone: 'repair', implemented: false, note: 'Repair placeholder only.', priority: 17 },
  { id: 'overlapSolver', label: 'Overlap', icon: '🧩', zone: 'repair', implemented: false, note: 'Repair placeholder only.', priority: 18 },
  { id: 'underlay', label: 'Underlay', icon: '🖼', zone: 'interop', implemented: true, note: 'Viewport supports underlay images through the store.', priority: 19 },
  { id: 'annotations', label: 'Issues', icon: '💬', zone: 'interop', implemented: false, note: 'Annotation layer is planned, not implemented.', priority: 20 },
  { id: 'minimap', label: 'Radar', icon: '🧭', zone: 'interop', implemented: false, note: 'No minimap/radar component is mounted yet.', priority: 21 }
];

export const Pro2D_toolMap = Object.fromEntries(Pro2D_toolRegistry.map((tool) => [tool.id, tool]));
export const Pro2D_blockedToolIds = Pro2D_toolRegistry.filter((tool) => tool.implemented === false).map((tool) => tool.id);

export function Pro2D_getToolsByZone(zone) {
  return Pro2D_toolRegistry.filter((tool) => tool.zone === zone);
}

export function Pro2D_getLeftRailTools() {
  const leftRailIds = ['pan', 'select', 'marquee', 'measure', 'line', 'bend', 'tee', 'break', 'connect', 'stretch', 'gapClean', 'overlapSolver', 'underlay', 'minimap'];
  return leftRailIds.map((id) => Pro2D_toolMap[id]).filter(Boolean);
}

export function Pro2D_getBlockedToolMessage(tool) {
  if (!tool || tool.implemented !== false) return '';
  const short = tool.blockedReasonShort || tool.note || 'Planned, not implemented yet.';
  return `${tool.label} stays disabled: ${short}`;
}
