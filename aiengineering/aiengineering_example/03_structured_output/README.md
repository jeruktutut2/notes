# 📘 Modul 3 — Structured Output dengan Pydantic

Modul ini membahas teknik **Structured Output**, yaitu bagaimana memaksa Model AI (LLM) untuk selalu merespon dalam bentuk data terstruktur JSON murni yang tervalidasi menggunakan perpustakaan **Pydantic**.

---

## 🎯 Mengapa Ini Penting?
Secara default, respon LLM berupa kalimat bercerita yang tidak menentu (*unstructured text*). Jika aplikasi kamu membutuhkan data untuk dimasukkan ke database SQL, dikirim ke REST API internal, atau memicu logic program, kamu membutuhkan jaminan **Type-Safety** (misal: jumlah item harus integer, harga harus float).

---

## 🔑 Komponen Utama Pydantic
1. **`BaseModel`**: Kelas dasar untuk menentukan struktur field dan tipe data.
2. **`Field(description=...)`**: Penjelasan kegunaan field yang diubah menjadi deskripsi JSON Schema untuk memberi petunjuk pada LLM.
3. **`model_validate_json(raw_str)`**: Metode untuk memvalidasi string JSON mentah dari LLM menjadi instance objek Python yang aman.

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# Pastikan Ollama sudah berjalan
ollama serve

# Jalankan parser nota & ekstraktor tiket CS
python 03_structured_output/main.py
```
