package repositories

import (
	"context"
	modelentities "timeout/models/entities"

	"github.com/jmoiron/sqlx"
)

type Test2Repository interface {
	Sleep(tx *sqlx.Tx, ctx context.Context, second int) (result string, err error)
	SleepWithDb(db *sqlx.DB, ctx context.Context, second int) (result string, err error)
	Create(tx *sqlx.Tx, ctx context.Context, test2 modelentities.Test2) (rowsAffected int64, err error)
	CreateWithDb(db *sqlx.DB, ctx context.Context, test2 modelentities.Test2) (rowsAffected int64, err error)
}

type test2Repository struct {
}

func NewTest2Repository() Test2Repository {
	return &test2Repository{}
}

func (repository *test2Repository) Sleep(tx *sqlx.Tx, ctx context.Context, second int) (result string, err error) {
	err = tx.GetContext(ctx, &result, `SELECT PG_SLEEP($1);`, second)
	return
}

func (repository *test2Repository) SleepWithDb(db *sqlx.DB, ctx context.Context, second int) (result string, err error) {
	err = db.GetContext(ctx, &result, `SELECT PG_SLEEP($1);`, second)
	return
}

func (repository *test2Repository) Create(tx *sqlx.Tx, ctx context.Context, test2 modelentities.Test2) (rowsAffected int64, err error) {
	result, err := tx.ExecContext(ctx, `INSERT INTO test2(test) VALUES($1);`, test2.Test)
	if err != nil {
		return
	}
	return result.RowsAffected()
}

func (repository *test2Repository) CreateWithDb(db *sqlx.DB, ctx context.Context, test2 modelentities.Test2) (rowsAffected int64, err error) {
	result, err := db.ExecContext(ctx, `INSERT INTO test2(test) VALUES($1);`, test2.Test)
	if err != nil {
		return
	}
	return result.RowsAffected()
}
