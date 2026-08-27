# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

EXECUTION_MODE: AUTO
AUTO_STATE: RUNNING
SCOPE_AUTHORITY: LOCKED_TO_APPROVED_MISSION
MERGE_AUTHORITY: OWNER_AUTHORIZED_FOR_COMPLETION

MIGRATION_NOTE: EP-0001 and EP-0002 were created before the split index/endpoint-file architecture. Their exact historical content is preserved in Git blob `2ea710e3b0120e2a2e739b96e6c035d3caca35f5`; they are not rewritten into synthetic normalized endpoint files.

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | Endpoint file | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|---|
| COMMON-ENG-PR-DELIVERY-V2 | Complete canonical Common adoption and prove downstream relay operation | EP-0009 | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0009.md | PENDING | READY_FOR_NEXT_LEG | Cross-repository engineering-agent delivery governance | Open/merge Common closure PR, then start Advanced_Analysis abrupt-loss and fabricated-anchor pilot without touching production engineering code |

## ENDPOINT LOG

| Endpoint | Chain | Leg | Checkpoint head | State | Locator |
|---|---|---|---|---|---|
| EP-0001 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | fdeab8553196d69ace9c021d79e790fdbd65d6fd | QUALIFICATION_REQUIRED | git-blob:2ea710e3b0120e2a2e739b96e6c035d3caca35f5#EP-0001 |
| EP-0002 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | 4a207360c504ea45a426b3e3469f5fc2fb1fd35b | QUALIFICATION_REQUIRED | git-blob:2ea710e3b0120e2a2e739b96e6c035d3caca35f5#EP-0002 |
| EP-0003 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | 2d9160bd123eb91ca9c7f9e99ecbf050e4a07c3b | READY_FOR_NEXT_LEG | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0003.md |
| EP-0004 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | cde9ee0f9d3a6ddf143b15d6c3cf24096e779ddb | READY_FOR_NEXT_LEG | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0004.md |
| EP-0005 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | be44c1f1e1f47c0069c4061bafcf5d00732567cd | QUALIFICATION_REQUIRED | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0005.md |
| EP-0006 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | 5a6c9d37b2b3a409c0504f8e62422ac354b3576f | QUALIFICATION_REQUIRED | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0006.md |
| EP-0007 | COMMON-ENG-PR-DELIVERY-V2 | LEG-002 | 98b36f72015f12d8bf4f4e1bedce4753d911bfdc | QUALIFICATION_REQUIRED | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0007.md |
| EP-0008 | COMMON-ENG-PR-DELIVERY-V2 | LEG-003 | 77d7afc1fda71ec916e5d5b12f9730847cc52309 | READY_FOR_NEXT_LEG | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0008.md |
| EP-0009 | COMMON-ENG-PR-DELIVERY-V2 | LEG-003 | 961e0a4917c622b9ee45a357fe73f9b74325ad1b | READY_FOR_NEXT_LEG | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0009.md |
