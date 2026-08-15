package handler

import (
	"net/http"

	"echo-otel-demo/internal/model"
	"echo-otel-demo/internal/repository"

	"github.com/labstack/echo/v5"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
)

var tracer = otel.Tracer("handler")

type UserHandler struct {
	repo repository.UserRepository
}

func NewUserHandler(repo repository.UserRepository) *UserHandler {
	return &UserHandler{repo: repo}
}

// GetAllUsers godoc
// GET /api/v1/users
func (h *UserHandler) GetAllUsers(c *echo.Context) error {
	ctx, span := tracer.Start(c.Request().Context(), "Handler.GetAllUsers")
	defer span.End()

	users, err := h.repo.GetAll(ctx)
	if err != nil {
		span.RecordError(err)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"data":  users,
		"total": len(users),
	})
}

// GetUserByID godoc
// GET /api/v1/users/:id
func (h *UserHandler) GetUserByID(c *echo.Context) error {
	id := c.Param("id")

	ctx, span := tracer.Start(c.Request().Context(), "Handler.GetUserByID")
	defer span.End()
	span.SetAttributes(attribute.String("user.id", id))

	user, err := h.repo.GetByID(ctx, id)
	if err != nil {
		span.RecordError(err)
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": "user not found",
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"data": user,
	})
}

// CreateUser godoc
// POST /api/v1/users
func (h *UserHandler) CreateUser(c *echo.Context) error {
	var req model.CreateUserRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "invalid request body",
		})
	}

	ctx, span := tracer.Start(c.Request().Context(), "Handler.CreateUser")
	defer span.End()

	user, err := h.repo.Create(ctx, req)
	if err != nil {
		span.RecordError(err)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
	}

	return c.JSON(http.StatusCreated, map[string]interface{}{
		"data": user,
	})
}

// UpdateUser godoc
// PUT /api/v1/users/:id
func (h *UserHandler) UpdateUser(c *echo.Context) error {
	id := c.Param("id")

	var req model.UpdateUserRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "invalid request body",
		})
	}

	ctx, span := tracer.Start(c.Request().Context(), "Handler.UpdateUser")
	defer span.End()
	span.SetAttributes(attribute.String("user.id", id))

	user, err := h.repo.Update(ctx, id, req)
	if err != nil {
		span.RecordError(err)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"data": user,
	})
}

// DeleteUser godoc
// DELETE /api/v1/users/:id
func (h *UserHandler) DeleteUser(c *echo.Context) error {
	id := c.Param("id")

	ctx, span := tracer.Start(c.Request().Context(), "Handler.DeleteUser")
	defer span.End()
	span.SetAttributes(attribute.String("user.id", id))

	if err := h.repo.Delete(ctx, id); err != nil {
		span.RecordError(err)
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": "user not found",
		})
	}

	return c.JSON(http.StatusOK, map[string]string{
		"message": "user deleted successfully",
	})
}
