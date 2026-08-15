package service

import (
	"context"
	"errors"
	"fmt"
	"time"

	"distributed_lock/internal/lock"

	"github.com/jmoiron/sqlx"
)

var (
	ErrLockAcquireFailed = errors.New("gagal mendapatkan distributed lock, silakan coba beberapa saat lagi")
	ErrInsufficientFunds = errors.New("saldo tidak mencukupi")
)

type WalletService struct {
	db        *sqlx.DB
	redisLock *lock.RedisLockManager
	pgLock    *lock.PGLockManager
}

func NewWalletService(db *sqlx.DB, redisLock *lock.RedisLockManager, pgLock *lock.PGLockManager) *WalletService {
	return &WalletService{
		db:        db,
		redisLock: redisLock,
		pgLock:    pgLock,
	}
}

// InitSchema membuat tabel accounts jika belum ada
func (w *WalletService) InitSchema(ctx context.Context) error {
	schema := `
	CREATE TABLE IF NOT EXISTS accounts (
		id INT PRIMARY KEY,
		balance NUMERIC(15, 2) NOT NULL DEFAULT 0.00
	);`
	_, err := w.db.ExecContext(ctx, schema)
	return err
}

// ResetBalance mereset saldo akun ke nilai awal
func (w *WalletService) ResetBalance(ctx context.Context, accountID int, initialBalance float64) error {
	query := `
	INSERT INTO accounts (id, balance) 
	VALUES ($1, $2)
	ON CONFLICT (id) DO UPDATE SET balance = $2;`
	_, err := w.db.ExecContext(ctx, query, accountID, initialBalance)
	return err
}

// GetBalance mengambil saldo saat ini
func (w *WalletService) GetBalance(ctx context.Context, accountID int) (float64, error) {
	var balance float64
	err := w.db.GetContext(ctx, &balance, "SELECT balance FROM accounts WHERE id = $1", accountID)
	return balance, err
}

// 1. WithdrawNoLock: TANPA LOCKING (Simulasi Race Condition)
func (w *WalletService) WithdrawNoLock(ctx context.Context, accountID int, amount float64) (float64, error) {
	var balance float64
	err := w.db.GetContext(ctx, &balance, "SELECT balance FROM accounts WHERE id = $1", accountID)
	if err != nil {
		return 0, err
	}

	if balance < amount {
		return balance, ErrInsufficientFunds
	}

	// Simulasi delay I/O untuk memperbesar gap race condition
	time.Sleep(50 * time.Millisecond)

	newBalance := balance - amount
	_, err = w.db.ExecContext(ctx, "UPDATE accounts SET balance = $1 WHERE id = $2", newBalance, accountID)
	if err != nil {
		return 0, err
	}

	return newBalance, nil
}

// 2. WithdrawRedisLock: DENGAN REDIS LOCK + CONTEXT TIMEOUT PROTECTION (Proteksi 0.1%)
func (w *WalletService) WithdrawRedisLock(ctx context.Context, accountID int, amount float64) (float64, error) {
	ttl := 5 * time.Second
	lockKey := fmt.Sprintf("lock:account:%d", accountID)

	token, acquired, err := w.redisLock.AcquireLock(ctx, lockKey, ttl)
	if err != nil {
		return 0, err
	}
	if !acquired {
		return 0, ErrLockAcquireFailed
	}
	defer w.redisLock.ReleaseLock(ctx, lockKey, token)

	// PROTEKSI 0.1%: Context Timeout diset 4 detik (< 5s TTL Redis).
	// Jika query DB macet / lebih lama dari 4 detik, Go membatalkan transaksi otomatis sebelum TTL habis!
	execCtx, cancel := context.WithTimeout(ctx, 4*time.Second)
	defer cancel()

	var balance float64
	err = w.db.GetContext(execCtx, &balance, "SELECT balance FROM accounts WHERE id = $1", accountID)
	if err != nil {
		return 0, err
	}

	if balance < amount {
		return balance, ErrInsufficientFunds
	}

	time.Sleep(50 * time.Millisecond) // Jeda aman karena locked

	newBalance := balance - amount
	_, err = w.db.ExecContext(execCtx, "UPDATE accounts SET balance = $1 WHERE id = $2", newBalance, accountID)
	if err != nil {
		return 0, err
	}

	return newBalance, nil
}

// 2b. WithdrawRedisWatchdogLock: DENGAN REDIS WATCHDOG (AUTO-RENEWAL TTL HEARTBEAT)
func (w *WalletService) WithdrawRedisWatchdogLock(ctx context.Context, accountID int, amount float64) (float64, error) {
	ttl := 5 * time.Second
	lockKey := fmt.Sprintf("lock:account:%d", accountID)

	// Menggunakan Watchdog yang memperpanjang TTL kunci tiap ~1.6 detik secara berkala
	guard, acquired, err := w.redisLock.AcquireLockWithWatchdog(ctx, lockKey, ttl)
	if err != nil {
		return 0, err
	}
	if !acquired {
		return 0, ErrLockAcquireFailed
	}
	defer guard.Release(ctx)

	execCtx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()

	var balance float64
	err = w.db.GetContext(execCtx, &balance, "SELECT balance FROM accounts WHERE id = $1", accountID)
	if err != nil {
		return 0, err
	}

	if balance < amount {
		return balance, ErrInsufficientFunds
	}

	time.Sleep(50 * time.Millisecond)

	newBalance := balance - amount
	_, err = w.db.ExecContext(execCtx, "UPDATE accounts SET balance = $1 WHERE id = $2", newBalance, accountID)
	if err != nil {
		return 0, err
	}

	return newBalance, nil
}

// 3. WithdrawPGSessionLock: DENGAN POSTGRESQL SESSION ADVISORY LOCK
func (w *WalletService) WithdrawPGSessionLock(ctx context.Context, accountID int, amount float64) (float64, error) {
	lockKey := fmt.Sprintf("lock:account:%d", accountID)
	sessionLock, acquired, err := w.pgLock.AcquireSessionLock(ctx, lockKey)
	if err != nil {
		return 0, err
	}
	if !acquired {
		return 0, ErrLockAcquireFailed
	}
	defer sessionLock.Release(ctx)

	var balance float64
	err = w.db.GetContext(ctx, &balance, "SELECT balance FROM accounts WHERE id = $1", accountID)
	if err != nil {
		return 0, err
	}

	if balance < amount {
		return balance, ErrInsufficientFunds
	}

	time.Sleep(50 * time.Millisecond)

	newBalance := balance - amount
	_, err = w.db.ExecContext(ctx, "UPDATE accounts SET balance = $1 WHERE id = $2", newBalance, accountID)
	if err != nil {
		return 0, err
	}

	return newBalance, nil
}

// 4. WithdrawPGTxLock: DENGAN POSTGRESQL TRANSACTION ADVISORY LOCK
func (w *WalletService) WithdrawPGTxLock(ctx context.Context, accountID int, amount float64) (float64, error) {
	tx, err := w.db.BeginTxx(ctx, nil)
	if err != nil {
		return 0, err
	}
	defer tx.Rollback()

	lockKey := fmt.Sprintf("lock:account:%d", accountID)
	acquired, err := w.pgLock.AcquireTxLock(ctx, tx, lockKey)
	if err != nil {
		return 0, err
	}
	if !acquired {
		return 0, ErrLockAcquireFailed
	}

	var balance float64
	err = tx.GetContext(ctx, &balance, "SELECT balance FROM accounts WHERE id = $1", accountID)
	if err != nil {
		return 0, err
	}

	if balance < amount {
		return balance, ErrInsufficientFunds
	}

	time.Sleep(50 * time.Millisecond)

	newBalance := balance - amount
	_, err = tx.ExecContext(ctx, "UPDATE accounts SET balance = $1 WHERE id = $2", newBalance, accountID)
	if err != nil {
		return 0, err
	}

	if err := tx.Commit(); err != nil {
		return 0, err
	}

	return newBalance, nil
}
