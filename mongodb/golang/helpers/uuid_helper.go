package helpers

import "github.com/google/uuid"

type UuidHelper interface {
	GenerateUuidV7() (string, error)
}

type uuidHelper struct {
}

func NewUuidHelper() UuidHelper {
	return &uuidHelper{}
}

func (helper *uuidHelper) GenerateUuidV7() (string, error) {
	uuid, err := uuid.NewV7()
	if err != nil {
		return "", err
	}
	return uuid.String(), nil
}
