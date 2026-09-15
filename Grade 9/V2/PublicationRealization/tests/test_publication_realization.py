#!/usr/bin/env python3
import copy, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/"fixtures"
sys.path.insert(0,str(ROOT/"validator"))
from validate_publication import validate

def load(p): return json.loads(Path(p).read_text())
def expect_fail(fn,label):
    try: fn()
    except Exception: return
    raise AssertionError(label)

def realize(td, product=None, target=None, policy=None):
    product=product or F/"learner_semantic_product.synthetic.json"
    target=target or F/"publication_target.synthetic.json"
    policy=policy or F/"publication_realization_policy.synthetic.json"
    subprocess.run([sys.executable,str(ROOT/"engine/realize_publication.py"),"--product",str(product),"--target",str(target),"--policy",str(policy),"--out",str(td)],check=True,capture_output=True)

passes=0
with tempfile.TemporaryDirectory() as t:
    td=Path(t); realize(td)
    product=load(F/"learner_semantic_product.synthetic.json"); target=load(F/"publication_target.synthetic.json")
    structure=load(td/"publication_structure.json"); pmap=load(td/"physical_page_map.json"); audit=load(td/"publication_audit.json"); manifest=load(td/"publication_manifest.json"); pdf=(td/"candidate.pdf").read_bytes()
    assert validate(product,structure,pmap,audit,manifest,pdf,target); passes+=1
    with tempfile.TemporaryDirectory() as t2:
        td2=Path(t2); realize(td2)
        for fn in ["candidate.pdf","publication_structure.json","physical_page_map.json","publication_audit.json","publication_manifest.json","publication_realization_result.json"]:
            assert (td/fn).read_bytes()==(td2/fn).read_bytes(), fn
        passes+=1
    bad=copy.deepcopy(structure); bad["page_intents"][0]["content_refs"].pop()
    expect_fail(lambda: validate(product,bad,pmap,audit,manifest,pdf,target),"missing material not rejected"); passes+=1
    bad=copy.deepcopy(structure); bad["page_intents"][0]["content_refs"].append(bad["page_intents"][0]["content_refs"][0])
    expect_fail(lambda: validate(product,bad,pmap,audit,manifest,pdf,target),"duplicate material not rejected"); passes+=1
    bad=copy.deepcopy(pmap); bad["content_placements"][0]["x1"]=target["paper"]["width_pt"]+10
    expect_fail(lambda: validate(product,structure,bad,audit,manifest,pdf,target),"bounds not rejected"); passes+=1
    bad=copy.deepcopy(pmap); bad["content_placements"][0]["fragment_kind"]="CONTINUATION"
    expect_fail(lambda: validate(product,structure,bad,audit,manifest,pdf,target),"orphan continuation not rejected"); passes+=1
    badpdf=pdf+b"\n"
    expect_fail(lambda: validate(product,structure,pmap,audit,manifest,badpdf,target),"byte drift not rejected"); passes+=1
    bad=copy.deepcopy(pmap); bad["page_intents"][0]["physical_pages"]=[99]
    expect_fail(lambda: validate(product,structure,bad,audit,manifest,pdf,target),"page intent drift not rejected"); passes+=1
    bad=copy.deepcopy(pmap); bad["actual_placement_evidence"]=False
    expect_fail(lambda: validate(product,structure,bad,audit,manifest,pdf,target),"planned evidence accepted"); passes+=1
    bad=copy.deepcopy(manifest); bad["artifacts"].append({"role":"PUBLICATION_AUDIT","path":"publication_manifest.json","sha256":"0"*64,"bytes":1})
    expect_fail(lambda: validate(product,structure,pmap,audit,bad,pdf,target),"self-reference not rejected"); passes+=1
    bad=copy.deepcopy(manifest); bad["package_digest"]="0"*64
    expect_fail(lambda: validate(product,structure,pmap,audit,bad,pdf,target),"package digest drift not rejected"); passes+=1
    bad=copy.deepcopy(audit); bad["quality_states"]["pedagogy_usability"]="PASS"
    expect_fail(lambda: validate(product,structure,pmap,bad,manifest,pdf,target),"engineering implied pedagogy pass"); passes+=1
    bad=copy.deepcopy(structure); bad["page_intents"][0]["content_refs"][0]="D-RULE"
    expect_fail(lambda: validate(product,bad,pmap,audit,manifest,pdf,target),"decorative substitution accepted"); passes+=1
    contaminated=copy.deepcopy(load(F/"publication_realization_policy.synthetic.json")); contaminated["benchmark_template"]="PR156"
    cp=td/"contaminated.json"; cp.write_text(json.dumps(contaminated))
    with tempfile.TemporaryDirectory() as t3:
        r=subprocess.run([sys.executable,str(ROOT/"engine/realize_publication.py"),"--product",str(F/"learner_semantic_product.synthetic.json"),"--target",str(F/"publication_target.synthetic.json"),"--policy",str(cp),"--out",t3],capture_output=True)
        assert r.returncode!=0
    passes+=1
    material=[x for x in product["content_items"] if x["materiality"]=="MATERIAL"]
    assert len(material)==len(pmap["content_placements"]); passes+=1
    roles=[x["role"] for x in manifest["artifacts"]]; assert len(roles)==len(set(roles)); passes+=1
    assert pdf.startswith(b"%PDF-1.4") and pdf.endswith(b"%%EOF\n"); passes+=1
print(f"V2-06 Publication Realization falsifiers: {passes} PASS")
