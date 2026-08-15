# 02. Output Control & Repetition Penalties

## Overview
Selain Sampling Parameters, LLM menyediakan **Output Control** (Max Tokens, Stop Sequences) dan **Repetition Penalties** (Frequency Penalty, Presence Penalty) untuk mengendalikan panjang generasi dan pengulangan kata.

---

## 1. Output Control

### A. Max Tokens (`max_tokens` / `max_completion_tokens`)
Menentukan jumlah maksimum token yang boleh dihasilkan oleh LLM dalam satu respons.
- **Penting**: `max_tokens` hanya membatasi **output**, bukan input.
- Jika LLM terhenti karena mencapai `max_tokens`, `finish_reason` API akan bernilai `"length"`, bukan `"stop"`. Hal ini dapat menyebabkan kalimat atau struktur JSON terpotong di tengah jalan (*truncated JSON*).

### B. Stop Sequences (`stop`)
Daftar string atau token kustom yang menginstruksikan LLM untuk **segera menghentikan generasi** saat string tersebut muncul.
- Contoh: `stop=["\n\n", "User:", "```"]`
- **Use Case**:
  - Mencegah model melakukan halusinasi percakapan berlanjut (misal: model berpura-pura menjadi User).
  - Menghentikan output setelah menyelesaikan blok kode.

---

## 2. Repetition Penalties (Penalti Pengulangan)

Frequency Penalty dan Presence Penalty digunakan untuk mencegah LLM mengulang kata atau kalimat yang sama secara terus menerus (*looping repetition*).

### A. Frequency Penalty ($[-2.0 \text{ hingga } 2.0]$)
Memberikan penalti pada token berdasarkan **frekuensi (jumlah berapa kali) token tersebut telah muncul** dalam teks yang dihasilkan sejauh ini.

$$Penalti \propto \text{count}(t_i)$$

- **Nilai Positif ($0.1 - 1.0$)**: Mengurangi kemungkinan LLM mengulang kata yang sama persis secara berturut-turut.
- **Nilai Negatif ($-0.1 - -1.0$)**: Mendorong LLM untuk lebih sering mengulang kata-kata tertentu.

### B. Presence Penalty ($[-2.0 \text{ hingga } 2.0]$)
Memberikan penalti rata kepada token jika token tersebut **pernah muncul setidaknya satu kali** dalam teks yang telah dihasilkan, tanpa peduli berapa kali frekuensinya.

$$Penalti = \begin{cases} \text{penalty_value} & \text{jika count}(t_i) > 0 \\ 0 & \text{lainnya} \end{cases}$$

- **Nilai Positif ($0.1 - 1.0$)**: Mendorong model untuk beralih ke topik baru dan memperkenalkan kata-kata baru.

---

## Ringkasan Perbedaan Penalties

| Parameter | Basis Penalti | Efek Utama |
| :--- | :--- | :--- |
| **Frequency Penalty** | Proposional terhadap frekuensi kemunculan kata | Mencegah pengulangan kata spesifik (misal: pengulangan nama/istilah berulang) |
| **Presence Penalty** | Binary (pernah muncul vs belum pernah) | Mendorong keanekaragaman topik baru (*topic shift*) |
