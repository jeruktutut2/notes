package repositories

import (
	"context"
	modelentities "note-golang-fiberv3-timeout/models/entities"

	"github.com/jmoiron/sqlx"
)

type Test1Repository interface {
	Sleep(tx *sqlx.Tx, ctx context.Context, second int) (result string, err error)
	SleepWithDb(db *sqlx.DB, ctx context.Context, second int) (result string, err error)
	Create(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error)
	CreateWithDb(db *sqlx.DB, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error)
}

type test1Repository struct {
}

func NewTest1Repository() Test1Repository {
	return &test1Repository{}
}

func (repository *test1Repository) Sleep(tx *sqlx.Tx, ctx context.Context, second int) (result string, err error) {
	err = tx.GetContext(ctx, &result, `SELECT PG_SLEEP($1);`, second)
	return
}

func (repository *test1Repository) SleepWithDb(db *sqlx.DB, ctx context.Context, second int) (result string, err error) {
	err = db.GetContext(ctx, &result, `SELECT PG_SLEEP($1);`, second)
	return
}

func (repository *test1Repository) Create(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error) {
	result, err := tx.ExecContext(ctx, `INSERT INTO test1(test) VALUES($1);`, test1.Test)
	if err != nil {
		return
	}
	return result.RowsAffected()
}

func (repository *test1Repository) CreateWithDb(db *sqlx.DB, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error) {
	result, err := db.ExecContext(ctx, `INSERT INTO test1(test) VALUES($1);`, test1.Test)
	if err != nil {
		return
	}
	return result.RowsAffected()
}
