#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from core2b_runtime import choose_next_item,digest

def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--session",required=True);ap.add_argument("--legal-pool",required=True);ap.add_argument("--core1b-receipts",required=True);ap.add_argument("--hint-policy",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    session=load(a.session);pool=load(a.legal_pool);payload=load(a.core1b_receipts);receipts={r["receipt_id"]:r for r in (payload if isinstance(payload,list) else payload.get("receipts",[]))};hint=load(a.hint_policy)
    chosen=choose_next_item(session,pool,receipts,hint)
    out={"schema_version":"1.0.0","session_id":session["session_id"],"core2a_legal_pool_ref":pool["product_id"],"core2a_legal_pool_digest":digest(pool),"selected_core2a_item_ref":chosen["overlay"]["core2a_item_ref"],"derived_min_state":chosen["derived_min_state"],"display_transfer_label":chosen["overlay"]["display_transfer_label"],"authority_statement":"SELECTION_ONLY_CORE2A_REMAINS_LEGALITY_AUTHORITY"};out["selection_digest"]=digest(out)
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
