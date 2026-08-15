package application

import (
	"context"
	"fmt"

	"go.opentelemetry.io/otel"

	"github.com/example/modular-monolith/internal/modules/notification/domain"
)

var tracer = otel.Tracer("module.notification")

type service struct {
	repo domain.NotificationRepository
}

func NewService(repo domain.NotificationRepository) domain.NotificationService {
	return &service{repo: repo}
}

func (s *service) Create(ctx context.Context, userID, title, message string) (*domain.Notification, error) {
	ctx, span := tracer.Start(ctx, "NotificationService.Create")
	defer span.End()

	n := &domain.Notification{
		UserID:  userID,
		Title:   title,
		Message: message,
	}

	if err := s.repo.Create(ctx, n); err != nil {
		return nil, fmt.Errorf("failed to create notification: %w", err)
	}
	return n, nil
}

func (s *service) GetByID(ctx context.Context, id string) (*domain.Notification, error) {
	ctx, span := tracer.Start(ctx, "NotificationService.GetByID")
	defer span.End()

	return s.repo.GetByID(ctx, id)
}

func (s *service) ListByUser(ctx context.Context, userID string, page, limit int) ([]*domain.Notification, int64, error) {
	ctx, span := tracer.Start(ctx, "NotificationService.ListByUser")
	defer span.End()

	if page < 1 {
		page = 1
	}
	if limit < 1 || limit > 100 {
		limit = 10
	}
	offset := (page - 1) * limit
	return s.repo.ListByUser(ctx, userID, limit, offset)
}

func (s *service) MarkAsRead(ctx context.Context, id string) error {
	ctx, span := tracer.Start(ctx, "NotificationService.MarkAsRead")
	defer span.End()

	return s.repo.MarkAsRead(ctx, id)
}
