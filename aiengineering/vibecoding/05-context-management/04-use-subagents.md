# 04 - Ask AI to Use Subagents, If Possible

## 🎯 Definisi & Konsep
**Ask AI to Use Subagents** adalah delegasi tugas spesifik kepada agen AI sekunder (subagent/child agent) yang beroperasi dalam isolasi konteksnya sendiri untuk menyelesaikan tugas kompleks (seperti memunculkan agen penjelajah web, agen pemindai linter, atau agen pengujian).

Setelah subagent menyelesaikan tugasnya, subagent hanya mengembalikan hasil akhir/ringkasan ke percakapan utama tanpa mengotori ruang konteks utama.

---

## 🛠️ Contoh Penggunaan Subagent

```text
Gunakan subagent untuk melakukan riset pada dokumentasi library `Chart.js` v4 terbaru mengenai cara membuat bar chart teranimasi dengan nilai dinamis.
Setelah subagent mendapatkan sampel kodenya, berikan kodenya di percakapan utama ini.
```
