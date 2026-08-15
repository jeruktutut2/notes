package usecase

import (
	"context"
	"errors"

	"github.com/example/modular-monolith/internal/modules/wallet/domain"
)

// WalletUseCase mengimplementasikan business logic untuk module wallet
type WalletUseCase struct {
	walletRepo domain.WalletRepository
	txMgr      domain.TransactionManager
}

// NewWalletUseCase membuat instance baru dari WalletUseCase
func NewWalletUseCase(walletRepo domain.WalletRepository, txMgr domain.TransactionManager) *WalletUseCase {
	return &WalletUseCase{
		walletRepo: walletRepo,
		txMgr:      txMgr,
	}
}

// Transfer memindahkan saldo dari satu user ke user lain secara atomik menggunakan transaksi
func (uc *WalletUseCase) Transfer(ctx context.Context, senderID, receiverID string, amount int64) error {
	if amount <= 0 {
		return errors.New("jumlah transfer harus lebih dari 0")
	}

	// Membungkus proses penarikan dan penambahan saldo dalam satu transaksi
	return uc.txMgr.RunInTx(ctx, func(txCtx context.Context) error {
		// PENTING: Gunakan txCtx agar berjalan dalam transaksi

		// 1. Cek saldo pengirim
		senderWallet, err := uc.walletRepo.GetByUserID(txCtx, senderID)
		if err != nil {
			return err
		}
		if senderWallet.Balance < amount {
			return errors.New("saldo tidak mencukupi")
		}

		// 2. Cek eksistensi dompet penerima
		receiverWallet, err := uc.walletRepo.GetByUserID(txCtx, receiverID)
		if err != nil {
			return err
		}

		// 3. Kurangi saldo pengirim
		if err := uc.walletRepo.UpdateBalance(txCtx, senderWallet.ID, -amount); err != nil {
			return err
		}

		// 4. Tambah saldo penerima
		if err := uc.walletRepo.UpdateBalance(txCtx, receiverWallet.ID, amount); err != nil {
			return err
		}

		// Jika return nil, transaksi akan di-commit
		return nil
	})
}
