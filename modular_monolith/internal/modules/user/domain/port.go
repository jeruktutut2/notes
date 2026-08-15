package domain

import "context"

// UserRepository is the OUTBOUND PORT for user data persistence.
// Implemented by adapters (e.g., PostgreSQL adapter).
// Defined in domain so that the application service can depend on it
// without knowing the concrete implementation.
type UserRepository interface {
	Create(ctx context.Context, u *User) error
	GetByID(ctx context.Context, id string) (*User, error)
	GetByEmail(ctx context.Context, email string) (*User, error)
	List(ctx context.Context, limit, offset int) ([]*User, int64, error)
	Update(ctx context.Context, u *User) error
	Delete(ctx context.Context, id string) error
}

// UserService is the INBOUND PORT defining use cases for the user domain.
// Implemented by the application service layer.
// Used by inbound adapters (e.g., HTTP handler) to interact with the domain.
type UserService interface {
	Create(ctx context.Context, name, email, password string) (*User, error)
	GetByID(ctx context.Context, id string) (*User, error)
	List(ctx context.Context, page, limit int) ([]*User, int64, error)
	Update(ctx context.Context, id, name, email string) (*User, error)
	Delete(ctx context.Context, id string) error
	Login(ctx context.Context, email, password string) (*User, string, error)
}
