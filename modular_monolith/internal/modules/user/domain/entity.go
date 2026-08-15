package domain

import "time"

// User represents the user domain entity.
// Domain entities are free from infrastructure concerns (no JSON tags, no DB tags).
type User struct {
	ID        string
	Name      string
	Email     string
	Password  string
	CreatedAt time.Time
	UpdatedAt time.Time
}
