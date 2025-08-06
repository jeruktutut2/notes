package utils

import (
	"context"
	"database/sql"
	"log"
	"time"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

type PostgresUtil interface {
	GetDb() *sqlx.DB
	BeginTxx(ctx context.Context, options *sql.TxOptions) (*sqlx.Tx, error)
	Close()
	CommitOrRollback(tx *sqlx.Tx, err error) error
}

type postgresUtil struct {
	db *sqlx.DB
}

func NewPostgresUtil() PostgresUtil {
	println(time.Now().String(), "postgres: connecting to localhost:5432")
	db, err := sqlx.Connect("postgres", "user=postgres dbname=test1 sslmode=disable password=12345 host=localhost port=5432 application_name=test1")
	if err != nil {
		log.Fatalln("postgres: error when connecting to:", err)
	}

	db.SetMaxOpenConns(10)
	db.SetMaxIdleConns(10)
	db.SetConnMaxLifetime(time.Duration(10) * time.Minute)
	db.SetConnMaxLifetime(time.Duration(10) * time.Minute)
	println(time.Now().String(), "postgres: connected to localhost:5432")

	println(time.Now().String(), "postgres: pinging to localhost:5432")
	err = db.Ping()
	if err != nil {
		log.Fatalln("postgres: error when pinging to:", err)
	}
	println(time.Now().String(), "postgres: pinged to localhost:5432")

	return &postgresUtil{
		db: db,
	}
}

func (util *postgresUtil) GetDb() *sqlx.DB {
	return util.db
}

func (util *postgresUtil) BeginTxx(ctx context.Context, options *sql.TxOptions) (*sqlx.Tx, error) {
	return util.db.BeginTxx(ctx, options)
}

func (util *postgresUtil) Close() {
	println(time.Now().String(), "postgres: closing to localhost:5432")
	err := util.db.Close()
	if err != nil {
		log.Fatalln("postgres: error when closing to:", err)
	}
	println(time.Now().String(), "postgres: closed to localhost:5432")
}

func (util *postgresUtil) CommitOrRollback(tx *sqlx.Tx, err error) error {
	if err == nil {
		err = tx.Commit()
		if err != nil && err != sql.ErrTxDone {
			err = tx.Rollback()
			if err != nil && err != sql.ErrTxDone {
				return err
			}
			return nil
		}
		return nil
	} else {
		err = tx.Rollback()
		if err != nil && err != sql.ErrTxDone {
			return err
		}
		return nil
	}
}
