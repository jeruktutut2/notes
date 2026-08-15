// AI Agents Interactive Learning Visualizer JS

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initTopicDetails();
  initReActSimulator();
  initTopologyVisualizer();
  initToolsInspector();
});

// 1. Tab Switching
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const pane = document.getElementById(`tab-${targetTab}`);
      if (pane) pane.classList.add('active');
    });
  });
}

// 2. Topic Details for Roadmap Tab
const TOPIC_DATA = {
  usecases: {
    title: "01. Agents Usecases",
    tag: "Aplikasi Industri",
    body: `
      <p>AI Agent digunakan untuk mengotomatiskan tugas-tugas kompleks berurutan yang membutuhkan perencanaan dan eksekusi alat:</p>
      <ul>
        <li><strong>Customer Support:</strong> Resolusi tiket otonom, eksekusi refund, dan sinkronisasi CRM.</li>
        <li><strong>Code Assistants:</strong> Membaca repositori, menganalisis bug, menulis kode multi-file, dan memverifikasi unit test.</li>
        <li><strong>Autonomous Research:</strong> Web scraping, ekstraksi artikel PDF, dan visualisasi data CSV secara otomatis.</li>
        <li><strong>Workflow Automation:</strong> Mengabaikan batas API antar SaaS (Slack, Gmail, HubSpot, Jira).</li>
      </ul>
    `
  },
  react: {
    title: "02. ReAct Prompting Framework",
    tag: "Reasoning Loop",
    body: `
      <p><strong>ReAct (Reasoning and Acting)</strong> menggabungkan logika berpikir dan eksekusi alat secara bergantian:</p>
      <ol>
        <li><strong>Thought:</strong> LLM mengevaluasi situasi dan merencanakan aksi berikutnya.</li>
        <li><strong>Action:</strong> LLM menentukan nama tool dan argumen JSON yang akan dipanggil.</li>
        <li><strong>Observation:</strong> Hasil eksekusi tool dikembalikan ke LLM context window.</li>
        <li><strong>Final Answer:</strong> Menyampaikan hasil akhir saat informasi sudah mencukupi.</li>
      </ol>
    `
  },
  tools: {
    title: "03. Tools & Function Calling",
    tag: "Native Architecture",
    body: `
      <p>Native Function Calling memungkinkan LLM menghasilkan struktur JSON valid yang sesuai dengan deskripsi fungsi:</p>
      <ul>
        <li><strong>Schema Registration:</strong> Menggunakan Pydantic / JSON Schema untuk tipe data parameter yang akurat.</li>
        <li><strong>Type Safety & Validation:</strong> Mencegah syntax error dibandingkan string parsing murni.</li>
        <li><strong>Context Injection:</strong> Mengirimkan kembali <code>tool_call_id</code> dan payload hasil fungsi ke LLM.</li>
      </ul>
    `
  },
  multiagent: {
    title: "04. Multi-Agent Systems",
    tag: "Sistem Terdistribusi",
    body: `
      <p>Mengatasi batas context window dan kebingungan instruksi dengan membagi tugas ke beberapa agen spesialis:</p>
      <ul>
        <li><strong>Orchestrator-Workers:</strong> Manager agent memecah tugas dan menugaskan worker.</li>
        <li><strong>Sequential Pipeline:</strong> Output Agen A mengalir langsung menjadi input Agen B.</li>
        <li><strong>Router Agent:</strong> Mengklasifikasikan niat pengguna untuk mengarahkan ke agen spesialis.</li>
      </ul>
    `
  },
  manual: {
    title: "05.1 Building Agents: Manual Implementation",
    tag: "Pure Python",
    body: `<p>Membangun agent dari nol menggunakan pure Python while-loop dan state memory dictionary tanpa framework external.</p>`
  },
  openai: {
    title: "05.2 Building Agents: OpenAI AgentKit / SDK",
    tag: "Swarm Handoff",
    body: `<p>Memanfaatkan Assistant API dan pola Swarm untuk melacak persistent thread dan melakukan handoff antar agent.</p>`
  },
  claude: {
    title: "05.3 Building Agents: Claude Agent SDK",
    tag: "Computer Use & Tool Blocks",
    body: `<p>Menggunakan Anthropic Tool Use API dengan <code>tool_use</code> dan <code>tool_result</code> content blocks serta fitur Computer Use.</p>`
  },
  vertex: {
    title: "05.4 Building Agents: Vertex AI Agent Builder",
    tag: "Enterprise Grounding",
    body: `<p>Platform GCP terkelola untuk Enterprise RAG, Search Grounding, dan integrasi OpenAPI extension.</p>`
  },
  google: {
    title: "05.5 Building Agents: Google ADK",
    tag: "Multimodal Gemini",
    body: `<p>Google Agent Development Kit untuk menangani input multimodal (teks, audio, gambar, video) dan Code Execution Sandbox.</p>`
  }
};

function initTopicDetails() {
  showTopicDetail('usecases');
}

function showTopicDetail(key) {
  const data = TOPIC_DATA[key];
  if (!data) return;

  document.getElementById('detail-title').innerText = data.title;
  document.getElementById('detail-tag').innerText = data.tag;
  document.getElementById('detail-body').innerHTML = data.body;
}

// 3. ReAct Simulator Logic
const REACT_PRESETS = {
  refund: [
    { type: 'thought', text: 'User meminta refund untuk pesanan #ORD-9901. Saya harus mengecek status pesanan di database terlebih dahulu.' },
    { type: 'action', text: 'check_order_status(order_id="ORD-9901")' },
    { type: 'observation', text: 'Order ORD-9901: Item=Keyboard Mekanikal, Status=DELIVERED, RefundEligible=True' },
    { type: 'thought', text: 'Pesanan terbukti dikirim dan memenuhi syarat refund. Saya akan mengeksekusi tool refund.' },
    { type: 'action', text: 'process_refund(order_id="ORD-9901")' },
    { type: 'observation', text: 'SUKSES: Refund sebesar Rp 250.000 telah diproses ke saldo akun.' },
    { type: 'final', text: 'Permintaan refund Anda untuk pesanan #ORD-9901 sebesar Rp 250.000 telah diproses.' }
  ],
  math: [
    { type: 'thought', text: 'Saya perlu menghitung luas lingkaran r=7 cm.' },
    { type: 'action', text: 'calculate_math(expr="3.14159 * 7 * 7")' },
    { type: 'observation', text: '153.938' },
    { type: 'thought', text: 'Hasil luas lingkaran adalah 153.94 cm^2. Sekarang kalikan dengan 3.' },
    { type: 'action', text: 'calculate_math(expr="153.938 * 3")' },
    { type: 'observation', text: '461.814' },
    { type: 'final', text: 'Hasil akhir luas lingkaran r=7 cm dikali 3 adalah 461.81 cm².' }
  ],
  devops: [
    { type: 'thought', text: 'Saya harus mengecek ketersediaan disk space dan cpu server.' },
    { type: 'action', text: 'execute_bash(command="df -h && top -n 1")' },
    { type: 'observation', text: 'Disk Avail: 38GB (24% used). CPU Load: 1.2% idle: 98.8%' },
    { type: 'final', text: 'Status server sangat sehat: Disk terpakai 24% dan CPU load hanya 1.2%.' }
  ]
};

let currentTraceSteps = [];
let currentStepIndex = 0;

function initReActSimulator() {
  const presetSelect = document.getElementById('query-preset');
  const customQuery = document.getElementById('custom-query');
  const runBtn = document.getElementById('btn-run-react');
  const nextBtn = document.getElementById('btn-next-step');
  const resetBtn = document.getElementById('btn-reset-react');

  presetSelect.addEventListener('change', () => {
    const val = presetSelect.value;
    if (val === 'refund') customQuery.value = "Saya mau refund pesanan ORD-9901";
    else if (val === 'math') customQuery.value = "Berapa luas lingkaran r=7 jika dikali 3?";
    else if (val === 'devops') customQuery.value = "Cek ketersediaan disk dan CPU server";
  });
  presetSelect.dispatchEvent(new Event('change'));

  runBtn.addEventListener('click', () => {
    const key = presetSelect.value;
    currentTraceSteps = REACT_PRESETS[key] || REACT_PRESETS['refund'];
    currentStepIndex = 0;
    document.getElementById('react-trace-list').innerHTML = '';
    nextBtn.disabled = false;
    renderNextTraceStep();
  });

  nextBtn.addEventListener('click', () => {
    renderNextTraceStep();
  });

  resetBtn.addEventListener('click', () => {
    currentStepIndex = 0;
    currentTraceSteps = [];
    document.getElementById('react-trace-list').innerHTML = '<div class="empty-trace-state"><i class="fa-solid fa-terminal"></i> Klik \'Run ReAct Simulation\' untuk memulai trace.</div>';
    nextBtn.disabled = true;
  });
}

function renderNextTraceStep() {
  if (currentStepIndex >= currentTraceSteps.length) {
    document.getElementById('btn-next-step').disabled = true;
    return;
  }

  const step = currentTraceSteps[currentStepIndex];
  const list = document.getElementById('react-trace-list');

  const card = document.createElement('div');
  card.className = `trace-card ${step.type}`;
  card.innerHTML = `
    <div class="trace-card-title">${step.type}</div>
    <div class="trace-card-body">${step.text}</div>
  `;

  list.appendChild(card);
  list.scrollTop = list.scrollHeight;
  currentStepIndex++;
}

// 4. Multi-Agent Topology Visualizer
function initTopologyVisualizer() {
  const topoBtns = document.querySelectorAll('.topo-btn');
  topoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      topoBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderTopology(btn.getAttribute('data-topo'));
    });
  });
  renderTopology('hierarchical');
}

function renderTopology(type) {
  const canvas = document.getElementById('topology-canvas');
  if (type === 'hierarchical') {
    canvas.innerHTML = `
      <div style="display:flex; flex-direction:column; align-items:center; gap:2rem; width:100%;">
        <div style="padding:1rem 2rem; background:rgba(245,158,11,0.2); border:2px solid #f59e0b; border-radius:12px; font-weight:700;">
          👑 Orchestrator Agent (Manager)
        </div>
        <div style="display:flex; gap:2rem; justify-content:center; width:100%;">
          <div style="padding:1rem; background:rgba(6,182,212,0.15); border:1px solid #06b6d4; border-radius:10px;">🤖 Researcher Worker</div>
          <div style="padding:1rem; background:rgba(59,130,246,0.15); border:1px solid #3b82f6; border-radius:10px;">✍️ Writer Worker</div>
          <div style="padding:1rem; background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:10px;">🔍 Reviewer Worker</div>
        </div>
      </div>
    `;
  } else if (type === 'sequential') {
    canvas.innerHTML = `
      <div style="display:flex; align-items:center; gap:1.5rem; justify-content:center; width:100%;">
        <div style="padding:1rem; background:rgba(6,182,212,0.15); border:1px solid #06b6d4; border-radius:10px;">1. Planner Agent</div>
        <i class="fa-solid fa-arrow-right" style="color:var(--text-muted)"></i>
        <div style="padding:1rem; background:rgba(59,130,246,0.15); border:1px solid #3b82f6; border-radius:10px;">2. Coder Agent</div>
        <i class="fa-solid fa-arrow-right" style="color:var(--text-muted)"></i>
        <div style="padding:1rem; background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:10px;">3. QA Tester Agent</div>
      </div>
    `;
  } else {
    canvas.innerHTML = `
      <div style="display:flex; align-items:center; gap:3rem; justify-content:center; width:100%;">
        <div style="padding:1.5rem; background:rgba(139,92,246,0.2); border:2px solid #8b5cf6; border-radius:12px; font-weight:700;">
          🚦 Router / Dispatcher Agent
        </div>
        <div style="display:flex; flex-direction:column; gap:1rem;">
          <div style="padding:0.75rem 1.5rem; background:rgba(239,68,68,0.15); border:1px solid #ef4444; border-radius:8px;">💳 Billing Agent</div>
          <div style="padding:0.75rem 1.5rem; background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:8px;">🛠️ Tech Support Agent</div>
        </div>
      </div>
    `;
  }
}

// 5. Tool Inspector Code Blocks Populator
function initToolsInspector() {
  document.getElementById('schema-code-preview').innerText = JSON.stringify({
    "type": "function",
    "function": {
      "name": "check_order_status",
      "description": "Cek status pengiriman & kelayakan refund pesanan.",
      "parameters": {
        "type": "object",
        "properties": {
          "order_id": { "type": "string", "description": "ID unik pesanan" }
        },
        "required": ["order_id"]
      }
    }
  }, null, 2);

  document.getElementById('request-code-preview').innerText = JSON.stringify({
    "id": "call_9901_abc",
    "type": "function",
    "function": {
      "name": "check_order_status",
      "arguments": "{\"order_id\": \"ORD-9901\"}"
    }
  }, null, 2);

  document.getElementById('result-code-preview').innerText = JSON.stringify({
    "role": "tool",
    "tool_call_id": "call_9901_abc",
    "content": "Order ORD-9901: Item=Keyboard Mekanikal, Status=DELIVERED, RefundEligible=True"
  }, null, 2);
}
