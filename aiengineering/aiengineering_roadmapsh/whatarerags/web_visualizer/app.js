/**
 * APP.JS - Interactive Web Visualizer Logic for 'What Are RAGs'
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initRoadmapDiagram();
    initChunkingLab();
    initPipelineSimulator();
    initMatrixEvaluator();
    initFrameworkSwitcher();
});

/* --------------------------------------------------------------------------
 * 1. TAB NAVIGATION
 * -------------------------------------------------------------------------- */
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');

            navButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });
}

/* --------------------------------------------------------------------------
 * 2. ROADMAP DIAGRAM INTERACTIVE PANEL
 * -------------------------------------------------------------------------- */
const NODE_DETAILS = {
    'usecases': {
        title: '🎯 RAG Usecases',
        desc: 'Kasus penggunaan utama RAG meliputi Enterprise Knowledge Base (Q&A Dokumen SOP internal), Customer Support Chatbot (integrasi data transaksi & retur real-time), Codebase QA (pencarian repositori monorepo), dan Analisis Regulasi Medis/Hukum dengan sitasi dokumen.'
    },
    'vs-finetuning': {
        title: '⚖️ RAG vs Fine-tuning',
        desc: 'RAG digunakan untuk memperbarui data fakta privat/terkini secara instant via Vector DB tanpa halusinasi dan menyediakan sitasi. Fine-tuning digunakan untuk mengubah style, tone, format output (JSON mode), atau penyesuaian domain tanpa memperbarui data terorganisir.'
    },
    'chunking': {
        title: '✂️ Chunking (Implementing RAG)',
        desc: 'Tahap 1: Memotong dokumen panjang menjadi pecahan (chunks) berukuran terukur (Fixed-size, Sentence, Recursive, atau Semantic) dengan area overlap agar konteks di perbatasan kalimat tidak hilang.'
    },
    'embedding': {
        title: '🔢 Embedding (Implementing RAG)',
        desc: 'Tahap 2: Mengkonversi setiap text chunk menjadi dense vector embedding berdimensi tinggi (misal 1536 dimensi pada OpenAI text-embedding-3-small) yang mewakili makna semantisnya.'
    },
    'vectordb': {
        title: '🗄️ Vector Database (Implementing RAG)',
        desc: 'Tahap 3: Menyimpan vector dan payload metadata (teks asli, halaman, ID dokumen) ke dalam Vector DB (FAISS, Chroma, Pinecone) menggunakan struktur indeks cepat seperti HNSW atau IVF.'
    },
    'retrieval': {
        title: '🔎 Retrieval Process (Implementing RAG)',
        desc: 'Tahap 4: Mengambil Top-K chunks paling relevan menggunakan Cosine Similarity, Hybrid Search (Dense Vector + BM25 Sparse Keyword), metadata filter, serta Cross-Encoder Re-ranking.'
    },
    'generation': {
        title: '🤖 Generation (Implementing RAG)',
        desc: 'Tahap 5: Menyusun Augmented System Prompt yang menggabungkan pertanyaan pengguna dan konteks dokumen hasil retrieval, kemudian mengirimkannya ke LLM untuk mensintesis jawaban bersitasi.'
    }
};

function initRoadmapDiagram() {
    const nodes = document.querySelectorAll('.roadmap-node, .step-card, .way-item');
    const titleElem = document.getElementById('panel-title');
    const descElem = document.getElementById('panel-desc');

    nodes.forEach(node => {
        node.addEventListener('click', () => {
            const key = node.getAttribute('data-node') || node.getAttribute('data-way');
            if (NODE_DETAILS[key]) {
                titleElem.innerText = NODE_DETAILS[key].title;
                descElem.innerText = NODE_DETAILS[key].desc;
            } else if (key) {
                titleElem.innerText = `🧱 Framework / Approach: ${key.toUpperCase()}`;
                descElem.innerText = `Metode pengimplementasian RAG menggunakan ${key}. Anda dapat membandingkan sintaks kodenya pada tab 'Framework Switcher'.`;
            }
        });
    });
}

/* --------------------------------------------------------------------------
 * 3. LIVE CHUNKING LAB
 * -------------------------------------------------------------------------- */
function initChunkingLab() {
    const strategySelect = document.getElementById('chunk-strategy');
    const sizeInput = document.getElementById('chunk-size');
    const overlapInput = document.getElementById('chunk-overlap');
    const textInput = document.getElementById('input-text');

    const valSize = document.getElementById('val-size');
    const valOverlap = document.getElementById('val-overlap');
    const chunkCount = document.getElementById('chunk-count');
    const chunksOutput = document.getElementById('chunks-output');

    function updateChunks() {
        const strategy = strategySelect.value;
        const size = parseInt(sizeInput.value);
        const overlap = parseInt(overlapInput.value);
        const text = textInput.value.trim();

        valSize.innerText = size;
        valOverlap.innerText = overlap;

        if (!text) {
            chunksOutput.innerHTML = '<p class="text-muted">Teks kosong.</p>';
            chunkCount.innerText = 0;
            return;
        }

        let chunks = [];
        if (strategy === 'fixed') {
            let start = 0;
            while (start < text.length) {
                let end = Math.min(start + size, text.length);
                let c = text.substring(start, end).trim();
                if (c) chunks.push(c);
                start += Math.max(size - overlap, 1);
            }
        } else if (strategy === 'sentence') {
            const sentences = text.split(/(?<=[.!?])\s+/);
            chunks = sentences.filter(s => s.trim().length > 0);
        } else if (strategy === 'recursive') {
            const parts = text.split('\n');
            parts.forEach(p => {
                if (p.length <= size) {
                    if (p.trim()) chunks.push(p.trim());
                } else {
                    let sub = p.split('. ');
                    sub.forEach(s => { if (s.trim()) chunks.push(s.trim()); });
                }
            });
        }

        chunkCount.innerText = chunks.length;
        chunksOutput.innerHTML = chunks.map((c, idx) => `
            <div class="chunk-card">
                <div class="chunk-header">
                    <span>Chunk #${idx + 1}</span>
                    <span>${c.length} Karakter (~${Math.ceil(c.length / 4)} Tokens)</span>
                </div>
                <div class="chunk-text">"${escapeHtml(c)}"</div>
            </div>
        `).join('');
    }

    strategySelect.addEventListener('change', updateChunks);
    sizeInput.addEventListener('input', updateChunks);
    overlapInput.addEventListener('input', updateChunks);
    textInput.addEventListener('input', updateChunks);

    updateChunks();
}

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/* --------------------------------------------------------------------------
 * 4. EXECUTION PIPELINE SIMULATOR
 * -------------------------------------------------------------------------- */
function initPipelineSimulator() {
    const btnRun = document.getElementById('btn-run-sim');
    const queryInput = document.getElementById('user-query-input');
    const finalResp = document.getElementById('sim-final-response');

    btnRun.addEventListener('click', () => {
        const query = queryInput.value.trim() || "Berapa lama garansi laptop gaming?";
        
        // Step animations
        const steps = [1, 2, 3, 4];
        steps.forEach(s => document.getElementById(`sim-step-${s}`).classList.remove('running'));
        
        finalResp.innerText = "⏳ Sedang memproses alur kerja RAG...";

        setTimeout(() => {
            document.getElementById('sim-step-1').classList.add('running');
            document.getElementById('sim-out-1').innerText = `Vector: [0.142, -0.892, 0.431, 0.052 ... 16 dim]`;
        }, 300);

        setTimeout(() => {
            document.getElementById('sim-step-2').classList.add('running');
            document.getElementById('sim-out-2').innerText = `Scanning HNSW Index... Cosine Similarity Score: 0.924`;
        }, 900);

        setTimeout(() => {
            document.getElementById('sim-step-3').classList.add('running');
            document.getElementById('sim-out-3').innerText = `Retrieved Doc ID #DOC-101: "Garansi resmi berlaku 2 tahun di Service Center."`;
        }, 1500);

        setTimeout(() => {
            document.getElementById('sim-step-4').classList.add('running');
            document.getElementById('sim-out-4').innerText = `System Prompt Augmented dengan 1 Top Context Chunk!`;
            
            finalResp.innerHTML = `
                <strong>Berdasarkan Dokumen Garansi #DOC-101:</strong><br>
                Laptop Gaming dilengkapi garansi resmi selama 2 tahun untuk sparepart utama di seluruh Service Center resmi. Klaim garansi wajib membawa kartu garansi asli. [Sitasi: DOC-101]
            `;
        }, 2100);
    });
}

/* --------------------------------------------------------------------------
 * 5. RAG VS FINE-TUNING EVALUATOR
 * -------------------------------------------------------------------------- */
function initMatrixEvaluator() {
    const freqInput = document.getElementById('param-freq');
    const citInput = document.getElementById('param-citation');
    const styleInput = document.getElementById('param-style');
    const budgetInput = document.getElementById('param-budget');

    const recBadge = document.getElementById('rec-badge');
    const recExplanation = document.getElementById('rec-explanation');

    function evaluate() {
        const freq = parseInt(freqInput.value);
        const cit = parseInt(citInput.value);
        const style = parseInt(styleInput.value);
        const budget = parseInt(budgetInput.value);

        if (freq >= 3 || cit >= 3) {
            if (style >= 4) {
                recBadge.innerText = "HYBRID APPROACH (RAG + Fine-Tuning)";
                recExplanation.innerText = "Proyek Anda butuh RAG untuk fakta & sitasi terkini, plus Fine-Tuning untuk mengajari gaya/format output yang sangat ketat.";
            } else {
                recBadge.innerText = "RAG (Retrieval-Augmented Generation)";
                recExplanation.innerText = "Solusi terbaik! Data Anda cepat berubah / butuh sitasi eksplisit. RAG sangat murah dan hemat waktu dibandingkan fine-tuning.";
            }
        } else if (style >= 4) {
            recBadge.innerText = "FINE-TUNING";
            recExplanation.innerText = "Proyek Anda tidak butuh update data sering, namun memerlukan kustomisasi nada dan format output khusus.";
        } else {
            recBadge.innerText = "PROMPT ENGINEERING MURNI";
            recExplanation.innerText = "Cukup gunakan System Prompt yang disusun baik tanpa perlu infrastruktur RAG atau fine-tuning.";
        }
    }

    [freqInput, citInput, styleInput, budgetInput].forEach(inp => inp.addEventListener('input', evaluate));
    evaluate();
}

/* --------------------------------------------------------------------------
 * 6. FRAMEWORK SWITCHER CODE PLAYGROUND
 * -------------------------------------------------------------------------- */
const CODE_SNIPPETS = {
    'sdks': {
        title: 'Pure Python / Direct SDKs',
        code: `# 1. Direct Chunking & Vector Search
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 2. Query Vector DB directly
query_vec = get_embedding("Berapa lama garansi?")
scores = [cosine_similarity(query_vec, doc_vec) for doc_vec in doc_vectors]
top_chunk = documents[np.argmax(scores)]

# 3. Direct LLM Call
prompt = f"Konteks: {top_chunk}\\n\\nPertanyaan: Berapa lama garansi?"
response = openai.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])`
    },
    'langchain': {
        title: 'LangChain Framework',
        code: `from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Pipeline
loader = TextLoader("sop_hr.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=vectorstore.as_retriever())
result = qa_chain.invoke("Berapa jatah cuti melahirkan?")`
    },
    'llamaindex': {
        title: 'LlamaIndex Framework',
        code: `from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

# 1. Load & Index
documents = SimpleDirectoryReader("./data_sop").load_data()
index = VectorStoreIndex.from_documents(documents)

# 2. Query Engine
query_engine = index.as_query_engine(similarity_top_k=3)
response = query_engine.query("Berapa jatah cuti melahirkan?")
print(response)`
    },
    'haystack': {
        title: 'Haystack by Deepset',
        code: `from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator

# Modular Nodes Pipeline
pipeline = Pipeline()
pipeline.add_component("retriever", text_embedder_retriever)
pipeline.add_component("prompt_builder", PromptBuilder(template=template))
pipeline.add_component("llm", OpenAIGenerator())

pipeline.connect("retriever.documents", "prompt_builder.documents")
pipeline.connect("prompt_builder", "llm")
result = pipeline.run({"retriever": {"query": "Garansi laptop"}})`
    },
    'ragflow': {
        title: 'RAGFlow (Deep Doc Parsing & Agentic RAG)',
        code: `# RAGFlow mengotomatiskan Deep Document Parsing (PDF, Tables, Scans)
# Dan menyediakan Agentic Flow Orchestration via HTTP API / SDK

from ragflow_sdk import RAGFlow

client = RAGFlow(api_key="ragflow_secret_key")
dataset = client.create_dataset(name="HR_Policies")
dataset.upload_document(filepath="SOP_Internal.pdf", parser_config={"chunk_token_num": 128})

session = client.create_session(dataset_ids=[dataset.id])
response = session.ask("Berapa hari cuti tahunan?")`
    }
};

function initFrameworkSwitcher() {
    const buttons = document.querySelectorAll('.fw-btn');
    const titleElem = document.getElementById('fw-title');
    const codeDisplay = document.getElementById('code-display');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-fw');
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            if (CODE_SNIPPETS[key]) {
                titleElem.innerText = CODE_SNIPPETS[key].title;
                codeDisplay.innerText = CODE_SNIPPETS[key].code;
            }
        });
    });

    // Default load SDKs
    titleElem.innerText = CODE_SNIPPETS['sdks'].title;
    codeDisplay.innerText = CODE_SNIPPETS['sdks'].code;
}
