package modelrequests

import "github.com/google/uuid"

type DeleteRequest struct {
	Id uuid.UUID `json:"id"`
}
