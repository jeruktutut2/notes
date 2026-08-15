"""
=================================================================
2. PIPELINE INFERENCE DENGAN HUGGING FACE
=================================================================
Hugging Face menyediakan `pipeline()` — sebuah abstraksi tingkat
tinggi yang memudahkan inference tanpa perlu setup manual
(tokenizer, model, post-processing).

Pipeline mendukung banyak task:
- text-classification    → Analisis sentimen, klasifikasi topik
- ner                    → Named Entity Recognition
- summarization          → Meringkas teks panjang
- translation            → Terjemahan bahasa
- question-answering     → Menjawab pertanyaan berdasarkan konteks
- text-generation        → Membuat teks baru (GPT-style)
- fill-mask              → Mengisi kata yang hilang (BERT-style)
- zero-shot-classification → Klasifikasi tanpa training khusus

Keuntungan pipeline:
✅ Tidak perlu tahu detail tokenizer/model
✅ Otomatis download model dari Hub
✅ Otomatis post-processing (softmax, decoding, dsb.)
✅ Bisa langsung dipakai dengan 1-2 baris kode
=================================================================
"""

from transformers import pipeline
import time

def demo_text_classification():
    """Task 1: Klasifikasi Teks / Sentiment Analysis."""
    print("=" * 60)
    print("TASK 1: Text Classification (Sentiment Analysis)")
    print("=" * 60)

    # Membuat pipeline — model akan didownload otomatis
    classifier = pipeline("text-classification")

    teks_list = [
        "I absolutely love this new phone!",
        "The service was awful and the food was cold.",
        "It's an average experience, not bad not great."
    ]

    print("\n📊 Hasil Klasifikasi:")
    for teks in teks_list:
        waktu_mulai = time.time()
        hasil = classifier(teks)
        latensi = (time.time() - waktu_mulai) * 1000

        print(f"   Input  : {teks}")
        print(f"   Label  : {hasil[0]['label']} (skor: {hasil[0]['score']:.4f})")
        print(f"   Latensi: {latensi:.1f} ms")
        print()


def demo_ner():
    """Task 2: Named Entity Recognition — mendeteksi entitas dalam teks."""
    print("=" * 60)
    print("TASK 2: Named Entity Recognition (NER)")
    print("=" * 60)

    ner_pipeline = pipeline("ner", aggregation_strategy="simple")

    teks = "Elon Musk founded SpaceX in Hawthorne, California in 2002."
    print(f"\n📝 Input: {teks}")

    hasil = ner_pipeline(teks)

    print("\n🏷️ Entitas yang ditemukan:")
    for entity in hasil:
        print(f"   [{entity['entity_group']}] \"{entity['word']}\" "
              f"(skor: {entity['score']:.4f})")


def demo_summarization():
    """Task 3: Summarization — meringkas teks panjang."""
    print("=" * 60)
    print("TASK 3: Text Summarization")
    print("=" * 60)

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    teks_panjang = """
    Artificial intelligence (AI) has transformed the way we live and work. 
    From virtual assistants like Siri and Alexa to self-driving cars, AI is 
    becoming an integral part of daily life. In healthcare, AI algorithms 
    can analyze medical images to detect diseases earlier than traditional 
    methods. In finance, machine learning models predict market trends and 
    detect fraudulent transactions. The education sector uses AI to 
    personalize learning experiences for students. However, the rapid 
    advancement of AI also raises concerns about job displacement, privacy, 
    and ethical considerations. Experts argue that responsible AI development 
    and regulation are crucial to ensure that the benefits of AI are shared 
    equitably across society.
    """

    print(f"\n📝 Teks Asli ({len(teks_panjang.split())} kata):")
    print(f"   {teks_panjang.strip()[:150]}...")

    waktu_mulai = time.time()
    hasil = summarizer(teks_panjang, max_length=60, min_length=20, do_sample=False)
    latensi = (time.time() - waktu_mulai) * 1000

    print(f"\n📋 Ringkasan ({len(hasil[0]['summary_text'].split())} kata):")
    print(f"   {hasil[0]['summary_text']}")
    print(f"   Latensi: {latensi:.0f} ms")


def demo_question_answering():
    """Task 4: Question Answering — menjawab pertanyaan dari konteks."""
    print("=" * 60)
    print("TASK 4: Question Answering (Extractive QA)")
    print("=" * 60)

    qa_pipeline = pipeline("question-answering")

    konteks = """
    Python is a high-level programming language created by Guido van Rossum 
    and first released in 1991. It emphasizes code readability and supports 
    multiple programming paradigms including procedural, object-oriented, 
    and functional programming. Python is widely used in web development, 
    data science, artificial intelligence, and automation.
    """

    pertanyaan_list = [
        "Who created Python?",
        "When was Python first released?",
        "What does Python emphasize?"
    ]

    print(f"\n📖 Konteks: {konteks.strip()[:100]}...")

    print("\n❓ Pertanyaan & Jawaban:")
    for pertanyaan in pertanyaan_list:
        hasil = qa_pipeline(question=pertanyaan, context=konteks)
        print(f"   Q: {pertanyaan}")
        print(f"   A: {hasil['answer']} (skor: {hasil['score']:.4f})")
        print()


def demo_text_generation():
    """Task 5: Text Generation — membuat teks baru."""
    print("=" * 60)
    print("TASK 5: Text Generation")
    print("=" * 60)

    generator = pipeline("text-generation", model="distilgpt2")

    prompt = "The future of artificial intelligence is"
    print(f"\n📝 Prompt: \"{prompt}\"")

    waktu_mulai = time.time()
    hasil = generator(
        prompt,
        max_new_tokens=50,
        num_return_sequences=2,
        temperature=0.7,
        do_sample=True
    )
    latensi = (time.time() - waktu_mulai) * 1000

    print(f"\n✨ Hasil Generate (latensi: {latensi:.0f} ms):")
    for i, h in enumerate(hasil):
        print(f"   Variasi {i+1}: {h['generated_text']}")
        print()


def demo_zero_shot_classification():
    """Task 6: Zero-Shot Classification — klasifikasi tanpa training khusus."""
    print("=" * 60)
    print("TASK 6: Zero-Shot Classification")
    print("=" * 60)

    classifier = pipeline("zero-shot-classification")

    teks = "Apple just announced the new iPhone 16 with revolutionary AI features."
    kandidat_label = ["technology", "sports", "politics", "entertainment", "business"]

    print(f"\n📝 Teks: {teks}")
    print(f"🏷️ Kandidat Label: {kandidat_label}")

    hasil = classifier(teks, kandidat_label)

    print("\n📊 Hasil Klasifikasi (tanpa training khusus!):")
    for label, skor in zip(hasil['labels'], hasil['scores']):
        bar = "█" * int(skor * 30)
        print(f"   {label:15s} {skor:.4f} {bar}")


def main():
    print("🚀 Demo Pipeline Inference Hugging Face\n")
    print("Pipeline mempermudah inference — cukup tentukan task,")
    print("model akan didownload & dikonfigurasi secara otomatis.\n")

    demo_text_classification()
    print()
    demo_ner()
    print()
    demo_summarization()
    print()
    demo_question_answering()
    print()
    demo_text_generation()
    print()
    demo_zero_shot_classification()

    print("\n" + "=" * 60)
    print("✅ Selesai! Lanjut ke: 02_model_selection/")
    print("=" * 60)

if __name__ == "__main__":
    main()
