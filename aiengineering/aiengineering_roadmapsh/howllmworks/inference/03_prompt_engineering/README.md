# Implementasi Point 3: Prompt Engineering

Teknik merancang prompt yang efektif untuk mendapatkan output optimal dari model AI. Prompt engineering adalah skill kunci bagi AI Engineer karena kualitas output sangat bergantung pada cara kita memberikan instruksi ke model.

## Daftar File

1. `1_zero_shot_prompting.py`: Prompting tanpa contoh — model langsung menjawab berdasarkan pengetahuan yang sudah dipelajari saat training.
2. `2_few_shot_prompting.py`: Memberikan beberapa contoh input-output sebelum pertanyaan utama, agar model memahami pola/format yang diinginkan.
3. `3_chain_of_thought.py`: Memandu model untuk "berpikir langkah demi langkah" sebelum memberikan jawaban akhir — meningkatkan akurasi untuk masalah kompleks.
4. `4_system_prompt_design.py`: Merancang system prompt yang mendefinisikan peran, gaya, dan batasan model.

## Konsep Kunci

| Teknik | Deskripsi | Kapan Dipakai |
|--------|-----------|---------------|
| Zero-Shot | Langsung bertanya, tanpa contoh | Task sederhana, model besar |
| Few-Shot | Berikan 2-5 contoh dulu | Task spesifik, format tertentu |
| Chain-of-Thought | Minta model berpikir bertahap | Reasoning, math, logika |
| System Prompt | Definisikan peran & aturan | Semua production use-case |
