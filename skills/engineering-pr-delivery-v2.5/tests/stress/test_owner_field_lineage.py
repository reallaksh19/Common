from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
import yaml

HERE=Path(__file__).resolve()
SKILL=HERE.parents[2]
sys.path.insert(0,str(SKILL/"scripts"))

from validate_owner_field_lineage import REQUIRED_STAGES,validate


class OwnerFieldLineageStressTests(unittest.TestCase):
    def test_live_owner_field_lineage_contract_is_complete(self):
        errors,_=validate(SKILL)
        self.assertEqual([],errors)

    def test_declared_field_token_removal_is_release_failure(self):
        with tempfile.TemporaryDirectory() as td:
            skill=Path(td)
            (skill/"operating-model").mkdir(parents=True)
            surface=skill/"surface.txt";surface.write_text("KEEP\n",encoding="utf-8")
            manifest={
                "schema_version":"relay-v2.5-owner-field-lineage",
                "required_stages":list(REQUIRED_STAGES),
                "fields":[{
                    "id":"OWNER_SYNTHETIC",
                    "human_need":"Synthetic lineage witness.",
                    "authority":"Synthetic authority context.",
                    "stages":{
                        stage:[{"path":"surface.txt","tokens":["KEEP"]}]
                        for stage in REQUIRED_STAGES
                    },
                }],
            }
            (skill/"operating-model"/"owner-field-lineage.yaml").write_text(
                yaml.safe_dump(manifest,sort_keys=False),encoding="utf-8"
            )
            errors,_=validate(skill)
            self.assertEqual([],errors)

            surface.write_text("REMOVED\n",encoding="utf-8")
            errors,_=validate(skill)
            self.assertTrue(any("missing required token: KEEP" in x for x in errors))


if __name__=="__main__":
    unittest.main()
