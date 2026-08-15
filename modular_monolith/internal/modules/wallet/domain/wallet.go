package domain

import (
	"context"
	"time"
)

// Wallet merepresentasikan entitas dompet digital
type Wallet struct {
	ID        string
	UserID    string
	Balance   int64
	CreatedAt time.Time
	UpdatedAt time.Time
}

// WalletRepository adalah port outbound untuk operasi database dompet
type WalletRepository interface {
	Create(ctx context.Context, w *Wallet) error
	GetByUserID(ctx context.Context, userID string) (*Wallet, error)
	UpdateBalance(ctx context.Context, walletID string, amount int64) error
}

// TransactionManager adalah port outbound untuk mengatur lifecycle transaksi
type TransactionManager interface {
	RunInTx(ctx context.Context, fn func(txCtx context.Context) error) error
}
