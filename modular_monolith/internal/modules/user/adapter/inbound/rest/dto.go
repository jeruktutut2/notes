package rest

import (
	"time"

	"github.com/example/modular-monolith/internal/modules/user/domain"
)

// --- Request DTOs (inbound adapter concern) ---

// CreateUserRequest is the HTTP request DTO for creating a user.
type CreateUserRequest struct {
	Name     string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

// Validate checks required fields.
func (r *CreateUserRequest) Validate() string {
	if r.Name == "" {
		return "name is required"
	}
	if r.Email == "" {
		return "email is required"
	}
	if r.Password == "" {
		return "password is required"
	}
	return ""
}

// UpdateUserRequest is the HTTP request DTO for updating a user.
type UpdateUserRequest struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

// LoginRequest is the HTTP request DTO for user login.
type LoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

// --- Response DTOs (inbound adapter concern) ---

// UserResponse is the HTTP response DTO for a user.
// Maps from domain.User, excluding sensitive fields like Password.
type UserResponse struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// LoginResponse is the HTTP response DTO for login.
type LoginResponse struct {
	User  *UserResponse `json:"user"`
	Token string        `json:"token"`
}

// --- Mapping functions: Domain → Response DTO ---

func toUserResponse(u *domain.User) *UserResponse {
	if u == nil {
		return nil
	}
	return &UserResponse{
		ID:        u.ID,
		Name:      u.Name,
		Email:     u.Email,
		CreatedAt: u.CreatedAt,
		UpdatedAt: u.UpdatedAt,
	}
}

func toUserListResponse(users []*domain.User) []*UserResponse {
	result := make([]*UserResponse, len(users))
	for i, u := range users {
		result[i] = toUserResponse(u)
	}
	return result
}
