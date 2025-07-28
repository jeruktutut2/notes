package modelrequests

import "github.com/google/uuid"

type UpdateRequest struct {
	Id   uuid.UUID `json:"id"`
	Test string    `json:"test"`
}
