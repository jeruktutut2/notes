package notification

import (
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/notification/adapter/inbound/rest"
	"github.com/example/modular-monolith/internal/modules/notification/adapter/outbound/postgres"
	"github.com/example/modular-monolith/internal/modules/notification/application"
)

// RegisterRoutes wires the notification module's hexagonal dependencies and registers routes.
func RegisterRoutes(g *echo.Group, pool *pgxpool.Pool) {
	repo := postgres.NewRepository(pool)
	svc := application.NewService(repo)
	h := rest.NewHandler(svc)

	g.POST("", h.Create)
	g.GET("", h.List)
	g.GET("/:id", h.GetByID)
	g.PUT("/:id/read", h.MarkAsRead)
}
