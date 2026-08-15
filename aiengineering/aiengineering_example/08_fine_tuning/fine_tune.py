"""
==============================================================================
CONTOH MODUL 8B: SKRIP FINE-TUNING & CUSTOM OLLAMA MODELFILE
==============================================================================
Dalam AI Engineering, terdapat 2 tingkat penyesuaian model:
    1. Custom Modelfile (Ollama): Membuat varian model baru yang menyertakan
       system prompt kustom, parameter bawaan, & adapter secara permanen.
    2. LoRA / QLoRA Fine-Tuning: Melatih 1% bobot parameter menggunakan Unsloth
       di GPU (misal Google Colab T4) lalu mengeksportnya ke format GGUF.

File ini menghasilkan file `Modelfile` otomatis untuk Ollama dan menyediakan
template skrip QLoRA / Unsloth.

CARA PAKAI:
    - Jalankan: python fine_tune.py
==============================================================================
"""

import os

MODELFILE_PATH = os.path.join(os.path.dirname(__file__), "Modelfile")
NAMA_MODEL_CUSTOM = "cs-serba-jaya"


def buat_ollama_modelfile():
    """
    Menghasilkan file konfigurasi 'Modelfile' untuk membuat model custom di Ollama.
    """
    isi_modelfile = """# Base Model dari Google Gemma 3 4B
FROM gemma3:4b

# Atur parameter default
PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER stop "<|im_end|>"

# Atur System Prompt Permanen (Default Persona)
SYSTEM "" "
Kamu adalah CS Virtual Resmi Toko Serba Jaya.
Kamu selalu menyapa pelanggan dengan sopan menggunakan kata panggilan 'Kak'.
Jawablah pertanyaan pelanggan secara singkat, informatif, dan jelas.
"" "
"""
    with open(MODELFILE_PATH, "w", encoding="utf-8") as f:
        f.write(isi_modelfile.strip())

    print(f"✅ File 'Modelfile' berhasil dibuat di: {MODELFILE_PATH}\n")
    print("--- [INSTRUKSI MEMBUAT MODEL CUSTOM DI OLLAMA LOKAL] ---")
    print(f"1. Buka terminal di folder 08_fine_tuning")
    print(f"2. Jalankan perintah:")
    print(f"   ollama create {NAMA_MODEL_CUSTOM} -f Modelfile")
    print(f"3. Uji coba model baru kamu:")
    print(f"   ollama run {NAMA_MODEL_CUSTOM}\n")


def cetak_template_unsloth_qlora():
    """
    Mencetak petunjuk skrip Python QLoRA Unsloth yang biasa dijalankan di Google Colab.
    """
    print("=========================================================")
    print("TEMPLATE SKRIP FINE-TUNING QLoRA (UNSLOTH - GOOGLE COLAB)")
    print("=========================================================")
    
    skrip_colab = '''
# 1. Install Unsloth & Dependensi
# !pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

from unsloth import FastLanguageModel
import torch

max_seq_length = 2048
dtype = None # Auto detect
load_in_4bit = True # Gunakan QLoRA 4-bit quantization

# 2. Muat Base Model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/gemma-2-2b-it-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# 3. Tambahkan LoRA Adapter (Hanya melatih ~1% parameter)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
)

# 4. Latih Model dengan SFTTrainer...
print("Model siap difine-tune dengan dataset_finetune.jsonl!")
'''
    print(skrip_colab)


if __name__ == "__main__":
    buat_ollama_modelfile()
    cetak_template_unsloth_qlora()
