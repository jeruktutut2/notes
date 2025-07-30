package repositories

import (
	"context"
	modelentities "timeout/models/entities"

	"github.com/jmoiron/sqlx"
)

type Test3Repository interface {
	Sleep(tx *sqlx.Tx, ctx context.Context, second int) (result string, err error)
	SleepWithDb(db *sqlx.DB, ctx context.Context, second int) (result string, err error)
	Create(tx *sqlx.Tx, ctx context.Context, test3 modelentities.Test3) (rowsAffected int64, err error)
	CreateWithDb(db *sqlx.DB, ctx context.Context, test3 modelentities.Test3) (rowsAffected int64, err error)
}

type test3Repository struct {
}

func NewTest3Repository() Test3Repository {
	return &test3Repository{}
}

func (repository *test3Repository) Sleep(tx *sqlx.Tx, ctx context.Context, second int) (result string, err error) {
	err = tx.GetContext(ctx, &result, `SELECT PG_SLEEP($1);`, second)
	return
}

func (repository *test3Repository) SleepWithDb(db *sqlx.DB, ctx context.Context, second int) (result string, err error) {
	err = db.GetContext(ctx, &result, `SELECT PG_SLEEP($1);`, second)
	return
}

func (repository *test3Repository) Create(tx *sqlx.Tx, ctx context.Context, test3 modelentities.Test3) (rowsAffected int64, err error) {
	result, err := tx.ExecContext(ctx, `INSERT INTO test3(test) VALUES($1);`, test3.Test)
	if err != nil {
		return
	}
	return result.RowsAffected()
}

func (repository *test3Repository) CreateWithDb(db *sqlx.DB, ctx context.Context, test3 modelentities.Test3) (rowsAffected int64, err error) {
	result, err := db.ExecContext(ctx, `INSERT INTO test3(test) VALUES($1);`, test3.Test)
	if err != nil {
		return
	}
	return result.RowsAffected()
}
