from transformers import AutoModelForSequenceClassification, AutoTokenizer

def main():
    print("=== 2.2 Memuat Model Pre-Trained (Hugging Face) ===\n")
    
    # Kita menggunakan arsitektur DistilBERT (versi lebih ringan dari BERT)
    # yang sudah di-fine-tune untuk analisis sentimen (positif/negatif).
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    
    print(f"Mengunduh/Memuat Tokenizer dan Model: '{model_name}'...\n")
    print("(Ini mungkin memakan waktu sebentar jika belum pernah diunduh)\n")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        # AutoModelForSequenceClassification otomatis menambahkan layer klasifikasi di atas model dasar (BERT)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        print("Model berhasil dimuat!\n")
        
        # Contoh penggunaan langsung (Inference)
        teks = ["I love learning AI Engineering!", "The code is completely broken and full of bugs."]
        
        # Tokenisasi
        inputs = tokenizer(teks, padding=True, truncation=True, return_tensors="pt")
        
        # Prediksi
        outputs = model(**inputs)
        
        # Mendapatkan kelas prediksi (0 = Negatif, 1 = Positif)
        prediksi_id = outputs.logits.argmax(dim=-1)
        
        for i, t in enumerate(teks):
            label = model.config.id2label[prediksi_id[i].item()]
            print(f"Teks: '{t}'")
            print(f"Prediksi Sentimen: {label}\n")
            
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        print("Pastikan koneksi internet aktif untuk mengunduh model dari Hugging Face.")

if __name__ == "__main__":
    main()
