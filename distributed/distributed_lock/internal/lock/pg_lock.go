package lock

import (
	"context"
	"database/sql"
	"hash/fnv"

	"github.com/jmoiron/sqlx"
)

type PGLockManager struct {
	db *sqlx.DB
}

func NewPGLockManager(db *sqlx.DB) *PGLockManager {
	return &PGLockManager{db: db}
}

// StringToBigIntHash mengkonversi key string menjadi int64 menggunakan FNV-1a hash
// karena PostgreSQL pg_try_advisory_lock menerima parameter BIGINT (int64).
func StringToBigIntHash(key string) int64 {
	h := fnv.New64a()
	h.Write([]byte(key))
	return int64(h.Sum64())
}

// SessionLockConn membungkus koneksi khusus untuk Session Advisory Lock
type SessionLockConn struct {
	conn   *sql.Conn
	lockID int64
}

// AcquireSessionLock mengambil penguncian level Session pada koneksi DB dedicated
func (p *PGLockManager) AcquireSessionLock(ctx context.Context, key string) (*SessionLockConn, bool, error) {
	conn, err := p.db.Conn(ctx)
	if err != nil {
		return nil, false, err
	}

	lockID := StringToBigIntHash(key)

	var locked bool
	err = conn.QueryRowContext(ctx, "SELECT pg_try_advisory_lock($1)", lockID).Scan(&locked)
	if err != nil {
		conn.Close()
		return nil, false, err
	}

	if !locked {
		conn.Close()
		return nil, false, nil
	}

	return &SessionLockConn{
		conn:   conn,
		lockID: lockID,
	}, true, nil
}

// Release melepaskan session advisory lock dan mengembalikan koneksi ke pool
func (s *SessionLockConn) Release(ctx context.Context) error {
	defer s.conn.Close()
	var unlocked bool
	err := s.conn.QueryRowContext(ctx, "SELECT pg_advisory_unlock($1)", s.lockID).Scan(&unlocked)
	return err
}

// AcquireTxLock mengambil penguncian level Transaksi di dalam *sqlx.Tx
func (p *PGLockManager) AcquireTxLock(ctx context.Context, tx *sqlx.Tx, key string) (bool, error) {
	lockID := StringToBigIntHash(key)
	var locked bool
	err := tx.QueryRowContext(ctx, "SELECT pg_try_advisory_xact_lock($1)", lockID).Scan(&locked)
	if err != nil {
		return false, err
	}
	return locked, nil
}
