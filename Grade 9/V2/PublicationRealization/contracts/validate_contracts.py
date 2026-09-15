#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/"contracts"; F=ROOT/"fixtures"
pairs=[
("learner-semantic-product.schema.json","learner_semantic_product.synthetic.json"),
("publication-realization-policy.schema.json","publication_realization_policy.synthetic.json")
]
for s,f in pairs:
    schema=json.loads((C/s).read_text()); obj=json.loads((F/f).read_text()); Draft202012Validator(schema).validate(obj)
with tempfile.TemporaryDirectory() as td:
    subprocess.run([sys.executable,str(ROOT/"engine/realize_publication.py"),"--product",str(F/"learner_semantic_product.synthetic.json"),"--target",str(F/"publication_target.synthetic.json"),"--policy",str(F/"publication_realization_policy.synthetic.json"),"--out",td],check=True)
    outs=[("publication-structure.schema.json","publication_structure.json"),("physical-page-map.schema.json","physical_page_map.json"),("publication-audit.schema.json","publication_audit.json"),("publication-manifest.schema.json","publication_manifest.json"),("publication-realization-result.schema.json","publication_realization_result.json")]
    for s,f in outs:
        Draft202012Validator(json.loads((C/s).read_text())).validate(json.loads((Path(td)/f).read_text()))
print("V2-06 contract + generated artifact validation: PASS")
