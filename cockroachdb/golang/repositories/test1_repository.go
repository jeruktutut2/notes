package repositories

import (
	"context"
	modelentities "note-golang-cockroachdb/models/entities"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Test1Repository interface {
	Create(tx pgx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error)
	GetById(pool *pgxpool.Pool, ctx context.Context, id uuid.UUID) (test1 modelentities.Test1, err error)
	GetAll(pool *pgxpool.Pool, ctx context.Context) (test1s []modelentities.Test1, err error)
	Update(tx pgx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error)
	Delete(tx pgx.Tx, ctx context.Context, id uuid.UUID) (rowsAffected int64, err error)
}

type test1Repository struct {
}

func NewTest1Repository() Test1Repository {
	return &test1Repository{}
}

func (repository *test1Repository) Create(tx pgx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error) {
	result, err := tx.Exec(ctx, "INSERT INTO test1(id, test) VALUES($1, $2);", test1.Id, test1.Test)
	if err != nil {
		return
	}
	rowsAffected = result.RowsAffected()
	return
}

func (repository *test1Repository) GetById(pool *pgxpool.Pool, ctx context.Context, id uuid.UUID) (test1 modelentities.Test1, err error) {
	err = pool.QueryRow(ctx, "SELECT id, test FROM test1 WHERE id = $1;", id).Scan(&test1.Id, &test1.Test)
	return
}

func (repository *test1Repository) GetAll(pool *pgxpool.Pool, ctx context.Context) (test1s []modelentities.Test1, err error) {
	rows, err := pool.Query(ctx, "SELECT id, test FROM test1;")
	if err != nil {
		return
	}
	defer rows.Close()

	for rows.Next() {
		var test1 modelentities.Test1
		err = rows.Scan(&test1.Id, &test1.Test)
		if err != nil {
			test1s = []modelentities.Test1{}
			return
		}
		test1s = append(test1s, test1)
	}
	return
}

func (repository *test1Repository) Update(tx pgx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error) {
	result, err := tx.Exec(ctx, "UPDATE test1 SET test = $1 WHERE id = $2;", test1.Test, test1.Id)
	if err != nil {
		return
	}
	rowsAffected = result.RowsAffected()
	return
}

func (repository *test1Repository) Delete(tx pgx.Tx, ctx context.Context, id uuid.UUID) (rowsAffected int64, err error) {
	result, err := tx.Exec(ctx, "DELETE FROM test1 WHERE id = $1;", id)
	if err != nil {
		return
	}
	rowsAffected = result.RowsAffected()
	return
}
