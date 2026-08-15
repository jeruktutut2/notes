package models

import "time"

type Employee struct {
	ID        int        `json:"id"`
	Name      string     `json:"name"`
	Position  string     `json:"position"`
	CreatedAt *time.Time `json:"created_at,omitempty"`
	ServedBy  string     `json:"served_by,omitempty"` // MySQL @@hostname
}

type CreateEmployeeRequest struct {
	Name     string `json:"name"`
	Position string `json:"position"`
}

type TransactionRequest struct {
	Name     string `json:"name"`
	Position string `json:"position"`
}
