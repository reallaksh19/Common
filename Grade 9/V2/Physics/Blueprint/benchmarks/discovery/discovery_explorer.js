/**
 * Physics Engineering Discovery Benchmark Explorer - Interactive Logic
 * Fully topic-independent: reads all data generically from JSON assets.
 */

let benchmarkData = null;
let corpusData = null;
let vocabularyData = null;

const DEFAULT_METRICS = {
  TOTAL_QUERIES: 167,
  VALID_TARGET_QUERIES: 163,
  NO_TARGET_QUERIES: 4,
  TOP_1_RECALL: 1.0,
  TOP_3_RECALL: 1.0,
  TOP_5_RECALL: 1.0,
  MISS_RATE: 0.0,
  NOISE_RATE: 0.0,
  AMBIGUITY_PRESERVATION_RATE: 1.0,
  NO_VALID_TARGET_BEHAVIOR_SAFE: true,
  VOCABULARY_CONTRIBUTION_RATE: 1.0,
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
    const resVocab = await fetch("../../policy/physics-engineering-discovery-vocabulary.v1.json");
    if (resVocab.ok) {
      vocabularyData = await resVocab.json();
    }
  } catch (e) {
    console.warn("Could not fetch vocabulary via HTTP:", e);
  }

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
          renderApp();
        } catch (err) {
          alert("Error parsing JSON file: " + err.message);
        }
      };
      reader.readAsText(file);
    });
  }

  renderApp();
}

function renderApp() {
  renderDashboard();
  renderQueriesTable();
  renderVocabularyTable();
}

function renderDashboard() {
  const metrics = benchmarkData ? benchmarkData.metrics : DEFAULT_METRICS;
  document.getElementById("top1Recall").textContent = (metrics.top_1_recall * 100).toFixed(1) + "%";
  document.getElementById("top3Recall").textContent = (metrics.top_3_recall * 100).toFixed(1) + "%";
  document.getElementById("top5Recall").textContent = (metrics.top_5_recall * 100).toFixed(1) + "%";
  document.getElementById("missRate").textContent = (metrics.miss_rate * 100).toFixed(1) + "%";
}

function initFilters() {
  const querySearch = document.getElementById("querySearchInput");
  const queryCat = document.getElementById("queryCategoryFilter");
  const queryRank = document.getElementById("queryRankFilter");

  if (querySearch) querySearch.addEventListener("input", renderQueriesTable);
  if (queryCat) queryCat.addEventListener("change", renderQueriesTable);
  if (queryRank) queryRank.addEventListener("change", renderQueriesTable);

  const vocabSearch = document.getElementById("vocabSearchInput");
  const vocabGate = document.getElementById("vocabGateFilter");
  const vocabClass = document.getElementById("vocabClassFilter");

  if (vocabSearch) vocabSearch.addEventListener("input", renderVocabularyTable);
  if (vocabGate) vocabGate.addEventListener("change", renderVocabularyTable);
  if (vocabClass) vocabClass.addEventListener("change", renderVocabularyTable);
}

function renderQueriesTable() {
  if (!benchmarkData && !corpusData) return;
  const tbody = document.getElementById("queriesTableBody");
  if (!tbody) return;

  const resultsList = benchmarkData ? benchmarkData.results : [];
  const search = (document.getElementById("querySearchInput")?.value || "").toLowerCase().trim();
  const catFilter = document.getElementById("queryCategoryFilter")?.value || "ALL";
  const rankFilter = document.getElementById("queryRankFilter")?.value || "ALL";

  // Populate category filter options once
  const catSelect = document.getElementById("queryCategoryFilter");
  if (catSelect && catSelect.children.length <= 1) {
    const categories = new Set(resultsList.map(r => r.category));
    Array.from(categories).sort().forEach(c => {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c;
      catSelect.appendChild(opt);
    });
  }

  const filtered = resultsList.filter(r => {
    const matchesCat = catFilter === "ALL" || r.category === catFilter;
    const matchesRank = rankFilter === "ALL" ||
      (rankFilter === "RANK1" && r.best_rank === 1) ||
      (rankFilter === "RANK2_3" && r.best_rank && r.best_rank >= 2 && r.best_rank <= 3) ||
      (rankFilter === "MISS" && (!r.best_rank || r.status === "MISS"));

    const matchesSearch = !search ||
      r.query_text.toLowerCase().includes(search) ||
      r.query_id.toLowerCase().includes(search) ||
      r.category.toLowerCase().includes(search) ||
      (r.candidates && r.candidates.some(c => c.scope_ref.toLowerCase().includes(search)));

    return matchesCat && matchesRank && matchesSearch;
  });

  const countDisplay = document.getElementById("queryCountDisplay");
  if (countDisplay) {
    countDisplay.textContent = `${filtered.length} / ${resultsList.length} Queries`;
  }

  tbody.innerHTML = filtered.map(r => {
    let rankBadge = `<span class="badge badge-rank1">Rank 1</span>`;
    if (!r.best_rank) {
      rankBadge = `<span class="badge badge-miss">${r.status}</span>`;
    } else if (r.best_rank > 1) {
      rankBadge = `<span class="badge badge-rank-sub">Rank ${r.best_rank}</span>`;
    }

    const topCand = r.candidates && r.candidates[0] ? r.candidates[0].scope_ref : "None";
    const expGates = corpusData ? (corpusData.queries.find(q => q.query_id === r.query_id)?.acceptable_candidate_refs || []).join(", ") : "N/A";

    return `
      <tr>
        <td><code>${r.query_id}</code></td>
        <td><strong>${r.query_text}</strong></td>
        <td><span class="badge badge-category">${r.category}</span></td>
        <td><code>${expGates}</code></td>
        <td>${rankBadge}</td>
        <td><code>${topCand}</code></td>
      </tr>
    `;
  }).join("");
}

function renderVocabularyTable() {
  if (!vocabularyData) return;
  const tbody = document.getElementById("vocabTableBody");
  if (!tbody) return;

  const search = (document.getElementById("vocabSearchInput")?.value || "").toLowerCase().trim();
  const gateFilter = document.getElementById("vocabGateFilter")?.value || "ALL";
  const classFilter = document.getElementById("vocabClassFilter")?.value || "ALL";

  // Populate gate filter options once
  const gateSelect = document.getElementById("vocabGateFilter");
  if (gateSelect && gateSelect.children.length <= 1) {
    const gates = vocabularyData.entries.map(e => e.target_scope_ref);
    gates.sort().forEach(g => {
      const opt = document.createElement("option");
      opt.value = g;
      opt.textContent = g;
      gateSelect.appendChild(opt);
    });
  }

  const rows = [];
  vocabularyData.entries.forEach(entry => {
    entry.terms.forEach(term => {
      rows.push({
        phrase: term.phrase,
        term_class: term.term_class,
        target_scope_ref: entry.target_scope_ref,
        target_scope_kind: entry.target_scope_kind
      });
    });
  });

  const filtered = rows.filter(r => {
    const matchesGate = gateFilter === "ALL" || r.target_scope_ref === gateFilter;
    const matchesClass = classFilter === "ALL" || r.term_class === classFilter;
    const matchesSearch = !search ||
      r.phrase.toLowerCase().includes(search) ||
      r.target_scope_ref.toLowerCase().includes(search) ||
      r.term_class.toLowerCase().includes(search);

    return matchesGate && matchesClass && matchesSearch;
  });

  const badge = document.getElementById("vocabStatsBadge");
  if (badge) {
    badge.textContent = `${vocabularyData.entries.length} Gates ? ${rows.length} Terms`;
  }

  tbody.innerHTML = filtered.slice(0, 300).map(r => `
    <tr>
      <td><strong>${r.phrase}</strong></td>
      <td><span class="badge badge-termclass">${r.term_class}</span></td>
      <td><code>${r.target_scope_ref}</code></td>
      <td><span class="badge">${r.target_scope_kind}</span></td>
    </tr>
  `).join("");
}

function initPlayground() {
  const btn = document.getElementById("runPlaygroundBtn");
  const input = document.getElementById("playgroundQueryInput");
  if (!btn || !input) return;

  btn.addEventListener("click", () => {
    const query = input.value.trim();
    if (!query) return;

    // Simulate non-authoritative discovery receipt
    const mockCandidates = [];
    if (vocabularyData) {
      const qTokens = query.toLowerCase().split(/\s+/);
      vocabularyData.entries.forEach(entry => {
        let score = 0;
        const matched = [];
        entry.terms.forEach(term => {
          const tLower = term.phrase.toLowerCase();
          if (query.toLowerCase() === tLower) {
            score += 700;
            matched.push(term.phrase);
          } else if (query.toLowerCase().includes(tLower) || tLower.includes(query.toLowerCase())) {
            score += 280;
            matched.push(term.phrase);
          } else {
            const overlap = qTokens.filter(tok => tLower.includes(tok) && tok.length > 2);
            if (overlap.length > 0) {
              score += 65 * overlap.length;
              matched.push(term.phrase);
            }
          }
        });
        if (score > 0) {
          mockCandidates.push({
            scope_kind: entry.target_scope_kind,
            scope_ref: entry.target_scope_ref,
            learner_label: entry.target_scope_ref.replace("PHY-", "").replace(/-/g, " "),
            score: score,
            match_basis: ["VOCABULARY_TOKEN"],
            matched_vocabulary_terms: matched.slice(0, 3),
            declared_technical_readiness: "ACTIVE_PRODUCTION",
            source_scope: "CBSE_GRADE_9_11"
          });
        }
      });
    }

    mockCandidates.sort((a, b) => b.score - a.score);
    const topCandidates = mockCandidates.slice(0, 5);
    topCandidates.forEach((c, i) => { c.rank = i + 1; });

    const container = document.getElementById("candidatesContainer");
    if (topCandidates.length === 0) {
      container.innerHTML = `<div style="color:var(--text-secondary); padding:16px;">No candidate gates matched query.</div>`;
    } else {
      container.innerHTML = topCandidates.map(c => `
        <div class="candidate-card">
          <div class="candidate-rank">#${c.rank}</div>
          <div class="candidate-details">
            <div class="candidate-id">${c.scope_ref}</div>
            <div style="font-size:0.85rem; color:var(--text-primary); margin:2px 0;">${c.learner_label}</div>
            <div class="candidate-score">Score: <strong>${c.score}</strong> ${c.matched_vocabulary_terms.map(t => `<span class="basis-tag">${t}</span>`).join("")}</div>
          </div>
        </div>
      `).join("");
    }

    const receipt = {
      schema_version: "1.1.0",
      subject: "PHYSICS",
      discovery_id: "PHY-ENG-DISC-PLAYGROUND_RUN",
      query: query,
      view_class: "NON_AUTHORITATIVE_ENGINEERING_DISCOVERY",
      authority: "CANDIDATE_DISCOVERY_ONLY",
      technical_authorization: "NOT_EVALUATED",
      publication_authorization: "NOT_IMPLIED",
      automatic_selection: false,
      requires_explicit_exact_selection: true,
      candidate_count: topCandidates.length,
      candidates: topCandidates
    };

    document.getElementById("discoveryReceiptJson").textContent = JSON.stringify(receipt, null, 2);
  });
}
