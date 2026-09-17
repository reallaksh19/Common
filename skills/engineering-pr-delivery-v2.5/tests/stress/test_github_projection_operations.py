from __future__ import annotations
import copy,sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]))
from test_core import good,dump
from validate_github_projection import validate as github_projection
from validate_github_generation_history import validate as generation_history
from validate_projection_convergence import validate as projection_convergence
from validate_issue_projection_tree import validate as issue_tree
from github_projection_next import next_action
from begin_github_operation import begin
from reconcile_github_projection import reconcile
from activate_github_generation import activate


def publication():return {"attempt_count":0,"last_attempt_basis":[],"receipt":None,"last_error":None}
def verification():return {"status":"NOT_RUN","observed_issue_number":None,"observed_issue_id":None,"observed_github_state":None,"observed_relationships":[],"basis":[]}
def operation(oid,kind,node,related=None,depends=None,desired=None,effects=None):
    desired=copy.deepcopy(desired or {})
    if kind in {"CREATE","UPDATE","PUBLISH_HANDOVER","SUPERSEDE","REVISE"}:desired.setdefault("body_marker",f"<!-- relay-operation:{oid} -->")
    return {"id":oid,"kind":kind,"state":"PREPARED","idempotency_key":f"relay:GHGEN-1:{oid}","depends_on":list(depends or []),"subject":{"issue_node":node,"related_nodes":list(related or [])},"preconditions":{},"desired":desired,"publication":publication(),"verification":verification(),"reconciliation":{"issue_graph_effects":list(effects or []),"complete_when":["external desired state verified by readback"]}}

def observation(oid,*,result="VERIFIED",issue_number=11,issue_id="gid-11",github_state="OPEN",marker=True,relationships=None,receipt=None,attempted=False):
    return {"schema_version":"relay-v2.5-github-observation","generation_id":"GHGEN-1","operation_id":oid,"candidate_basis":[f"connector-attempt:{oid}"],"publication":{"attempted":attempted,"receipt":receipt,"error":None},"readback":{"performed":True,"found":github_state!="ABSENT","issue_number":issue_number,"issue_id":issue_id,"github_state":github_state,"marker_present":marker,"relationships":list(relationships or []),"body_digest":"digest","basis":[f"readback:{oid}"]},"result":result,"reason":"synthetic readback"}

def setup_projection(root:Path):
    _,_,_,state=good(root);state["repository"]["remote"]="owner/synthetic"
    graph={"schema_version":"relay-v2.5","graph_revision":"IG-1","nodes":[
        {"id":"ISSUE-PARENT","state":"ACTIVE","github_state":"OPEN","github":{"issue_number":10,"issue_id":"gid-10"},"child_rollup":{"graph_revision":"IG-1","direct_children":[{"id":"ISSUE-CHILD","state":"ACTIVE","github_state":"ABSENT"}],"derived_state":"ACTIVE","all_children_terminal":False}},
        {"id":"ISSUE-CHILD","state":"ACTIVE","github_state":"ABSENT","roadmap_node":"WP-1"}],
        "relationships":[{"from":"ISSUE-PARENT","relation":"PARENT_OF","to":"ISSUE-CHILD"}]}
    relation={"from":"ISSUE-PARENT","relation":"PARENT_OF","to":"ISSUE-CHILD"}
    ops=[
        operation("GHOP-CREATE","CREATE","ISSUE-CHILD",desired={"title":"Child work","body_projection":"source-derived child issue","github_state":"OPEN","relationships":[]},effects=[{"node":"ISSUE-CHILD","set_github_state":"OPEN","set_issue_number":"OBSERVED","set_issue_id":"OBSERVED"}]),
        operation("GHOP-LINK","LINK","ISSUE-CHILD",related=["ISSUE-PARENT"],depends=["GHOP-CREATE"],desired={"relationships":[relation]}),
        operation("GHOP-HANDOVER","PUBLISH_HANDOVER","ISSUE-PARENT",depends=["GHOP-LINK"],desired={"body_projection":"source-derived current handover","relationships":[]})]
    plan={"schema_version":"relay-v2.5-github-projection","generation":{"id":"GHGEN-1","repository":"owner/synthetic","roadmap_revision":"RM-0001","issue_graph_revision":"IG-1","execution_ref":"EP-1","state":"PREPARED","supersedes_generation":None,"basis":["roadmap:RM-0001","issue-graph:IG-1"]},"operations":ops}
    rel="agents/relay/projection/generations/GHGEN-1.yaml";dump(root/rel,plan);dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph)
    state["projection"]={"required":True,"state":"PENDING","operation_id":"GHGEN-1","target":"github:owner/synthetic:issues","adapter":"GITHUB_ISSUES","plan":rel,"roadmap_revision":"RM-0001","execution_ref":"EP-1","receipt":None,"basis":["generation:GHGEN-1"],"observed":None,"superseded_operations":[]}
    state["relay_readiness"].update({"projection_ready":False,"handover_ready":False});dump(root/"agents/relay/REPO_STATE.yaml",state)
    return graph,plan,state

def write_obs(root:Path,doc:dict,name="OBS.yaml"):
    path=root/name;dump(path,doc);return path

class GitHubProjectionOperationStressTests(unittest.TestCase):
    def test_create_link_handover_converges_without_connector_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);relation={"from":"ISSUE-PARENT","relation":"PARENT_OF","to":"ISSUE-CHILD"};setup_projection(root)
            self.assertEqual([],github_projection(root)[0]);self.assertEqual("PUBLISH",next_action(root)["action"])
            first=begin(root,["before-call:GHOP-CREATE"],True);self.assertEqual("GHOP-CREATE",first["operation_id"]);self.assertEqual("RECONCILE",next_action(root)["action"])
            reconcile(root,write_obs(root,observation("GHOP-CREATE",receipt=None,attempted=False)),True)
            plan=yaml.safe_load((root/"agents/relay/projection/generations/GHGEN-1.yaml").read_text());created=plan["operations"][0]
            self.assertEqual(1,created["publication"]["attempt_count"]);self.assertTrue(str(created["publication"]["receipt"]).startswith("READBACK_RECOVERY:"));self.assertEqual("PUBLISH",next_action(root)["action"])
            begin(root,["before-call:GHOP-LINK"],True);reconcile(root,write_obs(root,observation("GHOP-LINK",relationships=[relation],receipt="link-receipt"),"LINK.yaml"),True)
            begin(root,["before-call:GHOP-HANDOVER"],True);reconcile(root,write_obs(root,observation("GHOP-HANDOVER",issue_number=10,issue_id="gid-10",receipt="handover-receipt"),"HANDOVER.yaml"),True)
            self.assertEqual("COMPLETE",next_action(root)["action"]);self.assertEqual([],github_projection(root)[0]);self.assertEqual([],projection_convergence(root)[0]);self.assertEqual([],issue_tree(root)[0])
            state=yaml.safe_load((root/"agents/relay/REPO_STATE.yaml").read_text());graph=yaml.safe_load((root/"agents/relay/roadmap/ISSUE_GRAPH.yaml").read_text());child=next(x for x in graph["nodes"] if x["id"]=="ISSUE-CHILD")
            self.assertEqual("IN_SYNC",state["projection"]["state"]);self.assertTrue(state["relay_readiness"]["projection_ready"]);self.assertEqual(11,child["github"]["issue_number"]);self.assertEqual("OPEN",child["github_state"])

    def test_uncertain_create_must_reconcile_before_retry(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);setup_projection(root);begin(root,["before-call"],True)
            unconfirmed=observation("GHOP-CREATE",result="UNCONFIRMED",issue_number=None,issue_id=None,github_state="UNKNOWN",marker=False,receipt=None,attempted=False);reconcile(root,write_obs(root,unconfirmed),True)
            self.assertEqual("RECONCILE",next_action(root)["action"])
            recovered=observation("GHOP-CREATE",receipt=None,attempted=False);reconcile(root,write_obs(root,recovered,"RECOVERED.yaml"),True)
            plan=yaml.safe_load((root/"agents/relay/projection/generations/GHGEN-1.yaml").read_text());self.assertEqual(1,plan["operations"][0]["publication"]["attempt_count"]);self.assertEqual("VERIFIED",plan["operations"][0]["state"])

    def test_dependency_and_marker_contract_prevent_out_of_order_or_ambiguous_publish(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,plan,_=setup_projection(root);self.assertEqual("GHOP-CREATE",next_action(root)["operation_id"])
            plan["operations"][0]["desired"]["body_marker"]="missing stable marker";dump(root/"agents/relay/projection/generations/GHGEN-1.yaml",plan);self.assertTrue(any("relay-operation:GHOP-CREATE" in x for x in github_projection(root)[0]))

    def test_close_requires_terminal_repository_truth_and_reopen_requires_reactivated_work(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);setup_projection(root);graph=yaml.safe_load((root/"agents/relay/roadmap/ISSUE_GRAPH.yaml").read_text());child=next(x for x in graph["nodes"] if x["id"]=="ISSUE-CHILD");child.update({"github_state":"OPEN","github":{"issue_number":11},"state":"ACTIVE"});dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph)
            close=operation("GHOP-CLOSE","CLOSE","ISSUE-CHILD",desired={"github_state":"CLOSED"});plan={"schema_version":"relay-v2.5-github-projection","generation":{"id":"GHGEN-1","repository":"owner/synthetic","roadmap_revision":"RM-0001","issue_graph_revision":"IG-1","execution_ref":"EP-1","state":"PREPARED","supersedes_generation":None,"basis":["test"]},"operations":[close]};dump(root/"agents/relay/projection/generations/GHGEN-1.yaml",plan);self.assertTrue(any("terminal repository work state" in x for x in github_projection(root)[0]))
            child["state"]="COMPLETE";child["closure_receipt"]={};dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph);self.assertEqual([],github_projection(root)[0])
            child.update({"state":"ACTIVE","github_state":"CLOSED"});dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph);plan["operations"]=[operation("GHOP-REOPEN","REOPEN","ISSUE-CHILD",desired={"github_state":"OPEN"})];dump(root/"agents/relay/projection/generations/GHGEN-1.yaml",plan);self.assertEqual([],github_projection(root)[0])

    def test_supersede_revise_and_update_require_repository_relationship_truth(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);setup_projection(root);graph=yaml.safe_load((root/"agents/relay/roadmap/ISSUE_GRAPH.yaml").read_text());graph["nodes"]=[{"id":"OLD","state":"SUPERSEDED","github_state":"OPEN","github":{"issue_number":20}},{"id":"NEW","state":"ACTIVE","github_state":"OPEN","github":{"issue_number":21}}];graph["relationships"]=[{"from":"NEW","relation":"SUPERSEDES","to":"OLD"}];dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph);rel={"from":"NEW","relation":"SUPERSEDES","to":"OLD"}
            ops=[operation("GHOP-SUPER","SUPERSEDE","OLD",related=["NEW"],desired={"body_projection":"supersession handover","relationships":[rel]}),operation("GHOP-REVISE","REVISE","NEW",desired={"body_projection":"revised issue projection"}),operation("GHOP-UPDATE","UPDATE","NEW",desired={"body_projection":"updated status"})]
            plan={"schema_version":"relay-v2.5-github-projection","generation":{"id":"GHGEN-1","repository":"owner/synthetic","roadmap_revision":"RM-0001","issue_graph_revision":"IG-1","execution_ref":"EP-1","state":"PREPARED","supersedes_generation":None,"basis":["test"]},"operations":ops};dump(root/"agents/relay/projection/generations/GHGEN-1.yaml",plan);self.assertEqual([],github_projection(root)[0])
            graph["relationships"]=[];dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph);self.assertTrue(any("SUPERSEDES relationship" in x for x in github_projection(root)[0]))

    def test_uncertain_generation_can_be_superseded_without_fabricating_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);setup_projection(root);begin(root,["before-call"],True)
            new=operation("GHOP-NEW","PUBLISH_HANDOVER","ISSUE-PARENT",desired={"body_projection":"new generation handover"});new["idempotency_key"]="relay:GHGEN-2:GHOP-NEW"
            new_plan={"schema_version":"relay-v2.5-github-projection","generation":{"id":"GHGEN-2","repository":"owner/synthetic","roadmap_revision":"RM-0001","issue_graph_revision":"IG-1","execution_ref":"EP-1","state":"PREPARED","supersedes_generation":None,"basis":["new desired generation"]},"operations":[new]};new_rel="agents/relay/projection/generations/GHGEN-2.yaml";dump(root/new_rel,new_plan)
            result=activate(root,new_rel,True);self.assertEqual("GHGEN-1",result["supersedes_generation"]);self.assertEqual([],projection_convergence(root)[0]);self.assertEqual([],generation_history(root)[0]);self.assertEqual("GHOP-NEW",next_action(root)["operation_id"])
            state=yaml.safe_load((root/"agents/relay/REPO_STATE.yaml").read_text());old=yaml.safe_load((root/"agents/relay/projection/generations/GHGEN-1.yaml").read_text());hist=state["projection"]["superseded_operations"][-1]
            self.assertEqual("SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED",hist["disposition"]);self.assertIsNone(hist["receipt"]);self.assertEqual("SUPERSEDED",old["generation"]["state"]);self.assertTrue(all(x["state"] in {"VERIFIED","FAILED","SUPERSEDED"} for x in old["operations"]))

if __name__=="__main__":unittest.main()
