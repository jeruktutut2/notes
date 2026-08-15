package repository

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/bsa/migration/internal/model"
)

// UserRepository mengelola operasi database untuk entitas User.
type UserRepository struct {
	pool *pgxpool.Pool
}

// NewUserRepository membuat UserRepository baru.
func NewUserRepository(pool *pgxpool.Pool) *UserRepository {
	return &UserRepository{pool: pool}
}

// GetAll mengembalikan semua user dari database.
func (r *UserRepository) GetAll(ctx context.Context) ([]*model.User, error) {
	query := `
		SELECT id, username, full_name, email, phone_number, is_active, created_at, updated_at
		FROM users
		ORDER BY id ASC
	`

	rows, err := r.pool.Query(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("gagal query users: %w", err)
	}
	defer rows.Close()

	var users []*model.User
	for rows.Next() {
		u := &model.User{}
		err := rows.Scan(
			&u.ID, &u.Username, &u.FullName, &u.Email,
			&u.PhoneNumber, &u.IsActive, &u.CreatedAt, &u.UpdatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("gagal scan user: %w", err)
		}
		users = append(users, u)
	}

	return users, rows.Err()
}

// GetByID mengembalikan user berdasarkan ID.
func (r *UserRepository) GetByID(ctx context.Context, id int64) (*model.User, error) {
	query := `
		SELECT id, username, full_name, email, phone_number, is_active, created_at, updated_at
		FROM users
		WHERE id = $1
	`

	u := &model.User{}
	err := r.pool.QueryRow(ctx, query, id).Scan(
		&u.ID, &u.Username, &u.FullName, &u.Email,
		&u.PhoneNumber, &u.IsActive, &u.CreatedAt, &u.UpdatedAt,
	)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("user dengan ID %d tidak ditemukan", id)
		}
		return nil, fmt.Errorf("gagal query user: %w", err)
	}

	return u, nil
}

// Create membuat user baru di database.
func (r *UserRepository) Create(ctx context.Context, req *model.CreateUserRequest) (*model.User, error) {
	query := `
		INSERT INTO users (username, full_name, email, phone_number, password)
		VALUES ($1, $2, $3, $4, $5)
		RETURNING id, username, full_name, email, phone_number, is_active, created_at, updated_at
	`

	u := &model.User{}
	err := r.pool.QueryRow(ctx, query,
		req.Username, req.FullName, req.Email, req.PhoneNumber, req.Password,
	).Scan(
		&u.ID, &u.Username, &u.FullName, &u.Email,
		&u.PhoneNumber, &u.IsActive, &u.CreatedAt, &u.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("gagal membuat user: %w", err)
	}

	return u, nil
}

// Update mengupdate data user yang sudah ada.
func (r *UserRepository) Update(ctx context.Context, id int64, req *model.UpdateUserRequest) (*model.User, error) {
	// Ambil data user yang ada dulu
	existing, err := r.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update field yang dikirim
	if req.FullName != "" {
		existing.FullName = req.FullName
	}
	if req.Email != "" {
		existing.Email = req.Email
	}
	if req.PhoneNumber != "" {
		existing.PhoneNumber = req.PhoneNumber
	}
	if req.IsActive != nil {
		existing.IsActive = *req.IsActive
	}

	query := `
		UPDATE users
		SET full_name = $2, email = $3, phone_number = $4, is_active = $5, updated_at = $6
		WHERE id = $1
		RETURNING id, username, full_name, email, phone_number, is_active, created_at, updated_at
	`

	u := &model.User{}
	err = r.pool.QueryRow(ctx, query,
		id, existing.FullName, existing.Email, existing.PhoneNumber, existing.IsActive, time.Now(),
	).Scan(
		&u.ID, &u.Username, &u.FullName, &u.Email,
		&u.PhoneNumber, &u.IsActive, &u.CreatedAt, &u.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("gagal mengupdate user: %w", err)
	}

	return u, nil
}

// Delete menghapus user berdasarkan ID.
func (r *UserRepository) Delete(ctx context.Context, id int64) error {
	query := `DELETE FROM users WHERE id = $1`

	result, err := r.pool.Exec(ctx, query, id)
	if err != nil {
		return fmt.Errorf("gagal menghapus user: %w", err)
	}

	if result.RowsAffected() == 0 {
		return fmt.Errorf("user dengan ID %d tidak ditemukan", id)
	}

	return nil
}
