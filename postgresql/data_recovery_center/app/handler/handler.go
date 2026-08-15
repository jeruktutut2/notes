package handler

import (
	"net/http"
	"strconv"
	"time"

	"drc-app/model"
	"drc-app/repository"

	"github.com/labstack/echo/v5"
)

type Handler struct {
	repo repository.Repository
}

func NewHandler(repo repository.Repository) *Handler {
	return &Handler{repo: repo}
}

func (h *Handler) Health(c echo.Context) error {
	ctx := c.Request().Context()
	err := h.repo.Ping(ctx)

	target := h.repo.GetActiveTarget()
	status := "UP"
	dbStatus := "CONNECTED"

	if err != nil {
		status = "DEGRADED"
		dbStatus = "DISCONNECTED"
	}

	return c.JSON(http.StatusOK, echo.Map{
		"status":        status,
		"db_status":     dbStatus,
		"active_target": target,
		"timestamp":     time.Now().Format(time.RFC3339),
	})
}

func (h *Handler) GetStatus(c echo.Context) error {
	ctx := c.Request().Context()
	res, err := h.repo.GetSystemStatus(ctx)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, model.GenericResponse{
			Success: false,
			Message: err.Error(),
		})
	}
	return c.JSON(http.StatusOK, model.GenericResponse{
		Success: true,
		Message: "System status retrieved",
		Data:    res,
	})
}

func (h *Handler) GetReplication(c echo.Context) error {
	ctx := c.Request().Context()
	res, err := h.repo.GetReplicationInfo(ctx)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, model.GenericResponse{
			Success: false,
			Message: err.Error(),
		})
	}
	return c.JSON(http.StatusOK, model.GenericResponse{
		Success: true,
		Message: "Replication info retrieved",
		Data:    res,
	})
}

func (h *Handler) CreateData(c echo.Context) error {
	var req model.CreateDataRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, model.GenericResponse{
			Success: false,
			Message: "Invalid request payload: " + err.Error(),
		})
	}

	if req.Title == "" {
		return c.JSON(http.StatusBadRequest, model.GenericResponse{
			Success: false,
			Message: "Title is required",
		})
	}

	ctx := c.Request().Context()
	item, err := h.repo.CreateData(ctx, req)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, model.GenericResponse{
			Success: false,
			Message: "Failed to create data: " + err.Error(),
		})
	}

	return c.JSON(http.StatusCreated, model.GenericResponse{
		Success: true,
		Message: "Data created successfully on " + h.repo.GetActiveTarget(),
		Data:    item,
	})
}

func (h *Handler) ListData(c echo.Context) error {
	ctx := c.Request().Context()
	items, err := h.repo.ListData(ctx)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, model.GenericResponse{
			Success: false,
			Message: err.Error(),
		})
	}
	return c.JSON(http.StatusOK, model.GenericResponse{
		Success: true,
		Message: "Data retrieved successfully",
		Data:    items,
	})
}

func (h *Handler) GetDataByID(c echo.Context) error {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		return c.JSON(http.StatusBadRequest, model.GenericResponse{
			Success: false,
			Message: "Invalid ID format",
		})
	}

	ctx := c.Request().Context()
	item, err := h.repo.GetDataByID(ctx, id)
	if err != nil {
		return c.JSON(http.StatusNotFound, model.GenericResponse{
			Success: false,
			Message: err.Error(),
		})
	}

	return c.JSON(http.StatusOK, model.GenericResponse{
		Success: true,
		Message: "Data item found",
		Data:    item,
	})
}

func (h *Handler) Failover(c echo.Context) error {
	ctx := c.Request().Context()
	start := time.Now()

	err := h.repo.SetActiveTarget("drc")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, model.GenericResponse{
			Success: false,
			Message: err.Error(),
		})
	}

	duration := int(time.Since(start).Milliseconds())

	_ = h.repo.RecordFailover(ctx, "failover", "pg-dc", "pg-drc", "API_REQUEST", duration, "Application database target switched to DRC")

	return c.JSON(http.StatusOK, model.GenericResponse{
		Success: true,
		Message: "App target switched to DRC (Recovery Center)",
		Data: echo.Map{
			"active_target": "drc",
			"duration_ms":   duration,
		},
	})
}

func (h *Handler) Failback(c echo.Context) error {
	ctx := c.Request().Context()
	start := time.Now()

	err := h.repo.SetActiveTarget("dc")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, model.GenericResponse{
			Success: false,
			Message: err.Error(),
		})
	}

	duration := int(time.Since(start).Milliseconds())

	_ = h.repo.RecordFailover(ctx, "failback", "pg-drc", "pg-dc", "API_REQUEST", duration, "Application database target restored to DC Primary")

	return c.JSON(http.StatusOK, model.GenericResponse{
		Success: true,
		Message: "App target restored to DC (Data Center Primary)",
		Data: echo.Map{
			"active_target": "dc",
			"duration_ms":   duration,
		},
	})
}

func (h *Handler) GetLogs(c echo.Context) error {
	ctx := c.Request().Context()
	logs, err := h.repo.ListDRLogs(ctx)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, model.GenericResponse{
			Success: false,
			Message: err.Error(),
		})
	}
	return c.JSON(http.StatusOK, model.GenericResponse{
		Success: true,
		Message: "DR logs retrieved",
		Data:    logs,
	})
}
