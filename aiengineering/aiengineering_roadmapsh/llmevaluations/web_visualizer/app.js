// app.js - Interactive Engine for LLM Evaluations Visualizer

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initRoadmapNodes();
  initDeterministicEval();
  initLLMJudge();
  initChatbotArena();
  initRAGTriadSliders();
});

// 1. Tab Navigation
function initTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      switchTab(target);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabId || (tabId === 'tab-tools' && btn.dataset.tab === 'tab-tools'));
  });

  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.toggle('active', content.id === tabId);
  });
}

// 2. Roadmap Architecture Node Clicks
function initRoadmapNodes() {
  const nodes = document.querySelectorAll('.node-btn');
  nodes.forEach(node => {
    node.addEventListener('click', () => {
      nodes.forEach(n => n.classList.remove('highlighted'));
      node.classList.add('highlighted');
      
      const target = node.dataset.target;
      if (target === 'tab-deepeval' || target === 'tab-ragas') {
        switchTab('tab-tools');
      } else {
        switchTab(target);
      }
    });
  });
}

// 3. Deterministic Evaluator Engine
function initDeterministicEval() {
  const btn = document.getElementById('btn-run-det');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const candidate = document.getElementById('det-candidate').value;
    const reference = document.getElementById('det-reference').value;

    const em = candidate.strip().toLowerCase() === reference.strip().toLowerCase();
    const levSim = calculateLevenshteinSim(candidate, reference);
    const bleu = calculateSimpleBleu(candidate, reference);
    const rouge1 = calculateSimpleRouge(candidate, reference, 1);
    const rougeL = calculateSimpleRouge(candidate, reference, 'L');

    document.getElementById('res-em').textContent = em ? 'TRUE (Exact Match)' : 'FALSE';
    document.getElementById('res-em').style.color = em ? '#10b981' : '#ef4444';
    
    document.getElementById('res-lev').textContent = `${(levSim * 100).toFixed(1)}%`;
    document.getElementById('res-bleu').textContent = bleu.toFixed(4);
    document.getElementById('res-rouge1').textContent = rouge1.toFixed(4);
    document.getElementById('res-rougel').textContent = rougeL.toFixed(4);
  });
}

// Helper string strip
String.prototype.strip = function() { return this.replace(/^\s+|\s+$/g, ''); };

function calculateLevenshteinSim(s1, s2) {
  const m = s1.length, n = s2.length;
  if (Math.max(m, n) === 0) return 1.0;
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (s1[i - 1] === s2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
      else dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return 1.0 - (dp[m][n] / Math.max(m, n));
}

function calculateSimpleBleu(cand, ref) {
  const cWords = cand.toLowerCase().split(/\s+/);
  const rWords = ref.toLowerCase().split(/\s+/);
  if (cWords.length === 0) return 0;
  let matches = 0;
  cWords.forEach(w => { if (rWords.includes(w)) matches++; });
  const precision = matches / cWords.length;
  const bp = cWords.length >= rWords.length ? 1.0 : Math.exp(1 - rWords.length / cWords.length);
  return precision * bp;
}

function calculateSimpleRouge(cand, ref, type) {
  const cWords = cand.toLowerCase().split(/\s+/);
  const rWords = ref.toLowerCase().split(/\s+/);
  let matches = 0;
  cWords.forEach(w => { if (rWords.includes(w)) matches++; });
  const prec = matches / cWords.length;
  const rec = matches / rWords.length;
  return (prec + rec) > 0 ? (2 * prec * rec) / (prec + rec) : 0;
}

// 4. LLM Judge Simulator
function initLLMJudge() {
  const btn = document.getElementById('btn-run-judge');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const query = document.getElementById('judge-query').value;
    const respA = document.getElementById('judge-resp-a').value;
    const respB = document.getElementById('judge-resp-b').value;
    const posSwap = document.getElementById('chk-position-swap').checked;

    let winner = "Model A";
    let cotText = `[G-Eval CoT Analysis]:\n1. Query Focus: '${query}'\n2. Model A memberikan penjelasan teknis tentang Vector DB & Embedding.\n3. Model B memberikan penjelasan yang terlalu umum dan tidak akurat.`;
    let biasStatus = posSwap ? "Position Bias: Swapped & Neutralized (2 Passes)" : "Position Bias: Single Pass (Unchecked)";

    document.getElementById('judge-winner').textContent = `🏆 Pemenang: ${winner}`;
    document.getElementById('bias-status').textContent = biasStatus;
    document.getElementById('judge-cot-text').textContent = cotText;
  });
}

// 5. Chatbot Arena ELO System
const arenaRatings = {
  "GPT-4o": 1250,
  "Claude-3.5-Sonnet": 1245,
  "Model Alpha (Current)": 1000,
  "Model Beta (Current)": 1000,
  "Llama-3-8B": 980
};

function initChatbotArena() {
  renderEloLeaderboard();

  document.querySelectorAll('.vote-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const vote = btn.dataset.vote;
      let rA = arenaRatings["Model Alpha (Current)"];
      let rB = arenaRatings["Model Beta (Current)"];

      const k = 32;
      const eA = 1 / (1 + Math.pow(10, (rB - rA) / 400));
      const eB = 1 / (1 + Math.pow(10, (rA - rB) / 400));

      let sA = 0.5, sB = 0.5;
      if (vote === 'alpha') { sA = 1.0; sB = 0.0; }
      else if (vote === 'beta') { sA = 0.0; sB = 1.0; }

      arenaRatings["Model Alpha (Current)"] = Math.round(rA + k * (sA - eA));
      arenaRatings["Model Beta (Current)"] = Math.round(rB + k * (sB - eB));

      renderEloLeaderboard();
    });
  });
}

function renderEloLeaderboard() {
  const tbody = document.getElementById('elo-leaderboard-body');
  if (!tbody) return;

  const sorted = Object.entries(arenaRatings).sort((a, b) => b[1] - a[1]);
  tbody.innerHTML = sorted.map(([model, elo], idx) => `
    <tr>
      <td>#${idx + 1}</td>
      <td><strong>${model}</strong></td>
      <td>${elo}</td>
    </tr>
  `).join('');
}

// 6. RAG Triad Sliders Engine
function initRAGTriadSliders() {
  const fSlide = document.getElementById('slide-faith');
  const rSlide = document.getElementById('slide-relev');
  const pSlide = document.getElementById('slide-prec');

  if (!fSlide) return;

  const updateTriad = () => {
    const f = parseInt(fSlide.value);
    const r = parseInt(rSlide.value);
    const p = parseInt(pSlide.value);

    document.getElementById('val-faith').textContent = `${f}%`;
    document.getElementById('val-relev').textContent = `${r}%`;
    document.getElementById('val-prec').textContent = `${p}%`;

    const avg = Math.round((f + r + p) / 3);
    document.getElementById('triad-overall-num').textContent = avg;

    const label = document.getElementById('triad-status-text');
    if (avg >= 85) {
      label.textContent = "EXCELLENT RAG PIPELINE";
      label.style.color = "#10b981";
    } else if (avg >= 70) {
      label.textContent = "ACCEPTABLE / MINOR DRIFT";
      label.style.color = "#f59e0b";
    } else {
      label.textContent = "CRITICAL RAG FAILURE";
      label.style.color = "#ef4444";
    }
  };

  [fSlide, rSlide, pSlide].forEach(s => s.addEventListener('input', updateTriad));
  updateTriad();
}
