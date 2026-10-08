RELAY RESET R1-B.1 — Native GitHub comment source receipt
Parent: https://github.com/reallaksh19/Common/issues/787
Leaf: https://github.com/reallaksh19/Common/issues/795

Standalone module (does not import unmerged PR #790). Fixed api.github.com HTTPS GET only, no GitHub writes or privileges. Typed receipt validates returned numeric comment identity, bound issue/REST/HTML permalinks, repository-owner login and native OWNER association, timestamps, current body digest and resource bounds. Injected mocks are marked INJECTED_UNVERIFIED. Only a default native GET is marked NATIVE_FIXED_HTTPS_GET, which still does NOT grant Owner approval, original ChatGPT transcript provenance, acceptance, custody or roadmap authority. Organizational delegation is unsupported pending R1-B.2. Run node --test skills/engineering-relay-v1/github-comment-source-v1.test.mjs. Native example GitHub owner comment: https://github.com/reallaksh19/Common/issues/789#issuecomment-6062832157
