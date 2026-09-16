// Blueprint Architecture Explorer - Client Application
let manifestData = null;
let currentView = "components";

async function loadManifest() {
  try {
    const response = await fetch("architecture_observation_manifest.json");
    if (!response.ok) throw new Error("Network response was not ok");
    manifestData = await response.json();
    initApp();
  } catch (error) {
    console.warn("Fetch failed, attempting fallback to file picker:", error);
    document.getElementById("contentPanel").innerHTML = `
      <div class="gap-alert-card">
        <div class="gap-alert-title">Manifest Auto-Load Blocked by Browser Local File Policy</div>
        <p>Browsers restrict <code>fetch()</code> over the <code>file://</code> protocol. To view the architecture explorer:</p>
        <p>1. <strong>Direct File Selection:</strong> Choose <code>architecture_observation_manifest.json</code> from this directory:</p>
        <div style="margin: 0.75rem 0;">
          <input type="file" id="manifestFileInput" accept=".json" style="background:var(--bg-card); color:var(--text-primary); padding:0.4rem; border:1px solid var(--border-color); border-radius:4px;">
        </div>
        <p>2. <strong>Or Local Server:</strong> Run <code>python -m http.server</code> in this directory and browse to <code>http://localhost:8000</code>.</p>
      </div>`;
    const fileInput = document.getElementById("manifestFileInput");
    if (fileInput) {
      fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (evt) => {
          try {
            manifestData = JSON.parse(evt.target.result);
            initApp();
          } catch (err) {
            alert("Error parsing JSON manifest: " + err.message);
          }
        };
        reader.readAsText(file);
      });
    }
  }
}

function initApp() {
  renderStats();
  populateFilters();
  setupEventListeners();
  renderCurrentView();
}

function renderStats() {
  if (!manifestData) return;
  document.getElementById("statComponents").textContent = manifestData.component_count;
  document.getElementById("statRelations").textContent = manifestData.relation_count;
  const gapCount = Object.values(manifestData.gap_reports || {}).reduce((acc, arr) => acc + arr.length, 0);
  document.getElementById("statGaps").textContent = gapCount;
  const schemas = Object.values(manifestData.components).filter(c => c.component_type === "SCHEMA").length;
  document.getElementById("statSchemas").textContent = schemas;
}

function populateFilters() {
  if (!manifestData) return;
  const domains = new Set();
  const types = new Set();

  Object.values(manifestData.components).forEach(c => {
    if (c.authority_domain) domains.add(c.authority_domain);
    if (c.component_type) types.add(c.component_type);
  });

  const domainSelect = document.getElementById("filterDomain");
  domainSelect.innerHTML = '<option value="ALL">All Authority Domains</option>';
  Array.from(domains).sort().forEach(d => {
    domainSelect.innerHTML += `<option value="${d}">${d}</option>`;
  });

  const typeSelect = document.getElementById("filterType");
  typeSelect.innerHTML = '<option value="ALL">All Component Types</option>';
  Array.from(types).sort().forEach(t => {
    typeSelect.innerHTML += `<option value="${t}">${t}</option>`;
  });
}

function setupEventListeners() {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", e => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentView = btn.dataset.view;
      renderCurrentView();
    });
  });

  document.getElementById("searchInput").addEventListener("input", filterAndRender);
  document.getElementById("filterDomain").addEventListener("change", filterAndRender);
  document.getElementById("filterType").addEventListener("change", filterAndRender);

  document.querySelectorAll(".preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.getElementById("searchInput").value = btn.dataset.query;
      filterAndRender();
    });
  });
}

function filterAndRender() {
  renderCurrentView();
}

function getFilteredComponents() {
  if (!manifestData) return [];
  const search = document.getElementById("searchInput").value.toLowerCase().trim();
  const domain = document.getElementById("filterDomain").value;
  const type = document.getElementById("filterType").value;

  return Object.values(manifestData.components).filter(c => {
    const matchesDomain = domain === "ALL" || c.authority_domain === domain;
    const matchesType = type === "ALL" || c.component_type === type;
    const matchesSearch = !search ||
      c.name.toLowerCase().includes(search) ||
      c.title.toLowerCase().includes(search) ||
      c.path.toLowerCase().includes(search) ||
      c.authority_domain.toLowerCase().includes(search);

    return matchesDomain && matchesType && matchesSearch;
  });
}

function renderCurrentView() {
  document.querySelectorAll(".view-section").forEach(s => s.classList.remove("active"));
  const activeSection = document.getElementById(`view-${currentView}`);
  if (activeSection) activeSection.classList.add("active");

  switch (currentView) {
    case "components":
      renderComponentGrid();
      break;
    case "lifecycle":
      renderLifecycleTable();
      break;
    case "authority":
      renderAuthorityMap();
      break;
    case "graph":
      renderDependencyGraph();
      break;
    case "gaps":
      renderGapsView();
      break;
  }
}

function renderComponentGrid() {
  const container = document.getElementById("componentGrid");
  const components = getFilteredComponents();
  if (components.length === 0) {
    container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px;">No components matched filter criteria.</div>`;
    return;
  }

  container.innerHTML = components.map(c => `
    <div class="component-card">
      <div class="card-header">
        <div class="card-title">${c.name}</div>
        <span class="badge badge-${c.component_type}">${c.component_type}</span>
      </div>
      <div class="card-domain">${c.authority_domain}</div>
      <div class="card-meta">
        <div><strong>Path:</strong> <code>${c.path}</code></div>
        ${c.schema_version !== "N/A" ? `<div><strong>Version:</strong> ${c.schema_version}</div>` : ""}
        ${c.producer_refs.length ? `<div><strong>Producers:</strong> <span class="rel-tag-list">${c.producer_refs.map(r => `<span class="rel-tag">${r.replace("engine:", "")}</span>`).join("")}</span></div>` : ""}
        ${c.validator_refs.length ? `<div><strong>Validators:</strong> <span class="rel-tag-list">${c.validator_refs.map(r => `<span class="rel-tag">${r.replace("engine:", "")}</span>`).join("")}</span></div>` : ""}
        ${c.consumer_refs.length ? `<div><strong>Consumers:</strong> <span class="rel-tag-list">${c.consumer_refs.map(r => `<span class="rel-tag">${r.replace("engine:", "")}</span>`).join("")}</span></div>` : ""}
        ${c.test_refs.length ? `<div><strong>Tests:</strong> <span class="rel-tag-list">${c.test_refs.map(r => `<span class="rel-tag">${r.replace("test:", "")}</span>`).join("")}</span></div>` : ""}
      </div>
    </div>
  `).join("");
}

function renderLifecycleTable() {
  const container = document.getElementById("lifecycleTableBody");
  if (!manifestData) return;
  const schemas = Object.values(manifestData.components).filter(c => c.component_type === "SCHEMA");

  container.innerHTML = schemas.map(s => {
    const producers = s.producer_refs.map(p => p.replace("engine:", "")).join(", ") || '<span style="color:var(--text-secondary)">None</span>';
    const validators = s.validator_refs.map(v => v.replace("engine:", "")).join(", ") || '<span style="color:var(--accent-rose)">None</span>';
    const consumers = s.consumer_refs.map(c => c.replace("engine:", "")).join(", ") || '<span style="color:var(--text-secondary)">None</span>';
    const tests = s.test_refs.map(t => t.replace("test:", "")).join(", ") || '<span style="color:var(--accent-amber)">None</span>';

    return `
      <tr>
        <td><strong>${s.name}</strong><br><small style="color:var(--text-secondary)">${s.authority_domain}</small></td>
        <td><code>${producers}</code></td>
        <td><code>${validators}</code></td>
        <td><code>${consumers}</code></td>
        <td><code>${tests}</code></td>
      </tr>
    `;
  }).join("");
}

function renderAuthorityMap() {
  const container = document.getElementById("authorityMapContainer");
  if (!manifestData) return;
  const domainGroups = {};

  Object.values(manifestData.components).forEach(c => {
    const d = c.authority_domain || "UNASSIGNED";
    if (!domainGroups[d]) domainGroups[d] = [];
    domainGroups[d].push(c);
  });

  container.innerHTML = Object.entries(domainGroups).sort().map(([domain, comps]) => `
    <div class="component-card" style="margin-bottom: 16px;">
      <div class="card-header">
        <h3 style="color:var(--accent-blue); font-size:1.1rem;">${domain}</h3>
        <span class="badge" style="background:var(--bg-secondary); color:var(--text-primary);">${comps.length} components</span>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px;">
        ${comps.map(c => `<span class="rel-tag" style="background:rgba(255,255,255,0.05);">${c.name} <small style="color:var(--text-secondary)">(${c.component_type})</small></span>`).join("")}
      </div>
    </div>
  `).join("");
}

function renderDependencyGraph() {
  const svg = document.getElementById("graphSvg");
  if (!svg || !manifestData) return;

  const width = svg.clientWidth || 900;
  const height = svg.clientHeight || 650;
  svg.innerHTML = "";

  // Render a clean SVG representation of key subsystem relationships
  const subsystems = [
    { id: "GT", label: "Ground Truth", x: 120, y: 320, color: "#38bdf8" },
    { id: "C0", label: "Core0 Evidence Router", x: 300, y: 320, color: "#818cf8" },
    { id: "C1", label: "Core1 Semantic Models", x: 480, y: 200, color: "#c084fc" },
    { id: "C2", label: "Core2 Assessment Demand", x: 480, y: 440, color: "#f472b6" },
    { id: "ENG", label: "Engineering Gates Registry", x: 300, y: 100, color: "#34d399" },
    { id: "DISC", label: "Discovery (Non-Auth)", x: 120, y: 100, color: "#fbbf24" },
    { id: "CDR", label: "Canonical Domain Registry", x: 660, y: 320, color: "#2dd4bf" },
    { id: "SDU", label: "SDU Study Differentiation", x: 820, y: 200, color: "#a78bfa" },
    { id: "LAU", label: "LAU Learner Adaptation", x: 820, y: 440, color: "#f43f5e" },
    { id: "PUB", label: "Governed Publication", x: 980, y: 320, color: "#38bdf8" }
  ];

  const links = [
    { from: "DISC", to: "ENG", label: "exact selection" },
    { from: "ENG", to: "CDR", label: "custody binding" },
    { from: "GT", to: "C0", label: "evidence" },
    { from: "C0", to: "C1", label: "routes" },
    { from: "C0", to: "C2", label: "routes" },
    { from: "C1", to: "CDR", label: "concept join" },
    { from: "C2", to: "CDR", label: "problem join" },
    { from: "CDR", to: "SDU", label: "governed models" },
    { from: "CDR", to: "LAU", label: "governed problems" },
    { from: "SDU", to: "PUB", label: "Core1A/1B pages" },
    { from: "LAU", to: "PUB", label: "Core2A/2B pages" }
  ];

  // Draw links
  links.forEach(link => {
    const s = subsystems.find(n => n.id === link.from);
    const t = subsystems.find(n => n.id === link.to);
    if (!s || !t) return;

    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", s.x);
    line.setAttribute("y1", s.y);
    line.setAttribute("x2", t.x);
    line.setAttribute("y2", t.y);
    line.setAttribute("stroke", "#475569");
    line.setAttribute("stroke-width", "2");
    line.setAttribute("stroke-dasharray", link.from === "DISC" ? "4,4" : "none");
    svg.appendChild(line);

    // Midpoint label
    const midX = (s.x + t.x) / 2;
    const midY = (s.y + t.y) / 2;
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", midX);
    text.setAttribute("y", midY - 6);
    text.setAttribute("fill", "#94a3b8");
    text.setAttribute("font-size", "10");
    text.setAttribute("text-anchor", "middle");
    text.textContent = link.label;
    svg.appendChild(text);
  });

  // Draw nodes
  subsystems.forEach(node => {
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", node.x);
    circle.setAttribute("cy", node.y);
    circle.setAttribute("r", "32");
    circle.setAttribute("fill", "#1e293b");
    circle.setAttribute("stroke", node.color);
    circle.setAttribute("stroke-width", "3");

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", node.x);
    text.setAttribute("y", node.y + 4);
    text.setAttribute("fill", "#f8fafc");
    text.setAttribute("font-size", "11");
    text.setAttribute("font-weight", "600");
    text.setAttribute("text-anchor", "middle");
    text.textContent = node.id;

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", node.x);
    label.setAttribute("y", node.y + 46);
    label.setAttribute("fill", node.color);
    label.setAttribute("font-size", "10");
    label.setAttribute("font-weight", "500");
    label.setAttribute("text-anchor", "middle");
    label.textContent = node.label;

    g.appendChild(circle);
    g.appendChild(text);
    g.appendChild(label);
    svg.appendChild(g);
  });
}

function renderGapsView() {
  const container = document.getElementById("gapsContainer");
  if (!manifestData) return;
  const gaps = manifestData.gap_reports || {};

  container.innerHTML = `
    <div class="gap-alert-card">
      <div class="gap-alert-title">Schemas Without Validator (${gaps.schemas_without_validator?.length || 0})</div>
      <p style="font-size:0.85rem; margin-bottom:6px;">These schemas are defined in <code>contracts/</code> but have no dedicated <code>validate_*.py</code> validator or validation function detected in <code>engine/</code>:</p>
      <ul class="gap-list">
        ${(gaps.schemas_without_validator || []).map(id => `<li><code>${id.replace("schema:", "")}</code></li>`).join("")}
      </ul>
    </div>

    <div class="gap-alert-card" style="border-color: rgba(251, 191, 36, 0.4); background: rgba(251, 191, 36, 0.08);">
      <div class="gap-alert-title" style="color:var(--accent-amber);">Validators Without Tests (${gaps.validators_without_tests?.length || 0})</div>
      <p style="font-size:0.85rem; margin-bottom:6px;">These validators exist in <code>engine/</code> but have no discovered test suites in <code>tests/</code> importing them directly:</p>
      <ul class="gap-list">
        ${(gaps.validators_without_tests || []).map(id => `<li><code>${id.replace("engine:", "")}</code></li>`).join("")}
      </ul>
    </div>

    <div class="gap-alert-card" style="border-color: rgba(148, 163, 184, 0.4); background: rgba(148, 163, 184, 0.08);">
      <div class="gap-alert-title" style="color:var(--text-secondary);">Orphan / Unreferenced Schemas (${gaps.orphan_schemas?.length || 0})</div>
      <p style="font-size:0.85rem; margin-bottom:6px;">Schemas with no discovered producer, consumer, or validator:</p>
      <ul class="gap-list">
        ${(gaps.orphan_schemas || []).map(id => `<li><code>${id.replace("schema:", "")}</code></li>`).join("")}
      </ul>
    </div>
  `;
}

document.addEventListener("DOMContentLoaded", loadManifest);
