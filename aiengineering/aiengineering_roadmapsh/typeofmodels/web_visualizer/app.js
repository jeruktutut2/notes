// Interactive Web Visualizer Application Logic for Type of Models

document.addEventListener('DOMContentLoaded', () => {
    initNavigationTabs();
    initSimulateModel();
    initArchSelector();
    initVramCalculator();
    initTcoSimulator();
});

// 1. Navigation Tabs Switching Logic
function initNavigationTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });
}

// 2. Base vs Instruct Simulation
function initSimulateModel() {
    const btn = document.getElementById('btn-simulate-model');
    const promptInput = document.getElementById('prompt-input');
    const outBase = document.getElementById('out-base-model');
    const outInstruct = document.getElementById('out-instruct-model');

    if (!btn) return;

    btn.addEventListener('click', () => {
        const text = promptInput.value.trim() || "Apa ibukota Indonesia?";

        outBase.textContent = "Sedang mensimulasikan Base Completion...";
        outInstruct.textContent = "Sedang mensimulasikan Instruct Alignment...";

        setTimeout(() => {
            // Base model completion
            outBase.textContent = `${text} Jakarta.\nApa ibukota Malaysia? Kuala Lumpur.\nApa ibukota Jepang? Tokyo.`;

            // Instruct model response
            outInstruct.textContent = `[System: Assistant AI]\nJawab: Ibukota Negara Indonesia saat ini adalah Ibu Kota Nusantara (IKN) di Kalimantan Timur, menggantikan Jakarta sebagai pusat pemerintahan.`;
        }, 300);
    });
}

// 3. Architecture Selector Details
function initArchSelector() {
    const archBtns = document.querySelectorAll('.arch-btn');
    const container = document.getElementById('arch-details');

    const archData = {
        encoder: {
            title: "Encoder-Only (BERT, RoBERTa)",
            attention: "Full Bi-Directional Attention",
            output: "Vector Embeddings & Class Scores",
            useCases: "Semantic Search, Vector Indexing, Sentiment Analysis, Named Entity Recognition.",
            details: "Membaca teks dari dua arah sekaligus. Ideal untuk membuat Vektor Embedding, bukan untuk menghasilkan kalimat baru."
        },
        decoder: {
            title: "Decoder-Only (GPT-4, Llama 3, Qwen, Mistral)",
            attention: "Causal Masked Autoregressive Attention",
            output: "Generative Text (Next Token Prediction)",
            useCases: "LLM Conversational Chat, Code Generation, Reasoning, Tool Calling.",
            details: "Membaca dari kiri ke kanan. Memprediksi satu token berikutnya secara berurutan. Menjadi arsitektur standar mayoritas LLM modern."
        },
        encdec: {
            title: "Encoder-Decoder (T5, BART, Whisper)",
            attention: "Cross-Attention Sequence-to-Sequence",
            output: "Transformed Target Sequence",
            useCases: "Machine Translation, Document Summarization, Audio Transcription.",
            details: "Encoder mengonversi input ke matriks laten, Decoder menghasilkan kalimat target berbasis cross-attention."
        }
    };

    function renderArch(key) {
        const data = archData[key];
        container.innerHTML = `
            <div class="arch-box">
                <h3>${data.title}</h3>
                <p><strong>Mekanisme Attention:</strong> ${data.attention}</p>
                <p><strong>Bentuk Output:</strong> ${data.output}</p>
                <p><strong>Kasus Penggunaan Utama:</strong> ${data.useCases}</p>
                <p class="desc">${data.details}</p>
            </div>
        `;
    }

    archBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            archBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderArch(btn.getAttribute('data-arch'));
        });
    });

    renderArch('encoder');
}

// 4. VRAM Calculator Logic
function initVramCalculator() {
    const inputParams = document.getElementById('vram-params');
    const selectBits = document.getElementById('vram-bits');
    const inputCtx = document.getElementById('vram-context');

    const resWeight = document.getElementById('res-weight-gb');
    const resKv = document.getElementById('res-kv-gb');
    const resTotal = document.getElementById('res-total-vram');
    const resHw = document.getElementById('res-rec-hardware');

    function calculate() {
        const paramsB = parseFloat(inputParams.value) || 8.0;
        const bits = parseInt(selectBits.value) || 4;
        const ctx = parseInt(inputCtx.value) || 8192;

        const weightBytes = bits / 8.0;
        const weightGb = paramsB * weightBytes;

        // KV Cache Approx: 2 * layers(32) * heads(32) * head_dim(128) * ctx * fp16_bytes(2)
        const kvBytes = 2 * 32 * 32 * 128 * ctx * 2;
        const kvGb = kvBytes / (1024 * 1024 * 1024);

        const overheadGb = Math.max(1.5, weightGb * 0.15);
        const totalVram = weightGb + kvGb + overheadGb;

        resWeight.textContent = `${weightGb.toFixed(1)} GB`;
        resKv.textContent = `${kvGb.toFixed(1)} GB`;
        resTotal.textContent = `${totalVram.toFixed(1)} GB VRAM`;

        if (totalVram <= 8.0) {
            resHw.textContent = "NVIDIA RTX 3060 / 4060 8GB";
            resHw.className = "badge green";
        } else if (totalVram <= 16.0) {
            resHw.textContent = "NVIDIA RTX 4070 / 4080 16GB";
            resHw.className = "badge green";
        } else if (totalVram <= 24.0) {
            resHw.textContent = "NVIDIA RTX 3090 / 4090 24GB";
            resHw.className = "badge yellow";
        } else if (totalVram <= 80.0) {
            resHw.textContent = "1x NVIDIA A100 / H100 80GB";
            resHw.className = "badge yellow";
        } else {
            resHw.textContent = `Multi-GPU Cluster (${Math.ceil(totalVram / 80)}x A100 80GB)`;
            resHw.className = "badge red";
        }
    }

    [inputParams, selectBits, inputCtx].forEach(el => {
        if (el) el.addEventListener('input', calculate);
    });

    calculate();
}

// 5. TCO Calculator Logic
function initTcoSimulator() {
    const slider = document.getElementById('token-slider');
    const labelVal = document.getElementById('slider-val');

    const elMini = document.getElementById('cost-gpt4o-mini');
    const elGpt4 = document.getElementById('cost-gpt4o');
    const elSelf = document.getElementById('cost-selfhosted');
    const elSelfHw = document.getElementById('selfhosted-hw');

    if (!slider) return;

    function updateTco() {
        const volumeM = parseFloat(slider.value);
        labelVal.textContent = `${volumeM} Juta Token / Bulan`;

        const totalTokens = volumeM * 1000000;
        const inTokens = totalTokens * 0.7;
        const outTokens = totalTokens * 0.3;

        // GPT-4o-mini: $0.15 / 1M in, $0.60 / 1M out
        const costMini = (inTokens / 1e6 * 0.15) + (outTokens / 1e6 * 0.60);
        
        // GPT-4o: $2.50 / 1M in, $10.00 / 1M out
        const costGpt4 = (inTokens / 1e6 * 2.50) + (outTokens / 1e6 * 10.00);

        let selfCost = 250.0;
        let selfHwText = "1x RTX 4090 (24GB)";

        if (volumeM <= 20) {
            selfCost = 250.0;
            selfHwText = "1x RTX 4090 (24GB)";
        } else if (volumeM <= 150) {
            selfCost = 1200.0;
            selfHwText = "1x A100 (80GB)";
        } else {
            const nodes = Math.ceil(volumeM / 150);
            selfCost = nodes * 1200.0;
            selfHwText = `${nodes}x A100 (80GB Cluster)`;
        }

        elMini.textContent = `$${costMini.toFixed(2)} / bln`;
        elGpt4.textContent = `$${costGpt4.toFixed(2)} / bln`;
        elSelf.textContent = `$${selfCost.toFixed(2)} / bln`;
        elSelfHw.textContent = selfHwText;
    }

    slider.addEventListener('input', updateTco);
    updateTco();
}
