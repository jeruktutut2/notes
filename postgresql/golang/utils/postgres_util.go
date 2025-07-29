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
	Close(host string, port string)
	CommitOrRollback(tx *sqlx.Tx, err error) error
}

type postgresUtil struct {
	db *sqlx.DB
}

func NewPostgresUtil(host string, username string, password string, database string, port string, applicationName string, maxOpenConnection int, maxIdleConnection int, connectionMaxIdletime int, connectionMaxLifetime int) PostgresUtil {
	println(time.Now().String(), "postgres: connecting to", host, ":", port)
	db, err := sqlx.Connect("postgres", "user="+username+" dbname="+database+" sslmode=disable password="+password+" host="+host+" port="+port+" application_name="+applicationName)
	if err != nil {
		log.Fatalln("postgres: error when connecting to:", err)
	}

	db.SetMaxOpenConns(maxOpenConnection)
	db.SetMaxIdleConns(maxIdleConnection)
	db.SetConnMaxLifetime(time.Duration(connectionMaxIdletime) * time.Minute)
	db.SetConnMaxLifetime(time.Duration(connectionMaxLifetime) * time.Minute)
	println(time.Now().String(), "postgres: connected to", host, ":", port)

	println(time.Now().String(), "postgres: pinging to", host, ":", port)
	err = db.Ping()
	if err != nil {
		log.Fatalln("postgres: error when pinging to:", err)
	}
	println(time.Now().String(), "postgres: pinged to", host, ":", port)

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

func (util *postgresUtil) Close(host string, port string) {
	println(time.Now().String(), "postgres: closing to", host, ":", port)
	err := util.db.Close()
	if err != nil {
		log.Fatalln("postgres: error when closing to:", err)
	}
	println(time.Now().String(), "postgres: closed to", host, ":", port)
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
