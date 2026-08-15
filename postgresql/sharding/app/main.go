package main

import (
	"database/sql"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	_ "github.com/lib/pq"
)

type Map = map[string]any

type NodeInfo struct {
	NodeID   int    `json:"node_id"`
	NodeName string `json:"node_name"`
	NodePort int    `json:"node_port"`
	IsActive bool   `json:"is_active"`
	NodeRole string `json:"node_role"`
}

type NodePlacement struct {
	NodeName    string `json:"node_name"`
	TotalShards int    `json:"total_shards"`
}

type User struct {
	ID        int64     `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	Country   string    `json:"country"`
	CreatedAt time.Time `json:"created_at"`

	// Shard location information
	StoredInNode string `json:"stored_in_db_node,omitempty"`
	ShardID      int64  `json:"shard_id,omitempty"`
}

type CreateUserRequest struct {
	Name    string `json:"name"`
	Email   string `json:"email"`
	Country string `json:"country"`
}

type AnalyticsSummary struct {
	TotalUsers    int64            `json:"total_users"`
	TotalOrders   int64            `json:"total_orders"`
	CountryStats  map[string]int64 `json:"users_per_country"`
	NodePlacement []NodePlacement  `json:"node_placements"`
}

var db *sql.DB

func initDB() *sql.DB {
	host := getEnv("DB_HOST", "pgbouncer")
	port := getEnv("DB_PORT", "6432")
	user := getEnv("DB_USER", "postgres")
	password := getEnv("DB_PASSWORD", "postgrespassword")
	dbname := getEnv("DB_NAME", "citus_db")

	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)

	var database *sql.DB
	var err error

	for i := 1; i <= 10; i++ {
		database, err = sql.Open("postgres", dsn)
		if err == nil {
			err = database.Ping()
			if err == nil {
				log.Println("✅ Successfully connected to Citus Cluster via PgBouncer")
				database.SetMaxOpenConns(50)
				database.SetMaxIdleConns(10)
				database.SetConnMaxLifetime(5 * time.Minute)
				return database
			}
		}
		log.Printf("⏳ Waiting for DB connection (Attempt %d/10): %v", i, err)
		time.Sleep(3 * time.Second)
	}

	log.Fatalf("❌ Failed to connect to DB: %v", err)
	return nil
}

// Helper to query which Citus worker node & shard ID stores a specific user ID
func getShardInfoForUser(userID int64) (string, int64, error) {
	var nodeName string
	var shardID int64
	query := `
		SELECT n.nodename, p.shardid 
		FROM pg_dist_placement p 
		JOIN pg_dist_node n ON p.groupid = n.groupid 
		WHERE p.shardid = get_shard_id_for_distribution_column('users', $1::text)
		LIMIT 1
	`
	err := db.QueryRow(query, strconv.FormatInt(userID, 10)).Scan(&nodeName, &shardID)
	if err != nil {
		return "unknown", 0, err
	}
	return nodeName, shardID, nil
}

func main() {
	db = initDB()
	defer db.Close()

	e := echo.New()
	e.Use(middleware.Recover())

	// Routes
	e.GET("/health", healthCheck)
	e.GET("/nodes", getClusterNodes)
	e.POST("/users", createUser)        // Nambah single user (POST)
	e.GET("/users", getUsers)          // Select data users (GET list)
	e.GET("/users/:id", getUserByID)    // Select single user by ID (GET)
	e.POST("/seed", seedData)           // Bulk seed data
	e.GET("/analytics", getAnalytics)   // Distributed query analytics

	port := getEnv("PORT", "8080")
	log.Println("🚀 Echo v5 server starting on port :" + port)
	log.Fatal(e.Start(":" + port))
}

func healthCheck(c *echo.Context) error {
	err := db.Ping()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"status": "error", "message": err.Error()})
	}
	return c.JSON(http.StatusOK, Map{"status": "UP", "message": "Citus PgBouncer Connection Healthy (Echo v5)"})
}

// 1. PROCESS NAMBAH DATA (POST /users)
func createUser(c *echo.Context) error {
	req := new(CreateUserRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(http.StatusBadRequest, Map{"error": "Invalid JSON body"})
	}

	if req.Name == "" || req.Email == "" || req.Country == "" {
		return c.JSON(http.StatusBadRequest, Map{"error": "name, email, and country are required"})
	}

	var newID int64
	err := db.QueryRow(`INSERT INTO users (name, email, country) VALUES ($1, $2, $3) RETURNING id`, req.Name, req.Email, req.Country).Scan(&newID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}

	// Cari tahu data tersimpan di DB node mana
	nodeName, shardID, _ := getShardInfoForUser(newID)

	u := User{
		ID:           newID,
		Name:         req.Name,
		Email:        req.Email,
		Country:      req.Country,
		CreatedAt:    time.Now(),
		StoredInNode: nodeName,
		ShardID:      shardID,
	}

	return c.JSON(http.StatusCreated, Map{
		"message": "User data successfully added to sharded database",
		"data":    u,
		"sharding_info": Map{
			"stored_in_db_node": nodeName,
			"shard_id":          shardID,
			"distribution_key":  "id",
			"distribution_val":  newID,
		},
	})
}

// 2. PROCESS SELECT SINGLE DATA (GET /users/:id)
func getUserByID(c *echo.Context) error {
	idParam := c.Param("id")
	id, err := strconv.ParseInt(idParam, 10, 64)
	if err != nil {
		return c.JSON(http.StatusBadRequest, Map{"error": "Invalid user ID"})
	}

	var u User
	err = db.QueryRow(`SELECT id, name, email, country, created_at FROM users WHERE id = $1`, id).Scan(&u.ID, &u.Name, &u.Email, &u.Country, &u.CreatedAt)
	if err == sql.ErrNoRows {
		return c.JSON(http.StatusNotFound, Map{"message": "User not found"})
	} else if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}

	// Fetch shard location metadata
	nodeName, shardID, _ := getShardInfoForUser(id)
	u.StoredInNode = nodeName
	u.ShardID = shardID

	// Fetch co-located orders
	rows, err := db.Query(`SELECT id, product_name, amount, status, created_at FROM orders WHERE user_id = $1`, id)
	var orders []Map
	if err == nil {
		defer rows.Close()
		for rows.Next() {
			var orderID int64
			var prodName, status string
			var amount float64
			var createdAt time.Time
			if err := rows.Scan(&orderID, &prodName, &amount, &status, &createdAt); err == nil {
				orders = append(orders, Map{
					"order_id":     orderID,
					"product_name": prodName,
					"amount":       amount,
					"status":       status,
					"created_at":   createdAt,
				})
			}
		}
	}

	return c.JSON(http.StatusOK, Map{
		"user":   u,
		"orders": orders,
		"sharding_info": Map{
			"fetched_from_db_node": nodeName,
			"shard_id":            shardID,
		},
	})
}

// 3. PROCESS SELECT ALL DATA (GET /users)
func getUsers(c *echo.Context) error {
	limitStr := c.QueryParam("limit")
	limit := 20
	if limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 {
			limit = l
		}
	}

	rows, err := db.Query(`SELECT id, name, email, country, created_at FROM users ORDER BY id DESC LIMIT $1`, limit)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}
	defer rows.Close()

	var users []User
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.Country, &u.CreatedAt); err != nil {
			return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
		}

		// Attach node location for each user
		nodeName, shardID, _ := getShardInfoForUser(u.ID)
		u.StoredInNode = nodeName
		u.ShardID = shardID

		users = append(users, u)
	}

	return c.JSON(http.StatusOK, Map{
		"total_returned": len(users),
		"users":          users,
	})
}

func getClusterNodes(c *echo.Context) error {
	rows, err := db.Query(`SELECT nodeid, nodename, nodeport, isactive, noderole FROM pg_dist_node ORDER BY nodeid`)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}
	defer rows.Close()

	var nodes []NodeInfo
	for rows.Next() {
		var n NodeInfo
		if err := rows.Scan(&n.NodeID, &n.NodeName, &n.NodePort, &n.IsActive, &n.NodeRole); err != nil {
			return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
		}
		nodes = append(nodes, n)
	}

	placementRows, err := db.Query(`
		SELECT nodename, count(*) as total_shards 
		FROM pg_dist_placement 
		JOIN pg_dist_node ON pg_dist_placement.groupid = pg_dist_node.groupid 
		GROUP BY nodename 
		ORDER BY nodename
	`)
	var placements []NodePlacement
	if err == nil {
		defer placementRows.Close()
		for placementRows.Next() {
			var p NodePlacement
			_ = placementRows.Scan(&p.NodeName, &p.TotalShards)
			placements = append(placements, p)
		}
	}

	return c.JSON(http.StatusOK, Map{
		"active_nodes": nodes,
		"placements":   placements,
	})
}

func seedData(c *echo.Context) error {
	countStr := c.QueryParam("count")
	count := 100
	if countStr != "" {
		if c, err := strconv.Atoi(countStr); err == nil && c > 0 {
			count = c
		}
	}

	countries := []string{"Indonesia", "Singapore", "Malaysia", "Japan", "United States", "Germany"}
	products := []string{"Laptop Gaming", "Wireless Earbuds", "Mechanical Keyboard", "Monitor 4K", "Smartwatch"}

	tx, err := db.Begin()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}
	defer tx.Rollback()

	userStmt, err := tx.Prepare(`INSERT INTO users (name, email, country) VALUES ($1, $2, $3) RETURNING id`)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}
	defer userStmt.Close()

	orderStmt, err := tx.Prepare(`INSERT INTO orders (user_id, product_name, amount) VALUES ($1, $2, $3)`)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}
	defer orderStmt.Close()

	r := rand.New(rand.NewSource(time.Now().UnixNano()))

	var insertedUsers int
	for i := 1; i <= count; i++ {
		name := fmt.Sprintf("User_%d_%d", time.Now().Unix(), i)
		email := fmt.Sprintf("user_%d_%d@example.com", time.Now().Unix(), i)
		country := countries[r.Intn(len(countries))]

		var userID int64
		err := userStmt.QueryRow(name, email, country).Scan(&userID)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
		}

		numOrders := r.Intn(3) + 1
		for j := 0; j < numOrders; j++ {
			product := products[r.Intn(len(products))]
			amount := float64(r.Intn(500)+50) + 0.99
			_, err = orderStmt.Exec(userID, product, amount)
			if err != nil {
				return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
			}
		}
		insertedUsers++
	}

	if err := tx.Commit(); err != nil {
		return c.JSON(http.StatusInternalServerError, Map{"error": err.Error()})
	}

	return c.JSON(http.StatusOK, Map{
		"message": fmt.Sprintf("Successfully seeded %d sharded users and orders across Citus cluster (Echo v5)", insertedUsers),
	})
}

func getAnalytics(c *echo.Context) error {
	var totalUsers int64
	var totalOrders int64

	_ = db.QueryRow(`SELECT count(*) FROM users`).Scan(&totalUsers)
	_ = db.QueryRow(`SELECT count(*) FROM orders`).Scan(&totalOrders)

	rows, err := db.Query(`SELECT country, count(*) FROM users GROUP BY country ORDER BY count(*) DESC`)
	countryStats := make(map[string]int64)
	if err == nil {
		defer rows.Close()
		for rows.Next() {
			var country string
			var cnt int64
			if err := rows.Scan(&country, &cnt); err == nil {
				countryStats[country] = cnt
			}
		}
	}

	placementRows, err := db.Query(`
		SELECT nodename, count(*) as total_shards 
		FROM pg_dist_placement 
		JOIN pg_dist_node ON pg_dist_placement.groupid = pg_dist_node.groupid 
		GROUP BY nodename 
		ORDER BY nodename
	`)
	var placements []NodePlacement
	if err == nil {
		defer placementRows.Close()
		for placementRows.Next() {
			var p NodePlacement
			_ = placementRows.Scan(&p.NodeName, &p.TotalShards)
			placements = append(placements, p)
		}
	}

	return c.JSON(http.StatusOK, AnalyticsSummary{
		TotalUsers:    totalUsers,
		TotalOrders:   totalOrders,
		CountryStats:  countryStats,
		NodePlacement: placements,
	})
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}
