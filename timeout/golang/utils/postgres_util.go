package utils

import (
	"context"
	"database/sql"
	"log"
	"os"
	"strconv"
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
	println(time.Now().String(), "postgres: connecting to", os.Getenv("POSTGRES_HOST"), ":", os.Getenv("POSTGRES_PORT"))
	db, err := sqlx.Connect("postgres", "user="+os.Getenv("POSTGRES_USERNAME")+" dbname="+os.Getenv("POSTGRES_DATABASE")+" sslmode=disable password="+os.Getenv("POSTGRES_PASSWORD")+" host="+os.Getenv("POSTGRES_HOST")+" port="+os.Getenv("POSTGRES_PORT")+" application_name="+os.Getenv("POSTGRES_USERNAME"))
	if err != nil {
		log.Fatalln("postgres: error when connecting to:", err)
	}

	maxOpenConnectionEnv := os.Getenv("POSTGRES_MAX_OPEN_CONNECTION")
	maxOpenConnection, err := strconv.Atoi(maxOpenConnectionEnv)
	if err != nil {
		log.Fatalln("postgres: error when converting max open connection from string to int:", err)
	}
	db.SetMaxOpenConns(maxOpenConnection)

	maxIdleConnectionEnv := os.Getenv("POSTGRES_MAX_IDLE_CONNECTION")
	maxIdleConnection, err := strconv.Atoi(maxIdleConnectionEnv)
	if err != nil {
		log.Fatalln("postgres: error when converting max idle connection from string to int", err)
	}
	db.SetMaxIdleConns(maxIdleConnection)

	connectionMaxIdletimeEnv := os.Getenv("POSTGRES_CONNECTION_MAX_IDLETIME")
	connectionMaxIdletime, err := strconv.Atoi(connectionMaxIdletimeEnv)
	if err != nil {
		log.Fatalln("postgres: error when converting connection max idletime from string to int:", err)
	}
	db.SetConnMaxLifetime(time.Duration(connectionMaxIdletime) * time.Minute)

	connectionMaxLifetimeEnv := os.Getenv("POSTGRES_CONNECTION_MAX_LIFETIME")
	connectionMaxLifetime, err := strconv.Atoi(connectionMaxLifetimeEnv)
	if err != nil {
		log.Fatalln("postgres: error when converting connection max lifetime from string to int:", err)
	}
	db.SetConnMaxLifetime(time.Duration(connectionMaxLifetime) * time.Minute)
	println(time.Now().String(), "postgres: connected to", os.Getenv("POSTGRES_HOST"), ":", os.Getenv("POSTGRES_PORT"))

	println(time.Now().String(), "postgres: pinging to", os.Getenv("POSTGRES_HOST"), ":", os.Getenv("POSTGRES_PORT"))
	err = db.Ping()
	if err != nil {
		log.Fatalln("postgres: error when pinging to:", err)
	}
	println(time.Now().String(), "postgres: pinged to", os.Getenv("POSTGRES_HOST"), ":", os.Getenv("POSTGRES_PORT"))

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
	println(time.Now().String(), "postgres: closing to", os.Getenv("POSTGRES_HOST"))
	err := util.db.Close()
	if err != nil {
		log.Fatalln("postgres: error when closing to:", err)
	}
	println(time.Now().String(), "postgres: closed to", os.Getenv("POSTGRES_HOST"))
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
