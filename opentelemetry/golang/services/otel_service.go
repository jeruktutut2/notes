package services

import (
	"context"
	"time"
)

type OtelService interface {
	SetSpan(ctx context.Context) string
}

type otelService struct {
}

func NewOtelService() OtelService {
	return &otelService{}
}

func (service *otelService) SetSpan(ctx context.Context) string {
	time.Sleep(3 * time.Second)
	return "success"
}
