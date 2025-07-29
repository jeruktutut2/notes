package repositories

import (
	"context"

	modelentities "note-golang-postgresql/models/entities"

	"github.com/jmoiron/sqlx"
)

type PostgresRepository interface {
	Create(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (id int, err error)
	Get(db *sqlx.DB, ctx context.Context, id int) (test1 modelentities.Test1, err error)
	Update(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error)
	Delete(tx *sqlx.Tx, ctx context.Context, id int) (rowsAffected int64, err error)
}

type postgresRepository struct {
}

func NewPostgresRepository() PostgresRepository {
	return &postgresRepository{}
}

func (repository *postgresRepository) Create(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (id int, err error) {
	err = tx.GetContext(ctx, &id, `INSERT INTO test1 (test) VALUES ($1) RETURNING id;`, test1.Test)
	return
}

func (repository *postgresRepository) Get(db *sqlx.DB, ctx context.Context, id int) (test1 modelentities.Test1, err error) {
	err = db.GetContext(ctx, &test1, `SELECT id, test FROM test1 WHERE id = $1;`, id)
	return
}

func (repository *postgresRepository) Update(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error) {
	result, err := tx.ExecContext(ctx, `UPDATE test1 SET test = $1 WHERE id = $2;`, test1.Test, test1.Id)
	if err != nil {
		return
	}
	return result.RowsAffected()
}

func (repository *postgresRepository) Delete(tx *sqlx.Tx, ctx context.Context, id int) (rowsAffected int64, err error) {
	result, err := tx.ExecContext(ctx, `DELETE FROM test1 WHERE id = $1;`, id)
	if err != nil {
		return
	}
	return result.RowsAffected()
}
