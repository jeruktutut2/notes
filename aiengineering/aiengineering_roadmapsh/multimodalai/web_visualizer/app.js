// Multimodal AI Visualizer Logic

document.addEventListener('DOMContentLoaded', () => {
    initTabNavigation();
    initRoadmapInspector();
    initVisionLab();
    initAudioLab();
    initPipelineSimulator();
    initSdkSandbox();
});

// 1. TAB NAVIGATION
function initTabNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// 2. ROADMAP INSPECTOR DATA
const TOPIC_DETAILS = {
    'img-understanding': {
        title: '🖼️ Image Understanding (Visual Perception)',
        badge: 'Usecase 01',
        desc: 'Image Understanding memetakan piksel gambar menjadi representasi makna visual terstruktur. Menggabungkan Vision Transformer (ViT) dengan Large Language Model untuk Visual Question Answering (VQA), Optical Character Recognition (OCR), dan Object Detection.'
    },
    'img-generation': {
        title: '🎨 Image Generation (Text-to-Image)',
        badge: 'Usecase 02',
        desc: 'Image Generation menghasilkan gambar sintetis realistis dari deskripsi teks (*text prompt*). Menggunakan Latent Diffusion Models (LDM) dengan proses Reverse Denoising Sampling dan ControlNet untuk kontrol spasial.'
    },
    'vid-understanding': {
        title: '🎥 Video Understanding (Temporal Analysis)',
        badge: 'Usecase 03',
        desc: 'Video Understanding menambahkan dimensi waktu (temporal) pada persepsi visual. Menggunakan teknik Keyframe Sampling dan Cross-frame Attention untuk melacak urutan peristiwa dan aksi.'
    },
    'audio-proc': {
        title: '🔊 Audio Processing (Spectrogram & Feature Extraction)',
        badge: 'Usecase 04',
        desc: 'Pengolahan sinyal suara mentah (PCM Waveform) menggunakan Short-Time Fourier Transform (STFT) menjadi Log Mel-Spectrogram 80-channel untuk pengenalan suara dan event detection.'
    },
    'tts': {
        title: '🗣️ Text-to-Speech (TTS Vocoder & Voice Cloning)',
        badge: 'Usecase 05',
        desc: 'Teknologi sintesis vokal dari teks. Meliputi modul Grapheme-to-Phoneme, Tacotron/FastSpeech Acoustic Model, dan HiFi-GAN Neural Vocoder 24kHz untuk mengonversi mel-spectrogram menjadi gelombang audio alami.'
    },
    'stt': {
        title: '🎙️ Speech-to-Text (STT / ASR Whisper)',
        badge: 'Usecase 06',
        desc: 'Automatic Speech Recognition (ASR) berbasis arsitektur Transformer Encoder-Decoder Whisper. Mengonversi audio suara menjadi teks beserta timestamp per kata dan penanganan noise.'
    },
    'openai-vision': {
        title: '👁️ OpenAI Vision API (GPT-4o)',
        badge: 'API Task 01',
        desc: 'SDK resmi OpenAI untuk pemrosesan multimodal GPT-4o. Mendukung input gambar tunggal/ganda, detail mode (`low` vs `high`), dan keluaran JSON terstruktur.'
    },
    'dalle-api': {
        title: '🎨 DALL-E API (Image Synthesis)',
        badge: 'API Task 02',
        desc: 'API generasi citra visual DALL-E 3 buatan OpenAI. Menyediakan fitur otomatis Prompt Revision oleh GPT-4, kontrol kualitas `hd`, dan opsi aspek rasio.'
    },
    'nanobanana-api': {
        title: '🍌 NanoBanana API (Specialized REST SDK)',
        badge: 'API Task 03',
        desc: 'Model REST Endpoint terspesialisasi untuk pemrosesan multimodal berlatensi rendah dengan payload multipart data audio dan visual.'
    },
    'whisper-api': {
        title: '🎙️ Whisper API (Transcription & Translation)',
        badge: 'API Task 04',
        desc: 'API audio OpenAI untuk transkripsi otomatis dan penerjemahan langsung dari bahasa apapun ke Bahasa Inggris dengan keluaran format JSON, SRT, dan VTT.'
    },
    'hf-models': {
        title: '🤗 Hugging Face Multimodal Models',
        badge: 'API Task 05',
        desc: 'Kumpulan model open-source: CLIP untuk alignment teks-gambar zero-shot, BLIP/BLIP-2 untuk captioning, dan Florence-2 untuk deteksi objek multi-task.'
    },
    'langchain-multimodal': {
        title: '🦜🔗 LangChain for Multimodal Apps',
        badge: 'API Task 06',
        desc: 'Framework pengikatan multimodal via `HumanMessage` ber-payload image URL / base64 dan `ChatPromptTemplate` dinamis.'
    },
    'llamaindex-multimodal': {
        title: '🦙 LlamaIndex for Multimodal Apps',
        badge: 'API Task 07',
        desc: 'Framework pengindeksan data multimodal melalui `MultiModalVectorStoreIndex` untuk pencarian vektor silang modalitas (Cross-modal Retrieval).'
    }
};

function initRoadmapInspector() {
    const yellowCards = document.querySelectorAll('.yellow-card');
    const titleEl = document.getElementById('inspector-title');
    const badgeEl = document.getElementById('inspector-badge');
    const bodyEl = document.getElementById('inspector-body');

    yellowCards.forEach(card => {
        card.addEventListener('click', () => {
            const topic = card.getAttribute('data-topic');
            const data = TOPIC_DETAILS[topic];
            if (data) {
                titleEl.textContent = data.title;
                badgeEl.textContent = data.badge;
                bodyEl.textContent = data.desc;
            }
        });
    });
}

// 3. VISION LAB
function initVisionLab() {
    const btnVqa = document.getElementById('btn-run-vqa');
    const vqaOutput = document.getElementById('vqa-output');
    
    if (btnVqa) {
        btnVqa.addEventListener('click', () => {
            const imgSelect = document.getElementById('vqa-img-select').value;
            const prompt = document.getElementById('vqa-prompt').value;

            vqaOutput.textContent = `[Processing VQA via Vision Transformer Model...]\nSelected Image: ${imgSelect}\nPrompt Input: "${prompt}"\n\n✓ Patching visual features (16x16 pixels)...\n✓ Aligning tokens via Linear Projection...\n💡 Hasil Reasoning Vision:\n"Gambar ini teridentifikasi sebagai komponen sistem dengan kepastian visual 98.6%. Deteksi objek mengonfirmasi keselarasan instruksi."`;
        });
    }

    const btnDiff = document.getElementById('btn-run-diffusion');
    const diffPreview = document.getElementById('diff-preview');
    const cfgInput = document.getElementById('diff-cfg');
    const cfgVal = document.getElementById('diff-cfg-val');

    if (cfgInput) {
        cfgInput.addEventListener('input', () => {
            cfgVal.textContent = cfgInput.value;
        });
    }

    if (btnDiff) {
        btnDiff.addEventListener('click', () => {
            const prompt = document.getElementById('diff-prompt').value;
            diffPreview.innerHTML = '<div style="color:#fbbf24;">⏳ Sampling Reverse Diffusion (50 Denoising Steps)...</div>';
            
            setTimeout(() => {
                diffPreview.innerHTML = `
                    <div style="text-align:center; padding:10px;">
                        <div style="font-size:2rem;">🌆</div>
                        <div style="color:#a7f3d0; font-weight:600; font-size:0.85rem; margin-top:6px;">Canvas Rendered Successfully!</div>
                        <div style="color:#94a3b8; font-size:0.75rem;">Prompt: "${prompt}" (CFG: ${cfgInput.value})</div>
                    </div>
                `;
            }, 800);
        });
    }
}

// 4. AUDIO LAB
function initAudioLab() {
    const btnStt = document.getElementById('btn-run-stt');
    const sttOutput = document.getElementById('stt-output');

    if (btnStt) {
        btnStt.addEventListener('click', () => {
            sttOutput.textContent = `[Whisper ASR Model Transcribing...]\nLoading 80-channel Log Mel-Spectrogram...\nLanguage Detected: Indonesian (99.4%)\n\nFull Text: "Selamat datang di pembelajaran Whisper API. Sistem secara otomatis memberikan timestamp."\n\n[SRT Subtitle Output]\n1\n00:00,000 --> 00:03,500\nSelamat datang di pembelajaran Whisper API.`;
        });
    }

    const btnTts = document.getElementById('btn-run-tts');
    const ttsOutput = document.getElementById('tts-output');

    if (btnTts) {
        btnTts.addEventListener('click', () => {
            const text = document.getElementById('tts-input-text').value;
            const voice = document.getElementById('tts-voice-select').value;

            ttsOutput.textContent = `[HiFi-GAN Vocoder Active]\nTarget Voice Embedding: ${voice}\nConverting Text -> Phonemes -> Spectrogram...\n\n🔊 Generated WAV Audio Stream: 24,000 Hz, 16-bit Mono\nText Input: "${text}"`;
        });
    }
}

// 5. PIPELINE SIMULATOR
function initPipelineSimulator() {
    const btnSim = document.getElementById('btn-simulate-pipeline');
    const consoleBox = document.getElementById('pipeline-console');

    if (btnSim) {
        btnSim.addEventListener('click', () => {
            const steps = [
                document.getElementById('pipe-step-1'),
                document.getElementById('pipe-step-2'),
                document.getElementById('pipe-step-3'),
                document.getElementById('pipe-step-4')
            ];

            let i = 0;
            consoleBox.textContent = "🚀 Memulai Multimodal Execution Pipeline...";
            
            const interval = setInterval(() => {
                steps.forEach(s => s.classList.remove('active-step'));
                if (i < steps.length) {
                    steps[i].classList.add('active-step');
                    consoleBox.textContent += `\n▶ Step ${i+1}: Executed ${steps[i].querySelector('h4').textContent}`;
                    i++;
                } else {
                    clearInterval(interval);
                    consoleBox.textContent += "\n\n✨ Multimodal Inferencing Pipeline Selesai Sukses!";
                }
            }, 600);
        });
    }
}

// 6. SDK SANDBOX
const SDK_CODES = {
    'openai': {
        file: '01_openai_vision_api.py',
        code: `import json

def test_openai_vision():
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Jelaskan gambar ini!"},
                    {"type": "image_url", "image_url": {"url": "https://example.com/demo.png", "detail": "high"}}
                ]
            }
        ]
    }
    print("OpenAI Vision Request Ready:", json.dumps(payload, indent=2))

test_openai_vision()`,
        output: `OpenAI Vision Request Ready:
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Jelaskan gambar ini!"},
        {"type": "image_url": {"url": "https://example.com/demo.png", "detail": "high"}}
      ]
    }
  ]
}
💡 Respons GPT-4o Vision: "Gambar ini menunjukkan arsitektur sistem multimodal AI."`
    },
    'dalle': {
        file: '02_dalle_api.py',
        code: `def generate_dalle():
    prompt = "Kucing astronot membaca buku di stasiun luar angkasa"
    print(f"Generating DALL-E 3 Image for prompt: '{prompt}'")

generate_dalle()`,
        output: `Generating DALL-E 3 Image for prompt: 'Kucing astronot membaca buku di stasiun luar angkasa'
💡 Revised Prompt by OpenAI: "A cinematic high-resolution digital painting of a cat astronaut reading a book inside a futuristic space station."
🖼️ Output URL: https://oaidalleapiprodscus.blob.core.windows.net/generated_image.png`
    },
    'nanobanana': {
        file: '03_nanobanana_api.py',
        code: `class NanoBananaClient:
    def analyze(self, text, url):
        return {"status": 200, "prediction": "NanoBanana Multimodal Analysis Success"}

client = NanoBananaClient()
print(client.analyze("Deteksi anomali", "https://nanobanana.ai/sample.png"))`,
        output: `{'status': 200, 'prediction': 'NanoBanana Multimodal Analysis Success'}`
    },
    'whisper': {
        file: '04_whisper_api.py',
        code: `def transcribe_audio():
    print("Transcribing audio file via Whisper API...")
    return {"text": "Selamat datang di pembelajaran Whisper API."}

print(transcribe_audio())`,
        output: `Transcribing audio file via Whisper API...
{'text': 'Selamat datang di pembelajaran Whisper API.'}`
    },
    'hf': {
        file: '05_huggingface_models.py',
        code: `def clip_zero_shot():
    print("Calculating CLIP Cosine Similarity...")
    return [("dog in park", 0.942), ("sports car", 0.041)]

print(clip_zero_shot())`,
        output: `Calculating CLIP Cosine Similarity...
[('dog in park', 0.942), ('sports car', 0.041)]`
    },
    'langchain': {
        file: '06_langchain_multimodal.py',
        code: `print("LangChain ChatPromptTemplate with Image Messages Initialized.")`,
        output: `LangChain ChatPromptTemplate with Image Messages Initialized.
Chain Result: Perbandingan arsitektur visual berhasil diproses oleh LangChain Runnable.`
    },
    'llamaindex': {
        file: '07_llamaindex_multimodal.py',
        code: `print("LlamaIndex MultiModalVectorStoreIndex Created.")`,
        output: `LlamaIndex MultiModalVectorStoreIndex Created.
Retrieved Text & Image Nodes: [img_01, doc_01]
Synthesized Cross-modal Response Ready!`
    }
};

function initSdkSandbox() {
    const sdkBtns = document.querySelectorAll('.sdk-tab-btn');
    const filenameEl = document.getElementById('code-filename');
    const codeDisplayEl = document.getElementById('code-display');
    const sdkConsoleEl = document.getElementById('sdk-console');
    const btnRunCode = document.getElementById('btn-run-code');

    let currentSdk = 'openai';

    sdkBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            sdkBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            currentSdk = btn.getAttribute('data-sdk');
            const data = SDK_CODES[currentSdk];
            if (data) {
                filenameEl.textContent = data.file;
                codeDisplayEl.textContent = data.code;
                sdkConsoleEl.textContent = `[Console Output] Ready to run ${data.file}...`;
            }
        });
    });

    // Default view
    if (SDK_CODES['openai']) {
        codeDisplayEl.textContent = SDK_CODES['openai'].code;
    }

    if (btnRunCode) {
        btnRunCode.addEventListener('click', () => {
            const data = SDK_CODES[currentSdk];
            if (data) {
                sdkConsoleEl.textContent = `[Executing ${data.file}...]\n` + data.output;
            }
        });
    }
}
