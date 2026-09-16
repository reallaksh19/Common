#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml
from relaylib import load_yaml,require

def _required_manifest(manifest:dict)->list[str]:
    e=[];e+=require(manifest,["schema_version","repository","relay_protocol","roadmap","initial_position","initialization"],"BOOTSTRAP_MANIFEST")
    if manifest.get("schema_version")!="relay-v2.5-bootstrap":e.append("BOOTSTRAP_MANIFEST.schema_version must be relay-v2.5-bootstrap")
    e+=require(manifest.get("repository") or {},["name","remote","repository_type","default_branch"],"BOOTSTRAP_MANIFEST.repository");e+=require(manifest.get("relay_protocol") or {},["basis_ref"],"BOOTSTRAP_MANIFEST.relay_protocol");e+=require(manifest.get("roadmap") or {},["id","revision","title"],"BOOTSTRAP_MANIFEST.roadmap")
    pos=manifest.get("initial_position") or {};e+=require(pos,["objective","phase","work_package"],"BOOTSTRAP_MANIFEST.initial_position")
    for key in ("objective","phase","work_package"):e+=require(pos.get(key) or {},["id","title"],f"BOOTSTRAP_MANIFEST.initial_position.{key}")
    if not str((manifest.get("initialization") or {}).get("next_action","")).strip():e.append("BOOTSTRAP_MANIFEST.initialization.next_action must be explicit")
    return e

def build(manifest:dict)->dict[str,dict]:
    errors=_required_manifest(manifest)
    if errors:raise ValueError("; ".join(errors))
    repo=manifest["repository"];proto=manifest["relay_protocol"];road=manifest["roadmap"];pos=manifest["initial_position"];init=manifest["initialization"];oid=pos["objective"]["id"];pid=pos["phase"]["id"];wid=pos["work_package"]["id"]
    roadmap={"schema_version":"relay-v2.5","roadmap":{"id":road["id"],"revision":road["revision"],"title":road["title"]},"objectives":[{"id":oid,"title":pos["objective"]["title"],"state":"ACTIVE","definition":"PARTIALLY_DEFINED","phases":[{"id":pid,"title":pos["phase"]["title"],"state":"PLANNED","definition":"OWNER_REVIEW_REQUIRED","work_packages":[{"id":wid,"title":pos["work_package"]["title"],"state":"PLANNED","definition":"OWNER_REVIEW_REQUIRED","execution_status":"WAITING","depends_on":[]}]}]}]}
    state={"schema_version":"relay-v2.5","relay_state":"INITIALIZING","repository":{"name":repo["name"],"remote":repo["remote"]},"relay_protocol":{"version":"2.5","basis_ref":proto["basis_ref"]},"roadmap":{"id":road["id"],"revision":road["revision"],"path":"agents/relay/roadmap/OVERALL_ROADMAP.yaml"},"current_position":{"objective":oid,"phase":pid,"work_package":wid,"work_packages":[]},"execution_policy":{"mode":"SERIAL"},"active_ep":{"id":None,"path":None,"state":"NONE"},"last_checkpoint":{"id":"NONE","path":None},"predecessor_join":{"id":None,"path":None},"predecessor_replan":{"id":None,"path":None},"takeover_admissions":[],"progress":{"overall_percent":0,"phase_percent":0,"ep_percent":0,"basis_revision":"PB-0001"},"status_planes":{"execution":{"state":"WAITING","can_continue":False,"material_authority":"NONE","next_action":init["next_action"]},"quality":{"state":"OWNER_REVIEW_REQUIRED","findings":list(init.get("notes") or [])},"evidence":{"state":"NA","summary":"Relay bootstrap created; no executable engineering evidence exists yet.","not_run":[]},"stop":{"active":False,"category":"NONE","reason":"","basis":[]}},"projection":{"required":False,"state":"NOT_REQUIRED","operation_id":None,"target":None,"roadmap_revision":road["revision"],"execution_ref":"NONE","receipt":None,"basis":[]},"relay_readiness":{"baton_ready":False,"projection_ready":True,"handover_ready":False,"reasons":["Relay initialization is incomplete; no executable frontier/EP exists."]},"chat_context_required":False}
    profile={"schema_version":"relay-v2.5","repository_type":repo["repository_type"],"default_branch":repo["default_branch"],"important_paths":{},"commands":{},"protected_domains":[],"generated_paths":[],"repository_rules":[]}
    zero=lambda i:{"id":i,"earned_weight":0,"total_weight":0,"percent":0}
    progress={"schema_version":"relay-v2.5","progress_basis":{"id":"PB-0001","roadmap_revision":road["revision"]},"overall":{"earned_weight":0,"total_weight":0,"percent":0},"objectives":[zero(oid)],"phases":[zero(pid)],"work_packages":[zero(wid)],"execution_packages":[],"implementation_steps":[],"acceptance_criteria":[]}
    issue_graph={"schema_version":"relay-v2.5","nodes":[],"relationships":[]}
    return {"agents/relay/REPO_STATE.yaml":state,"agents/relay/REPO_PROFILE.yaml":profile,"agents/relay/roadmap/OVERALL_ROADMAP.yaml":roadmap,"agents/relay/roadmap/PROGRESS.yaml":progress,"agents/relay/roadmap/ISSUE_GRAPH.yaml":issue_graph}
def apply(root:Path,files:dict[str,dict]):
    collisions=[p for p in files if (root/p).exists()]
    if collisions:raise FileExistsError("bootstrap refuses to overwrite existing relay files: "+", ".join(collisions))
    for rel,data in files.items():
        path=root/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")
def main():
    ap=argparse.ArgumentParser(description="Create a repository-neutral V2.5 INITIALIZING relay scaffold. Dry-run by default.");ap.add_argument("manifest");ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--apply",action="store_true");a=ap.parse_args();manifest=load_yaml(Path(a.manifest).resolve());files=build(manifest);root=Path(a.repo_root).resolve();print("V2.5 bootstrap plan:")
    for path in files:print(f"  {'WRITE' if a.apply else 'WOULD WRITE'} {path}")
    if a.apply:apply(root,files);print("Bootstrap state: INITIALIZING. No EP was fabricated; reconcile roadmap and compute a frontier before material work.")
    else:print("Dry run only. Re-run with --apply to write these files.")
if __name__=="__main__":main()
