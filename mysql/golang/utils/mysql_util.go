package utils

import (
	"context"
	"database/sql"
	"log"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
)

type MysqlUtil interface {
	GetDb() *sqlx.DB
	BeginTxx(ctx context.Context, options *sql.TxOptions) (*sqlx.Tx, error)
	Close(host string, port string)
	CommitOrRollback(tx *sqlx.Tx, err error) error
}

type mysqlUtil struct {
	db *sqlx.DB
}

func NewMysqlUtil(host string, username string, password string, database string, port string, maxOpenConnection int, maxIdleConnection int, connectionMaxIdletime int, connectionMaxLifetime int) MysqlUtil {
	println(time.Now().String(), "mysql: connecting to", host, ":", port)
	db, err := sqlx.Connect("mysql", username+":"+password+"@("+host+":"+port+")/"+database)
	if err != nil {
		log.Fatalln("mysql: error when connecting to:", err)
	}
	db.SetMaxOpenConns(maxOpenConnection)
	db.SetMaxIdleConns(maxIdleConnection)
	db.SetConnMaxLifetime(time.Duration(connectionMaxIdletime) * time.Minute)
	db.SetConnMaxLifetime(time.Duration(connectionMaxLifetime) * time.Minute)
	println(time.Now().String(), "mysql: connected to", host, ":", port)

	println(time.Now().String(), "mysql: pinging to", host, ":", port)
	err = db.Ping()
	if err != nil {
		log.Fatalln("mysql: error when pinging to:", err)
	}
	println(time.Now().String(), "mysql: pinged to", host, ":", port)

	return &mysqlUtil{
		db: db,
	}
}

func (util *mysqlUtil) GetDb() *sqlx.DB {
	return util.db
}

func (util *mysqlUtil) BeginTxx(ctx context.Context, options *sql.TxOptions) (*sqlx.Tx, error) {
	return util.db.BeginTxx(ctx, options)
}

func (util *mysqlUtil) Close(host string, port string) {
	println(time.Now().String(), "mysql: closing to", host, ":", port)
	err := util.db.Close()
	if err != nil {
		log.Fatalln("mysql: error when closing to:", err)
	}
	println(time.Now().String(), "mysql: closed to", host, ":", port)
}

func (util *mysqlUtil) CommitOrRollback(tx *sqlx.Tx, err error) error {
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
