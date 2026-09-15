import copy
import json
import sys
import unittest
from pathlib import Path
from jsonschema import validate, ValidationError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"resolver"))
from resolve_scope import DependencyCycleError, ScopeInvariantError, canonical_bytes, resolve_canonical_knowledge_set, validate_goal_request, validate_target_scope, validate_learner_study_scope, validate_publication_scope

def load(name): return json.loads((ROOT/"fixtures"/name).read_text(encoding="utf-8"))
def schema(name): return json.loads((ROOT/"contracts"/name).read_text(encoding="utf-8"))

class V203ScopeTests(unittest.TestCase):
    def setUp(self):
        self.registry=load("canonical_registry.synthetic.json"); self.goal=load("learning_goal.synthetic.json"); self.scope=load("canonical_target_scope.synthetic.json"); self.study=load("learner_study_scope.synthetic.json"); self.pub=load("publication_scope.synthetic.json")
    def test_committed_fixtures_validate(self):
        validate(self.registry,schema("canonical-registry-snapshot.schema.json")); validate(self.goal,schema("learning-goal-request.schema.json")); validate(self.scope,schema("canonical-target-scope.schema.json")); validate(self.study,schema("learner-study-scope.schema.json")); validate(self.pub,schema("publication-scope.schema.json")); validate_goal_request(self.goal); validate_target_scope(self.goal,self.scope,self.registry); validate_learner_study_scope(self.scope,self.study); validate_publication_scope(self.study,self.pub)
    def test_cross_subject_dependency_is_composed_not_copied(self):
        out=resolve_canonical_knowledge_set(self.scope,self.registry); validate(out,schema("canonical-knowledge-set.schema.json")); by_id={x["canonical_id"]:x for x in out["dependency_bundles"]}; self.assertEqual(by_id["math.proportional-reasoning"]["resolution_status"],"COMPOSE_DEPENDENCY"); self.assertEqual(by_id["chem.variable-entity.meaning"]["resolution_status"],"REUSE_EXISTING"); self.assertEqual(by_id["math.equality-transform"]["resolution_status"],"REUSE_EXISTING"); forbidden={"definition","formula","rule_text","canonical_payload","semantic_expression"}; [self.assertFalse(forbidden&set(row)) for row in out["dependency_bundles"]]; self.assertEqual(len({x["canonical_id"] for x in out["dependency_bundles"]}),len(out["dependency_bundles"]))
    def test_transitive_dependency_closure_and_exact_binding(self):
        out=resolve_canonical_knowledge_set(self.scope,self.registry); ids={x["canonical_id"] for x in out["dependency_bundles"]}; self.assertIn("math.equality-transform",ids); idx={x["canonical_id"]:x for x in self.registry["assets"]}; [(self.assertEqual(row["version"],idx[row["canonical_id"]]["version"]),self.assertEqual(row["digest"],idx[row["canonical_id"]]["digest"])) for row in out["dependency_bundles"]]
    def test_deterministic_replay(self):
        self.assertEqual(canonical_bytes(resolve_canonical_knowledge_set(self.scope,self.registry)),canonical_bytes(resolve_canonical_knowledge_set(copy.deepcopy(self.scope),copy.deepcopy(self.registry))))
    def test_missing_dependency_becomes_gap_candidate(self):
        reg=copy.deepcopy(self.registry); next(a for a in reg["assets"] if a["canonical_id"]=="chem.gas-law.relationship")["dependencies"].append({"canonical_id":"math.missing-shared-asset","reason":"synthetic missing shared dependency"}); out=resolve_canonical_knowledge_set(self.scope,reg); self.assertIn("math.missing-shared-asset",{x["missing_canonical_id"] for x in out["canonical_gap_candidates"]}); self.assertIn(("math.missing-shared-asset","CANONICAL_GAP_CANDIDATE"),{(x["to_id"],x["status"]) for x in out["resolution_events"]})
    def test_stale_or_version_mismatch_requires_revalidation(self):
        reg=copy.deepcopy(self.registry); next(a for a in reg["assets"] if a["canonical_id"]=="math.proportional-reasoning")["status"]="STALE"; out=resolve_canonical_knowledge_set(self.scope,reg); self.assertEqual({x["canonical_id"]:x for x in out["dependency_bundles"]}["math.proportional-reasoning"]["resolution_status"],"REVALIDATE")
    def test_cycle_fails_closed(self):
        reg=copy.deepcopy(self.registry); next(a for a in reg["assets"] if a["canonical_id"]=="math.equality-transform")["dependencies"].append({"canonical_id":"math.proportional-reasoning","reason":"synthetic cycle"}); self.assertRaises(DependencyCycleError,resolve_canonical_knowledge_set,self.scope,reg)
    def test_mandatory_goal_cannot_be_silently_removed(self):
        bad=copy.deepcopy(self.scope); bad["target_obligations"]=[x for x in bad["target_obligations"] if x["canonical_id"]!="chem.gas-law.relationship"]; self.assertRaises(ScopeInvariantError,validate_target_scope,self.goal,bad,self.registry)
    def test_learner_state_cannot_silently_drop_required_target(self):
        bad=copy.deepcopy(self.study); bad["active_target_ids"]=[]; bad["deferred_required_targets"]=[]; self.assertRaises(ScopeInvariantError,validate_learner_study_scope,self.scope,bad)
    def test_required_target_may_be_explicitly_deferred_without_erasing_goal(self):
        deferred=copy.deepcopy(self.study); deferred["active_target_ids"]=[]; deferred["deferred_required_targets"]=[{"canonical_id":"chem.gas-law.relationship","reason_code":"DEPENDENCY_FIRST","decision_ref":"future-study-decision.synthetic.001"}]; validate_learner_study_scope(self.scope,deferred)
    def test_publication_scope_cannot_redefine_active_scope(self):
        bad=copy.deepcopy(self.pub); bad["selected_target_ids"]=[]; bad["omitted_active_targets"]=[]; self.assertRaises(ScopeInvariantError,validate_publication_scope,self.study,bad)
    def test_publication_scope_can_narrow_only_with_explicit_accounting(self):
        narrowed=copy.deepcopy(self.pub); narrowed["selected_target_ids"]=[]; narrowed["omitted_active_targets"]=[{"canonical_id":"chem.gas-law.relationship","reason_code":"SEQUENCED_TO_LATER_REALIZATION"}]; validate_publication_scope(self.study,narrowed)
    def test_excluded_target_cannot_be_reintroduced(self):
        scoped=copy.deepcopy(self.scope); scoped["target_obligations"]=[scoped["target_obligations"][0]]; scoped["excluded_target_ids"]=["math.coordinate-slope"]; validate_target_scope(self.goal,scoped,self.registry); bad=copy.deepcopy(self.study); bad["added_dependency_target_ids"].append("math.coordinate-slope"); self.assertRaises(ScopeInvariantError,validate_learner_study_scope,scoped,bad)
    def test_benchmark_like_input_key_rejected(self):
        bad=copy.deepcopy(self.goal); bad["benchmark_artifact_ref"]="PR157"; self.assertRaises(ScopeInvariantError,validate_goal_request,bad); self.assertRaises(ValidationError,validate,bad,schema("learning-goal-request.schema.json"))

if __name__=="__main__": unittest.main()
