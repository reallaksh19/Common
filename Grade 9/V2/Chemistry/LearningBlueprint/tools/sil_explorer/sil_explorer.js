document.addEventListener("DOMContentLoaded", () => {
  const catalog = window.SIL_CATALOG || [];
  const list = document.getElementById("packetList");
  const detail = document.getElementById("detailArea");
  const search = document.getElementById("searchInput");

  function renderList(items) {
    list.innerHTML = "";
    items.forEach(p => {
      const item = document.createElement("div");
      item.className = "packet-item";
      item.innerHTML = `<div class="packet-gid">${p.gate_id} &bull; ${p.grade_level}</div><div class="packet-title">${p.title}</div>`;
      item.addEventListener("click", () => showDetail(p, item));
      list.appendChild(item);
    });
  }

  function showDetail(p, elem) {
    document.querySelectorAll(".packet-item").forEach(i => i.classList.remove("active"));
    if (elem) elem.classList.add("active");

    detail.innerHTML = `
      <h2 style="color: #fff; margin-bottom: 0.5rem;">${p.title}</h2>
      <div style="color: #c084fc; font-family: monospace; margin-bottom: 1.5rem;">Gate ID: ${p.gate_id} | ${p.domain} | ${p.grade_level}</div>

      <div class="layer-card">
        <h3>Layer 1: Chemical Core & Preconditions</h3>
        <ul style="padding-left: 1.2rem; color: #cbd5e1;">
          ${p.preconditions.map(c => `<li>${c}</li>`).join("")}
        </ul>
      </div>

      <div class="layer-card">
        <h3>Layer 2: Learning Atoms</h3>
        ${p.atoms.map(a => `<div style="margin-bottom: 0.6rem;"><span class="atom-badge">${a.atom_id} (${a.atom_type})</span><span style="color: #e2e8f0;">${a.description}</span></div>`).join("")}
      </div>

      <div class="layer-card">
        <h3>Layer 2: Misconception Contrasts</h3>
        ${p.misconceptions.map(m => `<div style="margin-bottom: 0.8rem;"><strong style="color: #f87171;">Misconception:</strong> ${m.name}<br/><span style="color: #94a3b8;">Flawed Action: ${m.flawed_action}</span><br/><span style="color: #4ade80;">Diagnostic Cue: ${m.diagnostic_cue}</span></div>`).join("")}
      </div>

      <div class="layer-card">
        <h3>Layer 3: Reconstructable TTU Library</h3>
        ${p.ttus.map(t => `<div style="margin-bottom: 1rem;"><strong style="color: #38bdf8;">${t.ttu_id}: ${t.title}</strong><pre style="background: #0f172a; padding: 0.8rem; border-radius: 4px; font-family: monospace; font-size: 0.8rem; margin-top: 0.4rem; color: #f1f5f9; white-space: pre-wrap;">[INCOMPLETE STATE]\n${t.scaffold}\n\n[COMPLETION KEY]\n${t.completion_key}</pre></div>`).join("")}
      </div>
    `;
  }

  search.addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase();
    const filtered = catalog.filter(p => p.gate_id.toLowerCase().includes(q) || p.title.toLowerCase().includes(q));
    renderList(filtered);
  });

  renderList(catalog);
  if (catalog.length > 0) {
    showDetail(catalog[0], list.children[0]);
  }
});
