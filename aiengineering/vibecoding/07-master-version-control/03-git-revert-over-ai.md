# 03 - If You Need to Revert, Use Git Rather Than AI Native Revert Functionality

## 🎯 Definisi & Konsep
**Use Git Revert Over AI Native Revert** adalah mempercayakan proses pengembalian kode (*rollback*) ke perintah deterministic Git (`git checkout .`, `git reset --hard`, atau `git revert`) daripada meminta AI menulis ulang kode lama yang sudah terhapus lewat prompt verbal.

---

## 🛠️ Mengapa Menghindari "Undo via AI Prompt"?
Ketika Anda meminta AI: *"Tolong batalkan perubahan tadi dan kembalikan kode seperti sebelum kamu ubah"*, AI tidak memiliki ingatan byte-per-byte mengenai status file sebelumnya. AI akan mencoba **merekonstruksi ulang** kode tersebut dari memorinya, yang seringkali menghasilkan perbedaan halus (*silent bugs*).

Git menyimpan representasi biner yang 100% presisi.

---

## 💬 Perintah Git Rollback Presisi

```bash
# 1. Menghapus seluruh perubahan yang belum di-commit dan mengembalikan ke commit terakhir:
git reset --hard HEAD

# 2. Mengembalikan file spesifik yang dirusak AI:
git checkout HEAD -- src/components/Header.tsx

# 3. Menghapus file-file untracked baru yang dibuat oleh AI secara tidak sengaja:
git clean -fd
```
