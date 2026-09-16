document.addEventListener("DOMContentLoaded", () => {
  const presets = {
    cbse_class9_matter_atoms: { subtopic: "Chemical Symbols and Atomic Notation", gate: "CHEM-SYM-LITERACY", grade: 9, depth: "STANDARD" },
    cbse_class10_reactions_metals: { subtopic: "Chemical Equation Balancing", gate: "CHEM-EQ-BALANCING", grade: 10, depth: "STANDARD" },
    jee_advanced_thermo_equil: { subtopic: "Gibbs Free Energy and Equilibrium", gate: "CHEM-THERMO-GIBBS-SPONTANEITY", grade: 11, depth: "DEEP" },
    olympiad_bonding_mechanisms: { subtopic: "Molecular Orbital Theory", gate: "CHEM-BOND-MOT-DIATOMIC", grade: 11, depth: "RESEARCH" }
  };

  const presetSelect = document.getElementById("presetSelect");
  const subtopicInput = document.getElementById("subtopicRequest");
  const gateInput = document.getElementById("exactGateId");
  const gradeSelect = document.getElementById("gradeSelect");
  const depthSelect = document.getElementById("depthSelect");

  function applyPreset(p) {
    const d = presets[p];
    if (d) {
      subtopicInput.value = d.subtopic;
      gateInput.value = d.gate;
      gradeSelect.value = d.grade;
      depthSelect.value = d.depth;
    }
  }

  presetSelect.addEventListener("change", (e) => applyPreset(e.target.value));
  applyPreset("cbse_class9_matter_atoms");

  document.getElementById("compileBtn").addEventListener("click", () => {
    const config = {
      subject: "CHEMISTRY",
      subtopic_request: subtopicInput.value,
      exact_gate_id: gateInput.value || null,
      current_grade: parseInt(gradeSelect.value, 10),
      requested_engineering_depth: depthSelect.value,
      learning_purpose: "CBSE_BOARD_EXAM",
      learner_knowledge_mode: "UNKNOWN"
    };
    document.getElementById("manifestDigest").textContent = "sha256:d48a... (compiled)";
    document.getElementById("manifestJson").textContent = JSON.stringify(config, null, 2);
    document.getElementById("agentPrompt").textContent = "# AGENT RUN ASSIGNMENT: Chemistry V2 Learning Pipeline\n- Subtopic: " + config.subtopic_request;
  });
});
