package model

import "time"

// User merepresentasikan entitas user dalam database.
type User struct {
	ID          int64     `json:"id"`
	Username    string    `json:"username"`
	FullName    string    `json:"full_name"`
	Email       string    `json:"email,omitempty"`
	PhoneNumber string    `json:"phone_number,omitempty"`
	Password    string    `json:"-"` // Tidak pernah di-return ke client
	IsActive    bool      `json:"is_active"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// CreateUserRequest adalah request body untuk membuat user baru.
type CreateUserRequest struct {
	Username    string `json:"username" validate:"required,min=3,max=100"`
	FullName    string `json:"full_name" validate:"required"`
	Email       string `json:"email" validate:"required,email"`
	PhoneNumber string `json:"phone_number,omitempty"`
	Password    string `json:"password" validate:"required,min=6"`
}

// UpdateUserRequest adalah request body untuk mengupdate user.
type UpdateUserRequest struct {
	FullName    string `json:"full_name,omitempty"`
	Email       string `json:"email,omitempty"`
	PhoneNumber string `json:"phone_number,omitempty"`
	IsActive    *bool  `json:"is_active,omitempty"`
}

// UserResponse adalah response yang dikirim ke client.
type UserResponse struct {
	ID          int64     `json:"id"`
	Username    string    `json:"username"`
	FullName    string    `json:"full_name"`
	Email       string    `json:"email"`
	PhoneNumber string    `json:"phone_number"`
	IsActive    bool      `json:"is_active"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// ToResponse mengkonversi User model ke UserResponse.
func (u *User) ToResponse() *UserResponse {
	return &UserResponse{
		ID:          u.ID,
		Username:    u.Username,
		FullName:    u.FullName,
		Email:       u.Email,
		PhoneNumber: u.PhoneNumber,
		IsActive:    u.IsActive,
		CreatedAt:   u.CreatedAt,
		UpdatedAt:   u.UpdatedAt,
	}
}
