package application

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"

	"go.opentelemetry.io/otel"

	"github.com/example/modular-monolith/internal/modules/user/domain"
)

var tracer = otel.Tracer("module.user")

// service implements domain.UserService (inbound port).
// It depends on domain.UserRepository (outbound port), not on a concrete implementation.
type service struct {
	repo domain.UserRepository
}

// NewService creates a new user application service.
// Returns domain.UserService interface to enforce port abstraction.
func NewService(repo domain.UserRepository) domain.UserService {
	return &service{repo: repo}
}

// Create creates a new user with hashed password.
func (s *service) Create(ctx context.Context, name, email, password string) (*domain.User, error) {
	ctx, span := tracer.Start(ctx, "UserService.Create")
	defer span.End()

	u := &domain.User{
		Name:     name,
		Email:    email,
		Password: hashPassword(password),
	}

	if err := s.repo.Create(ctx, u); err != nil {
		return nil, fmt.Errorf("failed to create user: %w", err)
	}
	return u, nil
}

// GetByID retrieves a user by ID.
func (s *service) GetByID(ctx context.Context, id string) (*domain.User, error) {
	ctx, span := tracer.Start(ctx, "UserService.GetByID")
	defer span.End()

	return s.repo.GetByID(ctx, id)
}

// List retrieves a paginated list of users.
func (s *service) List(ctx context.Context, page, limit int) ([]*domain.User, int64, error) {
	ctx, span := tracer.Start(ctx, "UserService.List")
	defer span.End()

	if page < 1 {
		page = 1
	}
	if limit < 1 || limit > 100 {
		limit = 10
	}
	offset := (page - 1) * limit
	return s.repo.List(ctx, limit, offset)
}

// Update updates user information.
func (s *service) Update(ctx context.Context, id, name, email string) (*domain.User, error) {
	ctx, span := tracer.Start(ctx, "UserService.Update")
	defer span.End()

	u, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	if name != "" {
		u.Name = name
	}
	if email != "" {
		u.Email = email
	}

	if err := s.repo.Update(ctx, u); err != nil {
		return nil, fmt.Errorf("failed to update user: %w", err)
	}
	return u, nil
}

// Delete removes a user.
func (s *service) Delete(ctx context.Context, id string) error {
	ctx, span := tracer.Start(ctx, "UserService.Delete")
	defer span.End()

	return s.repo.Delete(ctx, id)
}

// Login validates user credentials and returns user with a demo token.
func (s *service) Login(ctx context.Context, email, password string) (*domain.User, string, error) {
	ctx, span := tracer.Start(ctx, "UserService.Login")
	defer span.End()

	u, err := s.repo.GetByEmail(ctx, email)
	if err != nil {
		return nil, "", fmt.Errorf("invalid credentials")
	}

	if u.Password != hashPassword(password) {
		return nil, "", fmt.Errorf("invalid credentials")
	}

	// In production, generate a proper JWT here.
	token := "demo-token-" + u.ID
	return u, token, nil
}

// hashPassword creates a simple SHA-256 hash. Use bcrypt in production.
func hashPassword(password string) string {
	h := sha256.Sum256([]byte(password))
	return hex.EncodeToString(h[:])
}
