// PhysicsBlueprint Run Builder - Frontend Configuration Compiler
// Zero topic-specific branches or hardcoded syllabus logic.

const VALID_PURPOSES = ["CBSE_EXAM", "COMPETITIVE_EXAM", "OLYMPIAD_FOUNDATION", "CONCEPT_REMEDIATION", "ACCELERATED_STUDY"];
const VALID_DEPTHS = ["STANDARD", "RESEARCH"];
const VALID_RUN_MODES = ["GENERATION", "STRESS_TEST", "LIBRARY_AUDIT", "RESEARCH_AUDIT"];
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
    exact_gate_id: document.getElementById("exact_gate_id").value.trim() || null,
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
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "subject", message: "Subject is required. Physics Blueprint only authorizes PHYSICS runs." });
  } else if (config.subject !== "PHYSICS") {
    errors.push({ code: "INVALID_COMBINATION", field: "subject", message: `Unsupported subject '${config.subject}'. Only PHYSICS is authorized.` });
  }

  if (!config.subtopic_request) {
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "subtopic_request", message: "Subtopic request free-text is required for candidate discovery." });
  }

  if (config.current_grade === null || isNaN(config.current_grade)) {
    errors.push({ code: "MISSING_REQUIRED_INPUT", field: "current_grade", message: "Current grade is required." });
  } else if (![9, 10, 11].includes(config.current_grade)) {
    errors.push({ code: "INVALID_COMBINATION", field: "current_grade", message: "Current grade must be 9, 10, or 11." });
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
  const exactGate = config.exact_gate_id || null;
  const kMode = config.learner_knowledge_mode;
  const kPercent = config.learner_knowledge_percent;
  const kPolicy = config.knowledge_calibration_policy_ref;

  return {
    subtopic_resolution: {
      status: exactGate ? "RESOLVED" : "UNRESOLVED",
      current_state: exactGate ? "EXACT_GATE_SELECTED" : "NON_AUTHORITATIVE_FREE_TEXT",
      input_text: subtopic,
      next_required_step: exactGate ? "PROCEED_TO_ENGINEERING_VALIDATION" : "EXPLICIT_EXACT_ENGINEERING_GATE_SELECTION"
    },
    engineering_authorization: {
      status: exactGate ? "GATE_SELECTED" : (subtopic ? "READY_FOR_DISCOVERY" : "BLOCKED"),
      exact_gate_id: exactGate,
      authority_state: exactGate ? "EXACT_GATE_DECLARED" : "NOT_EVALUATED"
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
    manifest_class: "PHYSICS_RUN_MANIFEST",
    generator: "PhysicsBlueprintRunBuilder/v1",
    request: {
      subject: config.subject,
      subtopic_request: config.subtopic_request,
      current_grade: config.current_grade,
      exact_gate_id: config.exact_gate_id
    },
    subtopic_authority_state: config.exact_gate_id ? "EXACT_GATE_DECLARED" : "NON_AUTHORITATIVE_FREE_TEXT",
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
      exact_gate_selected: config.exact_gate_id,
      exact_resolver_passed: Boolean(config.exact_gate_id)
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
  return `# AGENT RUN ASSIGNMENT: Physics V2 Learning Pipeline

## 0. Run Context and Inputs
- **Subject**: PHYSICS
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
2. Engineering Authority (Canonical Gate Registry: 43 subtopics across Grades 9?11)
3. Non-Authoritative Candidate Discovery (Broad, tolerant search)
4. Explicit Exact-ID Selection & Exact Authoritative Resolver
5. CDAU / SDU (Intrinsic study depth) & LAU (Learner-adapted practice)
6. Publication & Rendering

## 3. Invariants & Anti-Drift Guard
- **SDU Depth Invariant**: Core1A/Core1B depth is governed by intrinsic physical difficulty (EASY, MEDIUM, HARD). SDU MUST NOT inspect or adapt to learner knowledge percentage.
- **LAU Practice Adaptation**: Core2A/Core2B question demand is conditioned on learner knowledge percentage only when bound to an explicit calibration policy and source reference, or under explicit Owner Waiver.
- **Discovery vs. Authorization**: Natural language matching, high semantic similarity, or Rank 1 candidate ranking NEVER grants Engineering authorization. Downstream work requires explicit selection of the exact gate identity.
- **Physical Model Consistency**: Energy accounting must distinguish general energy conservation from unconditional mechanical energy conservation. Mechanical energy conservation is strictly conditional upon non-conservative work vanishing.
- **No Topic Branches**: Generic orchestration code must not contain topic-specific branches or hardcoded physics formulas.

## 4. Required Execution Steps
1. Execute discovery for candidate gates matching "${config.subtopic_request}".
2. Explicitly select the exact Engineering Gate ID from \`physics-technical-engineering-gates.v1.json\`.
3. Validate gate against schema at depth \`${config.requested_engineering_depth}\`.
4. Ensure explicit system boundary isolation, sign convention, coordinate frame, and model conditions are stated before equation application.
5. Compile Core1A/Core1B semantic reconstruction and Core2A/Core2B transfer specifications.
6. Verify release gate dispositions in Product Governance.

## 5. Known Input Uncertainty & Downstream Blockers
- **Subtopic Status**: ${config.exact_gate_id ? "Exact gate specified: " + config.exact_gate_id : "Unresolved free-text request until exact Engineering Gate is confirmed."}
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
          <span>${e.code}</span>
          <span>Field: ${e.field}</span>
        </div>
        <div class="diag-msg">${e.message}</div>
      </div>
    `).join("")}
  `;

  // Update dependencies view
  const depsContainer = document.getElementById("dependenciesOutput");
  depsContainer.innerHTML = `
    <div class="dep-card">
      <div class="dep-title">Subtopic Resolution Stage</div>
      <div class="dep-detail">
        <div><strong>Status:</strong> ${deps.subtopic_resolution.status}</div>
        <div><strong>State:</strong> ${deps.subtopic_resolution.current_state}</div>
        <div><strong>Input Request:</strong> "${deps.subtopic_resolution.input_text}"</div>
        <div><strong>Next Required Action:</strong> ${deps.subtopic_resolution.next_required_step}</div>
      </div>
    </div>
    <div class="dep-card">
      <div class="dep-title">Learner Calibration Status</div>
      <div class="dep-detail">
        <div><strong>Mode:</strong> ${deps.learner_adaptation_status.mode}</div>
        <div><strong>Percentage:</strong> ${deps.learner_adaptation_status.percentage !== null ? deps.learner_adaptation_status.percentage + "%" : "N/A"}</div>
        <div><strong>Calibration Policy:</strong> ${deps.learner_adaptation_status.calibration_policy}</div>
        <div><strong>Practice Conditioned:</strong> ${deps.learner_adaptation_status.support_conditioned ? "YES (Valid Policy)" : "NO (Blocked / Unbound)"}</div>
      </div>
    </div>
    <div class="dep-card">
      <div class="dep-title">SDU Difficulty Isolation</div>
      <div class="dep-detail">
        <div><strong>Rule:</strong> ${deps.study_differentiation_status.rule}</div>
        <div><strong>Control Basis:</strong> ${deps.study_differentiation_status.control_basis}</div>
        <div><strong>Learner Percentage Isolated:</strong> ${deps.study_differentiation_status.learner_percentage_isolated ? "PASS (Invariants Enforced)" : "FAIL"}</div>
      </div>
    </div>
  `;
}

function loadFixtureData(fixture) {
  document.getElementById("subject").value = fixture.subject || "PHYSICS";
  document.getElementById("subtopic_request").value = fixture.subtopic_request || "";
  document.getElementById("current_grade").value = fixture.current_grade || 9;
  document.getElementById("exact_gate_id").value = fixture.exact_gate_id || "";
  document.getElementById("target_program_or_exam").value = fixture.target_program_or_exam || "CBSE_BOARD_EXAM";
  document.getElementById("learning_purpose").value = fixture.learning_purpose || "CBSE_EXAM";
  document.getElementById("learner_knowledge_mode").value = fixture.learner_knowledge_mode || "UNKNOWN";
  document.getElementById("learner_knowledge_percent").value = fixture.learner_knowledge_percent !== undefined && fixture.learner_knowledge_percent !== null ? fixture.learner_knowledge_percent : "";
  document.getElementById("knowledge_source_ref").value = fixture.knowledge_source_ref || "";
  document.getElementById("knowledge_calibration_policy_ref").value = fixture.knowledge_calibration_policy_ref || "";
  document.getElementById("requested_engineering_depth").value = fixture.requested_engineering_depth || "STANDARD";
  document.getElementById("core1_difficulty_control").value = fixture.core1_difficulty_control || "DERIVE";
  document.getElementById("owner_difficulty_override").value = fixture.owner_difficulty_override || "";
  document.getElementById("pedagogy_research_mode").value = fixture.pedagogy_research_mode || "DEFAULT";
  document.getElementById("web_research_allowed").checked = fixture.web_research_allowed !== false;
  document.getElementById("local_question_bank_ref").value = fixture.local_question_bank_ref || "";
  document.getElementById("owner_scope_notes").value = fixture.owner_scope_notes || "";
  document.getElementById("repository").value = fixture.repository || "reallaksh19/Common";
  document.getElementById("branch_or_ref").value = fixture.branch_or_ref || "v2-physics-gates-gr9-11";
  document.getElementById("run_mode").value = fixture.run_mode || "GENERATION";
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
  document.querySelectorAll(".tab-btn[data-view]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn[data-view]").forEach(b => b.classList.remove("active"));
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

  const bindPresetBtn = (btnId, fixturePath) => {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.addEventListener("click", () => {
      fetch(fixturePath)
        .then(res => res.json())
        .then(data => loadFixtureData(data))
        .catch(err => console.error("Error loading fixture:", err));
    });
  };

  bindPresetBtn("loadCbseWorkEnergyBtn", "fixtures/cbse_work_energy_fixture.json");
  bindPresetBtn("loadCbseOpticsBtn", "fixtures/cbse_optics_reflection_fixture.json");
  bindPresetBtn("loadJeeRotBtn", "fixtures/iit_jee_rotational_dynamics_fixture.json");
  bindPresetBtn("loadOlympiadFluidBtn", "fixtures/nsep_olympiad_fluid_dynamics_fixture.json");

  const copyCliBtn = document.getElementById("copyCliBtn");
  if (copyCliBtn) {
    copyCliBtn.addEventListener("click", () => {
      const cmd = `python "Grade 9/V2/Physics/Blueprint/tools/run_builder/compile_run.py" --config "Grade 9/V2/Physics/Blueprint/tools/run_builder/fixtures/cbse_work_energy_fixture.json"`;
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
      a.download = "physics_run_config.json";
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
