# 02 - Start Each New Feature With a Clean Git Slate

## 🎯 Definisi & Konsep
**Start Each Feature With a Clean Slate** adalah memastikan bahwa `git status` dalam kondisi bersih (tanpa ada file uncommitted atau unstaged) sebelum Anda menginstruksikan AI memulai pengerjaan fitur baru.

---

## 🛠️ Mengapa "Clean Slate" Wajib?
1. **Kejelasan Context Diff**: Saat Anda meminta AI menguji kodenya, AI dan linter dapat membedakan mana kode lama vs mana kode baru yang dibuat untuk fitur ini.
2. **Keahlian Melacak Bug**: Jika terjadi kegagalan, Anda tinggal menjalankan `git diff` atau `git checkout .` untuk membuang eksperimen AI yang gagal tanpa takut menghapus pekerjaan sebelumnya.

---

## 💬 Perintah Terminal Persiapan Clean Slate
```bash
# Periksa status
git status

# Jika ada sisa file uncommitted, commit atau stash terlebih dahulu
git add .
git commit -m "docs: update spec document"

# Atau buat branch baru khusus fitur ini
git checkout -b feature/auth-google-oauth
```
