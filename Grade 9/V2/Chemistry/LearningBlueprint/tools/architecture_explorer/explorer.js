document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("architecture_observation_manifest.json");
    if (res.ok) {
      const data = await res.json();
      document.getElementById("statsBox").textContent = `Total Components: ${data.component_count} | Relations: ${data.relation_count} | Manifest Digest: ${data.manifest_digest.slice(0, 20)}...`;
      const grid = document.getElementById("componentsList");
      grid.innerHTML = "";
      Object.values(data.components).forEach(c => {
        const el = document.createElement("div");
        el.className = "comp-card";
        el.innerHTML = `<div class="comp-type">${c.component_type}</div><div class="comp-name">${c.name}</div>`;
        grid.appendChild(el);
      });
    }
  } catch (err) {
    document.getElementById("statsBox").textContent = "Loaded offline mode.";
  }
});
