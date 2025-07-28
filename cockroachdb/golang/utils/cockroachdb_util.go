package utils

import (
	"context"
	"fmt"
	"log"
	"strings"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type CockroachDbUtil interface {
	GetDb() *pgxpool.Pool
	BeginTx(ctx context.Context, txOptions pgx.TxOptions) (pgx.Tx, error)
	Close()
	CommitOrRollback(tx pgx.Tx, ctx context.Context, err error) error
}

type cockroachDbUtil struct {
	pool *pgxpool.Pool
}

func NewCockroachDbutil() CockroachDbUtil {
	ctx := context.Background()
	config, err := pgxpool.ParseConfig("postgres://root@localhost:26260/test1?sslmode=disable")
	if err != nil {
		log.Fatalln("error when parsing configuration to localhost:26260:", err)
	}
	config.MaxConns = 10
	config.MinConns = 2
	config.MaxConnLifetime = time.Minute * 10
	config.MaxConnIdleTime = time.Minute * 5
	config.HealthCheckPeriod = time.Minute * 10

	pool, err := pgxpool.NewWithConfig(ctx, config)
	if err != nil {
		log.Fatalln("error when connecting to localhost:26260:", err)
	}

	err = pool.Ping(ctx)
	if err != nil {
		log.Fatalln("error when pinging to localhost:26260:", err)
	}

	// to profiling (monitor total open conns, idle, busy, etc)
	stats := pool.Stat()
	fmt.Println("TotalConns:", stats.TotalConns())
	fmt.Println("IdleConns :", stats.IdleConns())
	fmt.Println("Acquired  :", stats.AcquiredConns())

	return &cockroachDbUtil{
		pool: pool,
	}
}

func (util *cockroachDbUtil) GetDb() *pgxpool.Pool {
	return util.pool
}

func (util *cockroachDbUtil) BeginTx(ctx context.Context, txOptions pgx.TxOptions) (pgx.Tx, error) {
	return util.pool.BeginTx(ctx, txOptions)
}

func (util *cockroachDbUtil) Close() {
	util.pool.Close()
}

func (util *cockroachDbUtil) CommitOrRollback(tx pgx.Tx, ctx context.Context, err error) error {
	if err == nil {
		err = tx.Commit(ctx)
		if err != nil && !strings.Contains(err.Error(), "transaction has already been committed or rolled back") {
			err = tx.Rollback(ctx)
			if err != nil && !strings.Contains(err.Error(), "transaction has already been committed or rolled back") {
				return err
			}
			return nil
		}
		return nil
	} else {
		err = tx.Rollback(ctx)
		if err != nil && !strings.Contains(err.Error(), "transaction has already been committed or rolled back") {
			return err
		}
		return nil
	}
}
