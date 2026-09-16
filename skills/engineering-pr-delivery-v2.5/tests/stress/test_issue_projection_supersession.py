from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"))
from validate_issue_projection_tree import validate as projection_tree
from validate_supersession import validate as supersession

def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def child_rollup(revision,children,derived,terminal=False):
    return {"graph_revision":revision,"direct_children":children,"derived_state":derived,"all_children_terminal":terminal}

def deep_graph():
    rev="IG-3"
    leaf_a={"id":"ISSUE-A","state":"COMPLETE","github_state":"CLOSED"}
    leaf_b={"id":"ISSUE-B","state":"ACTIVE","github_state":"OPEN"}
    mid={"id":"ISSUE-MID","state":"ACTIVE","github_state":"OPEN","child_rollup":child_rollup(rev,[{"id":"ISSUE-A","state":"COMPLETE","github_state":"CLOSED"},{"id":"ISSUE-B","state":"ACTIVE","github_state":"OPEN"}],"ACTIVE",False)}
    root={"id":"ISSUE-ROOT","state":"ACTIVE","github_state":"OPEN","child_rollup":child_rollup(rev,[{"id":"ISSUE-MID","state":"ACTIVE","github_state":"OPEN"}],"ACTIVE",False)}
    return {"schema_version":"relay-v2.5","graph_revision":rev,"nodes":[root,mid,leaf_a,leaf_b],"relationships":[{"from":"ISSUE-ROOT","relation":"PARENT_OF","to":"ISSUE-MID"},{"from":"ISSUE-MID","relation":"PARENT_OF","to":"ISSUE-A"},{"from":"ISSUE-MID","relation":"PARENT_OF","to":"ISSUE-B"}]}

def transfer(successor,acceptance,evidence,basis):
    return {"successor":successor,"basis":basis,"unresolved_acceptance":acceptance,"inputs":[],"risks":[],"decisions":[],"evidence":evidence}

def inheritance(predecessor,acceptance,evidence,basis):
    return {"predecessor":predecessor,"basis":basis,"unresolved_acceptance":acceptance,"inputs":[],"risks":[],"decisions":[],"evidence":evidence}

def chain_graph():
    acx={"id":"AC-X","state":"NOT_RUN","basis":["EP-A"]};acy={"id":"AC-Y","state":"NOT_RUN","basis":["EP-B"]}
    evx={"id":"EV-X","status":"NOT_RUN","basis_ref":"head-A","reason":"Runner unavailable."};evy={"id":"EV-Y","status":"NOT_RUN","basis_ref":"head-B","reason":"Dependency unavailable."}
    abasis=["CP-A"];bbasis=["CP-B"]
    a={"id":"ISSUE-A","state":"SUPERSEDED","github_state":"CLOSED","supersession_receipt":transfer("ISSUE-B",[acx],[evx],abasis)}
    b={"id":"ISSUE-B","state":"SUPERSEDED","github_state":"CLOSED","supersession_inheritance":inheritance("ISSUE-A",[acx],[evx],abasis),"supersession_receipt":transfer("ISSUE-C",[acx,acy],[evx,evy],bbasis)}
    c={"id":"ISSUE-C","state":"ACTIVE","github_state":"OPEN","supersession_inheritance":inheritance("ISSUE-B",[acx,acy],[evx,evy],bbasis)}
    return {"schema_version":"relay-v2.5","nodes":[a,b,c],"relationships":[{"from":"ISSUE-B","relation":"SUPERSEDES","to":"ISSUE-A"},{"from":"ISSUE-C","relation":"SUPERSEDES","to":"ISSUE-B"}]}

class IssueProjectionAndSupersessionStressTests(unittest.TestCase):
    def test_deep_parent_rollup_is_derived_from_direct_children(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",deep_graph());self.assertEqual([],projection_tree(root)[0])

    def test_stale_child_rollup_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);g=deep_graph();g["nodes"][1]["child_rollup"]["direct_children"][1]["state"]="COMPLETE";dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",g);self.assertTrue(any("state snapshot is stale" in x for x in projection_tree(root)[0]))

    def test_parent_tree_rejects_multiple_parents_and_cycles(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);g=deep_graph();g["relationships"].append({"from":"ISSUE-A","relation":"PARENT_OF","to":"ISSUE-MID"});dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",g);errors=projection_tree(root)[0];self.assertTrue(any("multiple parents" in x for x in errors));self.assertTrue(any("cycle" in x for x in errors))

    def test_closed_parent_cannot_hide_open_child(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);g=deep_graph();g["nodes"][0]["github_state"]="CLOSED";dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",g);self.assertTrue(any("child still GitHub OPEN" in x for x in projection_tree(root)[0]))

    def test_multi_generation_supersession_preserves_unresolved_items(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",chain_graph());self.assertEqual([],supersession(root)[0])

    def test_intermediate_supersession_cannot_drop_inherited_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);g=chain_graph();b=g["nodes"][1];c=g["nodes"][2];b["supersession_receipt"]["unresolved_acceptance"]=b["supersession_receipt"]["unresolved_acceptance"][1:];c["supersession_inheritance"]["unresolved_acceptance"]=c["supersession_inheritance"]["unresolved_acceptance"][1:];dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",g);self.assertTrue(any("drops inherited unresolved_acceptance item AC-X" in x for x in supersession(root)[0]))

    def test_intermediate_can_explicitly_resolve_inherited_item(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);g=chain_graph();b=g["nodes"][1];c=g["nodes"][2];b["supersession_receipt"]["unresolved_acceptance"]=b["supersession_receipt"]["unresolved_acceptance"][1:];c["supersession_inheritance"]["unresolved_acceptance"]=c["supersession_inheritance"]["unresolved_acceptance"][1:];b["supersession_resolution"]={"acceptance":[{"id":"AC-X","disposition":"RESOLVED","basis":["CP-B","TEST-X"]}],"evidence":[]};dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",g);self.assertEqual([],supersession(root)[0])

    def test_intermediate_cannot_mutate_inherited_evidence_status(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);g=chain_graph();g["nodes"][1]["supersession_receipt"]["evidence"][0]["status"]="PASS";g["nodes"][2]["supersession_inheritance"]["evidence"][0]["status"]="PASS";dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",g);self.assertTrue(any("mutates inherited evidence item EV-X" in x for x in supersession(root)[0]))

    def test_supersession_lineage_rejects_branching_and_cycles(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);g=chain_graph();g["relationships"].append({"from":"ISSUE-C","relation":"SUPERSEDES","to":"ISSUE-A"});g["relationships"].append({"from":"ISSUE-A","relation":"SUPERSEDES","to":"ISSUE-C"});dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",g);errors=supersession(root)[0];self.assertTrue(any("multiple successors" in x for x in errors));self.assertTrue(any("cycle" in x for x in errors))

if __name__=="__main__":unittest.main()
