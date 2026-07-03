const data = window.LAMBADA_VIEWER_DATA;

const els = {
  datasetMeta: document.getElementById("datasetMeta"),
  statusStrip: document.getElementById("statusStrip"),
  summaryBand: document.getElementById("summaryBand"),
  searchInput: document.getElementById("searchInput"),
  sortSelect: document.getElementById("sortSelect"),
  stepSelect: document.getElementById("stepSelect"),
  tieOnly: document.getElementById("tieOnly"),
  eosOnly: document.getElementById("eosOnly"),
  incorrectOnly: document.getElementById("incorrectOnly"),
  divergenceOnly: document.getElementById("divergenceOnly"),
  resetFilters: document.getElementById("resetFilters"),
  caseCount: document.getElementById("caseCount"),
  caseList: document.getElementById("caseList"),
  detailPane: document.getElementById("detailPane"),
};

const state = {
  selectedCase: data.cases[0]?.case || null,
  expandedExperiment: null,
};

const expById = new Map(data.experiments.map((exp) => [exp.id, exp]));

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function fmtPct(value) {
  return value == null ? "-" : `${Number(value).toFixed(2)}%`;
}

function fmtProb(value) {
  if (value == null) return "-";
  const number = Number(value);
  if (!Number.isFinite(number)) return "-";
  return number >= 0.01 ? number.toFixed(6) : number.toExponential(4);
}

function shortLabel(exp) {
  const model = exp.model_group
    .replace("GQA-SWA-SINK AS ", "SWA-SINK ")
    .replace("GQA ", "GQA ")
    .replace("Moonlight-16B-A3B", "Moonlight");
  const backend = exp.backend
    .replace("megatron_native", "Megatron")
    .replace("hf_bf16_no_cache", "HF bf16");
  return `${model} · ${backend}`;
}

function caseResults(caseItem) {
  return data.experiments.map((exp) => ({
    exp,
    result: caseItem.experiments[exp.id] || { ties: [] },
  }));
}

function allTies(caseItem) {
  return caseResults(caseItem).flatMap(({ exp, result }) =>
    (result.ties || []).map((tie) => ({ exp, result, tie })),
  );
}

function selectedStep() {
  return els.stepSelect.value === "all" ? null : Number(els.stepSelect.value);
}

function caseMatchesStep(caseItem, step) {
  if (!step) return true;
  return allTies(caseItem).some(({ tie }) => Number(tie.step) === step);
}

function searchableText(caseItem) {
  const generated = caseResults(caseItem)
    .map(({ result }) => `${result.predicted_word_normalized || ""} ${result.generated_text || ""}`)
    .join(" ");
  return `${caseItem.case} ${caseItem.target_text || ""} ${caseItem.prompt_text || ""} ${caseItem.prompt_text_zh || ""} ${generated}`.toLowerCase();
}

function filteredCases() {
  const query = els.searchInput.value.trim().toLowerCase();
  const step = selectedStep();
  let rows = data.cases.filter((caseItem) => {
    if (query && !searchableText(caseItem).includes(query)) return false;
    if (els.tieOnly.checked && caseItem.tie_count === 0) return false;
    if (els.eosOnly.checked && caseItem.eos_tie_count === 0) return false;
    if (els.incorrectOnly.checked && caseItem.correct_count === data.experiments.length) return false;
    if (els.divergenceOnly.checked && !caseItem.has_divergence) return false;
    if (!caseMatchesStep(caseItem, step)) return false;
    return true;
  });

  const sort = els.sortSelect.value;
  rows = [...rows].sort((a, b) => {
    if (sort === "tie_desc") {
      return b.tie_count - a.tie_count || a.row_idx - b.row_idx;
    }
    if (sort === "correct_asc") {
      return a.correct_count - b.correct_count || b.tie_count - a.tie_count || a.row_idx - b.row_idx;
    }
    if (sort === "divergence") {
      return Number(b.has_divergence) - Number(a.has_divergence) || b.tie_count - a.tie_count || a.row_idx - b.row_idx;
    }
    return a.row_idx - b.row_idx;
  });
  return rows;
}

function renderSummary() {
  const counts = data.integrity.counts;
  els.datasetMeta.textContent = `${counts.cases} cases · ${counts.experiments} experiments · ${counts.tie_rows} tie events · ${counts.unique_tie_cases} tie cases`;
  els.statusStrip.innerHTML = [
    `<span class="pill ${data.integrity.ok ? "ok" : "bad"}">integrity ${data.integrity.ok ? "ok" : "failed"}</span>`,
    `<span class="pill">generated ${escapeHtml(data.generated_at)}</span>`,
    `<span class="pill">scoring: ${escapeHtml(data.scoring)}</span>`,
  ].join("");

  els.summaryBand.innerHTML = data.experiments
    .map(
      (exp) => `
        <article class="summary-card">
          <h2>${escapeHtml(shortLabel(exp))}</h2>
          <div class="metric-grid">
            <div class="metric"><span>accuracy</span><strong>${fmtPct(exp.accuracy_percent)}</strong></div>
            <div class="metric"><span>correct</span><strong>${exp.correct}/${exp.total_cases}</strong></div>
            <div class="metric"><span>tie steps</span><strong>${exp.tie_steps}</strong></div>
            <div class="metric"><span>tie cases</span><strong>${exp.tie_case_count}</strong></div>
            <div class="metric"><span>EOS tie</span><strong>${exp.eos_tie_steps}</strong></div>
            <div class="metric"><span>backend</span><strong>${escapeHtml(exp.backend)}</strong></div>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderCaseList(rows) {
  els.caseCount.textContent = `${rows.length} cases`;
  els.caseList.innerHTML = rows
    .map((caseItem) => {
      const active = caseItem.case === state.selectedCase ? " active" : "";
      const tieClass = caseItem.tie_count ? " tie" : "";
      return `
        <button class="case-row${active}" type="button" data-case="${escapeHtml(caseItem.case)}">
          <span class="case-main">
            <span class="case-id">${escapeHtml(caseItem.case)}</span>
            <span class="case-target">target: ${escapeHtml(caseItem.target_text)}</span>
          </span>
          <span class="case-badges">
            <span class="mini-badge ok">${caseItem.correct_count}/${data.experiments.length}</span>
            <span class="mini-badge${tieClass}">tie ${caseItem.tie_count}</span>
          </span>
        </button>
      `;
    })
    .join("");
}

function renderTieTimeline(caseItem) {
  const ties = allTies(caseItem).sort((a, b) => Number(a.tie.step) - Number(b.tie.step) || a.exp.id.localeCompare(b.exp.id));
  if (!ties.length) {
    return `<div class="empty-state">No exact top-2 tie events for this case.</div>`;
  }
  return `
    <div class="tie-timeline">
      ${ties
        .map(({ exp, tie }) => {
          const eosClass = tie.contains_eos ? " eos" : "";
          return `
            <article class="tie-card${eosClass}">
              <div class="tie-topline">
                <span class="pill warn">step ${escapeHtml(tie.step)}</span>
                <span class="pill">${escapeHtml(shortLabel(exp))}</span>
                <span class="pill">selected <code>${escapeHtml(tie.selected_token_text)}</code></span>
                ${tie.contains_eos ? `<span class="pill bad">contains EOS ${escapeHtml(tie.eos_id)}</span>` : ""}
              </div>
              <div class="tie-grid">
                <div class="token-box">
                  <strong>top1</strong>
                  <code class="token-text">${escapeHtml(tie.top1_text)}</code>
                  <span class="token-meta">id ${escapeHtml(tie.top1_token_id)} · p ${fmtProb(tie.top1_prob)} · logp ${fmtProb(tie.top1_logprob)}</span>
                </div>
                <div class="token-box">
                  <strong>top2</strong>
                  <code class="token-text">${escapeHtml(tie.top2_text)}</code>
                  <span class="token-meta">id ${escapeHtml(tie.top2_token_id)} · p ${fmtProb(tie.top2_prob)} · logp ${fmtProb(tie.top2_logprob)}</span>
                </div>
              </div>
            </article>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderComparison(caseItem) {
  const rows = caseResults(caseItem);
  const expandedId =
    state.expandedExperiment && caseItem.experiments[state.expandedExperiment]
      ? state.expandedExperiment
      : rows.find(({ result }) => result.ties?.length)?.exp.id || rows[0]?.exp.id;
  state.expandedExperiment = expandedId;
  const expanded = caseItem.experiments[expandedId] || {};
  const expandedExp = expById.get(expandedId);

  return `
    <div class="comparison-grid">
      ${rows
        .map(({ exp, result }) => {
          const correct = result.correct ? "ok" : "bad";
          const active = exp.id === expandedId ? " active" : "";
          const ties = result.ties || [];
          return `
            <article class="backend-panel${active}" data-exp="${escapeHtml(exp.id)}">
              <h4>${escapeHtml(shortLabel(exp))}</h4>
              <div class="backend-result">
                <span class="pill ${correct}">${result.correct ? "correct" : "wrong"}</span>
                <span class="pill">pred <code>${escapeHtml(result.predicted_word_normalized || "-")}</code></span>
                <span class="pill ${ties.length ? "warn" : ""}">tie ${ties.length}</span>
              </div>
              <div class="generated-text">${escapeHtml(result.generated_text || "")}</div>
            </article>
          `;
        })
        .join("")}
    </div>
    <section class="raw-panel">
      <strong>Expanded backend: ${escapeHtml(shortLabel(expandedExp))}</strong>
      <pre>${escapeHtml(JSON.stringify(expanded, null, 2))}</pre>
    </section>
  `;
}

function renderDetail(caseItem) {
  if (!caseItem) {
    els.detailPane.innerHTML = `<div class="empty-state">No case matches the current filters.</div>`;
    return;
  }

  els.detailPane.innerHTML = `
    <div class="detail-inner">
      <div class="detail-header">
        <div>
          <h2>${escapeHtml(caseItem.case)}</h2>
          <div class="detail-meta">
            <span class="pill">row ${caseItem.row_idx}</span>
            <span class="pill">target <code>${escapeHtml(caseItem.target_text)}</code></span>
            <span class="pill ok">correct ${caseItem.correct_count}/${data.experiments.length}</span>
            <span class="pill ${caseItem.tie_count ? "warn" : ""}">tie ${caseItem.tie_count}</span>
            ${caseItem.eos_tie_count ? `<span class="pill bad">EOS tie ${caseItem.eos_tie_count}</span>` : ""}
            ${caseItem.has_divergence ? `<span class="pill warn">divergent predictions</span>` : ""}
          </div>
        </div>
      </div>

      <div class="section-title">
        <h3>Tie Timeline</h3>
        <span class="pill">exact top1/top2 probability equality</span>
      </div>
      ${renderTieTimeline(caseItem)}

      <div class="section-title">
        <h3>Prompt</h3>
        <span class="pill">${caseItem.char_len_prompt || caseItem.prompt_text.length} chars</span>
      </div>
      <div class="prompt-label">English source</div>
      <div class="prompt-box">${escapeHtml(caseItem.prompt_text)}</div>
      <div class="prompt-label">中文翻译</div>
      <div class="prompt-box zh">${escapeHtml(caseItem.prompt_text_zh || "暂无中文翻译")}</div>

      <div class="section-title">
        <h3>Backend Comparison</h3>
        <span class="pill">click a backend to expand raw fields</span>
      </div>
      ${renderComparison(caseItem)}
    </div>
  `;
}

function render() {
  const rows = filteredCases();
  if (!rows.some((item) => item.case === state.selectedCase)) {
    state.selectedCase = rows[0]?.case || null;
    state.expandedExperiment = null;
  }
  renderCaseList(rows);
  renderDetail(data.cases.find((item) => item.case === state.selectedCase));
}

function resetFilters() {
  els.searchInput.value = "";
  els.sortSelect.value = "tie_desc";
  els.stepSelect.value = "all";
  els.tieOnly.checked = false;
  els.eosOnly.checked = false;
  els.incorrectOnly.checked = false;
  els.divergenceOnly.checked = false;
  render();
}

els.caseList.addEventListener("click", (event) => {
  const row = event.target.closest("[data-case]");
  if (!row) return;
  state.selectedCase = row.dataset.case;
  state.expandedExperiment = null;
  render();
});

els.detailPane.addEventListener("click", (event) => {
  const panel = event.target.closest("[data-exp]");
  if (!panel) return;
  state.expandedExperiment = panel.dataset.exp;
  render();
});

[
  els.searchInput,
  els.sortSelect,
  els.stepSelect,
  els.tieOnly,
  els.eosOnly,
  els.incorrectOnly,
  els.divergenceOnly,
].forEach((el) => el.addEventListener("input", render));
els.resetFilters.addEventListener("click", resetFilters);

renderSummary();
render();
