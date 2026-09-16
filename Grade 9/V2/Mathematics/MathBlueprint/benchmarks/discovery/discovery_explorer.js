/**
 * Engineering Discovery Benchmark Explorer - Interactive Logic
 * Fully topic-independent: reads all data generically from JSON assets.
 */

let benchmarkData = null;
let corpusData = null;
let vocabularyData = null;

// Embedded baseline summary if local CORS blocks fetch()
const DEFAULT_METRICS = {
  TOTAL_QUERIES: 80,
  VALID_TARGET_QUERIES: 77,
  NO_TARGET_QUERIES: 3,
  TOP_1_RECALL: 1.0,
  TOP_3_RECALL: 1.0,
  TOP_5_RECALL: 1.0,
  MISS_RATE: 0.0,
  NOISE_RATE: 0.0541,
  AMBIGUITY_PRESERVATION_RATE: 0.95,
  NO_VALID_TARGET_BEHAVIOR_SAFE: true,
  VOCABULARY_CONTRIBUTION_RATE: 0.987,
  DETERMINISM: true
};

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initFilters();
  initPlayground();
  loadData();
});

function initTabs() {
  const tabs = document.querySelectorAll(".tab-btn[data-view]");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const viewName = tab.getAttribute("data-view");
      document.querySelectorAll(".view-panel").forEach(panel => {
        panel.style.display = "none";
      });

      const activePanel = document.getElementById(`${viewName}View`);
      if (activePanel) {
        activePanel.style.display = "block";
      }
    });
  });
}

async function loadData() {
  try {
    const resResults = await fetch("engineering_discovery_benchmark_results.json");
    if (resResults.ok) {
      benchmarkData = await resResults.json();
    }
  } catch (e) {
    console.warn("Could not fetch benchmark results via HTTP, checking local file notice:", e);
  }

  try {
    const resCorpus = await fetch("corpus/engineering_discovery_benchmark_corpus.v1.json");
    if (resCorpus.ok) {
      corpusData = await resCorpus.json();
    }
  } catch (e) {
    console.warn("Could not fetch corpus via HTTP:", e);
  }

  try {
    const resVocab = await fetch("../../policies/mathematics-engineering-discovery-vocabulary.v1.json");
    if (resVocab.ok) {
      vocabularyData = await resVocab.json();
    }
  } catch (e) {
    console.warn("Could not fetch vocabulary via HTTP:", e);
  }

  // Setup file input fallback
  const fileNotice = document.getElementById("localFileNotice");
  const fileInput = document.getElementById("localFileInput");
  if (!benchmarkData && fileNotice) {
    fileNotice.style.display = "block";
    fileInput.addEventListener("change", (ev) => {
      const file = ev.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const parsed = JSON.parse(e.target.result);
          if (parsed.results) {
            benchmarkData = parsed;
          } else if (parsed.entries) {
            vocabularyData = parsed;
          } else if (parsed.queries) {
            corpusData = parsed;
          }
          fileNotice.style.display = "none";
          renderAll();
        } catch (err) {
          alert("Error parsing JSON file: " + err.message);
        }
      };
      reader.readAsText(file);
    });
  }

  renderAll();
}

function renderAll() {
  renderMetrics();
  renderQueriesTable();
  renderVocabularyTable();
  populateDropdowns();
  runPlaygroundDiscovery();
}

function renderMetrics() {
  const metrics = (benchmarkData && benchmarkData.metrics) ? benchmarkData.metrics : DEFAULT_METRICS;
  document.getElementById("top1RecallVal").textContent = (metrics.TOP_1_RECALL * 100).toFixed(1) + "%";
  document.getElementById("top3RecallVal").textContent = (metrics.TOP_3_RECALL * 100).toFixed(1) + "%";
  document.getElementById("top5RecallVal").textContent = (metrics.TOP_5_RECALL * 100).toFixed(1) + "%";
  document.getElementById("missRateVal").textContent = (metrics.MISS_RATE * 100).toFixed(1) + "%";
  document.getElementById("totalQueriesVal").textContent = metrics.TOTAL_QUERIES || 80;

  if (vocabularyData && vocabularyData.entries) {
    const totalTerms = vocabularyData.entries.reduce((acc, e) => acc + (e.terms ? e.terms.length : 0), 0);
    document.getElementById("vocabTermsVal").textContent = totalTerms;
    document.getElementById("vocabStatsBadge").textContent = `${vocabularyData.entries.length} Gates • ${totalTerms} Terms`;
  }
}

function populateDropdowns() {
  if (corpusData && corpusData.queries) {
    const catSelect = document.getElementById("queryCategoryFilter");
    const categories = new Set(corpusData.queries.map(q => q.query_category));
    categories.forEach(cat => {
      if (!Array.from(catSelect.options).some(o => o.value === cat)) {
        const opt = document.createElement("option");
        opt.value = cat;
        opt.textContent = cat.replace(/_/g, " ");
        catSelect.appendChild(opt);
      }
    });
  }

  if (vocabularyData && vocabularyData.entries) {
    const gateSelect = document.getElementById("vocabGateFilter");
    vocabularyData.entries.forEach(entry => {
      if (!Array.from(gateSelect.options).some(o => o.value === entry.target_scope_ref)) {
        const opt = document.createElement("option");
        opt.value = entry.target_scope_ref;
        opt.textContent = entry.target_scope_ref;
        gateSelect.appendChild(opt);
      }
    });
  }
}

function renderQueriesTable() {
  const tbody = document.getElementById("queriesTableBody");
  tbody.innerHTML = "";

  const resultsList = (benchmarkData && benchmarkData.results) ? benchmarkData.results : [];
  const search = document.getElementById("querySearchInput").value.toLowerCase().trim();
  const catFilter = document.getElementById("queryCategoryFilter").value;
  const rankFilter = document.getElementById("queryRankFilter").value;

  let shownCount = 0;

  resultsList.forEach(item => {
    const hitRank = (item.hit_ranks && item.hit_ranks.length > 0) ? item.hit_ranks[0] : null;

    // Filters
    if (catFilter !== "ALL" && item.category !== catFilter) return;
    if (rankFilter === "RANK1" && hitRank !== 1) return;
    if (rankFilter === "RANK2_3" && (hitRank < 2 || hitRank > 3)) return;
    if (rankFilter === "MISS" && item.has_hit) return;

    const matchText = (item.query_id + " " + item.query_text + " " + (item.expected || []).join(" ")).toLowerCase();
    if (search && !matchText.includes(search)) return;

    shownCount++;
    const tr = document.createElement("tr");

    let rankBadge = `<span class="badge badge-miss">MISS</span>`;
    if (hitRank === 1) {
      rankBadge = `<span class="badge badge-rank1">Rank 1</span>`;
    } else if (hitRank && hitRank <= 3) {
      rankBadge = `<span class="badge badge-rank-sub">Rank ${hitRank}</span>`;
    } else if (hitRank) {
      rankBadge = `<span class="badge" style="background:var(--bg-card); color:var(--text-secondary);">Rank ${hitRank}</span>`;
    }

    const topObserved = (item.observed_candidates && item.observed_candidates.length > 0)
      ? item.observed_candidates[0]
      : "<em style='color:var(--text-secondary);'>None</em>";

    tr.innerHTML = `
      <td><strong>${item.query_id}</strong></td>
      <td>${escapeHtml(item.query_text)}</td>
      <td><span class="badge badge-category">${item.category}</span></td>
      <td><code>${(item.expected || []).join(", ") || "None (Out of Domain)"}</code></td>
      <td>${rankBadge}</td>
      <td><code>${topObserved}</code></td>
    `;
    tbody.appendChild(tr);
  });

  document.getElementById("queryCountDisplay").textContent = `${shownCount} of ${resultsList.length} Queries`;
}

function renderVocabularyTable() {
  const tbody = document.getElementById("vocabTableBody");
  tbody.innerHTML = "";

  if (!vocabularyData || !vocabularyData.entries) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:var(--text-secondary); padding:20px;">Vocabulary catalog loaded or available via HTTP/local file.</td></tr>`;
    return;
  }

  const search = document.getElementById("vocabSearchInput").value.toLowerCase().trim();
  const gateFilter = document.getElementById("vocabGateFilter").value;
  const classFilter = document.getElementById("vocabClassFilter").value;

  vocabularyData.entries.forEach(entry => {
    if (gateFilter !== "ALL" && entry.target_scope_ref !== gateFilter) return;

    (entry.terms || []).forEach(term => {
      if (classFilter !== "ALL" && term.term_class !== classFilter) return;
      if (search && !term.phrase.toLowerCase().includes(search) && !entry.target_scope_ref.toLowerCase().includes(search)) return;

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${escapeHtml(term.phrase)}</strong></td>
        <td><span class="badge badge-termclass">${term.term_class}</span></td>
        <td><code>${entry.target_scope_ref}</code></td>
        <td><span style="font-size:0.75rem; color:var(--text-secondary);">${entry.target_scope_kind}</span></td>
      `;
      tbody.appendChild(tr);
    });
  });
}

function initFilters() {
  ["querySearchInput", "queryCategoryFilter", "queryRankFilter"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", renderQueriesTable);
  });

  ["vocabSearchInput", "vocabGateFilter", "vocabClassFilter"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", renderVocabularyTable);
  });
}

function initPlayground() {
  const btn = document.getElementById("runPlaygroundBtn");
  const input = document.getElementById("playgroundQueryInput");
  if (btn && input) {
    btn.addEventListener("click", runPlaygroundDiscovery);
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") runPlaygroundDiscovery();
    });
  }
}

function runPlaygroundDiscovery() {
  const query = (document.getElementById("playgroundQueryInput").value || "").trim();
  const candidatesContainer = document.getElementById("candidatesContainer");
  const jsonBox = document.getElementById("discoveryReceiptJson");

  if (!query) {
    candidatesContainer.innerHTML = "<p style='color:var(--text-secondary); font-size:0.875rem;'>Please enter a search query.</p>";
    return;
  }

  // Pure generic scoring against loaded vocabulary entries
  const queryTokens = tokenize(query);
  const candidatesMap = {};

  if (vocabularyData && vocabularyData.entries) {
    vocabularyData.entries.forEach(entry => {
      const scopeRef = entry.target_scope_ref;
      let score = 0;
      const basis = [];

      (entry.terms || []).forEach(term => {
        const termPhrase = term.phrase.toLowerCase();
        if (query.toLowerCase() === termPhrase) {
          score += 100;
          basis.push("VOCABULARY_EXACT");
        } else if (query.toLowerCase().includes(termPhrase)) {
          score += 50;
          basis.push("VOCABULARY_SUBSTRING");
        } else {
          const termTokens = tokenize(termPhrase);
          const overlap = termTokens.filter(t => queryTokens.includes(t));
          if (overlap.length > 0) {
            score += overlap.length * 10;
            basis.push("TOKEN_OVERLAP");
          }
        }
      });

      if (score > 0) {
        if (!candidatesMap[scopeRef] || score > candidatesMap[scopeRef].score) {
          candidatesMap[scopeRef] = {
            scope_kind: entry.target_scope_kind || "ENGINEERING_GATE",
            scope_ref: scopeRef,
            score: Math.min(1.0, score / 100),
            match_basis: Array.from(new Set(basis))
          };
        }
      }
    });
  }

  const sortedCandidates = Object.values(candidatesMap)
    .sort((a, b) => b.score - a.score)
    .slice(0, 6)
    .map((c, idx) => ({ ...c, rank: idx + 1 }));

  // Render UI Cards
  candidatesContainer.innerHTML = "";
  if (sortedCandidates.length === 0) {
    candidatesContainer.innerHTML = `
      <div style="padding:16px; background:var(--bg-card); border-radius:6px; color:var(--text-secondary); font-size:0.875rem;">
        <em>Zero candidates found. Non-authoritative discovery does not fabricate identities for unmapped queries.</em>
      </div>
    `;
  } else {
    sortedCandidates.forEach(c => {
      const card = document.createElement("div");
      card.className = "candidate-card";
      card.innerHTML = `
        <div class="candidate-rank">#${c.rank}</div>
        <div class="candidate-details">
          <div class="candidate-id">${c.scope_ref}</div>
          <div class="candidate-score">Score: ${(c.score * 100).toFixed(0)}%</div>
        </div>
        <div>
          ${c.match_basis.map(b => `<span class="basis-tag">${b}</span>`).join("")}
        </div>
      `;
      candidatesContainer.appendChild(card);
    });
  }

  // Render JSON Receipt
  const receipt = {
    schema_version: "1.0.0",
    subject: "MATHEMATICS",
    authority: "CANDIDATE_DISCOVERY_ONLY",
    technical_authorization: "NOT_EVALUATED",
    publication_authorization: "NOT_IMPLIED",
    automatic_selection: false,
    requires_explicit_exact_selection: true,
    query_text: query,
    candidate_count: sortedCandidates.length,
    candidates: sortedCandidates
  };

  jsonBox.textContent = JSON.stringify(receipt, null, 2);
}

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9]/g, " ").split(/\s+/).filter(t => t.length > 1);
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
