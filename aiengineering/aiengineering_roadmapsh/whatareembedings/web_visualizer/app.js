// Interactive Logic for Web Visualizer Dashboard

// Tab Navigation
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    btn.classList.add('active');
    const tabId = btn.getAttribute('data-tab');
    document.getElementById(tabId).classList.add('active');
  });
});

// Helper Vector Functions
function parseVector(str) {
  return str.split(',').map(v => parseFloat(v.trim()) || 0);
}

function l2Normalize(vec) {
  const norm = Math.sqrt(vec.reduce((sum, val) => sum + val * val, 0));
  if (norm === 0) return vec;
  return vec.map(val => val / norm);
}

function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

function euclideanDistance(a, b) {
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    sum += (a[i] - b[i]) ** 2;
  }
  return Math.sqrt(sum);
}

function manhattanDistance(a, b) {
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    sum += Math.abs(a[i] - b[i]);
  }
  return sum;
}

// 1. Vector Math Calculator
function calculateVectorMetrics() {
  const vA = l2Normalize(parseVector(document.getElementById('vecA-input').value));
  const vB = l2Normalize(parseVector(document.getElementById('vecB-input').value));

  const cos = cosineSimilarity(vA, vB);
  const dot = vA.reduce((sum, val, idx) => sum + val * vB[idx], 0);
  const euc = euclideanDistance(vA, vB);
  const man = manhattanDistance(vA, vB);

  document.getElementById('res-cosine').innerText = cos.toFixed(4);
  document.getElementById('res-dot').innerText = dot.toFixed(4);
  document.getElementById('res-euclidean').innerText = euc.toFixed(4);
  document.getElementById('res-manhattan').innerText = man.toFixed(4);
}

document.getElementById('btn-calc-vector').addEventListener('click', calculateVectorMetrics);
calculateVectorMetrics();

// 2. Semantic Search Simulator
const SAMPLE_DOCS = [
  { id: 1, title: "Gawai & Smartphone", text: "Ponsel cerdas dengan kamera super jernih dan baterai awet.", cat: "tech" },
  { id: 2, title: "Resep Kuliner", text: "Cara membuat nasi goreng spesial pedas manis yang lezat.", cat: "food" },
  { id: 3, title: "Layanan Perbankan", text: "Kartu kredit terblokir saat transaksi luar negeri.", cat: "finance" },
  { id: 4, title: "Otomotif & Mobil", text: "Mobil listrik terbaru daya tempuh 500km sekali charge.", cat: "auto" }
];

function runSearchSimulator() {
  const q = document.getElementById('search-query-input').value.toLowerCase();
  
  // Keyword Search
  const kwContainer = document.getElementById('kw-results');
  kwContainer.innerHTML = '';
  SAMPLE_DOCS.forEach(doc => {
    const score = q.split(' ').filter(w => w.length > 2 && doc.text.toLowerCase().includes(w)).length;
    const item = document.createElement('div');
    item.className = 'result-item';
    item.innerHTML = `
      <div><strong>${doc.title}</strong><br><small style="color:var(--text-muted)">${doc.text}</small></div>
      <span class="score-badge" style="color:${score > 0 ? 'var(--accent-green)' : 'var(--accent-red)'}">Match: ${score}</span>
    `;
    kwContainer.appendChild(item);
  });

  // Vector Search Simulation
  const semContainer = document.getElementById('sem-results');
  semContainer.innerHTML = '';
  SAMPLE_DOCS.forEach(doc => {
    let sim = 0.15;
    if ((q.includes('hp') || q.includes('kamera') || q.includes('ponsel')) && doc.cat === 'tech') sim = 0.92;
    if ((q.includes('makan') || q.includes('resep') || q.includes('goreng')) && doc.cat === 'food') sim = 0.89;
    if ((q.includes('bank') || q.includes('kartu') || q.includes('transaksi')) && doc.cat === 'finance') sim = 0.94;
    if ((q.includes('mobil') || q.includes('otomotif') || q.includes('listrik')) && doc.cat === 'auto') sim = 0.91;

    const item = document.createElement('div');
    item.className = 'result-item';
    item.innerHTML = `
      <div><strong>${doc.title}</strong><br><small style="color:var(--text-muted)">${doc.text}</small></div>
      <span class="score-badge">Sim: ${sim.toFixed(4)}</span>
    `;
    semContainer.appendChild(item);
  });
}

document.getElementById('btn-run-search').addEventListener('click', runSearchSimulator);
runSearchSimulator();

// 3. Classification Playground
function runClassification() {
  const text = document.getElementById('classify-text-input').value.toLowerCase();
  const resContainer = document.getElementById('classify-results');
  resContainer.innerHTML = '';

  const intents = [
    { name: "BILLING & REFUND", score: text.includes('saldo') || text.includes('potong') || text.includes('uang') ? 0.94 : 0.12 },
    { name: "TECH SUPPORT", score: text.includes('error') || text.includes('crash') || text.includes('aplikasi') ? 0.88 : 0.08 },
    { name: "SHIPPING & TRACKING", score: text.includes('paket') || text.includes('resi') || text.includes('kurir') ? 0.90 : 0.05 }
  ];

  intents.sort((a, b) => b.score - a.score);
  intents.forEach(int => {
    const item = document.createElement('div');
    item.className = 'result-item';
    item.innerHTML = `
      <div><strong>${int.name}</strong></div>
      <span class="score-badge">Confidence: ${(int.score * 100).toFixed(1)}%</span>
    `;
    resContainer.appendChild(item);
  });
}

document.getElementById('btn-run-classify').addEventListener('click', runClassification);
runClassification();

// 4. Recommendation Engine
const PRODUCTS_WEB = [
  { id: 101, name: "Laptop Gaming ASUS ROG RTX 4080", cat: "gaming" },
  { id: 102, name: "Mouse Gaming Wireless Razer", cat: "gaming" },
  { id: 103, name: "Buku Panduan Data Science Python", cat: "books" },
  { id: 104, name: "Buku Pemrograman AI & LLM Engineering", cat: "books" },
  { id: 105, name: "Monitor Gaming Curved 240Hz 4K", cat: "gaming" }
];

function updateRecommendations() {
  const selectedId = parseInt(document.getElementById('select-product').value);
  const target = PRODUCTS_WEB.find(p => p.id === selectedId);
  const recContainer = document.getElementById('rec-results');
  recContainer.innerHTML = '';

  PRODUCTS_WEB.filter(p => p.id !== selectedId).forEach(p => {
    const sim = (p.cat === target.cat) ? (0.85 + Math.random() * 0.1) : (0.15 + Math.random() * 0.1);
    const item = document.createElement('div');
    item.className = 'result-item';
    item.innerHTML = `
      <div><strong>${p.name}</strong></div>
      <span class="score-badge">Match: ${sim.toFixed(4)}</span>
    `;
    recContainer.appendChild(item);
  });
}

document.getElementById('select-product').addEventListener('change', updateRecommendations);
updateRecommendations();

// 5. Anomaly Detection
function checkAnomaly() {
  const text = document.getElementById('anomaly-text-input').value.toLowerCase();
  const box = document.getElementById('anomaly-status-box');

  if (text.includes('abaikan') || text.includes('bypass') || text.includes('password') || text.includes('admin')) {
    box.style.background = 'rgba(248, 113, 113, 0.2)';
    box.style.border = '1px solid var(--accent-red)';
    box.style.color = 'var(--accent-red)';
    box.innerText = '🚨 PROMPT INJECTION / MALICIOUS ATTACK DETECTED! [BLOCKED]';
  } else if (text.includes('resep') || text.includes('makan') || text.includes('kucing')) {
    box.style.background = 'rgba(250, 204, 21, 0.2)';
    box.style.border = '1px solid var(--accent-yellow)';
    box.style.color = 'var(--accent-yellow)';
    box.innerText = '⚠️ OUT OF DISTRIBUTION (OOD) QUERY [OUT OF DOMAIN]';
  } else {
    box.style.background = 'rgba(74, 222, 128, 0.2)';
    box.style.border = '1px solid var(--accent-green)';
    box.style.color = 'var(--accent-green)';
    box.innerText = '✅ NORMAL IN-DOMAIN QUERY [PASSED TO LLM]';
  }
}

document.getElementById('btn-run-anomaly').addEventListener('click', checkAnomaly);
checkAnomaly();
