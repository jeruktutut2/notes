package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/example/modular-monolith/internal/modules/wallet/domain"
)

// dbEngine mengabstraksi fungsi query yang ada di pgx.Tx maupun pgxpool.Pool
type dbEngine interface {
	QueryRow(ctx context.Context, sql string, args ...any) pgx.Row
	Exec(ctx context.Context, sql string, arguments ...any) (pgconn.CommandTag, error)
}

// repository adalah OUTBOUND ADAPTER untuk PostgreSQL yang menerapkan domain.WalletRepository
type repository struct {
	pool *pgxpool.Pool
}

// NewRepository membuat repository dompet PostgreSQL baru
func NewRepository(pool *pgxpool.Pool) domain.WalletRepository {
	return &repository{pool: pool}
}

// getEngine mengekstrak pgx.Tx dari context jika ada, jika tidak kembalikan pool
func (r *repository) getEngine(ctx context.Context) dbEngine {
	tx, ok := ctx.Value(txKey{}).(pgx.Tx)
	if ok {
		return tx // Berjalan dalam scope transaksi
	}
	return r.pool // Berjalan secara mandiri (autocommit)
}

func (r *repository) Create(ctx context.Context, w *domain.Wallet) error {
	query := `
		INSERT INTO wallets (user_id, balance)
		VALUES ($1, $2)
		RETURNING id, created_at, updated_at`

	engine := r.getEngine(ctx)
	return engine.QueryRow(ctx, query, w.UserID, w.Balance).
		Scan(&w.ID, &w.CreatedAt, &w.UpdatedAt)
}

func (r *repository) GetByUserID(ctx context.Context, userID string) (*domain.Wallet, error) {
	query := `SELECT id, user_id, balance, created_at, updated_at FROM wallets WHERE user_id = $1`

	w := &domain.Wallet{}
	engine := r.getEngine(ctx)

	err := engine.QueryRow(ctx, query, userID).
		Scan(&w.ID, &w.UserID, &w.Balance, &w.CreatedAt, &w.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("wallet not found")
		}
		return nil, err
	}
	return w, nil
}

func (r *repository) UpdateBalance(ctx context.Context, walletID string, amount int64) error {
	query := `UPDATE wallets SET balance = balance + $1, updated_at = NOW() WHERE id = $2`

	engine := r.getEngine(ctx)
	tag, err := engine.Exec(ctx, query, amount, walletID)
	if err != nil {
		return err
	}
	if tag.RowsAffected() == 0 {
		return fmt.Errorf("wallet not found")
	}
	return nil
}
