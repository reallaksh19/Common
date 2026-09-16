document.addEventListener("DOMContentLoaded", async () => {
  let benchmarkData = null;
  try {
    const res = await fetch("engineering_discovery_benchmark_results.json");
    if (res.ok) {
      benchmarkData = await res.json();
      renderMetrics(benchmarkData.metrics, benchmarkData.total_queries);
      renderResults(benchmarkData.results);
    }
  } catch (err) {
    console.log("Could not load benchmark results dynamically. Using mock fallback.", err);
  }

  function renderMetrics(m, total) {
    if (!m) return;
    document.getElementById("metricTotal").textContent = total;
    document.getElementById("metricTop1").textContent = `${(m.top_1_recall * 100).toFixed(1)}%`;
    document.getElementById("metricTop5").textContent = `${(m.top_5_recall * 100).toFixed(1)}%`;
    document.getElementById("metricMiss").textContent = `${(m.miss_rate * 100).toFixed(1)}%`;
  }

  function renderResults(results) {
    const container = document.getElementById("resultsList");
    container.innerHTML = "";
    if (!results || results.length === 0) {
      container.innerHTML = "<p>No benchmark queries loaded.</p>";
      return;
    }
    results.slice(0, 30).forEach(r => {
      const card = document.createElement("div");
      card.className = "query-card";
      const topCand = r.candidates && r.candidates[0] ? r.candidates[0].scope_ref : (r.top_candidate || "None");
      card.innerHTML = `
        <div class="query-header">
          <span>${r.query_id} &bull; ${r.category}</span>
          <span style="color: ${r.status === 'HIT' ? '#4ade80' : '#38bdf8'}">${r.status}</span>
        </div>
        <div class="query-text">${r.query_text}</div>
        <div>
          <span class="candidate-tag">Top: ${topCand}</span>
        </div>
      `;
      container.appendChild(card);
    });
  }
});
