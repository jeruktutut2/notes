package handler

import (
	"log/slog"
	"net/http"
	"strconv"

	"github.com/labstack/echo/v5"

	"github.com/bsa/migration/internal/model"
	"github.com/bsa/migration/internal/repository"
)

// UserHandler menangani HTTP request untuk entitas User.
type UserHandler struct {
	repo *repository.UserRepository
}

// NewUserHandler membuat UserHandler baru.
func NewUserHandler(repo *repository.UserRepository) *UserHandler {
	return &UserHandler{repo: repo}
}

// RegisterRoutes mendaftarkan semua route untuk user.
func (h *UserHandler) RegisterRoutes(e *echo.Echo) {
	api := e.Group("/api")
	api.GET("/users", h.GetAll)
	api.GET("/users/:id", h.GetByID)
	api.POST("/users", h.Create)
	api.PUT("/users/:id", h.Update)
	api.DELETE("/users/:id", h.Delete)
}

// GetAll mengembalikan semua user.
// GET /api/users
func (h *UserHandler) GetAll(c *echo.Context) error {
	users, err := h.repo.GetAll(c.Request().Context())
	if err != nil {
		slog.Error("Gagal mengambil users", "error", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Gagal mengambil data users",
		})
	}

	// Konversi ke response
	responses := make([]*model.UserResponse, len(users))
	for i, u := range users {
		responses[i] = u.ToResponse()
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"data":  responses,
		"count": len(responses),
	})
}

// GetByID mengembalikan user berdasarkan ID.
// GET /api/users/:id
func (h *UserHandler) GetByID(c *echo.Context) error {
	id, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "ID harus berupa angka",
		})
	}

	user, err := h.repo.GetByID(c.Request().Context(), id)
	if err != nil {
		slog.Error("Gagal mengambil user", "error", err, "id", id)
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": err.Error(),
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"data": user.ToResponse(),
	})
}

// Create membuat user baru.
// POST /api/users
func (h *UserHandler) Create(c *echo.Context) error {
	req := new(model.CreateUserRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Format request tidak valid",
		})
	}

	// Validasi sederhana
	if req.Username == "" || req.Password == "" || req.Email == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "username, password, dan email wajib diisi",
		})
	}

	user, err := h.repo.Create(c.Request().Context(), req)
	if err != nil {
		slog.Error("Gagal membuat user", "error", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Gagal membuat user: " + err.Error(),
		})
	}

	slog.Info("User berhasil dibuat", "id", user.ID, "username", user.Username)

	return c.JSON(http.StatusCreated, map[string]interface{}{
		"data":    user.ToResponse(),
		"message": "User berhasil dibuat",
	})
}

// Update mengupdate data user.
// PUT /api/users/:id
func (h *UserHandler) Update(c *echo.Context) error {
	id, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "ID harus berupa angka",
		})
	}

	req := new(model.UpdateUserRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Format request tidak valid",
		})
	}

	user, err := h.repo.Update(c.Request().Context(), id, req)
	if err != nil {
		slog.Error("Gagal mengupdate user", "error", err, "id", id)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
	}

	slog.Info("User berhasil diupdate", "id", user.ID)

	return c.JSON(http.StatusOK, map[string]interface{}{
		"data":    user.ToResponse(),
		"message": "User berhasil diupdate",
	})
}

// Delete menghapus user berdasarkan ID.
// DELETE /api/users/:id
func (h *UserHandler) Delete(c *echo.Context) error {
	id, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "ID harus berupa angka",
		})
	}

	if err := h.repo.Delete(c.Request().Context(), id); err != nil {
		slog.Error("Gagal menghapus user", "error", err, "id", id)
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
	}

	slog.Info("User berhasil dihapus", "id", id)

	return c.JSON(http.StatusOK, map[string]string{
		"message": "User berhasil dihapus",
	})
}
