# 📘 Modul 6 — Agentic AI

Modul ini mempelajari **Agentic AI**, tren terbesar di mana Large Language Model bertindak sebagai "otak otonom" yang mampu membuat perencanaan (*planning*), memilih alat (*tools*), dan mengevaluasi hasil aksinya secara mandiri melalui siklus berulang.

---

## 🎯 Perbandingan Pendekatan

| Berkas | Pendekatan | Kelebihan | Kapan Digunakan |
|---|---|---|---|
| `agent_manual.py` | ReAct murni dari nol (Regex & Requests) | Memahami konsep dasar tanpa black-box framework. | Untuk pemahaman fondasi dan skenario ringan. |
| `agent_langgraph.py` | State Graph berbasis **LangGraph** | Sangat modular, stateful, toleran terhadap error, dan scalable. | Untuk aplikasi agentic skala produksi yang kompleks. |

---

## 🔄 Siklus Loop ReAct (Reasoning + Acting)
1. **Thought**: Agent menganalisis masalah dan memutuskan langkah selanjutnya.
2. **Action**: Agent menentukan tool mana yang dipanggil beserta argumennya.
3. **Observation**: Sistem mengeksekusi tool dan mengembalikan data hasil ke Agent.
4. **Final Answer**: Agent mengakhiri loop saat tugas selesai sepenuhnya.

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# 1. Menjalankan Agent ReAct Manual
python 06_agentic_ai/agent_manual.py

# 2. Menjalankan Konsep Agent LangGraph
python 06_agentic_ai/agent_langgraph.py
```
