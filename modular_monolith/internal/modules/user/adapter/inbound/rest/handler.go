package rest

import (
	"strconv"

	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/user/domain"
	"github.com/example/modular-monolith/internal/shared/response"
)

// Handler is the INBOUND ADAPTER for HTTP.
// It depends on domain.UserService (inbound port), not on a concrete service implementation.
type Handler struct {
	service domain.UserService
}

// NewHandler creates a new user HTTP handler.
func NewHandler(service domain.UserService) *Handler {
	return &Handler{service: service}
}

// Create handles POST /users
func (h *Handler) Create(c *echo.Context) error {
	var req CreateUserRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}
	if msg := req.Validate(); msg != "" {
		return response.BadRequest(c, msg)
	}

	user, err := h.service.Create(c.Request().Context(), req.Name, req.Email, req.Password)
	if err != nil {
		return response.InternalError(c, err.Error())
	}
	return response.Created(c, toUserResponse(user))
}

// GetByID handles GET /users/:id
func (h *Handler) GetByID(c *echo.Context) error {
	id := c.Param("id")
	user, err := h.service.GetByID(c.Request().Context(), id)
	if err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, toUserResponse(user))
}

// List handles GET /users
func (h *Handler) List(c *echo.Context) error {
	page, _ := strconv.Atoi(c.QueryParam("page"))
	limit, _ := strconv.Atoi(c.QueryParam("limit"))

	users, total, err := h.service.List(c.Request().Context(), page, limit)
	if err != nil {
		return response.InternalError(c, err.Error())
	}

	if page < 1 {
		page = 1
	}
	if limit < 1 {
		limit = 10
	}
	return response.Paginated(c, toUserListResponse(users), total, page, limit)
}

// Update handles PUT /users/:id
func (h *Handler) Update(c *echo.Context) error {
	id := c.Param("id")
	var req UpdateUserRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}

	user, err := h.service.Update(c.Request().Context(), id, req.Name, req.Email)
	if err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, toUserResponse(user))
}

// Delete handles DELETE /users/:id
func (h *Handler) Delete(c *echo.Context) error {
	id := c.Param("id")
	if err := h.service.Delete(c.Request().Context(), id); err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, map[string]string{"message": "user deleted"})
}

// Login handles POST /users/login
func (h *Handler) Login(c *echo.Context) error {
	var req LoginRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}

	user, token, err := h.service.Login(c.Request().Context(), req.Email, req.Password)
	if err != nil {
		return response.Error(c, 401, err.Error())
	}
	return response.OK(c, &LoginResponse{
		User:  toUserResponse(user),
		Token: token,
	})
}
