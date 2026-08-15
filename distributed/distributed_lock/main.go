package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"strconv"

	"distributed_lock/internal/lock"
	"distributed_lock/internal/service"

	"github.com/jmoiron/sqlx"
	"github.com/labstack/echo/v5"
	_ "github.com/lib/pq"
	"github.com/redis/go-redis/v9"
)

type WithdrawRequest struct {
	AccountID int     `json:"account_id"`
	Amount    float64 `json:"amount"`
}

type ResetRequest struct {
	AccountID int     `json:"account_id"`
	Balance   float64 `json:"balance"`
}

func main() {
	ctx := context.Background()

	// 1. Connect PostgreSQL
	dbDSN := "host=localhost port=5432 user=postgres password=postgrespassword dbname=distlock_db sslmode=disable"
	db, err := sqlx.Connect("postgres", dbDSN)
	if err != nil {
		log.Fatalf("Gagal terhubung ke PostgreSQL: %v\n(Pastikan docker compose up -d sudah berjalan)", err)
	}
	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(10)

	// 2. Connect Redis
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})
	if err := rdb.Ping(ctx).Err(); err != nil {
		log.Fatalf("Gagal terhubung ke Redis: %v\n(Pastikan docker compose up -d sudah berjalan)", err)
	}

	// 3. Init Lock Managers & Wallet Service
	redisLockMgr := lock.NewRedisLockManager(rdb)
	pgLockMgr := lock.NewPGLockManager(db)

	walletSvc := service.NewWalletService(db, redisLockMgr, pgLockMgr)
	if err := walletSvc.InitSchema(ctx); err != nil {
		log.Fatalf("Gagal inisialisasi schema DB: %v", err)
	}

	// 4. Init Echo v5 App
	e := echo.New()

	// Handler Reset Saldo
	e.POST("/reset", func(c *echo.Context) error {
		var req ResetRequest
		if err := c.Bind(&req); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		}
		if req.AccountID <= 0 {
			req.AccountID = 1
		}
		if req.Balance <= 0 {
			req.Balance = 1000000 // Default 1 Juta
		}

		if err := walletSvc.ResetBalance(c.Request().Context(), req.AccountID, req.Balance); err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"message":    "Saldo berhasil di-reset",
			"account_id": req.AccountID,
			"balance":    req.Balance,
		})
	})

	// Handler Cek Saldo
	e.GET("/balance", func(c *echo.Context) error {
		accountIDStr := c.QueryParam("account_id")
		accountID, _ := strconv.Atoi(accountIDStr)
		if accountID <= 0 {
			accountID = 1
		}

		balance, err := walletSvc.GetBalance(c.Request().Context(), accountID)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"account_id": accountID,
			"balance":    balance,
		})
	})

	// 1. Skenario Tanpa Lock
	e.POST("/withdraw/no-lock", func(c *echo.Context) error {
		var req WithdrawRequest
		if err := c.Bind(&req); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		}
		newBalance, err := walletSvc.WithdrawNoLock(c.Request().Context(), req.AccountID, req.Amount)
		if err != nil {
			return c.JSON(http.StatusConflict, map[string]string{"status": "REJECTED", "error": err.Error()})
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"status":      "SUCCESS",
			"new_balance": newBalance,
		})
	})

	// 2. Skenario Redis Distributed Lock + Context Timeout Protection
	e.POST("/withdraw/redis-lock", func(c *echo.Context) error {
		var req WithdrawRequest
		if err := c.Bind(&req); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		}
		newBalance, err := walletSvc.WithdrawRedisLock(c.Request().Context(), req.AccountID, req.Amount)
		if err != nil {
			if err == service.ErrLockAcquireFailed {
				return c.JSON(http.StatusLocked, map[string]string{"status": "LOCKED", "error": err.Error()})
			}
			return c.JSON(http.StatusBadRequest, map[string]string{"status": "REJECTED", "error": err.Error()})
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"status":      "SUCCESS",
			"new_balance": newBalance,
		})
	})

	// 2b. Skenario Redis Watchdog Lock (Auto-Renewal TTL)
	e.POST("/withdraw/redis-watchdog-lock", func(c *echo.Context) error {
		var req WithdrawRequest
		if err := c.Bind(&req); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		}
		newBalance, err := walletSvc.WithdrawRedisWatchdogLock(c.Request().Context(), req.AccountID, req.Amount)
		if err != nil {
			if err == service.ErrLockAcquireFailed {
				return c.JSON(http.StatusLocked, map[string]string{"status": "LOCKED", "error": err.Error()})
			}
			return c.JSON(http.StatusBadRequest, map[string]string{"status": "REJECTED", "error": err.Error()})
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"status":      "SUCCESS",
			"new_balance": newBalance,
		})
	})

	// 3. Skenario PG Session Advisory Lock
	e.POST("/withdraw/pg-session-lock", func(c *echo.Context) error {
		var req WithdrawRequest
		if err := c.Bind(&req); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		}
		newBalance, err := walletSvc.WithdrawPGSessionLock(c.Request().Context(), req.AccountID, req.Amount)
		if err != nil {
			if err == service.ErrLockAcquireFailed {
				return c.JSON(http.StatusLocked, map[string]string{"status": "LOCKED", "error": err.Error()})
			}
			return c.JSON(http.StatusBadRequest, map[string]string{"status": "REJECTED", "error": err.Error()})
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"status":      "SUCCESS",
			"new_balance": newBalance,
		})
	})

	// 4. Skenario PG Transaction Advisory Lock
	e.POST("/withdraw/pg-xact-lock", func(c *echo.Context) error {
		var req WithdrawRequest
		if err := c.Bind(&req); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		}
		newBalance, err := walletSvc.WithdrawPGTxLock(c.Request().Context(), req.AccountID, req.Amount)
		if err != nil {
			if err == service.ErrLockAcquireFailed {
				return c.JSON(http.StatusLocked, map[string]string{"status": "LOCKED", "error": err.Error()})
			}
			return c.JSON(http.StatusBadRequest, map[string]string{"status": "REJECTED", "error": err.Error()})
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"status":      "SUCCESS",
			"new_balance": newBalance,
		})
	})

	fmt.Println("🚀 Server Go Echo v5 berjalan di http://localhost:8080")
	if err := e.Start(":8080"); err != nil {
		log.Fatalf("Server stopped: %v", err)
	}
}
