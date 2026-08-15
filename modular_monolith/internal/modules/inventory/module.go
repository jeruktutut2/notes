package inventory

import (
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/inventory/adapter/inbound/rest"
	"github.com/example/modular-monolith/internal/modules/inventory/adapter/outbound/postgres"
	"github.com/example/modular-monolith/internal/modules/inventory/application"
)

// RegisterRoutes wires the inventory module's hexagonal dependencies and registers routes.
func RegisterRoutes(g *echo.Group, pool *pgxpool.Pool) {
	repo := postgres.NewRepository(pool)
	svc := application.NewService(repo)
	h := rest.NewHandler(svc)

	g.POST("", h.Create)
	g.GET("", h.List)
	g.GET("/:product_id", h.GetByProductID)
	g.PUT("/:product_id/adjust", h.Adjust)
}
