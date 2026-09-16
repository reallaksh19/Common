"use strict";
const G = require("./engine/gates.cjs"), P = require("./engine/products.cjs");
const S = require("./engine/similarity.cjs");
const clone = x => JSON.parse(JSON.stringify(x));
function run(input) {
  const rows = [];
  const ok = (condition, message) => { if (!condition) throw new Error(message); };
  function test(name, fn) {
    try { fn(); rows.push({ name, status: "PASS" }); }
    catch (e) { rows.push({ name, status: "FAIL", detail: e.message }); }
  }
  function rejects(fn, code) {
    let caught;
    try { fn(); } catch (e) { caught = e; }
    ok(caught && caught.code === code, "expected " + code + ", got " + (caught?.code || "accept"));
  }
  function mutateRegistry(name, change, code) {
    test(name, () => { const reg = clone(input.registry); change(reg);
      rejects(() => G.validateRegistry(reg, input.baseline), code); });
  }
  test("Nine registered gates retain 54 explicit obligations", () => {
    const result = G.validateRegistry(input.registry, input.baseline);
    ok(result.gate_count === 9 && input.registry.gates.reduce((n,g) => n+g.obligations.length,0) === 54, "count");
    ok(!result.release_authorized, "structural PASS must not grant release");
  });
  for (const b of input.bindings)
    test("Computed closure: " + b.id, () => {
      const report = G.evaluateTopic(input.registry, input.baseline, b);
      ok(report.closure.length === b.declared_closure.length, "closure");
      if (b.id === "GRAVITY-ADVANCED-HELD") ok(report.authoring === "BLOCKED_SCOPE", "held");
    });
  mutateRegistry("Deleting a required equation fails", r => r.gates[3].obligations.splice(1,1), "E_OBLIGATION_MISSING");
  mutateRegistry("Changing first-law sign fails", r => r.gates[3].obligations[1].statement = "Delta U = Q + W_by", "E_OBLIGATION_DRIFT");
  mutateRegistry("Dropping pressure-work applicability fails", r => r.gates[2].obligations[1].statement = "W = integral p dV always", "E_OBLIGATION_DRIFT");
  mutateRegistry("An unknown gate needs a baseline", r => r.gates.push({...clone(r.gates[0]),id:"NEW"}), "E_BASELINE_GATE_SET");
  mutateRegistry("Unknown prerequisite fails", r => r.gates[0].prerequisites.push("MISSING"), "E_UNKNOWN_GATE");
  mutateRegistry("Prerequisite cycle fails", r => r.gates[0].prerequisites.push(r.gates[3].id), "E_CYCLE");
  mutateRegistry("Claimed validated maturity fails", r => r.gates[3].maturity = "VALIDATED", "E_MATURITY");
  mutateRegistry("Self-approved subject state fails", r => r.gates[3].authority_state = "APPROVED", "E_BASELINE_CONTEXT");
  mutateRegistry("Blank evidence fails", r => r.gates[3].obligations[0].evidence_refs = [], "E_EVIDENCE_DRIFT");
  mutateRegistry("Representation outside dependency scope fails", r => r.gates[3].obligations.find(o=>o.kind==="REPRESENTATION").relation_ids = ["PHY-GR-POTENTIAL-R1"], "E_REP_BINDING_DRIFT");
  mutateRegistry("Easy enrichment research fails", r => r.gates[0].research_brief_ref = "WEB", "E_EASY_RESEARCH");
  mutateRegistry("Hard missing research fails", r => r.gates[3].research_brief_ref = null, "E_RESEARCH_BRIEF");
  mutateRegistry("Changing model scope without baseline review fails", r => r.gates[2].scope = "Any path", "E_BASELINE_CONTEXT");
  mutateRegistry("Dropping one representation-to-equation link fails", r => r.gates[2].obligations.find(o=>o.kind==="REPRESENTATION").relation_ids.pop(), "E_REP_BINDING_DRIFT");
  test("Stale binding version fails", () => {
    const b = clone(input.bindings[0]); b.registry_version = "old";
    rejects(()=>G.evaluateTopic(input.registry,input.baseline,b),"E_STALE_BINDING");
  });
  test("Omitted dependency closure fails", () => {
    const b = clone(input.bindings[0]); b.declared_closure.pop();
    rejects(()=>G.evaluateTopic(input.registry,input.baseline,b),"E_DECLARED_CLOSURE");
  });
  test("A fourth subtopic in one bundle fails", () => {
    const b = clone(input.bindings[1]); b.bundles = [b.selected_gates];
    rejects(()=>G.evaluateTopic(input.registry,input.baseline,b),"E_BUNDLE_SCOPE");
  });
  test("Shared prerequisite change invalidates transitive consumers", () => {
    const after = clone(input.registry); after.gates[2].version = 2;
    const impact = G.changeImpact(input.registry,after,[
      {id:"THERMO",gate_ids:["PHY-TH-FIRST-LAW"]},
      {id:"CYCLE",gate_ids:["PHY-TH-CYCLE"]},
      {id:"GRAVITY",gate_ids:["PHY-GR-NEWTON"]}]);
    ok(impact.invalidate.join(",")==="THERMO,CYCLE" && impact.retain[0]==="GRAVITY","impact");
  });
  test("Adding cycle retains existing first-law artifacts", () => {
    const before = clone(input.registry); before.gates = before.gates.filter(g=>g.id!=="PHY-TH-CYCLE");
    const impact = G.changeImpact(before,input.registry,[
      {id:"THERMO",gate_ids:["PHY-TH-FIRST-LAW"]},{id:"CYCLE",gate_ids:["PHY-TH-CYCLE"]}]);
    ok(impact.invalidate[0]==="CYCLE" && impact.retain[0]==="THERMO","extension");
  });
  for (const packet of input.products)
    test("Actual content-object closure: " + packet.core, () => {
      const report = P.validateProduct(packet,input.coverage,[]);
      ok(report.questions===packet.questions.length && !report.release_authorized,"report");
    });
  function mutateProduct(name, change, code) {
    test(name,()=>{const p=clone(input.products[0]);change(p);
      rejects(()=>P.validateProduct(p,input.coverage,[]),code);});
  }
  mutateProduct("Missing equation realization object fails",p=>p.objects=p.objects.filter(o=>!o.id.endsWith("-WORK")),"E_REALIZATION_MISSING");
  mutateProduct("Mandatory coverage cannot become optional",p=>p.coverage[0].disposition="NOT_APPLICABLE","E_REQUIRED_UNREALIZED");
  mutateProduct("Core-purpose action missing fails",p=>p.actions=p.actions.filter(x=>x!=="EXPLAIN"),"E_CORE_PURPOSE");
  mutateProduct("Answer removed fails",p=>p.objects=p.objects.filter(o=>o.kind!=="ANSWER"),"E_ANSWER_MISSING");
  mutateProduct("Generated item cannot impersonate source",p=>p.questions[0].official_claim=true,"E_FALSE_OFFICIAL");
  mutateProduct("Embedded unanswered prompt fails",p=>p.objects.push({id:"extra",kind:"PROMPT",content:"Why?"}),"E_EMBEDDED_PROMPT");
  test("Frozen number, stem and digest retained",()=>{
    const objects=new Map([["a",{kind:"ANSWER"}],["e",{kind:"EXPLANATION"}],["c",{kind:"CHECK"}]]);
    const source={id:"s",state:"AVAILABLE",original_number:"23(b)",stem:"Owner supplied text",digest:"exact-original-digest"};
    const q={id:"q",stem:source.stem,origin:"FROZEN_SOURCE",display_source:"Owner supplied Q23(b)",
      source_id:"s",original_number:"23(b)",source_digest:source.digest,answer_ref:"a",explanation_ref:"e",check_refs:["c"]};
    P.validateQuestion(q,new Map([["s",source]]),objects);
    rejects(()=>P.validateQuestion({...q,original_number:"24"},new Map([["s",source]]),objects),"E_SOURCE_DRIFT");
    rejects(()=>P.validateQuestion({...q,stem:"rewritten"},new Map([["s",source]]),objects),"E_SOURCE_DRIFT");
  });
  test("Core1 products do not require knowledge",()=>ok(P.validateCalibration(null,["CORE1A","CORE1B"],[]).status==="NOT_APPLICABLE","calibration"));
  test("Core2 absent calibration fails",()=>rejects(()=>P.validateCalibration(null,["CORE2A"],[]),"E_CAL_REQUIRED"));
  const controls={support:"GUIDED",question_demand:"NEAR",transfer_demand:"STRUCTURAL"};
  const policy={id:"SYNTHETIC-POLICY",authorization_ref:"SYNTHETIC-ONLY",bands:[{min:0,max:100,controls}]};
  const cal={basis:"KNOWLEDGE",percent:50,source_ref:"SYNTHETIC",scope:"test bucket",observed_at:"2026-09-14",policy_ref:policy.id,purpose:"COMPETITION",controls};
  test("Known percentage is a prediction, not mastery",()=>ok(P.validateCalibration(cal,["CORE2B"],[policy]).learner_fit==="PREDICTION_NOT_MASTERY","fit"));
  test("Calibration controls cannot silently drift",()=>rejects(()=>P.validateCalibration({...cal,controls:{...controls,support:"NONE"}},["CORE2A"],[policy]),"E_CAL_DRIFT"));
  test("Percentage cannot choose a missing purpose",()=>rejects(()=>P.validateCalibration({...cal,purpose:null},["CORE2A"],[policy]),"E_PURPOSE"));
  test("Invalid percentage fails",()=>rejects(()=>P.validateCalibration({...cal,percent:101},["CORE2A"],[policy]),"E_PERCENT"));
  const waiver={basis:"OWNER_WAIVER",purpose:"STARTER",controls,waiver:{owner_ref:"SYNTHETIC-OWNER",reason:"unknown",authorization_ref:"SYNTHETIC-ONLY",controls}};
  test("Owner-waiver path stays unvalidated against knowledge",()=>ok(P.validateCalibration(waiver,["CORE2B"],[]).learner_fit==="OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED","waiver"));
  test("Waiver cannot be invented without authority",()=>rejects(()=>P.validateCalibration({...waiver,waiver:{reason:"unknown"}},["CORE2A"],[]),"E_WAIVER_AUTHORITY"));
  test("Waiver and percentage cannot coexist",()=>rejects(()=>P.validateCalibration({...waiver,percent:50},["CORE2A"],[]),"E_WAIVER_PERCENT"));
  const prose=Array.from({length:70},(_,i)=>"word"+i).join(" ");
  test("Exact prose is review, not automatic semantic block",()=>{const x=S.compare(prose,prose);ok(x.signal==="HIGH_REVIEW"&&!x.automatic_block,"score");});
  test("Containment catches copied excerpt in a longer passage",()=>{const x=S.compare(prose,prose+" "+Array.from({length:100},(_,i)=>"new"+i).join(" "));ok(x.containment===1&&x.signal==="REVIEW","containment");});
  test("Equation reuse awaits educational judgment",()=>ok(S.adjudicate({}, {reviewer_ref:"synthetic",reason:"essential relation with changed action",classification:"SEMANTIC_REUSE"}).state==="ADJUDICATION_RECORDED","reuse"));
  test("Fading anchor cannot count as independent transfer",()=>ok(S.adjudicate({claims_independent_transfer:true},{reviewer_ref:"synthetic",reason:"same anchor",classification:"FADING_ANCHOR"}).state==="BLOCKED_FALSE_TRANSFER","fading"));
  test("Unreviewed similarity remains pending",()=>ok(S.adjudicate({},null).state==="REVIEW_PENDING","review"));
  test("Thermodynamics oracle: piston work in two unit systems",()=>{
    ok(180*(3.5-1.5)===360 && 180000*0.002===360 && 760-360===400,"oracle");
    ok(input.products[2].objects.find(o=>o.kind==="ANSWER").content.includes("+400"),"visible answer");
  });
  test("Thermodynamics oracle: two paths and reversal",()=>{
    const lower=100*(3-1),upper=300*(3-1),delta=650-lower;
    ok(lower===200&&upper===600&&delta===450&&delta+upper===1050,"paths");
    ok(-1050-(-600)===-450,"reverse");
  });
  test("Gravity oracle: exact and approximate energy errors",()=>{
    for(const x of [0.001,0.01,0.1,1]){
      const exact=x/(1+x),approx=x;
      ok(Math.abs((approx-exact)/exact-x)<1e-12,"energy error");
    }
    ok(Math.abs((1.01**2-1)-0.0201)<1e-12,"different field error");
  });
  test("Gravity oracle: field and escape scaling differ",()=>{
    ok(1/2**2===0.25 && Math.abs(Math.sqrt(1/2)-1/Math.sqrt(2))<1e-15,"ratios");
  });
  for (const product of input.products) test("Published Markdown retains all objects: "+product.core,()=>{
    const document=input.documents[product.core];
    ok(typeof document==="string","document missing");
    for(const object of product.objects)ok(document.includes(object.content),"omitted "+object.id);
  });
  return { status: rows.every(r=>r.status==="PASS")?"PASS":"FAIL", count:rows.length, tests:rows,
    scope:"Structural falsifiers and analytical calculations; no independent subject/learner approval.",
    node_cli:"NOT_RUN", browser_visual:"NOT_RUN", pdf_visual:"NOT_RUN", release_authorized:false };
}
module.exports={run};
