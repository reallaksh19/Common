# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

MIGRATION_NOTE: EP-0001 and EP-0002 were created before the split index/endpoint-file architecture. Their exact historical content is preserved in Git blob `2ea710e3b0120e2a2e739b96e6c035d3caca35f5`; they are not rewritten into synthetic normalized endpoint files.

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | Endpoint file | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|---|
| COMMON-ENG-PR-DELIVERY-V2 | Introduce and qualify crash-safe repo-wide engineering relay without replacing v1 yet | EP-0004 | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0004.md | #17 | READY_FOR_NEXT_LEG | Cross-repository engineering-agent delivery governance | Incoming agent re-grounds current main, answers EP-0004 Q1-Q5, and obtains separate verifier PASS before bounded root-policy adoption/pilot |

## ENDPOINT LOG

| Endpoint | Chain | Leg | Checkpoint head | State | Locator |
|---|---|---|---|---|---|
| EP-0001 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | fdeab8553196d69ace9c021d79e790fdbd65d6fd | QUALIFICATION_REQUIRED | git-blob:2ea710e3b0120e2a2e739b96e6c035d3caca35f5#EP-0001 |
| EP-0002 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | 4a207360c504ea45a426b3e3469f5fc2fb1fd35b | QUALIFICATION_REQUIRED | git-blob:2ea710e3b0120e2a2e739b96e6c035d3caca35f5#EP-0002 |
| EP-0003 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | 2d9160bd123eb91ca9c7f9e99ecbf050e4a07c3b | READY_FOR_NEXT_LEG | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0003.md |
| EP-0004 | COMMON-ENG-PR-DELIVERY-V2 | LEG-001 | cde9ee0f9d3a6ddf143b15d6c3cf24096e779ddb | READY_FOR_NEXT_LEG | agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0004.md |
