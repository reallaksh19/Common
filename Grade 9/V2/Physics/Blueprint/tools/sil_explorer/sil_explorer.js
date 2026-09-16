// Physics Subtopic Intelligence Library (SIL) Explorer UI
// Vanilla JS, zero external dependencies, 100% offline capable.

document.addEventListener("DOMContentLoaded", () => {
  const catalog = window.SIL_CATALOG || [];
  let currentPacketId = catalog.length > 0 ? catalog[0].gate_id : null;
  let activeTab = "layer1";
  let activeDomain = "ALL";
  let searchQuery = "";

  const packetListEl = document.getElementById("packet-list");
  const detailAreaEl = document.getElementById("detail-area");
  const searchInput = document.getElementById("search-input");
  const domainFiltersEl = document.getElementById("domain-filters");

  // Collect unique domains
  const domains = ["ALL", ...new Set(catalog.map(p => p.domain))];

  // Render Domain Filter Chips
  function renderDomainFilters() {
    domainFiltersEl.innerHTML = "";
    domains.forEach(d => {
      const chip = document.createElement("div");
      chip.className = `filter-chip ${d === activeDomain ? "active" : ""}`;
      chip.textContent = d === "ALL" ? "All Domains" : d.split("/")[0].trim();
      chip.title = d;
      chip.addEventListener("click", () => {
        activeDomain = d;
        renderDomainFilters();
        renderPacketList();
      });
      domainFiltersEl.appendChild(chip);
    });
  }

  // Filter packets
  function getFilteredPackets() {
    return catalog.filter(p => {
      const matchesDomain = activeDomain === "ALL" || p.domain === activeDomain;
      const q = searchQuery.toLowerCase();
      const matchesSearch = !q ||
        p.title.toLowerCase().includes(q) ||
        p.gate_id.toLowerCase().includes(q) ||
        p.domain.toLowerCase().includes(q);
      return matchesDomain && matchesSearch;
    });
  }

  // Render Packet List in Sidebar
  function renderPacketList() {
    const filtered = getFilteredPackets();
    packetListEl.innerHTML = "";

    if (filtered.length === 0) {
      packetListEl.innerHTML = '<div class="empty-state">No packets match search.</div>';
      return;
    }

    filtered.forEach(p => {
      const card = document.createElement("div");
      card.className = `packet-card ${p.gate_id === currentPacketId ? "selected" : ""}`;
      card.innerHTML = `
        <div class="card-header">
          <span class="card-id">${escapeHtml(p.gate_id)}</span>
          <span class="card-grade">${escapeHtml(p.grade_level)}</span>
        </div>
        <div class="card-title">${escapeHtml(p.title)}</div>
        <div class="card-tags">
          <span class="badge">${escapeHtml(p.domain.split("/")[0].trim())}</span>
          ${p.exam_families.slice(0, 3).map(e => `<span class="badge exam">${escapeHtml(e)}</span>`).join("")}
        </div>
      `;
      card.addEventListener("click", () => {
        currentPacketId = p.gate_id;
        renderPacketList();
        renderDetail();
      });
      packetListEl.appendChild(card);
    });
  }

  // Generate interactive SVG for Physics TTUs
  function renderSvgForTtu(gateId, ttuId) {
    if (gateId.includes("PROJ") || gateId.includes("GRAV-FREE-FALL")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <line x1="20" y1="140" x2="380" y2="140" stroke="#334155" stroke-width="1.5" />
          <line x1="40" y1="20" x2="40" y2="150" stroke="#334155" stroke-width="1.5" />
          <!-- Projectile parabola -->
          <path d="M 40,140 Q 200,10 360,140" fill="none" stroke="#38bdf8" stroke-width="2.5" />
          <!-- Launch velocity vector -->
          <line x1="40" y1="140" x2="100" y2="80" stroke="#f59e0b" stroke-width="2" marker-end="url(#arrow)" />
          <text x="60" y="130" fill="#f59e0b" font-size="10">θ</text>
          <text x="105" y="75" fill="#fcd34d" font-size="10">v₀</text>
          <!-- Apex -->
          <circle cx="200" cy="75" r="4" fill="#10b981" />
          <line x1="200" y1="75" x2="250" y2="75" stroke="#10b981" stroke-width="2" />
          <text x="255" y="78" fill="#6ee7b7" font-size="10">v_top = v₀ cos θ</text>
          <text x="200" y="155" fill="#94a3b8" font-size="10" text-anchor="middle">Horizontal Range R = (v₀² sin 2θ)/g</text>
        </svg>
      `;
    }
    if (gateId.includes("NLM") || gateId.includes("WEP") || gateId.includes("FORCE")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <!-- Incline plane -->
          <polygon points="50,140 350,140 350,40" fill="rgba(59,130,246,0.1)" stroke="#3b82f6" stroke-width="2" />
          <!-- Angle theta -->
          <text x="100" y="135" fill="#93c5fd" font-size="11">θ</text>
          <!-- Block on incline -->
          <rect x="180" y="70" width="40" height="30" transform="rotate(-18.4, 200, 85)" fill="#1e293b" stroke="#06b6d4" stroke-width="2" />
          <!-- FBD Vectors -->
          <!-- Gravity -->
          <line x1="200" y1="85" x2="200" y2="145" stroke="#ef4444" stroke-width="2" />
          <text x="205" y="140" fill="#fca5a5" font-size="10">mg</text>
          <!-- Normal -->
          <line x1="200" y1="85" x2="175" y2="35" stroke="#10b981" stroke-width="2" />
          <text x="160" y="35" fill="#6ee7b7" font-size="10">N = mg cos θ</text>
          <!-- Friction -->
          <line x1="200" y1="85" x2="240" y2="72" stroke="#f59e0b" stroke-width="2" />
          <text x="245" y="70" fill="#fcd34d" font-size="10">f_k = μN</text>
        </svg>
      `;
    }
    if (gateId.includes("CIRC") || gateId.includes("ROT") || gateId.includes("ORBIT")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <!-- Circular orbit -->
          <circle cx="200" cy="80" r="55" fill="rgba(139,92,246,0.1)" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="4,3" />
          <!-- Center -->
          <circle cx="200" cy="80" r="4" fill="#a78bfa" />
          <text x="208" y="83" fill="#a78bfa" font-size="10">O (Pivot)</text>
          <!-- Revolving mass -->
          <circle cx="200" cy="25" r="6" fill="#38bdf8" />
          <!-- Centripetal Force vector -->
          <line x1="200" y1="25" x2="200" y2="60" stroke="#ef4444" stroke-width="2" />
          <text x="205" y="50" fill="#fca5a5" font-size="10">F_c = mv²/R</text>
          <!-- Tangential velocity vector -->
          <line x1="200" y1="25" x2="255" y2="25" stroke="#10b981" stroke-width="2" />
          <text x="260" y="28" fill="#6ee7b7" font-size="10">v = ωR</text>
          <text x="200" y="152" fill="#94a3b8" font-size="10" text-anchor="middle">Pure Radial Acceleration: a_r ⊥ v</text>
        </svg>
      `;
    }
    if (gateId.includes("OPTIC") || gateId.includes("REF")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <!-- Principal Axis -->
          <line x1="20" y1="80" x2="380" y2="80" stroke="#334155" stroke-width="1.5" />
          <!-- Convex Lens -->
          <path d="M 200,20 Q 215,80 200,140 Q 185,80 200,20" fill="rgba(6,182,212,0.15)" stroke="#06b6d4" stroke-width="2" />
          <!-- Foci -->
          <circle cx="120" cy="80" r="3" fill="#f59e0b" />
          <text x="115" y="95" fill="#fcd34d" font-size="10">F₁</text>
          <circle cx="280" cy="80" r="3" fill="#f59e0b" />
          <text x="275" y="95" fill="#fcd34d" font-size="10">F₂</text>
          <!-- Object arrow -->
          <line x1="70" y1="80" x2="70" y2="40" stroke="#10b981" stroke-width="2.5" />
          <!-- Incident ray parallel -->
          <line x1="70" y1="40" x2="200" y2="40" stroke="#38bdf8" stroke-width="1.5" />
          <!-- Refracted ray through F2 -->
          <line x1="200" y1="40" x2="330" y2="120" stroke="#38bdf8" stroke-width="1.5" />
          <!-- Undeviated central ray -->
          <line x1="70" y1="40" x2="330" y2="120" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="3,2" />
          <text x="200" y="155" fill="#94a3b8" font-size="10" text-anchor="middle">Lens Formula: 1/f = 1/v - 1/u</text>
        </svg>
      `;
    }
    if (gateId.includes("ELEC") || gateId.includes("MAG")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <!-- Magnetic Field region -->
          <rect x="60" y="25" width="280" height="110" fill="rgba(16,185,129,0.05)" stroke="#334155" stroke-dasharray="2,2" />
          <!-- B field markers (crosses) -->
          <text x="80" y="55" fill="#334155" font-size="12">⊗</text>
          <text x="140" y="55" fill="#334155" font-size="12">⊗</text>
          <text x="200" y="55" fill="#334155" font-size="12">⊗</text>
          <text x="260" y="55" fill="#334155" font-size="12">⊗</text>
          <text x="320" y="55" fill="#334155" font-size="12">⊗</text>
          <text x="140" y="105" fill="#334155" font-size="12">⊗</text>
          <text x="260" y="105" fill="#334155" font-size="12">⊗</text>
          <!-- Wire conductor -->
          <line x1="200" y1="20" x2="200" y2="140" stroke="#f59e0b" stroke-width="3" />
          <!-- Current direction arrow -->
          <line x1="200" y1="110" x2="200" y2="60" stroke="#f59e0b" stroke-width="4" />
          <text x="210" y="65" fill="#fcd34d" font-size="11" font-weight="bold">I (Current)</text>
          <!-- Lorentz force arrow -->
          <line x1="200" y1="80" x2="120" y2="80" stroke="#ef4444" stroke-width="2.5" />
          <text x="100" y="75" fill="#fca5a5" font-size="11" font-weight="bold">F = I(L × B)</text>
          <text x="200" y="152" fill="#94a3b8" font-size="10" text-anchor="middle">Right Hand Rule: Thumb=I, Fingers=B, Palm=F</text>
        </svg>
      `;
    }
    // Default SHM/Wave canvas
    return `
      <svg class="svg-canvas" viewBox="0 0 400 160">
        <!-- Axes -->
        <line x1="20" y1="80" x2="380" y2="80" stroke="#334155" stroke-width="1.5" />
        <line x1="40" y1="15" x2="40" y2="145" stroke="#334155" stroke-width="1.5" />
        <!-- Harmonic Sine wave -->
        <path d="M 40,80 Q 80,15 120,80 T 200,80 T 280,80 T 360,80" fill="none" stroke="#a855f7" stroke-width="2.5" />
        <!-- Amplitude line -->
        <line x1="80" y1="80" x2="80" y2="47" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3,3" />
        <text x="85" y="65" fill="#fcd34d" font-size="10">A (Amplitude)</text>
        <circle cx="80" cy="47" r="3.5" fill="#f59e0b" />
        <text x="80" y="38" fill="#fcd34d" font-size="10" text-anchor="middle">Crest</text>
        <!-- Wavelength line -->
        <line x1="80" y1="20" x2="240" y2="20" stroke="#06b6d4" stroke-width="1.5" />
        <text x="160" y="15" fill="#67e8f9" font-size="10" text-anchor="middle">Wavelength λ = v/f</text>
        <text x="200" y="152" fill="#94a3b8" font-size="10" text-anchor="middle">Governing Invariant: x(t) = A sin(ωt + φ)</text>
      </svg>
    `;
  }

  // Render Detail Area
  function renderDetail() {
    const packet = catalog.find(p => p.gate_id === currentPacketId);
    if (!packet) {
      detailAreaEl.innerHTML = '<div class="empty-state">Select a subtopic packet from the sidebar.</div>';
      return;
    }

    detailAreaEl.innerHTML = `
      <div class="packet-hero">
        <div class="hero-meta">
          <span class="card-id">${escapeHtml(packet.gate_id)}</span>
          <span class="badge">${escapeHtml(packet.grade_level)}</span>
          ${packet.exam_families.map(e => `<span class="badge exam">${escapeHtml(e)}</span>`).join("")}
        </div>
        <div class="hero-title">${escapeHtml(packet.title)}</div>
        <div class="hero-domain">Domain: ${escapeHtml(packet.domain)}</div>
      </div>

      <div class="layer-tabs">
        <button class="tab-btn ${activeTab === "layer1" ? "active" : ""}" data-tab="layer1">Layer 1: Physical Core</button>
        <button class="tab-btn ${activeTab === "layer2" ? "active" : ""}" data-tab="layer2">Layer 2: Cognitive Atoms & Traps</button>
        <button class="tab-btn ${activeTab === "layer3" ? "active" : ""}" data-tab="layer3">Layer 3: Reconstructable TTUs</button>
        <button class="tab-btn ${activeTab === "layer4" ? "active" : ""}" data-tab="layer4">Layer 4: Problem Families</button>
      </div>

      <div class="layer-content">
        ${renderActiveTabContent(packet)}
      </div>
    `;

    // Bind tab clicks
    detailAreaEl.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        activeTab = btn.getAttribute("data-tab");
        renderDetail();
      });
    });
  }

  function renderActiveTabContent(p) {
    if (activeTab === "layer1") {
      return `
        <div class="section-box">
          <h3><span>⚖️</span> Non-Negotiable Physical Preconditions</h3>
          <ul class="bullet-list">
            ${p.preconditions.map(c => `<li>${escapeHtml(c)}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    if (activeTab === "layer2") {
      return `
        <div class="section-box">
          <h3><span>🧩</span> Learning Atom DAG (${p.atoms.length} Atoms)</h3>
          <div class="atom-grid">
            ${p.atoms.map(a => `
              <div class="atom-card">
                <div class="atom-header">
                  <span class="card-id">${escapeHtml(a.atom_id)}</span>
                  <span class="atom-type-badge type-${escapeHtml(a.atom_type)}">${escapeHtml(a.atom_type)}</span>
                </div>
                <div style="font-size:0.82rem; color:#cbd5e1;">${escapeHtml(a.description)}</div>
              </div>
            `).join("")}
          </div>
        </div>

        <div class="section-box">
          <h3><span>⚠️</span> Verified Misconception Contrast Pairs (${p.misconceptions.length} Pairs)</h3>
          ${p.misconceptions.map(m => `
            <div class="misc-card">
              <div class="misc-title">Misconception: ${escapeHtml(m.name)}</div>
              <div class="misc-field"><span class="misc-label">Flawed Action:</span> <span style="color:#f87171;">${escapeHtml(m.flawed_action)}</span></div>
              <div class="misc-field"><span class="misc-label">Diagnostic Cue:</span> <span style="color:#34d399;">${escapeHtml(m.diagnostic_cue)}</span></div>
            </div>
          `).join("")}
        </div>
      `;
    }

    if (activeTab === "layer3") {
      return `
        <div class="section-box">
          <h3><span>📐</span> Reconstructable Technical Task Units (${p.ttus.length} TTUs)</h3>
          <div class="ttu-container">
            ${p.ttus.map(t => `
              <div class="ttu-card">
                <div class="ttu-header">
                  <span class="ttu-id">${escapeHtml(t.ttu_id)}: ${escapeHtml(t.title)}</span>
                  <span class="badge">${escapeHtml(t.role)}</span>
                </div>
                <div class="interactive-preview">
                  ${renderSvgForTtu(p.gate_id, t.ttu_id)}
                </div>
                <div class="ttu-dual-panel">
                  <div class="ttu-box">
                    <h4>Incomplete Scaffold (Learner Facing)</h4>
                    <pre>${escapeHtml(t.scaffold)}</pre>
                  </div>
                  <div class="ttu-box">
                    <h4>Completion Key (Verification Only)</h4>
                    <pre>${escapeHtml(t.completion_key)}</pre>
                  </div>
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    if (activeTab === "layer4") {
      return `
        <div class="section-box">
          <h3><span>🎯</span> Competitive Exam Problem Families (${p.families.length} Families)</h3>
          <div class="bullet-list" style="list-style:none; padding-left:0;">
            ${p.families.map(f => `
              <li style="margin-bottom:12px; background:var(--bg-card); padding:12px; border-radius:6px; border:1px solid var(--border-color);">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                  <strong style="color:var(--accent-amber);">${escapeHtml(f.family_id)}</strong>
                  <span class="badge exam">${escapeHtml(f.tier)}</span>
                </div>
                <div style="font-size:0.85rem; color:#cbd5e1;">${escapeHtml(f.description)}</div>
              </li>
            `).join("")}
          </div>
        </div>
      `;
    }

    return "";
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Bind Search Input
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value;
    renderPacketList();
  });

  // Initial Boot
  renderDomainFilters();
  renderPacketList();
  renderDetail();
});
