# Motion2D/RelativeMotion packet index

**Packet schema:** M2D-PACKET-1.1.0  
**Topic:** PHY-M2D-RM-20260915  
**Review state:** SELF_REVIEW_NOT_INDEPENDENT; cold restart NOT_RUN.  
**Controlling architecture:** V3B PR #364 `6be71db1a321c449131a26ee3084b6b9c0edca28`.  
**Live comparison:** Physics PR #350 `2c4ece2833a8a6686607b5d038efe29674c5c6b6`; see `../qa/live-authority-reconciliation.md`.

Receiver rule: read the canonical `source-corpus.md`, `source-inventory.json`, `coverage.csv`, `equation-register.json`, `requirements.json`, and relevant Core files before editing. Verify hashes/heads anew. Source Q01–Q12 and Core2 are frozen; Q12 remains an underdetermination hold. K50 is synthetic. Do not infer independent review or release from author-run PASS evidence.

- [`PKT-B01-B03-v1.md`](PKT-B01-B03-v1.md) — frame/clock, path/displacement/averages, coordinates/components.
- [`PKT-B04-B06-v1.md`](PKT-B04-B06-v1.md) — constant planar motion, 1D relative motion, 2D relative velocity.
- [`PKT-B07-B08-v1.md`](PKT-B07-B08-v1.md) — meeting/collision, boat/current, rain/observer, ambiguity/closest-approach enrichment, extension impact.
