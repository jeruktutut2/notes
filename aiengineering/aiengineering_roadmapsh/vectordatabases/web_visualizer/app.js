// Vector Databases Explorer & 2D Vector Playground Logic

const VECTOR_DBS_DATA = {
    pinecone: {
        name: "Pinecone ⭐ (Featured Highlight)",
        type: "Cloud SaaS (Serverless / Managed Pods)",
        description: "Vector Database cloud-native terpopuler yang sepenuhnya managed. Pinecone menyediakan arsitektur Serverless dengan auto-scaling, latency sub-10ms, serta isolasi namespace per-tenant.",
        features: [
            "Serverless Indexing dengan skema bayar per-usage",
            "Support Namespaces untuk isolasi multi-tenant",
            "Single-stage hybrid search (Sparse-Dense Vectors)",
            "Metadata filtering ultra cepat tanpa re-indexing"
        ],
        code: `from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="YOUR_API_KEY")

# Create Serverless Index
pc.create_index(
    name="my-rag-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

index = pc.Index("my-rag-index")

# Upsert with Metadata & Namespace
index.upsert(
    vectors=[{"id": "doc1", "values": [0.1, 0.2, ...], "metadata": {"category": "AI"}}],
    namespace="tenant-a"
)`
    },
    chroma: {
        name: "Chroma DB 📦",
        type: "Embedded Open-Source Vector DB",
        description: "Database vektor open-source yang ringan untuk Python dan JavaScript. Chroma berjalan langsung di dalam proses aplikasi lokal tanpa perlu setup server rumit.",
        features: [
            "Zero setup: pip install chromadb",
            "Persistent Storage menggunakan Parquet/DuckDB",
            "Built-in embedding models integration",
            "Sangat ideal untuk local prototyping RAG"
        ],
        code: `import chromadb

client = chromadb.PersistentClient(path="./my_chroma_db")
collection = client.get_or_create_collection(name="kb_notes")

collection.add(
    documents=["RAG architecture with Chroma DB"],
    metadatas=[{"topic": "AI"}],
    ids=["id1"]
)

results = collection.query(
    query_texts=["What is RAG?"],
    n_results=2
)`
    },
    faiss: {
        name: "FAISS ⚡ (Facebook AI Similarity Search)",
        type: "In-Memory Vector Search Library (Meta AI)",
        description: "Library performa tinggi buatan Meta AI untuk pengindeksan dan pencarian vektor langsung di memori CPU/GPU. Menyediakan variasi algoritma paling komprehensif.",
        features: [
            "Performa GPU CUDA paling cepat di industri",
            "Support IVFFlat, HNSWFlat, dan Product Quantization (PQ)",
            "Recall 100% dengan IndexFlatL2",
            "In-memory Caching tanpa persistence bawaan"
        ],
        code: `import faiss
import numpy as np

d = 128 # dimension
index = faiss.IndexHNSWFlat(d, 32)

vectors = np.random.random((10000, d)).astype('float32')
index.add(vectors)

query = np.random.random((1, d)).astype('float32')
D, I = index.search(query, k=5) # Top-5 search`
    },
    qdrant: {
        name: "Qdrant 🦀",
        type: "Self-Hosted / Cloud Vector DB (Rust)",
        description: "Vector database berkecepatan tinggi yang dibangun menggunakan bahasa Rust. Qdrant unggul pada pemfilteran payload metadata tingkat lanjut dan throughput query tinggi.",
        features: [
            "Engine murni bahasa Rust (Memory Safe & Ultra Fast)",
            "Advanced Payload Indexing (Geo, Text, Range)",
            "Support Quantization (Scalar & Product Quantization)"
        ],
        code: `from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")
client.recreate_collection(
    collection_name="test_collection",
    vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE)
)`
    },
    lancedb: {
        name: "LanceDB 🗡️",
        type: "Embedded Multi-modal Vector DB",
        description: "Database vektor serverless berbasis format kolom 'Lance'. LanceDB dirancang khusus untuk menangani data multi-modal (gambar, video, audio, dan teks) dengan RAM footprint minimal.",
        features: [
            "On-disk Columnar Lance Data Format",
            "Zero Memory Copy untuk dataset skala besar",
            "Built-in Multimodal Embedding Pipelines"
        ],
        code: `import lancedb

db = lancedb.connect("./lancedb_data")
table = db.create_table("my_table", data=[{"vector": [1.1, 1.2], "text": "hello"}])
results = table.search([1.1, 1.2]).limit(2).to_df()`
    },
    supabase: {
        name: "Supabase (pgvector) ⚡",
        type: "Cloud Postgres Vector Extension",
        description: "Extension pgvector untuk PostgreSQL yang memungkinkan penyimpan dan pencarian vektor langsung di dalam database SQL relational Supabase.",
        features: [
            "ACID Compliance SQL + Vector Search",
            "Support HNSW dan IVFFlat index di Postgres",
            "Sangat ideal jika aplikasi web Anda sudah berbasis Supabase"
        ],
        code: `-- Enable pgvector extension
CREATE EXTENSION vector;

CREATE TABLE documents (
  id serial PRIMARY KEY,
  content text,
  embedding vector(1536)
);

-- HNSW Vector Index
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);`
    }
};

// State Variables
let currentTab = 'overview';
let activeDB = 'pinecone';
let datasetVectors = [];
let queryVector = { x: 300, y: 200 };
let isDraggingQuery = false;

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initDBSelector();
    initVectorCanvas();
    renderDBDetails('pinecone');
});

// Tab Navigation
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabTarget = btn.getAttribute('data-tab');
            switchTab(tabTarget);
        });
    });
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    const btn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
    const content = document.getElementById(`tab-${tabId}`);
    
    if (btn) btn.classList.add('active');
    if (content) content.classList.add('active');
}

// DB Selector
function initDBSelector() {
    const dbBtns = document.querySelectorAll('.db-select-btn');
    dbBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            dbBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const dbKey = btn.getAttribute('data-db');
            renderDBDetails(dbKey);
        });
    });
}

function selectDB(dbKey) {
    switchTab('dbs-explorer');
    const btn = document.querySelector(`.db-select-btn[data-db="${dbKey}"]`);
    if (btn) btn.click();
}

function renderDBDetails(dbKey) {
    const db = VECTOR_DBS_DATA[dbKey] || VECTOR_DBS_DATA['pinecone'];
    const card = document.getElementById('db-details-card');
    
    let featuresHTML = db.features.map(f => `<li>✅ ${f}</li>`).join('');

    card.innerHTML = `
        <h3>${db.name}</h3>
        <p class="subtitle" style="color: var(--primary-gold); margin-bottom: 12px;">Tipe: ${db.type}</p>
        <p style="color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">${db.description}</p>
        
        <h4 style="margin-bottom: 8px;">Karakteristik Utama:</h4>
        <ul style="list-style: none; margin-bottom: 20px; line-height: 1.8;">${featuresHTML}</ul>

        <h4 style="margin-bottom: 8px;">Contoh Kode Hands-On Python:</h4>
        <pre><code>${escapeHTML(db.code)}</code></pre>
    `;
}

function escapeHTML(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// 2D Vector Playground Canvas
function initVectorCanvas() {
    const canvas = document.getElementById('vectorCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Generate initial random dataset vectors
    generateInitialVectors(20);

    // Canvas Mouse Listeners
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        // Check if clicked near query vector
        const dist = Math.hypot(mouseX - queryVector.x, mouseY - queryVector.y);
        if (dist < 18) {
            isDraggingQuery = true;
        } else {
            // Add new dataset vector
            const categories = ['AI', 'Tech', 'Food'];
            const cat = categories[Math.floor(Math.random() * categories.length)];
            datasetVectors.push({
                id: `vec_${datasetVectors.length + 1}`,
                x: mouseX,
                y: mouseY,
                category: cat
            });
            drawCanvas();
        }
    });

    canvas.addEventListener('mousemove', (e) => {
        if (isDraggingQuery) {
            const rect = canvas.getBoundingClientRect();
            queryVector.x = e.clientX - rect.left;
            queryVector.y = e.clientY - rect.top;
            drawCanvas();
        }
    });

    window.addEventListener('mouseup', () => {
        isDraggingQuery = false;
    });

    // Controls listeners
    document.getElementById('metricSelect').addEventListener('change', drawCanvas);
    document.getElementById('categoryFilter').addEventListener('change', drawCanvas);
    document.getElementById('topkRange').addEventListener('input', (e) => {
        document.getElementById('topkVal').innerText = e.target.value;
        drawCanvas();
    });

    document.getElementById('addRandomBtn').addEventListener('click', () => {
        generateInitialVectors(5);
        drawCanvas();
    });

    document.getElementById('resetCanvasBtn').addEventListener('click', () => {
        datasetVectors = [];
        generateInitialVectors(15);
        drawCanvas();
    });

    drawCanvas();
}

function generateInitialVectors(count) {
    const canvas = document.getElementById('vectorCanvas');
    const categories = ['AI', 'Tech', 'Food'];
    for (let i = 0; i < count; i++) {
        datasetVectors.push({
            id: `vec_${datasetVectors.length + 1}`,
            x: Math.random() * (canvas.width - 60) + 30,
            y: Math.random() * (canvas.height - 60) + 30,
            category: categories[Math.floor(Math.random() * categories.length)]
        });
    }
}

function drawCanvas() {
    const canvas = document.getElementById('vectorCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 40) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    const metric = document.getElementById('metricSelect').value;
    const catFilter = document.getElementById('categoryFilter').value;
    const topK = parseInt(document.getElementById('topkRange').value);

    // Calculate Distances & Filter
    let candidates = datasetVectors.map(v => {
        let score = 0;
        if (metric === 'l2') {
            score = Math.hypot(v.x - queryVector.x, v.y - queryVector.y);
        } else if (metric === 'cosine') {
            // Cosine angle calculation from center
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;
            const qx = queryVector.x - cx, qy = queryVector.y - cy;
            const vx = v.x - cx, vy = v.y - cy;
            const dot = (qx * vx + qy * vy);
            const normQ = Math.hypot(qx, qy);
            const normV = Math.hypot(vx, vy);
            score = normQ && normV ? (dot / (normQ * normV)) : 0;
        } else {
            // Dot Product
            score = (queryVector.x * v.x + queryVector.y * v.y) / 1000;
        }
        return { ...v, score };
    });

    // Apply Payload Filter
    if (catFilter !== 'all') {
        candidates = candidates.filter(c => c.category === catFilter);
    }

    // Sort Top-K
    if (metric === 'l2') {
        candidates.sort((a, b) => a.score - b.score); // Nearest L2 = smallest
    } else {
        candidates.sort((a, b) => b.score - a.score); // Highest similarity
    }

    const topKMatches = candidates.slice(0, topK);
    const topKIds = new Set(topKMatches.map(m => m.id));

    // Draw Dataset Vector Dots
    datasetVectors.forEach(v => {
        const isMatch = topKIds.has(v.id);
        const isFilteredOut = catFilter !== 'all' && v.category !== catFilter;

        ctx.beginPath();
        ctx.arc(v.x, v.y, isMatch ? 8 : 5, 0, Math.PI * 2);
        
        if (isFilteredOut) {
            ctx.fillStyle = 'rgba(156, 163, 175, 0.2)';
        } else if (isMatch) {
            ctx.fillStyle = '#10b981';
            // Connection line to query
            ctx.strokeStyle = 'rgba(16, 185, 129, 0.5)';
            ctx.lineWidth = 2;
            ctx.moveTo(queryVector.x, queryVector.y);
            ctx.lineTo(v.x, v.y);
            ctx.stroke();
        } else {
            ctx.fillStyle = '#3b82f6';
        }
        ctx.fill();

        // Label
        ctx.fillStyle = '#9ca3af';
        ctx.font = '10px Fira Code';
        ctx.fillText(`${v.id} (${v.category})`, v.x + 10, v.y + 4);
    });

    // Draw Query Vector Dot (Red Star)
    ctx.beginPath();
    ctx.arc(queryVector.x, queryVector.y, 10, 0, Math.PI * 2);
    ctx.fillStyle = '#ef4444';
    ctx.shadowColor = '#ef4444';
    ctx.shadowBlur = 15;
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 11px Outfit';
    ctx.fillText('Query', queryVector.x - 16, queryVector.y - 14);

    // Update Results List UI
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = topKMatches.map((m, idx) => `
        <div class="result-card">
            <strong>#${idx + 1} ${m.id}</strong> (${m.category})
            <br><span style="color: #34d399;">Skor (${metric}): ${m.score.toFixed(4)}</span>
        </div>
    `).join('');
}
