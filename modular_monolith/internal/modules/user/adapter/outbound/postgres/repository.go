package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/example/modular-monolith/internal/modules/user/domain"
)

// repository is the OUTBOUND ADAPTER for PostgreSQL.
// It implements domain.UserRepository (outbound port).
type repository struct {
	pool *pgxpool.Pool
}

// NewRepository creates a new PostgreSQL user repository.
// Returns domain.UserRepository interface to enforce port abstraction.
func NewRepository(pool *pgxpool.Pool) domain.UserRepository {
	return &repository{pool: pool}
}

func (r *repository) Create(ctx context.Context, u *domain.User) error {
	query := `
		INSERT INTO users (name, email, password)
		VALUES ($1, $2, $3)
		RETURNING id, created_at, updated_at`

	return r.pool.QueryRow(ctx, query, u.Name, u.Email, u.Password).
		Scan(&u.ID, &u.CreatedAt, &u.UpdatedAt)
}

func (r *repository) GetByID(ctx context.Context, id string) (*domain.User, error) {
	query := `SELECT id, name, email, password, created_at, updated_at FROM users WHERE id = $1`

	u := &domain.User{}
	err := r.pool.QueryRow(ctx, query, id).
		Scan(&u.ID, &u.Name, &u.Email, &u.Password, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("user not found")
		}
		return nil, err
	}
	return u, nil
}

func (r *repository) GetByEmail(ctx context.Context, email string) (*domain.User, error) {
	query := `SELECT id, name, email, password, created_at, updated_at FROM users WHERE email = $1`

	u := &domain.User{}
	err := r.pool.QueryRow(ctx, query, email).
		Scan(&u.ID, &u.Name, &u.Email, &u.Password, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("user not found")
		}
		return nil, err
	}
	return u, nil
}

func (r *repository) List(ctx context.Context, limit, offset int) ([]*domain.User, int64, error) {
	// Count total.
	var total int64
	err := r.pool.QueryRow(ctx, `SELECT COUNT(*) FROM users`).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	query := `SELECT id, name, email, password, created_at, updated_at FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2`
	rows, err := r.pool.Query(ctx, query, limit, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var users []*domain.User
	for rows.Next() {
		u := &domain.User{}
		if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.Password, &u.CreatedAt, &u.UpdatedAt); err != nil {
			return nil, 0, err
		}
		users = append(users, u)
	}
	return users, total, rows.Err()
}

func (r *repository) Update(ctx context.Context, u *domain.User) error {
	query := `
		UPDATE users SET name = $1, email = $2, updated_at = NOW()
		WHERE id = $3
		RETURNING updated_at`

	return r.pool.QueryRow(ctx, query, u.Name, u.Email, u.ID).Scan(&u.UpdatedAt)
}

func (r *repository) Delete(ctx context.Context, id string) error {
	result, err := r.pool.Exec(ctx, `DELETE FROM users WHERE id = $1`, id)
	if err != nil {
		return err
	}
	if result.RowsAffected() == 0 {
		return fmt.Errorf("user not found")
	}
	return nil
}
