# Binary artifact bundle

The exact generated PDF/JSON stress-test payload is preserved as a single archive for agent handoff.

- Google Drive folder: https://drive.google.com/drive/folders/17tMeh1YpcvbpxrGBgpmEeiMa6NIVeYpt
- Archive: https://drive.google.com/file/d/1ujC3Z26NK1HoJHmqby-48ZJxlk5X1odJ/view?usp=drivesdk
- Archive filename: `PR323_Stress_Test_Artifact_Bundle.tar.xz`
- Archive SHA-256: `423d508b781ca8a05f336c6100b118d81f6939f3fc2fb240e635ed4f5ba5df3c`
- Size: 3,279,316 bytes

The archive contains the current best Core (1), Core (2), and manifest files for the seven-topic stress-test state captured in this handoff, plus the README, consolidated rebuild plan, and file-level SHA inventory.

## Extract

```bash
tar -xJf PR323_Stress_Test_Artifact_Bundle.tar.xz
cd pr323_artifacts_pack
sha256sum -c FILE_INVENTORY.sha256
```

## Why the binaries are external

The connected GitHub write surface used for this handoff supports repository UTF-8 text files but does not directly ingest local binary PDFs. Rather than pretending the PDFs were checked into GitHub, the branch records exact artifact names and hashes and points to this binary bundle. A binary-capable agent/client can vendor the files later without recomputing them.

Treat the PDFs as benchmark/stress-test artifacts, not production authority or release evidence. See `README.md`, `STATUS.json`, and `CONSOLIDATED_REBUILD_PLAN.md` for the governing status and continuation order.
