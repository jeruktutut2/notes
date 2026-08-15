package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	_ "github.com/lib/pq"
)

type Note struct {
	ID        int       `json:"id"`
	Title     string    `json:"title"`
	Content   string    `json:"content"`
	CreatedAt time.Time `json:"created_at"`
}

type NodeStatus struct {
	SiteName     string `json:"site_name"`
	DatabaseHost string `json:"database_host"`
	IsInRecovery bool   `json:"is_in_recovery"` // true = Standby DRC, false = Primary DC
	DBStatus     string `json:"db_status"`
	Timestamp    string `json:"timestamp"`
}

var db *sql.DB

func initDB() {
	dbHost := getEnv("DB_HOST", "localhost")
	dbPort := getEnv("DB_PORT", "5432")
	dbUser := getEnv("DB_USER", "postgres")
	dbPass := getEnv("DB_PASSWORD", "secret")
	dbName := getEnv("DB_NAME", "dcdrc_db")

	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable connect_timeout=5",
		dbHost, dbPort, dbUser, dbPass, dbName)

	var err error
	for i := 1; i <= 10; i++ {
		db, err = sql.Open("postgres", dsn)
		if err == nil {
			err = db.Ping()
			if err == nil {
				log.Printf("Successfully connected to PostgreSQL at %s:%s", dbHost, dbPort)
				break
			}
		}
		log.Printf("[%d/10] Waiting for PostgreSQL at %s:%s... error: %v", i, dbHost, dbPort, err)
		time.Sleep(2 * time.Second)
	}

	if err != nil {
		log.Printf("Warning: Could not ping database at startup: %v", err)
		return
	}

	// Create table if not exists (only if Primary)
	var inRecovery bool
	_ = db.QueryRow("SELECT pg_is_in_recovery()").Scan(&inRecovery)
	if !inRecovery {
		createTableQuery := `
		CREATE TABLE IF NOT EXISTS notes (
			id SERIAL PRIMARY KEY,
			title VARCHAR(255) NOT NULL,
			content TEXT NOT NULL,
			created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
		);`
		if _, err := db.Exec(createTableQuery); err != nil {
			log.Printf("Error creating table: %v", err)
		} else {
			log.Println("Database schema initialized successfully.")
		}
	}
}

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}

func checkDBStatus() (bool, error) {
	if db == nil {
		return false, fmt.Errorf("database connection nil")
	}
	var inRecovery bool
	err := db.QueryRow("SELECT pg_is_in_recovery()").Scan(&inRecovery)
	return inRecovery, err
}

func main() {
	e := echo.New()

	// Middlewares Echo v5
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// Initialize DB Connection
	initDB()

	siteName := getEnv("SITE_NAME", "UNKNOWN_SITE")

	// Routes
	e.GET("/", func(c echo.Context) error {
		inRecovery, err := checkDBStatus()
		dbState := "Primary (Read-Write)"
		if err != nil {
			dbState = fmt.Sprintf("Error: %v", err)
		} else if inRecovery {
			dbState = "Standby (Read-Only DRC)"
		}

		htmlContent := fmt.Sprintf(`
		<!DOCTYPE html>
		<html>
		<head>
			<title>DC DRC Echo v5 Service - %s</title>
			<style>
				body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
				.card { background: #1e293b; border-radius: 12px; padding: 24px; max-width: 600px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
				.badge { display: inline-block; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
				.badge-dc { background: #10b981; color: #022c22; }
				.badge-drc { background: #f59e0b; color: #451a03; }
				h1 { margin-top: 0; }
				code { background: #334155; padding: 2px 6px; border-radius: 4px; }
			</style>
		</head>
		<body>
			<div class="card">
				<h1>🏛️ Data Center Demo API (Echo v5)</h1>
				<p>Active Service Node: <strong>%s</strong></p>
				<p>Database Status: <span class="badge %s">%s</span></p>
				<hr style="border-color: #334155; margin: 20px 0;" />
				<h3>API Endpoints:</h3>
				<ul>
					<li><code>GET /health</code> - Health Check Endpoint</li>
					<li><code>GET /api/notes</code> - Read Notes List</li>
					<li><code>POST /api/notes</code> - Create Note (Requires Primary DC)</li>
				</ul>
			</div>
		</body>
		</html>
		`, siteName, siteName, func() string {
			if inRecovery {
				return "badge-drc"
			}
			return "badge-dc"
		}(), dbState)

		return c.HTML(http.StatusOK, htmlContent)
	})

	// Healthcheck endpoint for HAProxy/GSLB
	e.GET("/health", func(c echo.Context) error {
		inRecovery, err := checkDBStatus()
		if err != nil {
			return c.JSON(http.StatusServiceUnavailable, map[string]interface{}{
				"status":    "DOWN",
				"site":      siteName,
				"error":     err.Error(),
				"timestamp": time.Now().Format(time.RFC3339),
			})
		}

		return c.JSON(http.StatusOK, NodeStatus{
			SiteName:     siteName,
			DatabaseHost: getEnv("DB_HOST", "localhost"),
			IsInRecovery: inRecovery,
			DBStatus:     "UP",
			Timestamp:    time.Now().Format(time.RFC3339),
		})
	})

	// GET /api/notes
	e.GET("/api/notes", func(c echo.Context) error {
		if db == nil {
			return c.JSON(http.StatusServiceUnavailable, map[string]string{"error": "Database unavailable"})
		}

		rows, err := db.Query("SELECT id, title, content, created_at FROM notes ORDER BY id DESC LIMIT 50")
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}
		defer rows.Close()

		var notes []Note
		for rows.Next() {
			var n Note
			if err := rows.Scan(&n.ID, &n.Title, &n.Content, &n.CreatedAt); err != nil {
				return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
			}
			notes = append(notes, n)
		}

		inRecovery, _ := checkDBStatus()
		return c.JSON(http.StatusOK, map[string]interface{}{
			"site":           siteName,
			"is_in_recovery": inRecovery,
			"total":          len(notes),
			"data":           notes,
		})
	})

	// POST /api/notes
	e.POST("/api/notes", func(c echo.Context) error {
		if db == nil {
			return c.JSON(http.StatusServiceUnavailable, map[string]string{"error": "Database unavailable"})
		}

		inRecovery, err := checkDBStatus()
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}

		if inRecovery {
			return c.JSON(http.StatusForbidden, map[string]string{
				"error":   "Read-Only Replica (DRC Standby)",
				"message": "Cannot perform WRITE operation on DRC Standby node while in Read-Only mode.",
			})
		}

		var req struct {
			Title   string `json:"title"`
			Content string `json:"content"`
		}

		if err := c.Bind(&req); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid payload"})
		}

		if req.Title == "" {
			req.Title = fmt.Sprintf("Note created at %s", time.Now().Format("15:04:05"))
		}
		if req.Content == "" {
			req.Content = fmt.Sprintf("Sample content written to %s (Echo v5)", siteName)
		}

		var newID int
		err = db.QueryRow("INSERT INTO notes (title, content) VALUES ($1, $2) RETURNING id", req.Title, req.Content).Scan(&newID)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}

		return c.JSON(http.StatusCreated, map[string]interface{}{
			"message": "Note created successfully",
			"id":      newID,
			"site":    siteName,
		})
	})

	port := getEnv("PORT", "1323")
	log.Printf("Starting Golang Echo v5 Service [%s] on port :%s", siteName, port)
	log.Fatal(e.Start(":" + port))
}
