// Tab Switching Logic
function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(tab => {
    tab.classList.remove('active');
  });
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });

  const targetTab = document.getElementById(tabId);
  if (targetTab) {
    targetTab.classList.add('active');
  }

  // Highlight corresponding tab button
  const buttons = document.querySelectorAll('.tab-btn');
  if (tabId === 'tab-trace') buttons[0].classList.add('active');
  if (tabId === 'tab-cost') buttons[1].classList.add('active');
  if (tabId === 'tab-prod') buttons[2].classList.add('active');
  if (tabId === 'tab-tools') {
    buttons[3].classList.add('active');
    loadToolsMatrix();
  }
}

// 1. Load Sample Trace
async function loadSampleTrace() {
  const container = document.getElementById('trace-tree-container');
  container.innerHTML = '<p style="color: var(--text-muted);">Memuat pohon eksekusi trace...</p>';

  try {
    const res = await fetch('/api/sample-trace');
    const data = await res.json();

    let html = `
      <div style="background: rgba(56, 189, 248, 0.1); padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(56, 189, 248, 0.3); margin-bottom: 1rem;">
        <strong>Trace:</strong> ${data.name} | <strong>ID:</strong> ${data.trace_id} | <strong>Total Latency:</strong> ${data.total_duration_ms} ms
      </div>
    `;

    data.spans.forEach((span, index) => {
      const typeClass = span.type.toLowerCase();
      const indentStyle = `margin-left: ${index * 1.5}rem;`;

      html += `
        <div class="trace-node ${typeClass}" style="${indentStyle}">
          <div style="display: flex; justify-content: space-between; font-weight: 700;">
            <span>[${span.type}] ${span.name}</span>
            <span style="color: var(--accent-gold);">${span.duration_ms} ms</span>
          </div>
          <div class="trace-meta">
            <span>Span ID: ${span.span_id}</span>
            <span>Attributes: ${JSON.stringify(span.attributes)}</span>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<p style="color: var(--accent-red);">Gagal memuat trace: ${err.message}</p>`;
  }
}

// 2. Calculate Cost
async function calculateCost() {
  const model = document.getElementById('model-select').value;
  const prompt_tokens = parseInt(document.getElementById('input-tokens').value) || 0;
  const completion_tokens = parseInt(document.getElementById('output-tokens').value) || 0;
  const outputDiv = document.getElementById('cost-result-output');

  try {
    const res = await fetch('/api/calculate-cost', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model, prompt_tokens, completion_tokens })
    });
    const data = await res.json();

    outputDiv.innerHTML = `
      <p><strong>Model:</strong> ${data.model}</p>
      <p><strong>Input Tokens:</strong> ${data.prompt_tokens} (${data.input_cost_usd} USD)</p>
      <p><strong>Output Tokens:</strong> ${data.completion_tokens} (${data.output_cost_usd} USD)</p>
      <hr style="border-color: var(--border-color); margin: 0.5rem 0;">
      <p style="font-size: 1.2rem; color: var(--accent-gold); font-weight: 700;">
        Total Biaya: $${data.total_cost_usd} USD
      </p>
    `;
  } catch (err) {
    outputDiv.innerHTML = `<p style="color: var(--accent-red);">Gagal menghitung biaya: ${err.message}</p>`;
  }
}

// 3. Run Production Evaluation
async function runEvaluation() {
  const query = document.getElementById('eval-query').value;
  const context = document.getElementById('eval-context').value;
  const response = document.getElementById('eval-response').value;
  const resultDiv = document.getElementById('eval-result-container');

  resultDiv.style.display = 'block';
  resultDiv.innerHTML = '<p style="color: var(--text-muted);">Menjalankan LLM-as-a-Judge evaluation...</p>';

  try {
    const res = await fetch('/api/evaluate-output', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, context, response })
    });
    const data = await res.json();

    const isPassed = data.verdict.includes("PASSED");
    const statusColor = isPassed ? "var(--accent-green)" : "var(--accent-red)";

    resultDiv.innerHTML = `
      <div style="background: var(--bg-secondary); padding: 1.2rem; border-radius: 8px; border: 1px solid ${statusColor};">
        <h4 style="color: ${statusColor}; margin-bottom: 0.5rem;">Verdict: ${data.verdict}</h4>
        <p><strong>Faithfulness Score:</strong> ${(data.faithfulness_score * 100).toFixed(1)}%</p>
        <p><strong>Answer Relevance:</strong> ${(data.answer_relevance_score * 100).toFixed(1)}%</p>
        <p><strong>Hallucination Risk:</strong> ${(data.hallucination_risk * 100).toFixed(1)}%</p>
      </div>
    `;
  } catch (err) {
    resultDiv.innerHTML = `<p style="color: var(--accent-red);">Gagal mengevaluasi: ${err.message}</p>`;
  }
}

// 4. Load Tools Matrix
async function loadToolsMatrix() {
  const tbody = document.getElementById('tools-matrix-body');
  if (!tbody || tbody.children.length > 0) return;

  try {
    const res = await fetch('/api/observability-tools-matrix');
    const tools = await res.json();

    tbody.innerHTML = tools.map(t => `
      <tr>
        <td style="font-weight: 700; color: var(--accent-gold);">${t.name}</td>
        <td>${t.type}</td>
        <td>${t.key_features}</td>
        <td>${t.best_for}</td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" style="color: var(--accent-red);">Gagal memuat matriks tools: ${err.message}</td></tr>`;
  }
}

// On initial page load
document.addEventListener('DOMContentLoaded', () => {
  loadSampleTrace();
});
