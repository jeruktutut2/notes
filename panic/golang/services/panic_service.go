package services

import "context"

type PanicService interface {
	CheckPanic(ctx context.Context) string
}

type panicService struct {
}

func NewPanicService() PanicService {
	return &panicService{}
}

func (service *panicService) CheckPanic(ctx context.Context) string {
	panic("test panic")
}
