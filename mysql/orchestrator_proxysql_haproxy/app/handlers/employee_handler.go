package handlers

import (
	"net/http"

	"github.com/labstack/echo/v5"
	"orchestrator_proxysql_haproxy/app/db"
	"orchestrator_proxysql_haproxy/app/models"
)

type EmployeeHandler struct {
	Client *db.Client
}

func NewEmployeeHandler(client *db.Client) *EmployeeHandler {
	return &EmployeeHandler{Client: client}
}

// GET /api/employees - Normal Select (Routed via HAProxy -> ProxySQL to Replicas)
func (h *EmployeeHandler) GetEmployees(c *echo.Context) error {
	ctx := c.Request().Context()
	query := "SELECT id, name, position, created_at, @@hostname AS served_by FROM employees ORDER BY id ASC;"

	rows, err := h.Client.DB.QueryContext(ctx, query)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]any{
			"error": "Failed to fetch employees: " + err.Error(),
		})
	}
	defer rows.Close()

	var employees []models.Employee
	for rows.Next() {
		var emp models.Employee
		if err := rows.Scan(&emp.ID, &emp.Name, &emp.Position, &emp.CreatedAt, &emp.ServedBy); err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]any{
				"error": "Failed to scan employee row: " + err.Error(),
			})
		}
		employees = append(employees, emp)
	}

	return c.JSON(http.StatusOK, map[string]any{
		"data":  employees,
		"count": len(employees),
	})
}

// POST /api/employees - Normal Insert (Routed via HAProxy -> ProxySQL to Master)
func (h *EmployeeHandler) CreateEmployee(c *echo.Context) error {
	ctx := c.Request().Context()
	var req models.CreateEmployeeRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]any{
			"error": "Invalid request payload",
		})
	}

	if req.Name == "" || req.Position == "" {
		return c.JSON(http.StatusBadRequest, map[string]any{
			"error": "Name and position are required",
		})
	}

	query := "INSERT INTO employees (name, position) VALUES (?, ?);"
	res, err := h.Client.DB.ExecContext(ctx, query, req.Name, req.Position)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]any{
			"error": "Failed to insert employee: " + err.Error(),
		})
	}

	id, _ := res.LastInsertId()
	return c.JSON(http.StatusCreated, map[string]any{
		"message":  "Employee created successfully (Routed via HAProxy & ProxySQL)",
		"id":       id,
		"name":     req.Name,
		"position": req.Position,
	})
}

// POST /api/employees/transaction - Explicit Transaction (Routed via HAProxy -> ProxySQL Master)
func (h *EmployeeHandler) ExecuteTransaction(c *echo.Context) error {
	ctx := c.Request().Context()
	var req models.TransactionRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]any{
			"error": "Invalid request payload",
		})
	}

	if req.Name == "" {
		req.Name = "Transaction Employee"
	}
	if req.Position == "" {
		req.Position = "Transaction Role"
	}

	tx, err := h.Client.DB.BeginTx(ctx, nil)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]any{
			"error": "Failed to start transaction: " + err.Error(),
		})
	}
	defer tx.Rollback()

	var count int
	var masterHost string
	err = tx.QueryRowContext(ctx, "SELECT COUNT(*), @@hostname FROM employees;").Scan(&count, &masterHost)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]any{
			"error": "Failed to read inside transaction: " + err.Error(),
		})
	}

	insertQuery := "INSERT INTO employees (name, position) VALUES (?, ?);"
	res, err := tx.ExecContext(ctx, insertQuery, req.Name, req.Position)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]any{
			"error": "Failed to insert inside transaction: " + err.Error(),
		})
	}

	if err := tx.Commit(); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]any{
			"error": "Failed to commit transaction: " + err.Error(),
		})
	}

	id, _ := res.LastInsertId()
	return c.JSON(http.StatusCreated, map[string]any{
		"message":               "Transaction executed & committed via HAProxy -> ProxySQL Master",
		"inserted_id":           id,
		"previous_record_count": count,
		"executed_on_host":      masterHost,
	})
}

// GET /api/health - Health check
func (h *EmployeeHandler) HealthCheck(c *echo.Context) error {
	if err := h.Client.DB.Ping(); err != nil {
		return c.JSON(http.StatusServiceUnavailable, map[string]any{
			"status": "DOWN",
			"error":  err.Error(),
		})
	}
	return c.JSON(http.StatusOK, map[string]any{
		"status": "UP",
		"db":     "Connected via HAProxy -> ProxySQL",
	})
}
