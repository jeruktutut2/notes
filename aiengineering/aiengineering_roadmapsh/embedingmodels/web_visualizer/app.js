/**
 * app.js - Embedding Models Playground Logic
 * Handles interactive tabs, model architecture inspection, vector simulator math,
 * filterable comparison table, and RAM/Cost estimator.
 */

// Model Database Metadata
const MODEL_DB = {
    'openai': {
        name: 'Open AI Embeddings API',
        category: 'Proprietary',
        provider: 'OpenAI SaaS API',
        dimensions: '1,536 (text-embedding-3-small) / 3,072 (text-embedding-3-large)',
        context: '8,191 Tokens',
        mteb: '62.3 - 64.6',
        cost: '$0.02 per 1M Tokens (small)',
        description: 'Generasi v3 OpenAI membawa fitur Matryoshka Representation Learning. Pengembang dapat memotong dimensi vektor dari 1536 ke 512 atau 256 tanpa kehilangan kualitas pencarian signifikan.',
        code: `from openai import OpenAI\nclient = OpenAI()\nres = client.embeddings.create(\n    model="text-embedding-3-small",\n    input="AI Engineering Roadmap",\n    dimensions=512 # Matryoshka Truncation\n)\nvector = res.data[0].embedding`
    },
    'gemini': {
        name: 'Gemini Embedding',
        category: 'Proprietary',
        provider: 'Google GenAI Cloud',
        dimensions: '768 (text-embedding-004)',
        context: '2,048 Tokens',
        mteb: '63.8',
        cost: '$0.025 per 1M Tokens',
        description: 'Google Gemini menyediakan Task-Aware Embeddings. Vektor dioptimalkan berdasarkan parameter task_type (misal: RETRIEVAL_DOCUMENT vs RETRIEVAL_QUERY atau CLASSIFICATION).',
        code: `from google import genai\nfrom google.genai import types\nclient = genai.Client()\nres = client.models.embed_content(\n    model="text-embedding-004",\n    contents="Dokumen RAG",\n    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")\n)`
    },
    'cohere': {
        name: 'Cohere Embed',
        category: 'Proprietary',
        provider: 'Cohere Enterprise API',
        dimensions: '1,024 (embed-multilingual-v3.0)',
        context: '512 Tokens',
        mteb: '64.1',
        cost: '$0.10 per 1M Tokens',
        description: 'Model khusus enterprise yang mendukung 100+ bahasa. Memelopori kompresi native int8 & binary embeddings untuk menghemat hingga 96% kebutuhan RAM Vector Database.',
        code: `import cohere\nco = cohere.ClientV2()\nres = co.embed(\n    texts=["Enterprise Multilingual Search"],\n    model="embed-multilingual-v3.0",\n    input_type="search_document",\n    embedding_types=["float", "int8"]\n)`
    },
    'sentence-transformers': {
        name: 'Sentence Transformers',
        category: 'Open Source',
        provider: 'UKPLab / Local PyTorch',
        dimensions: '384 (all-MiniLM-L6-v2)',
        context: '256 Tokens',
        mteb: '56.3',
        cost: '$0.00 (Self-Host Local)',
        description: 'Framework open-source paling populer untuk eksekusi lokal. Model MiniLM-L6-v2 sangat cepat di CPU dengan ukuran binary hanya ~90MB.',
        code: `from sentence_transformers import SentenceTransformer, util\nmodel = SentenceTransformer('all-MiniLM-L6-v2')\nembeddings = model.encode(["Kalimat A", "Kalimat B"])\nsim = util.cos_sim(embeddings[0], embeddings[1])`
    },
    'huggingface': {
        name: 'Models on Hugging Face',
        category: 'Open Source',
        provider: 'Hugging Face Hub (BAAI, Nomic, dll)',
        dimensions: '384 (bge-small-en-v1.5) / 768 / 1024',
        context: '512 - 8,192 Tokens',
        mteb: '62.1 - 65.2 (Top Tier)',
        cost: '$0.00 (Self-Host Local)',
        description: 'Ribuan model SOTA dapat diakses langsung menggunakan library transformers. Teknik Mean Pooling digunakan untuk mengubah hidden states menjadi single dense vector.',
        code: `from transformers import AutoTokenizer, AutoModel\ntokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')\nmodel = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')\ninputs = tokenizer("Teks RAG", return_tensors='pt')\noutputs = model(**inputs)`
    },
    'jina': {
        name: 'Jina AI Embeddings',
        category: 'Open Source',
        provider: 'Jina AI Open Source & API',
        dimensions: '768 (jina-embeddings-v2-base-en)',
        context: '8,192 Tokens (Long Context)',
        mteb: '60.4',
        cost: '$0.00 (Self-Host)',
        description: 'Mendukung context window hingga 8,192 token (setara ~15 halaman PDF). MemperkenalkanLate Chunking untuk mencegah hilangnya konteks global antar paragraf.',
        code: `from transformers import AutoModel\nmodel = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)\nembeddings = model.encode(["Dokumen PDF Panjang... 8k tokens"])`
    }
};

// Full Matrix Data for Table
const TABLE_DATA = [
    { name: 'OpenAI text-embedding-3-small', category: 'Proprietary', provider: 'OpenAI', dim: 1536, context: 8191, mteb: 62.3, cost: '$0.02', deploy: 'Cloud API' },
    { name: 'OpenAI text-embedding-3-large', category: 'Proprietary', provider: 'OpenAI', dim: 3072, context: 8191, mteb: 64.6, cost: '$0.13', deploy: 'Cloud API' },
    { name: 'Google Gemini text-embedding-004', category: 'Proprietary', provider: 'Google', dim: 768, context: 2048, mteb: 63.8, cost: '$0.025', deploy: 'Cloud API' },
    { name: 'Cohere embed-multilingual-v3.0', category: 'Proprietary', provider: 'Cohere', dim: 1024, context: 512, mteb: 64.1, cost: '$0.10', deploy: 'Cloud API / VPC' },
    { name: 'Sentence-Transformers all-MiniLM-L6-v2', category: 'Open Source', provider: 'UKPLab', dim: 384, context: 256, mteb: 56.3, cost: '$0.00', deploy: 'Local CPU' },
    { name: 'BAAI bge-small-en-v1.5', category: 'Open Source', provider: 'Hugging Face', dim: 384, context: 512, mteb: 62.1, cost: '$0.00', deploy: 'Local / GPU' },
    { name: 'Jina AI jina-embeddings-v2-base-en', category: 'Open Source', provider: 'Jina AI', dim: 768, context: 8192, mteb: 60.4, cost: '$0.00', deploy: 'Local Docker' }
];

// Initialize UI
document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    populateTable(TABLE_DATA);
    calculateSimilarity();
    calculateEstimates();
    selectModel('openai');
    
    // Matryoshka Slider Listener
    const range = document.getElementById('matryoshka-range');
    range.addEventListener('input', (e) => {
        document.getElementById('dim-val-display').innerText = e.target.value;
    });
});

// Tab Switcher
function setupTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            tab.classList.add('active');
            const target = tab.getAttribute('data-tab');
            document.getElementById(`tab-${target}`).classList.add('active');
        });
    });
}

// Select & Inspect Model
function selectModel(key) {
    const data = MODEL_DB[key];
    if (!data) return;
    
    document.getElementById('detail-title').innerText = data.name;
    document.getElementById('detail-category').innerText = data.category;
    document.getElementById('spec-provider').innerText = data.provider;
    document.getElementById('spec-dim').innerText = data.dimensions;
    document.getElementById('spec-context').innerText = data.context;
    document.getElementById('spec-mteb').innerText = data.mteb;
    document.getElementById('spec-cost').innerText = data.cost;
    document.getElementById('spec-description').innerText = data.description;
    document.getElementById('spec-code').innerText = data.code;

    // Scroll to detail panel smoothly
    document.getElementById('model-detail-panel').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function closeDetailPanel() {
    // Keep visible or reset title
    document.getElementById('detail-title').innerText = 'Pilih Model di Diagram';
}

// Vector Math & Similarity Calculator
function generatePseudoVector(text, dim) {
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
        hash = (hash << 5) - hash + text.charCodeAt(i);
        hash |= 0;
    }
    
    let vec = [];
    let normSq = 0;
    for (let i = 0; i < dim; i++) {
        const val = Math.sin(hash + i * 0.1);
        vec.push(val);
        normSq += val * val;
    }
    const norm = Math.sqrt(normSq);
    return vec.map(v => v / norm); // L2 Normalized
}

function calculateSimilarity() {
    const textA = document.getElementById('text-1').value;
    const textB = document.getElementById('text-2').value;
    const dim = parseInt(document.getElementById('matryoshka-range').value);

    const vecA = generatePseudoVector(textA, dim);
    const vecB = generatePseudoVector(textB, dim);

    // Cosine Sim & Dot Product (identical for L2 normalized vectors)
    let dot = 0;
    let euclidSq = 0;
    for (let i = 0; i < dim; i++) {
        dot += vecA[i] * vecB[i];
        const diff = vecA[i] - vecB[i];
        euclidSq += diff * diff;
    }
    
    // Scale slightly for UI demo realism based on word overlap
    const wordsA = new Set(textA.toLowerCase().split(/\s+/));
    const wordsB = new Set(textB.toLowerCase().split(/\s+/));
    const intersection = [...wordsA].filter(x => wordsB.has(x));
    const overlapRatio = (intersection.length * 2) / (wordsA.size + wordsB.size || 1);
    
    const finalSim = Math.min(0.98, Math.max(0.25, 0.45 + overlapRatio * 0.5));
    const finalEuclidean = Math.sqrt(2 * (1 - finalSim));

    document.getElementById('res-cosine').innerText = finalSim.toFixed(4);
    document.getElementById('res-dot').innerText = finalSim.toFixed(4);
    document.getElementById('res-euclidean').innerText = finalEuclidean.toFixed(4);

    // Heatmap Render
    renderHeatmap('heatmap-a', vecA.slice(0, 30));
    renderHeatmap('heatmap-b', vecB.slice(0, 30));

    // Vector Array Preview
    const previewStr = '[' + vecA.slice(0, 8).map(n => n.toFixed(4)).join(', ') + ', ...]';
    document.getElementById('vector-array-preview').innerText = previewStr;
}

function renderHeatmap(containerId, slice) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    slice.forEach(val => {
        const cell = document.createElement('div');
        cell.className = 'heatmap-cell';
        // Normalize val to hue color
        const normVal = (val + 1) / 2; // 0 to 1
        const hue = Math.floor(normVal * 200 + 100); // Blue to Green/Yellow
        cell.style.backgroundColor = `hsl(${hue}, 80%, 45%)`;
        cell.title = `Val: ${val.toFixed(4)}`;
        container.appendChild(cell);
    });
}

// Table Filter & Render
function populateTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';
    data.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${item.name}</strong></td>
            <td><span class="badge ${item.category === 'Proprietary' ? 'badge-success' : 'badge-outline'}">${item.category}</span></td>
            <td>${item.provider}</td>
            <td><code>${item.dim}</code></td>
            <td>${item.context.toLocaleString()} tokens</td>
            <td><strong style="color:var(--accent-emerald)">${item.mteb}</strong></td>
            <td>${item.cost}</td>
            <td><code>${item.deploy}</code></td>
        `;
        tbody.appendChild(tr);
    });
}

function filterTable() {
    const query = document.getElementById('matrix-search').value.toLowerCase();
    const filtered = TABLE_DATA.filter(d => 
        d.name.toLowerCase().includes(query) || 
        d.provider.toLowerCase().includes(query)
    );
    populateTable(filtered);
}

function filterCategory(cat) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');

    if (cat === 'all') {
        populateTable(TABLE_DATA);
    } else {
        const filtered = TABLE_DATA.filter(d => d.category === cat);
        populateTable(filtered);
    }
}

// Estimator Calculations
function calculateEstimates() {
    const docs = parseFloat(document.getElementById('doc-count').value) || 0;
    const dim = parseInt(document.getElementById('dim-count').value) || 768;
    const monthlyTokens = parseFloat(document.getElementById('token-monthly').value) || 0;

    // RAM Calculations (bytes)
    // Float32 = 4 bytes per dim
    const bytesFloat32 = docs * dim * 4;
    const bytesInt8 = docs * dim * 1;
    const bytesBinary = docs * (dim / 8);

    document.getElementById('ram-float32').innerText = formatBytes(bytesFloat32);
    document.getElementById('ram-int8').innerText = `${formatBytes(bytesInt8)} (Hemat 75%)`;
    document.getElementById('ram-binary').innerText = `${formatBytes(bytesBinary)} (Hemat 96%)`;

    // API Cost Predictions
    const costOpenAI = monthlyTokens * 0.02;
    const costGemini = monthlyTokens * 0.025;
    const costCohere = monthlyTokens * 0.10;

    document.getElementById('cost-openai').innerText = `$${costOpenAI.toFixed(2)} / bulan`;
    document.getElementById('cost-gemini').innerText = `$${costGemini.toFixed(2)} / bulan`;
    document.getElementById('cost-cohere').innerText = `$${costCohere.toFixed(2)} / bulan`;
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
