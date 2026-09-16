# Mandatory Cold-Start Repository Discovery Protocol

Every standalone agent must establish complete repository ground truth before proposing or editing any files.

---

### Pre-Modification Discovery Sequence

Before making any changes, the executing agent must execute the following 10 discovery steps in order:

1. **Resolve Target Branch & Exact HEAD**:
   Identify the active branch, base branch, and exact git commit hash at start. Record this in the execution identity.

2. **Read Governing Manifests & Policies**:
   Locate and read the applicable generation, adoption, and authority manifests (e.g. `AGENTS.md`, `EXIT_GATE.md`, `README.md`, `manifest.json`).

3. **Locate Schema Registries & Normative Architecture**:
   Identify the Draft 2020-12 JSON schemas governing input and output contracts. Confirm which schemas define validation boundaries.

4. **Locate Producers & Consumers**:
   Identify which engine or script generates the target artifact, and which downstream tools or pipelines ingest it.

5. **Locate Existing Tests & CI Workflows**:
   Identify the regression test suites, unit tests, falsifiers, and GitHub Actions workflow definitions associated with the target domain.

6. **Locate Structural Reference Implementations**:
   Identify verified, adjacent implementations that can serve as structural patterns (without treating their case facts as authority).

7. **Search for Deprecated / Legacy Artifacts**:
   Explicitly search for obsolete or retired versions of the concept in the repository to prevent resurrecting superseded paradigms.

8. **Distinguish Canonical vs. Diagnostic Artifacts**:
   Classify existing artifacts into canonical (ground truth data, registries) versus diagnostic/temporary (runtime projections, feedback logs).

9. **Identify Cross-Domain Dependencies**:
   Map dependencies crossing subject boundaries (e.g. Physics depending on Vector Algebra or Calculus in Mathematics) and verify their governing interface contracts.

10. **Record Authority Chain**:
    Formulate and document the explicit chain of authority (Manifest → Policy → Schema → Data → Engine → Test) before initiating modifications.

---

### Non-Negotiable Cold-Start Rule

> **Do not treat a previously seen implementation as authority merely because it resembles the current task.**
>
> Resemblance is not specification. Only schemas, explicit contracts, and documented governing manifests have authority over the task.
