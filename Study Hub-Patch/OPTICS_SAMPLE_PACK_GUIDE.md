# Optics Sample Pack Guide

This sample pack is designed to test both the **Parent UI** and the **Kid UI** after the cumulative patch set is applied.

## Goal of the pack

The pack is not meant to be a complete textbook chapter. It is a **rich test chapter** that exercises the important authoring and learning paths:
- topic metadata
- topic cover asset
- page blocks
- equations
- SVG diagrams
- PNG/JPG images
- PDF attachment and PDF embed
- clarifiers and tips
- assertion–reason style MCQ
- concept-strengthener questions
- student-side helpful resources

## Topic created by the pack

Subject: `Physics`
Topic folder: `optics`
Topic id: `physics-optics`

## Pages included

1. `Light and Visibility`
2. `Reflection Basics`
3. `Refraction and Refractive Index`
4. `Lenses and Images`
5. `Tough Concepts and Practice`

## Asset types included

- PNG cover image
- JPG image
- SVG diagrams
- PDF worksheet/revision sheet
- external NCERT reference link

## Why this pack is useful for the parent UI

It tests whether a parent can:
- import a chapter pack
- see a new topic under Physics
- open topic metadata with cover/helper text already filled
- open pages that already contain mixed block types
- edit clarifiers/questions/resources without starting from empty JSON
- verify that imported assets are reusable in block editors

## Why this pack is useful for the kid UI

It tests whether a child can:
- open a topic home page with cover and helper text
- move through 5 ordered pages
- see clarifiers and tips in the right sidebar
- access page resources
- answer different supported question types
- use diagrams/PDFs as support material for difficult concepts

---

## How the pack is aligned to the NCERT optics chapter

This pack is loosely aligned to the NCERT *Ray Optics and Optical Instruments* chapter structure, especially these ideas:
- visible light occupies a small wavelength band and ray language is introduced early
- reflection uses the normal and equal incidence/reflection angles
- refractive index and refraction through interfaces are central concepts
- total internal reflection and practical demonstrations are discussed later
- lens relations and optical instruments build on the same sign/ray logic

The sample pack content itself is original and intentionally concise; it is designed for UI testing and parent/child workflows rather than textbook replacement.

---

## Import behavior expected

When imported through the Parent Dashboard, the pack should create:

```text
public/
  Physics/
    optics/
      topic.json
      pages/
        light-and-visibility.json
        reflection-basics.json
        refraction-and-refractive-index.json
        lenses-and-images.json
        tough-concepts-and-practice.json
      assets/
        optics-cover.png
        light-through-prism.jpg
        prism-dispersion.png
        reflection-law.svg
        refraction-slab.svg
        convex-lens-ray.svg
        optics-quick-revision.pdf
```

## localStorage behavior expected

The imported chapter pack should **not** be stored in localStorage.

localStorage should be used only for runtime state such as:
- parent page drafts
- parent PIN hash
- student progress keys like `student_progress__physics-optics`

That keeps chapter content deployable and student state device-local.

---

## Parent walkthrough: creating and using the chapter

### What the parent sees after import

1. Open Parent Dashboard.
2. Click **Import Pack** and choose `physics-optics-sample-pack.zip`.
3. The app restores:
   - 1 topic
   - 5 pages
   - 7 assets
4. Open **Physics → Optics**.
5. In Topic Setup, verify:
   - title = Optics
   - cover asset present
   - helper text present
   - tags present
6. Open each page and inspect:
   - Content tab
   - Clarifiers & Tips tab
   - Questions tab
   - Resources tab

### If the parent wants to add another subtopic page later

Use the topic editor and create a new page, for example:
- `Total Internal Reflection`
- `Human Eye`
- `Prism and Dispersion`

Then the parent can:
- add text/equation/media blocks
- attach PDFs/diagrams as resources
- add question sets for that new page
- export the whole chapter again as a ZIP pack

---

## Student walkthrough: learning the chapter

### What the child flow should feel like

1. Open **Physics → Optics**.
2. See topic overview, page count, estimated time, difficulty.
3. Start with `Light and Visibility`.
4. Move to `Reflection Basics` and inspect the right sidebar.
5. Use the reflection SVG when the normal/angle idea feels difficult.
6. Continue to `Refraction and Refractive Index`.
7. Open helpful resources if the child struggles with ray bending.
8. Move to `Lenses and Images` and compare the worked solution against the formula.
9. Use `Tough Concepts and Practice` as the parent-guided recap page.

### What makes the child flow more education-friendly

The sample pack deliberately includes:
- concept clarifiers
- mistake-prevention hints
- question support links
- diagram-first learning cues
- a PDF recap for slower review

This is much better than only offering MCQs after a dense text page.
