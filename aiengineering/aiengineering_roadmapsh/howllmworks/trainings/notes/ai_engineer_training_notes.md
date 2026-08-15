# Catatan Implementasi Model Training - AI Engineering

Berdasarkan bagian "Training" (atau Model Training/Fine-Tuning) pada roadmap AI Engineer (roadmap.sh/ai-engineer), berikut adalah konsep-konsep utama yang bisa dipelajari dan diimplementasikan secara langsung menggunakan bahasa pemrograman (terutama Python).

## 1. Persiapan Data (Data Preparation & Preprocessing)
Sebelum model dilatih, data harus disiapkan dalam format yang bisa dipahami oleh model (tensor/vektor).
*   **Apa yang dipelajari:** 
    *   Data Loading (memuat dataset besar).
    *   Pembersihan data (handling missing values, outliers).
    *   **Untuk NLP (Teks):** Tokenization, padding, truncation.
    *   **Untuk Computer Vision:** Resizing, normalization, data augmentation.
*   **Implementasi Kode (Python):**
    *   Menggunakan `pandas` atau `datasets` (Hugging Face) untuk memuat data dari file CSV, JSON, atau database.
    *   Menggunakan `AutoTokenizer` dari library `transformers` untuk memotong teks menjadi token numerik.
    *   Menggunakan `torchvision.transforms` untuk melakukan augmentasi gambar.

## 2. Mendefinisikan Model & Arsitektur
Memilih arsitektur jaringan saraf (neural networks) yang sesuai dengan masalah, atau menggunakan model *pre-trained* (Transfer Learning).
*   **Apa yang dipelajari:**
    *   Memahami layer dasar (Linear, Convolutional, Attention mechanisms).
    *   Memuat model *open-source* (misal: Llama, BERT, ResNet).
*   **Implementasi Kode (Python):**
    *   Membangun arsitektur kustom (dari nol) menggunakan subclass `torch.nn.Module` (PyTorch) atau Sequential API di Keras (TensorFlow).
    *   Memuat model *pre-trained* menggunakan `AutoModelForCausalLM`, `AutoModelForSequenceClassification`, dll. dari Hugging Face.

## 3. Proses Pelatihan (Training Loop) & Fine-Tuning
Ini adalah inti dari bagian training, di mana model belajar menyesuaikan bobotnya (*weights*) berdasarkan data latih.
*   **Apa yang dipelajari:**
    *   **Loss Function:** Fungsi matematis untuk mengukur seberapa besar tingkat error model (misal: Cross-Entropy, MSE).
    *   **Optimizer:** Algoritma untuk memperbarui bobot agar loss semakin kecil (misal: AdamW, SGD).
    *   **Backpropagation:** Menghitung gradien dari loss terhadap setiap bobot parameter.
    *   **PEFT (Parameter-Efficient Fine-Tuning):** Teknik seperti LoRA (Low-Rank Adaptation) atau QLoRA untuk melatih model besar (seperti LLM) dengan memori VRAM GPU yang terbatas.
*   **Implementasi Kode (Python):**
    *   **Low-level:** Menulis *training loop* manual dengan PyTorch. Proses standarnya meliputi:
        1.  Forward pass: `output = model(input)`
        2.  Hitung loss: `loss = criterion(output, target)`
        3.  Zero gradients: `optimizer.zero_grad()`
        4.  Backward pass: `loss.backward()`
        5.  Pembaruan bobot: `optimizer.step()`
    *   **High-level:** Menggunakan `Trainer` API dari Hugging Face atau `PyTorch Lightning` untuk mengabstraksi *training loop* agar lebih efisien dan rapi.
    *   **PEFT:** Menggunakan library `peft` dari Hugging Face untuk menerapkan adapter LoRA ke dalam model.

## 4. Evaluasi (Evaluation & Metrics)
Mengukur performa model menggunakan data yang tidak pernah dilihat sebelumnya (*Validation/Test set*) untuk mencegah *overfitting*.
*   **Apa yang dipelajari:**
    *   Metrik klasifikasi umum: Accuracy, Precision, Recall, F1-Score.
    *   Metrik khusus NLP: ROUGE, BLEU, Perplexity.
*   **Implementasi Kode (Python):**
    *   Menghitung metrik menggunakan fungsi bawaan `scikit-learn` (misal: `accuracy_score`, `classification_report`).
    *   Menggunakan library `evaluate` dari Hugging Face yang secara otomatis menghitung metrik standar yang kompleks.

## 5. Hyperparameter Tuning
Mencari kombinasi pengaturan terbaik agar model bisa belajar lebih optimal. Berbeda dengan parameter, *hyperparameter* tidak dipelajari oleh model selama training melainkan diatur sebelum training.
*   **Apa yang dipelajari:** Melakukan tuning untuk nilai *Learning rate*, *batch size*, jumlah *epochs*, *dropout rate*, dll.
*   **Implementasi Kode (Python):** Mengotomatiskan proses pencarian hiperparameter ini menggunakan library terpisah seperti `Optuna` atau `Ray Tune` untuk mencoba berbagai kombinasi secara sistematis.

## 6. Menyimpan & Ekspor Model
Menyimpan model akhir yang sudah dilatih agar siap digunakan di aplikasi (Deployment/Inference).
*   **Apa yang dipelajari:** Format penyimpanan *state dict* / *weights* model, dan format *export*.
*   **Implementasi Kode (Python):**
    *   Menyimpan dengan PyTorch: `torch.save(model.state_dict(), 'model_weights.pth')`.
    *   Menyimpan dengan Hugging Face: `model.save_pretrained('./my-fine-tuned-model')`.
    *   Mengekspor model ke format standar yang lebih ringan dan cepat untuk produksi menggunakan format ONNX (`torch.onnx.export`).
