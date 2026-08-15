# 📖 CATATAN TEORI: MULTIMODAL AI USECASES

File ini berisi catatan teori komprehensif mengenai **6 Utama Multimodal AI Usecases** berdasarkan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 🖼️ 1. Image Understanding

### Konsep Dasar
Image Understanding (Visual Perception) adalah kemampuan model AI untuk tidak hanya mendeteksi piksel gambar, melainkan memahami makna visual, konteks spasial, relasi antar-objek, dan melakukan pemetikan teks (OCR) serta penalaran visual (Visual Reasoning).

### Arsitektur Utama
1. **Vision Transformer (ViT)**: Membagi gambar berukuran $H \times W$ menjadi patch kecil (misal $16 \times 16$ piksel), kemudian memproyeksikannya menjadi urutan token visual (*visual tokens*).
2. **Cross-Attention & Projection Layer**: Menghubungkan visual tokens dari Vision Encoder (misal ViT atau CLIP) ke dalam embedding space milik Large Language Model (LLM).

---

## 🎨 2. Image Generation

### Konsep Dasar
Image Generation (Text-to-Image Synthesis) adalah proses pembuatan citra visual realistis atau artistik berdasarkan instruksi teks (*text prompt*).

### Arsitektur Utama
1. **Latent Diffusion Models (LDM)**: Model generasi yang bekerja di ruang latens yang terkompresi (Latent Space) menggunakan Variational Autoencoder (VAE) untuk efisiensi komputasi.
2. **Reverse Denoising Process**: Proses iteratif penghilangan noise Gaussian dari ruang latens acak dibimbing oleh embedding teks via Cross-Attention.
3. **ControlNet**: Ekstensi arsitektur untuk mengunci struktur gambar (misal pose tubuh, sketsa garis Canny, atau depth map).

---

## 🎥 3. Video Understanding

### Konsep Dasar
Video Understanding menambahkan dimensi waktu (temporal) pada persepsi visual. Model harus memahami bagaimana visual berubah dari frame ke frame.

### Strategi Sampling & Pemrosesan
1. **Keyframe Sampling**: Mengambil frame secara seragam (*uniform sampling*) atau berdasarkan perubahan adegan (*scene detection*).
2. **Spatio-Temporal Attention**: Menghubungkan informasi antar-frame untuk memahami aksi (misalnya membedakan "berlari menuju pintu" vs "berlari menjauhi pintu").

---

## 🔊 4. Audio Processing

### Konsep Dasar
Pengolahan sinyal audio menjadi representasi matematis yang dapat dipahami oleh jaringan saraf.

### Ekstraksi Fitur Audio
1. **Short-Time Fourier Transform (STFT)**: Mengonversi gelombang domain waktu (Waveform) menjadi domain frekuensi.
2. **Log Mel-Spectrogram**: Visualisasi frekuensi yang disesuaikan dengan skala pendengaran manusia (Mel Scale).

---

## 🗣️ 5. Text-to-Speech (TTS)

### Konsep Dasar
TTS mengonversi teks tertulis menjadi sinyal suara manusia yang alami dengan artikulasi dan emosi yang sesuai.

### Pipeline Arsitektur
```text
Text Input ──► Grapheme-to-Phoneme ──► Acoustic Model ──► Neural Vocoder ──► WAV Audio
```
1. **G2P (Grapheme-to-Phoneme)**: Teks diubah menjadi urutan fonem IPA.
2. **Acoustic Model (FastSpeech2/Tacotron)**: Menghasilkan Mel-Spectrogram dari fonem.
3. **Neural Vocoder (HiFi-GAN/BigVGAN)**: Menghasilkan gelombang suara PCM 24kHz dari spectrogram.

---

## 🎙️ 6. Speech-to-Text (STT / ASR)

### Konsep Dasar
Automatic Speech Recognition (ASR) mengonversi sinyal suara audio menjadi teks tertulis beserta informasi timestamp.

### Arsitektur Whisper
Whisper menggunakan arsitektur Transformer Sequence-to-Sequence berbasis encoder-decoder:
- **Encoder**: Menerima 80-channel Log Mel-Spectrogram audio.
- **Decoder**: Menggenerasi token teks beserta label bahasa dan timestamp kata demi kata.
