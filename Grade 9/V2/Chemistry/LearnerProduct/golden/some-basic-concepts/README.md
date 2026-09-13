# Some Basic Concepts — learner-product process golden

This directory contains **process goldens**, not a production NCERT chapter.

The semantic golden exercises a small formula/charge, particle↔symbol and atom-conservation slice. The rendered golden builder executes the same governed synthetic cold-start authority through the complete Chemistry learner-product machine chain:

```text
C-LP-00
→ semantic Core1A/Core2A realization
→ answer closure
→ C-LP-22 PDF realization
→ C-LP-23 actual-PDF preflight
→ C-LP-24 final machine audit
→ C-LP-25 frozen handoff
```

Build it with:

```bash
python 'Grade 9/V2/Chemistry/LearnerProduct/golden/some-basic-concepts/build_render_golden.py' \
  --out-dir /tmp/chemistry-lp-render-golden
```

Expected output includes:

```text
chemistry_core1a.pdf
chemistry_core2a.pdf
render_manifest.json
visual_preflight.json
raster-proof/*.png
final_audit.json
handoff_manifest.json
learner_product_manifest.json
GOLDEN_DECLARATION.json
```

CI uploads that directory as `chemistry-core1a-core2a-render-process-golden` for actual-size human inspection.

## Claims explicitly not made

```text
production_claim = false
official_source_claim = false
human_release_claim = false
```

This fixture does not replace the 68-question Some Basic Concepts denominator preserved in the NCERT authoring handoff. It validates the learner-product **process and rendering contracts** on a small deterministic slice. Human subject correctness, pedagogy, assessment design, visual usability and mature-design approval remain separate gates.
