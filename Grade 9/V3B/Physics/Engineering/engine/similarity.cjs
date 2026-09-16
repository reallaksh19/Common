"use strict";
function tokens(text) { return text.toLowerCase().match(/[\p{L}\p{N}]+/gu) || []; }
function shingles(words) {
  const result = new Set();
  for (let i = 0; i <= words.length - 5; i++) result.add(words.slice(i, i + 5).join(" "));
  return result;
}
function compare(a, b) {
  const ta = tokens(a), tb = tokens(b), sa = shingles(ta), sb = shingles(tb);
  const intersection = [...sa].filter(x => sb.has(x)).length;
  const union = sa.size + sb.size - intersection;
  const jaccard = union ? intersection / union : null;
  const containment = Math.min(sa.size, sb.size) ? intersection / Math.min(sa.size, sb.size) : null;
  const exact = a.trim() === b.trim() && a.trim().length > 0;
  const eligible = Math.min(ta.length, tb.length) >= 50;
  let signal = exact ? "HIGH_REVIEW" : "NO_LEXICAL_SIGNAL";
  if (!exact && eligible) {
    if (jaccard >= 0.90) signal = "HIGH_REVIEW";
    else if (jaccard >= 0.80 || containment >= 0.80) signal = "REVIEW";
    else if (jaccard >= 0.65) signal = "CANDIDATE";
  }
  return { exact, jaccard, containment, eligible, signal,
    maturity: "ENGINEERING", semantic_verdict: "NOT_ASSESSED", automatic_block: false };
}
function adjudicate(pair, decision) {
  if (!decision || !decision.reviewer_ref || !decision.reason)
    return { state: "REVIEW_PENDING", release_authorized: false };
  const classifications = ["SEMANTIC_REUSE", "PEDAGOGICAL_TRANSFORMATION", "FADING_ANCHOR",
    "STRUCTURAL_SIBLING", "FAR_TRANSFER_SIBLING", "NEAR_DUPLICATE", "PEDAGOGICAL_DUPLICATION"];
  if (!classifications.includes(decision.classification)) throw new Error("E_REUSE_CLASS");
  if (decision.classification === "PEDAGOGICAL_DUPLICATION")
    return { state: "BLOCKED_DUPLICATION", release_authorized: false };
  if (decision.classification === "FADING_ANCHOR" && pair.claims_independent_transfer)
    return { state: "BLOCKED_FALSE_TRANSFER", release_authorized: false };
  return { state: "ADJUDICATION_RECORDED", release_authorized: false };
}
module.exports = { compare, adjudicate };
