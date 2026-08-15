package response

import (
	"net/http"

	"github.com/labstack/echo/v5"
)

// APIResponse is the standard JSON response envelope.
type APIResponse struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
	Meta    *Meta       `json:"meta,omitempty"`
}

// Meta holds pagination metadata.
type Meta struct {
	Page       int   `json:"page"`
	Limit      int   `json:"limit"`
	Total      int64 `json:"total"`
	TotalPages int64 `json:"total_pages"`
}

// Success sends a successful JSON response.
func Success(c *echo.Context, status int, data interface{}) error {
	return c.JSON(status, APIResponse{
		Success: true,
		Data:    data,
	})
}

// Created sends a 201 response with the created resource.
func Created(c *echo.Context, data interface{}) error {
	return Success(c, http.StatusCreated, data)
}

// OK sends a 200 response.
func OK(c *echo.Context, data interface{}) error {
	return Success(c, http.StatusOK, data)
}

// Paginated sends a 200 response with pagination metadata.
func Paginated(c *echo.Context, data interface{}, total int64, page, limit int) error {
	totalPages := total / int64(limit)
	if total%int64(limit) != 0 {
		totalPages++
	}

	return c.JSON(http.StatusOK, APIResponse{
		Success: true,
		Data:    data,
		Meta: &Meta{
			Page:       page,
			Limit:      limit,
			Total:      total,
			TotalPages: totalPages,
		},
	})
}

// Error sends an error JSON response.
func Error(c *echo.Context, status int, message string) error {
	return c.JSON(status, APIResponse{
		Success: false,
		Message: message,
	})
}

// BadRequest sends a 400 response.
func BadRequest(c *echo.Context, message string) error {
	return Error(c, http.StatusBadRequest, message)
}

// NotFound sends a 404 response.
func NotFound(c *echo.Context, message string) error {
	return Error(c, http.StatusNotFound, message)
}

// InternalError sends a 500 response.
func InternalError(c *echo.Context, message string) error {
	return Error(c, http.StatusInternalServerError, message)
}
