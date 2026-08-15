package user

import (
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/user/adapter/inbound/rest"
	"github.com/example/modular-monolith/internal/modules/user/adapter/outbound/postgres"
	"github.com/example/modular-monolith/internal/modules/user/application"
)

// RegisterRoutes wires the user module's hexagonal dependencies and registers routes.
//
// Wiring (composition root):
//
//	PostgreSQL Adapter (outbound) → implements domain.UserRepository
//	Application Service           → implements domain.UserService, depends on domain.UserRepository
//	REST Handler (inbound)        → depends on domain.UserService
func RegisterRoutes(g *echo.Group, pool *pgxpool.Pool) {
	// Outbound adapter: PostgreSQL repository
	repo := postgres.NewRepository(pool)

	// Application service: business logic
	svc := application.NewService(repo)

	// Inbound adapter: HTTP handler
	h := rest.NewHandler(svc)

	g.POST("", h.Create)
	g.GET("", h.List)
	g.GET("/:id", h.GetByID)
	g.PUT("/:id", h.Update)
	g.DELETE("/:id", h.Delete)
	g.POST("/login", h.Login)
}
