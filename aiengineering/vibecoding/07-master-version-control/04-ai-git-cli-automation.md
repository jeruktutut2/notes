# 04 - Ask AI to Handle Your Git and GitHub CLI Tasks

## 🎯 Definisi & Konsep
**Ask AI to Handle Git & GitHub CLI** adalah mendelegasikan tugas-tugas administratif version control—seperti membuat Pull Request (PR), menyelesaikan merge conflict sederhana, membuat rilis tag, atau menulis deskripsi PR—kepada AI melalui antarmuka perintah CLI (`git` dan `gh`).

---

## 💬 Contoh Prompt Automasi GitHub CLI (gh)

### 1. Membuat Pull Request Otomatis
```text
Semua perubahan pada branch `feature/payment` sudah di-push.
Tolong gunakan GitHub CLI (`gh pr create`) untuk membuat Pull Request ke `main`. 
Isi judul dan deskripsi PR secara rinci berdasarkan `git log` perubahan pada branch ini.
```

### 2. Memeriksa Status CI/CD Workflow
```text
Jalankan perintah `gh run list` untuk memeriksa apakah build CI/CD GitHub Actions di branch ini sudah sukses atau gagal.
Jika gagal, ambil log error-nya dengan `gh run view --log-failed`.
```
