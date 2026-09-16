// MathBlueprint Run Builder - Frontend Configuration Compiler
// Zero topic-specific branches or hardcoded syllabus logic.

const VALID_PURPOSES = ["FIRST_STUDY", "CONSOLIDATION", "REVISION", "COMPETITIVE_EXAM"];
const VALID_DEPTHS = ["FOUNDATION", "STANDARD", "RESEARCH"];
const VALID_RUN_MODES = ["STRESS_TEST", "GENERATION", "LIBRARY_AUDIT", "RESEARCH_AUDIT"];
const VALID_MUTATION_MODES = ["READ_ONLY", "TEST_MUTATIONS_ALLOWED"];
const VALID_DIFFICULTIES = ["EASY", "MEDIUM", "HARD"];

function getFormConfig() {
  const kMode = document.getElementById("learner_knowledge_mode").value;
  const kPercentRaw = document.getElementById("learner_knowledge_percent").value;
  const gradeRaw = document.getElementById("current_grade").value;

  return {
    subject: document.getElementById("subject").value.trim(),
    subtopic_request: document.getElementById("subtopic_request").value.trim(),
    current_grade: gradeRaw ? parseInt(gradeRaw, 10) : null,
    target_program_or_exam: document.getElementById("target_program_or_exam").value.trim(),
    learning_purpose: document.getElementById("learning_purpose").value,
    learner_knowledge_mode: kMode,
    learner_knowledge_percent: kMode === "KNOWN_PERCENT" && kPercentRaw !== "" ? parseFloat(kPercentRaw) : null,
    knowledge_source_ref: document.getElementById("knowledge_source_ref").value.trim(),
    knowledge_calibration_policy_ref: document.getElementById("knowledge_calibration_policy_ref").value.trim(),
    requested_engineering_depth: document.getElementById("requested_engineering_depth").value,
    core1_difficulty_control: document.getElementById("core1_difficulty_control").value,
    owner_difficulty_override: document.getElementById("owner_difficulty_override").value || null,
    pedagogy_research_mode: document.getElementById("pedagogy_research_mode").value,
    web_research_allowed: document.getElementById("web_research_allowed").checked,
    local_question_bank_ref: document.getElementById("local_question_bank_ref").value.trim() || null,
    owner_scope_notes: document.getElementById("owner_scope_notes").value.trim() || null,
    repository: document.getElementById("repository").value.trim(),
    branch_or_ref: document.getElementById("branch_or_ref").value.trim(),
    run_mode: document.getElementById("run_mode").value,
    mutation_mode: document.getElementById("mutation_mode").value,
  };
}

function validateConfig(config) {
  const errors = [];

  if (!config.subject) {
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "subject", message: "Subject is required. Mathematics Blueprint only authorizes MATHEMATICS runs." });
  } else if (config.subject !== "MATHEMATICS") {
    errors.push({ code: "INVALID_COMBINATION", field: "subject", message: `Unsupported subject '${config.subject}'. Only MATHEMATICS is authorized.` });
  }

  if (!config.subtopic_request) {
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "subtopic_request", message: "Subtopic request is required for candidate discovery." });
  }

  if (config.current_grade === null || isNaN(config.current_grade)) {
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "current_grade", message: "Current grade is required." });
  } else if (config.current_grade < 1 || config.current_grade > 12) {
    errors.push({ code: "INVALID_COMBINATION", field: "current_grade", message: "Current grade must be an integer between 1 and 12." });
  }

  if (!config.learning_purpose) {
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "learning_purpose", message: "Learning purpose is required." });
  } else if (!VALID_PURPOSES.includes(config.learning_purpose)) {
    errors.push({ code: "UNKNOWN_POLICY", field: "learning_purpose", message: `Unknown purpose '${config.learning_purpose}'.` });
  }

  if (config.learner_knowledge_mode === "KNOWN_PERCENT") {
    if (config.learner_knowledge_percent === null || isNaN(config.learner_knowledge_percent)) {
      errors.push({ code: "MISSING_REQUIRED_INPUT", field: "learner_knowledge_percent", message: "Learner knowledge percent is required when mode is KNOWN_PERCENT." });
    } else if (config.learner_knowledge_percent < 0 || config.learner_knowledge_percent > 100) {
      errors.push({ code: "INVALID_COMBINATION", field: "learner_knowledge_percent", message: "Knowledge percent must be between 0 and 100." });
    }

    if (!config.knowledge_source_ref) {
      errors.push({ code: "MISSING_REQUIRED_INPUT", field: "knowledge_source_ref", message: "Knowledge source reference is required when percentage is supplied. Unattributed percentages are non-authoritative." });
    }

    if (!config.knowledge_calibration_policy_ref) {
      errors.push({ code: "MISSING_REQUIRED_INPUT", field: "knowledge_calibration_policy_ref", message: "Learner knowledge percentage is present, but no calibration-policy reference has been supplied. The percentage does not independently determine learner support." });
    }
  } else if (config.learner_knowledge_mode === "UNKNOWN") {
    if (config.learner_knowledge_percent !== null) {
      errors.push({ code: "INVALID_COMBINATION", field: "learner_knowledge_percent", message: "Knowledge percentage cannot be supplied when mode is UNKNOWN." });
    }
  }

  if (!config.requested_engineering_depth) {
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "requested_engineering_depth", message: "Engineering depth is required." });
  } else if (!VALID_DEPTHS.includes(config.requested_engineering_depth)) {
    errors.push({ code: "UNKNOWN_POLICY", field: "requested_engineering_depth", message: `Unknown depth '${config.requested_engineering_depth}'.` });
  }

  if (config.core1_difficulty_control === "OWNER_OVERRIDE") {
    if (!config.owner_difficulty_override) {
      errors.push({ code: "OWNER_DECISION_REQUIRED", field: "owner_difficulty_override", message: "Owner difficulty override is selected, but no difficulty badge was provided." });
    } else if (!VALID_DIFFICULTIES.includes(config.owner_difficulty_override)) {
      errors.push({ code: "UNKNOWN_POLICY", field: "owner_difficulty_override", message: `Unknown difficulty badge '${config.owner_difficulty_override}'.` });
    }
  }

  return errors;
}

function computeDependencies(config, errors) {
  const subtopic = config.subtopic_request || "";
  const kMode = config.learner_knowledge_mode;
  const kPercent = config.learner_knowledge_percent;
  const kPolicy = config.knowledge_calibration_policy_ref;

  return {
    subtopic_resolution: {
      status: "UNRESOLVED",
      current_state: "NON_AUTHORITATIVE_FREE_TEXT",
      input_text: subtopic,
      next_required_step: "EXPLICIT_EXACT_ENGINEERING_GATE_SELECTION"
    },
    engineering_authorization: {
      status: subtopic ? "READY_FOR_DISCOVERY" : "BLOCKED",
      exact_gate_id: null,
      authority_state: "NOT_EVALUATED"
    },
    learner_adaptation_status: {
      mode: kMode,
      percentage: kPercent,
      calibration_policy: kPolicy || "MISSING",
      support_conditioned: Boolean(kMode === "KNOWN_PERCENT" && kPercent !== null && kPolicy)
    },
    study_differentiation_status: {
      rule: "SDU_GOVERNED_BY_INTRINSIC_DIFFICULTY_ONLY",
      learner_percentage_isolated: true,
      control_basis: config.core1_difficulty_control
    },
    overall_run_status: errors.length === 0 ? "VALID_CONFIGURATION" : "CONFIGURATION_INCOMPLETE"
  };
}

function buildManifest(config, errors, deps) {
  return {
    schema_version: "1.0.0",
    subject: config.subject,
    subtopic_request: config.subtopic_request,
    subtopic_authority_state: "NON_AUTHORITATIVE_FREE_TEXT",
    learner: {
      current_grade: config.current_grade,
      knowledge_mode: config.learner_knowledge_mode,
      knowledge_percent: config.learner_knowledge_percent,
      knowledge_source_ref: config.knowledge_source_ref || null,
      calibration_policy_ref: config.knowledge_calibration_policy_ref || null
    },
    target: {
      learning_purpose: config.learning_purpose,
      target_program_or_exam: config.target_program_or_exam
    },
    engineering: {
      requested_depth: config.requested_engineering_depth,
      exact_gate_selected: null,
      exact_resolver_passed: false
    },
    core1_control: {
      difficulty_control: config.core1_difficulty_control,
      owner_difficulty_override: config.owner_difficulty_override || null,
      isolated_from_learner_percent: true
    },
    research: {
      web_research_allowed: config.web_research_allowed,
      pedagogy_research_mode: config.pedagogy_research_mode
    },
    context: {
      repository: config.repository,
      branch_or_ref: config.branch_or_ref,
      run_mode: config.run_mode,
      mutation_mode: config.mutation_mode,
      local_question_bank_ref: config.local_question_bank_ref || null,
      owner_scope_notes: config.owner_scope_notes || null
    },
    dependencies: deps,
    validation: {
      status: errors.length === 0 ? "VALID" : "INVALID",
      error_count: errors.length,
      errors: errors
    }
  };
}

function buildPrompt(config) {
  const webRes = config.web_research_allowed ? "Allowed" : "Prohibited";
  return `# AGENT RUN ASSIGNMENT: Mathematics V2 Learning Pipeline

## 0. Run Context and Inputs
- **Subject**: MATHEMATICS
- **Subtopic Request**: "${config.subtopic_request}" (NON-AUTHORITATIVE FREE-TEXT)
- **Target Program / Exam**: ${config.target_program_or_exam}
- **Current Grade**: ${config.current_grade}
- **Learning Purpose**: ${config.learning_purpose}
- **Learner Knowledge Mode**: ${config.learner_knowledge_mode} (Percent: ${config.learner_knowledge_percent !== null ? config.learner_knowledge_percent + "%" : "N/A"})
- **Requested Engineering Depth**: ${config.requested_engineering_depth}
- **Web Pedagogy Research**: ${webRes}
- **Run Mode**: ${config.run_mode}

## 1. Cold-Start Requirement
Operate as a strict cold-start implementation agent.
Assume no conversational memory of previous gate IDs, topic mappings, or test results.
Rediscover all schemas, policies, and gate registries directly from current repository files.

## 2. Authority Hierarchy
Preserve exact authority boundaries:
1. Ground Truth / Source Evidence (Immutable)
2. Engineering Authority (Canonical Gate Registry)
3. Non-Authoritative Candidate Discovery (Broad, tolerant search)
4. Explicit Exact-ID Selection & Exact Authoritative Resolver
5. CDAU / SDU (Intrinsic study depth) & LAU (Learner-adapted practice)
6. Publication & Rendering

## 3. Invariants & Anti-Drift Guard
- **SDU Depth Invariant**: Core1A/Core1B depth is governed by intrinsic mathematical difficulty (EASY, MEDIUM, HARD). SDU MUST NOT inspect or adapt to learner knowledge percentage.
- **LAU Practice Adaptation**: Core2A/Core2B question demand is conditioned on learner knowledge percentage only when bound to an explicit calibration policy and source reference, or under explicit Owner Waiver.
- **Discovery vs. Authorization**: Natural language matching, high semantic similarity, or Rank 1 candidate ranking NEVER grants Engineering authorization. Downstream work requires explicit selection of the exact gate identity.
- **No Topic Branches**: Generic orchestration code must not contain topic-specific branches or hardcoded mathematical formulas.

## 4. Required Execution Steps
1. Execute discovery for candidate gates matching "${config.subtopic_request}".
2. Explicitly select the exact Engineering Gate ID.
3. Validate gate against \`mathematics-technical-engineering-gates.v1.json\` at depth \`${config.requested_engineering_depth}\`.
4. If research is enabled, ensure claim-level coverage, evidence stance classification, and contradiction resolution.
5. Compile Core1A/Core1B and Core2A/Core2B generation specifications.
6. Verify release gate dispositions in Product Governance.

## 5. Known Input Uncertainty & Downstream Blockers
- **Subtopic Status**: Unresolved free-text request until exact Engineering Gate is confirmed.
- **Learner Calibration**: ${config.knowledge_calibration_policy_ref ? "Calibration policy is bound." : "No calibration policy supplied; learner percentage cannot independently condition support."}
`.trim();
}

function updateLiveOutputs() {
  const config = getFormConfig();
  const errors = validateConfig(config);
  const deps = computeDependencies(config, errors);
  const manifest = buildManifest(config, errors, deps);
  const prompt = buildPrompt(config);

  // Update prompt view
  document.getElementById("promptOutput").textContent = prompt;

  // Update manifest view
  document.getElementById("manifestOutput").textContent = JSON.stringify(manifest, null, 2);

  // Update validation view
  const valContainer = document.getElementById("validationOutput");
  valContainer.innerHTML = `
    <div class="status-badge status-${manifest.validation.status}">STATUS: ${manifest.validation.status} (${errors.length} diagnostics)</div>
    ${errors.length === 0 ? '<div style="color:var(--accent-emerald);">All configuration invariants satisfied. Ready for reproducible agent compilation.</div>' : ''}
    ${errors.map(e => `
      <div class="diag-card">
        <div class="diag-header">
          <span>[${e.code}] Field: <code>${e.field}</code></span>
        </div>
        <div class="diag-msg">${e.message}</div>
      </div>
    `).join("")}
  `;

  // Update dependencies view
  const depContainer = document.getElementById("dependenciesOutput");
  depContainer.innerHTML = `
    <div class="dep-card">
      <div class="dep-title">Subtopic Authority Resolution</div>
      <div class="dep-detail">
        <strong>Status:</strong> ${deps.subtopic_resolution.status}<br>
        <strong>Current State:</strong> <code>${deps.subtopic_resolution.current_state}</code><br>
        <strong>Input Text:</strong> "${deps.subtopic_resolution.input_text}"<br>
        <strong>Next Required Step:</strong> ${deps.subtopic_resolution.next_required_step}
      </div>
    </div>

    <div class="dep-card">
      <div class="dep-title">Engineering Gate Authorization</div>
      <div class="dep-detail">
        <strong>Status:</strong> ${deps.engineering_authorization.status}<br>
        <strong>Authority State:</strong> <code>${deps.engineering_authorization.authority_state}</code><br>
        <strong>Exact Gate ID:</strong> ${deps.engineering_authorization.exact_gate_id || "Unresolved (Selection pending)"}
      </div>
    </div>

    <div class="dep-card">
      <div class="dep-title">Learner Adaptation (LAU Core2)</div>
      <div class="dep-detail">
        <strong>Mode:</strong> ${deps.learner_adaptation_status.mode}<br>
        <strong>Percentage:</strong> ${deps.learner_adaptation_status.percentage !== null ? deps.learner_adaptation_status.percentage + "%" : "N/A"}<br>
        <strong>Calibration Policy:</strong> <code>${deps.learner_adaptation_status.calibration_policy}</code><br>
        <strong>Support Conditioned:</strong> ${deps.learner_adaptation_status.support_conditioned ? "YES" : "NO (Blocked until calibration policy supplied)"}
      </div>
    </div>

    <div class="dep-card">
      <div class="dep-title">Study Differentiation (SDU Core1)</div>
      <div class="dep-detail">
        <strong>Governing Invariant:</strong> ${deps.study_differentiation_status.rule}<br>
        <strong>Learner % Isolated:</strong> ${deps.study_differentiation_status.learner_percentage_isolated ? "YES (Strict isolation preserved)" : "NO"}<br>
        <strong>Control Basis:</strong> ${deps.study_differentiation_status.control_basis}
      </div>
    </div>
  `;
}

function loadFixtureData(fixture) {
  document.getElementById("subject").value = fixture.subject || "MATHEMATICS";
  document.getElementById("subtopic_request").value = fixture.subtopic_request || "";
  document.getElementById("current_grade").value = fixture.current_grade || "";
  document.getElementById("target_program_or_exam").value = fixture.target_program_or_exam || "";
  document.getElementById("learning_purpose").value = fixture.learning_purpose || "COMPETITIVE_EXAM";
  document.getElementById("learner_knowledge_mode").value = fixture.learner_knowledge_mode || "KNOWN_PERCENT";
  document.getElementById("learner_knowledge_percent").value = fixture.learner_knowledge_percent !== undefined ? fixture.learner_knowledge_percent : "";
  document.getElementById("knowledge_source_ref").value = fixture.knowledge_source_ref || "";
  document.getElementById("knowledge_calibration_policy_ref").value = fixture.knowledge_calibration_policy_ref || "";
  document.getElementById("requested_engineering_depth").value = fixture.requested_engineering_depth || "RESEARCH";
  document.getElementById("core1_difficulty_control").value = fixture.core1_difficulty_control || "DERIVE";
  document.getElementById("owner_difficulty_override").value = fixture.owner_difficulty_override || "";
  document.getElementById("pedagogy_research_mode").value = fixture.pedagogy_research_mode || "DEFAULT";
  document.getElementById("web_research_allowed").checked = fixture.web_research_allowed !== false;
  document.getElementById("local_question_bank_ref").value = fixture.local_question_bank_ref || "";
  document.getElementById("owner_scope_notes").value = fixture.owner_scope_notes || "";
  document.getElementById("repository").value = fixture.repository || "reallaksh19/Common";
  document.getElementById("branch_or_ref").value = fixture.branch_or_ref || "v2-math-core1a-textbook-quality";
  document.getElementById("run_mode").value = fixture.run_mode || "STRESS_TEST";
  document.getElementById("mutation_mode").value = fixture.mutation_mode || "READ_ONLY";

  toggleKnowledgeInputs();
  toggleDifficultyInputs();
  updateLiveOutputs();
}

function toggleKnowledgeInputs() {
  const mode = document.getElementById("learner_knowledge_mode").value;
  const isKnown = mode === "KNOWN_PERCENT";
  document.getElementById("learner_knowledge_percent").disabled = !isKnown;
  document.getElementById("knowledge_source_ref").disabled = !isKnown;
  document.getElementById("knowledge_calibration_policy_ref").disabled = !isKnown;
}

function toggleDifficultyInputs() {
  const ctrl = document.getElementById("core1_difficulty_control").value;
  document.getElementById("owner_difficulty_override").disabled = ctrl !== "OWNER_OVERRIDE";
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".output-view").forEach(v => v.classList.remove("active"));
      document.getElementById(`view-${btn.dataset.view}`).classList.add("active");
    });
  });

  const formInputs = document.querySelectorAll("#configForm input, #configForm select, #configForm textarea");
  formInputs.forEach(input => {
    input.addEventListener("input", updateLiveOutputs);
    input.addEventListener("change", updateLiveOutputs);
  });

  document.getElementById("learner_knowledge_mode").addEventListener("change", () => {
    toggleKnowledgeInputs();
    updateLiveOutputs();
  });

  document.getElementById("core1_difficulty_control").addEventListener("change", () => {
    toggleDifficultyInputs();
    updateLiveOutputs();
  });

  const JEE_PRESET = {
    subject: "MATHEMATICS",
    subtopic_request: "Theory of Equations",
    current_grade: 9,
    target_program_or_exam: "IIT-JEE preparation",
    learning_purpose: "COMPETITIVE_EXAM",
    learner_knowledge_mode: "KNOWN_PERCENT",
    learner_knowledge_percent: 70,
    knowledge_source_ref: "OWNER_SUPPLIED_DIAGNOSTIC",
    knowledge_calibration_policy_ref: "POL-MATH-KNOW-CALIB-V1",
    requested_engineering_depth: "RESEARCH",
    core1_difficulty_control: "DERIVE",
    owner_difficulty_override: null,
    pedagogy_research_mode: "DEFAULT",
    web_research_allowed: true,
    local_question_bank_ref: "LOCAL_FIXTURE_QBANK_G9_JEE",
    owner_scope_notes: "IIT-JEE Theory of Equations Fixture. Non-authoritative.",
    repository: "reallaksh19/Common",
    branch_or_ref: "v2-math-core1a-textbook-quality",
    run_mode: "STRESS_TEST",
    mutation_mode: "READ_ONLY"
  };

  const IOQM_PRESET = {
    subject: "MATHEMATICS",
    subtopic_request: "Euclidean Triangles & Circle Theorems",
    current_grade: 10,
    target_program_or_exam: "IOQM / Regional Mathematical Olympiad",
    learning_purpose: "COMPETITIVE_EXAM",
    learner_knowledge_mode: "UNKNOWN",
    learner_knowledge_percent: null,
    knowledge_source_ref: "",
    knowledge_calibration_policy_ref: "",
    requested_engineering_depth: "RESEARCH",
    core1_difficulty_control: "OWNER_OVERRIDE",
    owner_difficulty_override: "HARD",
    pedagogy_research_mode: "DEFAULT",
    web_research_allowed: true,
    local_question_bank_ref: "LOCAL_FIXTURE_QBANK_G10_IOQM",
    owner_scope_notes: "IOQM Olympiad Euclidean Geometry Fixture. Non-authoritative.",
    repository: "reallaksh19/Common",
    branch_or_ref: "v2-math-core1a-textbook-quality",
    run_mode: "STRESS_TEST",
    mutation_mode: "READ_ONLY"
  };

  const CBSE_PRESET = {
    subject: "MATHEMATICS",
    subtopic_request: "Pair of Linear Equations in Two Variables",
    current_grade: 10,
    target_program_or_exam: "CBSE Board Examination",
    learning_purpose: "CONSOLIDATION",
    learner_knowledge_mode: "KNOWN_PERCENT",
    learner_knowledge_percent: 85,
    knowledge_source_ref: "CBSE_PERIODIC_TEST_2",
    knowledge_calibration_policy_ref: "POL-MATH-KNOW-CALIB-V1",
    requested_engineering_depth: "STANDARD",
    core1_difficulty_control: "DERIVE",
    owner_difficulty_override: null,
    pedagogy_research_mode: "DEFAULT",
    web_research_allowed: false,
    local_question_bank_ref: "LOCAL_FIXTURE_QBANK_G10_CBSE",
    owner_scope_notes: "CBSE Board Examination Standard Fixture. Non-authoritative.",
    repository: "reallaksh19/Common",
    branch_or_ref: "v2-math-core1a-textbook-quality",
    run_mode: "STRESS_TEST",
    mutation_mode: "READ_ONLY"
  };

  const bindPresetBtn = (btnId, fixturePath, fallbackPreset) => {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.addEventListener("click", () => {
      fetch(fixturePath)
        .then(res => res.json())
        .then(data => loadFixtureData(data))
        .catch(() => loadFixtureData(fallbackPreset));
    });
  };

  bindPresetBtn("loadJeeFixtureBtn", "fixtures/theory_of_equations_jee_fixture.json", JEE_PRESET);
  bindPresetBtn("loadIoqmFixtureBtn", "fixtures/ioqm_olympiad_geometry_fixture.json", IOQM_PRESET);
  bindPresetBtn("loadCbseFixtureBtn", "fixtures/cbse_linear_equations_fixture.json", CBSE_PRESET);

  const copyCliBtn = document.getElementById("copyCliBtn");
  if (copyCliBtn) {
    copyCliBtn.addEventListener("click", () => {
      const cfg = getFormConfig();
      const cmd = `python "Grade 9/V2/Mathematics/MathBlueprint/tools/run_builder/compile_run.py" --config "Grade 9/V2/Mathematics/MathBlueprint/tools/run_builder/fixtures/theory_of_equations_jee_fixture.json"`;
      navigator.clipboard.writeText(cmd).then(() => {
        const oldText = copyCliBtn.textContent;
        copyCliBtn.textContent = "Copied to Clipboard!";
        setTimeout(() => { copyCliBtn.textContent = oldText; }, 2000);
      }).catch(() => {
        prompt("Copy CLI command:", cmd);
      });
    });
  }

  const exportConfigBtn = document.getElementById("exportConfigBtn");
  if (exportConfigBtn) {
    exportConfigBtn.addEventListener("click", () => {
      const cfg = getFormConfig();
      const blob = new Blob([JSON.stringify(cfg, null, 2) + "\n"], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "run_config.json";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  toggleKnowledgeInputs();
  toggleDifficultyInputs();
  updateLiveOutputs();
});
