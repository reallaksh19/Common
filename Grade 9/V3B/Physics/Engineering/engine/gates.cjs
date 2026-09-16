"use strict";
// Structural policy checker. Does not establish scientific truth or reviewer authority.
function insist(condition, code, detail) {
  if (!condition) { const e = new Error(code + ": " + detail); e.code = code; throw e; }
}
function nonempty(x) { return typeof x === "string" && x.trim().length > 0; }
function indexed(rows, label) {
  insist(Array.isArray(rows), "E_SHAPE", label);
  const map = new Map();
  for (const row of rows) {
    insist(row && nonempty(row.id), "E_ID", label);
    insist(!map.has(row.id), "E_DUPLICATE_ID", row.id);
    map.set(row.id, row);
  }
  return map;
}
function closure(map, starts) {
  const done = new Set(), active = new Set();
  function visit(id) {
    insist(map.has(id), "E_UNKNOWN_GATE", id);
    insist(!active.has(id), "E_CYCLE", id);
    if (done.has(id)) return;
    active.add(id);
    for (const dep of map.get(id).prerequisites) visit(dep);
    active.delete(id); done.add(id);
  }
  starts.forEach(visit);
  return [...done].sort();
}
function validateRegistry(registry, baseline) {
  insist(registry.version === baseline.registry_version, "E_BASELINE_VERSION", registry.version);
  const gates = indexed(registry.gates, "gates"), specs = indexed(baseline.gates, "baseline gates");
  insist(gates.size === specs.size && [...gates.keys()].every(id => specs.has(id)),
    "E_BASELINE_GATE_SET", "every new gate needs a separately versioned specification");
  const allAssets = new Map();
  for (const gate of gates.values()) {
    insist(Array.isArray(gate.prerequisites), "E_SHAPE", gate.id);
    const scope = new Set(closure(gates, [gate.id]));
    validateGate(gate, specs.get(gate.id));
    for (const item of gate.obligations) {
      insist(!allAssets.has(item.id), "E_ASSET_DUPLICATE", item.id);
      allAssets.set(item.id, { item, gate: gate.id });
    }
    insist(scope.has(gate.id), "E_CLOSURE", gate.id);
  }
  for (const gate of gates.values()) validateRelations(gate, gates, allAssets);
  return { status: "STRUCTURE_CHECKED", gate_count: gates.size,
    subject_review: "NOT_RUN", release_authorized: false };
}
function validateGate(gate, spec) {
  insist(gate.version === spec.version, "E_GATE_VERSION", gate.id);
  insist(gate.scope === spec.scope && gate.badge === spec.badge &&
    gate.authority_state === spec.authority_state, "E_BASELINE_CONTEXT", gate.id);
  insist(["DRAFT", "SOURCE_HELD"].includes(gate.authority_state), "E_AUTHORITY_STATE", gate.id);
  insist(gate.maturity === "ENGINEERING", "E_MATURITY", gate.id);
  insist(["EASY", "MEDIUM", "HARD"].includes(gate.badge) && nonempty(gate.badge_reason),
    "E_BADGE", gate.id);
  insist(nonempty(gate.title) && nonempty(gate.scope), "E_SCOPE", gate.id);
  const actual = indexed(gate.obligations, gate.id);
  for (const required of spec.required) {
    insist(actual.has(required.id), "E_OBLIGATION_MISSING", required.id);
    const item = actual.get(required.id);
    insist(item.kind === required.kind && item.statement === required.statement,
      "E_OBLIGATION_DRIFT", required.id);
    insist(JSON.stringify(item.relation_ids || []) === JSON.stringify(required.relation_ids || []),
      "E_REP_BINDING_DRIFT", required.id);
    insist(JSON.stringify(item.evidence_refs) === JSON.stringify(required.evidence_refs),
      "E_EVIDENCE_DRIFT", required.id);
    insist(Array.isArray(item.evidence_refs) && item.evidence_refs.length > 0 &&
      item.evidence_refs.every(nonempty), "E_EVIDENCE_REF", required.id);
  }
  insist(actual.size === spec.required.length, "E_UNBASELINED_OBLIGATION", gate.id);
  insist(JSON.stringify([...gate.prerequisites].sort()) ===
    JSON.stringify([...spec.prerequisites].sort()), "E_PREREQUISITE_DRIFT", gate.id);
  const kinds = new Set(gate.obligations.map(o => o.kind));
  for (const kind of ["CONCEPT", "RELATION", "REPRESENTATION", "MISCONCEPTION", "CHECK"])
    insist(kinds.has(kind), "E_TECHNICAL_SECTION", gate.id + ":" + kind);
  if (gate.badge !== "EASY")
    insist(nonempty(gate.research_brief_ref), "E_RESEARCH_BRIEF", gate.id);
  if (gate.badge === "EASY")
    insist(gate.research_brief_ref === null, "E_EASY_RESEARCH", gate.id);
}
function validateRelations(gate, map, allAssets) {
  const allowed = new Set(closure(map, [gate.id]));
  for (const item of gate.obligations.filter(o => o.kind === "REPRESENTATION")) {
    insist(Array.isArray(item.relation_ids) && item.relation_ids.length > 0,
      "E_REP_RELATION", item.id);
    for (const id of item.relation_ids) {
      const target = allAssets.get(id);
      insist(target && target.item.kind === "RELATION" && allowed.has(target.gate),
        "E_REP_SCOPE", item.id + " -> " + id);
    }
  }
}
function evaluateTopic(registry, baseline, binding) {
  validateRegistry(registry, baseline);
  insist(binding.registry_version === registry.version, "E_STALE_BINDING", binding.id);
  const map = indexed(registry.gates, "gates");
  const actual = closure(map, binding.selected_gates);
  insist(JSON.stringify(actual) === JSON.stringify([...binding.declared_closure].sort()),
    "E_DECLARED_CLOSURE", binding.id);
  for (const id of actual)
    insist(binding.gate_versions[id] === map.get(id).version, "E_STALE_GATE", id);
  insist(binding.bundles.length > 0, "E_BUNDLE_EMPTY", binding.id);
  const assigned = binding.bundles.flat();
  insist(binding.bundles.every(b => b.length >= 1 && b.length <= 3) &&
    new Set(assigned).size === assigned.length &&
    JSON.stringify([...assigned].sort()) === JSON.stringify([...binding.selected_gates].sort()),
    "E_BUNDLE_SCOPE", binding.id);
  const held = actual.filter(id => map.get(id).authority_state === "SOURCE_HELD");
  return { topic: binding.id, closure: actual, held_gates: held,
    structure: "STRUCTURE_CHECKED", authoring: held.length ? "BLOCKED_SCOPE" : "DESIGN_PREVIEW_ONLY",
    subject_review: "NOT_RUN", release_authorized: false };
}
function changeImpact(before, after, products) {
  const oldMap = indexed(before.gates, "old"), newMap = indexed(after.gates, "new");
  closure(newMap, [...newMap.keys()]);
  const ids = new Set([...oldMap.keys(), ...newMap.keys()]);
  const changed = [...ids].filter(id => JSON.stringify(oldMap.get(id)) !== JSON.stringify(newMap.get(id)));
  const affected = new Set(changed);
  let repeat = true;
  while (repeat) {
    repeat = false;
    for (const gate of [...oldMap.values(), ...newMap.values()])
      if (!affected.has(gate.id) && gate.prerequisites.some(id => affected.has(id))) {
        affected.add(gate.id); repeat = true;
      }
  }
  return { changed: changed.sort(), affected: [...affected].sort(),
    invalidate: products.filter(p => p.gate_ids.some(id => affected.has(id))).map(p => p.id),
    retain: products.filter(p => !p.gate_ids.some(id => affected.has(id))).map(p => p.id) };
}
module.exports = { insist, nonempty, indexed, closure, validateRegistry, evaluateTopic, changeImpact };
