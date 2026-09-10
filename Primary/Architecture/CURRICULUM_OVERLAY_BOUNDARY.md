# Primary curriculum overlay boundary

The Primary architecture supports curriculum alignment without duplicating canonical learning objects.

## Canonical rule

```text
LearningObject
   ├─ Grade 4 scope/depth
   ├─ Grade 5 scope/depth
   ├─ IB PYP mapping
   ├─ NCF-SE/NCERT mapping
   ├─ school/source mapping
   └─ later assessment-demand mapping
```

Curriculum profiles describe expected scope, sequence, evidence, language, and emphasis. They do not become separate knowledge ontologies.

## IB PYP

Treat PYP mappings as developmental/conceptual overlays. Do not hard-code a PYP language phase as equivalent to a school grade.

## India / CBSE-facing work

Prefer explicit mappings to NCF-SE Preparatory Stage, NCERT source material, and the child's actual school scope. `CBSE` may be a delivery/context label where useful, but the architecture should preserve the more precise curriculum/source basis.

## School/source priority

For an imminent assessment, the supplied textbook/workbook/teacher scope may be the most precise operational scope. Canonical correctness and source provenance remain separate so that simplifications, ambiguities, or source errors can be represented rather than silently normalized.

## Later competition

IMO/IOM and Spell Bee should attach through assessment-demand/stretch profiles. They may change transfer demand and practice emphasis but must not silently redefine foundational Grade 4–5 learning semantics.