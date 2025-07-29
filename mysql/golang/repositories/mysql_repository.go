package repositories

import (
	"context"
	modelentities "note-golang-mysql/models/entities"

	"github.com/jmoiron/sqlx"
)

type MysqlRepository interface {
	Create(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, lastInsertedId int64, err error)
	Get(db *sqlx.DB, ctx context.Context, id int) (test1 modelentities.Test1, err error)
	Update(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error)
	Delete(tx *sqlx.Tx, ctx context.Context, id int) (rowsAffected int64, err error)
}

type mysqlRepository struct {
}

func NewMysqlRepository() MysqlRepository {
	return &mysqlRepository{}
}

func (repository *mysqlRepository) Create(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, lastInsertedId int64, err error) {
	result, err := tx.ExecContext(ctx, `INSERT INTO test1 (test) VALUES (?);`, test1.Test)
	if err != nil {
		return
	}
	rowsAffected, err = result.RowsAffected()
	if err != nil {
		return
	}
	lastInsertedId, err = result.LastInsertId()
	if err != nil {
		return
	}
	return
}

func (repository *mysqlRepository) Get(db *sqlx.DB, ctx context.Context, id int) (test1 modelentities.Test1, err error) {
	// err = db.GetContext(ctx, &user, `SELECT id, email, password FROM users WHERE id = ?;`, user.Id)
	// fmt.Println("test1.Id:", test1.Id)
	err = db.GetContext(ctx, &test1, `SELECT id, test FROM test1 WHERE id = ?;`, id)
	return
}

func (repository *mysqlRepository) Update(tx *sqlx.Tx, ctx context.Context, test1 modelentities.Test1) (rowsAffected int64, err error) {
	result, err := tx.ExecContext(ctx, `UPDATE test1 SET test = ? WHERE id = ?;`, test1.Test, test1.Id)
	if err != nil {
		return
	}
	return result.RowsAffected()
}

func (repository *mysqlRepository) Delete(tx *sqlx.Tx, ctx context.Context, id int) (rowsAffected int64, err error) {
	result, err := tx.ExecContext(ctx, `DELETE FROM test1 WHERE id = ?;`, id)
	if err != nil {
		return
	}
	return result.RowsAffected()
}
