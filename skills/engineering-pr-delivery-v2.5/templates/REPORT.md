# Engineering relay report — generated projection

Do not hand-author this file as repository truth.

Generate structured source-derived report data with:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/render_report_projection.py <repo-root>
```

Human status/handover views are rendered from the same authority objects. If generated text disagrees with `OVERALL_ROADMAP.yaml`, `PROGRESS.yaml`, the current EP/plan, checkpoints, `ISSUE_GRAPH.yaml`, or `REPO_STATE.yaml`, the generated report is stale and must be regenerated; it never overrides those source objects.

Required report domains remain:

- Executive state
- Overall / phase / WP / step / acceptance progress
- Work completed
- Files changed
- Acceptance matrix
- Tests and evidence
- Quality findings
- Known limitations
- Owner decisions required
- GitHub issue changes
- Roadmap changes
- Exact ordered next work
- Successor EP / terminal disposition
- Qualification evidence when applicable
