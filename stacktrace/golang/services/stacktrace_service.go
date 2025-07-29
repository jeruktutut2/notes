package services

import (
	"context"
	"errors"
	"note-golang-stacktrace/helpers"
)

type Service interface {
	CheckStacktrace(ctx context.Context) string
}

type service struct {
}

func NewService() Service {
	return &service{}
}

func (service *service) CheckStacktrace(ctx context.Context) string {
	err := errors.New("error")
	requestId := "requestId"
	helpers.PrintLogToTerminal(err, requestId)
	return "check stacktrace"
}
