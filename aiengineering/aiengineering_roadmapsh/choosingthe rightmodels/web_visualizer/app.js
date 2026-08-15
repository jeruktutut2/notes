// Interactive Playground & Model Decision Matrix Logic

// Dataset Model Comprehensive
const MODEL_DATABASE = [
  {
    name: "Anthropic Claude 3.5 Sonnet",
    type: "closed",
    capability: ["coding", "long-context"],
    context: "200,000 Tokens",
    inputCost: "$3.00",
    outputCost: "$15.00",
    highlights: "SOTA Coding, Logical Reasoning, Prompt Caching (-90% cost), Computer Use",
    license: "Proprietary API",
    details: "Claude 3.5 Sonnet adalah model nomor #1 untuk pembuatan kode, refactoring, dan analisis arsitektur perangkat lunak. Fitur Prompt Caching menghemat biaya signifikan untuk dokumen sistem yang dikirim berulang."
  },
  {
    name: "Google Gemini 1.5 Pro",
    type: "closed",
    capability: ["multimodal", "long-context"],
    context: "2,000,000 Tokens",
    inputCost: "$1.25",
    outputCost: "$5.00",
    highlights: "Native Multimodal (Text/Video/Audio/PDF), 2 Million Tokens Window",
    license: "Proprietary API / GCP",
    details: "Gemini 1.5 Pro mengusung arsitektur native multimodal dari awal. Mampu mencerna video 1 jam, file audio podcast 3 jam, atau dokumen 1.000 halaman dalam sekali prompt tanpa ekstraktor terpisah."
  },
  {
    name: "OpenAI GPT-4o",
    type: "closed",
    capability: ["coding", "multimodal"],
    context: "128,000 Tokens",
    inputCost: "$2.50",
    outputCost: "$10.00",
    highlights: "Structured Outputs (100% Valid JSON), Tool Calling, Multimodal Audio API",
    license: "Proprietary API",
    details: "GPT-4o adalah workhorse utama dengan dukungan Structured Outputs (JSON Schema Pydantic) terjamin valid. Memiliki ekosistem integrasi terlengkap di industri."
  },
  {
    name: "OpenAI o1 / o3-mini",
    type: "closed",
    capability: ["reasoning"],
    context: "128,000 Tokens",
    inputCost: "$1.10 - $15.00",
    outputCost: "$4.40 - $60.00",
    highlights: "Inference Time Chain-of-Thought Search, Competition Math & Science",
    license: "Proprietary API",
    details: "Model reasoning o-series menggunakan alokasi token CoT internal untuk mengeksekusi langkah-langkah logika kompleks sebelum memberikan respons akhir."
  },
  {
    name: "Cohere Command R+",
    type: "closed",
    capability: ["long-context"],
    context: "128,000 Tokens",
    inputCost: "$3.00",
    outputCost: "$15.00",
    highlights: "Enterprise RAG Specialist, Anti-Halusinasi Grounded Citations",
    license: "Enterprise API",
    details: "Dirancang khusus untuk Knowledge Search perusahaan dengan fitur kutipan otomatis (citations) dari dokumen sumber."
  },
  {
    name: "Mistral Large 2",
    type: "closed",
    capability: ["coding"],
    context: "128,000 Tokens",
    inputCost: "$2.00",
    outputCost: "$6.00",
    highlights: "EU Data Sovereignty, High-efficiency Multilingual Reasoning",
    license: "Proprietary / Self-Host",
    details: "Model enterprise Eropa berkinerja tinggi yang mematuhi standar privasi GDPR ketat."
  },
  {
    name: "Meta Llama 3.1 (8B / 70B / 405B)",
    type: "open",
    capability: ["coding", "long-context"],
    context: "128,000 Tokens",
    inputCost: "Self-Hosted ($0)",
    outputCost: "Self-Hosted ($0)",
    highlights: "Open Weights Industry Standard, 1B - 405B Params, 128K Context",
    license: "Llama 3 Community",
    details: "Standar emas open weights. Llama 3.1 70B dapat di-host di server internal untuk kerahasiaan data 100%."
  },
  {
    name: "DeepSeek V3 & R1",
    type: "open",
    capability: ["reasoning", "coding"],
    context: "128,000 Tokens",
    inputCost: "Self-Host / $0.55",
    outputCost: "Self-Host / $2.19",
    highlights: "Mixture-of-Experts (671B Total / 37B Active), Open Weights Reasoning",
    license: "MIT License",
    details: "Menggunakan arsitektur MoE untuk mengaktifkan hanya 37B parameter per token, menghadirkan kemampuan reasoning o1 dengan efisiensi harga luar biasa."
  },
  {
    name: "Alibaba Qwen 2.5 (inc. Coder & Math)",
    type: "open",
    capability: ["coding", "reasoning"],
    context: "128,000 Tokens",
    inputCost: "Self-Hosted ($0)",
    outputCost: "Self-Hosted ($0)",
    highlights: "Superior Multilingual (Bahasa Indonesia), Qwen-Coder #1 Open Code",
    license: "Apache 2.0 / Qwen",
    details: "Varian Qwen 2.5-Coder sangat responsif untuk auto-completion lokal dan unggul dalam pemahaman instruksi bahasa non-Inggris."
  },
  {
    name: "Google Gemma 2 (2.7B / 9B / 27B)",
    type: "open",
    capability: ["coding"],
    context: "8,192 Tokens",
    inputCost: "Self-Hosted ($0)",
    outputCost: "Self-Hosted ($0)",
    highlights: "Lightweight On-Device Inference, Ultra-High Precision 9B/27B",
    license: "Gemma Terms",
    details: "Model open weight Google yang dirancang efisien untuk dijalankan pada GPU laptop konsumen (RTX 3060/4060) atau edge devices."
  }
];

// --- TAB NAVIGATION ---
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    btn.classList.add('active');
    const tabId = `tab-${btn.dataset.tab}`;
    document.getElementById(tabId).classList.add('active');
  });
});

// --- RENDER COMPARISON TABLE ---
function renderComparisonTable(data) {
  const tbody = document.getElementById('table-body');
  tbody.innerHTML = '';
  
  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 24px; color: var(--text-muted);">Tidak ada model yang cocok dengan filter.</td></tr>`;
    return;
  }
  
  data.forEach(item => {
    const tr = document.createElement('tr');
    const typeBadge = item.type === 'closed' 
      ? `<span class="card-badge gold">Closed</span>`
      : `<span class="card-badge green">Open Source</span>`;
      
    tr.innerHTML = `
      <td><strong>${item.name}</strong></td>
      <td>${typeBadge}</td>
      <td>${item.context}</td>
      <td>${item.inputCost}</td>
      <td>${item.outputCost}</td>
      <td><span class="pill">${item.highlights}</span></td>
      <td><small>${item.license}</small></td>
    `;
    tbody.appendChild(tr);
  });
}

// --- FILTER & SEARCH EVENT LISTENERS ---
function filterModels() {
  const search = document.getElementById('search-model').value.toLowerCase();
  const typeFilter = document.getElementById('filter-type').value;
  const capFilter = document.getElementById('filter-capability').value;
  
  const filtered = MODEL_DATABASE.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(search) || item.highlights.toLowerCase().includes(search);
    const matchesType = typeFilter === 'all' || item.type === typeFilter;
    const matchesCap = capFilter === 'all' || item.capability.includes(capFilter);
    return matchesSearch && matchesType && matchesCap;
  });
  
  renderComparisonTable(filtered);
}

document.getElementById('search-model').addEventListener('input', filterModels);
document.getElementById('filter-type').addEventListener('change', filterModels);
document.getElementById('filter-capability').addEventListener('change', filterModels);

// --- ROADMAP CLICK HIGHLIGHT ---
function highlightModel(key) {
  const panel = document.getElementById('model-detail-panel');
  const title = document.getElementById('detail-title');
  const desc = document.getElementById('detail-description');
  const tags = document.getElementById('detail-tags');
  
  const match = MODEL_DATABASE.find(m => m.name.toLowerCase().includes(key));
  if (match) {
    title.innerText = `💡 ${match.name}`;
    desc.innerText = match.details;
    tags.innerHTML = `
      <span class="pill">Context: ${match.context}</span>
      <span class="pill">Input Cost: ${match.inputCost}</span>
      <span class="pill">Output Cost: ${match.outputCost}</span>
      <span class="pill">License: ${match.license}</span>
    `;
  }
}

// --- VRAM CALCULATOR LOGIC ---
function updateVramCalculator() {
  const params = parseFloat(document.getElementById('calc-params').value) || 8.0;
  const bits = parseInt(document.getElementById('calc-bits').value) || 4;
  
  const bytesPerParam = bits / 8.0;
  const weightsGb = (params * 1e9 * bytesPerParam) / (1024 * 1024 * 1024);
  const totalVram = weightsGb * 1.20; // 20% Overhead
  
  document.getElementById('res-weights').innerText = `${weightsGb.toFixed(2)} GB`;
  document.getElementById('res-vram').innerText = `${totalVram.toFixed(2)} GB`;
  
  let hw = "";
  if (totalVram <= 8) hw = "MacBook M1/M2/M3 (8GB RAM) / RTX 3060 (12GB)";
  else if (totalVram <= 24) hw = "1x RTX 4090 (24GB VRAM) / Mac Studio (32GB)";
  else if (totalVram <= 80) hw = "1x NVIDIA A100 (80GB VRAM) / 2x RTX 4090";
  else hw = "Cluster 8x NVIDIA H100 (8x80GB VRAM)";
  
  document.getElementById('res-hardware').innerText = hw;
}

document.getElementById('calc-params').addEventListener('input', updateVramCalculator);
document.getElementById('calc-bits').addEventListener('change', updateVramCalculator);

// --- API COST ESTIMATOR LOGIC ---
const COST_RATES = {
  "gpt-4o": { in: 2.50, out: 10.00 },
  "gpt-4o-mini": { in: 0.15, out: 0.60 },
  "claude-3-5-sonnet": { in: 3.00, out: 15.00 },
  "claude-3-5-haiku": { in: 1.00, out: 5.00 },
  "gemini-1-5-pro": { in: 1.25, out: 5.00 },
  "gemini-1-5-flash": { in: 0.075, out: 0.30 },
  "deepseek-r1": { in: 0.55, out: 2.19 }
};

function updateCostEstimator() {
  const modelKey = document.getElementById('cost-model-select').value;
  const inTokensM = parseFloat(document.getElementById('input-tokens-m').value) || 0;
  const outTokensM = parseFloat(document.getElementById('output-tokens-m').value) || 0;
  
  const rates = COST_RATES[modelKey] || { in: 2.50, out: 10.00 };
  const totalCost = (inTokensM * rates.in) + (outTokensM * rates.out);
  
  document.getElementById('res-total-cost').innerText = `$${totalCost.toFixed(2)} USD`;
  
  const statusElem = document.getElementById('cost-status');
  if (totalCost < 50) {
    statusElem.innerText = "Ekonomis & Terjangkau";
    statusElem.style.background = "rgba(16, 185, 129, 0.2)";
    statusElem.style.color = "#10b981";
  } else if (totalCost < 300) {
    statusElem.innerText = "Skala Moderat Enterprise";
    statusElem.style.background = "rgba(251, 191, 36, 0.2)";
    statusElem.style.color = "#fbbf24";
  } else {
    statusElem.innerText = "High Volume Consumption";
    statusElem.style.background = "rgba(239, 68, 68, 0.2)";
    statusElem.style.color = "#ef4444";
  }
}

document.getElementById('cost-model-select').addEventListener('change', updateCostEstimator);
document.getElementById('input-tokens-m').addEventListener('input', updateCostEstimator);
document.getElementById('output-tokens-m').addEventListener('input', updateCostEstimator);

// --- DECISION TREE WIZARD LOGIC ---
let wizardState = { privacy: null, priority: null };

function wizardAnswer(step, choice) {
  if (step === 1) {
    wizardState.privacy = choice;
    document.getElementById('wizard-q1').classList.add('hidden');
    if (choice === 'cloud') {
      document.getElementById('wizard-q2-cloud').classList.remove('hidden');
    } else {
      document.getElementById('wizard-q2-selfhost').classList.remove('hidden');
    }
  } else if (step === 2) {
    wizardState.priority = choice;
    document.getElementById('wizard-q2-cloud').classList.add('hidden');
    document.getElementById('wizard-q2-selfhost').classList.add('hidden');
    showRecommendation();
  }
}

function showRecommendation() {
  const recCard = document.getElementById('rec-card-content');
  const resContainer = document.getElementById('wizard-recommendation');
  
  let title = "";
  let reason = "";
  let modelName = "";
  
  if (wizardState.privacy === 'cloud') {
    if (wizardState.priority === 'coding') {
      modelName = "Anthropic Claude 3.5 Sonnet";
      reason = "Model #1 terbaik untuk Software Engineering, Architecture, dan Refactoring. Manfaatkan Prompt Caching untuk menghemat biaya hingga 90%.";
    } else if (wizardState.priority === 'multimodal') {
      modelName = "Google Gemini 1.5 Pro";
      reason = "Memiliki 2 Juta Token Context Window dan dukungan native pemrosesan video/audio tanpa ekstraksi terpisah.";
    } else if (wizardState.priority === 'reasoning') {
      modelName = "DeepSeek R1 atau OpenAI o1 / o3-mini";
      reason = "Menggunakan Chain-of-Thought reasoning untuk memecahkan masalah matematika, sains, dan algoritma rumit.";
    } else {
      modelName = "Google Gemini 1.5 Flash / OpenAI GPT-4o-mini";
      reason = "Model super cepat dengan latensi ultra rendah dan harga sangat terjangkau ($0.075 / 1M token).";
    }
  } else {
    if (wizardState.priority === 'edge') {
      modelName = "Meta Llama 3.2 (3B) / Google Gemma 2 (2.7B)";
      reason = "Sangat ringan, mampu berjalan lancar pada perangkat mobile, laptop standard, atau edge devices dengan RAM < 8GB.";
    } else if (wizardState.priority === 'server') {
      modelName = "Meta Llama 3.1 70B atau DeepSeek R1 (671B MoE)";
      reason = "Performa sekelas closed-model frontier yang dapat di-host sepenuhnya di server GPU internal tanpa kebocoran data.";
    } else {
      modelName = "Alibaba Qwen 2.5-Coder 32B";
      reason = "Spesialis code completion open-source terbaik yang mendukung Bahasa Indonesia dan puluhan bahasa pemrograman.";
    }
  }
  
  recCard.innerHTML = `
    <h4 style="font-size: 1.3rem; color: var(--accent-gold); margin-bottom: 8px;">👑 ${modelName}</h4>
    <p style="color: var(--text-muted); font-size: 0.95rem;">${reason}</p>
  `;
  
  resContainer.classList.remove('hidden');
}

function resetWizard() {
  wizardState = { privacy: null, priority: null };
  document.getElementById('wizard-q1').classList.remove('hidden');
  document.getElementById('wizard-q2-cloud').classList.add('hidden');
  document.getElementById('wizard-q2-selfhost').classList.add('hidden');
  document.getElementById('wizard-recommendation').classList.add('hidden');
}

// Initializations
renderComparisonTable(MODEL_DATABASE);
updateVramCalculator();
updateCostEstimator();
