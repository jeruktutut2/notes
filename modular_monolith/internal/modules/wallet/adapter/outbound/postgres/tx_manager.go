package postgres

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/example/modular-monolith/internal/modules/wallet/domain"
)

// txKey digunakan agar tidak terjadi tabrakan nama di dalam context
type txKey struct{}

// txManager implementasi dari domain.TransactionManager untuk PostgreSQL
type txManager struct {
	pool *pgxpool.Pool
}

// NewTransactionManager membuat instance baru dari txManager
func NewTransactionManager(pool *pgxpool.Pool) domain.TransactionManager {
	return &txManager{pool: pool}
}

// RunInTx menjalankan fungsi fn di dalam sebuah database transaction (pgx.Tx).
// Objek pgx.Tx disisipkan ke dalam context agar bisa diambil oleh repository.
func (tm *txManager) RunInTx(ctx context.Context, fn func(ctx context.Context) error) error {
	tx, err := tm.pool.Begin(ctx)
	if err != nil {
		return err
	}

	// Buat context baru turunan dari ctx, berisi objek tx
	txCtx := context.WithValue(ctx, txKey{}, tx)

	// Jalankan bisnis logik
	err = fn(txCtx)
	if err != nil {
		// Rollback jika ada error
		_ = tx.Rollback(ctx)
		return err
	}

	// Commit jika tidak ada error
	return tx.Commit(ctx)
}
