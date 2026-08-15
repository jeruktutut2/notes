const ROADMAP_DATA = {
    "llm-works": {
        title: "LLMs and How They Work?",
        badge: "Introduction",
        content: `
            <p><strong>Large Language Model (LLM)</strong> adalah model deep learning berbasis arsitektur Transformer Decoder-only yang dilatih pada triliunan token teks.</p>
            <h4>Mekanisme Utama:</h4>
            <ul>
                <li><strong>Next-Token Prediction</strong>: Memprediksi probabilitas token berikutnya berdasarkan urutan token sebelumnya.</li>
                <li><strong>Self-Attention Mechanism</strong>: Memungkinkan model menghubungkan bobot relevansi antar kata meskipun terpisah jauh.</li>
                <li><strong>Pre-training vs Instruction Tuning</strong>: Pre-training menghasilkan Base Model, sedangkan SFT + RLHF/DPO menghasilkan Instruct Model.</li>
            </ul>
        `
    },
    "what-is-prompt": {
        title: "What is a Prompt?",
        badge: "Introduction",
        content: `
            <p><strong>Prompt</strong> adalah teks masukan, konteks, instruksi, dan data yang diberikan kepada LLM untuk mengarahkan pembentukan respons.</p>
            <h4>5 Komponen Utama Prompt:</h4>
            <ol>
                <li><strong>System Instruction</strong>: Peran dan aturan dasar.</li>
                <li><strong>Context</strong>: Informasi latar belakang.</li>
                <li><strong>Task / Instruction</strong>: Tugas spesifik yang harus dikerjakan.</li>
                <li><strong>Input Data</strong>: Teks yang akan diproses.</li>
                <li><strong>Output Format</strong>: Format jawaban (JSON, XML, Markdown).</li>
            </ol>
        `
    },
    "what-is-pe": {
        title: "What is Prompt Engineering?",
        badge: "Introduction",
        content: `
            <p>Seni dan ilmu merancang masukan teks secara sistematis untuk mengoptimalkan output LLM <strong>tanpa mengubah bobot (weights) model</strong>.</p>
            <h4>Tujuan Utama:</h4>
            <ul>
                <li>Meningkatkan akurasi dan konsistensi.</li>
                <li>Mencegah halusinasi dan serangan Prompt Injection.</li>
                <li>Menghasilkan format terstruktur untuk aplikasi software.</li>
            </ul>
        `
    },
    "term-tokens": {
        title: "Tokens (Tokenisasi)",
        badge: "Common Terminology",
        content: `
            <p>Unit terkecil teks yang diproses oleh LLM. 1 token &approx; 4 karakter bahasa Inggris (&approx; 0.75 kata).</p>
            <pre>Teks: "Prompt Engineering"
Tokens: ["Prompt", " ing", " Engineering"]</pre>
        `
    },
    "term-context": {
        title: "Context Window",
        badge: "Common Terminology",
        content: `
            <p>Batas maksimum total token (input + output) yang dapat diproses LLM dalam 1 request.</p>
            <ul>
                <li><strong>GPT-4o</strong>: 128,000 token</li>
                <li><strong>Claude 3.5 Sonnet</strong>: 200,000 token</li>
                <li><strong>Gemini 1.5 Pro</strong>: 2,000,000 token</li>
            </ul>
        `
    },
    "cfg-temp": {
        title: "Temperature ($T$)",
        badge: "LLM Configuration",
        content: `
            <p>Mengontrol kreativitas dan acaknya respons LLM.</p>
            <ul>
                <li><strong>T = 0.0</strong>: Deterministik (Greedy). Cocok untuk Coding, Math, JSON.</li>
                <li><strong>T = 0.7</strong>: Keseimbangan kreativitas dan akurasi.</li>
                <li><strong>T = 1.2+</strong>: Sangat acak dan berpotensi halusinasi.</li>
            </ul>
        `
    },
    "tech-cot": {
        title: "Chain of Thought (CoT) Prompting",
        badge: "Prompting Techniques",
        content: `
            <p>Mendorong LLM menguraikan tahapan berpikir sebelum memberikan jawaban akhir.</p>
            <pre>[Prompt]
Berapa 15% dari 240? Mari kita berpikir langkah demi langkah.

[Output CoT]
Langkah 1: 10% dari 240 = 24.
Langkah 2: 5% dari 240 = 12.
Langkah 3: Total = 24 + 12 = 36.</pre>
        `
    },
    "tech-tot": {
        title: "Tree of Thoughts (ToT) Prompting",
        badge: "Prompting Techniques",
        content: `
            <p>Mengeksplorasi beberapa cabang pemikiran sekaligus dalam struktur pohon (Tree Graph) dengan algoritma BFS/DFS untuk memecahkan masalah kompleks.</p>
        `
    },
    "out-structured": {
        title: "Structured Outputs (JSON, XML, CSV)",
        badge: "Outputs & Enforcement",
        content: `
            <p>Memaksa LLM mengembalikan output terstruktur yang dapat diparse secara otomatis oleh aplikasi.</p>
            <pre>```json
{
  "status": "success",
  "data": {"sentiment": "positif", "score": 0.95}
}
```</pre>
        `
    },
    "best-practices-all": {
        title: "14 Gold Rules of Prompting Best Practices",
        badge: "Roadmap Best Practices",
        content: `
            <ol>
                <li>Provide few-shot examples for structure or output style you need</li>
                <li>Keep your prompts short and concise</li>
                <li>Ask for structured output if it helps e.g. JSON, XML, Markdown, CSV</li>
                <li>Use variables / placeholders in your prompts</li>
                <li>Prioritize giving clearer instructions over adding constraints</li>
                <li>Control the maximum output length</li>
                <li>Experiment with input formats and writing styles</li>
                <li>Tune sampling (temperature, top-k, top-p) for determinism vs creativity</li>
                <li>Guard against prompt injection; sanitize user text</li>
                <li>Automate evaluation; integrate unit tests for outputs</li>
                <li>Document and track prompt versions</li>
                <li>Optimize for latency & cost in production pipelines</li>
                <li>Document decisions, failures, and learnings for future devs</li>
                <li>Delimit different sections with triple backticks or XML tags</li>
            </ol>
        `
    }
};
