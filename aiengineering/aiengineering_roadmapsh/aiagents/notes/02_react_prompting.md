# 02. ReAct Prompting (Reasoning + Acting Framework)

**ReAct (Reasoning and Acting)** adalah paradigma dasar yang paling banyak digunakan untuk membangun AI Agent otonom. Dikenalkan oleh Yao et al. (2022), ReAct mengombinasikan *Reasoning Trace* (pikiran logis LLM) dan *Task-Specific Actions* (interaksi dengan alat luar/dunia nyata) secara bergantian.

---

## 1. Konsep Dasar ReAct Framework

```
                    +--------------------------------+
                    |           USER GOAL            |
                    +--------------------------------+
                                    |
                                    v
            +------------------------------------------------+
            |                  THOUGHT                       |
            |   (LLM merencanakan / menganalisis situasi)    |
            +------------------------------------------------+
                                    |
                                    v
            +------------------------------------------------+
            |                   ACTION                       |
            |   (LLM memilih Tool & membuat argumen JSON)    |
            +------------------------------------------------+
                                    |
                                    v
            +------------------------------------------------+
            |                 OBSERVATION                    |
            | (Hasil dari eksekusi Tool dikembalikan ke LLM) |
            +------------------------------------------------+
                                    |
                 [Apakah Goal Sudah Tercapai?]
                      /                    \
                     Tidak                 Ya
                    /                        \
                   v                          v
       (Ulangi ke THOUGHT)             FINAL ANSWER
```

---

## 2. Struktur Loop ReAct

1. **Thought (Pemikiran)**: Agent mengevaluasi masalah saat ini, apa yang sudah diketahui dari *Observation* sebelumnya, dan apa yang harus dilakukan berikutnya.
2. **Action (Aksi)**: Agent memutuskan memanggil salah satu alat yang tersedia dalam format yang telah ditentukan (misalnya: `Action: calculator(expression="15 * 42")`).
3. **Observation (Pengamatan)**: Environment mengeksekusi alat tersebut dan mengembalikan hasilnya ke agen (misalnya: `Observation: 630`).
4. **Final Answer (Jawaban Akhir)**: Ketika agen memiliki cukup informasi untuk menyelesaikan tugas, agen mengeluarkan jawaban akhir ke pengguna.

---

## 3. Contoh ReAct Execution Trace

**User Query**: *"Berapa populasi Jakarta dikali 2, lalu ditambah populasi Bandung?"*

```text
Thought: Saya perlu mencari populasi terbaru kota Jakarta dan Bandung terlebih dahulu.
Action: search_web("populasi jakarta terbaru")
Observation: Menurut data BPS 2024, populasi DKI Jakarta adalah 10.680.000 jiwa.

Thought: Sekarang saya sudah mendapatkan populasi Jakarta (10.680.000). Langkah selanjutnya adalah mengalikannya dengan 2.
Action: calculator("10680000 * 2")
Observation: 21360000

Thought: Sekarang saya perlu mencari populasi kota Bandung.
Action: search_web("populasi kota bandung terbaru")
Observation: Populasi kota Bandung pada tahun 2024 adalah 2.530.000 jiwa.

Thought: Sekarang saya akan menjumlahkan hasil perkalian populasi Jakarta (21.360.000) dengan populasi Bandung (2.530.000).
Action: calculator("21360000 + 2530000")
Observation: 23890000

Thought: Saya telah mendapatkan hasil akhir dari seluruh kalkulasi.
Final Answer: Hasil perkalian populasi Jakarta (10,68 juta x 2 = 21,36 juta) ditambah populasi Bandung (2,53 juta) adalah 23.890.000 jiwa.
```

---

## 4. Struktur Prompt Template ReAct (System Prompt)

```text
Anda adalah AI Agent otonom yang menyelesaikan masalah dengan pola ReAct (Thought -> Action -> Observation).

Anda memiliki akses ke tools berikut:
{tool_descriptions}

Gunakan format berikut untuk setiap langkah:

Question: Pertanyaan/Tugas yang harus diselesaikan
Thought: Pikirkan langkah logis apa yang harus diambil
Action: [NamaTool](argumen_json)
Observation: Hasil dari eksekusi tool akan dimasukkan di sini oleh sistem
... (proses Thought/Action/Observation ini bisa berulang N kali)
Thought: Saya sekarang tahu jawaban akhirnya
Final Answer: Jawaban akhir lengkap untuk user

Aturan Penting:
1. Hanya keluarkan SATU Thought dan SATU Action per langkah.
2. Selalu tunggu Observation sebelum membuat Thought berikutnya.
3. Jangan mengarang Observation!
```

---

## 5. Keuntungan & Keterbatasan ReAct

### Keuntungan:
- **Interpretability (Transparansi)**: Kita dapat membaca jejak pemikiran (`Thought`) agen untuk memahami alasan di balik aksi tertentu.
- **Error Recovery (Koreksi Diri)**: Jika sebuah `Action` menghasilkan error di `Observation`, agen bisa membuat `Thought` baru untuk mencoba pendekatan atau alat alternatif.
- **Hallucination Mitigation**: Mengandalkan fakta empiris dari `Observation` eksternal alih-alih ingatan statis LLM.

### Keterbatasan:
- **Infinite Loops**: Agen bisa terjebak memanggil tool yang sama berulang kali jika tidak ada penanganan max iteration limit.
- **Context Window Bloat**: Jejak *Thought-Action-Observation* menumpuk cepat dan memakan tokens context window LLM.
