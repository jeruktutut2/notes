#!/usr/bin/env python3
"""
02_transformers_js_web.py
Modul konsep dan demonstrasi Transformers.js (@xenova/transformers):
- Client-side In-Browser Machine Learning (ONNX Runtime + WebGPU)
- Zero-server cost NLP (Text Classification, Embeddings, Summarization)
"""

def generate_transformers_js_code_snippet() -> str:
    """Menghasilkan contoh snippet kode JavaScript Transformers.js."""
    return """// Contoh Kode Integration Transformers.js di Web App Frontend (HTML/JS)
import { pipeline } from '@xenova/transformers';

// 1. Inisialisasi Pipeline Text Classification (Model berjalan 100% di browser!)
const classifier = await pipeline('sentiment-analysis', 'Xenova/distilbert-base-uncased-finetuned-sst-2-english');

// 2. Jalankan Inferensi tanpa server backend!
const result = await classifier('Produk ini sangat luar biasa dan berkinerja tinggi!');
console.log(result);
// Output: [{ label: 'POSITIVE', score: 0.9998 }]

// 3. Inisialisasi Feature Extraction (Embedding) untuk In-Browser Vector Search
const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
const output = await extractor('Search query text', { pooling: 'mean', normalize: true });
console.log('Vector Embedding Array:', output.data);
"""

def main():
    print("=" * 65)
    print(" 🌐 TRANSFORMERS.JS: CLIENT-SIDE WEB INFERENCE EXPLORER")
    print("=" * 65)
    
    print("\n💡 Apa itu Transformers.js?")
    print(" Transformers.js adalah porting JavaScript resmi dari library Python Transformers.")
    print(" Memungkinkan model Machine Learning berjalan langsung di browser pengguna via WebGPU / WebAssembly.")
    
    print("\n⚡ Manfaat Utama untuk Web App Architecture:")
    print(" 1. Biaya Server = $0 (Inferensi ditanggung oleh CPU/GPU pengguna).")
    print(" 2. 100% Privacy (Data sensitif user tidak pernah keluar dari perangkat).")
    print(" 3. Dapat berjalan secara 100% Offline tanpa koneksi internet.")
    
    print("\n💻 Contoh Kode Implementasi Front-End:")
    print(generate_transformers_js_code_snippet())

if __name__ == "__main__":
    main()
