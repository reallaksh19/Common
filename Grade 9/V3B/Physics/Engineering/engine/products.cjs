"use strict";
const { insist, nonempty, indexed } = require("./gates.cjs");
const cores = ["CORE1A", "CORE1B", "CORE2A", "CORE2B"];
const grammars = {
  CORE1A: ["EXPLAIN", "REPRESENT", "WORK", "VERIFY"],
  CORE1B: ["ELICIT", "ATTEMPT", "HINT", "RESOLVE", "GENERALIZE"],
  CORE2A: ["QUESTION", "SETUP", "REPRESENT", "WORK", "VERIFY"],
  CORE2B: ["QUESTION", "ATTEMPT", "SELECT_MODEL", "HINT", "RESOLVE", "TRANSFER_CHECK"]
};
function validateCalibration(cal, requested, policies) {
  if (!requested.some(x => x === "CORE2A" || x === "CORE2B"))
    return { status: "NOT_APPLICABLE" };
  insist(cal && ["KNOWLEDGE", "OWNER_WAIVER"].includes(cal.basis), "E_CAL_REQUIRED", "Core2A/B");
  insist(["STARTER", "PRACTICE", "REVISION", "COMPETITION"].includes(cal.purpose),
    "E_PURPOSE", cal.purpose);
  insist(cal.controls && nonempty(cal.controls.support) &&
    nonempty(cal.controls.question_demand) && nonempty(cal.controls.transfer_demand),
    "E_CONTROLS", "support and demand must be explicit");
  if (cal.basis === "KNOWLEDGE") validatePercent(cal, policies);
  else {
    insist(cal.percent == null && cal.policy_ref == null && cal.source_ref == null,
      "E_WAIVER_PERCENT", "do not invent a percentage");
    insist(cal.waiver && nonempty(cal.waiver.owner_ref) && nonempty(cal.waiver.reason) &&
      nonempty(cal.waiver.authorization_ref), "E_WAIVER_AUTHORITY", "owner record required");
    insist(JSON.stringify(cal.controls) === JSON.stringify(cal.waiver.controls),
      "E_WAIVER_DRIFT", "resolved controls differ from owner");
  }
  return { status: "SPECIFICATION_MATCH", learner_fit: cal.basis === "OWNER_WAIVER" ?
    "OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED" : "PREDICTION_NOT_MASTERY" };
}
function validatePercent(cal, policies) {
  insist(cal.waiver == null && typeof cal.percent === "number" &&
    Number.isFinite(cal.percent) && cal.percent >= 0 && cal.percent <= 100,
    "E_PERCENT", "0..100, no simultaneous waiver");
  insist(nonempty(cal.source_ref) && nonempty(cal.scope) && nonempty(cal.observed_at),
    "E_PERCENT_CONTEXT", "source, scope and date");
  const policy = policies.find(p => p.id === cal.policy_ref);
  insist(policy && nonempty(policy.authorization_ref), "E_CAL_POLICY", cal.policy_ref);
  const matches = policy.bands.filter(b => cal.percent >= b.min && cal.percent <= b.max);
  insist(matches.length === 1, "E_CAL_RANGE", "exactly one policy band must match");
  insist(JSON.stringify(matches[0].controls) === JSON.stringify(cal.controls),
    "E_CAL_DRIFT", "actual controls differ from named policy");
}
function validateQuestion(q, sourceMap, objects) {
  insist(nonempty(q.id) && nonempty(q.stem) && nonempty(q.display_source),
    "E_QUESTION_SOURCE", q.id);
  insist(["FROZEN_SOURCE", "AUTHOR_CREATED", "ADAPTED"].includes(q.origin),
    "E_QUESTION_ORIGIN", q.id);
  if (q.origin === "FROZEN_SOURCE") {
    const source = sourceMap.get(q.source_id);
    insist(source && source.state === "AVAILABLE", "E_SOURCE_HELD", q.id);
    insist(q.original_number === source.original_number &&
      q.stem === source.stem && q.source_digest === source.digest,
      "E_SOURCE_DRIFT", q.id);
  } else {
    insist(q.original_number == null && q.official_claim === false,
      "E_FALSE_OFFICIAL", q.id);
    insist(q.display_source.startsWith(q.origin === "ADAPTED" ? "Adapted" : "Author-created"),
      "E_ORIGIN_LABEL", q.id);
    if (q.origin === "ADAPTED") insist(sourceMap.has(q.parent_source_id), "E_PARENT_SOURCE", q.id);
  }
  insist(objects.has(q.answer_ref) && objects.has(q.explanation_ref), "E_ANSWER_MISSING", q.id);
  insist(objects.get(q.answer_ref).kind === "ANSWER" &&
    objects.get(q.explanation_ref).kind === "EXPLANATION", "E_ANSWER_TYPE", q.id);
  insist(Array.isArray(q.check_refs) && q.check_refs.length > 0 &&
    q.check_refs.every(id => objects.has(id) && objects.get(id).kind === "CHECK"),
    "E_ANSWER_CHECK", q.id);
}
function validateProduct(packet, baseline, sourceRows) {
  insist(cores.includes(packet.core), "E_CORE", packet.core);
  insist(packet.baseline_version === baseline.version, "E_PRODUCT_STALE", packet.id);
  const objects = indexed(packet.objects, "objects");
  for (const obj of objects.values()) insist(nonempty(obj.content), "E_EMPTY_OBJECT", obj.id);
  const coverage = indexed(packet.coverage, "coverage");
  const required = baseline.assets.filter(a => a.applicable_cores.includes(packet.core));
  insist(coverage.size === required.length, "E_COVERAGE_COUNT", packet.id);
  for (const asset of required) validateDisposition(asset, coverage.get(asset.id), objects, packet.core);
  const actions = new Set(packet.actions);
  for (const action of grammars[packet.core]) insist(actions.has(action), "E_CORE_PURPOSE", action);
  insist(packet.actions.every(action => objects.has(packet.action_refs[action])),
    "E_ACTION_EVIDENCE", packet.core);
  const sourceMap = indexed(sourceRows, "sources");
  indexed(packet.questions, "questions");
  for (const question of packet.questions) validateQuestion(question, sourceMap, objects);
  const promptIds = packet.objects.filter(o => o.kind === "PROMPT").map(o => o.id).sort();
  insist(JSON.stringify(promptIds) === JSON.stringify(packet.questions.map(q => q.prompt_ref).sort()),
    "E_EMBEDDED_PROMPT", "every declared prompt must have a question record and answer");
  insist(packet.questions.every(q => objects.get(q.prompt_ref)?.content === q.stem),
    "E_PROMPT_DRIFT", packet.id);
  return { status: "STRUCTURE_CHECKED", mandatory_assets: required.length,
    questions: packet.questions.length, semantic_review: "NOT_RUN", release_authorized: false };
}
function validateDisposition(asset, row, objects, core) {
  insist(row, "E_COVERAGE_MISSING", asset.id);
  insist(["REALIZED", "TRANSFORMED", "REFERENCE", "NOT_APPLICABLE", "HELD"].includes(row.disposition),
    "E_DISPOSITION", asset.id);
  const mandatory = asset.required_cores.includes(core);
  if (mandatory) insist(["REALIZED", "TRANSFORMED"].includes(row.disposition),
    "E_REQUIRED_UNREALIZED", asset.id);
  if (["REALIZED", "TRANSFORMED", "REFERENCE"].includes(row.disposition))
    insist(Array.isArray(row.object_refs) && row.object_refs.length > 0 &&
      row.object_refs.every(id => objects.has(id)), "E_REALIZATION_MISSING", asset.id);
  if (row.disposition !== "REALIZED") insist(nonempty(row.reason), "E_DISPOSITION_REASON", asset.id);
  if (row.disposition === "TRANSFORMED")
    insist(row.parent_asset_id === asset.id && nonempty(row.learner_action),
      "E_TRANSFORMATION", asset.id);
}
module.exports = { validateCalibration, validateQuestion, validateProduct };
