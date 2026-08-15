# 01 - Use `git commit` Regularly After Every Successful AI Task

## 🎯 Definisi & Konsep
**Frequent Git Commits** adalah kebiasaan melakukan commit perubahan ke Git setiap kali satu sub-tugas kecil yang diberikan kepada AI berhasil diverifikasi dan berjalan dengan baik.

Commit bukan sekadar untuk menyimpan di server remote (GitHub/GitLab), melainkan untuk membuat **save point / checkpoint** lokal yang aman.

---

## 🛠️ Mengapa Rutin Commit Penting saat Vibe Coding?
Jika Anda membiarkan AI mengubah 10 file sekaligus tanpa commit intermediate, lalu pada file ke-11 AI membuat kesalahan destruktif, sangat sulit untuk memisahkan kode mana yang sudah benar dan mana yang merusak.

---

## 💬 Contoh Prompt Pembuatan Commit Pesan Otomatis
```text
Fitur pencarian produk sudah berhasil diuji dan tidak ada error.
Tolong buatkan git commit pesan konvensional (conventional commits style) yang menjelaskan perubahan ini, lalu jalankan git commit.
```

### Hasil Commit Message AI:
```text
feat(search): implement client-side product filtering with debounced input

- Add useDebounce custom hook
- Update ProductList component with search query state
- Add unit test for search filter function
```
