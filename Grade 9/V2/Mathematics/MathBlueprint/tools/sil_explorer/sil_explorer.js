// Subtopic Intelligence Library (SIL) Explorer UI
// Vanilla JS, zero dependencies, offline capable.

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
      chip.textContent = d === "ALL" ? "All Domains" : d.split("&")[0].trim();
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
          <span class="badge">${escapeHtml(p.domain.split("&")[0].trim())}</span>
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

  // Generate interactive SVG for TTUs
  function renderSvgForTtu(gateId, ttuId) {
    if (gateId.includes("QUAD") || gateId.includes("PARAB")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <line x1="20" y1="130" x2="380" y2="130" stroke="#334155" stroke-width="1.5" />
          <line x1="200" y1="10" x2="200" y2="150" stroke="#334155" stroke-width="1.5" />
          <!-- Parabola curve -->
          <path d="M 60,30 Q 200,160 340,30" fill="none" stroke="#38bdf8" stroke-width="2.5" />
          <!-- Vertex -->
          <circle cx="200" cy="95" r="4" fill="#f59e0b" />
          <text x="210" y="98" fill="#f59e0b" font-size="10" font-family="sans-serif">Vertex (-b/2a, -D/4a)</text>
          <!-- Roots -->
          <circle cx="118" cy="130" r="4" fill="#10b981" />
          <text x="105" y="145" fill="#10b981" font-size="10" font-family="sans-serif">α</text>
          <circle cx="282" cy="130" r="4" fill="#10b981" />
          <text x="285" y="145" fill="#10b981" font-size="10" font-family="sans-serif">β</text>
        </svg>
      `;
    }
    if (gateId.includes("TRI")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <!-- Triangle ABC -->
          <polygon points="200,20 80,140 320,140" fill="rgba(59,130,246,0.1)" stroke="#3b82f6" stroke-width="2" />
          <!-- Parallel line DE -->
          <line x1="140" y1="80" x2="260" y2="80" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3" />
          <text x="195" y="15" fill="#93c5fd" font-size="11" font-weight="bold">A</text>
          <text x="65" y="145" fill="#93c5fd" font-size="11" font-weight="bold">B</text>
          <text x="325" y="145" fill="#93c5fd" font-size="11" font-weight="bold">C</text>
          <text x="120" y="82" fill="#fcd34d" font-size="10">D</text>
          <text x="268" y="82" fill="#fcd34d" font-size="10">E</text>
          <text x="200" y="115" fill="#94a3b8" font-size="10" text-anchor="middle">DE || BC ⇒ AD/DB = AE/EC</text>
        </svg>
      `;
    }
    if (gateId.includes("CIRC")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <!-- Circle -->
          <circle cx="200" cy="80" r="60" fill="rgba(139,92,246,0.1)" stroke="#8b5cf6" stroke-width="2" />
          <circle cx="200" cy="80" r="3" fill="#a78bfa" />
          <text x="208" y="83" fill="#a78bfa" font-size="10">O</text>
          <!-- Tangent line -->
          <line x1="100" y1="140" x2="300" y2="140" stroke="#10b981" stroke-width="2" />
          <!-- Radius to tangent -->
          <line x1="200" y1="80" x2="200" y2="140" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3,3" />
          <text x="200" y="155" fill="#6ee7b7" font-size="10" text-anchor="middle">Tangent ⊥ Radius (PT² = PA·PB)</text>
        </svg>
      `;
    }
    if (gateId.includes("TRIG")) {
      return `
        <svg class="svg-canvas" viewBox="0 0 400 160">
          <!-- Right triangle -->
          <polygon points="120,130 280,130 280,30" fill="rgba(6,182,212,0.1)" stroke="#06b6d4" stroke-width="2" />
          <!-- Right angle symbol -->
          <polyline points="265,130 265,115 280,115" fill="none" stroke="#94a3b8" stroke-width="1.5" />
          <text x="140" y="122" fill="#38bdf8" font-size="11">θ</text>
          <text x="200" y="145" fill="#94a3b8" font-size="10" text-anchor="middle">Adjacent (cos θ)</text>
          <text x="290" y="85" fill="#94a3b8" font-size="10">Opposite (sin θ)</text>
          <text x="180" y="70" fill="#fcd34d" font-size="10">Hypotenuse = 1</text>
        </svg>
      `;
    }
    // Default Cartesian / Function Grid
    return `
      <svg class="svg-canvas" viewBox="0 0 400 160">
        <line x1="30" y1="130" x2="370" y2="130" stroke="#334155" stroke-width="1.5" />
        <line x1="200" y1="15" x2="200" y2="145" stroke="#334155" stroke-width="1.5" />
        <path d="M 60,110 L 150,80 L 250,40 L 340,20" fill="none" stroke="#a855f7" stroke-width="2" />
        <text x="200" y="85" fill="#c084fc" font-size="10" text-anchor="middle">Mathematical Invariant Scaffold</text>
      </svg>
    `;
  }

  // Render Detail Area
  function renderDetail() {
    const packet = catalog.find(p => p.gate_id === currentPacketId);
    if (!packet) {
      detailAreaEl.innerHTML = '<div class="empty-state">Select a packet from the sidebar.</div>';
      return;
    }

    let tabContentHtml = "";
    if (activeTab === "layer1") {
      tabContentHtml = `
        <div class="section-box">
          <h3><span>🔒</span> Non-Negotiable Mathematical Preconditions</h3>
          <ul class="bullet-list">
            ${packet.preconditions.map(p => `<li>${formatMath(p)}</li>`).join("")}
          </ul>
        </div>
      `;
    } else if (activeTab === "layer2") {
      tabContentHtml = `
        <div class="section-box">
          <h3><span>🧩</span> Learning Atom DAG (${packet.atoms.length} Atoms)</h3>
          <div class="atom-grid">
            ${packet.atoms.map(a => `
              <div class="atom-card">
                <div class="atom-header">
                  <span class="card-id">${escapeHtml(a.atom_id)}</span>
                  <span class="atom-type-badge type-${escapeHtml(a.atom_type)}">${escapeHtml(a.atom_type)}</span>
                </div>
                <div style="font-size: 0.85rem; color: #cbd5e1;">${formatMath(a.description)}</div>
              </div>
            `).join("")}
          </div>
        </div>
        <div class="section-box" style="margin-top: 16px;">
          <h3><span>⚠️</span> Misconception Diagnostic Contrasts (${packet.misconceptions.length} Pairs)</h3>
          ${packet.misconceptions.map(m => `
            <div class="misc-card">
              <div class="misc-title">Misconception: ${escapeHtml(m.name)}</div>
              <div class="misc-field"><span class="misc-label">Flawed Action:</span> ${formatMath(m.flawed_action)}</div>
              <div class="misc-field"><span class="misc-label">Diagnostic Cue:</span> ${formatMath(m.diagnostic_cue)}</div>
            </div>
          `).join("")}
        </div>
      `;
    } else if (activeTab === "layer3") {
      tabContentHtml = `
        <div class="section-box">
          <h3><span>📐</span> Reconstructable TTUs (${packet.ttus.length} Scaffolds)</h3>
          <div class="ttu-container">
            ${packet.ttus.map(t => `
              <div class="ttu-card">
                <div class="ttu-header">
                  <div>
                    <span class="ttu-id">${escapeHtml(t.ttu_id)}</span>
                    <span style="font-weight: 600; margin-left: 8px;">${escapeHtml(t.title)}</span>
                  </div>
                  <span class="badge" style="background: rgba(245,158,11,0.2); color: #fcd34d;">${escapeHtml(t.role)}</span>
                </div>
                <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 8px;">
                  <strong>Kind:</strong> ${escapeHtml(t.kind)} &bull; <strong>Viewport:</strong> ${escapeHtml(t.viewport)}
                </div>
                <div class="interactive-preview">
                  ${renderSvgForTtu(packet.gate_id, t.ttu_id)}
                </div>
                <div class="ttu-dual-panel">
                  <div class="ttu-box">
                    <h4>Incomplete Scaffold</h4>
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
    } else if (activeTab === "layer4") {
      tabContentHtml = `
        <div class="section-box">
          <h3><span>🏆</span> Competitive Exam Problem Taxonomy (${packet.families.length} Families)</h3>
          <div style="display: flex; flex-direction: column; gap: 12px;">
            ${packet.families.map(f => `
              <div style="background: var(--bg-card); border-left: 4px solid var(--accent-emerald); padding: 12px; border-radius: 4px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                  <strong style="color: #6ee7b7; font-family: monospace;">${escapeHtml(f.family_id)}</strong>
                  <span class="badge exam">${escapeHtml(f.tier)}</span>
                </div>
                <div style="font-size: 0.88rem; color: #cbd5e1;">${formatMath(f.description)}</div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    detailAreaEl.innerHTML = `
      <div class="packet-hero">
        <div class="hero-meta">
          <span class="header-badge">Section ${packet.section_number}</span>
          <span class="card-id" style="font-size: 0.9rem;">${escapeHtml(packet.gate_id)}</span>
          <span class="hero-domain">&bull; ${escapeHtml(packet.domain)}</span>
        </div>
        <div class="hero-title">${escapeHtml(packet.title)}</div>
        <div class="card-tags">
          <span class="badge" style="background: rgba(6,182,212,0.2); color: #67e8f9;">${escapeHtml(packet.grade_level)}</span>
          ${packet.exam_families.map(e => `<span class="badge exam">${escapeHtml(e)}</span>`).join("")}
        </div>
      </div>

      <div class="layer-tabs">
        <button class="tab-btn ${activeTab === 'layer1' ? 'active' : ''}" data-tab="layer1">Layer 1: Preconditions</button>
        <button class="tab-btn ${activeTab === 'layer2' ? 'active' : ''}" data-tab="layer2">Layer 2: Atoms & Misconceptions</button>
        <button class="tab-btn ${activeTab === 'layer3' ? 'active' : ''}" data-tab="layer3">Layer 3: Reconstructable TTUs</button>
        <button class="tab-btn ${activeTab === 'layer4' ? 'active' : ''}" data-tab="layer4">Layer 4: Problem Families</button>
      </div>

      <div class="layer-content">
        ${tabContentHtml}
      </div>
    `;

    // Bind tab events
    detailAreaEl.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        activeTab = btn.getAttribute("data-tab");
        renderDetail();
      });
    });
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

  function formatMath(str) {
    if (!str) return "";
    let s = escapeHtml(str);
    // Render bold markdown
    s = s.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // Render code markdown
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    return s;
  }

  // Bind Search Input
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value.trim();
    renderPacketList();
  });

  // Init
  renderDomainFilters();
  renderPacketList();
  renderDetail();
});
