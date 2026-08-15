package repository

import (
	"context"
	"fmt"

	"echo-otel-demo/internal/model"

	"github.com/jackc/pgx/v5/pgxpool"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
)

var tracer = otel.Tracer("repository")

type UserRepository interface {
	GetAll(ctx context.Context) ([]model.User, error)
	GetByID(ctx context.Context, id string) (*model.User, error)
	Create(ctx context.Context, req model.CreateUserRequest) (*model.User, error)
	Update(ctx context.Context, id string, req model.UpdateUserRequest) (*model.User, error)
	Delete(ctx context.Context, id string) error
}

type userRepository struct {
	pool *pgxpool.Pool
}

func NewUserRepository(pool *pgxpool.Pool) UserRepository {
	return &userRepository{pool: pool}
}

func (r *userRepository) GetAll(ctx context.Context) ([]model.User, error) {
	ctx, span := tracer.Start(ctx, "UserRepository.GetAll")
	defer span.End()

	rows, err := r.pool.Query(ctx,
		"SELECT id, name, email, created_at, updated_at FROM users ORDER BY created_at DESC",
	)
	if err != nil {
		return nil, fmt.Errorf("query users: %w", err)
	}
	defer rows.Close()

	var users []model.User
	for rows.Next() {
		var u model.User
		if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.CreatedAt, &u.UpdatedAt); err != nil {
			return nil, fmt.Errorf("scan user: %w", err)
		}
		users = append(users, u)
	}

	span.SetAttributes(attribute.Int("users.count", len(users)))
	return users, nil
}

func (r *userRepository) GetByID(ctx context.Context, id string) (*model.User, error) {
	ctx, span := tracer.Start(ctx, "UserRepository.GetByID")
	defer span.End()
	span.SetAttributes(attribute.String("user.id", id))

	var u model.User
	err := r.pool.QueryRow(ctx,
		"SELECT id, name, email, created_at, updated_at FROM users WHERE id = $1", id,
	).Scan(&u.ID, &u.Name, &u.Email, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("query user by id: %w", err)
	}
	return &u, nil
}

func (r *userRepository) Create(ctx context.Context, req model.CreateUserRequest) (*model.User, error) {
	ctx, span := tracer.Start(ctx, "UserRepository.Create")
	defer span.End()
	span.SetAttributes(attribute.String("user.email", req.Email))

	var u model.User
	err := r.pool.QueryRow(ctx,
		"INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email, created_at, updated_at",
		req.Name, req.Email,
	).Scan(&u.ID, &u.Name, &u.Email, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("insert user: %w", err)
	}
	return &u, nil
}

func (r *userRepository) Update(ctx context.Context, id string, req model.UpdateUserRequest) (*model.User, error) {
	ctx, span := tracer.Start(ctx, "UserRepository.Update")
	defer span.End()
	span.SetAttributes(attribute.String("user.id", id))

	var u model.User
	err := r.pool.QueryRow(ctx,
		"UPDATE users SET name = $1, email = $2, updated_at = NOW() WHERE id = $3 RETURNING id, name, email, created_at, updated_at",
		req.Name, req.Email, id,
	).Scan(&u.ID, &u.Name, &u.Email, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("update user: %w", err)
	}
	return &u, nil
}

func (r *userRepository) Delete(ctx context.Context, id string) error {
	ctx, span := tracer.Start(ctx, "UserRepository.Delete")
	defer span.End()
	span.SetAttributes(attribute.String("user.id", id))

	result, err := r.pool.Exec(ctx, "DELETE FROM users WHERE id = $1", id)
	if err != nil {
		return fmt.Errorf("delete user: %w", err)
	}
	if result.RowsAffected() == 0 {
		return fmt.Errorf("user not found: %s", id)
	}
	return nil
}
